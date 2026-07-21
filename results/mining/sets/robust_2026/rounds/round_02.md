# robust_2026 — Round 2

**Goal:** the core low-turnover veins are saturated (R1), so mine less-covered
territory: lottery/peak, peak-timing (HighDay), downside/tail asymmetry. 15
candidates, no overnight-gap.

## Funnel

| stage | pass | note |
|---|---|---|
| candidates | 15 | — |
| S1 | 12 | 3 below 0.03 (amp-skew, intermediate-mom, crash-day-rarity) |
| S2 | 9 | 3 lock (relturnf/relamount peak 0.98–0.99 vs ralpha_0026; vr_peak 0.72) — low-corr veins clear easily |
| S3 | 7 | amp_max dup of ret_max; ret_skew dup of semivol_asym |
| S4 | **5** | amp_peak_recency (OOS 0.019) & vol_rank (mono −0.07) fail |

Accepted → ralpha_0027-0031: `ret_max_20`, `vol_peak_recency_60`,
`turnf_peak_recency_120`, `downsemivol_60`, `semivol_asym_ret_60`. Set 26 → 31.
**All 5 had negative cost-aware net at S4** (high-turnover veins).

## 2026 cross-check — none survive

| factor | expr | 2026 sIC | 2026 net | verdict |
|---|---|---|---|---|
| ralpha_0027 | `-TsMax(RET,20)` (MAX lottery) | +0.048 | −23.1% | valid only |
| ralpha_0031 | `TsStd(RET·up)−TsStd(RET·down)` | +0.048 | −7.7% | valid only |
| ralpha_0030 | `-TsStd(RET·(RET<0),60)` | +0.025 | −16.9% | neither |
| ralpha_0028 | `HighDay(VOLUME,60)` | +0.024 | +0.1% | efficient only |
| ralpha_0029 | `HighDay(TURN_F,120)` | +0.014 | −7.8% | neither |

**0/5 valid+efficient in 2026** → all 5 retired.

## Outcome of the campaign (Rounds 1+2)

33 candidates over 2 rounds → **only 1 factor kept** (ralpha_0026, peak relative
volume). The curated `robust_2026` set is **near-optimal by construction**: its
low-turnover efficient veins S2-lock immediately, and the remaining minable veins
(lottery / MAX / timing / downside semivol) are valid in 2017-25 but **too
high-turnover to survive 2026 costs** — validity ≠ tradability, again. The 6
non-qualifying accepts were retired to keep the set true to its criterion
(robust in both periods AND efficient). Set: 24 → **25**.
