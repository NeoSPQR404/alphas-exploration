# canonical_composite — Round 3 (40 candidates) — 2026-07-10.
# Generated to the memory generation_plan(40): recent rate 0.575 -> rich
# vein -> 70/15/15 exploit/probe/explore.
#   exploit (28): NEW three-way products (threeway family, 0.82 success)
#   probe   (6):  legacy strong-parent PAIRS (pair family, undetermined)
#   explore (6):  the two seeded insights — four-way products (3) and
#                 sign-conditioned composition (3)
# avoid: new-class parent PAIRS and weak parents (forbidden patterns).

SET_NAME = "canonical_composite"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_DIPBUY = f"(({_GAP}) < 0) * (({_ID}) > 0)"
_CAPIT = f"(({_GAP}) < 0) * (({_ID}) < 0)"

# strong parent pool (all |IS IC| >= ~0.05 as individual factors)
P = {
    # stretch / state / shape
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    "hlmed60":   f"-TsMed({_HL}, 60)",
    "semivol":   "-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
    # counts / magnitudes / textures
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "max20":     "-TsMax(RET, 20)",
    "aggrmax":   f"-TsMax({_AGG}, 20)",
    "hlburst":   f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)",
    "nvolburst": f"-TsCount({_NVOL} > 2, 60)",
    "gapdipmag": f"TsSum(({_GAP}) * {_DIPBUY}, 60)",
    "gapcapmag": f"TsSum(({_GAP}) * {_CAPIT}, 60)",
    "aggrhigh":  f"-TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60)",
    "hlbest":    f"-TsMean(({_HL}) * (RET >= TsMax(RET, 20)), 60)",
    "nvoldip":   f"-TsMean(({_NVOL}) * {_DIPBUY}, 60)",
    # fresh parents not yet composed
    "hlonhivol": f"-TsMean(({_HL}) * ({_NVOL} > 1), 60)",
    "retonhivol": "-TsSum(RET * (VOLUME > TsMean(VOLUME, 60)), 60)",
    "idonhivol": f"-TsSum(({_ID}) * (VOLUME > TsMean(VOLUME, 120)), 120)",
    "mingap":    f"-TsMin({_GAP}, 60)",
    "semivol120": "-(TsStd((RET + Abs(RET)) / 2, 120) - TsStd((RET - Abs(RET)) / 2, 120))",
}

def R(k):  # demeaned rank of parent k
    return f"(CsRank({P[k]}) - 0.5)"

def C3(n, a, b, c, why):
    return dict(name=n, expr=f"{R(a)} * {R(b)} * {R(c)}",
                family="threeway", rationale=why, logic_score=65)

def C(n, a, b, why):
    return dict(name=n, expr=f"{R(a)} * {R(b)}", family="pair",
                rationale=why, logic_score=65)

def C4(n, a, b, c, d, why):
    return dict(name=n, expr=f"{R(a)} * {R(b)} * {R(c)} * {R(d)}",
                family="fourway", rationale=why, logic_score=63)

def SG(n, a, b, why):  # sign-conditioned: A's magnitude gated by B's side
    return dict(name=n, expr=f"{R(a)} * Sign({R(b)})",
                family="signgate", rationale=why, logic_score=63)

CANDIDATES = [
    # ===== EXPLOIT: 28 new three-way products (fresh-parent triples) =====
    C3("x3_max20_med_amtself", "max20", "med60", "amtself", "Lottery mag x stretch x state."),
    C3("x3_max20_volclock_amtself", "max20", "volclock", "amtself", "Lottery mag x clock x state."),
    C3("x3_hlonhivol_med_volclock", "hlonhivol", "med60", "volclock", "Conditional range x stretch x clock."),
    C3("x3_hlonhivol_rev60_amtself", "hlonhivol", "rev60", "amtself", "Conditional range x reversal x state."),
    C3("x3_retonhivol_med_volclock", "retonhivol", "med60", "volclock", "Returns-on-attention x stretch x clock."),
    C3("x3_retonhivol_volclock_amtself", "retonhivol", "volclock", "amtself", "Returns-on-attention x clock x state."),
    C3("x3_idonhivol_med_amtself", "idonhivol", "med60", "amtself", "Intraday-on-attention x stretch x state."),
    C3("x3_idonhivol_rev60_volclock", "idonhivol", "rev60", "volclock", "Intraday-on-attention x reversal x clock."),
    C3("x3_mingap_med_amtself", "mingap", "med60", "amtself", "Gap-crash depth x stretch x state."),
    C3("x3_mingap_volclock_amtself", "mingap", "volclock", "amtself", "Gap-crash depth x clock x state."),
    C3("x3_semivol120_med_volclock", "semivol120", "med60", "volclock", "Semiannual semivol x stretch x clock."),
    C3("x3_semivol120_rev60_amtself", "semivol120", "rev60", "amtself", "Semiannual semivol x reversal x state."),
    C3("x3_max20_hlmed_amtself", "max20", "hlmed60", "amtself", "Lottery x median range x state."),
    C3("x3_gapcapmag_rev60_volclock", "gapcapmag", "rev60", "volclock", "Capitulation depth x reversal x clock."),
    C3("x3_gapdipmag_rev60_volclock", "gapdipmag", "rev60", "volclock", "Dip depth x reversal x clock."),
    C3("x3_aggrhigh_hlmed_amtself", "aggrhigh", "hlmed60", "amtself", "Aggr-highs x median range x state."),
    C3("x3_hlbest_gapvol_volclock", "hlbest", "gapvol", "volclock", "Best-day x overnight risk x clock."),
    C3("x3_nvoldip_gapvol_amtself", "nvoldip", "gapvol", "amtself", "Crowd-absorption x overnight risk x state."),
    C3("x3_hlonhivol_maxfreq_amtself", "hlonhivol", "maxfreq", "amtself", "Conditional range x lottery x state."),
    C3("x3_retonhivol_rev60_amtself", "retonhivol", "rev60", "amtself", "Returns-on-attention x reversal x state."),
    C3("x3_max20_gapvol_amtself", "max20", "gapvol", "amtself", "Lottery x overnight risk x state."),
    C3("x3_hlmed_rev60_amtself", "hlmed60", "rev60", "amtself", "Median range x reversal x state."),
    C3("x3_hlmed_maxfreq_volclock", "hlmed60", "maxfreq", "volclock", "Median range x lottery x clock."),
    C3("x3_semivol_gapvol_amtself", "semivol", "gapvol", "amtself", "Vol-shape x overnight risk x state."),
    C3("x3_aggrmax_gapvol_amtself", "aggrmax", "gapvol", "amtself", "Peak aggr x overnight risk x state."),
    C3("x3_hlburst_rev60_amtself", "hlburst", "rev60", "amtself", "Range-burst x reversal x state."),
    C3("x3_nvolburst_rev60_amtself", "nvolburst", "rev60", "amtself", "Attn-burst x reversal x state."),
    C3("x3_idonhivol_gapvol_amtself", "idonhivol", "gapvol", "amtself", "Intraday-on-attention x overnight risk x state."),
    # ===== PROBE: 6 legacy strong-parent pairs (untried) =====
    C("x_max20_amtself", "max20", "amtself", "Lottery mag x state pair."),
    C("x_hlmed_amtself", "hlmed60", "amtself", "Median range x state pair."),
    C("x_semivol120_amtself", "semivol120", "amtself", "Semiannual semivol x state pair."),
    C("x_retonhivol_amtself", "retonhivol", "amtself", "Returns-on-attention x state pair."),
    C("x_hlonhivol_amtself", "hlonhivol", "amtself", "Conditional range x state pair."),
    C("x_mingap_rev60", "mingap", "rev60", "Gap-crash depth x reversal pair."),
    # ===== EXPLORE: 6 insight probes =====
    # four-way-products insight
    C4("x4_med_volclock_amtself_maxfreq", "med60", "volclock", "amtself", "maxfreq",
       "4-way: stretch x clock x state x lottery (four-way-products insight)."),
    C4("x4_gapvol_med_amtself_rev60", "gapvol", "med60", "amtself", "rev60",
       "4-way: overnight risk x stretch x state x reversal."),
    C4("x4_aggrmax_med_volclock_amtself", "aggrmax", "med60", "volclock", "amtself",
       "4-way: peak aggr x stretch x clock x state."),
    # sign-conditioned-composition insight
    SG("xsg_med_by_volclock", "med60", "volclock",
       "Median stretch gated by the SIDE of the volume clock (sign-conditioned insight)."),
    SG("xsg_max20_by_amtself", "max20", "amtself",
       "Lottery magnitude gated by the side of dollar-attention state."),
    SG("xsg_gapvol_by_med", "gapvol", "med60",
       "Overnight risk gated by the side of the stretch."),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
