# Round 2 — 2026-07-07

Memory-guided round: exploit leg decomposition / tail / interaction
patterns, probe untouched axes (beta, size, illiquidity, fundamentals),
≤2 candidates per family.

**Funnel: 19 → S1 10 → S2 8 → S3 8 → S4 7 accepted.**
Alpha set: 20 factors, diversity eigen-entropy **0.879**. Runtime 15 min.
Year-sign rates now read 1.00 (the round-1 NaN-denominator fix verified).

## Accepted factors

| name | expression | dir | IS IC / ICIR | OOS22-23 IC / ICIR | IS LS | OOS LS | rank-AC 10d | PFS | decay 1/5/10/20d |
|---|---|---|---|---|---|---|---|---|---|
| alpha_0014 | `TsSum(OPEN/Delay(CLOSE,1)−1, 60)` | + | 0.042 / 0.52 | 0.035 / 0.47 | 0.78% | 0.65% | 0.87 | 0.98 | .017/.030/.040/.053 |
| alpha_0015 | `-TsStd(OPEN/Delay(CLOSE,1)−1, 20)` | + | 0.070 / 0.54 | **0.085 / 0.68** | 0.74% | 0.99% | 0.71 | 0.89 | .044/.063/.074/.086 |
| alpha_0016 | `-(TsStd((RET+Abs(RET))/2,20) − TsStd((RET−Abs(RET))/2,20))` | + | 0.062 / 0.58 | 0.067 / 0.74 | 1.12% | 0.87% | 0.44 | 0.98 | .040/.056/.063/.071 |
| alpha_0017 | `CsRank(HighDay(TURN_F, 60))` | + | 0.041 / 0.60 | 0.032 / 0.40 | 0.72% | 0.29% | 0.49 | 0.93 | .025/.036/.038/.039 |
| alpha_0018 | `(CsRank(-TsSum(CLOSE/OPEN−1,20))−.5)×(CsRank(-TsMean(TURN_F,20))−.5)` | **−** | −0.035 / −0.65 | **−0.048 / −0.90** | −0.91% | −1.22% | 0.40 | 0.99 | −.017/−.031/−.038/−.046 |
| alpha_0019 | `(CsRank(-TsMax(RET,20))−.5)×(CsRank(-(TsMean(TURN_F,5)/TsMean(TURN_F,60)))−.5)` | **−** | −0.037 / −0.83 | −0.028 / −0.64 | −0.73% | −0.63% | 0.22 | 0.99 | −.018/−.029/−.034/−.038 |
| alpha_0020 | `CsIndNeutralize(CsRank(CFP), IND)` | + | 0.033 / 0.36 | 0.030 / 0.28 | 0.34% | 0.20% | 0.96 | 0.98 | .018/.025/.032/.041 |

Highlights: **gap_vol** (alpha_0015) and **updown_asym** (alpha_0016) are
OOS-stronger than IS; both **interaction terms** came out with *negative*
sign — names where the two bullish parent signals agree underperform
(agreement = crowding?), with near-zero correlation to their parents
(max set-corr 0.17) and the best OOS ICIR of the round (−0.90).

## Rejected

- **S1 (9)** — `kurt` (−0.12), `turn_amp_corr` (IC 0.017), `ret_autocorr`
  (−0.09), `amihud` (ICIR 0.18), `sue_ttm` (IC 0.018, cov 0.86),
  `low_beta` (0.08), `resi_trend` (0.08), `rsq_choppy` (−0.08),
  `close_pos` (0.12), `size_nl` (−0.26).
- **S2 (2)** — `max_intraday` corr 0.90 vs alpha_0007 (1.02× IC, below the
  1.3× replacement bar); `vol_of_vol` corr 0.72 vs alpha_0007.

## Distilled

**Successful (new):** demeaned-rank interaction template (low parent corr
by construction, strong ICIR, negative sign = agreement is bearish);
semivol asymmetry is the one orthogonal vol construct; attention duration
(HighDay on turnover) orthogonal to turnover level; CFP value decays less
than EP. **Reinforced:** leg decomposition (but don't leg-decompose MAX).

**Forbidden (new):** classic slow premia (beta / size shape / Amihud) at
10d; the entire price-path-shape family (trend residual, R², autocorr,
close position); kurtosis; rolling-TTM earnings momentum (needs
announcement-dated surprise instead).

## Notes for Round 3

- Interaction template with other parent pairs (e.g. gap_vol × turnover,
  semivol × value); try 3-way ranks cautiously.
- Announcement-dated earnings surprise from forecast/express (event-based,
  not rolling TTM) — needs a small data-prep step.
- Moneyflow / hk_hold / margin_detail base extension remains the biggest
  untapped material.
- Set is 20 factors; consider starting a combined-alpha (equal-weight rank
  composite) tracking artifact and a per-family concentration report.
