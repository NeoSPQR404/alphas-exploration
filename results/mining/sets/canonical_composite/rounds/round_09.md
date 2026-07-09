# Canonical set — Round 9 — 2026-07-09 (10 candidates) — TARGET MET

Closing round: fresh 3-way triples from untried parent combinations.

**Funnel: 10 → S1 9 → S2 8 → S3 8 → S4 8 accepted.**
Canonical set: **105 factors** (target 100 exceeded), diversity **0.764**.
Runtime 30 min.

## Accepted (8) — all 3-way products

| construct | OOS IC |
|---|---|
| cx3_max20_med_volclock | **+0.060** |
| cx3_gapvol_med_volclock | +0.055 |
| cx3_semivol_volclock_amtself | +0.052 |
| cx3_gapvol_rev60_amtself | +0.051 |
| cx3_aggrmax_rev60_amtself | +0.048 |
| cx3_hlburst_amtself_rev60 | +0.045 |
| cx3_semivol_med_maxfreq | +0.044 |
| cx3_aggrburst_med_amtself | +0.037 |

All 3/3 sub-universes, 7/7 years. The 3-way tier finishes 15/17 across
rounds 8–9.

## Rejected (2)

- S1: cx3_hlmed_volclock_maxfreq 0.029 (just under the bar).
- S2: cx3_nvolburst_rev20_volclock 0.73 vs a round-8 3-way — the 3-way
  space itself starts self-colliding at ~15 members.

## Campaign summary (canonical set)

105 factors from 8 fields (OPEN/HIGH/LOW/CLOSE/VOLUME/AMOUNT/VWAP/RET)
in 9 rounds: 34 transfer, 44 novel canonical constructs, 27 compositions.
Acceptance path: 34, 21, 16, 7, 2, 1, 5, 13, 8 — the composition pivot
at round 7 broke the saturation that rounds 5–6 hit. Every factor clears
|rank IC| ≥ 0.03 IS (2017–21) and OOS (2022–23); the 2024–25 holdout
remains unread for this set.
