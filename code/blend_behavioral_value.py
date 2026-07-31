#!/usr/bin/env python3
"""Behavioral (10d) + value (20d) blend test: does the orthogonal value sleeve
improve the combined book's risk-adjusted quality over full history (2017-25)?

Builds the neutralized behavioral composite B (behavioral_full) and value
composite V (value_20d) from stored values, confirms orthogonality, then sweeps
blend weight wV over the two horizons, reporting daily-IC mean / ICIR (risk-
adjusted signal quality) and long-excess ann.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining import alphaseval as ae          # noqa: E402
from mining import construct as cs           # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FULL = ("20170101", "20251231")
WEIGHTS = [0.0, 0.2, 0.3, 0.5, 0.7, 1.0]
HORIZONS = [10, 20]


def icir(ic):
    ic = ic.dropna()
    return float(ic.mean() / ic.std()) if len(ic) > 20 and ic.std() > 0 else np.nan


def main():
    panel = Panel()                                  # 2017-2025 (stored values)
    mask = panel.universe_mask("all")
    print("building composites from stored values...", flush=True)
    B, nB = cs.set_composite(Registry("main"), panel, mask, "stored")
    B = cs.neutralize_factor(B, panel, mask)
    print(f"  behavioral B: {nB} factors", flush=True)
    V, nV = cs.set_composite(Registry("value_20d"), panel, mask, "stored")
    V = cs.neutralize_factor(V, panel, mask)
    print(f"  value V: {nV} factors", flush=True)

    mfull = ae.slice_dates(mask, *FULL)
    xcorr = float(ae.factor_corr(ae.slice_dates(B, *FULL), ae.slice_dates(V, *FULL), mfull))
    print(f"\ncross-sectional rank corr(B, V) = {xcorr:+.3f}  (low = orthogonal)")

    rB = ae._masked(B, mask).rank(axis=1, pct=True)
    rV = ae._masked(V, mask).rank(axis=1, pct=True)

    out = {"n_behavioral": nB, "n_value": nV, "corr_BV": xcorr, "grid": []}
    print(f"\n{'horizon':>7} {'wV':>5} {'mean_IC':>8} {'ICIR':>7} {'excess_ann':>11} {'ic_corr(B,V)':>13}")
    for h in HORIZONS:
        label = panel.label(h)
        icB = ae.slice_dates(ae.daily_ic(B, label, mask), *FULL)
        icV = ae.slice_dates(ae.daily_ic(V, label, mask), *FULL)
        s = np.corrcoef(icB.dropna().align(icV.dropna(), join="inner")[0],
                        icB.dropna().align(icV.dropna(), join="inner")[1])[0, 1]
        for wV in WEIGHTS:
            blend = (1 - wV) * rB + wV * rV
            ic = ae.slice_dates(ae.daily_ic(blend, label, mask), *FULL)
            bt = ae.window_backtest(blend, label, mask, FULL, h)
            exc = bt["long_excess_ann"] if bt else np.nan
            row = {"horizon": h, "wV": wV, "mean_ic": float(ic.mean()),
                   "icir": icir(ic), "excess_ann": float(exc), "ic_corr_BV": float(s)}
            out["grid"].append(row)
            print(f"{h:>7} {wV:>5.1f} {ic.mean():>+8.4f} {icir(ic):>7.2f} "
                  f"{exc:>+11.1%} {s:>+13.3f}")
    (ROOT / "results" / "mining" / "blend_behavioral_value.json").write_text(
        json.dumps(out, indent=2, default=float))
    print("\nsaved results/mining/blend_behavioral_value.json")


if __name__ == "__main__":
    main()
