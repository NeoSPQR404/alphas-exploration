# Canonical set — Round 16 — 2026-07-09 (40 candidates, extended run 1/5)

Parallel class-hunt across 9 untouched structural classes. Individual
only; thresholds unchanged.

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2/S3 |corr|<0.70,
replace ≥1.3× · S4: OOS same-sign ≥max(0.03, 0.4×IS); ≥2/3 of
{HS300,CSI500,CSI1000} same-sign ≥0.005; yearly sign-rate ≥0.60; rolling
120d/step 20 sign-rate ≥0.70; block-bootstrap B=1000, block=10, seed=11,
p≤0.05.

**Funnel: 40 → S1 15 → S2 7 → S3 5 → S4 5 accepted.**
Canonical set: **93 factors**, diversity 0.746. Runtime 30 min.

## Accepted (5) — three NEW classes

| name | expression | class | IS IC / ICIR | OOS IC |
|---|---|---|---|---|
| calpha_0115 | `-TsCount(|CLOSE/VWAP−1|<0.002, 60)` (stalemate days) | pin | −0.049 / −0.35 | **−0.070** |
| calpha_0116 | `-TsCount(OPEN<Delay(LOW,1), 60)` (range-breaking gap-downs) | true gap | 0.036 / 0.35 | 0.044 |
| calpha_0117 | unfilled gap-up count (island days) | true gap | 0.030 / 0.52 | 0.044 |
| calpha_0118 | `-TsMean(nvol·(CLOSE≤TsMin(CLOSE,20)), 60)` (crowd at lows) | vol-at-ext | −0.040 / −0.42 | −0.041 |
| calpha_0119 | volume-at-highs − volume-at-lows | vol-at-ext | 0.053 / 0.48 | 0.040 |

## Rejected (35)

- S2 (8): week-run extremes 0.70–0.77 vs max_eff family; true-gap
  magnitudes 0.73–0.84 vs gapmed/mingap; blowoff 0.75; heavy-dip
  variants 0.73–0.80 vs the dipbuy family.
- S3 (2): vol_at_high and range_at_high → dups of vol_ext_asym.
- S1 (25): zone occupancy, peak asynchrony, MA-duration, round trips,
  acceleration, triple-condition day-types all dead. Near-misses logged:
  ma_cross −0.034/−0.29, near_low_occ 0.030/0.27, vol/range
  acceleration ~0.028/0.33–0.34.

## Next (run 2/5)

Exploit the three live classes: contested/wide/exhaustion pins, typed
true-gap events (bought gap-downs, faded gap-ups, islands down),
volume-at-extremes variants and bands, plus 8 near-miss jitters.
