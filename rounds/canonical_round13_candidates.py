# Canonical set — Round 13 (15 candidates) — 2026-07-09.
# Novelty run 3/5: day-types deeper (volume-conditioned types, bar
# patterns, aggression-on-type variants). Individual only, thresholds
# unchanged.

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
    # ---------------- volume-conditioned day-types (5)
    dict(name="c_churn_freq", expr=f"-TsCount((({_NVOL} > 2) * (Abs(RET) < 0.005)) > 0.5, 60)", family="daytype",
         rationale="Churn days: heavy volume, no net move — absorption/distribution battles (volume without progress).", logic_score=72),
    dict(name="c_churn_freq120", expr=f"-TsCount((({_NVOL} > 2) * (Abs(RET) < 0.005)) > 0.5, 120)", family="daytype",
         rationale="Semi-annual churn habit.", logic_score=70),
    dict(name="c_accum_freq", expr=f"-TsCount((({_NVOL} > 1) * (({_ID}) > 0) * (({_AGG}) > 0)) > 0.5, 60)", family="daytype",
         rationale="Accumulation days: heavy volume, up intraday, strong close — textbook demand days.", logic_score=70),
    dict(name="c_quiet_up_freq", expr=f"TsCount((({_NVOL} < 0.5) * (RET > 0)) > 0.5, 60)", family="daytype",
         rationale="Quiet up-days: drift without attention — stealth strength.", logic_score=69),
    dict(name="c_breakout_vol", expr=f"-TsCount(((CLOSE >= TsMax(CLOSE, 20)) * ({_NVOL} > 1)) > 0.5, 60)", family="daytype",
         rationale="New-high days on heavy volume: witnessed breakouts (unconditioned high-making died; conditioning may change it).", logic_score=68),
    # ---------------- bar-pattern counts (3)
    dict(name="c_inside_freq", expr="-TsCount(((HIGH < Delay(HIGH, 1)) * (LOW > Delay(LOW, 1))) > 0.5, 60)", family="daytype",
         rationale="Inside days: range compression events — coiling frequency.", logic_score=69),
    dict(name="c_outside_freq", expr="-TsCount(((HIGH > Delay(HIGH, 1)) * (LOW < Delay(LOW, 1))) > 0.5, 60)", family="daytype",
         rationale="Outside days: engulfing expansion — two-sided violence.", logic_score=69),
    dict(name="c_inside_freq120", expr="-TsCount(((HIGH < Delay(HIGH, 1)) * (LOW > Delay(LOW, 1))) > 0.5, 120)", family="daytype",
         rationale="Semi-annual coiling habit.", logic_score=67),
    # ---------------- aggression / magnitude on other types (4)
    dict(name="c_aggr_capit", expr=f"-TsMean(({_AGG}) * {_CAPIT}, 60)", family="daytype",
         rationale="Closing aggression on capitulation days (the dip-buy version just accepted at OOS 0.068).", logic_score=68),
    dict(name="c_aggr_fade", expr=f"-TsMean(({_AGG}) * {_FADE}, 60)", family="daytype",
         rationale="Closing aggression on gap-and-fade days.", logic_score=68),
    dict(name="c_aggr_dipbuy120", expr=f"-TsMean(({_AGG}) * {_DIPBUY}, 120)", family="daytype",
         rationale="Semi-annual band of the accepted aggr_dipbuy.", logic_score=67),
    dict(name="c_fade_mag", expr=f"-TsSum(({_ID}) * {_FADE}, 60)", family="daytype",
         rationale="Magnitude of fading: cumulative intraday selloff on gap-up days.", logic_score=67),
    # ---------------- near-miss jitters (3)
    dict(name="c_bigdip_buy120", expr=f"-TsCount(((({_GAP}) < -TsStd({_GAP}, 60)) * (({_ID}) > 0)) > 0.5, 120)", family="daytype",
         rationale="Large-dip absorption at 120d (60d was 0.027/0.51 — just under the IC bar).", logic_score=67),
    dict(name="c_gap_dipmag", expr=f"TsSum(({_GAP}) * {_DIPBUY}, 60)", family="daytype",
         rationale="How deep were the bought dips: gap magnitude on dip-bought days.", logic_score=66),
    dict(name="c_dist_days120", expr=f"-TsCount((({_NVOL} > 1) * (RET < 0)) > 0.5, 120)", family="daytype",
         rationale="Distribution days (heavy-volume declines) at 120d — the down-side attention count that failed at 60d in main.", logic_score=66),
]

assert len(CANDIDATES) == 15, len(CANDIDATES)
