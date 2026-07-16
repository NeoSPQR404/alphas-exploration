# canonical_composite — Round 4 (40 candidates) — 2026-07-10.
# generation_plan(40): rich vein 0.588 -> 70/15/15.
#   exploit (28): fresh three-way products from parents not yet composed
#   probe   (6):  strong-parent pairs
#   explore (6):  four-way-products insight (status: testing, 1/3)
# sign-conditioned-composition insight was REFUTED (0/3) -> dropped.

SET_NAME = "canonical_composite"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_DIPBUY = f"(({_GAP}) < 0) * (({_ID}) > 0)"

P = {
    # stretch / state / clock anchors
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    # fresh strong parents not yet composed
    "aggrmax60": f"-TsMax({_AGG}, 60)",
    "min60":     "-TsMin(RET, 60)",
    "semivol60": "-(TsStd((RET + Abs(RET)) / 2, 60) - TsStd((RET - Abs(RET)) / 2, 60))",
    "gapmed":    f"TsMed({_GAP}, 60)",
    "retonhiHL": f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 120)), 120)",
    "aggrupdn":  f"-(TsStd(({_AGG}) * (RET > 0), 60) - TsStd(({_AGG}) * (RET < 0), 60))",
    "hlupdn":    f"-(TsStd(({_HL}) * (RET > 0), 120) - TsStd(({_HL}) * (RET < 0), 120))",
    "lagchase":  f"-TsCorr({_NVOL}, Delay(RET, 1), 60)",
    "nvolspike": "-(TsMean(VOLUME, 5) / TsMean(VOLUME, 60))",
    "maxfreq120": "-TsCount(RET > 2 * TsStd(RET, 60), 120)",
    "aggrmin60": f"TsMin({_AGG}, 60)",
    "gapmed20":  f"TsMed({_GAP}, 20)",
    "retvrcorr": "-TsCorr(RET, VOLUME / TsMean(VOLUME, 60), 60)",
    # anchors reused for pairs/4-ways
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "hlmed60":   f"-TsMed({_HL}, 60)",
}

def R(k): return f"(CsRank({P[k]}) - 0.5)"
def C3(n,a,b,c,w): return dict(name=n, expr=f"{R(a)} * {R(b)} * {R(c)}", family="threeway", rationale=w, logic_score=65)
def C(n,a,b,w): return dict(name=n, expr=f"{R(a)} * {R(b)}", family="pair", rationale=w, logic_score=65)
def C4(n,a,b,c,d,w): return dict(name=n, expr=f"{R(a)} * {R(b)} * {R(c)} * {R(d)}", family="fourway", rationale=w, logic_score=63)

CANDIDATES = [
    # ===== EXPLOIT: 28 fresh three-ways =====
    C3("x3_aggrmax60_med_amtself", "aggrmax60", "med60", "amtself", "Quarterly peak aggr x stretch x state."),
    C3("x3_aggrmax60_volclock_amtself", "aggrmax60", "volclock", "amtself", "Quarterly peak aggr x clock x state."),
    C3("x3_min60_med_amtself", "min60", "med60", "amtself", "Quarterly crash x stretch x state."),
    C3("x3_min60_volclock_amtself", "min60", "volclock", "amtself", "Quarterly crash x clock x state."),
    C3("x3_semivol60_med_volclock", "semivol60", "med60", "volclock", "Quarterly semivol x stretch x clock."),
    C3("x3_semivol60_rev60_amtself", "semivol60", "rev60", "amtself", "Quarterly semivol x reversal x state."),
    C3("x3_gapmed_med_amtself", "gapmed", "med60", "amtself", "Overnight drift x stretch x state."),
    C3("x3_gapmed_volclock_amtself", "gapmed", "volclock", "amtself", "Overnight drift x clock x state."),
    C3("x3_retonhiHL_med_volclock", "retonhiHL", "med60", "volclock", "Returns-on-wide x stretch x clock."),
    C3("x3_retonhiHL_rev60_amtself", "retonhiHL", "rev60", "amtself", "Returns-on-wide x reversal x state."),
    C3("x3_aggrupdn_med_volclock", "aggrupdn", "med60", "volclock", "Aggr-asymmetry x stretch x clock."),
    C3("x3_aggrupdn_rev60_amtself", "aggrupdn", "rev60", "amtself", "Aggr-asymmetry x reversal x state."),
    C3("x3_hlupdn_med_amtself", "hlupdn", "med60", "amtself", "Range-asymmetry x stretch x state."),
    C3("x3_hlupdn_volclock_amtself", "hlupdn", "volclock", "amtself", "Range-asymmetry x clock x state."),
    C3("x3_lagchase_med_amtself", "lagchase", "med60", "amtself", "Lagged chase x stretch x state."),
    C3("x3_lagchase_volclock_amtself", "lagchase", "volclock", "amtself", "Lagged chase x clock x state."),
    C3("x3_nvolspike_med_amtself", "nvolspike", "med60", "amtself", "Volume spike x stretch x state."),
    C3("x3_nvolspike_rev60_volclock", "nvolspike", "rev60", "volclock", "Volume spike x reversal x clock."),
    C3("x3_maxfreq120_med_amtself", "maxfreq120", "med60", "amtself", "Semiannual lottery x stretch x state."),
    C3("x3_maxfreq120_volclock_amtself", "maxfreq120", "volclock", "amtself", "Semiannual lottery x clock x state."),
    C3("x3_aggrmin60_med_amtself", "aggrmin60", "med60", "amtself", "Capitulation close x stretch x state."),
    C3("x3_aggrmin60_rev60_volclock", "aggrmin60", "rev60", "volclock", "Capitulation close x reversal x clock."),
    C3("x3_gapmed20_med_amtself", "gapmed20", "med60", "amtself", "Fast overnight drift x stretch x state."),
    C3("x3_retvrcorr_med_volclock", "retvrcorr", "med60", "volclock", "Return-attention coupling x stretch x clock."),
    C3("x3_retvrcorr_rev60_amtself", "retvrcorr", "rev60", "amtself", "Return-attention coupling x reversal x state."),
    C3("x3_aggrmax60_gapvol_amtself", "aggrmax60", "gapvol", "amtself", "Quarterly aggr x overnight risk x state."),
    C3("x3_semivol60_gapvol_amtself", "semivol60", "gapvol", "amtself", "Quarterly semivol x overnight risk x state."),
    C3("x3_retonhiHL_gapvol_amtself", "retonhiHL", "gapvol", "amtself", "Returns-on-wide x overnight risk x state."),
    # ===== PROBE: 6 strong-parent pairs =====
    C("x_aggrmax60_amtself", "aggrmax60", "amtself", "Quarterly aggr x state pair."),
    C("x_min60_amtself", "min60", "amtself", "Quarterly crash x state pair."),
    C("x_semivol60_amtself", "semivol60", "amtself", "Quarterly semivol x state pair."),
    C("x_retonhiHL_amtself", "retonhiHL", "amtself", "Returns-on-wide x state pair."),
    C("x_gapmed_rev60", "gapmed", "rev60", "Overnight drift x reversal pair."),
    C("x_aggrmin60_amtself", "aggrmin60", "amtself", "Capitulation close x state pair."),
    # ===== EXPLORE: 6 four-way products (insight: testing) =====
    C4("x4_aggrmax60_med_volclock_amtself", "aggrmax60", "med60", "volclock", "amtself", "4-way: aggr x stretch x clock x state."),
    C4("x4_semivol60_med_volclock_amtself", "semivol60", "med60", "volclock", "amtself", "4-way: semivol x stretch x clock x state."),
    C4("x4_gapvol_rev60_volclock_amtself", "gapvol", "rev60", "volclock", "amtself", "4-way: overnight x reversal x clock x state."),
    C4("x4_maxfreq_med_amtself_gapvol", "maxfreq", "med60", "amtself", "gapvol", "4-way: lottery x stretch x state x overnight."),
    C4("x4_retonhiHL_med_volclock_amtself", "retonhiHL", "med60", "volclock", "amtself", "4-way: returns-on-wide x stretch x clock x state."),
    C4("x4_hlmed60_med_volclock_amtself", "hlmed60", "med60", "volclock", "amtself", "4-way: median range x stretch x clock x state."),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
