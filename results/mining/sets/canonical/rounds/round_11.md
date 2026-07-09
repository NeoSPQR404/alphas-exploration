# Canonical set — Round 11 — 2026-07-09 (18 candidates, novelty run 1/5)

Individual factors only; thresholds unchanged. Explored: joint-condition
day-type counts, cross-quantity elasticities, shape ratios, distribution
shape on non-return quantities, duration measures.

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2/S3 |corr|<0.70,
replace ≥1.3× · S4: OOS same-sign ≥max(0.03, 0.4×IS); ≥2/3 of
{HS300,CSI500,CSI1000} same-sign ≥0.005; yearly sign-rate ≥0.60; rolling
120d/step 20 sign-rate ≥0.70; block-bootstrap B=1000, block=10, seed=11,
p≤0.05.

**Funnel: 18 → S1 4 → S2 4 → S3 3 → S4 1 accepted.**
Canonical set: **81 factors**, diversity 0.753. Runtime 11 min.

## Accepted (1) — a genuine novel vein

| name | expression | dir | IS IC / ICIR | OOS IC | S4 detail |
|---|---|---|---|---|---|
| calpha_0107 | `TsCount((gap<0)·(intraday>0), 60)` (dip-bought days) | − | −0.041 / −0.55 | **−0.064** | 3/3 uni, years 1.00, rolling ✓, boot p=0.000 |

Joint gap-direction × intraday-direction day-types are untouched space:
names whose gap-downs keep getting bought intraday **underperform** —
visible dip-buying is distribution, not accumulation. OOS stronger than
IS, and only 0.63 max correlation to 80 residents.

## Rejected (17)

- S4 (2): fade_freq OOS 0.024 (just under); nvol_burst_amp OOS 0.011.
- S3 (1): dipbuy_freq120 dup of the 60d version.
- S1 (14): elasticities (range/gap-per-attention 0.11–0.32), clustering
  coefficients (|IC| ~0.02), burst-amplitude ratios, hl_skew, nvol_kurt,
  duration, robust Amihud; near-misses logged: aggr_on_gapdn 0.029,
  gap_sign_bal120 ICIR 0.52 / IC 0.024.

## Next (run 2/5)

Exploit the day-type vein: capitulation days, large-gap conditioning,
volume-conditioned day-types, conversion-rate ratios (share of gap-downs
that get bought), post-day-type returns, and the two near-misses.
