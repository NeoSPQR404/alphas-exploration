#!/usr/bin/env python3
"""Cross-set meta-composite: blend the three sets' neutralized composites.

The three sets (behavioral_full, canonical, canonical_composite) are built
from different vocabularies, so their signals should be only partly
correlated. This script:

  1. builds each set's size+industry NEUTRALIZED EW-rank composite (the
     recommended construction, code/mining/construct.py) over 2017-2026;
  2. measures pairwise cross-sectional rank correlation and daily-IC-series
     correlation (the diversification evidence);
  3. blends them two ways -- equal-weight rank and IR-weighted rank -- and
  4. backtests every standalone set and both meta variants on the full
     (2017-25) and fresh 2026 windows (decile / long-excess / LS / IC).

Outputs results/mining/meta_composite.json (+ META_COMPOSITE.md written
separately). Run: python3 code/meta_composite.py
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
from mining import construct as cs           # noqa: E402
from mining import pipeline as pl            # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402
from neutralize_eval import backtest, WINDOWS  # reuse the eval backtester # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FULL = ("20170101", "20251231")
SETS = [("main", "behavioral_full"), ("canonical", "canonical"),
        ("canonical_composite", "canonical_composite")]


def set_neu_composite(set_name, panel, mask, t0):
    """Neutralized EW-rank composite of a set's active factors, recomputed
    from expressions over the full 2017-2026 panel.

    Streams the factor frames (one alive at a time) into the rank-sum -- a
    list of ~100 full-panel frames is >10 GB and swaps the machine to death.
    """
    reg = Registry(set_name)
    count = {"n": 0}

    def oriented():
        for a in reg.active():
            try:
                F = pl.compute_factor(a["expression"], panel) * a["direction"]
            except Exception:
                continue
            count["n"] += 1
            yield F

    comp = cs.oriented_composite(oriented(), mask)
    neu = cs.neutralize_factor(comp, panel, mask)
    print(f"  [{set_name}] {count['n']} factors, neutralized [{time.time()-t0:.0f}s]",
          flush=True)
    return neu, count["n"]


def weighted_composite(frames, weights, mask):
    """Weighted mean of per-date pct ranks of oriented frames."""
    num, den = None, float(sum(weights))
    for F, w in zip(frames, weights):
        r = ae._masked(F, mask).rank(axis=1, pct=True) * w
        num = r if num is None else num.add(r, fill_value=0)
    return num / den


def main():
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    keys = [s[0] for s in SETS]

    comps, nfac = {}, {}
    for sn, _ in SETS:
        comps[sn], nfac[sn] = set_neu_composite(sn, panel, mask, t0)

    # -- diversification: pairwise cross-sectional rank corr + IC-series corr
    mfull = ae.slice_dates(mask, *FULL)
    pair_corr = {}
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a = ae.slice_dates(comps[keys[i]], *FULL)
            b = ae.slice_dates(comps[keys[j]], *FULL)
            pair_corr[f"{keys[i]}~{keys[j]}"] = float(ae.factor_corr(a, b, mfull))

    ic_series = {k: ae.daily_ic(comps[k], label, mask) for k in keys}
    ic_full = {k: ae.slice_dates(ic_series[k], *FULL) for k in keys}
    icir = {k: float(ic_full[k].mean() / ic_full[k].std())
            if ic_full[k].std() > 0 else 0.0 for k in keys}
    ic_corr = {}
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            s = pd.concat([ic_full[keys[i]], ic_full[keys[j]]], axis=1).dropna()
            ic_corr[f"{keys[i]}~{keys[j]}"] = float(s.iloc[:, 0].corr(s.iloc[:, 1]))

    # -- meta blends
    meta_ew = cs.oriented_composite([comps[k] for k in keys], mask)
    w = [max(icir[k], 0.0) for k in keys]
    meta_irw = weighted_composite([comps[k] for k in keys], w, mask)

    # -- backtest standalones + metas
    variants = {**{k: comps[k] for k in keys},
                "meta_ew": meta_ew, "meta_irw": meta_irw}
    results = {name: {wn: backtest(sig, label, mask, win)
                      for wn, win in WINDOWS.items()}
               for name, sig in variants.items()}

    out = {
        "n_factors": nfac,
        "construction": "size+industry neutralized EW-rank composite per set",
        "pairwise_rank_corr": pair_corr,
        "ic_series_corr": ic_corr,
        "full_window_ic": {k: float(ic_full[k].mean()) for k in keys},
        "full_window_icir": icir,
        "irw_weights": {keys[i]: w[i] for i in range(len(keys))},
        "results": results,
    }
    p = ROOT / "results" / "mining" / "meta_composite.json"
    p.write_text(json.dumps(out, indent=2, default=float))

    # -- console summary
    print("\npairwise cross-sectional rank corr:")
    for k, v in pair_corr.items():
        print(f"  {k:40} {v:+.3f}")
    print("IC-series corr:")
    for k, v in ic_corr.items():
        print(f"  {k:40} {v:+.3f}")
    print(f"\n{'variant':22} {'full_exc':>9} {'full_IC':>8} {'2026_exc':>9} "
          f"{'2026_LS':>8} {'2026_IC':>8}")
    for name in variants:
        f = results[name]["full"]; y = results[name]["y2026"]
        print(f"{name:22} {f['long_excess_ann']:>+9.1%} {f['ic_mean']:>+8.3f} "
              f"{y['long_excess_ann']:>+9.1%} {y['ls_gross_ann']:>+8.1%} "
              f"{y['ic_mean']:>+8.3f}")
    print(f"\ndone [{time.time()-t0:.0f}s] -> {p}")


if __name__ == "__main__":
    main()
