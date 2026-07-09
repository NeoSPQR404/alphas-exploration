# Round 11 — 2026-07-08 (40 candidates)

Themes: conditional aggregations + masked-std asymmetries across
quantities, idiosyncratic (RegResi) structures, robust midrange tails,
120d bands. (Run interrupted twice: once by user request before any
evaluation, once by iCloud eviction of `data/_wide_cache` — which
triggered the full relocation of `data/` to `~/quant_local` with a
symlink; final rerun clean.)

**Funnel: 40 → S1 25 → S2 14 → S3 14 → S4 14 accepted.**
Alpha set: **95 factors**, diversity **0.781**. Runtime 58 min.

## Accepted (14)

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR | rank-AC 10d |
|---|---|---|---|---|---|
| alpha_0119 | `-TsSum(RET·(TURN_F>mean120), 120)` | + | 0.055 / 0.47 | **0.083 / 0.71** | 0.89 |
| alpha_0120 | `-TsCount((VR>1)·(RET>0), 60)` | + | 0.046 / 0.47 | 0.044 / 0.38 | 0.79 |
| alpha_0121 | `-(TsStd(AMP·(RET>0),20) − TsStd(AMP·(RET<0),20))` | + | 0.072 / **0.94** | 0.076 / **0.86** | 0.47 |
| alpha_0122 | `-(TsStd(TURN_F·(RET>0),60) − …(RET<0),60))` | + | 0.063 / 0.69 | 0.059 / 0.64 | 0.79 |
| alpha_0123 | `-TsSum(RegResi(RET,BENCH,60), 20)` (idio rev) | + | 0.041 / 0.35 | 0.043 / 0.36 | 0.41 |
| alpha_0124 | `-TsCorr(MF_LG_NET, RET, 120)` | + | 0.041 / 0.36 | 0.056 / 0.58 | 0.98 |
| alpha_0125 | `-(TsMed(H/L−1,20)/TsMed(H/L−1,120))` (hl term) | + | 0.039 / 0.41 | 0.035 / 0.28 | 0.70 |
| alpha_0126 | `-(TsStd(RET,5)/TsStd(RET,250))` | + | 0.042 / 0.50 | 0.053 / 0.51 | 0.22 |
| alpha_0127 | `semivol asym, 120d` | + | 0.050 / 0.45 | **0.079 / 0.77** | 0.90 |
| alpha_0128 | `TsMed(gap, 120)` | + | 0.044 / 0.59 | 0.050 / 0.58 | 0.88 |
| alpha_0129 | `-TsMean(Sign(RET)·VR, 120)` | + | 0.041 / 0.47 | 0.030 / 0.25 | 0.91 |
| alpha_0130 | `-TsCount(RET > 2·std60, 120)` | + | 0.043 / 0.47 | 0.052 / 0.55 | 0.91 |
| alpha_0131 | `-TsCount(AMP > 2·mean60, 120)` | + | 0.040 / 0.49 | 0.034 / 0.34 | 0.93 |
| alpha_0132 | `TsMin(CLOSE/VWAP−1, 60)` | + | 0.056 / 0.37 | 0.063 / 0.42 | 0.87 |

Highlights: **amp_updown_asym** (alpha_0121) is the round's quality
star — ICIR 0.94 IS / 0.86 OOS; **ret_on_hivol120** and **semivol120**
are OOS-stronger than IS; **mf_ret_corr120** rescued the flow-coupling
band whose 60d version died at corr; **idio_rev** is the first
market-residual factor in the set.

## Rejected (26)

- **S1 (15)** — midrange-median tails (all 3), mf_on_down60,
  aggr_on_down60, gap_on_hivr60, gap_after_down, mf_updown_asym,
  idio_med, gapabs_turn_corr60, gap_vr_corr60, turn_gap_corr,
  aggr_attn_corr120, gapdn_freq120, hl_med250.
- **S2 (11)** — the key discovery: **60d conditional return sums are
  intr_mom60 in disguise** (ret_on_hivr60 / ret_on_hiamp60 /
  id_on_hivol60 all ~0.70–0.75 vs alpha_0045) while the 120d tier
  escapes; idio_max~max_eff 0.91 (only *reversal* transfers to
  residuals); vr_updown_asym~signed_attn 0.71; plus 120d event-count
  collisions (flat_open120, vr_burst120, limit_touch120, aggr_hi_vr120,
  amp_on_down, mf_sm_amp_corr).

## Distilled

**Successful:** the 120d tier is a full vein (conditionals, asymmetries,
couplings, semivol, medians, counts); masked-std asymmetry generalizes
across quantities; idio reversal works. **Forbidden:** 60d conditional
return sums (intr_mom60 aliases); midrange-median tails; down-day
conditional means; only reversal transfers to residuals.
