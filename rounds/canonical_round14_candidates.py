# Canonical set — Round 14 (12 candidates) — 2026-07-09.
# Novelty run 4/5: per-type magnitudes and textures (magnitude-on-type
# beats count-of-type). Individual only, thresholds unchanged.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_DIPBUY = f"(({_GAP}) < 0) * (({_ID}) > 0)"
_FADE = f"(({_GAP}) > 0) * (({_ID}) < 0)"
_CAPIT = f"(({_GAP}) < 0) * (({_ID}) < 0)"

CANDIDATES = [
    # ---------------- gap depth by type (3)
    dict(name="c_gap_capitmag", expr=f"TsSum(({_GAP}) * {_CAPIT}, 60)", family="daytype",
         rationale="Depth of capitulation gaps: how hard the unbought opens hit (dip version OOS 0.082).", logic_score=70),
    dict(name="c_gap_fademag", expr=f"-TsSum(({_GAP}) * {_FADE}, 60)", family="daytype",
         rationale="Size of the gap-ups that faded: magnitude of failed enthusiasm.", logic_score=68),
    dict(name="c_gap_dipmag120", expr=f"TsSum(({_GAP}) * {_DIPBUY}, 120)", family="daytype",
         rationale="Semi-annual band of the run-3 winner (corr gate arbitrates vs 60d).", logic_score=68),
    # ---------------- range/attention texture on typed days (5)
    dict(name="c_hl_dipbuy", expr=f"-TsMean(({_HL}) * {_DIPBUY}, 60)", family="daytype",
         rationale="Range on dip-bought days: how violent the absorption battle was.", logic_score=69),
    dict(name="c_hl_capit", expr=f"-TsMean(({_HL}) * {_CAPIT}, 60)", family="daytype",
         rationale="Range on capitulation days: orderly vs disorderly declines.", logic_score=68),
    dict(name="c_nvol_dipbuy", expr=f"-TsMean(({_NVOL}) * {_DIPBUY}, 60)", family="daytype",
         rationale="Attention on dip-bought days: crowd size at the absorption.", logic_score=68),
    dict(name="c_id_capitmag", expr=f"TsSum(({_ID}) * {_CAPIT}, 60)", family="daytype",
         rationale="Intraday continuation depth on capitulation days.", logic_score=67),
    dict(name="c_capit_dmg", expr=f"TsSum((({_GAP}) + ({_ID})) * {_CAPIT}, 60)", family="daytype",
         rationale="Total damage on capitulation days: gap + intraday combined.", logic_score=67),
    # ---------------- covariance-magnitude probes (2)
    dict(name="c_gapid_covmag", expr=f"TsSum(({_GAP}) * ({_ID}), 60)", family="overnight",
         rationale="Signed gap×intraday product sum: continuation-minus-fade magnitude (corr version dead; magnitude aggregation untested).", logic_score=66),
    dict(name="c_aggr_capit120", expr=f"-TsMean(({_AGG}) * {_CAPIT}, 120)", family="daytype",
         rationale="Semi-annual aggression-on-capitulation (60d accepted OOS -0.064).", logic_score=66),
    # ---------------- near-miss jitters (2)
    dict(name="c_breakout_vol120", expr=f"-TsCount(((CLOSE >= TsMax(CLOSE, 20)) * ({_NVOL} > 1)) > 0.5, 120)", family="daytype",
         rationale="Witnessed breakouts at 120d (60d IC 0.031/ICIR 0.27, both just under).", logic_score=66),
    dict(name="c_dipbuy_freq20", expr=f"TsCount({_DIPBUY} > 0.5, 20)", family="daytype",
         rationale="Fast dip-bought count (60d is the accepted anchor; monthly band).", logic_score=66),
]

assert len(CANDIDATES) == 12, len(CANDIDATES)
