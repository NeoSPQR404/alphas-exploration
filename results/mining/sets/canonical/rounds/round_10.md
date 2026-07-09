# Canonical set — Round 10 — 2026-07-09 (19 candidates, INDIVIDUAL only)

Context: before this round the 26 composition factors were split out to
`sets/canonical_composite/`, leaving 79 individual factors; per user
directive this round uses **no composition rules** — every candidate is
a single expression over raw fields. First round gated by the upgraded
stage 4 (rolling + bootstrap).

## Evaluation parameters (complete)

| parameter | value |
|---|---|
| field whitelist (AST-enforced) | OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT, VWAP, RET |
| label | fwd_ret_10d (entry t+1 vwap, suspension-aware) |
| universe / mask | full-A `tradable_entry`, min 50 names/date |
| IC definition | daily cross-sectional Spearman rank IC |
| IS window / OOS-gate window | 2017-01-01…2021-12-31 / 2022-01-01…2023-12-31 |
| S1 | \|IS IC\| ≥ 0.03, \|IS ICIR\| ≥ 0.30, coverage ≥ 0.60 |
| S2 | \|corr\| < 0.70 vs residents; replacement at ≥ 1.3× \|IS IC\| |
| S3 | intra-round dedup at \|corr\| < 0.70, keep-best by \|ICIR\| |
| S4-T1 OOS | same sign, \|OOS IC\| ≥ max(0.03, 0.4×\|IS IC\|) |
| S4-T2 universes | ≥2 of {HS300, CSI500, CSI1000}, same-sign IC ≥ 0.005 |
| S4-T3 yearly | ≥60% same-sign years 2017–2023 |
| S4-T4 rolling | 120d windows, step 20; sign-rate ≥ 0.70 |
| S4-T5 bootstrap | moving-block, B=1000, block=10, seed=11, p ≤ 0.05 |

**Funnel: 19 → S1 7 → S2 1 → S3 1 → S4 1 accepted.**
Canonical set: **80 individual factors**, diversity **0.753**. Runtime 8 min.

## Accepted (1)

| name | expression | IS IC / ICIR | OOS IC / ICIR | rolling / bootstrap |
|---|---|---|---|---|
| calpha_0106 | `-TsMean((H/L−1)/TsMed(H/L−1,60)−1, 10)` (smoothed robust range deviation) | 0.041 / 0.45 | 0.034 / — | 1.00 / p=0.000 |

The one success is a near-miss rescue: 10-day smoothing lifted the raw
daily version (IC 0.026) over the bar.

## Rejected (18) — the exhaustion signature

- **S2 corr-locks (6)**: the strong new constructs all alias residents —
  awvol/awmove (attention-weighted vol, IS 0.073–0.075!) 0.77–0.78 vs
  vol-term family; vwapgap_vol 0.088 IS 0.073 vs gapvol; gap_abs_med
  0.77 vs hlmed60; att_span 0.89; ovnmom30 0.74 vs ovnmom60.
- **S1 (12)**: novel asymmetries dead (amihud_updown 0.13/0.10 ICIR,
  ovnshare_updown −0.08); range-path constructs under bar (hl_slope
  0.27, hl_persist 0.34/IC 0.021); all remaining band jitters under one
  bar or the other.

## Distilled

Individual-factor space in the canonical vocabulary is **exhausted**:
what's new is weak, what's strong is owned. Growth paths from here are
structural — new fields, a different label horizon (20d sub-track), or
relaxed corr thresholds — not more formulas.
