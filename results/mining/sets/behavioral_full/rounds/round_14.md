# behavioral_full — Round 14

**Goal:** continue Round 13 — robust factors for BOTH 2017-2025 and 2026,
**no overnight-gap**. Round 13 showed median/mean **RATIO** (bounded, low-turnover)
is robust+efficient while the **GAP** is valid-but-not-tradable, and turnover-spike
rarity is live. This round pushes median/mean RATIOs and **activity CV** (bounded
dispersion of volume-like quantities) on fresh quantities, plus event-rarity at
fresh thresholds. Drops couplings (dead under neutralization).

## Funnel

| stage | pass | rejected |
|---|---|---|
| candidates | 19 | — |
| S1 quick IC | 12 | 7 (below 0.03 after neutralized gating) |
| S2 set-correlation | 7 | 5 (median/mean ratios of vol/turn/amount co-lock vs alpha_0146; calm-3x lock vs alpha_0144) |
| S3 intra-round dedup | 6 | 1 (cv_turnf_120 dup of cv_relamount_120) |
| S4 robustness | **4** | 2 (med_amount_ratio_120 OOS 0.023<0.03; volume_trend_ratio mono −0.41) |

Set size **113 → 117**; diversity 0.769. Evaluation parameters identical to
Round 13 (label fwd_ret_10d, GATE_ON_NEUTRALIZED, S1 0.03/0.30/0.60, S2/S3 0.70,
S4 6-test incl. monotonicity ≥0.60; cost_aware reported).

## Accepted (4) — with the 2026 cross-check

| factor | vein | expression | IS IC | ICIR | OOS IC | mono | **2026 sIC** | **2026 net** | turn | robust BOTH |
|---|---|---|---|---|---|---|---|---|---|---|
| alpha_0155 | range-CV | `-TsStd(AMP,120)/TsMed(AMP,120)` | +0.038 | 0.42 | +0.031 | 1.00 | **+0.101** | **+22.7%** | 0.33 | ✅ |
| alpha_0153 | activity-CV | `-TsStd(AMOUNT/TsMean(AMOUNT,20),120)` | +0.053 | 0.69 | +0.045 | 0.99 | **+0.080** | **+5.9%** | 0.31 | ✅ |
| alpha_0152 | robust ratio | `TsMed(VR,60)/TsMean(VR,60)` | +0.040 | 0.67 | +0.044 | 0.99 | **+0.062** | **+8.8%** | 0.52 | ✅ |
| alpha_0154 | event-rarity | `-TsCount(VR>3,120)` | +0.034 | 0.57 | +0.034 | 0.98 | +0.053 | n/a (turn 0.84) | 0.84 | valid only |

**2026 outcome: 4/4 valid, 3/4 also efficient.** The activity-CV / liquidity-shape
constructs (range-CV, relative-amount-CV, VR ratio) are all robust in both periods
and tradable net of cost; only the high-turnover VR>3 rarity is cost-eaten.

## Rejects by tier

- **S1 (7):** `med_absret_ratio` +0.009, `med_amp_ratio` +0.029 (just under),
  `med_relvol`/`med_relamount` wrong-signed, `med_relturnf` +0.017,
  `calm_ret3sigma` +0.015, `relvol_skew` +0.012.
- **S2 (5):** `med_volume_ratio_60` (0.94) & `med_turnf_ratio_60` (0.93) lock vs
  **alpha_0146** — median/mean ratios of volume-like quantities are one signal;
  `cv_vr_60` (0.79) vs alpha_0151; `calm_turnf3`/`calm_amount3` (0.82/0.84) vs
  **alpha_0144**.
- **S4 (2):** `med_amount_ratio_120` OOS 0.023 < 0.03; `volume_trend_ratio`
  monotonicity −0.41 (< 0.60).

## Lessons (distilled)

1. **Activity-stability / liquidity-shape is the robust+efficient non-overnight
   meta-vein.** CV (dispersion) and median/mean ratio of volume-like quantities:
   erratic/spiky liquidity → fragile → underperforms; calm/stable → outperforms.
   Best of the whole campaign: `-TsStd(AMP,120)/TsMed(AMP,120)` (range-CV,
   median-scaled) — 2026 net **+22.7%**, turnover 0.33.
2. **One representative per liquidity-spikiness concept** — median/mean ratios of
   VOLUME/TURN_F/AMOUNT co-lock (~0.93); only genuinely distinct quantities
   (VR-ratio, range-CV) clear S2. Rounds 13→14 are now each other's S2 walls.
3. High-turnover rarity (VR>3) stays valid but is cost-eaten — the turnover/cost
   filter keeps pushing the winners toward the low-turnover shape/stability veins.
