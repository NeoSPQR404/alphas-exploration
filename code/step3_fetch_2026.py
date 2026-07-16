"""Step 3 — fetch 2026 raw data to extend the panel for a fresh OOS backtest.

Fetches the by-date endpoints for 2026 (through the latest trading day) into
tushare-data/data/raw/<endpoint>/2026/, same layout as the 2017-2025 base.
Fundamentals (income/balance/cashflow/forecast/express) are NOT refetched —
the panel build reuses the cached prep (data/_prep_cache/), i.e. TTM values
are carried forward from the last 2025 announcement (documented caveat: Q1-2026
reports announced ~Apr-2026 are not incorporated).

Also refreshes trade_cal and the index_daily benchmarks for 2026.

Usage: python3 code/step3_fetch_2026.py   (resumable; sandbox must be off)
"""
import sys
import time
from pathlib import Path

import pandas as pd
import tushare as ts

REPO = Path(__file__).resolve().parents[2] / "tushare-data"
sys.path.insert(0, str(REPO))
RAW = REPO / "data" / "raw"

from tsbarra import config  # noqa: E402
from tsbarra.client import TushareClient  # noqa: E402
from tsbarra import fetch_prices  # noqa: E402
from tsbarra.logutil import setup  # noqa: E402

START, END = "20260101", "20260716"
BY_DATE = ("daily", "daily_basic", "adj_factor", "stk_limit", "suspend_d",
           "moneyflow", "hk_hold", "margin_detail")
INDEXES = ("000300.SH", "000905.SH", "000852.SH")

config.RATE_LIMITS.update({ep: 190 for ep in BY_DATE})


def refresh_calendar_and_indexes():
    pro = ts.pro_api(open(REPO / "token.txt").read().strip())
    # trade_cal: append 2026
    cal_path = RAW / "trade_cal.parquet"
    cal = pd.read_parquet(cal_path)
    new = pro.trade_cal(exchange="SSE", start_date=START, end_date=END)
    cal = pd.concat([cal[cal["cal_date"] < START], new], ignore_index=True)
    cal = cal.drop_duplicates("cal_date").sort_values("cal_date")
    cal.to_parquet(cal_path, index=False)
    print(f"trade_cal -> {cal['cal_date'].max()}", flush=True)
    # index_daily benchmarks
    for code in INDEXES:
        f = RAW / f"index_daily_{code}.parquet" if code != "000300.SH" else None
        for attempt in range(3):
            try:
                df = pro.index_daily(ts_code=code, start_date=START, end_date=END)
                break
            except Exception as e:
                print(f"index {code} retry: {e}"); time.sleep(15)
        # append into the per-index file if it exists, else the index_daily dir
        dst = RAW / f"index_daily_{code}.parquet"
        if dst.exists():
            old = pd.read_parquet(dst)
            df = pd.concat([old[old["trade_date"] < START], df], ignore_index=True)
        df = df.drop_duplicates(["ts_code", "trade_date"]).sort_values("trade_date")
        df.to_parquet(dst, index=False)
        print(f"index_daily {code} -> {len(df)} rows", flush=True)


if __name__ == "__main__":
    log = setup()
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("cal", "all"):
        # calendar first so fetch_by_date sees 2026 trading days
        refresh_calendar_and_indexes()
    if mode in ("fetch", "all"):
        client = TushareClient()
        fetch_prices.fetch_by_date(client, datasets=BY_DATE, start=START, end=END)
    log.info("2026 fetch step done.")
