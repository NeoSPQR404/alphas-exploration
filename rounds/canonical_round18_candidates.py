# Canonical set — Round 18 (40 candidates) — 2026-07-09.
# Extended campaign 3/5: systematic threshold/window jitter of every
# ICIR-viable near-miss (the R17 revival lesson), plus remaining
# at-event textures and acceleration variants. Individual only,
# thresholds unchanged.

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
    # ---------------- near-miss jitters: window (10)
    dict(name="c_island_up250", expr=f"-TsCount(({_TG_UP} * (LOW > Delay(HIGH, 1))) > 0.5, 250)", family="truegap",
         rationale="Annual island habit (120d was 0.028/0.39 — ICIR-viable, IC under).", logic_score=67),
    dict(name="c_ext_day_bal120", expr="-(TsCount(CLOSE >= TsMax(CLOSE, 20), 120) - TsCount(CLOSE <= TsMin(CLOSE, 20), 120))",
         family="occupancy", rationale="High-making minus low-making days at 120d (60d was 0.029/0.24).", logic_score=66),
    dict(name="c_aggr_tgdn120", expr=f"-TsMean(({_AGG}) * {_TG_DN}, 120)", family="truegap",
         rationale="Aggression on range-breaking gap-downs at 120d (60d was 0.019/0.31).", logic_score=66),
    dict(name="c_unfollowed_shock120", expr=f"-TsCount(((Abs(Delay({_GAP}, 1)) > 2 * TsStd({_GAP}, 60)) * ({_NVOL} < 1)) > 0.5, 120)",
         family="daytype", rationale="Quiet days after big gaps at 120d (60d was -0.014/-0.36 — strong ICIR, IC under).", logic_score=67),
    dict(name="c_min_fortnight_run", expr="-TsMin(TsSum(RET, 10), 120)", family="run_extreme",
         rationale="Worst fortnight over 120d (weekly runs ICIR-stuck ~0.27; longer run length).", logic_score=66),
    dict(name="c_max_fortnight_run", expr="-TsMax(TsSum(RET, 10), 120)", family="run_extreme",
         rationale="Best fortnight over 120d.", logic_score=66),
    dict(name="c_vol_at_high10", expr=f"-TsMean(({_NVOL}) * (CLOSE >= TsMax(CLOSE, 10)), 60)", family="vol_at_ext",
         rationale="Attention at 10d highs (60d-anchor version was 0.028/0.25; faster anchor).", logic_score=66),
    dict(name="c_roundtrip_wide", expr=f"-TsCount(((Abs({_GAP}) > TsStd({_GAP}, 60)) * (Abs(RET) < 0.01)) > 0.5, 60)", family="roundtrip",
         rationale="Round-trips with looser flat threshold (0.005->0.01; was -0.026/-0.32).", logic_score=66),
    dict(name="c_near_low_occ3", expr="TsCount(CLOSE < TsMin(CLOSE, 60) * 1.03, 60)", family="occupancy",
         rationale="Tighter low-zone occupancy (5%->3%; was 0.030/0.27).", logic_score=66),
    dict(name="c_ma_band_occ", expr="-TsCount(Abs(CLOSE / TsMean(CLOSE, 20) - 1) < 0.02, 60)", family="whipsaw",
         rationale="Wider MA band (0.01->0.02): band occupancy rather than pinning.", logic_score=65),
    # ---------------- at-event textures (10)
    dict(name="c_aggr_ext_asym", expr=f"-(TsMean(({_AGG}) * (CLOSE >= TsMax(CLOSE, 20)), 60) - TsMean(({_AGG}) * (CLOSE <= TsMin(CLOSE, 20)), 60))",
         family="vol_at_ext", rationale="Aggression at highs minus at lows (highs side accepted 0.053; the spread).", logic_score=68),
    dict(name="c_nvol_at_best", expr=f"-TsMean(({_NVOL}) * (RET >= TsMax(RET, 20)), 60)", family="vol_at_ext",
         rationale="Crowd on the best day of the month: witnessed lottery.", logic_score=67),
    dict(name="c_nvol_at_worst", expr=f"-TsMean(({_NVOL}) * (RET <= TsMin(RET, 20)), 60)", family="vol_at_ext",
         rationale="Crowd on the worst day: witnessed crash.", logic_score=67),
    dict(name="c_hl_at_best", expr=f"-TsMean(({_HL}) * (RET >= TsMax(RET, 20)), 60)", family="vol_at_ext",
         rationale="Range on the best day: clean vs churny rallies.", logic_score=66),
    dict(name="c_aggr_at_worst", expr=f"-TsMean(({_AGG}) * (RET <= TsMin(RET, 20)), 60)", family="vol_at_ext",
         rationale="Closing aggression on the worst day: defended crashes.", logic_score=67),
    dict(name="c_gap_after_best", expr=f"-TsMean(({_GAP}) * (Delay(RET, 1) >= Delay(TsMax(RET, 20), 1)), 60)", family="vol_at_ext",
         rationale="Next-morning gap after the best day: overnight follow-through.", logic_score=66),
    dict(name="c_pin_at_ext", expr=f"-TsCount(({_PIN} * ((CLOSE >= TsMax(CLOSE, 20)) + (CLOSE <= TsMin(CLOSE, 20)))) > 0.5, 120)",
         family="stalemate", rationale="Stalemates AT price extremes: battles at the edge.", logic_score=67),
    dict(name="c_id_at_high", expr=f"-TsMean(({_ID}) * (CLOSE >= TsMax(CLOSE, 20)), 60)", family="vol_at_ext",
         rationale="Intraday leg on high-making days: gapped-to vs traded-to highs.", logic_score=66),
    dict(name="c_truegap_at_ext", expr=f"-TsCount((({_TG_UP} + {_TG_DN}) * ((CLOSE >= TsMax(CLOSE, 20)) + (CLOSE <= TsMin(CLOSE, 20)))) > 0.5, 120)",
         family="truegap", rationale="Range-breaking gaps that landed at monthly extremes.", logic_score=66),
    dict(name="c_zeroret_at_low", expr="TsCount(((Abs(RET) < 0.001) * (CLOSE <= TsMin(CLOSE, 20) * 1.03)) > 0.5, 120)",
         family="occupancy", rationale="Frozen days near lows: abandoned names.", logic_score=66),
    # ---------------- acceleration family (6)
    dict(name="c_volat_accel", expr="-(TsStd(RET, 20) / (Delay(TsStd(RET, 20), 20) + 0.0001))", family="acceleration",
         rationale="Volatility acceleration month-over-month (attention version accepted 0.042; lagged ratio differs from concurrent vol-term).", logic_score=67),
    dict(name="c_hl_accel120", expr=f"-(TsMean({_HL}, 20) / Delay(TsMean({_HL}, 20), 40))", family="acceleration",
         rationale="Range acceleration with a 2-month lag.", logic_score=66),
    dict(name="c_amt_accel", expr="-(TsMean(AMOUNT, 20) / (Delay(TsMean(AMOUNT, 20), 20) + 1))", family="acceleration",
         rationale="Dollar-attention acceleration (volume version accepted; dollar may differ via price drift).", logic_score=65),
    dict(name="c_vol_accel_q", expr="-(TsMean(VOLUME, 60) / (Delay(TsMean(VOLUME, 60), 60) + 1))", family="acceleration",
         rationale="Quarterly attention acceleration.", logic_score=66),
    dict(name="c_gapvol_accel", expr=f"-(TsStd({_GAP}, 20) / (Delay(TsStd({_GAP}, 20), 20) + 0.0001))", family="acceleration",
         rationale="Overnight-risk acceleration.", logic_score=66),
    dict(name="c_pin_accel", expr=f"-(TsCount({_PIN} > 0.5, 20) - Delay(TsCount({_PIN} > 0.5, 20), 20))", family="acceleration",
         rationale="Stalemate-frequency acceleration.", logic_score=65),
    # ---------------- pin/doji micro-variants (5)
    dict(name="c_id_pin_freq", expr=f"-TsCount(Abs({_ID}) < 0.002, 60)", family="stalemate",
         rationale="Open-to-close pins (exact dojis): intraday stalemates (vwap version OOS -0.070; open-anchored differs).", logic_score=67),
    dict(name="c_both_pin", expr=f"-TsCount(({_PIN} * (Abs({_ID}) < 0.002)) > 0.5, 60)", family="stalemate",
         rationale="Pinned to BOTH vwap and open: total stalemate.", logic_score=66),
    dict(name="c_pin_tight", expr=f"-TsCount(Abs({_AGG}) < 0.001, 60)", family="stalemate",
         rationale="Tighter vwap pin (0.002->0.001).", logic_score=65),
    dict(name="c_pin_loose", expr=f"-TsCount(Abs({_AGG}) < 0.004, 60)", family="stalemate",
         rationale="Looser vwap pin (0.002->0.004).", logic_score=65),
    dict(name="c_aggr_flip_freq", expr=f"-TsCount(Sign({_AGG}) != Sign(Delay({_AGG}, 1)), 60)", family="stalemate",
         rationale="Aggression side flip-flops: alternating who wins the close.", logic_score=66),
    # ---------------- wildcards (9)
    dict(name="c_vwap_drift", expr="-(VWAP / Delay(VWAP, 20) - 1)", family="reversal",
         rationale="VWAP-to-VWAP monthly drift: volume-weighted reversal (close-based bands owned; vwap-based path differs).", logic_score=66),
    dict(name="c_vwap_hl_pos_med", expr="-TsMed((VWAP - LOW) / (HIGH - LOW), 120)", family="micro",
         rationale="Median vwap position in range at 120d (main's mean-20d failed; robust long window is the last test of this family).", logic_score=64),
    dict(name="c_up_gap_burst", expr=f"-TsCount(({_GAP}) > 2 * TsStd({_GAP}, 60), 120)", family="overnight",
         rationale="Extreme gap-up habit at 120d (gapdn version failed at 60/120 in canonical; up-side untested here).", logic_score=65),
    dict(name="c_close_range_med", expr="-TsMed((CLOSE - LOW) / (HIGH - LOW), 120)", family="micro",
         rationale="Median close position in range at 120d (60d failed at S1 0.13 — the long-window robust retry).", logic_score=64),
    dict(name="c_amihud_asym_60", expr="-(TsMean((Abs(RET) / AMOUNT) * (RET > 0), 60) - TsMean((Abs(RET) / AMOUNT) * (RET < 0), 60))",
         family="liquidity", rationale="Asymmetric impact at 60d (20d was 0.13 ICIR; quarterly may stabilize).", logic_score=65),
    dict(name="c_updn_amt_ratio", expr="-(TsSum(AMOUNT * (RET > 0), 60) / (TsSum(AMOUNT, 60) + 1))", family="volume",
         rationale="Dollar share on up days (volume version deduped in main; dollar flavor).", logic_score=65),
    dict(name="c_range_per_vol", expr=f"-TsMed(({_HL}) / ({_NVOL} + 0.1), 60)", family="liquidity",
         rationale="Range per unit attention: movement the crowd DIDN'T cause (median form).", logic_score=66),
    dict(name="c_quiet_range", expr=f"-TsMean(({_HL}) * ({_NVOL} < 0.5), 60)", family="conditional",
         rationale="Range on dead-volume days: unexplained movement.", logic_score=66),
    dict(name="c_loud_still", expr=f"-TsCount((({_NVOL} > 2) * (({_HL}) < TsMed({_HL}, 60))) > 0.5, 60)", family="daytype",
         rationale="Heavy volume, small range: high-effort low-progress days (churn with tighter range def).", logic_score=66),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
