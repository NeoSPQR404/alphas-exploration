# canonical_composite — Round 2 (40 candidates) — 2026-07-10.
# Extend the fresh campaign. Retrieve (composite memory): templates =
# count/magnitude/texture parent x stretch/state parent; 3-ways with
# volclock strongest; parents <~0.05 IS IC don't compose; count x count
# fails. This round: exploit the strong new-class parents (all with
# |IS IC| >= 0.05) that Round 1 confirmed, expand the 3-way grid, and
# probe untried strong-parent pairs.

SET_NAME = "canonical_composite"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_DIPBUY = f"(({_GAP}) < 0) * (({_ID}) > 0)"

# Parent pool — only strong (|IS IC| >= ~0.05) canonical factors, the
# gate on composition quality from Round 1.
P = {
    # stretch / state
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "rev20":     f"-TsSum({_ID}, 20)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    "hlmed60":   f"-TsMed({_HL}, 60)",
    "semivol":   "-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
    # counts / magnitudes / textures
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "hlburst":   f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)",
    "nvolburst": f"-TsCount({_NVOL} > 2, 60)",
    "aggrmax":   f"-TsMax({_AGG}, 20)",
    "gapdipmag": f"TsSum(({_GAP}) * {_DIPBUY}, 60)",
    "gapcapmag": f"TsSum(({_GAP}) * ((({_GAP}) < 0) * (({_ID}) < 0)), 60)",
    "aggrhigh":  f"-TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60)",
    "hlbest":    f"-TsMean(({_HL}) * (RET >= TsMax(RET, 20)), 60)",
    "nvoldip":   f"-TsMean(({_NVOL}) * {_DIPBUY}, 60)",
    "pinfast":   f"-TsCount(Abs({_AGG}) < 0.002, 20)",
    "volat":     "-(TsSum(CLOSE / OPEN - 1, 60))",
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
    # ---- new-class parent pairs with stretch/state (10)
    C("x_gapdipmag_amtself", "gapdipmag", "amtself", "Dip-depth x dollar state."),
    C("x_gapdipmag_volclock", "gapdipmag", "volclock", "Dip-depth x clock."),
    C("x_gapcapmag_med", "gapcapmag", "med60", "Capitulation-depth x stretch."),
    C("x_gapcapmag_amtself", "gapcapmag", "amtself", "Capitulation-depth x state."),
    C("x_aggrhigh_amtself", "aggrhigh", "amtself", "Aggression-at-highs x state."),
    C("x_aggrhigh_rev60", "aggrhigh", "rev60", "Aggression-at-highs x reversal."),
    C("x_hlbest_med", "hlbest", "med60", "Best-day texture x stretch."),
    C("x_hlbest_amtself", "hlbest", "amtself", "Best-day texture x state."),
    C("x_nvoldip_med", "nvoldip", "med60", "Crowd-at-absorption x stretch."),
    C("x_nvoldip_amtself", "nvoldip", "amtself", "Crowd-at-absorption x state."),
    # ---- untried strong-parent pairs (6)
    C("x_semivol_amtself", "semivol", "amtself", "Vol-shape x state."),
    C("x_gapvol_amtself", "gapvol", "amtself", "Overnight risk x state."),
    C("x_aggrmax_amtself", "aggrmax", "amtself", "Peak aggression x state."),
    C("x_hlmed_amtself", "hlmed60", "amtself", "Median range x state."),
    C("x_semivol_med", "semivol", "med60", "Vol-shape x stretch."),
    C("x_aggrmax_rev60", "aggrmax", "rev60", "Peak aggression x reversal."),
    # ---- new-class 3-ways (14)
    C3("x3_gapcapmag_volclock_amtself", "gapcapmag", "volclock", "amtself", "Cap-depth x clock x state."),
    C3("x3_aggrhigh_rev60_amtself", "aggrhigh", "rev60", "amtself", "Aggr-highs x reversal x state."),
    C3("x3_hlbest_med_volclock", "hlbest", "med60", "volclock", "Best-day x stretch x clock."),
    C3("x3_nvoldip_med_volclock", "nvoldip", "med60", "volclock", "Crowd-absorption x stretch x clock."),
    C3("x3_gapdipmag_med_amtself", "gapdipmag", "med60", "amtself", "Dip-depth x stretch x state."),
    C3("x3_aggrhigh_maxfreq_med", "aggrhigh", "maxfreq", "med60", "Aggr-highs x lottery x stretch."),
    C3("x3_hlbest_volclock_amtself", "hlbest", "volclock", "amtself", "Best-day x clock x state."),
    C3("x3_semivol_volclock_amtself", "semivol", "volclock", "amtself", "Vol-shape x clock x state."),
    C3("x3_gapvol_med_amtself", "gapvol", "med60", "amtself", "Overnight risk x stretch x state."),
    C3("x3_hlburst_med_amtself", "hlburst", "med60", "amtself", "Range-burst x stretch x state."),
    C3("x3_nvolburst_volclock_amtself", "nvolburst", "volclock", "amtself", "Attn-burst x clock x state."),
    C3("x3_aggrmax_rev60_volclock", "aggrmax", "rev60", "volclock", "Peak aggr x reversal x clock."),
    C3("x3_gapcapmag_med_maxfreq", "gapcapmag", "med60", "maxfreq", "Cap-depth x stretch x lottery."),
    C3("x3_semivol_med_maxfreq", "semivol", "med60", "maxfreq", "Vol-shape x stretch x lottery."),
    # ---- control probes (4): count x count (should fail), weak parent
    C("x_maxfreq_hlburst", "maxfreq", "hlburst", "Count x count control (expected fail)."),
    C("x_gapdipmag_gapcapmag", "gapdipmag", "gapcapmag", "Two day-type magnitudes: correlated parents probe."),
    C3("x3_pinfast_med_volclock", "pinfast", "med60", "volclock", "Weak pin parent inside a 3-way probe."),
    C("x_volat_amtself", "volat", "amtself", "Quarterly reversal x state (rev60 sibling check)."),
    # ---- fill to 40: more new-class 3-ways (6)
    C3("x3_nvoldip_rev60_amtself", "nvoldip", "rev60", "amtself", "Crowd-absorption x reversal x state."),
    C3("x3_gapdipmag_volclock_maxfreq", "gapdipmag", "volclock", "maxfreq", "Dip-depth x clock x lottery."),
    C3("x3_aggrhigh_gapvol_amtself", "aggrhigh", "gapvol", "amtself", "Aggr-highs x overnight risk x state."),
    C3("x3_hlbest_maxfreq_amtself", "hlbest", "maxfreq", "amtself", "Best-day x lottery x state."),
    C3("x3_semivol_rev60_volclock", "semivol", "rev60", "volclock", "Vol-shape x reversal x clock."),
    C3("x3_hlmed_volclock_amtself", "hlmed60", "volclock", "amtself", "Median range x clock x state."),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
