# Canonical set — Round 4 (28 candidates) — generated 2026-07-08.
#
# Set 70 -> target 100. Space tightening: range-attention couplings and
# gap conditionals are closed; meanmed/idmed long bands under the bar.
# This round: overnight-momentum bands, conditional RANGE (novel),
# robust deviation constructs (value-vs-own-median), studentized range,
# 250d tier tests for asym/conditional/count classes, remaining fills.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ---------------- overnight momentum bands (3)
    dict(name="c_ovnmom20", expr=f"TsSum({_GAP}, 20)", family="overnight",
         rationale="Monthly overnight momentum (60d resident; 20d coexisted nowhere yet).", logic_score=70),
    dict(name="c_ovnmom120", expr=f"TsSum({_GAP}, 120)", family="overnight",
         rationale="Semi-annual overnight momentum.", logic_score=69),
    dict(name="c_ovn_rev7", expr=f"DecayLinear({_GAP}, 7)", family="overnight",
         rationale="Weekly decayed overnight band (fast momentum or reversal — data decides).", logic_score=67),
    # ---------------- conditional range — novel class (3)
    dict(name="c_hl_on_hivol", expr=f"-TsMean(({_HL}) * ({_NVOL} > 1), 20)", family="conditional",
         rationale="Range on high-attention days: how violent is the stock WHEN the crowd shows up.", logic_score=71),
    dict(name="c_hl_on_hivol60", expr=f"-TsMean(({_HL}) * ({_NVOL} > 1), 60)", family="conditional",
         rationale="Quarterly conditional range.", logic_score=70),
    dict(name="c_vol_on_downdays", expr=f"-(TsSum(({_NVOL}) * (RET < 0), 60) / TsSum({_NVOL}, 60))",
         family="conditional", rationale="Attention share spent on down days: distribution-day intensity.", logic_score=69),
    # ---------------- robust deviations — novel class (3)
    dict(name="c_hl_med_dev", expr=f"-(({_HL}) / TsMed({_HL}, 60) - 1)", family="volatility",
         rationale="Today's range vs own median range: robust range-state (deviation, not level).", logic_score=70),
    dict(name="c_nvol_med_dev", expr=f"-(({_NVOL}) / (TsMed({_NVOL}, 60) + 0.1) - 1)", family="volume",
         rationale="Today's attention vs own median attention.", logic_score=68),
    dict(name="c_range_stud", expr="-((TsMax(RET, 60) - TsMin(RET, 60)) / TsStd(RET, 60))", family="lottery",
         rationale="Studentized return range: tail activity scaled by dispersion (scale-free tails).", logic_score=69),
    # ---------------- 250d tier tests (5)
    dict(name="c_semivol250", expr="-(TsStd((RET + Abs(RET)) / 2, 250) - TsStd((RET - Abs(RET)) / 2, 250))",
         family="volatility", rationale="Annual semivol asymmetry (20/60/120 all resident and coexisting).", logic_score=68),
    dict(name="c_hl_updown250", expr=f"-(TsStd(({_HL}) * (RET > 0), 250) - TsStd(({_HL}) * (RET < 0), 250))",
         family="asymmetry", rationale="Annual range asymmetry.", logic_score=67),
    dict(name="c_id_on_hivol250", expr=f"-TsSum(({_ID}) * (VOLUME > TsMean(VOLUME, 250)), 250)",
         family="conditional", rationale="Annual intraday-on-attention conditional.", logic_score=67),
    dict(name="c_attn_up_cnt250", expr=f"-TsCount((({_NVOL} > 1) * (RET > 0)) > 0.5, 250)",
         family="conditional", rationale="Annual attention-up-day count.", logic_score=66),
    dict(name="c_zeroret250", expr="-TsCount(Abs(RET) < 0.001, 250)", family="liquidity",
         rationale="Annual zero-return habit.", logic_score=66),
    # ---------------- aggression / vwap fills (4)
    dict(name="c_aggr_sum60", expr=f"-TsSum({_AGG}, 60)", family="aggression",
         rationale="Quarterly cumulative aggression (10d mean failed universes; the sum band may not).", logic_score=67),
    dict(name="c_aggrmin120", expr=f"TsMin({_AGG}, 120)", family="aggression",
         rationale="Semi-annual deepest capitulation (20/60 resident).", logic_score=66),
    dict(name="c_aggr_hi_nvol120", expr=f"-TsMean(({_AGG}) * ({_NVOL} > 1), 120)", family="conditional",
         rationale="Semi-annual conditional aggression (20/60 resident; main's 120 died only at corr).", logic_score=66),
    dict(name="c_vwap_gap_med", expr=f"TsMed(OPEN / Delay(VWAP, 1) - 1, 60)", family="overnight",
         rationale="Median open-vs-prior-vwap gap: volume-anchored overnight drift.", logic_score=67),
    # ---------------- leg vol / misc fills (9)
    dict(name="c_idvol60", expr=f"-TsStd({_ID}, 60)", family="volatility",
         rationale="Intraday-leg vol standalone (died vs turn_low in main; no turnover family here).", logic_score=68),
    dict(name="c_min120", expr="-TsMin(RET, 120)", family="lottery",
         rationale="Semi-annual MIN (20/60 resident and coexisting).", logic_score=66),
    dict(name="c_maxfreq20", expr="-TsCount(RET > 2 * TsStd(RET, 60), 20)", family="lottery",
         rationale="Fast lottery-day count.", logic_score=66),
    dict(name="c_gap_share60", expr=f"-TsMean(Abs({_GAP}) / ({_HL}), 60)", family="overnight",
         rationale="Quarterly overnight share of range (20d failed the OOS bar at 0.018; band may lift).", logic_score=66),
    dict(name="c_gap_updown60", expr=f"-(TsStd(({_GAP}) * (RET > 0), 60) - TsStd(({_GAP}) * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly gap asymmetry (20d failed S1 in main; quarterly semivol pattern says retry).", logic_score=66),
    dict(name="c_hi_nvol_vol", expr=f"-TsStd(RET * ({_NVOL} > 1), 20)", family="volatility",
         rationale="Volatility ON attention days: crowd-conditional risk.", logic_score=67),
    dict(name="c_updn_freq_hl", expr=f"-(TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60) - TsCount(({_HL}) < 0.5 * TsMean({_HL}, 60), 60))",
         family="event", rationale="Range-burst days minus range-collapse days: net excitement balance.", logic_score=66),
    dict(name="c_zeroret20", expr="-TsCount(Abs(RET) < 0.001, 20)", family="liquidity",
         rationale="Fast zero-return count.", logic_score=65),
    dict(name="c_close_pos_med", expr="-TsMed((CLOSE - LOW) / (HIGH - LOW), 60)", family="candle",
         rationale="Median close position in range: the robust framing of a dead level family (last candle test).", logic_score=64),
    # ---------------- coupling last stand (1)
    dict(name="c_id_nvol_corr60", expr=f"-TsCorr({_ID}, {_NVOL}, 60)", family="coupling",
         rationale="Quarterly intraday-attention coupling (20d accepted; range/gap partners dead but ID partner lives).", logic_score=67),
]

assert len(CANDIDATES) == 28, len(CANDIDATES)
