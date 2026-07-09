# Canonical set — Round 15 (12 candidates) — 2026-07-09.
# Novelty run 5/5 (final): normalized typed textures to break the S2
# self-locks, remaining vein corners, three non-vein wildcards.
# Individual only, thresholds unchanged.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_DIPBUY = f"(({_GAP}) < 0) * (({_ID}) > 0)"
_CAPIT = f"(({_GAP}) < 0) * (({_ID}) < 0)"

CANDIDATES = [
    # ---------------- normalized typed textures (4) — S2-lock breakers
    dict(name="c_hl_dipbuy_norm", expr=f"-(TsMean(({_HL}) * {_DIPBUY}, 60) / TsMed({_HL}, 60))", family="daytype",
         rationale="Battle intensity on dip-bought days RELATIVE to own typical range — raw version hit 0.78 vs hlmed60; normalization strips the level.", logic_score=69),
    dict(name="c_hl_capit_norm", expr=f"-(TsMean(({_HL}) * {_CAPIT}, 60) / TsMed({_HL}, 60))", family="daytype",
         rationale="Capitulation-day range vs own typical range.", logic_score=68),
    dict(name="c_capit_rel_depth", expr=f"TsSum(({_GAP}) * {_CAPIT}, 60) / (TsStd({_GAP}, 60) + 0.001)", family="daytype",
         rationale="Capitulation depth in own-gap-vol units: scale-free damage.", logic_score=68),
    dict(name="c_recover_eff", expr=f"-(TsSum(({_ID}) * {_DIPBUY}, 60) / (Abs(TsSum(({_GAP}) * {_DIPBUY}, 60)) + 0.001))", family="daytype",
         rationale="Recovery efficiency: intraday recovery per unit of dip depth on bought days.", logic_score=68),
    # ---------------- remaining vein corners (4)
    dict(name="c_nvol_capit", expr=f"-TsMean(({_NVOL}) * {_CAPIT}, 60)", family="daytype",
         rationale="Crowd size at capitulations (dip version accepted at ICIR 0.78).", logic_score=68),
    dict(name="c_amihud_dipbuy", expr=f"TsMean((Abs(RET) / AMOUNT) * {_DIPBUY}, 60)", family="daytype",
         rationale="Price impact during absorption days: thin vs deep dip-buying.", logic_score=67),
    dict(name="c_bigdip_vwap_mag", expr=f"-TsSum(({_AGG}) * (({_GAP}) < -TsStd({_GAP}, 60)), 60)", family="daytype",
         rationale="Closing aggression on LARGE gap-down days: conviction under stress.", logic_score=67),
    dict(name="c_dipbuy_rec", expr=f"CsRank(HighDay({_DIPBUY}, 120))", family="daytype",
         rationale="Days since the last dip-bought day: absorption recency (recency class weak historically — one vein slot).", logic_score=65),
    # ---------------- non-vein wildcards (4)
    dict(name="c_dollar_depth", expr=f"-TsMed(AMOUNT / (({_HL}) + 0.001), 60)", family="liquidity",
         rationale="Dollar depth: money traded per unit of range — how much flow it takes to move price (inverse-impact, robust median).", logic_score=69),
    dict(name="c_gap_kurt", expr=f"-TsKurt({_GAP}, 60)", family="overnight",
         rationale="Gap tail-shape: episodic overnight shocks vs steady drift (return kurt dead; gap kurt untested).", logic_score=65),
    dict(name="c_aggr_med_dev", expr=f"-(({_AGG}) - TsMed({_AGG}, 60))", family="aggression",
         rationale="Today's aggression vs own median stance: robust aggression surprise.", logic_score=65),
    dict(name="c_range_eff_med", expr=f"-TsMed(Abs(RET) / (({_HL}) + 0.001), 60)", family="volatility",
         rationale="Median movement efficiency: net move per unit range, robust form (mean form failed at S1; median may differ).", logic_score=65),
]

assert len(CANDIDATES) == 12, len(CANDIDATES)
