# behavioral_full — frozen set snapshot (2026-07-08)

105 factors mined over rounds 1-12 on the full field vocabulary (OHLCV,
vwap, turnover, volume_ratio, amplitude, limit-board fields, moneyflow,
valuation, industry, bench). All clear |rank IC| >= 0.03 in-sample
(2017-21) AND OOS (2022-23); honest-tested on the 2024-25 holdout
(105/105 sign-consistent, median IC 0.051, EW composite 0.110 — see
HOLDOUT_REPORT.md).

This snapshot is FROZEN: the files here are a point-in-time copy of the
live registry/memory at the moment of archiving. The live set continues
at results/mining/alpha_set.json ("main"). Factor values remain in the
shared store (data/mining/alpha_values/, names alpha_0001..alpha_0143
incl. retired) and are rebuildable from expressions.
