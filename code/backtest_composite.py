#!/usr/bin/env python3
"""Portfolio backtest of a set's equal-weight rank composite.

Design (matches the label construction — no execution fantasy):
- signal: mean of oriented per-date pct ranks of all active factors
- rebalance every HORIZON trading days; selection among tradable_entry
  names; equal weight
- period return of a held name = fwd_ret_{HORIZON}d at the rebalance date
  (entry t+1 vwap -> exit t+1+H vwap, suspension-aware). The H-day grid
  chains these vwap-to-vwap legs exactly.
- costs: turnover x (buy + sell) per side, applied per period
- outputs: <set_dir>/backtest.json

Run: python3 code/backtest_composite.py <set_name>
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
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

COST_SIDES_BP = (15.0, 30.0)   # base and stress, per side
Q = 10
PERIODS_PER_YEAR = 250 / cfg.HORIZON

WINDOWS = {
    "full": ("20170101", "20251231"),
    "is": (cfg.IS_START, cfg.IS_END),
    "oos_gate": (cfg.OOS_START, cfg.OOS_END),
    "holdout": (cfg.HOLDOUT_START, cfg.HOLDOUT_END),
}


def stats(period_ret: pd.Series) -> dict:
    r = period_ret.dropna()
    if len(r) < 8:
        return {}
    ann_ret = float((1 + r).prod() ** (PERIODS_PER_YEAR / len(r)) - 1)
    ann_vol = float(r.std() * np.sqrt(PERIODS_PER_YEAR))
    curve = (1 + r).cumprod()
    dd = float((curve / curve.cummax() - 1).min())
    return {
        "n_periods": int(len(r)),
        "ann_return": ann_ret,
        "ann_vol": ann_vol,
        "sharpe": float(ann_ret / ann_vol) if ann_vol > 0 else np.nan,
        "max_drawdown": dd,
        "hit_rate": float((r > 0).mean()),
        "mean_period_ret": float(r.mean()),
    }


def main(set_name: str):
    t0 = time.time()
    panel = Panel()
    reg = Registry(set_name)
    if set_name == "main":
        set_dir = ROOT / "results" / "mining"
    else:
        set_dir = ROOT / "results" / "mining" / "sets" / set_name
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    actives = reg.active()
    print(f"backtest [{set_name}]: {len(actives)} factors")

    rank_sum = None
    for i, a in enumerate(actives):
        F = reg.values(a["name"]) * a["direction"]
        r = ae._masked(F, mask).rank(axis=1, pct=True)
        rank_sum = r if rank_sum is None else rank_sum.add(r, fill_value=0)
        if (i + 1) % 15 == 0:
            print(f"{i+1}/{len(actives)} [{time.time()-t0:.0f}s]")
    comp = rank_sum / len(actives)

    dates = comp.index[::cfg.HORIZON]
    L = ae._masked(label, mask)

    rows = []
    prev_long, prev_short = set(), set()
    bench_ret = panel.wide("bench_close").iloc[:, 0]
    for d in dates:
        s = comp.loc[d]
        l = L.loc[d]
        ok = s.notna() & l.notna()
        if ok.sum() < 200:
            continue
        ranks = s[ok].rank(pct=True)
        longs = set(ranks.index[ranks > 1 - 1.0 / Q])
        shorts = set(ranks.index[ranks <= 1.0 / Q])
        long_ret = float(l[list(longs)].mean())
        short_ret = float(l[list(shorts)].mean())
        mkt_ret = float(l[ok].mean())
        to_l = 1.0 if not prev_long else 1 - len(longs & prev_long) / max(len(longs), 1)
        to_s = 1.0 if not prev_short else 1 - len(shorts & prev_short) / max(len(shorts), 1)
        # decile means for monotonicity
        grp = np.minimum((ranks * Q).astype(int), Q - 1)
        dec = l[ok].groupby(grp).mean().reindex(range(Q)).values
        rows.append({"date": d, "long": long_ret, "short": short_ret,
                     "mkt": mkt_ret, "to_long": to_l, "to_short": to_s,
                     "deciles": dec})
        prev_long, prev_short = longs, shorts

    df = pd.DataFrame(rows).set_index("date")
    # benchmark (CSI300) period returns on the same grid
    bidx = [d for d in df.index]
    b = bench_ret.reindex(comp.index).ffill()
    bpos = [comp.index.get_loc(d) for d in bidx]
    bper = []
    for p in bpos:
        i0, i1 = min(p + 1, len(b) - 1), min(p + 1 + cfg.HORIZON, len(b) - 1)
        bper.append(b.iloc[i1] / b.iloc[i0] - 1)
    df["csi300"] = bper

    out = {"set": set_name, "n_factors": len(actives),
           "horizon": cfg.HORIZON, "quantiles": Q,
           "cost_bp_per_side": list(COST_SIDES_BP), "windows": {}}

    dec_mat = np.vstack(df["deciles"].values)
    out["decile_mean_period_ret"] = [float(x) for x in np.nanmean(dec_mat, axis=0)]

    for wname, (s, e) in WINDOWS.items():
        w = df[(df.index >= s) & (df.index <= e)]
        if not len(w):
            continue
        entry = {
            "long_only_gross": stats(w["long"]),
            "long_excess_mkt": stats(w["long"] - w["mkt"]),
            "long_excess_csi300": stats(w["long"] - w["csi300"]),
            "ls_gross": stats(w["long"] - w["short"]),
            "market_ew": stats(w["mkt"]),
            "csi300": stats(w["csi300"]),
            "avg_turnover_long": float(w["to_long"].mean()),
        }
        for bp in COST_SIDES_BP:
            c = bp / 1e4
            lo_net = w["long"] - w["to_long"] * 2 * c
            ls_net = (w["long"] - w["short"]) - (w["to_long"] + w["to_short"]) * 2 * c
            entry[f"long_only_net_{int(bp)}bp"] = stats(lo_net)
            entry[f"ls_net_{int(bp)}bp"] = stats(ls_net)
        out["windows"][wname] = entry

    # yearly long-only net (base cost) and LS gross
    c = COST_SIDES_BP[0] / 1e4
    lo_net = df["long"] - df["to_long"] * 2 * c
    yearly = {}
    for y, g in df.groupby(df.index.str[:4]):
        yearly[y] = {
            "long_net_base": float((1 + (g["long"] - g["to_long"] * 2 * c)).prod() - 1),
            "mkt": float((1 + g["mkt"]).prod() - 1),
            "csi300": float((1 + g["csi300"]).prod() - 1),
            "ls_gross": float((1 + (g["long"] - g["short"])).prod() - 1),
        }
    out["yearly"] = yearly

    path = set_dir / "backtest.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print(json.dumps({k: v for k, v in out["windows"]["full"].items()
                      if k in ("long_only_gross", "long_only_net_15bp",
                               "ls_gross", "avg_turnover_long")}, indent=2))
    print(f"done in {time.time()-t0:.0f}s -> {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
