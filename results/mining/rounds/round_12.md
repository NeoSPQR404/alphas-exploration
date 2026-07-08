# Round 12 — 2026-07-08 (39 candidates) — 100-FACTOR TARGET MET

Themes: asymmetry family completion across bands, 120d conditional tier,
zero-return illiquidity (Lesmond), idio bands, annual coupling bands.

**Funnel: 39 → S1 32 → S2 14 (+1 replacement) → S3 12 → S4 11 accepted.**
Alpha set: **105 factors** (all with |IC| ≥ 0.03 IS *and* OOS),
diversity **0.776**. Runtime 66 min.

## Accepted (11)

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR |
|---|---|---|---|---|
| alpha_0133 | aggr up/down asym, 20d | + | 0.045 / 0.54 | 0.039 / 0.57 |
| alpha_0134 | amp up/down asym, 60d (replaces alpha_0078) | + | 0.073 / **0.94** | 0.076 / 0.74 |
| alpha_0135 | turnover up/down asym, 120d | + | 0.058 / 0.59 | 0.058 / 0.61 |
| alpha_0136 | `-TsCount(|RET|<0.001, 60)` (zero-return illiq) | − | −0.040 / −0.43 | −0.039 / −0.37 |
| alpha_0137 | `-TsSum(RET·(VR>1), 120)` | + | 0.064 / 0.52 | **0.085 / 0.64** |
| alpha_0138 | attention-up-day count, 120d | + | 0.033 / 0.36 | 0.048 / 0.43 |
| alpha_0139 | idio reversal, 60d | + | 0.053 / 0.46 | 0.039 / 0.33 |
| alpha_0140 | `-TsCorr(RET, AMP, 120)` | + | 0.046 / 0.56 | 0.067 / 0.77 |
| alpha_0141 | `-TsCorr(aggr, AMP, 60)` | + | 0.047 / 0.62 | 0.056 / 0.72 |
| alpha_0142 | aggression-burst count, 120d | + | 0.033 / 0.46 | 0.041 / 0.52 |
| alpha_0143 | `-TsMax(gap, 60)` (quarterly biggest gap-up) | + | 0.044 / 0.44 | 0.062 / 0.56 |

Highlights: **ret_on_hivr120** OOS 0.085; **zeroret_freq** — the Lesmond
zero-return probe — accepted with the illiquidity-premium sign (more
zero-return days → higher forward returns); **4th replacement**:
amp_updown_60 displaced the 20d semivol asymmetry (alpha_0078).

## Rejected (28)

- **S1 (7)** — gap_updown_asym 0.25, flatclose_freq, mf_amp_corr120
  (0.029, just under), aggr_vol_term, min_eff120, mf_abs_med,
  gap_sign_bal (0.61 ICIR but IC 0.025 under the bar).
- **S2 (18!)** — the correlation wall at 100+ factors: amp_term_med
  **1.00** vs hl_term, med_dev_vwap **0.99** vs med_band60,
  mf_ret_corr250 0.88 vs its 120d sibling, idio_min/idio_hivol 0.85+
  vs min_eff/ret_on_hivol60, limit_up_close_ratio 0.82 vs limit_touch,
  max_eff120 / aggr_max120 vs their 60d siblings, and more.
- **S3 (2)** — amp_updown_120 dup of amp_updown_60; zeroret_freq120 dup
  of zeroret_freq.
- **S4 (2)** — attn_dn_cnt OOS 0.021; lag_chase250 OOS 0.022 (the
  annual tier decays below the 0.03 bar).

## Distilled

**Successful:** zero-return illiquidity; asymmetry family complete across
quantities and bands. **Forbidden:** the S2 wall — band extension is
exhausted for most veins; the annual (250d) tier fails OOS; the formulaic
OHLCV+flow space against this 105-factor set is effectively mined out.
Further growth needs new data, replacements, or a different label horizon.

## Milestone

**105 active factors, every one with |rank IC| ≥ 0.03 in-sample AND in
the 2022–23 OOS window** — the user's 0.03 standard, reached across
rounds 10–12 (12 + 14 + 11 accepted after the 34-factor purge).
Diversity 0.776. Four replacements executed lifetime. The 2024–25
holdout remains untouched and unread.
