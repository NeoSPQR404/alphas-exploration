#!/bin/bash
# Double-click to watch the 2026 OOS-backtest pipeline live.
cd "$(dirname "$0")/.."
exec python3 code/step3_progress_live.py
