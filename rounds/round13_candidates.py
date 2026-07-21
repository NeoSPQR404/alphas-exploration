"""Round 13 (behavioral_full) — robust factors for BOTH 2017-25 and 2026,
explicitly AVOIDING the overnight-gap vein (OPEN/Delay(CLOSE,1)-1).

The 2026 per-factor screen (VALID_2026.md) showed that, besides overnight-gap,
the robust + tradable veins are: event-rarity ("calm" stocks outperform),
cross-quantity coupling correlations, and low idio/systematic-share. This round
mines those veins on FRESH quantities/pairs (the set is at the S2 wall, so
novelty = fresh quantity, not a new window on a taken one), plus a few
genuinely-new structural classes (volume clustering, attention-scaled momentum,
market-direction masked dispersion). No OPEN/Delay(CLOSE,1) constructs.
"""
SET_NAME = "main"

CANDIDATES = [
    # -- Event-rarity / "calm" on fresh quantities (low turnover, 2026-robust).
    #    Negative sign: fewer recent spikes -> higher forward return.
    {"name": "calm_turnf_120", "family": "event_freq", "logic_score": 0.7,
     "expr": "-TsCount(TURN_F > 2 * TsMean(TURN_F, 60), 120)",
     "rationale": "Turnover-spike rarity (fresh quantity vs amp/vr/vol event reps); calm names outperform."},
    {"name": "calm_amount_120", "family": "event_freq", "logic_score": 0.7,
     "expr": "-TsCount(AMOUNT > 2 * TsMean(AMOUNT, 60), 120)",
     "rationale": "Dollar-volume-spike rarity; distinct from volume-count (amount weights price)."},
    {"name": "calm_amount_60", "family": "event_freq", "logic_score": 0.6,
     "expr": "-TsCount(AMOUNT > 2 * TsMean(AMOUNT, 60), 60)",
     "rationale": "Shorter-band amount-spike rarity."},
    {"name": "calm_retshock_120", "family": "event_freq", "logic_score": 0.65,
     "expr": "-TsCount(Abs(RET) > 2 * TsStd(RET, 60), 120)",
     "rationale": "Return-shock rarity (sigma-scaled); calm-return names outperform."},
    {"name": "calm_retshock_60", "family": "event_freq", "logic_score": 0.55,
     "expr": "-TsCount(Abs(RET) > 2 * TsStd(RET, 60), 60)",
     "rationale": "Shorter-band return-shock rarity."},
    {"name": "calm_mfshock_120", "family": "event_freq", "logic_score": 0.55,
     "expr": "-TsCount(Abs(MF_LG_NET) > 2 * TsStd(MF_LG_NET, 60), 120)",
     "rationale": "Large-order-flow shock rarity (frequency, not level/accumulation which is dead)."},
    {"name": "calm_vwapdev_120", "family": "event_freq", "logic_score": 0.6,
     "expr": "-TsCount(Abs(CLOSE / VWAP - 1) > 2 * TsStd(CLOSE / VWAP - 1, 60), 120)",
     "rationale": "Intraday close-vs-vwap deviation shock rarity (intraday, not overnight)."},

    # -- Cross-quantity coupling correlations on fresh pairs (still minting).
    {"name": "coup_turnf_absret_60", "family": "coupling", "logic_score": 0.7,
     "expr": "-TsCorr(TURN_F, Abs(RET), 60)",
     "rationale": "Attention-risk coupling: turnover riding volatility = crowding, fades."},
    {"name": "coup_turnf_absret_120", "family": "coupling", "logic_score": 0.6,
     "expr": "-TsCorr(TURN_F, Abs(RET), 120)",
     "rationale": "Semi-annual band of attention-risk coupling."},
    {"name": "coup_vr_ret_120", "family": "coupling", "logic_score": 0.6,
     "expr": "-TsCorr(VR, RET, 120)",
     "rationale": "Volume-ratio vs return agreement, long band (price-volume agreement fades)."},
    {"name": "coup_amount_amp_120", "family": "coupling", "logic_score": 0.55,
     "expr": "TsCorr(AMOUNT, AMP, 120)",
     "rationale": "Liquidity-range coupling: range needing dollar volume = fragile."},
    {"name": "coup_amp_vr_120", "family": "coupling", "logic_score": 0.55,
     "expr": "-TsCorr(AMP, VR, 120)",
     "rationale": "Range-volume coupling long band."},
    {"name": "coup_mfsm_ret_60", "family": "flow_coupling", "logic_score": 0.6,
     "expr": "-TsCorr(MF_SM_NET, RET, 60)",
     "rationale": "Retail (small-order) flow vs return coupling — fresh flow field vs the large-order reps."},
    {"name": "coup_mfnet_amp_60", "family": "flow_coupling", "logic_score": 0.55,
     "expr": "-TsCorr(MF_NET, AMP, 60)",
     "rationale": "Net-flow vs range coupling (net field, fresh pair)."},
    {"name": "coup_mflg_turnf_60", "family": "flow_coupling", "logic_score": 0.55,
     "expr": "-TsCorr(MF_LG_NET, TURN_F, 60)",
     "rationale": "Institutional-flow vs attention coupling (fresh pair)."},

    # -- Robust / median gap on fresh quantities (first-class success family).
    {"name": "med_amount_ratio_60", "family": "robust", "logic_score": 0.65,
     "expr": "TsMed(AMOUNT, 60) / TsMean(AMOUNT, 60)",
     "rationale": "Dollar-volume distribution skew (median/mean); low = spiky liquidity."},
    {"name": "med_amp_gap_60", "family": "robust", "logic_score": 0.6,
     "expr": "TsMean(AMP, 60) - TsMed(AMP, 60)",
     "rationale": "Range mean-median gap = range right-skew (occasional violent days)."},
    {"name": "med_absret_gap_120", "family": "robust", "logic_score": 0.6,
     "expr": "TsMean(Abs(RET), 120) - TsMed(Abs(RET), 120)",
     "rationale": "|Return| mean-median gap = shock-driven vol vs baseline (long band)."},
    {"name": "med_amount_gap_120", "family": "robust", "logic_score": 0.55,
     "expr": "TsMean(AMOUNT, 120) - TsMed(AMOUNT, 120)",
     "rationale": "Dollar-volume right-skew, semi-annual band."},

    # -- Systematic-share / benchmark-coupling (success with anti-intuitive sign).
    {"name": "rsq_bench_120", "family": "systematic", "logic_score": 0.6,
     "expr": "-(TsCorr(RET, BENCH_RET, 120) * TsCorr(RET, BENCH_RET, 120))",
     "rationale": "Systematic share (R^2 vs bench) long band; index-coupled names lag (anti-intuitive sign)."},
    {"name": "rsq_bench_term", "family": "systematic", "logic_score": 0.55,
     "expr": "TsCorr(RET, BENCH_RET, 20) * TsCorr(RET, BENCH_RET, 20) - TsCorr(RET, BENCH_RET, 120) * TsCorr(RET, BENCH_RET, 120)",
     "rationale": "R^2 term structure (recent vs long systematic share) — new construct."},
    {"name": "beta_instability", "family": "systematic", "logic_score": 0.55,
     "expr": "-TsStd(RegBeta(RET, BENCH_RET, 20), 60)",
     "rationale": "Beta instability: names with drifting market sensitivity are riskier/fade."},

    # -- Genuinely-new structural classes (avoid forbidden: not Amihud, not plain
    #    vol, not autocorr-of-returns, not flow levels, not anchor/position).
    {"name": "vol_clustering_vr", "family": "persistence", "logic_score": 0.6,
     "expr": "TsCorr(VR, Delay(VR, 5), 60)",
     "rationale": "Volume-ratio clustering (volume ARCH persistence) — new class, distinct from return autocorr."},
    {"name": "vol_clustering_turnf", "family": "persistence", "logic_score": 0.55,
     "expr": "TsCorr(TURN_F, Delay(TURN_F, 5), 60)",
     "rationale": "Turnover clustering / attention persistence."},
    {"name": "mom_per_attention", "family": "efficiency", "logic_score": 0.6,
     "expr": "TsSum(RET, 20) / TsSum(TURN_F, 20)",
     "rationale": "Attention-scaled momentum: return earned per unit turnover (info-diffusion, not Amihud)."},
    {"name": "downmkt_disp_asym", "family": "asymmetry", "logic_score": 0.6,
     "expr": "TsStd(RET * (BENCH_RET < 0), 60) - TsStd(RET * (BENCH_RET > 0), 60)",
     "rationale": "Masked-std asymmetry on market direction: down-market vs up-market return dispersion."},
    {"name": "amount_trend_stability", "family": "persistence", "logic_score": 0.5,
     "expr": "-TsStd(AMOUNT / TsMean(AMOUNT, 20), 60)",
     "rationale": "Stability of relative dollar volume: erratic liquidity = fragile (CV of relative amount)."},
]

assert len(CANDIDATES) == 27, len(CANDIDATES)
