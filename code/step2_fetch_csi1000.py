#!/usr/bin/env python3
"""Fetch CSI1000 (000852.SH) index_weight into tushare-data/data/raw/.

Matches the format of the existing index_weight_000300.SH.parquet /
index_weight_000905.SH.parquet files: columns
[index_code, con_code, trade_date, weight], one snapshot per month.

Usage: python3 code/step2_fetch_csi1000.py
"""
import time
from pathlib import Path

import pandas as pd
import tushare as ts

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "tushare-data" / "data" / "raw"
TOKEN = (ROOT.parent / "tushare-data" / "token.txt").read_text().strip()

INDEX = "000852.SH"
OUT = RAW / f"index_weight_{INDEX}.parquet"
START_YEAR, END_YEAR = 2016, 2025


def main():
    pro = ts.pro_api(TOKEN)
    frames = []
    months = [
        (f"{y}{m:02d}01", f"{y}{m:02d}31")
        for y in range(START_YEAR, END_YEAR + 1)
        for m in range(1, 13)
    ]
    for start, end in months:
        for attempt in range(3):
            try:
                df = pro.index_weight(index_code=INDEX, start_date=start, end_date=end)
                break
            except Exception as e:
                print(f"{start}: retry {attempt + 1} after {e}")
                time.sleep(15)
        else:
            raise RuntimeError(f"failed month {start}")
        if df is not None and len(df):
            frames.append(df)
            print(f"{start}: {len(df)} rows")
        time.sleep(0.35)  # stay under rate limit

    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset=["con_code", "trade_date"])
    out = out.sort_values(["trade_date", "con_code"]).reset_index(drop=True)
    out.to_parquet(OUT, index=False)
    print(f"saved {len(out)} rows -> {OUT}")
    print(out["trade_date"].min(), out["trade_date"].max())


if __name__ == "__main__":
    main()
