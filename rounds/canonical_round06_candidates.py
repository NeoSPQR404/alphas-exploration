# Canonical set — Round 6 (18 candidates) — generated 2026-07-08.
#
# Set 78 -> target 100. Acceptance decaying (34,21,16,7,2): this round is
# band-jitter retries of recorded near-misses (S1 ICIR~0.30 or S4 OOS
# just under 0.03 — different windows shift both) plus tail-ratio forms
# and extensions of the ret_on_hiHL discovery.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ---------------- extensions of the ret_on_hiHL star (3)
    dict(name="c_ret_on_hiHL60", expr=f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 60)), 60)", family="conditional",
         rationale="Quarterly band of the set's best factor (120d OOS 0.092).", logic_score=72),
    dict(name="c_ret_on_hiHL250", expr=f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 250)), 250)", family="conditional",
         rationale="Annual band of the star.", logic_score=70),
    dict(name="c_id_on_hiHL120", expr=f"-TsSum(({_ID}) * (({_HL}) > TsMean({_HL}, 120)), 120)", family="conditional",
         rationale="Intraday-leg version at 120d (60d died at S2 vs rev20; the star's tier may escape).", logic_score=69),
    # ---------------- near-miss band-jitter retries (9)
    dict(name="c_ret_asym_cnt120", expr="-(TsCount(RET > TsStd(RET, 60), 120) - TsCount(RET < -TsStd(RET, 60), 120))",
         family="lottery", rationale="1-sigma count asymmetry at 120d (60d was 0.032/ICIR 0.2996).", logic_score=68),
    dict(name="c_wma_cross_slow", expr="-(WMA(CLOSE, 10) / WMA(CLOSE, 40) - 1)", family="reversal",
         rationale="Slower WMA cross (5/20 hit ICIR 0.30 twice; window shift is the last try).", logic_score=67),
    dict(name="c_ovnmom40", expr=f"TsSum({_GAP}, 40)", family="overnight",
         rationale="Overnight momentum between the failed 20d and resident 60d.", logic_score=66),
    dict(name="c_vwap_gap_med120", expr="TsMed(OPEN / Delay(VWAP, 1) - 1, 120)", family="overnight",
         rationale="VWAP-anchored median gap at 120d (60d was 0.032/ICIR 0.29).", logic_score=67),
    dict(name="c_aggr_sum120", expr=f"-TsSum({_AGG}, 120)", family="aggression",
         rationale="Semi-annual cumulative aggression (60d was 0.028).", logic_score=66),
    dict(name="c_updn_freq_hl120", expr=f"-(TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 120) - TsCount(({_HL}) < 0.5 * TsMean({_HL}, 60), 120))",
         family="event", rationale="Net excitement balance at 120d (60d was 0.027/0.30).", logic_score=66),
    dict(name="c_hl_cv120", expr=f"-(TsStd({_HL}, 120) / TsMean({_HL}, 120))", family="volatility",
         rationale="Range CV at 120d (20d failed S4 at OOS 0.023; longer bands lift OOS).", logic_score=66),
    dict(name="c_att_autocorr60", expr=f"-TsCorr({_NVOL}, Delay({_NVOL}, 1), 60)", family="volume",
         rationale="Attention persistence at 60d (20d failed S4 at OOS 0.028).", logic_score=66),
    dict(name="c_vol_on_down120", expr=f"-(TsSum(({_NVOL}) * (RET < 0), 120) / TsSum({_NVOL}, 120))",
         family="conditional", rationale="Attention share on down days at 120d (60d failed S4 at 0.026).", logic_score=66),
    # ---------------- tail-ratio forms — novel (4)
    dict(name="c_tail_ratio", expr="-(TsMax(RET, 60) / Abs(TsMin(RET, 60)))", family="lottery",
         rationale="Up-tail / down-tail magnitude ratio: scale-free tail asymmetry.", logic_score=68),
    dict(name="c_gap_tail_ratio", expr=f"-(TsMax({_GAP}, 60) / Abs(TsMin({_GAP}, 60)))", family="overnight",
         rationale="Overnight tail ratio.", logic_score=67),
    dict(name="c_hl_spike_ratio", expr=f"-(TsMax({_HL}, 60) / TsMed({_HL}, 60))", family="volatility",
         rationale="Range spike ratio: worst day vs typical day.", logic_score=67),
    dict(name="c_drift_state", expr="-TsRank(TsMean(RET, 5), 250)", family="reversal",
         rationale="Weekly drift vs own year: momentum-state self-rank.", logic_score=66),
    # ---------------- remaining band probes (2)
    dict(name="c_min_gap120", expr=f"-TsMin({_GAP}, 120)", family="overnight",
         rationale="Semi-annual deepest gap-down (60d resident at -0.064).", logic_score=65),
    dict(name="c_nvol_burst250", expr=f"-TsCount({_NVOL} > 2, 250)", family="volume",
         rationale="Annual attention-burst habit (60/120 resident).", logic_score=65),
]

assert len(CANDIDATES) == 18, len(CANDIDATES)
