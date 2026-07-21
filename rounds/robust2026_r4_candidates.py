"""robust_2026 Round 4 — value family, second attempt. R3 showed standalone
value is orthogonal but too weak at 10d. This round tries the forms with the
best remaining shot: value INTERACTED with the working behavioral signals
(concentrate value where it works), value+quality composites, deep-value
(value minus momentum), and earnings-stability quality. Still 10d, no overnight.
"""
SET_NAME = "robust_2026"

CANDIDATES = [
    # value x working-signal interactions (concentrate value where it pays)
    {"name": "value_x_lowturn", "family": "value_interact", "logic_score": 0.55,
     "expr": "(CsRank(EP) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
     "rationale": "Cheap AND low-attention (value works better in neglected names)."},
    {"name": "value_x_stability", "family": "value_interact", "logic_score": 0.55,
     "expr": "(CsRank(CFP) - 0.5) * (CsRank(-TsStd(AMP, 120) / TsMed(AMP, 120)) - 0.5)",
     "rationale": "Cheap AND stable-range (value among calm names)."},
    {"name": "value_x_calm", "family": "value_interact", "logic_score": 0.5,
     "expr": "(CsRank(EP) - 0.5) * (CsRank(-TsCount(AMP > 2 * TsMean(AMP, 60), 120)) - 0.5)",
     "rationale": "Cheap AND event-rare (value among boring stocks)."},

    # value + quality composites
    {"name": "value_quality_both", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(EP) * CsRank(CFP)",
     "rationale": "Cheap on BOTH earnings and cash-flow yield (agreement)."},
    {"name": "triple_value_indneut", "family": "value", "logic_score": 0.55,
     "expr": "CsIndNeutralize(EP + CFP + SP, IND)",
     "rationale": "Industry-neutral triple value composite (EP+CFP+SP)."},
    {"name": "value_cheap_book", "family": "value", "logic_score": 0.5,
     "expr": "CsRank(CFP) + CsRank(EP) - CsRank(PB)",
     "rationale": "Value (CFP+EP) tilted to cheap book."},

    # deep / contrarian value
    {"name": "value_minus_mom", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(EP) - CsRank(TsSum(RET, 120))",
     "rationale": "Contrarian value: cheap and NOT already run up (value minus 6m momentum)."},
    {"name": "value_z_indneut", "family": "value", "logic_score": 0.5,
     "expr": "CsZscore(CsIndNeutralize(EP, IND))",
     "rationale": "Standardized industry-neutral earnings yield."},

    # earnings-stability quality (fundamental, not price)
    {"name": "earnings_yield_stability", "family": "quality", "logic_score": 0.55,
     "expr": "-TsStd(EP, 120)",
     "rationale": "Stable earnings yield = predictable earners (low fundamental risk)."},
    {"name": "cfp_smooth_level", "family": "value", "logic_score": 0.5,
     "expr": "TsMean(CFP, 60)",
     "rationale": "Smoothed cash-flow yield level (noise-reduced value)."},
    {"name": "accruals_level_indneut", "family": "quality", "logic_score": 0.5,
     "expr": "CsIndNeutralize(CFP - EP, IND)",
     "rationale": "Accruals level (cash-flow minus earnings yield); high = cash-backed."},

    # value re-rating, short band + interacted
    {"name": "value_rerate_20", "family": "value_mom", "logic_score": 0.5,
     "expr": "Delta(CsIndNeutralize(EP, IND), 20)",
     "rationale": "Short-band industry-neutral value re-rating."},
    {"name": "value_x_flowdiv", "family": "value_interact", "logic_score": 0.5,
     "expr": "(CsRank(EP) - 0.5) * (CsRank(-TsCorr(MF_LG_NET, RET, 20)) - 0.5)",
     "rationale": "Cheap AND institutional-flow diverging from price."},
]

assert len(CANDIDATES) == 13, len(CANDIDATES)
