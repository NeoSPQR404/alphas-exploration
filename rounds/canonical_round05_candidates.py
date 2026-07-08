# Canonical set — Round 5 (16 candidates) — generated 2026-07-08.
#
# Set 76 -> target 100. Retrieve: conditional RANGE minted (hl_on_hivol60
# OOS 0.081) — this round pushes conditional-X-on-attention across
# quantities and directions, plus the few remaining novel forms. The
# vocabulary is near exhaustion; round 6 will band-jitter the recorded
# near-misses.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ---------------- conditional-on-attention family (7)
    dict(name="c_gapvol_on_hivol", expr=f"-TsStd(({_GAP}) * ({_NVOL} > 1), 20)", family="conditional",
         rationale="Overnight risk on attention days: gaps when the crowd is watching.", logic_score=70),
    dict(name="c_hl_on_down", expr=f"-TsMean(({_HL}) * (RET < 0), 20)", family="conditional",
         rationale="Range on down days: crash texture (conditional masking decorrelates from the level).", logic_score=70),
    dict(name="c_hl_on_lovol", expr=f"TsMean(({_HL}) * ({_NVOL} < 1), 20)", family="conditional",
         rationale="Range on QUIET days: unwatched price discovery (complement of the R4 winner).", logic_score=69),
    dict(name="c_hl_on_hivol250", expr=f"-TsMean(({_HL}) * ({_NVOL} > 1), 250)", family="conditional",
         rationale="Annual conditional range.", logic_score=68),
    dict(name="c_id_on_hiHL60", expr=f"-TsSum(({_ID}) * (({_HL}) > TsMean({_HL}, 60)), 60)", family="conditional",
         rationale="Intraday reversal harvested on wide-range days, quarterly.", logic_score=68),
    dict(name="c_ret_on_hiHL120", expr=f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 120)), 120)", family="conditional",
         rationale="Semi-annual returns earned on wide days.", logic_score=68),
    dict(name="c_max_on_hivol", expr=f"-TsMax(RET * ({_NVOL} > 1), 20)", family="conditional",
         rationale="Biggest attention-day move: crowd-witnessed lottery.", logic_score=68),
    # ---------------- remaining novel forms (9)
    dict(name="c_ret_asym_cnt", expr="-(TsCount(RET > TsStd(RET, 60), 60) - TsCount(RET < -TsStd(RET, 60), 60))",
         family="lottery", rationale="1-sigma day-count asymmetry: softer tail balance than the 2-sigma counts.", logic_score=68),
    dict(name="c_hl_cv", expr=f"-(TsStd({_HL}, 20) / TsMean({_HL}, 20))", family="volatility",
         rationale="Range CV: erratic vs steady daily ranges (volcv analog on range).", logic_score=68),
    dict(name="c_att_autocorr", expr=f"-TsCorr({_NVOL}, Delay({_NVOL}, 1), 20)", family="volume",
         rationale="Attention persistence: sticky vs flash crowds.", logic_score=67),
    dict(name="c_wma_cross", expr="-(WMA(CLOSE, 5) / WMA(CLOSE, 20) - 1)", family="reversal",
         rationale="Weighted MA cross (main-set near-miss at ICIR 0.296/IC 0.0396 — one clean retry).", logic_score=67),
    dict(name="c_id_updown60", expr=f"-(TsStd(({_ID}) * (RET > 0), 60) - TsStd(({_ID}) * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly intraday-leg asymmetry (20d died at S2 vs rev20; band may escape).", logic_score=67),
    dict(name="c_gapmax120", expr=f"-TsMax({_GAP}, 120)", family="overnight",
         rationale="Semi-annual biggest gap-up.", logic_score=66),
    dict(name="c_aggr_updown120", expr=f"-(TsStd(({_AGG}) * (RET > 0), 120) - TsStd(({_AGG}) * (RET < 0), 120))",
         family="asymmetry", rationale="Semi-annual aggression asymmetry (20/60 resident).", logic_score=66),
    dict(name="c_nvol_min", expr=f"TsMin({_NVOL}, 20)", family="volume",
         rationale="Attention-drought depth: the quietest day of the month (neglect extreme).", logic_score=66),
    dict(name="c_travel_eff", expr=f"-(Abs(TsSum(RET, 20)) / TsSum({_HL}, 20))", family="probe",
         rationale="Movement efficiency: net displacement per unit of range traveled (novel form of a dead family — last path-shape test).", logic_score=64),
]

assert len(CANDIDATES) == 16, len(CANDIDATES)
