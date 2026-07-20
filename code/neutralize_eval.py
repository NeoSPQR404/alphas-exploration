#!/usr/bin/env python3
"""Style/status filter + size&industry neutralization — evaluation layer.

For each set, recompute the EW oriented-rank composite once, then evaluate
four portfolio-construction variants on the historical (2017-25) and the
fresh 2026 window:

  raw            top-decile long over all tradable names (baseline)
  filtered       + investable universe (drop ST, <250d listed, smallest
                 30% by circ_mv — the shell/micro-cap speculative names)
  neutralized    composite residualized per-date against log(circ_mv) and
                 SW-L1 industry (Barra-lite), over all tradable names
  filt_neutral   both

Reports, per variant/window: decile curve, long-only excess-vs-universe
ann return, long-short gross ann return, and the signal's daily rank IC.

Run: python3 code/neutralize_eval.py <set_name>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import pipeline as pl            # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
Q = 10
PPY = 250 / cfg.HORIZON
SIZE_DROP = 0.30          # drop the smallest 30% by circ_mv
MIN_DAYS = 250            # exclude names listed < 250 trading days
WINDOWS = {"full": ("20170101", "20251231"), "y2026": ("20260101", "20261231")}


def neutralize(sig, size_log, ind_codes, univ):
    """Per-date residual of sig on [industry dummies, log size], within the
    universe mask. Sequential: industry-demean, then regress out size."""
    S = sig.where(univ)
    Z = size_log.where(univ)
    sv = S.to_numpy(); zv = Z.to_numpy(); iv = ind_codes.to_numpy()
    out = np.full_like(sv, np.nan)
    for t in range(sv.shape[0]):
        row, z, ic = sv[t], zv[t], iv[t]
        ok = ~np.isnan(row) & ~np.isnan(z) & ~np.isnan(ic)
        if ok.sum() < 50:
            continue
        r = row.copy()
        g = ic[ok].astype(int)
        # industry demean
        ng = int(g.max()) + 1
        gsum = np.bincount(g, weights=r[ok], minlength=ng)
        gcnt = np.bincount(g, minlength=ng)
        gmean = np.divide(gsum, gcnt, out=np.zeros_like(gsum), where=gcnt > 0)
        r[ok] = r[ok] - gmean[g]
        # regress out size (standardized)
        zz = z[ok]; zz = (zz - zz.mean())
        denom = (zz * zz).sum()
        if denom > 0:
            beta = (r[ok] * zz).sum() / denom
            r[ok] = r[ok] - beta * zz
        out[t] = np.where(ok, r, np.nan)
    return pd.DataFrame(out, index=sig.index, columns=sig.columns)


def backtest(sig, label, univ, window):
    """Decile / long-only / long-short on `univ`, sliced to `window`."""
    s0, e0 = window
    idx = sig.index
    grid = idx[(idx >= s0) & (idx <= e0)][::cfg.HORIZON]
    Suv = sig.where(univ); Luv = ae._masked(label, univ)
    dec, longx, ls = [], [], []
    for d in grid:
        sv, lv = Suv.loc[d], Luv.loc[d]
        ok = sv.notna() & lv.notna()
        if ok.sum() < 100:
            continue
        rk = sv[ok].rank(pct=True)
        top = lv[ok][rk > 1 - 1.0 / Q].mean()
        bot = lv[ok][rk <= 1.0 / Q].mean()
        uni = lv[ok].mean()
        grp = np.minimum((rk * Q).astype(int), Q - 1)
        dec.append(lv[ok].groupby(grp).mean().reindex(range(Q)).values)
        longx.append(top - uni); ls.append(top - bot)
    if len(longx) < 3:
        return None
    longx, ls = np.array(longx), np.array(ls)
    ann = lambda a: float((1 + a).prod() ** (PPY / len(a)) - 1)
    ic = ae.daily_ic(sig.where(univ), label, univ)
    ic = ic[(ic.index >= s0) & (ic.index <= e0)].dropna()
    return {"n_rebal": len(longx),
            "long_excess_ann": ann(longx), "long_excess_cum": float((1 + longx).prod() - 1),
            "ls_gross_ann": ann(ls), "ls_gross_cum": float((1 + ls).prod() - 1),
            "ic_mean": float(ic.mean()) if len(ic) else None,
            "deciles": [float(x) for x in np.nanmean(np.vstack(dec), axis=0)]}


def main(set_name):
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))
    reg = Registry(set_name)
    mask = panel.universe_mask("all")                 # tradable_entry
    label = panel.label(cfg.HORIZON)
    actives = reg.active()
    print(f"[{set_name}] recompute {len(actives)} factors")
    rank_sum, n = None, 0
    for a in actives:
        try:
            F = pl.compute_factor(a["expression"], panel) * a["direction"]
        except Exception:
            continue
        r = ae._masked(F, mask).rank(axis=1, pct=True)
        rank_sum = r if rank_sum is None else rank_sum.add(r, fill_value=0)
        n += 1
    comp = rank_sum / n
    print(f"  composite done [{time.time()-t0:.0f}s]; building style/status")

    size = panel.wide("CMV").astype(float)
    size_log = np.log(size.where(size > 0))
    ind = panel.wide("INDUSTRY")
    is_st = panel.wide("is_st").astype(float) > 0
    days = panel.wide("DAYS_ON").astype(float)
    size_rank = size.rank(axis=1, pct=True)
    invest = mask & (~is_st.reindex_like(mask).fillna(False)) \
        & (days >= MIN_DAYS) & (size_rank > SIZE_DROP)
    invest = invest.fillna(False)

    comp_neu = neutralize(comp, size_log, ind, mask)
    print(f"  neutralized [{time.time()-t0:.0f}s]")

    variants = {"raw": (comp, mask), "filtered": (comp, invest),
                "neutralized": (comp_neu, mask), "filt_neutral": (comp_neu, invest)}
    out = {"set": set_name, "n_factors": n,
           "filter": {"drop_ST": True, "min_days_on_market": MIN_DAYS,
                      "drop_smallest_pct": SIZE_DROP},
           "neutralize": "per-date residual on [SW-L1 industry, log circ_mv]",
           "variants": {}}
    for vname, (sig, univ) in variants.items():
        out["variants"][vname] = {w: backtest(sig, label, univ, win)
                                  for w, win in WINDOWS.items()}
    p = (ROOT / "results" / "mining" / "sets"
         / ("behavioral_full" if set_name == "main" else set_name) / "neutralize_eval.json")
    p.write_text(json.dumps(out, indent=2, default=float))
    # console summary
    for v in variants:
        f = out["variants"][v]["full"]; y = out["variants"][v]["y2026"]
        print(f"  {v:13} full: exc {f['long_excess_ann']:+.1%} IC {f['ic_mean']:+.3f} | "
              f"2026: exc {y['long_excess_ann']:+.1%} LS {y['ls_gross_ann']:+.1%} IC {y['ic_mean']:+.3f}")
    print(f"done [{time.time()-t0:.0f}s] -> {p}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
