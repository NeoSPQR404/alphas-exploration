# behavioral_full — the main alpha set

105 factors mined over rounds 1–12 on the full field vocabulary (OHLCV,
vwap, turnover, volume_ratio, amplitude, limit-board fields, moneyflow,
valuation, industry, bench). All clear |rank IC| ≥ 0.03 in-sample
(2017–21) AND OOS (2022–23), plus the upgraded stage-4 battery
(sub-universes, yearly, rolling-window, block-bootstrap — see
STAGE4_REEVAL.md).

**Layout note (2026-07-09):** this directory started as a frozen
snapshot but is now the *live* home of the main set — the registry
(`alpha_set.json`), experience memory, per-round artifacts (`rounds/`,
`holdout/`), and all evaluation reports were consolidated here, and the
code's "main" paths point here (`Registry("main")`, `Memory("main")`,
round runner, evaluation scripts). Factor values live in
`data/mining/alpha_values/` (local, rebuildable from expressions).

## Contents

| file | what |
|---|---|
| `alpha_set.json` / `.csv` | live registry: 105 active + 38 retired with provenance |
| `experience_memory.json` | 12 rounds, successful/forbidden patterns |
| `rounds/round_NN.{md,json}` | per-round reports (funnel, tables, lessons) |
| `holdout/` | per-round holdout snapshots + `full_set_eval.json` |
| `HOLDOUT_REPORT.md` | 2024–25 honest test (read once, 2026-07-08 — spent) |
| `BACKTEST_REPORT.md` / `backtest.json` | composite backtest 2017–2025 |
| `STAGE4_REEVAL.md` / `stage4_reeval.json` | upgraded stage-4 re-evaluation, all parameters |

Headline results: honest test 105/105 sign-consistent, median holdout IC
0.051, EW composite 0.110; backtest LO net-15bp +11.8%/yr (excess vs
universe +8.0%/yr, IR 1.09); stage-4 re-eval 105/105 pass.
