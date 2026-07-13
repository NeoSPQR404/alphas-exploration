# canonical_composite — Round 1 (40 candidates) — 2026-07-10.
# Fresh composition campaign over the current 105 individual canonical
# factors. Templates from the prior campaign (git history): pairs =
# excitement-count x stretch/state (negative sign), 3-ways positive and
# richest; void/conditional parents fail; volclock only inside 3-ways.
# 18 re-derivations of prior winners + 22 new-parent compositions.

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
    # legacy champions
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
    # new-class parents (accepted rounds 11-18)
    "dipbuy":    f"TsCount({_DIPBUY} > 0.5, 60)",
    "gapdipmag": f"TsSum(({_GAP}) * {_DIPBUY}, 60)",
    "pin":       f"-TsCount(Abs({_AGG}) < 0.002, 60)",
    "truegapdn": "-TsCount((OPEN < Delay(LOW, 1)) > 0.5, 60)",
    "island":    "-TsCount(((OPEN > Delay(HIGH, 1)) * (LOW > Delay(HIGH, 1))) > 0.5, 60)",
    "doji":      f"-TsCount(Abs({_ID}) < 0.002, 60)",
    "aggrhigh":  f"-TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60)",
    "hlbest":    f"-TsMean(({_HL}) * (RET >= TsMax(RET, 20)), 60)",
    "volaccel":  "-(TsMean(VOLUME, 20) / (Delay(TsMean(VOLUME, 20), 20) + 1))",
}

def _ix(a, b):
    return f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5)"

def _ix3(a, b, c):
    return (f"(CsRank({P[a]}) - 0.5) * (CsRank({P[b]}) - 0.5) "
            f"* (CsRank({P[c]}) - 0.5)")

def C(n, a, b, why):
    return dict(name=n, expr=_ix(a, b), family="pair", rationale=why,
                logic_score=66)

def C3(n, a, b, c, why):
    return dict(name=n, expr=_ix3(a, b, c), family="threeway",
                rationale=why, logic_score=65)

CANDIDATES = [
    # ------------- re-derivations of prior winners (18)
    C("x_nvolburst_med", "nvolburst", "med60", "Prior winner re-derived."),
    C("x_hlburst_rev20", "hlburst", "rev20", "Prior winner re-derived."),
    C("x_aggrmax_med", "aggrmax", "med60", "Prior winner re-derived."),
    C("x_maxfreq_amtself", "maxfreq", "amtself", "Prior winner re-derived."),
    C("x_maxfreq_med", "maxfreq", "med60", "Prior winner re-derived."),
    C("x_hlburst_amtself", "hlburst", "amtself", "Prior winner re-derived."),
    C("x_aggrburst_med", "aggrburst", "med60", "Prior winner re-derived."),
    C("x_aggrburst_rev20", "aggrburst", "rev20", "Prior winner re-derived."),
    C("x_nvolburst_rev60", "nvolburst", "rev60", "Prior winner re-derived."),
    C("x_maxfreq_rev60", "maxfreq", "rev60", "Prior winner re-derived."),
    C3("x3_med_volclock_maxfreq", "med60", "volclock", "maxfreq", "Prior 3-way re-derived."),
    C3("x3_rev60_volclock_amtself", "rev60", "volclock", "amtself", "Prior 3-way re-derived."),
    C3("x3_aggrmax_med_volclock", "aggrmax", "med60", "volclock", "Prior 3-way re-derived."),
    C3("x3_hlburst_nvolburst_med", "hlburst", "nvolburst", "med60", "Prior 3-way re-derived."),
    C3("x3_nvolburst_med_amtself", "nvolburst", "med60", "amtself", "Prior 3-way re-derived."),
    C3("x3_gapvol_maxfreq_med", "gapvol", "maxfreq", "med60", "Prior 3-way re-derived."),
    C3("x3_maxfreq_amtself_med", "maxfreq", "amtself", "med60", "Prior 3-way re-derived."),
    C3("x3_hlburst_volclock_rev20", "hlburst", "volclock", "rev20", "Prior 3-way re-derived."),
    # ------------- new-parent pairs (12)
    C("x_dipbuy_med", "dipbuy", "med60", "Absorption count x stretch."),
    C("x_dipbuy_amtself", "dipbuy", "amtself", "Absorption x dollar-attention state."),
    C("x_dipbuy_gapvol", "dipbuy", "gapvol", "Absorption x overnight risk."),
    C("x_pin_med", "pin", "med60", "Stalemates x stretch."),
    C("x_pin_rev60", "pin", "rev60", "Stalemates x reversal."),
    C("x_pin_amtself", "pin", "amtself", "Stalemates x dollar state."),
    C("x_truegapdn_med", "truegapdn", "med60", "Range-breaks x stretch."),
    C("x_truegapdn_amtself", "truegapdn", "amtself", "Range-breaks x dollar state."),
    C("x_island_med", "island", "med60", "Islands x stretch."),
    C("x_doji_med", "doji", "med60", "Dojis x stretch."),
    C("x_maxfreq_hlbest", "maxfreq", "hlbest", "Lottery count x best-day texture state."),
    C("x_dipbuy_maxfreq", "dipbuy", "maxfreq", "Absorption x lottery (two counts — failed template, one control probe)."),
    # ------------- new-parent 3-ways (10)
    C3("x3_dipbuy_med_volclock", "dipbuy", "med60", "volclock", "Absorption x stretch x clock."),
    C3("x3_dipbuy_maxfreq_med", "dipbuy", "maxfreq", "med60", "Absorption x lottery x stretch."),
    C3("x3_pin_med_volclock", "pin", "med60", "volclock", "Stalemates x stretch x clock."),
    C3("x3_pin_maxfreq_amtself", "pin", "maxfreq", "amtself", "Stalemates x lottery x state."),
    C3("x3_truegapdn_med_amtself", "truegapdn", "med60", "amtself", "Range-breaks x stretch x state."),
    C3("x3_gapdipmag_volclock_amtself", "gapdipmag", "volclock", "amtself", "Dip-depth magnitude x clock x state."),
    C3("x3_aggrhigh_med_volclock", "aggrhigh", "med60", "volclock", "Aggression-at-highs x stretch x clock."),
    C3("x3_hlbest_rev60_amtself", "hlbest", "rev60", "amtself", "Best-day texture x reversal x state."),
    C3("x3_volaccel_med_maxfreq", "volaccel", "med60", "maxfreq", "Acceleration x stretch x lottery."),
    C3("x3_doji_rev60_volclock", "doji", "rev60", "volclock", "Dojis x reversal x clock."),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
