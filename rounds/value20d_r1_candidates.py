"""value_20d Round 1 — a dedicated 20-DAY value/fundamental sleeve. Value has
more punch at a monthly horizon than at 10d (R3-R4 on robust_2026 showed value is
orthogonal but too weak at 10d). Fresh set, prefix valpha_.

Sets HORIZON=20 for this round's process only (round.py runs this file via runpy
before it reads cfg.HORIZON; each round is a separate process). Gates on
fwd_ret_20d; GATE_ON_NEUTRALIZED still strips size+industry, so these test
size-orthogonal residual value at 20d. Raw yields let the gate neutralize.
"""
from mining import config as cfg
cfg.HORIZON = 20                      # 20-day horizon for this sleeve

SET_NAME = "value_20d"

CANDIDATES = [
    # core value yields (gate neutralizes size+industry -> residual value)
    {"name": "ep", "family": "value", "logic_score": 0.7,
     "expr": "EP", "rationale": "Earnings yield (raw; gate neutralizes size+industry)."},
    {"name": "cfp", "family": "value", "logic_score": 0.7,
     "expr": "CFP", "rationale": "Cash-flow yield."},
    {"name": "sp", "family": "value", "logic_score": 0.6,
     "expr": "SP", "rationale": "Sales yield."},
    {"name": "bp", "family": "value", "logic_score": 0.6,
     "expr": "BP", "rationale": "Book yield (dead at 10d; may work at 20d)."},
    {"name": "value_combo", "family": "value", "logic_score": 0.65,
     "expr": "EP + CFP", "rationale": "Combined earnings + cash-flow yield."},
    {"name": "value_composite", "family": "value", "logic_score": 0.65,
     "expr": "CsRank(EP) + CsRank(CFP) + CsRank(SP)",
     "rationale": "Cross-sectional value composite rank."},
    {"name": "value_agree", "family": "value", "logic_score": 0.6,
     "expr": "CsRank(EP) * CsRank(CFP)",
     "rationale": "Cheap on BOTH earnings and cash-flow yield."},

    # quality from yields
    {"name": "roe_proxy", "family": "quality", "logic_score": 0.65,
     "expr": "EP / BP", "rationale": "EP/BP = E/B = ROE proxy (quality)."},
    {"name": "asset_turnover", "family": "quality", "logic_score": 0.55,
     "expr": "SP / BP", "rationale": "SP/BP = S/B = asset turnover."},
    {"name": "accruals", "family": "quality", "logic_score": 0.6,
     "expr": "CFP / EP", "rationale": "Cash-flow vs earnings (accruals quality)."},
    {"name": "earnings_stability", "family": "quality", "logic_score": 0.55,
     "expr": "-TsStd(EP, 120)", "rationale": "Stable earnings yield = predictable earners."},

    # value re-rating / change
    {"name": "ep_rerate_60", "family": "value_mom", "logic_score": 0.6,
     "expr": "Delta(EP, 60)", "rationale": "Earnings-yield re-rating (quarter)."},
    {"name": "cfp_rerate_120", "family": "value_mom", "logic_score": 0.55,
     "expr": "Delta(CFP, 120)", "rationale": "Cash-flow-yield re-rating (semi-annual)."},

    # valuation inverses / size / contrarian
    {"name": "cheap_book", "family": "value", "logic_score": 0.55,
     "expr": "-PB", "rationale": "Cheap book (inverse PB)."},
    {"name": "cheap_sales", "family": "value", "logic_score": 0.55,
     "expr": "-PS", "rationale": "Cheap sales (inverse PS)."},
    {"name": "size_small", "family": "size", "logic_score": 0.5,
     "expr": "-Log(CMV)", "rationale": "Small-size premium (slower factor; 20d)."},
    {"name": "value_minus_mom", "family": "value", "logic_score": 0.6,
     "expr": "CsRank(EP) - CsRank(TsSum(RET, 120))",
     "rationale": "Contrarian value: cheap and not already run up."},
    {"name": "quality_value", "family": "quality", "logic_score": 0.6,
     "expr": "CsRank(EP / BP) + CsRank(CFP)",
     "rationale": "Quality (ROE) + value (CFP) composite."},
]

assert len(CANDIDATES) == 18, len(CANDIDATES)
