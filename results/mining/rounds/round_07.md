# Round 7 — 2026-07-07 (40 candidates)

Exploit round: lead-lag flow couplings, unexplored corr pairs, MF event
structures, bands of accepted couplings, behavioral interactions.

**Funnel: 40 → S1 20 → S2 13 → S3 13 → S4 11 accepted.**
Alpha set: **67 factors**, diversity **0.840**. Runtime 38 min.

## Accepted (11)

| name | expression | IS IC / ICIR | OOS IC / ICIR |
|---|---|---|---|
| alpha_0058 | `-TsCorr(MF_LG_NET, AMP, 20)` | 0.043 / 0.56 | 0.041 / 0.55 |
| alpha_0059 | `-TsCorr(MF_LG_NET, CLOSE/VWAP−1, 20)` | 0.048 / 0.61 | 0.048 / 0.62 |
| alpha_0060 | `-TsCorr(Abs(gap), TURN_F, 20)` | 0.032 / 0.52 | 0.019 / 0.33 |
| alpha_0061 | `CsRank(HighDay(VR, 120))` | 0.033 / 0.54 | 0.015 / 0.24 |
| alpha_0062 | `-TsCount(aggr > 2·TsStd(aggr,60), 60)` | 0.042 / 0.55 | 0.033 / 0.42 |
| alpha_0063 | `CsRank(HighDay(Abs(gap), 120))` | 0.031 / 0.51 | 0.016 / 0.26 |
| alpha_0064 | `-TsCorr(RET, VR, 60)` | 0.052 / 0.60 | 0.044 / 0.53 |
| alpha_0065 | `-TsCorr(TURN_F, TsStd(RET,5), 60)` | 0.038 / 0.62 | 0.038 / 0.64 |
| alpha_0066 | `-TsCorr(TURN_F, Delay(RET,1), 60)` | 0.040 / 0.57 | 0.044 / 0.55 |
| alpha_0067 | `-(CLOSE/TsMed(CLOSE,60)−1)` | 0.058 / 0.42 | **0.070 / 0.52** |
| alpha_0068 | ix: vol_clock × intraday reversal | −0.038 / −0.75 | −0.036 / −0.63 |

(Names in registry are alpha_0058–0068; table shows core expressions.)

## Distilled

**Successful:** corr constructs are band-separable (3/3 quarterly bands
accepted, but not the MF one — 0.76 vs its own 20d); MF coupling extends
to price-action quantities (AMP, close-vs-vwap) but not volume ones
(TURN, gap); burst-frequency AND burst-recency mintable per quantity.

**Forbidden:** lead-lag flow/attention correlations (dead at S1 or OOS);
crash-side frequency (tails asymmetric: down-magnitude works, down-
frequency doesn't); 7 more second-representative S2 kills (vr_on_up ~
signed_attn at 0.98).

## Set status

67 factors. Largest families: overnight 6, interaction 6, volume_price 5,
lottery 5. S1 pass rate halved vs R5 (50% → 33% on comparable classes) —
diminishing returns visible but corr-band + interaction pools still open.
