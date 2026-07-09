# Canonical set — Round 14 — 2026-07-09 (12 candidates, novelty run 4/5)

Per-type magnitudes/textures. Individual only; thresholds unchanged.

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2/S3 |corr|<0.70,
replace ≥1.3× · S4: OOS same-sign ≥max(0.03, 0.4×IS); ≥2/3 of
{HS300,CSI500,CSI1000} same-sign ≥0.005; yearly sign-rate ≥0.60; rolling
120d/step 20 sign-rate ≥0.70; block-bootstrap B=1000, block=10, seed=11,
p≤0.05.

**Funnel: 12 → S1 9 → S2 4 → S3 4 → S4 3 accepted.**
Canonical set: **87 factors**, diversity 0.746. Runtime 17 min.

## Accepted (3)

| name | expression | dir | IS IC / ICIR | OOS IC | S4 |
|---|---|---|---|---|---|
| calpha_0111 | `TsSum(gap · capit_day, 60)` (capitulation-gap depth) | + | 0.066 / 0.48 | **0.078** | 3/3, 1.00, roll ✓, p=0.000 |
| calpha_0112 | `-TsMean(nvol · dipbuy_day, 60)` (crowd size at absorption) | + | 0.070 / **0.78** | 0.070 | 3/3, 1.00, roll ✓, p=0.000 |
| calpha_0113 | `TsCount(dipbuy_day, 20)` (fast dip-bought count) | − | −0.035 / −0.54 | −0.053 | 3/3, 1.00, roll ✓, p=0.000 |

## Rejected (9)

- **S2 (6) — the vein self-locks**: hl_dipbuy (IS 0.078!) 0.78 vs
  hlmed60; hl_capit 0.76; id_capitmag / capit_dmg / aggr_capit120
  0.82–0.84 vs the new capitulation family; gap_dipmag120 0.84 vs its
  own 60d band.
- **S1 (3)**: gap_fademag 0.17 (fade side, 4th straight failure);
  gapid_covmag ICIR 0.43 / IC 0.027; breakout_vol120 0.15.

## Tally after 4/5 runs

7 novel factors from 61 candidates — all from the day-type class. Run 5
(final): normalized typed textures to break the S2 locks, attention on
capitulation, recovery efficiency, typed liquidity, and three non-vein
wildcards (dollar depth, gap kurtosis, robust aggression surprise).
