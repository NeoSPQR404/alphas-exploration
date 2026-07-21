# robust_2026 — Round 1

**Goal:** grow the curated robust+efficient, non-overnight set. S2 is only vs the
24 residents, so proven-vein forms that S2-locked in behavioral_full got another
shot. 18 candidates: activity-CV / liquidity-shape on fresh quantities,
event-rarity, idio/systematic, robust-Sharpe, skew.

## Funnel

| stage | pass | note |
|---|---|---|
| candidates | 18 | — |
| S1 | 12 | 6 below 0.03 (robust-Sharpe, |ret|-shape, skews, outflow-rarity) |
| S2 | 4 | **8 locked** — the activity-CV vein is saturated in the curated set: `hl_cv_med_120` = **1.00 dup of ralpha_0001**; vr/relturnf/relvol/amount CV all 0.73–0.98 vs ralpha_0005; calm_amount 0.92 vs ralpha_0002; rsq 0.78; turnf_cv 0.89 |
| S3 | 4 | — |
| S4 | **2** | idio_sum (mono 0.30) & amp_trend (mono 0.12) fail monotonicity |

Accepted: `calm_retshock_120` → ralpha_0025, `relvol_peak_60` → ralpha_0026.
Set 24 → 26. Params identical to behavioral_full R13-14.

## 2026 cross-check

| factor | expr | 2026 sIC | 2026 net | verdict |
|---|---|---|---|---|
| ralpha_0026 | `-TsMax(VOLUME/TsMean(VOLUME,20),60)` | +0.062 | **+6.9%** | ✅ kept |
| ralpha_0025 | `-TsCount(Abs(RET)>2·std,120)` | +0.038 | −5.3% | valid only → retired |

## Lesson

The curated set is **already saturated in its low-turnover efficient veins** —
activity-CV / median-mean forms S2-lock instantly (one exact dup). Only
peak-relative-volume (a lottery form absent from the residents) cleared and held
in 2026.
