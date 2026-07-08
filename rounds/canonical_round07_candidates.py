# Canonical set — Round 7 (26 candidates) — generated 2026-07-08.
#
# User decision at saturation (79/100): COMPOSE factors from the current
# set. Demeaned-rank interactions have near-zero corr with parents by
# construction (beats the S2 wall); the 0.03 IC bar is the filter.
# Parent selection per main-set lessons: strong simple-quantity
# behavioral parents from DIFFERENT families; no correlation-construct
# parents. Two 3-way products probe deeper composition.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

# parent pool (expressions of accepted canonical factors)
P = {
    "hlmed60":   f"-TsMed({_HL}, 60)",
    "max20":     "-TsMax(RET, 20)",
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    "aggrmax":   f"-TsMax({_AGG}, 20)",
    "aggrmin":   f"TsMin({_AGG}, 20)",
    "rev20":     f"-TsSum({_ID}, 20)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "nvolspike": "-(TsMean(VOLUME, 5) / TsMean(VOLUME, 60))",
    "nvolburst": f"-TsCount({_NVOL} > 2, 60)",
    "hlburst":   f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "zeroret":   "-TsCount(Abs(RET) < 0.001, 60)",
    "flatopen":  f"-TsCount(Abs({_GAP}) < 0.001, 60)",
    "mingap60":  f"-TsMin({_GAP}, 60)",
    "semivol20": "-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
    "rethiHL":   f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 120)), 120)",
    "hlhivol":   f"-TsMean(({_HL}) * ({_NVOL} > 1), 60)",
    "volcv":     "-(TsStd(VOLUME, 20) / TsMean(VOLUME, 20))",
}

def _ix(a, b):
    return f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5)"

def _ix3(a, b, c):
    return f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5) * (CsRank({P[c]}) - 0.5)"

def C(name, a, b, why, ls=68):
    return dict(name=name, expr=_ix(a, b), family="composition",
                rationale=why, logic_score=ls)

CANDIDATES = [
    # analogs of main-set interactions that cleared >= 0.03
    C("cx_hlburst_rev", "hlburst", "rev20", "Range-burst habit x reversal (main analog OOS 0.043)."),
    C("cx_nvolburst_med", "nvolburst", "med60", "Attention bursts x quarterly stretch (main analog OOS 0.041)."),
    C("cx_volclock_rev", "volclock", "rev60", "Volume clock x quarterly reversal (main analog OOS 0.036)."),
    C("cx_medband_volclock", "med60", "volclock", "Median stretch x volume clock."),
    # champion pairings across families
    C("cx_hlmed_max", "hlmed60", "max20", "Median range x lottery."),
    C("cx_hlmed_volclock", "hlmed60", "volclock", "Median range x volume clock."),
    C("cx_hlmed_flatopen", "hlmed60", "flatopen", "Median range x attention void."),
    C("cx_hlmed_zeroret", "hlmed60", "zeroret", "Median range x zero-return illiquidity."),
    C("cx_gapvol_maxfreq", "gapvol", "maxfreq", "Overnight risk x lottery frequency."),
    C("cx_gapvol_nvolspike", "gapvol", "nvolspike", "Overnight risk x volume spike."),
    C("cx_gapvol_amtself", "gapvol", "amtself", "Overnight risk x dollar-attention state."),
    C("cx_aggrmax_med", "aggrmax", "med60", "Peak aggression x quarterly stretch."),
    C("cx_aggrmax_zeroret", "aggrmax", "zeroret", "Peak aggression x illiquidity."),
    C("cx_aggrmin_nvolburst", "aggrmin", "nvolburst", "Capitulation depth x attention bursts."),
    C("cx_max_mingap", "max20", "mingap60", "Day-lottery x gap-crash: cross-leg tails."),
    C("cx_maxfreq_amtself", "maxfreq", "amtself", "Lottery frequency x dollar-attention state."),
    C("cx_semivol_volclock", "semivol20", "volclock", "Vol shape x volume clock."),
    C("cx_semivol_zeroret", "semivol20", "zeroret", "Vol shape x illiquidity."),
    C("cx_rethiHL_volclock", "rethiHL", "volclock", "Star conditional x volume clock."),
    C("cx_rethiHL_flatopen", "rethiHL", "flatopen", "Star conditional x attention void."),
    C("cx_hlhivol_zeroret", "hlhivol", "zeroret", "Conditional range x illiquidity."),
    C("cx_mingap_volclock", "mingap60", "volclock", "Gap-crash x volume clock."),
    C("cx_volcv_med", "volcv", "med60", "Volume churn x quarterly stretch."),
    C("cx_rev20_gapvol", "rev20", "gapvol", "Reversal x overnight risk."),
    # 3-way probes
    dict(name="cx3_med_volclock_maxfreq", expr=_ix3("med60", "volclock", "maxfreq"),
         family="composition",
         rationale="3-way product: stretch x clock x lottery-frequency (deep-composition probe).", logic_score=64),
    dict(name="cx3_hlmed_gapvol_zeroret", expr=_ix3("hlmed60", "gapvol", "zeroret"),
         family="composition",
         rationale="3-way product: range x overnight risk x illiquidity.", logic_score=64),
]

assert len(CANDIDATES) == 26, len(CANDIDATES)
