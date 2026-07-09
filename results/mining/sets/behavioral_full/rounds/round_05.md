# Round 5 — 2026-07-07 (40 candidates)

Structurally new classes: conditional aggregation, candle anatomy,
limit-board fields, event recency/frequency, cross-quantity correlations,
long bands, seasonality.

**Funnel: 40 → S1 22 → S2 17 → S3 16 → S4 15 accepted.**
Alpha set: **51 factors**, diversity eigen-entropy **0.842**. Runtime 39 min.

## Accepted (15)

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR | rank-AC 10d |
|---|---|---|---|---|---|
| alpha_0037 | `-TsSum(RET·Delay(limit_up_touch,1), 60)` | + | 0.021 / 0.45 | 0.024 / **0.75** | 0.78 |
| alpha_0038 | `-TsCount(one_word_board, 120)` | + | 0.032 / 0.41 | 0.021 / 0.38 | 0.93 |
| alpha_0039 | `CsRank(HighDay(limit_up_touch, 120))` | + | 0.040 / 0.56 | 0.035 / 0.56 | 0.80 |
| alpha_0040 | `-TsCount(AMP > 2·TsMean(AMP,60), 60)` | + | 0.044 / 0.54 | 0.033 / 0.33 | 0.83 |
| alpha_0041 | `-TsCount(gap < −2·TsStd(gap,60), 60)` | + | 0.026 / 0.48 | 0.025 / 0.44 | 0.82 |
| alpha_0042 | `-TsCorr(CLOSE/VWAP−1, TURN_F, 20)` | + | 0.023 / 0.39 | 0.033 / 0.54 | 0.40 |
| alpha_0043 | `-TsCorr(TURN_F, TsStd(RET,5), 20)` | + | 0.035 / 0.61 | 0.033 / 0.61 | 0.34 |
| alpha_0044 | `-(TsSum(VOL,20)/TsSum(VOL,250))` (vol clock) | + | 0.056 / 0.54 | **0.076 / 0.62** | 0.84 |
| alpha_0045 | `-TsSum(CLOSE/OPEN−1, 60)` (quarterly band) | + | **0.072 / 0.60** | **0.072 / 0.53** | 0.82 |
| alpha_0046 | `-TsCorr(TURN_F, Delay(RET,2), 20)` | + | 0.034 / 0.51 | 0.034 / 0.45 | 0.39 |
| alpha_0047 | `-TsMean(Sign(RET)·VR, 20)` | + | 0.049 / 0.48 | 0.039 / 0.35 | 0.47 |
| alpha_0048 | `-(TsMean(RET,20) − TsMed(RET,20))` | + | 0.033 / 0.50 | 0.041 / 0.63 | 0.38 |
| alpha_0049 | `-(TsMax(TURN_F,60)/TsMean(TURN_F,250))` | + | 0.046 / 0.56 | 0.038 / 0.39 | 0.86 |
| alpha_0050 | ix: limit_touch × gap_vol | − | −0.040 / −0.74 | −0.026 / −0.43 | 0.60 |
| alpha_0051 | ix: med_rev × vr_mean | − | −0.042 / −0.87 | −0.036 / **−0.76** | 0.04 |

Highlights: **vol_clock** posts the strongest OOS IC in the whole set
(0.076); **quarterly intraday reversal** confirms bands are separable a
third time (corr 0.54 vs the 20d version); the **limit-board family**
generalized in every direction tried (recency, one-word count, post-event
returns); the **interaction template is 4-for-6**, always with the
negative "agreement is bearish" sign.

## Near-miss worth recording

`ret_amp_corr` beat alpha_0006 by 1.65× (replacement-eligible) but also
correlated ≥0.7 with a second incumbent it couldn't displace → rejected.
The runner printed a misleading "PASS, replaces" line for this case
(candidate had `replace` set but `pass=False`); fixed in round.py. The
registry was never corrupted (nothing retired, 51 = 36+15 consistent).

## Rejected (25)

- **S1 (18)** — full candle-anatomy family (upper/lower shadow, asymmetry,
  body: ICIR ≤ 0.26); most conditional splits (by market tail, down-days,
  low-vol days, gap×VR); seasonality echo; 1y band (cov 0.76 also thin);
  listing age; days-since-low; overnight continuation; down-elasticity;
  attention-trough recency; limit_down count (0.29, just under);
  volume-path R² (IC 0.019).
- **S2 (5)** — amt_selfrank~turn_selfrank **0.96**, pvcorr_selfrank~parent
  0.89, turn_medmean~turn_cv 0.75, cv_dispersion~turn_low 0.71,
  ret_on_hivol~semivol_asym 0.72 (the "smart money" split is semivol
  asymmetry in disguise), ret_amp_corr (above).
- **S3 (1)** — vol_share_up dup of signed_attn.

## Distilled

**Successful:** long bands (quarterly reversal, yearly volume clock);
limit-board event family; cross-quantity correlations; interaction
template 4-for-6. **Forbidden:** candle anatomy; self-rank within the
same construct; seasonality/1y-band/listing-age/market-state conditioning.

## Next

OHLCV transform space is visibly depleting (S1 pass rate 55%, S2 kill
rate rising, diversity 0.90→0.842). The moneyflow / northbound / margin
base extension is the next move (already coded; building caches now).
