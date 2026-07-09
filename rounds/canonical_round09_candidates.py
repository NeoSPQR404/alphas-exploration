# Canonical set — Round 9 (10 candidates) — generated 2026-07-09.
#
# Set 97 -> target 100: closing round. cR8 went 7/7 on 3-way products;
# this round is fresh 3-way triples from untried parent combinations
# (count/stretch/state pools), avoiding mingap and count-x-count books.

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
    "hlmed60":   f"-TsMed({_HL}, 60)",
    "semivol":   "-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
    "max20":     "-TsMax(RET, 20)",
}

def _ix3(a, b, c):
    return (f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5) "
            f"* (CsRank({P[c]}) - 0.5)")

def C3(name, a, b, c, why):
    return dict(name=name, expr=_ix3(a, b, c), family="composition3",
                rationale=why, logic_score=65)

CANDIDATES = [
    C3("cx3_semivol_volclock_amtself", "semivol", "volclock", "amtself",
       "Vol-shape x clock x dollar-state."),
    C3("cx3_max20_med_volclock", "max20", "med60", "volclock",
       "Lottery magnitude x stretch x clock."),
    C3("cx3_gapvol_rev60_amtself", "gapvol", "rev60", "amtself",
       "Overnight risk x reversal x state."),
    C3("cx3_aggrburst_med_amtself", "aggrburst", "med60", "amtself",
       "Aggression bursts x stretch x state."),
    C3("cx3_hlmed_volclock_maxfreq", "hlmed60", "volclock", "maxfreq",
       "Median range x clock x lottery freq."),
    C3("cx3_semivol_med_maxfreq", "semivol", "med60", "maxfreq",
       "Vol-shape x stretch x lottery freq."),
    C3("cx3_nvolburst_rev20_volclock", "nvolburst", "rev20", "volclock",
       "Attention bursts x fast reversal x clock."),
    C3("cx3_aggrmax_rev60_amtself", "aggrmax", "rev60", "amtself",
       "Peak aggression x reversal x state."),
    C3("cx3_gapvol_med_volclock", "gapvol", "med60", "volclock",
       "Overnight risk x stretch x clock."),
    C3("cx3_hlburst_amtself_rev60", "hlburst", "amtself", "rev60",
       "Range bursts x state x reversal."),
]

assert len(CANDIDATES) == 10, len(CANDIDATES)
