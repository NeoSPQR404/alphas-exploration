# Canonical set — Round 12 (16 candidates) — 2026-07-09.
# Novelty run 2/5: exploit the day-type vein found in run 1 (dip-bought
# days OOS -0.064). Individual factors only, thresholds unchanged.

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
    # ---------------- day-type family expansion (10)
    dict(name="c_capit_freq", expr=f"-TsCount({_CAPIT} > 0.5, 60)", family="daytype",
         rationale="Capitulation days: gapped down AND kept falling intraday.", logic_score=70),
    dict(name="c_daytype_bal", expr=f"-(TsCount({_DIPBUY} > 0.5, 60) - TsCount({_CAPIT} > 0.5, 60))", family="daytype",
         rationale="Dip-bought minus capitulation days: net absorption balance after gap-downs.", logic_score=70),
    dict(name="c_dipbuy_share", expr=f"-(TsCount({_DIPBUY} > 0.5, 60) / (TsCount(({_GAP}) < 0, 60) + 1))", family="daytype",
         rationale="CONVERSION RATE: share of gap-downs that got bought back — absorption efficiency, scale-free.", logic_score=72),
    dict(name="c_fade_share", expr=f"-(TsCount({_FADE} > 0.5, 60) / (TsCount(({_GAP}) > 0, 60) + 1))", family="daytype",
         rationale="Share of gap-ups that faded: failure rate of overnight enthusiasm.", logic_score=71),
    dict(name="c_bigdip_buy", expr=f"-TsCount(((({_GAP}) < -TsStd({_GAP}, 60)) * (({_ID}) > 0)) > 0.5, 60)", family="daytype",
         rationale="Large-gap-down days that got bought: conviction absorption events.", logic_score=70),
    dict(name="c_fade_freq120", expr=f"-TsCount({_FADE} > 0.5, 120)", family="daytype",
         rationale="Gap-and-fade habit at 120d (60d passed S1-S3, OOS 0.024 just under — longer counts stabilized siblings).", logic_score=69),
    dict(name="c_dipbuy_hivol", expr=f"-TsCount(({_DIPBUY} * ({_NVOL} > 1)) > 0.5, 60)", family="daytype",
         rationale="Dip-bought days WITH the crowd present: witnessed absorption.", logic_score=69),
    dict(name="c_dipbuy_mag", expr=f"-TsSum(({_ID}) * {_DIPBUY}, 60)", family="daytype",
         rationale="Magnitude of dip-buying: cumulative intraday recovery on gap-down days.", logic_score=69),
    dict(name="c_post_dipbuy_ret", expr=f"-TsSum(RET * Delay({_DIPBUY}, 1), 60)", family="daytype",
         rationale="Returns on days AFTER dip-bought days: follow-through quality.", logic_score=68),
    dict(name="c_aggr_dipbuy", expr=f"-TsMean(({_AGG}) * {_DIPBUY}, 60)", family="daytype",
         rationale="Closing aggression on dip-bought days: how hard the recovery pushed.", logic_score=68),
    # ---------------- vwap-flavored day-types (2)
    dict(name="c_vwap_recover", expr=f"-TsCount(((({_GAP}) < 0) * (({_AGG}) > 0)) > 0.5, 60)", family="daytype",
         rationale="Gapped down but closed above vwap: strong-form recovery days.", logic_score=68),
    dict(name="c_vwap_fail", expr=f"-TsCount(((({_GAP}) > 0) * (({_AGG}) < 0)) > 0.5, 60)", family="daytype",
         rationale="Gapped up but closed below vwap: strong-form failure days.", logic_score=68),
    # ---------------- near-miss retries (4)
    dict(name="c_aggr_on_gapdn60", expr=f"-TsMean(({_AGG}) * (({_GAP}) < 0), 60)", family="daytype",
         rationale="Aggression on gap-down days at 60d (20d was IC 0.029, just under).", logic_score=67),
    dict(name="c_gap_sign_bal180", expr=f"-Abs(TsMean(Sign({_GAP}), 180))", family="overnight",
         rationale="Gap one-sidedness at 180d (ICIR 0.52 at 120d, IC 0.024 — longer window for the IC bar).", logic_score=67),
    dict(name="c_gap_sign_bal250", expr=f"-Abs(TsMean(Sign({_GAP}), 250))", family="overnight",
         rationale="Annual gap one-sidedness.", logic_score=66),
    dict(name="c_capit_share", expr=f"-(TsCount({_CAPIT} > 0.5, 60) / (TsCount(({_GAP}) < 0, 60) + 1))", family="daytype",
         rationale="Share of gap-downs that kept falling: failure rate of dip demand.", logic_score=68),
]

assert len(CANDIDATES) == 16, len(CANDIDATES)
