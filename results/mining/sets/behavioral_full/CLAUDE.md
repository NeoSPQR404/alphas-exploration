# behavioral_full — the main alpha set (code arg `"main"`)

**112 factors** mined over rounds 1–14 on the **full field vocabulary**
(OHLCV, vwap, turnover, VR, amplitude, limit boards, moneyflow,
northbound, margin, valuation, industry). The live home of the "main"
set — `Registry("main")`/`Memory("main")` and the round runner all point
here. Rounds 13–14 mined non-overnight veins (event-rarity, robust
median/mean ratio) and added 12; **5 were then moved to `robust_2026`**.

## Headline results (see the *_REPORT.md files)
- **Honest test** (2024–25, spent, original 105): 105/105 sign-consistent,
  median holdout IC 0.051, EW composite 0.110.
- **Backtest (neutralized + buffer 2.5, 10d):** excess vs universe +7.6%/yr
  IR 1.15, long-only net@15bp +13.6% (see `TURNOVER_OVERLAY.md`). Raw
  behavioral book excess +8.0%/yr IR 1.09; ~half the paper alpha is in the
  unshortable short leg.
- **Walk-forward:** selection generalizes, OOS IC ~88–97% of in-sample,
  7/7 positive test years (`WALKFORWARD.md`).

## Contents
`alpha_set.json`/`.csv` (112 active + retired w/ provenance),
`experience_memory.json` (14 rounds), `rounds/`, `holdout/`,
`HOLDOUT_REPORT.md`, `BACKTEST_REPORT.md`, `STAGE4_REEVAL.md`,
`turnover_overlay.json`, `backtest_neutral*.json`, `neutralize_eval.json`,
`ic_monitor` entry, `round13_2026.json`/`round14_2026.json`. Values in
`data/mining/alpha_values/`.
