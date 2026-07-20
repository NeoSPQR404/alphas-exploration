#!/usr/bin/env python3
"""Compute the extra series the report graphs need, per set:
  - composite rank-IC in each window (is / oos_gate / holdout / 2026)
  - 2026 per-rebalance long / market / csi300 returns (for equity curves)
Recomputes each set's EW oriented-rank composite once over 2017-2026.
Output: results/mining/analysis_2026.json
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
WINDOWS = {"is": (cfg.IS_START, cfg.IS_END), "oos_gate": (cfg.OOS_START, cfg.OOS_END),
           "holdout": (cfg.HOLDOUT_START, cfg.HOLDOUT_END), "y2026": ("20260101", "20261231")}


def main():
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    L = ae._masked(label, mask)
    RAW = ROOT.parent / "tushare-data" / "data" / "raw"
    bench = pd.read_parquet(RAW / "index_daily" / "000300.SH.parquet")
    bench = bench.set_index("trade_date")["close"].sort_index()

    out = {}
    for set_name in ("main", "canonical", "canonical_composite"):
        reg = Registry(set_name)
        actives = reg.active()
        print(f"[{set_name}] recomputing {len(actives)} factors [{time.time()-t0:.0f}s]")
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

        ic = ae.daily_ic(comp, label, mask)      # daily rank IC of the composite
        icw = {}
        for w, (s, e) in WINDOWS.items():
            seg = ic[(ic.index >= s) & (ic.index <= e)].dropna()
            icw[w] = float(seg.mean()) if len(seg) else None

        # 2026 per-rebalance long / mkt / csi300 for the equity curve
        idx = comp.index
        win = idx[(idx >= "20260101") & (idx <= "20261231")]
        dates = win[::cfg.HORIZON]
        b = bench.reindex(idx).ffill()
        series = []
        for d in dates:
            sv, lv = comp.loc[d], L.loc[d]
            ok = sv.notna() & lv.notna()
            if ok.sum() < 100:
                continue
            rk = sv[ok].rank(pct=True)
            longs = rk.index[rk > 1 - 1.0 / Q]
            p = idx.get_loc(d)
            b0, b1 = min(p + 1, len(b) - 1), min(p + 1 + cfg.HORIZON, len(b) - 1)
            series.append({"date": d, "long": float(lv[longs].mean()),
                           "mkt": float(lv[ok].mean()),
                           "csi300": float(b.iloc[b1] / b.iloc[b0] - 1)})
        out[set_name] = {"ic_by_window": icw, "y2026_series": series, "n_factors": n}
        print(f"  IC {({k: round(v,3) if v else v for k,v in icw.items()})}")

    (ROOT / "results" / "mining" / "analysis_2026.json").write_text(
        json.dumps(out, indent=2, default=float))
    print(f"done in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
