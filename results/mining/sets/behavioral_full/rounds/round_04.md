# Round 4 — 2026-07-07 (40 candidates)

First large round (40). **Funnel: 40 → S1 26 → S2 17 → S3 14 → S4 12.**
Alpha set: 36 factors, diversity eigen-entropy **0.848**. Runtime 32 min.

## Accepted factors

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR | rank-AC 10d |
|---|---|---|---|---|---|
| alpha_0025 | maxfreq × turn_selfrank interaction | − | −0.045 / −0.69 | −0.028 / −0.53 | 0.32 |
| alpha_0026 | `-RegBeta(Abs(RET), TURN_F, 20)` (fragility) | − | −0.066 / −0.65 | −0.045 / −0.44 | 0.64 |
| alpha_0027 | `-TsCorr(TURN_F, Delay(RET,1), 20)` (lag chase) | + | 0.053 / 0.69 | 0.050 / 0.54 | 0.42 |
| alpha_0028 | `-TsRank(TsStd(gap,20), 120)` (gap-vol self-rank) | + | 0.038 / 0.55 | 0.033 / 0.41 | 0.50 |
| alpha_0029 | `-TsMean(|gap|/AMP, 20)` (overnight share) | + | 0.042 / 0.71 | 0.020 / 0.36 | 0.60 |
| alpha_0030 | `-TsMin(RET, 20)` (MIN mirror) | − | −0.048 / −0.32 | −0.053 / −0.39 | 0.63 |
| alpha_0031 | `-TsCount(limit_up_touch>0.5, 60)` | + | **0.077 / 0.72** | **0.057 / 0.66** | 0.88 |
| alpha_0032 | `-(TsStd(RET,5)/TsStd(RET,60))` (vol term) | + | 0.027 / 0.34 | 0.034 / 0.39 | 0.11 |
| alpha_0033 | `-(CLOSE/TsMed(CLOSE,20)−1)` (median reversal) | + | 0.045 / 0.34 | 0.051 / 0.41 | 0.18 |
| alpha_0034 | `-TsMean(VR, 20)` (volume-ratio attention) | + | 0.044 / 0.51 | 0.040 / 0.46 | 0.24 |
| alpha_0035 | `TsRank(Amihud20, 120)` (illiquidity self-rank) | + | 0.040 / 0.41 | **0.049 / 0.41** | 0.66 |
| alpha_0036 | `-(TsCorr(RET,BENCH,60)²)` (systematic share) | − | −0.051 / −0.49 | −0.050 / −0.41 | 0.87 |

Headline: **limit_up_touch count** is the best new factor (new field, not
new transform — its decile LS is NaN due to massive ties at zero touches;
rank IC is the honest metric for it). **Amihud rescued** by TS self-rank
after failing as a level in R2. **Systematic share (R²)** works with the
anti-intuitive positive sign where beta and semibeta both died.

## Rejected (28)

- **S1 (14)** — all six quality/value levels (ROE 0.20, op-margin 0.17,
  cash 0.09, leverage 0.00, SP 0.25, FCFP 0.24), anchor/position family
  (hi52, dd_depth, vwap_pos, open_pos, gap_fade), semibeta_asym,
  pv_slope_div, free_float, ix_rev5_volresp, wma_cross (0.30 icir, IC ok
  but under).
- **S2 (9)** — monotone-transform deaths: outlier_habit→max_eff 0.78,
  ampresp→turn_low 0.78, turn_conc→turn_cv 0.91, rev_skip→intraday_rev
  0.89, intraday_skew→skew 0.74 (predicted: leg lesson generalizes),
  upmove_share 0.79, amp_spike 0.75, turn_trend 0.70, volresp_asym 0.74.
- **S4 (2)** — ep_tsrank (2/3 universes, OOS 0.010), fc_mid (OOS −0.011,
  year-rate 0.57: guidance is regime-dead like all earnings-linked
  signals).

## Distilled

**Successful:** new FIELDS beat new transforms (limit_up_touch, VR);
TS self-rank rescues failed levels (Amihud) and dodges saturation; MIN
mirror = crash continuation; R² systematic share (anti-intuitive sign);
lag/direction changes decorrelate elasticity, up/down splits don't.

**Forbidden:** ALL fundamental levels beyond EP/CFP (quality dead at 10d);
guidance; monotone transforms of accepted quantities (9 corr kills);
anchor/position family.

## Notes for Round 5

- Structurally new classes to try: conditional aggregation (returns earned
  on high- vs low-attention days), candle anatomy (shadows/body), more
  limit-board fields (limit_down, one_word_board), event-recency
  (HighDay on limit touches), seasonality echo.
- Then: the moneyflow / hk_hold / margin base extension is the real next
  frontier — behavioral transforms of OHLCV are visibly depleting
  (diversity 0.90 → 0.848, S2 kill-rate rising).
