"""Live terminal dashboard for the Step 1 data pipeline.

Usage:  python3 step1_progress_live.py [fetch_log] [rebuild_log]
Refreshes every 5 s. Reads progress from the filesystem (raw file counts,
panel/base mtimes), so it works even without the log files. Ctrl-C to exit.
"""
from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "tushare-data" / "data" / "raw"
PANEL = ROOT / "tushare-data" / "data" / "panel"
BASE = ROOT / "alphas-exploration" / "data" / "base"

ENDPOINTS = [("stk_limit", "涨跌停价"), ("suspend_d", "停复牌"),
             ("moneyflow", "资金流向"), ("hk_hold", "北向持股"),
             ("margin_detail", "融资融券")]
TOTAL_DAYS = 2430          # trade days 2016-2025
PANEL_YEARS = list(range(2017, 2026))
RUN_START = None           # set on first observation of today's rebuild

fetch_log = Path(sys.argv[1]) if len(sys.argv) > 1 else None
rebuild_log = Path(sys.argv[2]) if len(sys.argv) > 2 else None

GREEN, BLUE, DIM, BOLD, RESET = "\033[32m", "\033[34m", "\033[2m", "\033[1m", "\033[0m"


def count(ep: str) -> int:
    d = RAW / ep
    if not d.exists():
        return 0
    return sum(1 for _ in d.rglob("*.parquet"))


def bar(n: int, total: int, width: int = 34) -> str:
    pct = min(n / total, 1.0)
    fill = int(pct * width)
    color = GREEN if pct >= 1 else BLUE
    return f"{color}{'█' * fill}{DIM}{'░' * (width - fill)}{RESET} {n:>5}/{total} {pct*100:5.1f}%"


def tail(p: Path | None, keep: str = "") -> str:
    if not p or not p.exists():
        return ""
    try:
        lines = p.read_text(errors="ignore").strip().splitlines()
        for line in reversed(lines):
            if keep in line:
                return line[-110:]
    except OSError:
        pass
    return ""


def freshness(p: Path) -> str:
    if not p.exists():
        return f"{DIM}not built{RESET}"
    age = time.time() - p.stat().st_mtime
    when = datetime.fromtimestamp(p.stat().st_mtime).strftime("%m-%d %H:%M")
    mark = GREEN + "rebuilt today" + RESET if age < 86400 else DIM + "stale" + RESET
    return f"{when}  {mark}"


while True:
    out = ["\033[2J\033[H"]  # clear + home
    out.append(f"{BOLD}Step 1 — alphas-exploration data pipeline{RESET}   "
               f"{DIM}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  (refresh 5s, Ctrl-C quits){RESET}\n")

    out.append(f"{BOLD}Endpoint fetch{RESET}  {DIM}2016-2025, one call per trade day{RESET}")
    done_total = 0
    for ep, cn in ENDPOINTS:
        n = count(ep)
        done_total += min(n, TOTAL_DAYS)
        out.append(f"  {ep:<14}{cn:　<5} {bar(n, TOTAL_DAYS)}")
    out.append(f"  {'ALL':<14}{'':　<5} {bar(done_total, TOTAL_DAYS * len(ENDPOINTS))}\n")

    line = tail(fetch_log, "INFO")
    if line:
        out.append(f"  {DIM}log: {line}{RESET}\n")

    out.append(f"{BOLD}Panel rebuild (tushare-data/data/panel){RESET}")
    for y in PANEL_YEARS:
        out.append(f"  year={y}   {freshness(PANEL / f'year={y}' / 'panel.parquet')}")
    line = tail(rebuild_log, "INFO")
    if line:
        out.append(f"  {DIM}log: {line}{RESET}")
    out.append("")

    out.append(f"{BOLD}Mining base (alphas-exploration/data/base){RESET}")
    if BASE.exists() and any(BASE.glob("year=*")):
        for yd in sorted(BASE.glob("year=*")):
            out.append(f"  {yd.name}   {freshness(yd / 'base.parquet')}")
    else:
        out.append(f"  {DIM}pending — waits for fetch + rebuild{RESET}")

    print("\n".join(out), flush=True)
    time.sleep(5)
