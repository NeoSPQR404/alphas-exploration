#!/usr/bin/env python3
"""Fresh out-of-sample backtest on the 2026 window (genuinely unseen data).

Unlike backtest_composite.py, this RECOMPUTES every factor from its stored
expression over the 2026-extended panel (registry values only run to 2025),
then evaluates the EW oriented-rank composite on 2026 only. The label
(fwd_ret_10d, t+1 vwap → t+11 vwap) is complete through ~late-June 2026;
later dates are dropped automatically (NaN label).

Run: python3 code/backtest_2026.py <set_name>   (main|canonical|canonical_composite)
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
COST_SIDES_BP = (15.0, 30.0)
Q = 10
PPY = 250 / cfg.HORIZON
WIN = ("20260101", "20261231")   # 2026 OOS window


def stats(r: pd.Series) -> dict:
    r = r.dropna()
    if len(r) < 4:
        return {"n_periods": int(len(r))}
    ann = float((1 + r).prod() ** (PPY / len(r)) - 1)
    vol = float(r.std() * np.sqrt(PPY))
    curve = (1 + r).cumprod()
    return {"n_periods": int(len(r)), "ann_return": ann, "ann_vol": vol,
            "sharpe": float(ann / vol) if vol > 0 else np.nan,
            "max_drawdown": float((curve / curve.cummax() - 1).min()),
            "hit_rate": float((r > 0).mean()),
            "mean_period_ret": float(r.mean()),
            "cum_return": float((1 + r).prod() - 1)}


def main(set_name: str):
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))      # include 2026
    reg = Registry(set_name)
    set_dir = (ROOT / "results" / "mining" / "sets" / "behavioral_full"
               if set_name == "main"
               else ROOT / "results" / "mining" / "sets" / set_name)
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    actives = reg.active()
    print(f"2026 backtest [{set_name}]: {len(actives)} factors, recomputing")

    rank_sum = None
    n_used = 0
    for i, a in enumerate(actives):
        try:
            F = pl.compute_factor(a["expression"], panel) * a["direction"]
        except Exception as e:
            print(f"  skip {a['name']}: {type(e).__name__}")
            continue
        rank_sum = (ae._masked(F, mask).rank(axis=1, pct=True) if rank_sum is None
                    else rank_sum.add(ae._masked(F, mask).rank(axis=1, pct=True),
                                      fill_value=0))
        n_used += 1
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(actives)} [{time.time()-t0:.0f}s]")
    comp = rank_sum / n_used

    # 2026 rebalance grid, label-complete only
    idx = comp.index
    win = idx[(idx >= WIN[0]) & (idx <= WIN[1])]
    dates = win[::cfg.HORIZON]
    L = ae._masked(label, mask)
    # CSI300 benchmark read directly from raw index_daily (robust for 2026;
    # panel bench_close may not populate the new year)
    RAW = ROOT.parent / "tushare-data" / "data" / "raw"
    bench = None
    for cand in (RAW / "index_daily" / "000300.SH.parquet",
                 RAW / "index_daily_000300.SH.parquet"):
        if cand.exists():
            bi = pd.read_parquet(cand)
            bi = bi[bi["ts_code"] == "000300.SH"] if "ts_code" in bi else bi
            bench = bi.set_index("trade_date")["close"].sort_index()
            break
    if bench is None:
        bench = panel.wide("bench_close").iloc[:, 0]
    bench = bench.reindex(idx).ffill()

    rows = []
    pl_long = pl_short = None
    for d in dates:
        s, l = comp.loc[d], L.loc[d]
        ok = s.notna() & l.notna()
        if ok.sum() < 100:
            continue
        rk = s[ok].rank(pct=True)
        longs = set(rk.index[rk > 1 - 1.0 / Q]); shorts = set(rk.index[rk <= 1.0 / Q])
        to_l = 1.0 if pl_long is None else 1 - len(longs & pl_long) / max(len(longs), 1)
        to_s = 1.0 if pl_short is None else 1 - len(shorts & pl_short) / max(len(shorts), 1)
        grp = np.minimum((rk * Q).astype(int), Q - 1)
        dec = l[ok].groupby(grp).mean().reindex(range(Q)).values
        p = idx.get_loc(d)
        b0, b1 = min(p + 1, len(bench) - 1), min(p + 1 + cfg.HORIZON, len(bench) - 1)
        rows.append({"date": d, "long": float(l[list(longs)].mean()),
                     "short": float(l[list(shorts)].mean()),
                     "mkt": float(l[ok].mean()), "to_long": to_l, "to_short": to_s,
                     "csi300": float(bench.iloc[b1] / bench.iloc[b0] - 1),
                     "deciles": dec})
        pl_long, pl_short = longs, shorts

    df = pd.DataFrame(rows).set_index("date")
    out = {"set": set_name, "window": "2026", "n_factors": n_used,
           "n_rebalances": len(df), "dates": [df.index.min(), df.index.max()],
           "horizon": cfg.HORIZON, "cost_bp_per_side": list(COST_SIDES_BP),
           "decile_mean_period_ret": [float(x) for x in
                                      np.nanmean(np.vstack(df["deciles"].values), axis=0)]}
    c = COST_SIDES_BP[0] / 1e4
    out["long_only_gross"] = stats(df["long"])
    out["long_only_net_15bp"] = stats(df["long"] - df["to_long"] * 2 * c)
    out["long_only_net_30bp"] = stats(df["long"] - df["to_long"] * 2 * (COST_SIDES_BP[1] / 1e4))
    out["long_excess_mkt"] = stats(df["long"] - df["mkt"])
    out["long_excess_csi300"] = stats(df["long"] - df["csi300"])
    out["ls_gross"] = stats(df["long"] - df["short"])
    out["market_ew"] = stats(df["mkt"])
    out["csi300"] = stats(df["csi300"])
    out["avg_turnover_long"] = float(df["to_long"].mean())

    path = set_dir / "backtest_2026.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print(json.dumps({k: out[k] for k in ("n_factors", "n_rebalances", "dates",
          "long_only_net_15bp", "long_excess_mkt", "ls_gross", "avg_turnover_long")},
          indent=2, default=float))
    print(f"done in {time.time()-t0:.0f}s -> {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
