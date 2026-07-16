#!/usr/bin/env python3
"""Orchestrate the 2026 pipeline after the raw fetch: clean index fetch →
rebuild panel/2026 → build base/2025+2026 → clear wide cache → 3 backtests.

Emits one clean STAGE line per step (for live streaming) and waits for the
raw fetch to finish first. Run in background.
"""
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / "tushare-data"
RAW = REPO / "data" / "raw"
WIDE = ROOT / "data" / "_wide_cache"
FETCH_EPS = ["daily", "daily_basic", "adj_factor", "stk_limit", "suspend_d",
             "moneyflow", "hk_hold", "margin_detail"]
N = 128


def say(msg):
    print(f"STAGE {time.strftime('%H:%M:%S')} | {msg}", flush=True)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=str(ROOT), **kw)


def fetch_complete():
    return all(len(list((RAW / ep / "2026").glob("*.parquet"))) >= N
               for ep in FETCH_EPS if (RAW / ep / "2026").exists()) and \
        all((RAW / ep / "2026").exists() for ep in FETCH_EPS)


def main():
    # 1. wait for raw fetch
    say("waiting for raw fetch to finish")
    while not fetch_complete():
        time.sleep(15)
    say("raw fetch COMPLETE (8/8 endpoints, 128 days)")

    # 2. clean CSI300/CSI500/CSI1000 index 2026
    say("fetching 2026 index benchmarks")
    import tushare as ts
    pro = ts.pro_api((REPO / "token.txt").read_text().strip())
    for code in ("000300.SH", "000905.SH", "000852.SH"):
        dst = RAW / "index_daily" / f"{code}.parquet"
        try:
            new = pro.index_daily(ts_code=code, start_date="20260101", end_date="20260716")
            if dst.exists():
                old = pd.read_parquet(dst)
                new = pd.concat([old[old["trade_date"] < "20260101"], new], ignore_index=True)
            new = new.drop_duplicates(["ts_code", "trade_date"]).sort_values("trade_date")
            dst.parent.mkdir(parents=True, exist_ok=True)
            new.to_parquet(dst, index=False)
        except Exception as e:
            say(f"  index {code} WARN: {type(e).__name__}")
        time.sleep(0.5)
    say("index benchmarks done")

    # 3. rebuild panel/2026
    say("building panel/2026 (this can take a few minutes)")
    r = run([sys.executable, "code/step1_rebuild_panel.py", "2026"])
    say(f"panel/2026 {'DONE' if r.returncode == 0 else 'FAILED rc=' + str(r.returncode)}")

    # 4. build base/2025+2026
    say("building base/2025 + base/2026")
    r = run([sys.executable, "code/step1_build_base.py", "2025", "2026"])
    say(f"base build {'DONE' if r.returncode == 0 else 'FAILED rc=' + str(r.returncode)}")

    # 5. clear wide cache so factors recompute including 2026
    say("clearing wide cache for 2026-inclusive recompute")
    if WIDE.exists():
        for f in WIDE.glob("*.parquet"):
            f.unlink()

    # 6. backtests
    for folder, arg in (("behavioral_full", "main"), ("canonical", "canonical"),
                        ("canonical_composite", "canonical_composite")):
        say(f"backtesting {folder} on 2026 window")
        r = run([sys.executable, "code/backtest_2026.py", arg])
        say(f"backtest {folder} {'DONE' if r.returncode == 0 else 'FAILED rc=' + str(r.returncode)}")

    say("PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
