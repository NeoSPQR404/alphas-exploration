"""value_20d Round 2 — R1 kept one value-level factor (valpha_0001 EP*CFP);
raw yields all S3-collapse into it (value is ~one signal). So mine constructs
DISTINCT from value-level: value momentum / re-rating, value x behavioral
interactions (concentrate value in neglected/calm names), quality-change,
value+size. 20d horizon.
"""
from mining import config as cfg
cfg.HORIZON = 20

SET_NAME = "value_20d"

CANDIDATES = [
    # value x behavioral interactions (concentrate value where it works)
    {"name": "value_x_lowturn", "family": "value_interact", "logic_score": 0.6,
     "expr": "(CsRank(EP) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
     "rationale": "Cheap AND neglected (low attention) — value works in ignored names."},
    {"name": "value_x_calm", "family": "value_interact", "logic_score": 0.55,
     "expr": "(CsRank(EP) - 0.5) * (CsRank(-TsCount(AMP > 2 * TsMean(AMP, 60), 120)) - 0.5)",
     "rationale": "Cheap AND event-rare (boring value)."},
    {"name": "value_x_stability", "family": "value_interact", "logic_score": 0.55,
     "expr": "(CsRank(CFP) - 0.5) * (CsRank(-TsStd(AMP, 120) / TsMed(AMP, 120)) - 0.5)",
     "rationale": "Cheap AND stable-range."},

    # value / quality change (distinct from value level)
    {"name": "roe_change_60", "family": "quality_mom", "logic_score": 0.6,
     "expr": "Delta(EP / BP, 60)", "rationale": "Improving ROE (quality momentum)."},
    {"name": "value_rerate_indneut_60", "family": "value_mom", "logic_score": 0.55,
     "expr": "Delta(CsIndNeutralize(EP, IND), 60)",
     "rationale": "Industry-neutral earnings-yield re-rating."},
    {"name": "ep_rerate_accel", "family": "value_mom", "logic_score": 0.5,
     "expr": "Delta(EP, 20) - Delta(EP, 60)",
     "rationale": "Value re-rating acceleration (short minus long change)."},
    {"name": "sales_growth_cheap", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(SP) + CsRank(Delta(SP, 120))",
     "rationale": "Cheap sales AND growing sales."},

    # value quality composites (distinct blends)
    {"name": "quality_x_value", "family": "quality", "logic_score": 0.6,
     "expr": "CsRank(EP / BP) * CsRank(CFP)",
     "rationale": "High ROE AND high cash-flow yield."},
    {"name": "value_disagree", "family": "quality", "logic_score": 0.5,
     "expr": "CsRank(CFP) - CsRank(EP)",
     "rationale": "Cash-flow cheap but earnings not = conservative-accruals value."},

    # value stability / smoothing
    {"name": "value_stable_rank", "family": "value", "logic_score": 0.5,
     "expr": "-TsStd(CsRank(EP), 120)",
     "rationale": "Persistently-cheap (stable value rank)."},
    {"name": "value_smooth_z", "family": "value", "logic_score": 0.5,
     "expr": "CsZscore(TsMean(EP, 60))",
     "rationale": "Smoothed standardized earnings yield."},

    # value + size / value + contrarian (different mom band)
    {"name": "cheap_small", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(EP) - CsRank(Log(CMV))",
     "rationale": "Cheap AND small (value + size)."},
    {"name": "value_minus_shortmom", "family": "value", "logic_score": 0.55,
     "expr": "CsRank(EP) - CsRank(TsSum(RET, 20))",
     "rationale": "Cheap and NOT run up over the last month (contrarian value, short band)."},
]

assert len(CANDIDATES) == 13, len(CANDIDATES)
