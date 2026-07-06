#!/bin/zsh
cd "$(dirname "$0")"
exec python3 step1_progress_live.py \
  "/private/tmp/claude-501/-Users-NEO-MAO-Desktop-Quant-Research/c323091f-4fc1-4782-9909-db7e92ae1cbb/scratchpad/fetch_missing.log" \
  "/private/tmp/claude-501/-Users-NEO-MAO-Desktop-Quant-Research/c323091f-4fc1-4782-9909-db7e92ae1cbb/scratchpad/rebuild_panel.log"
