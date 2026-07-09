# Round 1 — 2026-07-06

First round: experience memory was empty, so the batch deliberately spanned
9 families (20 candidates) to seed both pattern buckets.

**Funnel: 20 → S1 18 → S2 18 (set empty) → S3 13 → S4 13 accepted.**
Alpha set: 13 factors, diversity eigen-entropy **0.90**. Runtime 25 min.

## Accepted factors

IC = daily rank IC vs `fwd_ret_10d`, full-A `tradable_entry` universe.
LS = mean 10-day top-minus-bottom decile spread (non-overlapping).
Direction −1 = trade the flipped sign of the expression.

| name | expression | dir | IS IC / ICIR | OOS22-23 IC / ICIR | IS LS | OOS LS | rank-AC 10d | PFS | decay 1/5/10/20d |
|---|---|---|---|---|---|---|---|---|---|
| alpha_0001 | `-TsMean(TURN_F, 20)` | + | 0.090 / 0.59 | 0.080 / 0.54 | 1.24% | 1.27% | 0.92 | 0.95 | .045/.070/.087/.107 |
| alpha_0002 | `-(TsMean(TURN_F,5)/TsMean(TURN_F,60))` | + | 0.038 / 0.37 | 0.050 / 0.47 | 0.60% | 0.54% | 0.41 | 0.87 | .031/.039/.041/.044 |
| alpha_0003 | `-(TsStd(TURN_F,20)/TsMean(TURN_F,20))` | + | 0.049 / 0.68 | 0.042 / 0.72 | 0.82% | 0.22% | 0.42 | 0.81 | .034/.044/.047/.048 |
| alpha_0004 | `-TsCorr(CsRank(CLOSE),CsRank(VOLUME),10)` | + | 0.064 / 0.97 | 0.039 / 0.53 | 0.95% | 0.39% | 0.17 | 0.94 | .036/.050/.057/.064 |
| alpha_0005 | `-TsCorr(TsRank(CLOSE,10),TsRank(VOLUME,10),10)` | + | 0.060 / 0.79 | 0.036 / 0.44 | 0.83% | 0.16% | 0.17 | 0.94 | .033/.044/.053/.066 |
| alpha_0006 | `-TsCorr(TURN_F, RET, 20)` | + | 0.032 / 0.40 | 0.048 / 0.64 | 0.26% | 0.70% | 0.38 | 0.96 | .024/.031/.037/.044 |
| alpha_0007 | `-TsMax(RET, 20)` | + | 0.083 / 0.74 | 0.091 / 0.72 | 0.95% | 0.92% | 0.61 | 0.91 | .053/.074/.085/.098 |
| alpha_0008 | `-TsSkew(RET, 60)` | + | 0.037 / 0.49 | 0.040 / 0.67 | 0.66% | 0.28% | 0.78 | 0.99 | .025/.034/.038/.042 |
| alpha_0009 | `CsIndNeutralize(CsRank(EP), IND)` | + | 0.041 / 0.34 | 0.018 / 0.16 | 0.21% | −0.10% | 0.97 | 0.98 | .023/.029/.034/.041 |
| alpha_0010 | `-TsSum(OPEN/Delay(CLOSE,1)−1, 20)` | **−** | −0.028 / −0.40 | −0.027 / −0.44 | −0.50% | −0.43% | 0.56 | 0.98 | −.013/−.021/−.028/−.036 |
| alpha_0011 | `-TsSum(CLOSE/OPEN−1, 20)` | + | 0.066 / 0.53 | 0.071 / 0.57 | 1.21% | 1.21% | 0.48 | 0.98 | .041/.058/.068/.081 |
| alpha_0012 | `CsRank(HighDay(CLOSE, 60))` | + | 0.034 / 0.33 | 0.029 / 0.25 | 0.57% | 0.53% | 0.60 | 0.93 | .019/.030/.033/.036 |
| alpha_0013 | `-TsMean(CLOSE/VWAP−1, 10)` | + | 0.032 / 0.31 | 0.025 / 0.26 | 1.21% | 1.01% | 0.08 | 0.98 | .025/.027/.030/.035 |

All 13: 3/3 sub-universes passed except alpha_0013 (2/3); 7/7 same-sign
yearly IC 2017–2023 (a NaN-year denominator bug initially printed 0.78; fixed
in `alphaseval.yearly_ic`, artifacts patched).

## Rejected

- **S1** — `rev_path` (sign-count reversal, ICIR 0.21), `bp_ind`
  (book-to-price, ICIR 0.24).
- **S3 dedup** — `rev20`, `rev20_ind` → duplicates of `intraday_rev`
  (alpha_0011); `lowvol`, `amp_low` → duplicates of `max_eff` (alpha_0007);
  `ivol` → duplicate of `turn_low` (alpha_0001).

## Distilled (written to experience_memory.json)

**Successful:** turnover/attention axis dominant but near saturation;
tail/lottery (TsMax, skew) beats plain vol; price-volume agreement
correlations = best ICIR; **leg decomposition** — intraday leg carries
reversal (subsumed whole-return reversal), overnight leg is *momentum*
(sign flipped vs. intuition); within-industry EP is the one value survivor.

**Forbidden:** sign-only path reversal; BP at 10d; standalone vol/amp/ivol
variants (collapse into max_eff/turnover); whole-return 1-month reversal;
>2 candidates per family per round (over-saturation).

## Notes for Round 2

- Untouched raw material: moneyflow, hk_hold (northbound), margin_detail —
  needs a small base extension before use.
- Try: leg decomposition applied to other signals; conditional/interaction
  forms (e.g. reversal conditioned on turnover); vol-of-vol and up/down
  asymmetry; growth from forecast/express (coverage-gated); slower
  fundamental factors probably want the 20d label variant.
- alpha_0009 (EP) OOS decay is heavy (0.041→0.018, LS negative OOS);
  watch it — a future correlated-but-stronger factor should replace it
  via the 1.3× rule.
