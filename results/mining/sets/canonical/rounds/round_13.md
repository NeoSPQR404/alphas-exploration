# Canonical set — Round 13 — 2026-07-09 (15 candidates, novelty run 3/5)

Day-types deeper: volume-conditioned types, bar patterns, aggression/
magnitude on types. Individual only; thresholds unchanged (full
parameter block identical to round_11.md: whitelist 8 canonical fields;
fwd_ret_10d t+1 vwap; tradable_entry ≥50; S1 0.03/0.30/0.60; S2/S3
corr<0.70 + 1.3×; S4 OOS ≥max(0.03, 0.4×IS) + ≥2/3 universes + yearly
≥0.60 + rolling 120/20 ≥0.70 + bootstrap 1000/10/seed 11 p≤0.05).

**Funnel: 15 → S1 5 → S2 3 → S3 3 → S4 2 accepted.**
Canonical set: **84 factors**, diversity 0.749. Runtime 11 min.

## Accepted (2)

| name | expression | IS IC / ICIR | OOS IC | S4 |
|---|---|---|---|---|
| calpha_0109* | `TsSum(gap · dipbuy_day, 60)` (depth of bought dips) | 0.072 / 0.60 | **0.082** | 3/3, 1.00, roll ✓, p=0.000 |
| calpha_0110* | `-TsMean((CLOSE/VWAP−1) · capit_day, 60)` (aggression on capitulation days) | −0.054 / −0.36 | −0.064 | 3/3, 1.00, roll ✓, p=0.000 |

(*ids per registry order of acceptance this round)

## Rejected (13)

- S2 (3): accum_freq 0.74 vs hl_on_hivol; aggr_dipbuy120 0.78 vs its
  own 60d band; (counts starting to self-lock within the vein).
- S1 (10): bar patterns dead (inside 0.17, outside 0.08); churn days
  ICIR-viable but IC ~0.019; quiet-drift, breakout-with-volume,
  fade-side magnitudes/aggression all under.

## Experiment tally after 3/5 runs

4 genuine novel factors from 49 candidates — all from the day-type
class run 1 surfaced. Lesson shift: magnitude-on-type > count-of-type.
Run 4 targets per-type magnitudes/textures (gap depths, ranges,
attention on typed days).
