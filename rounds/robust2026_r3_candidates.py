"""robust_2026 Round 3 — NEW DATA FAMILY: value / fundamentals (orthogonal to
the set's all-price/volume/flow residents). Fields: EP/BP/SP/CFP yields, PE/PB/PS
valuations, CMV size, industry-neutralization.

Caveat (project history): fundamentals are largely DEAD at the 10d horizon — only
industry-neutral EP/CFP value has ever cleared; BP, quality levels, earnings
momentum are behavioral_full-forbidden. Under GATE_ON_NEUTRALIZED the gate also
size-neutralizes, removing value's size component, so only size-orthogonal value
alpha can survive. This round tests which value/quality constructs clear at 10d
AND hold in 2026. Best-shot forms: industry-neutral value, ROE-from-yields
quality, value composites, value re-rating.
"""
SET_NAME = "robust_2026"

CANDIDATES = [
    # industry-neutral value yields (the known survivors' form)
    {"name": "ep_indneut", "family": "value", "logic_score": 0.65,
     "expr": "CsIndNeutralize(EP, IND)",
     "rationale": "Industry-neutral earnings yield — the one value signal that has cleared at 10d."},
    {"name": "cfp_indneut", "family": "value", "logic_score": 0.65,
     "expr": "CsIndNeutralize(CFP, IND)",
     "rationale": "Industry-neutral cash-flow yield — the second value survivor, holds OOS better."},
    {"name": "sp_indneut", "family": "value", "logic_score": 0.55,
     "expr": "CsIndNeutralize(SP, IND)",
     "rationale": "Industry-neutral sales yield (less-tried value quantity)."},
    {"name": "bp_indneut", "family": "value", "logic_score": 0.45,
     "expr": "CsIndNeutralize(BP, IND)",
     "rationale": "Industry-neutral book yield (dead in behavioral_full; retest for this set)."},
    {"name": "value_combo", "family": "value", "logic_score": 0.6,
     "expr": "CsIndNeutralize(EP, IND) + CsIndNeutralize(CFP, IND)",
     "rationale": "Combined industry-neutral EP+CFP value (the two survivors, blended)."},
    {"name": "value_rank_composite", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(EP) + CsRank(CFP) + CsRank(SP)",
     "rationale": "Cross-sectional value composite rank (EP/CFP/SP)."},

    # quality: ROE-from-yields (E/B), asset turnover (S/B), accruals (CFP/EP)
    {"name": "roe_proxy", "family": "quality", "logic_score": 0.6,
     "expr": "EP / BP",
     "rationale": "EP/BP = E/B = ROE proxy (quality) built from available yields."},
    {"name": "roe_indneut", "family": "quality", "logic_score": 0.6,
     "expr": "CsIndNeutralize(EP / BP, IND)",
     "rationale": "Industry-neutral ROE proxy."},
    {"name": "asset_turnover", "family": "quality", "logic_score": 0.5,
     "expr": "SP / BP",
     "rationale": "SP/BP = S/B = asset-turnover proxy."},
    {"name": "accruals_quality", "family": "quality", "logic_score": 0.55,
     "expr": "CsIndNeutralize(CFP / EP, IND)",
     "rationale": "CFP/EP = cash-flow vs earnings (accruals quality); high = earnings backed by cash."},

    # value re-rating (change in yield)
    {"name": "ep_rerate_60", "family": "value_mom", "logic_score": 0.55,
     "expr": "Delta(EP, 60)",
     "rationale": "Earnings-yield re-rating over a quarter (value improving)."},
    {"name": "cfp_rerate_120", "family": "value_mom", "logic_score": 0.5,
     "expr": "Delta(CFP, 120)",
     "rationale": "Cash-flow-yield re-rating, semi-annual."},

    # valuation inverse / size
    {"name": "cheap_pb", "family": "value", "logic_score": 0.45,
     "expr": "-CsIndNeutralize(PB, IND)",
     "rationale": "Industry-neutral cheap-book (inverse PB)."},
    {"name": "cheap_ps", "family": "value", "logic_score": 0.5,
     "expr": "-CsIndNeutralize(PS, IND)",
     "rationale": "Industry-neutral cheap-sales (inverse PS)."},
    {"name": "size_small", "family": "size", "logic_score": 0.45,
     "expr": "-Log(CMV)",
     "rationale": "Small-size premium (size is slow/weak at 10d; retest under neutralized gating)."},
    {"name": "quality_value", "family": "quality", "logic_score": 0.55,
     "expr": "CsRank(EP / BP) + CsRank(CFP)",
     "rationale": "Quality (ROE) + value (CFP) composite rank."},
]

assert len(CANDIDATES) == 16, len(CANDIDATES)
