# Round 10 — 2026-07-07 (40 candidates, first round under the 0.03 standard)

Context: before this round the user raised the IC standard to
**|IC| ≥ 0.03 in both IS and OOS** — 34 factors purged (set 103 → 69),
`S1_MIN_ABS_IC` and `S4_MIN_OOS_ABS_IC` raised to 0.03. This round is
pure exploitation of proven high-IC classes: bands of champions,
robust/median, terms/shapes, strong couplings, long-window events.

**Funnel: 40 → S1 25 → S2 13 → S3 13 → S4 12 accepted.**
Alpha set: **81 factors**, diversity **0.793**. Runtime 53 min (plus one
aborted run — see incident note below).

## Accepted (12)

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR | rank-AC 10d |
|---|---|---|---|---|---|
| alpha_0107 | `-TsMax(CLOSE/VWAP−1, 60)` | + | 0.081 / 0.68 | 0.077 / 0.53 | 0.86 |
| alpha_0108 | `-TsMax(RET, 60)` | + | 0.077 / 0.65 | **0.080 / 0.60** | 0.85 |
| alpha_0109 | `-TsMin(RET, 60)` | − | −0.048 / −0.31 | −0.058 / −0.41 | 0.86 |
| alpha_0110 | `TsMed(gap, 20)` | + | 0.042 / 0.67 | 0.043 / 0.66 | 0.54 |
| alpha_0111 | `TsMed(CLOSE/OPEN−1, 20)` | − | −0.039 / −0.40 | −0.041 / −0.37 | 0.45 |
| alpha_0112 | `-TsCorr(TURN_F, Delay(RET,1), 120)` | + | 0.047 / 0.51 | 0.041 / 0.52 | 0.88 |
| alpha_0113 | `-TsCorr(RET, VR, 120)` | + | 0.036 / 0.49 | 0.037 / 0.49 | 0.92 |
| alpha_0114 | `-TsCorr(TURN_F, TsStd(RET,5), 120)` | + | 0.036 / 0.59 | 0.031 / 0.40 | 0.90 |
| alpha_0115 | `-TsCorr(CLOSE/VWAP−1, AMP, 20)` | + | 0.044 / 0.63 | 0.050 / 0.70 | 0.46 |
| alpha_0116 | `-(TsStd(TURN_F·(RET>0),20) − TsStd(TURN_F·(RET<0),20))` | + | 0.065 / **0.81** | 0.068 / **0.80** | 0.45 |
| alpha_0117 | `-TsMean((CLOSE/VWAP−1)·(VR>1), 60)` | + | 0.051 / 0.63 | 0.048 / 0.63 | 0.84 |
| alpha_0118 | `-TsSum(RET·(TURN_F>TsMean(TURN_F,60)), 60)` | + | 0.065 / 0.58 | **0.082 / 0.71** | 0.80 |

Highlights:

- **ret_on_hivol60** (alpha_0118): returns earned on high-attention days,
  quarterly — OOS 0.082, OOS-stronger than IS. The 20d version died at S2
  in R5 (semivol proxy); the quarterly band is its own animal.
- **turn_updown_asym** (alpha_0116): a NEW construct class — masked-std
  asymmetry (turnover volatility on up-days minus down-days) — ICIR 0.81
  IS / 0.80 OOS, the most stable factor of the round.
- **Quarterly tails clear next to their 20d siblings** (max_eff60,
  aggr_max60, min_eff60 at ~0.65 corr): tail bands decorrelate.
- Fast (20d) median drifts of both legs accepted; 120d coupling bands
  accepted (lag_chase120, ret_vr_corr120, attn_risk_corr120).

## Rejected (28)

- **S1 (15)** — all four champion-parent interactions (|IC| 0.007–0.027:
  under the 0.03 bar the interaction class is effectively dead), term
  ratios (gapvol/idvol/turnvol/vr terms — ICs 0.02–0.028 too thin now),
  med_band240 (ICIR 0.21), mean_med_gap120, vr_med60, gap_vr_corr,
  maxfreq250, vr_burst250, limit_dn_mag.
- **S2 (12)** — shape variants of residents: medvol~hl_med60 0.89,
  upvol_share~semivol 0.95, downvol60~hl_med60 0.78, idvol60~turn_low
  0.72, hl_med20~turn_low 0.72, hl_max~max_eff 0.71, gap_min~gap_vol
  0.79, vol_clock60~vol_clock 0.78, id_vr_corr~ret_vr_corr 0.89,
  mf_id_corr60 0.81, amp_term_slow 0.87, intraday_skew~semivol60 0.75
  (the unlocked retry failed against the replacement factor).
- **S4 (1)** — limit_touch250: OOS 0.026 < 0.03, the new OOS bar's first
  kill.

## Incident note

The first execution of this round crashed twice with filesystem
`TimeoutError [Errno 60]`: iCloud "Optimize Mac Storage" had evicted the
git-ignored `data/mining/alpha_values/` store (~6.7GB) from the synced
Desktop. Fix: 37 retired factors' value files deleted, remaining 69
materialized via `brctl download`, converted to float32 (half size), and
relocated to `~/quant_local/` (outside iCloud) with a symlink at the old
path; `registry.values()` gained a retry guard, and new factor values are
written float32. The rerun completed cleanly.

## Distilled

**Successful:** quarterly conditional aggregations; masked-std
asymmetries (new class); 60d tails decorrelate from 20d; 120d coupling
bands. **Forbidden:** shape/term variants of residents (S2); interactions
under the 0.03 bar; 250d event counts (OOS decay).
