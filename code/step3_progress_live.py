#!/usr/bin/env python3
"""Live terminal dashboard for the 2026 OOS-backtest pipeline.

Shows, refreshing in place: the 2026 raw fetch (per-endpoint progress),
the panel/base build stage, the wide-cache state, and the three set
backtests — with the headline number as each lands.

Usage:
    python3 code/step3_progress_live.py          # live, refresh every 2s
    python3 code/step3_progress_live.py --once   # render a single frame
"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "tushare-data" / "data" / "raw"
BASE = ROOT / "data" / "base"
WIDE = ROOT / "data" / "_wide_cache"
SETS_DIR = ROOT / "results" / "mining" / "sets"

FETCH_EPS = ["daily", "daily_basic", "adj_factor", "stk_limit", "suspend_d",
             "moneyflow", "hk_hold", "margin_detail"]
N_DAYS = 128
SETS = [("behavioral_full", "main"), ("canonical", "canonical"),
        ("canonical_composite", "canonical_composite")]

C = {"g": "\033[32m", "y": "\033[33m", "c": "\033[36m", "d": "\033[90m",
     "b": "\033[1m", "r": "\033[31m", "x": "\033[0m"}


def bar(done, total, width=24):
    f = 0 if total == 0 else done / total
    n = int(f * width)
    col = C["g"] if f >= 1 else (C["c"] if f > 0 else C["d"])
    return f"{col}{'█' * n}{C['d']}{'░' * (width - n)}{C['x']} {done:>4}/{total}"


def count(ep):
    d = RAW / ep / "2026"
    return len(list(d.glob("*.parquet"))) if d.exists() else 0


def frame():
    L = []
    L.append(f"{C['b']}{C['c']}═══ 2026 OOS backtest pipeline "
             f"{time.strftime('%H:%M:%S')} ═══{C['x']}")
    L.append("")
    # stage 1: fetch
    fetched = {ep: count(ep) for ep in FETCH_EPS}
    fetch_done = all(v >= N_DAYS for v in fetched.values())
    tot = sum(fetched.values())
    tag = f"{C['g']}✓{C['x']}" if fetch_done else f"{C['y']}…{C['x']}"
    L.append(f"{C['b']}[1] fetch 2026 raw{C['x']}  {tag}  "
             f"({tot}/{N_DAYS * len(FETCH_EPS)} files)")
    for ep in FETCH_EPS:
        L.append(f"    {ep:<14} {bar(fetched[ep], N_DAYS)}")
    L.append("")
    # stage 2: panel + base
    panel26 = (ROOT.parent / "tushare-data" / "data" / "panel" / "year=2026").exists()
    base26 = (BASE / "year=2026" / "base.parquet").exists()
    def st(ok, running):
        return f"{C['g']}✓ done{C['x']}" if ok else (
            f"{C['y']}… running{C['x']}" if running else f"{C['d']}pending{C['x']}")
    L.append(f"{C['b']}[2] build panel/2026{C['x']}   {st(panel26, fetch_done and not panel26)}")
    L.append(f"{C['b']}[3] build base/2026{C['x']}    {st(base26, panel26 and not base26)}")
    wide_ok = WIDE.exists() and any(WIDE.glob("*.parquet"))
    L.append(f"{C['b']}[4] wide cache{C['x']}         "
             f"{C['g']+'✓ ready'+C['x'] if wide_ok else C['d']+'cleared/rebuilding'+C['x']}")
    L.append("")
    # stage 3: backtests
    L.append(f"{C['b']}[5] backtests (2026 window){C['x']}")
    for folder, _ in SETS:
        f = SETS_DIR / folder / "backtest_2026.json"
        if f.exists():
            try:
                d = json.loads(f.read_text())
                lo = d.get("long_only_net_15bp", {}).get("ann_return")
                ex = d.get("long_excess_mkt", {}).get("ann_return")
                nb = d.get("n_rebalances")
                lo_s = f"{lo:+.1%}" if isinstance(lo, (int, float)) else "n/a"
                ex_s = f"{ex:+.1%}" if isinstance(ex, (int, float)) else "n/a"
                msg = (f"{C['g']}✓{C['x']}  LO net15 {C['b']}{lo_s}{C['x']}  "
                       f"excess-mkt {ex_s}  ({nb} rebal)")
            except Exception:
                msg = f"{C['y']}… writing{C['x']}"
        else:
            msg = f"{C['d']}pending{C['x']}"
        L.append(f"    {folder:<22} {msg}")
    L.append("")
    stage = ("fetching" if not fetch_done else "building panel" if not panel26
             else "building base" if not base26
             else "backtesting" if not all((SETS_DIR / s / "backtest_2026.json").exists()
                                           for s, _ in SETS) else "COMPLETE")
    scol = C["g"] if stage == "COMPLETE" else C["y"]
    L.append(f"{C['b']}stage:{C['x']} {scol}{stage}{C['x']}")
    return "\n".join(L)


def main():
    once = "--once" in sys.argv
    if once:
        print(frame())
        return
    try:
        print("\033[2J", end="")           # clear
        while True:
            print("\033[H", end="")         # home
            out = frame()
            print(out + "\033[0J", flush=True)
            if "COMPLETE" in out:
                print(f"\n{C['g']}{C['b']}pipeline complete.{C['x']}")
                break
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{C['d']}(stopped){C['x']}")


if __name__ == "__main__":
    main()
