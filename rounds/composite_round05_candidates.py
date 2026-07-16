# canonical_composite — Round 5 (34 candidates) — 2026-07-10.
# Close from 88 to 100. Pairs and four-ways are closed (forbidden);
# insights four-way + sign-conditioned refuted. Pure exploitation of the
# threeway tier (0.82 success): FRESH triples among confirmed-strong
# parents, novel combinations to minimise S2 dedup against 88 residents.

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

P = {
    "med60":     "-(CLOSE / TsMed(CLOSE, 60) - 1)",
    "rev60":     f"-TsSum({_ID}, 60)",
    "amtself":   "-TsRank(Log(AMOUNT), 120)",
    "volclock":  "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))",
    "gapvol":    f"-TsStd({_GAP}, 20)",
    "max20":     "-TsMax(RET, 20)",
    "aggrmax":   f"-TsMax({_AGG}, 20)",
    "aggrmax60": f"-TsMax({_AGG}, 60)",
    "semivol":   "-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
    "semivol60": "-(TsStd((RET + Abs(RET)) / 2, 60) - TsStd((RET - Abs(RET)) / 2, 60))",
    "semivol120": "-(TsStd((RET + Abs(RET)) / 2, 120) - TsStd((RET - Abs(RET)) / 2, 120))",
    "maxfreq":   "-TsCount(RET > 2 * TsStd(RET, 60), 60)",
    "hlburst":   f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)",
    "nvolburst": f"-TsCount({_NVOL} > 2, 60)",
    "nvolspike": "-(TsMean(VOLUME, 5) / TsMean(VOLUME, 60))",
    "gapdipmag": f"TsSum(({_GAP}) * {_DIPBUY}, 60)",
    "gapcapmag": f"TsSum(({_GAP}) * {_CAPIT}, 60)",
    "aggrhigh":  f"-TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60)",
    "hlbest":    f"-TsMean(({_HL}) * (RET >= TsMax(RET, 20)), 60)",
    "nvoldip":   f"-TsMean(({_NVOL}) * {_DIPBUY}, 60)",
    "hlonhivol": f"-TsMean(({_HL}) * ({_NVOL} > 1), 60)",
    "retonhivol": "-TsSum(RET * (VOLUME > TsMean(VOLUME, 60)), 60)",
    "idonhivol": f"-TsSum(({_ID}) * (VOLUME > TsMean(VOLUME, 120)), 120)",
    "retonhiHL": f"-TsSum(RET * (({_HL}) > TsMean({_HL}, 120)), 120)",
    "hlmed60":   f"-TsMed({_HL}, 60)",
}

def R(k): return f"(CsRank({P[k]}) - 0.5)"
def C3(n,a,b,c,w): return dict(name=n, expr=f"{R(a)} * {R(b)} * {R(c)}", family="threeway", rationale=w, logic_score=65)

CANDIDATES = [
    # two-novel + one-anchor (fresh cross-family interactions)
    C3("x3_max20_semivol_amtself", "max20", "semivol", "amtself", "Lottery x vol-shape x state."),
    C3("x3_max20_aggrmax_volclock", "max20", "aggrmax", "volclock", "Lottery x peak-aggr x clock."),
    C3("x3_semivol_aggrmax_amtself", "semivol", "aggrmax", "amtself", "Vol-shape x peak-aggr x state."),
    C3("x3_hlbest_aggrhigh_volclock", "hlbest", "aggrhigh", "volclock", "Best-day x aggr-at-highs x clock."),
    C3("x3_gapdipmag_gapcapmag_volclock", "gapdipmag", "gapcapmag", "volclock", "Dip-depth x cap-depth x clock."),
    C3("x3_nvoldip_hlbest_amtself", "nvoldip", "hlbest", "amtself", "Crowd-absorption x best-day x state."),
    C3("x3_retonhivol_idonhivol_amtself", "retonhivol", "idonhivol", "amtself", "Ret-on-attn x intraday-on-attn x state."),
    C3("x3_hlonhivol_retonhivol_volclock", "hlonhivol", "retonhivol", "volclock", "Range-on-attn x ret-on-attn x clock."),
    C3("x3_max20_hlbest_volclock", "max20", "hlbest", "volclock", "Lottery x best-day x clock."),
    C3("x3_semivol120_aggrmax60_amtself", "semivol120", "aggrmax60", "amtself", "Semiannual semivol x quarterly aggr x state."),
    C3("x3_nvolspike_maxfreq_amtself", "nvolspike", "maxfreq", "amtself", "Volume spike x lottery x state."),
    C3("x3_hlburst_aggrmax_volclock", "hlburst", "aggrmax", "volclock", "Range-burst x peak-aggr x clock."),
    C3("x3_nvolburst_semivol_amtself", "nvolburst", "semivol", "amtself", "Attn-burst x vol-shape x state."),
    C3("x3_gapdipmag_aggrhigh_amtself", "gapdipmag", "aggrhigh", "amtself", "Dip-depth x aggr-at-highs x state."),
    C3("x3_retonhiHL_hlbest_amtself", "retonhiHL", "hlbest", "amtself", "Ret-on-wide x best-day x state."),
    C3("x3_aggrmax60_semivol60_volclock", "aggrmax60", "semivol60", "volclock", "Quarterly aggr x semivol x clock."),
    C3("x3_max20_gapdipmag_volclock", "max20", "gapdipmag", "volclock", "Lottery x dip-depth x clock."),
    # novel + two fresh-anchor-pair
    C3("x3_max20_med_gapvol", "max20", "med60", "gapvol", "Lottery x stretch x overnight risk."),
    C3("x3_semivol_med_gapvol", "semivol", "med60", "gapvol", "Vol-shape x stretch x overnight risk."),
    C3("x3_hlbest_med_rev60", "hlbest", "med60", "rev60", "Best-day x stretch x reversal."),
    C3("x3_nvoldip_med_rev60", "nvoldip", "med60", "rev60", "Crowd-absorption x stretch x reversal."),
    C3("x3_gapdipmag_med_rev60", "gapdipmag", "med60", "rev60", "Dip-depth x stretch x reversal."),
    C3("x3_retonhivol_med_rev60", "retonhivol", "med60", "rev60", "Ret-on-attn x stretch x reversal."),
    C3("x3_hlonhivol_med_rev60", "hlonhivol", "med60", "rev60", "Range-on-attn x stretch x reversal."),
    C3("x3_idonhivol_med_rev60", "idonhivol", "med60", "rev60", "Intraday-on-attn x stretch x reversal."),
    C3("x3_max20_med_rev60", "max20", "med60", "rev60", "Lottery x stretch x reversal."),
    C3("x3_semivol_volclock_rev60", "semivol", "volclock", "rev60", "Vol-shape x clock x reversal."),
    C3("x3_maxfreq_volclock_rev60", "maxfreq", "volclock", "rev60", "Lottery x clock x reversal."),
    C3("x3_aggrmax_volclock_rev60", "aggrmax", "volclock", "rev60", "Peak-aggr x clock x reversal."),
    C3("x3_nvolburst_med_gapvol", "nvolburst", "med60", "gapvol", "Attn-burst x stretch x overnight risk."),
    C3("x3_hlmed_gapvol_amtself", "hlmed60", "gapvol", "amtself", "Median range x overnight risk x state."),
    C3("x3_hlbest_gapvol_amtself", "hlbest", "gapvol", "amtself", "Best-day x overnight risk x state."),
    C3("x3_semivol60_med_amtself", "semivol60", "med60", "amtself", "Quarterly semivol x stretch x state."),
    C3("x3_gapcapmag_gapvol_amtself", "gapcapmag", "gapvol", "amtself", "Cap-depth x overnight risk x state."),
]

assert len(CANDIDATES) == 34, len(CANDIDATES)
