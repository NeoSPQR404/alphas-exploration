"""Step 1 — validate the cleaned mining base (data/base).

Sanity checks per year:
  * uniqueness of (ts_code, trade_date); calendar alignment vs trade_cal
  * vwap within [low, high]; ret_1d consistent with pct_chg where gap==1
  * flag rates: limit_up/down close, one-word boards, ST share, entry blocked
  * label coverage: fwd_ret_* non-NaN share, tradable_entry share
  * industry coverage: sw_l1 non-null share
Writes results/step1_base_validation.json and prints a table.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "base"
TS = ROOT.parent / "tushare-data" / "data"
OUT = ROOT / "results"

CHECK_COLS = ["ts_code", "trade_date", "low", "high", "vwap", "pct_chg",
              "ret_1d", "gap_days", "is_st", "sw_l1_code", "days_on_market",
              "limit_up_close", "limit_down_close", "one_word_board",
              "entry_blocked_next", "tradable_entry", "up_limit",
              "fwd_ret_1d", "fwd_ret_5d", "fwd_ret_10d", "fwd_ret_20d"]

report = {}
cal = pd.read_parquet(TS / "raw" / "trade_cal.parquet")
cal_open = set(cal[cal["is_open"] == 1]["cal_date"].astype(str))

for ydir in sorted(BASE.glob("year=*")):
    year = ydir.name.split("=")[1]
    df = pd.read_parquet(ydir / "base.parquet",
                         columns=[c for c in CHECK_COLS])
    r = {"rows": len(df)}
    r["dup_keys"] = int(df.duplicated(["ts_code", "trade_date"]).sum())
    days = set(df["trade_date"].astype(str).unique())
    r["days"] = len(days)
    r["days_not_in_cal"] = sorted(days - cal_open)
    r["missing_cal_days"] = len([d for d in cal_open if d.startswith(year)]) - len(days)

    v_ok = df["vwap"].between(df["low"], df["high"]) | df["vwap"].isna()
    r["vwap_out_of_range"] = int((~v_ok).sum())
    r["vwap_nan_rate"] = round(float(df["vwap"].isna().mean()), 5)

    m = df["gap_days"] == 1
    diff = (df.loc[m, "ret_1d"] * 100 - df.loc[m, "pct_chg"]).abs()
    r["ret_vs_pctchg_p99"] = round(float(diff.quantile(0.99)), 4)

    for c in ["limit_up_close", "limit_down_close", "one_word_board",
              "entry_blocked_next", "is_st", "tradable_entry"]:
        if c in df:
            r[f"{c}_rate"] = round(float(df[c].mean()), 4)
    r["up_limit_nan_rate"] = round(float(df["up_limit"].isna().mean()), 4) \
        if "up_limit" in df else None
    for h in [1, 5, 10, 20]:
        r[f"fwd_ret_{h}d_cov"] = round(float(df[f"fwd_ret_{h}d"].notna().mean()), 4)
    r["sw_l1_cov"] = round(float(df["sw_l1_code"].notna().mean()), 4)
    r["median_days_on_market"] = float(df["days_on_market"].median())
    report[year] = r
    print(year, {k: v for k, v in r.items()
                 if k in ("rows", "dup_keys", "vwap_out_of_range",
                          "ret_vs_pctchg_p99", "is_st_rate", "tradable_entry_rate",
                          "sw_l1_cov", "up_limit_nan_rate", "fwd_ret_20d_cov")})

OUT.mkdir(exist_ok=True)
with open(OUT / "step1_base_validation.json", "w") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print("written:", OUT / "step1_base_validation.json")
