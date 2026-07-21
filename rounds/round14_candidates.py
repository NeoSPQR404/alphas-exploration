"""Round 14 (behavioral_full) — push Round 13's two confirmed robust+efficient
veins, still avoiding overnight-gap.

Round 13 learned: median/mean RATIO (bounded, low-turnover) is robust AND
efficient in 2026, while the mean-median GAP is valid-but-not-tradable; and
turnover-spike rarity is a live event_freq quantity. So this round mines
median/mean RATIOS and median relative-levels on FRESH quantities (VOLUME,
|RET|, TURN_F, AMP, VR), activity-CV (bounded dispersion), and event-rarity at
fresh thresholds/quantities. Drops couplings (die under neutralized gating) and
GAP constructs (cost-inefficient). No OPEN/Delay(CLOSE,1).
"""
SET_NAME = "main"

CANDIDATES = [
    # -- Median/mean RATIO on fresh quantities (the efficient robust construct).
    {"name": "med_volume_ratio_60", "family": "robust", "logic_score": 0.65,
     "expr": "TsMed(VOLUME, 60) / TsMean(VOLUME, 60)",
     "rationale": "Volume distribution skew (median/mean); low = spiky volume, fragile."},
    {"name": "med_absret_ratio_60", "family": "robust", "logic_score": 0.65,
     "expr": "TsMed(Abs(RET), 60) / TsMean(Abs(RET), 60)",
     "rationale": "|Return| median/mean = vol-shape (shock-driven vs steady vol), bounded/robust."},
    {"name": "med_turnf_ratio_60", "family": "robust", "logic_score": 0.6,
     "expr": "TsMed(TURN_F, 60) / TsMean(TURN_F, 60)",
     "rationale": "Turnover distribution skew; fresh quantity vs the VR-ratio resident."},
    {"name": "med_amp_ratio_60", "family": "robust", "logic_score": 0.6,
     "expr": "TsMed(AMP, 60) / TsMean(AMP, 60)",
     "rationale": "Range median/mean RATIO (the GAP version was valid-but-not-efficient; ratio may trade)."},
    {"name": "med_amount_ratio_120", "family": "robust", "logic_score": 0.55,
     "expr": "TsMed(AMOUNT, 120) / TsMean(AMOUNT, 120)",
     "rationale": "Long-band dollar-volume median/mean (the 60d ratio was the R13 winner)."},
    {"name": "med_vr_ratio_60", "family": "robust", "logic_score": 0.5,
     "expr": "TsMed(VR, 60) / TsMean(VR, 60)",
     "rationale": "60d band of the volume-ratio median/mean (band separation vs the 20d resident)."},

    # -- Median relative-LEVEL (robust level of a self-normalized quantity).
    {"name": "med_relvol_60", "family": "robust", "logic_score": 0.6,
     "expr": "TsMed(VOLUME / TsMean(VOLUME, 20), 60)",
     "rationale": "Robust median of relative volume: persistently elevated volume = crowded."},
    {"name": "med_relamount_60", "family": "robust", "logic_score": 0.55,
     "expr": "TsMed(AMOUNT / TsMean(AMOUNT, 20), 60)",
     "rationale": "Robust median of relative dollar volume."},
    {"name": "med_relturnf_neg_120", "family": "robust", "logic_score": 0.55,
     "expr": "-TsMed(TURN_F / TsMean(TURN_F, 20), 120)",
     "rationale": "Persistent high relative turnover = crowded attention, fades (negative)."},

    # -- Activity CV (bounded dispersion; volume/turnover, NOT price vol).
    {"name": "cv_vr_60", "family": "activity_cv", "logic_score": 0.55,
     "expr": "-TsStd(VR, 60) / TsMean(VR, 60)",
     "rationale": "Volume-ratio CV: erratic volume = fragile (distinct from price vol; VOLUME-CV resident exists)."},
    {"name": "cv_turnf_120", "family": "activity_cv", "logic_score": 0.5,
     "expr": "-TsStd(TURN_F, 120) / TsMean(TURN_F, 120)",
     "rationale": "Turnover CV long band."},
    {"name": "cv_relamount_120", "family": "activity_cv", "logic_score": 0.5,
     "expr": "-TsStd(AMOUNT / TsMean(AMOUNT, 20), 120)",
     "rationale": "Long-band relative-amount stability (R13 alpha_0151 was the 60d version)."},

    # -- Event-rarity at fresh thresholds / quantities (calm vein).
    {"name": "calm_turnf3_120", "family": "event_freq", "logic_score": 0.55,
     "expr": "-TsCount(TURN_F > 3 * TsMean(TURN_F, 60), 120)",
     "rationale": "3x turnover-spike rarity (rarer than the 2x R13 winner)."},
    {"name": "calm_vr3_120", "family": "event_freq", "logic_score": 0.55,
     "expr": "-TsCount(VR > 3, 120)",
     "rationale": "VR>3 spike rarity (vs the VR>2/60d resident)."},
    {"name": "calm_amount3_120", "family": "event_freq", "logic_score": 0.5,
     "expr": "-TsCount(AMOUNT > 3 * TsMean(AMOUNT, 60), 120)",
     "rationale": "3x dollar-volume spike rarity."},
    {"name": "calm_ret3sigma_120", "family": "event_freq", "logic_score": 0.5,
     "expr": "-TsCount(Abs(RET) > 3 * TsStd(RET, 60), 120)",
     "rationale": "3-sigma return-shock rarity (rarer tail than 2-sigma)."},

    # -- New structural classes (bounded, non-forbidden).
    {"name": "volume_trend_ratio", "family": "persistence", "logic_score": 0.5,
     "expr": "TsMed(VOLUME, 60) / TsMed(VOLUME, 120)",
     "rationale": "Median-volume trend ratio (recent vs long, robust to spikes)."},
    {"name": "relvol_skew_neg", "family": "tail", "logic_score": 0.5,
     "expr": "-TsSkew(VOLUME / TsMean(VOLUME, 20), 60)",
     "rationale": "Relative-volume skewness (occasional huge volume days), distinct from return skew."},
    {"name": "range_cv_med_120", "family": "activity_cv", "logic_score": 0.5,
     "expr": "-TsStd(AMP, 120) / TsMed(AMP, 120)",
     "rationale": "Range dispersion scaled by median range (robust-denominator CV)."},
]

assert len(CANDIDATES) == 19, len(CANDIDATES)
