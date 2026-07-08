# Canonical set — Round 3 (34 candidates) — generated 2026-07-08.
#
# Set 55 -> target 100. Retrieve: nvol conditionals/asyms/events mint,
# nvol couplings with range/gap partners die at S1 (except possibly at
# longer bands), main-set band-coexistence patterns (semivol 20/60/120,
# min 20/60, meanmed 20/60/120 all coexisted there). This round sweeps
# remaining tiers: bands of residents that coexisted in the main set,
# turnover-analog constructs that never had a canonical test (spike,
# lag2), range bursts, gap conditionals.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ---------------- bands that coexisted in the main set (14)
    dict(name="c_semivol60", expr="-(TsStd((RET + Abs(RET)) / 2, 60) - TsStd((RET - Abs(RET)) / 2, 60))",
         family="volatility", rationale="Quarterly semivol (20/120 in set; all three coexisted in main).", logic_score=74),
    dict(name="c_meanmed60", expr="-(TsMean(RET, 60) - TsMed(RET, 60))", family="reversal",
         rationale="Quarterly mean-median gap.", logic_score=70),
    dict(name="c_meanmed120", expr="-(TsMean(RET, 120) - TsMed(RET, 120))", family="reversal",
         rationale="Semi-annual mean-median gap.", logic_score=69),
    dict(name="c_volterm_mid", expr="-(TsStd(RET, 20) / TsStd(RET, 120))", family="volatility",
         rationale="Mid-band vol term (main accepted).", logic_score=70),
    dict(name="c_hlterm_slow", expr=f"-(TsMed({_HL}, 60) / TsMed({_HL}, 250))", family="volatility",
         rationale="Slow median-range term ratio.", logic_score=68),
    dict(name="c_min60", expr="-TsMin(RET, 60)", family="lottery",
         rationale="Quarterly MIN (coexisted with 20d in main).", logic_score=70),
    dict(name="c_max120", expr="-TsMax(RET, 120)", family="lottery",
         rationale="Semi-annual MAX (died at 0.72 in main vs 60d — retest without the main set's shadow).", logic_score=67),
    dict(name="c_aggrmax60", expr=f"-TsMax({_AGG}, 60)", family="aggression",
         rationale="Quarterly peak aggression (coexisted in main).", logic_score=70),
    dict(name="c_aggr_burst120", expr=f"-TsCount(({_AGG}) > 2 * TsStd({_AGG}, 60), 120)", family="aggression",
         rationale="Semi-annual aggression bursts (main accepted).", logic_score=68),
    dict(name="c_hl_updown120", expr=f"-(TsStd(({_HL}) * (RET > 0), 120) - TsStd(({_HL}) * (RET < 0), 120))",
         family="asymmetry", rationale="Semi-annual range asymmetry.", logic_score=69),
    dict(name="c_vol_updown120", expr=f"-(TsStd(({_NVOL}) * (RET > 0), 120) - TsStd(({_NVOL}) * (RET < 0), 120))",
         family="asymmetry", rationale="Semi-annual volume asymmetry.", logic_score=68),
    dict(name="c_rev120", expr=f"-TsSum({_ID}, 120)", family="reversal",
         rationale="Semi-annual intraday reversal band.", logic_score=69),
    dict(name="c_idmed120", expr=f"TsMed({_ID}, 120)", family="reversal",
         rationale="Semi-annual median intraday drift.", logic_score=68),
    dict(name="c_gapvol60", expr=f"-TsStd({_GAP}, 60)", family="overnight",
         rationale="Quarterly overnight risk (died 0.74 vs 20d in main — retest here).", logic_score=67),
    # ---------------- turnover-analog constructs never canonically tested (5)
    dict(name="c_nvol_spike", expr="-(TsMean(VOLUME, 5) / TsMean(VOLUME, 60))", family="volume",
         rationale="Volume spike vs baseline (turn_spike analog, main R1 accept).", logic_score=73),
    dict(name="c_lag2", expr=f"-TsCorr({_NVOL}, Delay(RET, 2), 20)", family="coupling",
         rationale="Two-day lagged chase (main accepted).", logic_score=69),
    dict(name="c_lag2_60", expr=f"-TsCorr({_NVOL}, Delay(RET, 2), 60)", family="coupling",
         rationale="Quarterly band of the above.", logic_score=68),
    dict(name="c_nvolmax", expr=f"-TsMax({_NVOL}, 20)", family="volume",
         rationale="Biggest attention day (vr_max died vs turn_cv in main; no turn_cv here).", logic_score=69),
    dict(name="c_nvolmax60", expr=f"-TsMax({_NVOL}, 60)", family="volume",
         rationale="Quarterly biggest attention day.", logic_score=68),
    # ---------------- range/gap events (5)
    dict(name="c_hl_burst", expr=f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 60)", family="event",
         rationale="Range-burst days (amp_burst analog, main accepted).", logic_score=70),
    dict(name="c_hl_burst120", expr=f"-TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 120)", family="event",
         rationale="Semi-annual range-burst habit.", logic_score=68),
    dict(name="c_gapmed20", expr=f"TsMed({_GAP}, 20)", family="overnight",
         rationale="Fast median overnight drift (main accepted).", logic_score=69),
    dict(name="c_min_gap60", expr=f"-TsMin({_GAP}, 60)", family="overnight",
         rationale="Quarterly deepest gap-down (20d died vs gap_vol in main; band may escape).", logic_score=66),
    dict(name="c_gapmax20", expr=f"-TsMax({_GAP}, 20)", family="overnight",
         rationale="Monthly biggest gap-up (60d in set).", logic_score=66),
    # ---------------- couplings at deeper bands (3)
    dict(name="c_hl_nvol_corr120", expr=f"-TsCorr({_HL}, {_NVOL}, 120)", family="coupling",
         rationale="Range-attention coupling at 120d (20d had ICIR 0.34 but IC under bar — bands usually lift IC).", logic_score=67),
    dict(name="c_pvcorr60", expr="-TsCorr(CsRank(CLOSE), CsRank(VOLUME), 60)", family="coupling",
         rationale="Quarterly price-volume agreement (10d version in set).", logic_score=68),
    dict(name="c_illiq_term", expr="-(TsMean(Abs(RET) / AMOUNT, 20) / TsMean(Abs(RET) / AMOUNT, 120))", family="liquidity",
         rationale="Illiquidity term structure: price impact vs own baseline.", logic_score=67),
    # ---------------- conditionals (7)
    dict(name="c_gap_on_hivol60", expr=f"TsSum(({_GAP}) * ({_NVOL} > 1), 60)", family="conditional",
         rationale="Gap momentum on attention days, quarterly (20d failed in main; tier lesson says retry higher).", logic_score=67),
    dict(name="c_gap_on_hivol120", expr=f"TsSum(({_GAP}) * ({_NVOL} > 1), 120)", family="conditional",
         rationale="Semi-annual gap-with-attention momentum.", logic_score=67),
    dict(name="c_ret_on_lovol120", expr="TsSum(RET * (VOLUME < TsMean(VOLUME, 120)), 120)", family="conditional",
         rationale="Quiet-day returns persist (S1-failed at 20d in main; the 120d tier rescued its sibling).", logic_score=67),
    dict(name="c_upday_share_hivol", expr=f"-(TsCount((({_NVOL} > 1) * (RET > 0)) > 0.5, 60) / (TsCount({_NVOL} > 1, 60) + 1))",
         family="conditional", rationale="Share of attention days that were up-days: crowd win-rate ratio.", logic_score=67),
    dict(name="c_aggr_updown", expr=f"-(TsStd(({_AGG}) * (RET > 0), 20) - TsStd(({_AGG}) * (RET < 0), 20))",
         family="asymmetry", rationale="Aggression asymmetry across up/down days (main accepted 0.039 OOS).", logic_score=69),
    dict(name="c_aggr_updown60", expr=f"-(TsStd(({_AGG}) * (RET > 0), 60) - TsStd(({_AGG}) * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly aggression asymmetry.", logic_score=68),
    dict(name="c_id_updown", expr=f"-(TsStd(({_ID}) * (RET > 0), 20) - TsStd(({_ID}) * (RET < 0), 20))",
         family="asymmetry", rationale="Intraday-leg vol asymmetry across up/down days.", logic_score=68),
]

assert len(CANDIDATES) == 34, len(CANDIDATES)
