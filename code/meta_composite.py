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
import itertools
import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import construct as cs           # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FULL = ("20170101", "20251231")
WINDOWS = {"full": FULL, "y2026": ("20260101", "20261231")}
SETS = [("main", "behavioral_full"), ("canonical", "canonical"),
        ("canonical_composite", "canonical_composite")]


def set_neu_composite(set_name, panel, mask, t0):
    """Neutralized EW-rank composite of a set's active factors, recomputed
    from expressions over the full 2017-2026 panel (streamed via
    construct.set_composite -- a list of ~100 full-panel frames swaps the box)."""
    comp, n = cs.set_composite(Registry(set_name), panel, mask, "expr")
    neu = cs.neutralize_factor(comp, panel, mask)
    print(f"  [{set_name}] {n} factors, neutralized [{time.time()-t0:.0f}s]",
          flush=True)
    return neu, n


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
    for ka, kb in itertools.combinations(keys, 2):
        a = ae.slice_dates(comps[ka], *FULL)
        b = ae.slice_dates(comps[kb], *FULL)
        pair_corr[f"{ka}~{kb}"] = float(ae.factor_corr(a, b, mfull))

    ic_series = {k: ae.daily_ic(comps[k], label, mask) for k in keys}
    ic_full = {k: ae.slice_dates(ic_series[k], *FULL) for k in keys}
    icir = {k: float(ic_full[k].mean() / ic_full[k].std())
            if ic_full[k].std() > 0 else 0.0 for k in keys}
    ic_corr = {}
    for ka, kb in itertools.combinations(keys, 2):
        s = pd.concat([ic_full[ka], ic_full[kb]], axis=1).dropna()
        ic_corr[f"{ka}~{kb}"] = float(s.iloc[:, 0].corr(s.iloc[:, 1]))

    # -- meta blends
    frames = [comps[k] for k in keys]
    w = [max(icir[k], 0.0) for k in keys]
    meta_ew = cs.oriented_composite(frames, mask)
    meta_irw = cs.oriented_composite(frames, mask, weights=w)

    # -- backtest standalones + metas
    variants = {**{k: comps[k] for k in keys},
                "meta_ew": meta_ew, "meta_irw": meta_irw}
    results = {name: {wn: ae.window_backtest(sig, label, mask, win, cfg.HORIZON)
                      for wn, win in WINDOWS.items()}
               for name, sig in variants.items()}

    out = {
        "n_factors": nfac,
        "construction": "size+industry neutralized EW-rank composite per set",
        "pairwise_rank_corr": pair_corr,
        "ic_series_corr": ic_corr,
        "full_window_ic": {k: float(ic_full[k].mean()) for k in keys},
        "full_window_icir": icir,
        "irw_weights": dict(zip(keys, w)),
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
