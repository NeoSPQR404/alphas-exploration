# Canonical set — Round 3 — 2026-07-08 (34 candidates)

Tier sweep: bands that coexisted in the main set (semivol, min, aggrmax,
meanmed), turnover-analog constructs never canonically tested (volume
spike, 2-day lag chase), range/gap events, deeper-band coupling retries.

**Funnel: 34 → S1 27 → S2 18 → S3 18 → S4 16 accepted.**
Canonical set: **70 factors**, diversity **0.763**. Runtime 54 min.

## Accepted (16) — highlights

| construct | OOS IC | note |
|---|---|---|
| c_aggrmax60 `-TsMax(CLOSE/VWAP−1, 60)` | **0.077** | coexists with 20d sibling |
| c_hl_updown120 (range asym, 120d) | **0.074** | ICIR 0.91 IS / 0.76 OOS |
| c_semivol60 | 0.070 | 20/60/120 coexist, as in main |
| c_min_gap60 `-TsMin(gap, 60)` | **−0.064** | quarterly deepest gap-down — a construct the main set never held (its 20d version died there) |
| c_min60 `-TsMin(RET, 60)` | −0.058 | |
| c_nvol_spike `-(TsMean(V,5)/TsMean(V,60))` | 0.052 | turn_spike analog |
| c_gapmed20 | 0.043 | fast median overnight drift |
| c_aggr_updown 20d / 60d | 0.039 / 0.043 | aggression asymmetry pair |
| c_aggr_burst120 | 0.041 | |
| c_vol_updown120 | 0.038 | |
| c_volterm_mid (20/120) | 0.038 | |
| c_lag2 20d / 60d | 0.034 / 0.034 | 2-day lagged chase |
| c_hl_burst 60d / 120d | 0.032 / 0.033 | range-burst counts |

## Rejected (18)

- **S1 (7)** — meanmed60 0.027 / meanmed120 0.025 (IC < 0.03),
  idmed120, hlterm_slow, hl_nvol_corr120 IC 0.015 (range-attention
  coupling dead at every band in this vocabulary), ret_on_lovol120,
  upday_share_hivol.
- **S2 (9)** — max120~max-family 0.72, rev120~rev-family 0.70,
  gapvol60~gapvol 0.74, nvolmax 0.70 / nvolmax60 0.83, gapmax20 0.77,
  illiq_term −0.87 vs zeroret, gap_on_hivol60 0.73, id_updown 0.73.
- **S4 (2)** — pvcorr60 OOS 0.019; gap_on_hivol120 0.013 (gap
  conditionals dead at all tiers).

## Distilled

**Successful:** main-set band-coexistence patterns replicate; gap-crash
magnitude (min_gap60) is canonical-only alpha; turnover analogs (spike,
lag2) transfer. **Forbidden:** range-attention couplings and gap
conditionals are closed books; meanmed/idmed long bands under the bar.
