# Canonical set — Round 16 (40 candidates) — 2026-07-09.
# Extended novelty campaign 1/5 at 40/round. Strategy: parallel
# class-hunting — 9 untouched structural classes, 3-6 variants each.
# Individual factors only, thresholds unchanged.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_TG_UP = "(OPEN > Delay(HIGH, 1))"      # true gap: open beyond prior range
_TG_DN = "(OPEN < Delay(LOW, 1))"

CANDIDATES = [
    # ---------------- A. true-gap (range-breaking) events (6)
    dict(name="c_truegap_up_freq", expr=f"-TsCount({_TG_UP} > 0.5, 60)", family="truegap",
         rationale="Range-breaking gap-ups: opens beyond yesterday's HIGH (stronger event than close-relative gaps).", logic_score=70),
    dict(name="c_truegap_dn_freq", expr=f"-TsCount({_TG_DN} > 0.5, 60)", family="truegap",
         rationale="Range-breaking gap-downs.", logic_score=69),
    dict(name="c_truegap_up_mag", expr=f"TsSum((OPEN / Delay(HIGH, 1) - 1) * {_TG_UP}, 60)", family="truegap",
         rationale="Cumulative overshoot beyond prior highs.", logic_score=69),
    dict(name="c_truegap_dn_mag", expr=f"TsSum((OPEN / Delay(LOW, 1) - 1) * {_TG_DN}, 60)", family="truegap",
         rationale="Cumulative undershoot beyond prior lows.", logic_score=69),
    dict(name="c_island_up_freq", expr=f"-TsCount(({_TG_UP} * (LOW > Delay(HIGH, 1))) > 0.5, 60)", family="truegap",
         rationale="Unfilled gap-ups: never traded back into prior range all day — island strength.", logic_score=68),
    dict(name="c_truegap_bal", expr=f"-(TsCount({_TG_UP} > 0.5, 60) - TsCount({_TG_DN} > 0.5, 60))", family="truegap",
         rationale="Net range-breaking direction.", logic_score=67),
    # ---------------- B. volume-at-extremes asymmetry (5)
    dict(name="c_vol_at_high", expr=f"-TsMean(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Attention on days making 20d highs: crowd at the top (Wyckoff distribution).", logic_score=71),
    dict(name="c_vol_at_low", expr=f"-TsMean(({_NVOL}) * (CLOSE <= TsMin(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Attention on days making 20d lows: crowd at the bottom.", logic_score=70),
    dict(name="c_vol_ext_asym", expr=f"-(TsMean(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 20)), 60) - TsMean(({_NVOL}) * (CLOSE <= TsMin(CLOSE, 20)), 60))",
         family="vol_at_ext", rationale="Volume-at-highs minus volume-at-lows: where the crowd trades.", logic_score=71),
    dict(name="c_range_at_high", expr=f"-TsMean(({_HL}) * (CLOSE >= TsMax(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Range on high-making days: churny vs clean tops.", logic_score=68),
    dict(name="c_aggr_at_low", expr=f"-TsMean(({_AGG}) * (CLOSE <= TsMin(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Closing aggression on low-making days: defended vs abandoned lows.", logic_score=68),
    # ---------------- C. zone occupancy (4)
    dict(name="c_near_high_occ", expr="-TsCount(CLOSE > TsMax(CLOSE, 60) * 0.95, 60)", family="occupancy",
         rationale="Days spent within 5% of the 60d high: time-in-zone, not distance (anchors dead, occupancy untested).", logic_score=69),
    dict(name="c_near_low_occ", expr="TsCount(CLOSE < TsMin(CLOSE, 60) * 1.05, 60)", family="occupancy",
         rationale="Days spent within 5% of the 60d low.", logic_score=68),
    dict(name="c_occ_bal", expr="-(TsCount(CLOSE > TsMax(CLOSE, 60) * 0.95, 60) - TsCount(CLOSE < TsMin(CLOSE, 60) * 1.05, 60))",
         family="occupancy", rationale="Net zone occupancy.", logic_score=67),
    dict(name="c_mid_occ", expr="-TsCount(Abs(CLOSE / TsMed(CLOSE, 60) - 1) < 0.02, 60)", family="occupancy",
         rationale="Days pinned near own median: range-bound-ness.", logic_score=67),
    # ---------------- D. peak asynchrony (4)
    dict(name="c_pv_peak_async", expr="-Abs(HighDay(CLOSE, 60) - HighDay(VOLUME, 60))", family="asynchrony",
         rationale="Price-peak vs volume-peak time distance: synchronized peaks = blowoff; diverged = rotation.", logic_score=69),
    dict(name="c_pv_peak_lead", expr="HighDay(VOLUME, 60) - HighDay(CLOSE, 60)", family="asynchrony",
         rationale="Does volume peak before price (signed lead): early-crowd vs late-crowd names.", logic_score=69),
    dict(name="c_ph_pl_dist", expr="-Abs(HighDay(CLOSE, 60) - LowDay(CLOSE, 60))", family="asynchrony",
         rationale="High-to-low time distance: V-shaped vs drawn-out ranges.", logic_score=66),
    dict(name="c_prange_peak_async", expr=f"-Abs(HighDay({_HL}, 60) - HighDay(VOLUME, 60))", family="asynchrony",
         rationale="Range-peak vs volume-peak distance.", logic_score=66),
    # ---------------- E. MA-crossing / whipsaw (4)
    dict(name="c_ma_cross_freq", expr="-TsCount(Abs(CLOSE / TsMean(CLOSE, 20) - 1) < 0.01, 60)", family="whipsaw",
         rationale="Days pinned to own 20d MA: indecision persistence.", logic_score=67),
    dict(name="c_ma_above_dur", expr="-TsCount(CLOSE > TsMean(CLOSE, 20), 60)", family="whipsaw",
         rationale="Time above 20d MA (duration form of trend; above-median version failed — MA version differs by weighting).", logic_score=66),
    dict(name="c_whipsaw_freq", expr="-TsCount(Abs(RET) > 2 * Abs(TsMean(RET, 20)) * 10, 60)", family="whipsaw",
         rationale="Days whose move dwarfs the trend: noise dominance (scaled).", logic_score=64),
    dict(name="c_vwap_pin_freq", expr=f"-TsCount(Abs({_AGG}) < 0.002, 60)", family="whipsaw",
         rationale="Days closing pinned to vwap: battle stalemates.", logic_score=66),
    # ---------------- F. round-trip days (3)
    dict(name="c_roundtrip_freq", expr=f"-TsCount(((Abs({_GAP}) > TsStd({_GAP}, 60)) * (Abs(RET) < 0.005)) > 0.5, 60)", family="roundtrip",
         rationale="Opened far, closed flat: full round-trip days — max disagreement.", logic_score=68),
    dict(name="c_roundtrip_mag", expr=f"-TsSum(Abs({_GAP}) * (Abs(RET) < 0.005), 60)", family="roundtrip",
         rationale="Cumulative gap distance surrendered on flat-close days.", logic_score=67),
    dict(name="c_intra_roundtrip", expr=f"-TsCount(((({_HL}) > 2 * TsMed({_HL}, 60)) * (Abs(RET) < 0.005)) > 0.5, 60)", family="roundtrip",
         rationale="Huge range, flat close: intraday round trips.", logic_score=67),
    # ---------------- G. weekly-run extremes (4)
    dict(name="c_max_week_runup", expr="-TsMax(TsSum(RET, 5), 60)", family="run_extreme",
         rationale="Best 5-day run in the quarter: week-scale lottery (day-scale MAX is resident; week scale untested).", logic_score=68),
    dict(name="c_min_week_run", expr="-TsMin(TsSum(RET, 5), 60)", family="run_extreme",
         rationale="Worst 5-day run: week-scale crash.", logic_score=67),
    dict(name="c_max_week_id", expr=f"-TsMax(TsSum({_ID}, 5), 60)", family="run_extreme",
         rationale="Best intraday-leg week.", logic_score=66),
    dict(name="c_week_run_asym", expr="-(TsMax(TsSum(RET, 5), 60) + TsMin(TsSum(RET, 5), 60))", family="run_extreme",
         rationale="Run asymmetry: best week + worst week (midrange of runs).", logic_score=66),
    # ---------------- H. trend-break / acceleration (4)
    dict(name="c_rev_accel", expr=f"-(TsSum({_ID}, 10) - Delay(TsSum({_ID}, 10), 10))", family="acceleration",
         rationale="Intraday-drift acceleration: this fortnight vs last.", logic_score=66),
    dict(name="c_gap_accel", expr=f"(TsSum({_GAP}, 10) - Delay(TsSum({_GAP}, 10), 10))", family="acceleration",
         rationale="Overnight-drift acceleration.", logic_score=66),
    dict(name="c_vol_accel", expr="-(TsMean(VOLUME, 10) / (Delay(TsMean(VOLUME, 10), 10) + 1))", family="acceleration",
         rationale="Attention acceleration: fortnight-over-fortnight volume ratio.", logic_score=66),
    dict(name="c_range_accel", expr=f"-(TsMean({_HL}, 10) / Delay(TsMean({_HL}, 10), 10))", family="acceleration",
         rationale="Range-regime acceleration.", logic_score=66),
    # ---------------- I. triple-condition day-types (6)
    dict(name="c_capitrev_freq", expr=f"TsCount(((RET < -2 * TsStd(RET, 60)) * (({_AGG}) > 0)) > 0.5, 120)", family="daytype",
         rationale="Crash days that closed above vwap: absorbed crashes (capitulation-reversal).", logic_score=69),
    dict(name="c_blowoff_freq", expr=f"-TsCount(((RET > 2 * TsStd(RET, 60)) * ({_NVOL} > 2)) > 0.5, 120)", family="daytype",
         rationale="Huge up-days on huge volume: blowoff events.", logic_score=68),
    dict(name="c_silent_crash", expr=f"TsCount(((RET < -2 * TsStd(RET, 60)) * ({_NVOL} < 1)) > 0.5, 120)", family="daytype",
         rationale="Crashes without volume: air pockets (no seller conviction).", logic_score=68),
    dict(name="c_dip_hl_buy", expr=f"-TsCount(((({_GAP}) < 0) * (({_ID}) > 0) * (({_HL}) > TsMed({_HL}, 60))) > 0.5, 60)",
         family="daytype", rationale="Dip-bought days with wide range: violent absorption battles.", logic_score=67),
    dict(name="c_quiet_capit", expr=f"TsCount((((({_GAP}) < 0) * (({_ID}) < 0)) * ({_NVOL} < 1)) > 0.5, 60)", family="daytype",
         rationale="Capitulations without volume: orderly abandonment.", logic_score=67),
    dict(name="c_heavy_dipbuy_mag", expr=f"TsSum(({_GAP}) * ((({_GAP}) < 0) * (({_ID}) > 0) * ({_NVOL} > 1)), 60)", family="daytype",
         rationale="Depth of bought dips on heavy volume: witnessed absorption depth.", logic_score=67),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
