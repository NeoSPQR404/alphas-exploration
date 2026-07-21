"""robust_2026 Round 1 — grow the curated set with new robust+efficient,
non-overnight factors. S2 is only vs the 24 residents, so proven-vein forms on
FRESH quantities/bands that S2-locked in behavioral_full get another shot.
Veins: activity-stability / liquidity-shape (CV, median/mean), event-rarity,
idio/systematic, plus new classes (robust-Sharpe, skew). No OPEN/Delay(CLOSE,1).
"""
SET_NAME = "robust_2026"

CANDIDATES = [
    # activity-stability / liquidity-shape (fresh quantities/median-scaling)
    {"name": "vr_cv_med_120", "family": "activity_cv", "logic_score": 0.6,
     "expr": "-TsStd(VR, 120) / TsMed(VR, 120)",
     "rationale": "Volume-ratio CV median-scaled, long band (resident CVs are AMP/AMOUNT/VOLUME)."},
    {"name": "hl_cv_med_120", "family": "activity_cv", "logic_score": 0.6,
     "expr": "-TsStd(HIGH / LOW - 1, 120) / TsMed(HIGH / LOW - 1, 120)",
     "rationale": "Intraday HL-range CV median-scaled (distinct range quantity from AMP)."},
    {"name": "relturnf_cv_120", "family": "activity_cv", "logic_score": 0.6,
     "expr": "-TsStd(TURN_F / TsMean(TURN_F, 20), 120)",
     "rationale": "Relative-turnover CV long band (resident is relative-AMOUNT CV)."},
    {"name": "relvol_cv_120", "family": "activity_cv", "logic_score": 0.55,
     "expr": "-TsStd(VOLUME / TsMean(VOLUME, 20), 120)",
     "rationale": "Relative-volume CV long band."},
    {"name": "amount_cv_med_120", "family": "activity_cv", "logic_score": 0.55,
     "expr": "-TsStd(AMOUNT, 120) / TsMed(AMOUNT, 120)",
     "rationale": "Dollar-volume CV median-scaled (parallels the AMP-CV resident)."},
    {"name": "amp_ratio_120", "family": "robust", "logic_score": 0.55,
     "expr": "TsMed(AMP, 120) / TsMean(AMP, 120)",
     "rationale": "Range median/mean RATIO long band (residents have VR/AMOUNT ratios)."},

    # event-rarity on fresh quantities / directions
    {"name": "calm_amount_120", "family": "event_freq", "logic_score": 0.6,
     "expr": "-TsCount(AMOUNT > 2 * TsMean(AMOUNT, 60), 120)",
     "rationale": "Dollar-volume-spike rarity (resident is VOLUME-count; amount weights price)."},
    {"name": "calm_retshock_120", "family": "event_freq", "logic_score": 0.55,
     "expr": "-TsCount(Abs(RET) > 2 * TsStd(RET, 60), 120)",
     "rationale": "Return-shock rarity (sigma-scaled), fresh quantity."},
    {"name": "calm_outflow_120", "family": "event_freq", "logic_score": 0.5,
     "expr": "-TsCount(MF_LG_NET < -2 * TsStd(MF_LG_NET, 60), 120)",
     "rationale": "Large-outflow-day rarity (directional institutional-flow event)."},

    # idio / systematic (fresh bands)
    {"name": "idio_sum_120", "family": "idio", "logic_score": 0.55,
     "expr": "-TsSum(RegResi(RET, BENCH_RET, 120), 120)",
     "rationale": "Idiosyncratic cumulative residual, long band (resident is 60d)."},
    {"name": "rsq_bench_120", "family": "systematic", "logic_score": 0.55,
     "expr": "-(TsCorr(RET, BENCH_RET, 120) * TsCorr(RET, BENCH_RET, 120))",
     "rationale": "Systematic share (R^2) long band (resident R^2 is 60d)."},

    # new classes (robust, low-turnover, non-forbidden)
    {"name": "robust_sharpe_60", "family": "robust", "logic_score": 0.6,
     "expr": "TsMed(RET, 60) / TsStd(RET, 60)",
     "rationale": "Robust risk-adjusted momentum (median return / vol) — new construct."},
    {"name": "absret_shape_60", "family": "robust", "logic_score": 0.55,
     "expr": "TsMed(Abs(RET), 60) / TsStd(Abs(RET), 60)",
     "rationale": "|Return| median/std = vol-shape (shock-driven vs steady)."},
    {"name": "turnf_skew_neg_60", "family": "tail", "logic_score": 0.55,
     "expr": "-TsSkew(TURN_F, 60)",
     "rationale": "Turnover skewness: occasional attention spikes = crowded, fades."},
    {"name": "relvol_skew_neg_120", "family": "tail", "logic_score": 0.5,
     "expr": "-TsSkew(VOLUME / TsMean(VOLUME, 20), 120)",
     "rationale": "Relative-volume skewness long band (distinct from return skew)."},
    {"name": "relvol_peak_60", "family": "lottery", "logic_score": 0.5,
     "expr": "-TsMax(VOLUME / TsMean(VOLUME, 20), 60)",
     "rationale": "Peak relative volume (volume lottery): extreme volume day = attention, fades."},
    {"name": "amp_trend_neg_60", "family": "persistence", "logic_score": 0.5,
     "expr": "-TsSlope(AMP, 60)",
     "rationale": "Rising range trend = building instability, fades."},
    {"name": "turnf_cv_med_60", "family": "activity_cv", "logic_score": 0.5,
     "expr": "-TsStd(TURN_F, 60) / TsMed(TURN_F, 60)",
     "rationale": "Turnover CV median-scaled, 60d (resident turnover CV is mean-scaled 20d)."},
]

assert len(CANDIDATES) == 18, len(CANDIDATES)
