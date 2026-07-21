# behavioral_full — Round 13

**Goal:** find factors robust in BOTH 2017-2025 (the gates) AND the fresh 2026
window, **avoiding the overnight-gap vein** (`OPEN/Delay(CLOSE,1)-1`). Candidates
target the veins that both still-mint and survived the 2026 screen
([[VALID_2026.md]]): event-rarity ("calm"), robust/median, cross-quantity
coupling, on FRESH quantities, plus a few new structural classes.

## Funnel

| stage | pass | rejected |
|---|---|---|
| candidates | 27 | — |
| S1 quick IC | 15 | 12 (IC/ICIR below bar after neutralized gating) |
| S2 set-correlation | 9 | 6 (S2-lock vs residents; 1 exact 1.00 dup) |
| S3 intra-round dedup | 8 | 1 (calm_amount_120 dup of calm_turnf_120) |
| S4 robustness | **8** | 0 |

Set size **105 → 113**; diversity 0.772.

## Evaluation parameters (all gates)

- Label `fwd_ret_10d` (t+1 vwap, suspension-aware); full-A `tradable_entry`;
  daily Spearman rank IC; **`GATE_ON_NEUTRALIZED=True`** (S1/S4 score the
  size+industry neutralized signal).
- Windows: IS 2017-2021 · OOS-gate 2022-2023 · holdout 2024-2025 (snapshot,
  not gated) · **2026 = fresh screen (below)**.
- S1 |IS IC|≥0.03, |ICIR|≥0.30, cov≥0.60. S2 |corr|<0.70 vs 105 residents
  (1.3× replacement). S3 dedup 0.70. S4: OOS same-sign ≥max(0.03, 0.4×|IS|);
  ≥2/3 sub-universes {HS300,CSI500,CSI1000} same-sign ≥0.005; yearly sign-rate
  ≥0.60; rolling 120d/step-20 sign-rate ≥0.70; block bootstrap B=1000/block=10/
  seed=11/p≤0.05; **decile-monotonicity ≥0.60**. cost_aware_score reported
  (net long-excess @15bp), gate off.

## Accepted (8) — with the 2026 cross-check

| factor | vein | expression | IS IC (neut) | ICIR | OOS IC | mono | net@15bp | **2026 sIC** | **2026 net** | robust BOTH |
|---|---|---|---|---|---|---|---|---|---|---|
| alpha_0144 | event-rarity | `-TsCount(TURN_F > 2*TsMean(TURN_F,60), 120)` | +0.045 | 0.59 | +0.049 | 1.00 | +2.9% | **+0.071** | **+15.4%** | ✅ |
| alpha_0146 | robust (ratio) | `TsMed(AMOUNT,60)/TsMean(AMOUNT,60)` | +0.038 | 0.57 | +0.030 | 0.98 | +1.1% | **+0.057** | **+8.3%** | ✅ |
| alpha_0151 | persistence | `-TsStd(AMOUNT/TsMean(AMOUNT,20),60)` | +0.059 | 0.80 | +0.050 | 0.98 | +7.0% | +0.073 | −0.6% | valid only |
| alpha_0147 | robust (gap) | `TsMean(AMP,60)-TsMed(AMP,60)` | −0.059 | −0.77 | −0.070 | −0.96 | +1.1% | +0.061 | −7.8% | valid only |
| alpha_0148 | robust (gap) | `TsMean(Abs(RET),120)-TsMed(Abs(RET),120)` | −0.056 | −0.48 | −0.082 | −0.99 | +3.5% | +0.056 | −11.0% | valid only |
| alpha_0149 | robust (gap) | `TsMean(AMOUNT,120)-TsMed(AMOUNT,120)` | −0.059 | −0.50 | −0.065 | −0.78 | +1.6% | +0.051 | −10.1% | valid only |
| alpha_0145 | flow coupling | `-TsCorr(MF_NET,AMP,60)` | +0.031 | 0.59 | +0.039 | 0.71 | −3.5% | +0.106 | n/a | valid only |
| alpha_0150 | systematic | `-TsStd(RegBeta(RET,BENCH_RET,20),60)` | +0.044 | 0.42 | +0.076 | 0.92 | −0.0% | +0.024 | −11.5% | **neither** |

**2026 outcome: 7/8 stay valid, but only 2/8 are also efficient** (alpha_0144
turnover-spike rarity, alpha_0146 dollar-volume median/mean ratio). These two
are the round's deliverable — genuinely new, robust in both periods, tradable
net of cost, and NOT overnight-gap.

## Rejects by tier

- **S1 (12):** coupling correlations mostly neutralize to ~0 (`coup_turnf_absret`
  ±0.00, `coup_amp_vr` −0.007, `coup_mflg_turnf` +0.005); flow-shock frequency
  weak (+0.005); vwap-dev calm +0.025; volume-clustering ±0.01; downmkt-disp
  +0.002; mom_per_attention −0.031 (wrong-signed vs intent).
- **S2 (6):** `calm_amount_60`/`calm_retshock_60/120` lock vs existing event
  reps (0.80-0.82); `coup_vr_ret_120` = **exact 1.00 dup of alpha_0113**;
  `coup_mfsm_ret_60` 0.79 vs alpha_0124; `rsq_bench_120` locks vs systematic
  resident.
- **S3 (1):** `calm_amount_120` dup of `calm_turnf_120` (kept the stronger).

## Lessons (distilled to memory)

1. **Turnover-spike rarity** (`-TsCount(TURN_F>2·mean,120)`) is a genuinely new
   robust event_freq quantity — clears S2, and is the round's best 2026 result
   (+15% net). Calm-attention names outperform. The amount/return-shock variants
   S2-lock against existing amp/vr/volume reps.
2. **Median/mean RATIO of dollar volume** extends the robust family to AMOUNT and
   is efficient in 2026; the **mean-median GAP** versions are *valid but not
   tradable* (turnover eats them). **Validity ≠ tradability — prefer bounded
   RATIO over GAP.**
3. **Coupling correlations are largely dead under neutralized gating** (size/
   industry residualization removes attention-risk couplings; one was an exact
   dup). **Systematic-share / beta-instability is regime-dependent** — strong in
   2017-25 (OOS 0.076) but decays below the 2026 bar.
