# Canonical set — Round 17 — 2026-07-09 (40 candidates, extended run 2/5)

Exploitation of R16's three new classes + near-miss jitters. Individual
only; thresholds unchanged (parameter block identical to round_16.md:
8-field whitelist; fwd_ret_10d t+1 vwap; tradable_entry ≥50; S1
0.03/0.30/0.60; S2/S3 corr<0.70 + 1.3×; S4 OOS ≥max(0.03,0.4×IS) + ≥2/3
universes + yearly ≥0.60 + rolling 120/20 ≥0.70 + bootstrap 1000/10/11
p≤0.05).

**Funnel: 40 → S1 12 → S2 7 → S3 7 → S4 7 accepted.**
Canonical set: **100 individual factors**, diversity 0.745. Runtime 33 min.

## Accepted (7)

| name | expression | IS IC / ICIR | OOS IC |
|---|---|---|---|
| calpha_0120 | `-TsCount(pin, 20)` (fast stalemates) | −0.043 / −0.41 | **−0.061** |
| calpha_0121* | `-TsMean(aggr·(CLOSE≥TsMax(CLOSE,20)), 60)` (aggression at highs) | 0.061 / 0.55 | 0.053 |
| calpha_0122* | `-TsMean(nvol·truegap_day, 60)` (crowd at range-breaks) | 0.053 / 0.63 | 0.048 |
| calpha_0123* | `-TsCount(|CLOSE/MA20−1|<0.005, 60)` (tight MA pins) | −0.031 / −0.31 | −0.048 |
| calpha_0124* | `-(vol20 / vol20 a month ago)` (attention acceleration) | 0.035 / 0.41 | 0.042 |
| calpha_0125* | `-TsCount(truegap_dn, 250)` (annual range-break habit) | 0.033 / 0.34 | 0.040 |
| calpha_0126* | `-TsMean(nvol·(|gap|>2σ), 120)` (crowd at gap shocks) | 0.045 / 0.65 | 0.034 |

(*ids by acceptance order)

Two class REVIVALS via jitter: MA-pin (threshold 0.01→0.005) and
acceleration (fortnight→monthly ratio). Lesson: jitter thresholds, not
just windows.

## Rejected (33)

- S1 (28): conditioned pins all dead (contested/wide/lazy/gap −0.10 to
  −0.31); pin at 120/250 decays; typed true-gap sub-events thin;
  at-extreme textures (hl/gap/id) 0.09–0.13.
- S2 (5): lazy_pin 0.82 vs pin20; truegap_dn120 0.80; tg_dn_bought 0.77;
  island_mag 0.91; vol_ext_asym120 0.76.

## Tally: extended campaign 12/80 through 2 runs; set at 100.
