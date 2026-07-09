# Canonical set — Round 17 (40 candidates) — 2026-07-09.
# Extended campaign 2/5: exploit the three classes minted in R16 —
# vwap-pin/stalemate (OOS -0.070), true gaps, volume-at-extremes —
# plus near-miss jitters. Individual only, thresholds unchanged.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_TG_UP = "(OPEN > Delay(HIGH, 1))"
_TG_DN = "(OPEN < Delay(LOW, 1))"
_PIN = f"(Abs({_AGG}) < 0.002)"

CANDIDATES = [
    # ---------------- vwap-pin / stalemate family (10)
    dict(name="c_pin_freq20", expr=f"-TsCount({_PIN} > 0.5, 20)", family="stalemate",
         rationale="Fast pin count (60d version OOS -0.070).", logic_score=69),
    dict(name="c_pin_freq120", expr=f"-TsCount({_PIN} > 0.5, 120)", family="stalemate",
         rationale="Semi-annual stalemate habit.", logic_score=69),
    dict(name="c_pin_freq250", expr=f"-TsCount({_PIN} > 0.5, 250)", family="stalemate",
         rationale="Annual stalemate habit.", logic_score=68),
    dict(name="c_contested_pin", expr=f"-TsCount(({_PIN} * ({_NVOL} > 1)) > 0.5, 60)", family="stalemate",
         rationale="Pins on heavy volume: CONTESTED stalemates (the battle nobody won).", logic_score=71),
    dict(name="c_lazy_pin", expr=f"-TsCount(({_PIN} * ({_NVOL} < 1)) > 0.5, 60)", family="stalemate",
         rationale="Pins on light volume: nobody showed up.", logic_score=68),
    dict(name="c_pin_battle_mag", expr=f"-TsSum(({_HL}) * {_PIN}, 60)", family="stalemate",
         rationale="Range consumed on pin days: how big the stalemated battles were.", logic_score=69),
    dict(name="c_wide_pin", expr=f"-TsCount(({_PIN} * (({_HL}) > TsMed({_HL}, 60))) > 0.5, 60)", family="stalemate",
         rationale="Wide-range pins: violent battles ending flat.", logic_score=69),
    dict(name="c_pin_after_run", expr=f"-TsCount(({_PIN} * (Abs(TsSum(RET, 5)) > TsStd(RET, 60) * 3)) > 0.5, 60)", family="stalemate",
         rationale="Pins right after big weekly runs: exhaustion stalls.", logic_score=68),
    dict(name="c_gap_pin", expr=f"-TsCount(((Abs({_GAP}) > TsStd({_GAP}, 60)) * {_PIN}) > 0.5, 60)", family="stalemate",
         rationale="Big gap, pinned close: overnight conviction neutralized by day.", logic_score=68),
    dict(name="c_nvol_pin", expr=f"-TsMean(({_NVOL}) * {_PIN}, 60)", family="stalemate",
         rationale="Attention on pin days: crowd size at stalemates.", logic_score=68),
    # ---------------- true-gap family (10)
    dict(name="c_truegap_dn120", expr=f"-TsCount({_TG_DN} > 0.5, 120)", family="truegap",
         rationale="Semi-annual range-breaking gap-down habit (60d accepted 0.044).", logic_score=68),
    dict(name="c_island_up120", expr=f"-TsCount(({_TG_UP} * (LOW > Delay(HIGH, 1))) > 0.5, 120)", family="truegap",
         rationale="Semi-annual unfilled gap-up habit (60d accepted 0.044).", logic_score=68),
    dict(name="c_island_dn_freq", expr=f"TsCount(({_TG_DN} * (HIGH < Delay(LOW, 1))) > 0.5, 60)", family="truegap",
         rationale="Unfilled gap-downs: island weakness.", logic_score=68),
    dict(name="c_tg_dn_bought", expr=f"-TsCount(({_TG_DN} * (({_ID}) > 0)) > 0.5, 60)", family="truegap",
         rationale="Range-breaking gap-downs that got bought: extreme absorption events.", logic_score=69),
    dict(name="c_tg_up_faded", expr=f"-TsCount(({_TG_UP} * (({_ID}) < 0)) > 0.5, 60)", family="truegap",
         rationale="Range-breaking gap-ups that faded.", logic_score=67),
    dict(name="c_nvol_truegap", expr=f"-TsMean(({_NVOL}) * ({_TG_UP} + {_TG_DN}), 60)", family="truegap",
         rationale="Attention on range-breaking days.", logic_score=67),
    dict(name="c_aggr_truegap_dn", expr=f"-TsMean(({_AGG}) * {_TG_DN}, 60)", family="truegap",
         rationale="Closing aggression on range-breaking gap-downs.", logic_score=67),
    dict(name="c_tg_dn_mag_norm", expr=f"TsSum((OPEN / Delay(LOW, 1) - 1) * {_TG_DN}, 60) / (TsStd({_GAP}, 60) + 0.001)", family="truegap",
         rationale="Undershoot depth in own-gap-vol units (raw version locked at 0.73 vs mingap60).", logic_score=67),
    dict(name="c_island_mag", expr=f"TsSum((LOW / Delay(HIGH, 1) - 1) * ({_TG_UP} * (LOW > Delay(HIGH, 1))), 60)", family="truegap",
         rationale="Cumulative island-gap clearance: how far above prior range the unfilled gaps stayed.", logic_score=66),
    dict(name="c_truegap_dn250", expr=f"-TsCount({_TG_DN} > 0.5, 250)", family="truegap",
         rationale="Annual range-breaking gap-down habit.", logic_score=66),
    # ---------------- volume-at-extremes family (8)
    dict(name="c_vol_at_high60", expr=f"-TsMean(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 60)), 120)", family="vol_at_ext",
         rationale="Attention at 60d highs over semi-annual window (20d-anchor version deduped into asym; different anchor).", logic_score=68),
    dict(name="c_vol_at_low60", expr=f"-TsMean(({_NVOL}) * (CLOSE <= TsMin(CLOSE, 60)), 120)", family="vol_at_ext",
         rationale="Attention at 60d lows (accepted at 20d anchor: -0.041).", logic_score=68),
    dict(name="c_vol_ext_asym120", expr=f"-(TsMean(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 20)), 120) - TsMean(({_NVOL}) * (CLOSE <= TsMin(CLOSE, 20)), 120))",
         family="vol_at_ext", rationale="Semi-annual volume-at-extremes asymmetry (60d accepted 0.040).", logic_score=68),
    dict(name="c_hl_at_low", expr=f"-TsMean(({_HL}) * (CLOSE <= TsMin(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Range on low-making days: panicky vs orderly lows.", logic_score=67),
    dict(name="c_aggr_at_high", expr=f"-TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Closing aggression on high-making days: chased vs faded highs.", logic_score=67),
    dict(name="c_gap_at_high", expr=f"-TsMean(({_GAP}) * (CLOSE >= TsMax(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Gap contribution on high-making days: overnight-driven highs.", logic_score=66),
    dict(name="c_vol_at_gapext", expr=f"-TsMean(({_NVOL}) * (Abs({_GAP}) > 2 * TsStd({_GAP}, 60)), 120)", family="vol_at_ext",
         rationale="Attention on extreme-gap days.", logic_score=66),
    dict(name="c_id_at_low", expr=f"-TsMean(({_ID}) * (CLOSE <= TsMin(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Intraday action on low-making days: fought vs surrendered lows.", logic_score=66),
    # ---------------- near-miss jitters (8)
    dict(name="c_ma_cross120", expr="-TsCount(Abs(CLOSE / TsMean(CLOSE, 20) - 1) < 0.01, 120)", family="whipsaw",
         rationale="MA-pinned days at 120d (60d was -0.034/-0.29, just under ICIR).", logic_score=66),
    dict(name="c_ma_pin_tight", expr="-TsCount(Abs(CLOSE / TsMean(CLOSE, 20) - 1) < 0.005, 60)", family="whipsaw",
         rationale="Tighter MA pin threshold.", logic_score=66),
    dict(name="c_near_low_occ120", expr="TsCount(CLOSE < TsMin(CLOSE, 60) * 1.05, 120)", family="occupancy",
         rationale="Low-zone occupancy at 120d (60d was 0.030/0.27).", logic_score=66),
    dict(name="c_vol_accel60", expr="-(TsMean(VOLUME, 20) / (Delay(TsMean(VOLUME, 20), 20) + 1))", family="acceleration",
         rationale="Attention acceleration month-over-month (fortnight version 0.028/0.33).", logic_score=66),
    dict(name="c_range_accel60", expr=f"-(TsMean({_HL}, 20) / Delay(TsMean({_HL}, 20), 20))", family="acceleration",
         rationale="Range acceleration month-over-month (0.027/0.34 at fortnight).", logic_score=66),
    dict(name="c_truegap_up120", expr=f"-TsCount({_TG_UP} > 0.5, 120)", family="truegap",
         rationale="Gap-up habit at 120d (60d was 0.019/0.31 — under IC but viable ICIR).", logic_score=65),
    dict(name="c_roundtrip120", expr=f"-TsCount(((Abs({_GAP}) > TsStd({_GAP}, 60)) * (Abs(RET) < 0.005)) > 0.5, 120)", family="roundtrip",
         rationale="Round-trip days at 120d (60d was -0.026/-0.32).", logic_score=65),
    dict(name="c_min_week_run120", expr="-TsMin(TsSum(RET, 5), 120)", family="run_extreme",
         rationale="Worst week over 120d (60d was -0.043/-0.27, ICIR just under).", logic_score=65),
    # ---------------- wildcards (4)
    dict(name="c_pin_asym", expr=f"-(TsCount(({_PIN} * (({_GAP}) > 0)) > 0.5, 60) - TsCount(({_PIN} * (({_GAP}) < 0)) > 0.5, 60))",
         family="stalemate", rationale="Pinned closes after gap-ups minus after gap-downs: which side keeps getting neutralized.", logic_score=66),
    dict(name="c_ext_day_bal", expr="-(TsCount(CLOSE >= TsMax(CLOSE, 20), 60) - TsCount(CLOSE <= TsMin(CLOSE, 20), 60))",
         family="occupancy", rationale="High-making minus low-making day balance (making-days, not zone occupancy).", logic_score=66),
    dict(name="c_vol_med_at_ext", expr=f"-TsMed(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 20)) + 0 * CLOSE, 120)", family="vol_at_ext",
         rationale="Median (robust) attention at highs.", logic_score=64),
    dict(name="c_quiet_after_gap", expr=f"-TsCount(((Abs(Delay({_GAP}, 1)) > 2 * TsStd({_GAP}, 60)) * ({_NVOL} < 1)) > 0.5, 60)",
         family="daytype", rationale="Quiet days right after big gaps: unfollowed shocks.", logic_score=65),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
