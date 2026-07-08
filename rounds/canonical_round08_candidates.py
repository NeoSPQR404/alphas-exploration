# Canonical set — Round 8 (21 candidates) — generated 2026-07-08.
#
# Set 84 -> target 100. Retrieve (cR7): composition pattern = one
# excitement-COUNT parent x one stretch/STATE parent; 3-way products
# work (0.053, positive sign) and raise diversity; void/conditional/
# volclock-pair parents dead. This round: saturate the count x stretch
# grid and expand the 3-way tier.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

P = {
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "hlburst":   f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)",
    "nvolburst": f"-TsCount({_NVOL} > 2, 60)",
    "aggrburst": f"-TsCount(({_AGG}) > 2 * TsStd({_AGG}, 60), 60)",
    "rev20":     f"-TsSum({_ID}, 20)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    "aggrmax":   f"-TsMax({_AGG}, 20)",
    "mingap60":  f"-TsMin({_GAP}, 60)",
    "hlmed60":   f"-TsMed({_HL}, 60)",
}

def _ix(a, b):
    return f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5)"

def _ix3(a, b, c):
    return f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5) * (CsRank({P[c]}) - 0.5)"

def C(name, a, b, why, ls=67):
    return dict(name=name, expr=_ix(a, b), family="composition",
                rationale=why, logic_score=ls)

def C3(name, a, b, c, why, ls=65):
    return dict(name=name, expr=_ix3(a, b, c), family="composition3",
                rationale=why, logic_score=ls)

CANDIDATES = [
    # ------------- count x stretch/state grid completion (11)
    C("cx_nvolburst_rev20", "nvolburst", "rev20", "Attention bursts x monthly reversal."),
    C("cx_nvolburst_rev60", "nvolburst", "rev60", "Attention bursts x quarterly reversal."),
    C("cx_nvolburst_amtself", "nvolburst", "amtself", "Attention bursts x dollar-attention state."),
    C("cx_hlburst_med", "hlburst", "med60", "Range bursts x quarterly stretch."),
    C("cx_hlburst_amtself", "hlburst", "amtself", "Range bursts x dollar-attention state."),
    C("cx_maxfreq_med", "maxfreq", "med60", "Lottery frequency x quarterly stretch."),
    C("cx_maxfreq_rev60", "maxfreq", "rev60", "Lottery frequency x quarterly reversal."),
    C("cx_aggrburst_med", "aggrburst", "med60", "Aggression bursts x stretch."),
    C("cx_aggrburst_rev20", "aggrburst", "rev20", "Aggression bursts x reversal."),
    C("cx_mingap_maxfreq", "mingap60", "maxfreq", "Gap-crash depth x lottery frequency."),
    C("cx_mingap_nvolburst", "mingap60", "nvolburst", "Gap-crash depth x attention bursts."),
    # ------------- count x count (2)
    C("cx_nvolburst_hlburst", "nvolburst", "hlburst", "Two excitement counts agreeing: crowd + range."),
    C("cx_maxfreq_aggrburst", "maxfreq", "aggrburst", "Return-lottery x aggression-lottery agreement."),
    # ------------- 3-way tier (8)
    C3("cx3_hlburst_volclock_rev", "hlburst", "volclock", "rev20", "Burst x clock x reversal."),
    C3("cx3_nvolburst_med_amtself", "nvolburst", "med60", "amtself", "Burst x stretch x state."),
    C3("cx3_gapvol_maxfreq_med", "gapvol", "maxfreq", "med60", "Overnight risk x lottery x stretch."),
    C3("cx3_maxfreq_amtself_med", "maxfreq", "amtself", "med60", "Lottery x state x stretch."),
    C3("cx3_hlburst_nvolburst_med", "hlburst", "nvolburst", "med60", "Double-burst x stretch."),
    C3("cx3_aggrmax_med_volclock", "aggrmax", "med60", "volclock", "Aggression x stretch x clock."),
    C3("cx3_mingap_maxfreq_volclock", "mingap60", "maxfreq", "volclock", "Crash x lottery x clock."),
    C3("cx3_rev60_volclock_amtself", "rev60", "volclock", "amtself", "Reversal x clock x state."),
]

assert len(CANDIDATES) == 21, len(CANDIDATES)
