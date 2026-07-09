# Canonical set — Round 12 — 2026-07-09 (16 candidates, novelty run 2/5)

Day-type vein exploitation. Individual factors only; thresholds
unchanged (same full parameter block as round_11.md: whitelist
OPEN/HIGH/LOW/CLOSE/VOLUME/AMOUNT/VWAP/RET; fwd_ret_10d t+1 vwap;
tradable_entry ≥50; S1 |IC|≥0.03/|ICIR|≥0.30/cov≥0.60; S2/S3 corr<0.70,
1.3× replace; S4 = OOS ≥max(0.03,0.4×IS) + ≥2/3 universes + yearly ≥0.60
+ rolling 120/20 ≥0.70 + bootstrap B=1000/block=10/seed=11 p≤0.05).

**Funnel: 16 → S1 7 → S2 4 → S3 4 → S4 1 accepted.**
Canonical set: **82 factors**, diversity 0.752. Runtime 12 min.

## Accepted (1)

| name | expression | IS IC / ICIR | OOS IC | S4 |
|---|---|---|---|---|
| calpha_0108 | `-TsMean((CLOSE/VWAP−1)·dipbuy_day, 60)` (aggression on dip-bought days) | 0.070 / 0.68 | **0.068** | 3/3, 1.00, roll ✓, p=0.000 |

## Rejected (15)

- S2 corr-locks (3): dipbuy_mag (IS 0.076!) 0.74 vs med_band60;
  dipbuy_hivol 0.71; vwap_recover 0.76 vs dipbuy_freq.
- S4 (2): the fade side is real but weak — fade_share OOS −0.024 (2/3
  uni), fade_freq120 −0.021; both just under the 0.03 bar.
- S1 (10): ratios/balances/post-returns of day-types; gap one-sidedness
  at 180/250 (ICIR 0.43+ but IC never clears 0.03).

## Verdict so far (runs 1–2)

2 genuine novel factors from 34 candidates, both from the day-type
class. Run 3 pushes day-types further: churn days (volume without
progress), accumulation days, inside/outside bar counts, breakout-with-
volume, aggression on other day-types.
