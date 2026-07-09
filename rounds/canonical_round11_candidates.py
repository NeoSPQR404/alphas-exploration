# Canonical set — Round 11 (18 candidates) — 2026-07-09.
# Run 1 of 5 in the user's novelty experiment: individual factors only,
# thresholds unchanged. Unexplored grammar: dual-condition day-type
# counts, cross-quantity elasticities, shape ratios, clustering
# coefficients, duration measures.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ---------------- dual-condition day types (5)
    dict(name="c_dipbuy_freq", expr=f"TsCount((({_GAP}) < 0) * (({_ID}) > 0) > 0.5, 60)", family="daytype",
         rationale="Dip-bought days: opened down, closed up intraday — absorption demand.", logic_score=72),
    dict(name="c_dipbuy_freq120", expr=f"TsCount((({_GAP}) < 0) * (({_ID}) > 0) > 0.5, 120)", family="daytype",
         rationale="Semi-annual dip-bought habit.", logic_score=70),
    dict(name="c_fade_freq", expr=f"-TsCount((({_GAP}) > 0) * (({_ID}) < 0) > 0.5, 60)", family="daytype",
         rationale="Gap-and-fade days: opened up, sold off — distribution into strength.", logic_score=72),
    dict(name="c_conform_freq", expr=f"-TsCount((({_GAP}) > 0) * (({_ID}) > 0) > 0.5, 60)", family="daytype",
         rationale="Conforming up days (gap up AND intraday up): one-way crowding.", logic_score=69),
    dict(name="c_aggr_on_gapdn", expr=f"-TsMean(({_AGG}) * (({_GAP}) < 0), 20)", family="daytype",
         rationale="Late-day aggression specifically on gap-down days: defiance texture.", logic_score=68),
    # ---------------- cross-quantity elasticities (4)
    dict(name="c_range_att_beta", expr=f"-RegBeta({_HL}, {_NVOL}, 20)", family="elasticity",
         rationale="Range per unit attention: how much movement the marginal crowd buys (nvol-RETURN betas died; nvol-RANGE untested).", logic_score=70),
    dict(name="c_gap_att_beta", expr=f"-RegBeta(Abs({_GAP}), {_NVOL}, 20)", family="elasticity",
         rationale="Overnight shock per unit attention.", logic_score=68),
    dict(name="c_vol_cluster", expr="RegBeta(Abs(RET), Delay(Abs(RET), 1), 20)", family="elasticity",
         rationale="Volatility clustering coefficient (GARCH persistence as a characteristic; direction to data).", logic_score=69),
    dict(name="c_gap_cluster", expr=f"RegBeta(Abs({_GAP}), Delay(Abs({_GAP}), 1), 20)", family="elasticity",
         rationale="Overnight-shock clustering.", logic_score=67),
    # ---------------- shape ratios (4)
    dict(name="c_hl_burst_amp", expr=f"-(TsMax({_HL}, 60) / TsMed({_HL}, 60))", family="shape",
         rationale="Burst amplitude: worst day's range vs typical range (scale-free excitability).", logic_score=70),
    dict(name="c_hl_range_ratio", expr=f"-((TsMax({_HL}, 60) - TsMin({_HL}, 60)) / TsMed({_HL}, 60))", family="shape",
         rationale="Range of ranges over median range: regime instability.", logic_score=68),
    dict(name="c_nvol_burst_amp", expr=f"-(TsMax({_NVOL}, 60) / TsMed({_NVOL}, 60))", family="shape",
         rationale="Attention burst amplitude vs typical attention.", logic_score=68),
    dict(name="c_gap_burst_amp", expr=f"-(TsMax(Abs({_GAP}), 60) / (TsMed(Abs({_GAP}), 60) + 0.001))", family="shape",
         rationale="Overnight shock amplitude vs typical gap.", logic_score=67),
    # ---------------- distribution shape on non-return quantities (3)
    dict(name="c_hl_skew", expr=f"-TsSkew({_HL}, 60)", family="shape",
         rationale="Range skewness: occasional explosive days vs steady widening (return skew is owned; range skew untested).", logic_score=67),
    dict(name="c_nvol_kurt", expr=f"-TsKurt({_NVOL}, 60)", family="shape",
         rationale="Attention kurtosis: fat-tailed crowd arrival (return kurt dead in main; attention kurt untested).", logic_score=66),
    dict(name="c_gap_sign_bal120", expr=f"-Abs(TsMean(Sign({_GAP}), 120))", family="overnight",
         rationale="Gap-direction one-sidedness at 120d (main-set near-miss: ICIR 0.61, IC 0.025 at 60d).", logic_score=67),
    # ---------------- duration measures (2)
    dict(name="c_above_med_dur", expr="-TsCount(CLOSE > TsMed(CLOSE, 60), 60)", family="duration",
         rationale="Time spent above own median price: stretch DURATION rather than magnitude.", logic_score=68),
    dict(name="c_amihud_med", expr="TsMed(Abs(RET) / AMOUNT, 60)", family="liquidity",
         rationale="Median price impact: robust Amihud level (self-rank resident is a different transform).", logic_score=67),
]

assert len(CANDIDATES) == 18, len(CANDIDATES)
