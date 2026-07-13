# behavioral_full — the main alpha set (code arg `"main"`)

105 factors mined over rounds 1–12 on the **full field vocabulary**
(OHLCV, vwap, turnover, VR, amplitude, limit boards, moneyflow,
northbound, margin, valuation, industry). The live home of the "main"
set — `Registry("main")`/`Memory("main")` and the round runner all point
here.

## Headline results (see the *_REPORT.md files)
- **Honest test** (2024–25, spent): 105/105 sign-consistent, median
  holdout IC 0.051, EW composite 0.110.
- **Backtest**: long-only top-decile net-15bp +11.8%/yr; excess vs its
  own universe +8.0%/yr, IR 1.09; ~half the paper alpha is in the
  unshortable short leg.
- **Stage-4 re-eval**: 105/105 pass all 5 sub-tests.

## Contents
`alpha_set.json`/`.csv` (105 active + 38 retired w/ provenance),
`experience_memory.json` (12 rounds, ~72 patterns), `rounds/`,
`holdout/`, `HOLDOUT_REPORT.md`, `BACKTEST_REPORT.md`,
`STAGE4_REEVAL.md`, `README.md`. Values in
`data/mining/alpha_values/`.
