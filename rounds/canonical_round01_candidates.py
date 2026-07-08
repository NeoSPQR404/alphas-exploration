# Canonical set — Round 1 (40 candidates) — generated 2026-07-08.
#
# Independent factor set restricted to canonical price/volume features:
# OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT, VWAP, RET (hfq-consistent).
# No turnover, volume_ratio, amplitude field, limit boards, flows,
# fundamentals, industry, or bench. AST-enforced via FIELD_WHITELIST.
#
# Generation: 12 rounds of main-set experience distilled into this
# vocabulary. Turnover-based winners are re-expressed with normalized
# volume (nvol = VOLUME / TsMean(VOLUME, 60)); amplitude via HIGH/LOW-1;
# gates identical (0.03 standard, 4 stages). Set starts empty, so S2 is
# trivial and intra-round dedup does the pruning.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"

CANDIDATES = [
    # ------------------------------------------------ reversal / stretch
    dict(name="c_rev20", expr=f"-TsSum({_ID}, 20)", family="reversal",
         rationale="Monthly intraday-leg reversal (main-set staple, holdout 0.093).", logic_score=85),
    dict(name="c_rev60", expr=f"-TsSum({_ID}, 60)", family="reversal",
         rationale="Quarterly intraday reversal (holdout champion 0.095).", logic_score=84),
    dict(name="c_rev7", expr=f"-DecayLinear({_ID}, 7)", family="reversal",
         rationale="Weekly decayed band.", logic_score=76),
    dict(name="c_med20", expr="-(CLOSE / TsMed(CLOSE, 20) - 1)", family="reversal",
         rationale="Monthly median stretch.", logic_score=78),
    dict(name="c_med60", expr="-(CLOSE / TsMed(CLOSE, 60) - 1)", family="reversal",
         rationale="Quarterly median stretch (holdout 0.094).", logic_score=80),
    dict(name="c_meanmed20", expr="-(TsMean(RET, 20) - TsMed(RET, 20))", family="reversal",
         rationale="Mean-median return gap: robust within-window skew.", logic_score=72),
    # ------------------------------------------------ overnight leg
    dict(name="c_gapvol", expr=f"-TsStd({_GAP}, 20)", family="overnight",
         rationale="Overnight-gap risk (main-set top-3 OOS).", logic_score=80),
    dict(name="c_gapmed60", expr=f"TsMed({_GAP}, 60)", family="overnight",
         rationale="Median overnight drift = robust overnight momentum.", logic_score=76),
    dict(name="c_ovnmom60", expr=f"TsSum({_GAP}, 60)", family="overnight",
         rationale="Quarterly overnight momentum.", logic_score=74),
    dict(name="c_ovnshare", expr=f"-TsMean(Abs({_GAP}) / ({_HL}), 20)", family="overnight",
         rationale="Share of daily range realized overnight.", logic_score=72),
    dict(name="c_gapmax60", expr=f"-TsMax({_GAP}, 60)", family="overnight",
         rationale="Quarterly biggest gap-up.", logic_score=70),
    dict(name="c_flatopen", expr=f"-TsCount(Abs({_GAP}) < 0.001, 60)", family="overnight",
         rationale="Attention-void opens (anti-intuitive holdout survivor).", logic_score=70),
    # ------------------------------------------------ tails / lottery
    dict(name="c_max20", expr="-TsMax(RET, 20)", family="lottery",
         rationale="MAX effect (holdout 0.091).", logic_score=84),
    dict(name="c_max60", expr="-TsMax(RET, 60)", family="lottery",
         rationale="Quarterly MAX.", logic_score=78),
    dict(name="c_min20", expr="-TsMin(RET, 20)", family="lottery",
         rationale="MIN mirror: crash continuation.", logic_score=74),
    dict(name="c_maxfreq", expr="-TsCount(RET > 2 * TsStd(RET, 60), 60)", family="lottery",
         rationale="Extreme-day frequency.", logic_score=76),
    dict(name="c_maxfreq120", expr="-TsCount(RET > 2 * TsStd(RET, 60), 120)", family="lottery",
         rationale="Semi-annual lottery habit.", logic_score=72),
    # ------------------------------------------------ vol shapes
    dict(name="c_semivol20", expr="-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
         family="volatility", rationale="Up/down semivol asymmetry.", logic_score=80),
    dict(name="c_semivol120", expr="-(TsStd((RET + Abs(RET)) / 2, 120) - TsStd((RET - Abs(RET)) / 2, 120))",
         family="volatility", rationale="Semi-annual semivol asymmetry (holdout 0.085).", logic_score=76),
    dict(name="c_volterm", expr="-(TsStd(RET, 5) / TsStd(RET, 60))", family="volatility",
         rationale="Vol term structure.", logic_score=74),
    dict(name="c_volterm_slow", expr="-(TsStd(RET, 5) / TsStd(RET, 250))", family="volatility",
         rationale="Fast/annual vol term.", logic_score=71),
    dict(name="c_hlmed60", expr=f"-TsMed({_HL}, 60)", family="volatility",
         rationale="Median daily range — the main set's best OOS factor (0.094).", logic_score=82),
    dict(name="c_hlterm", expr=f"-(TsMed({_HL}, 20) / TsMed({_HL}, 120))", family="volatility",
         rationale="Median-range term ratio.", logic_score=72),
    # ------------------------------------------------ aggression (close vs vwap)
    dict(name="c_aggrmax", expr=f"-TsMax({_AGG}, 20)", family="aggression",
         rationale="Peak late-day aggression (holdout 0.083).", logic_score=76),
    dict(name="c_aggrmin", expr=f"TsMin({_AGG}, 20)", family="aggression",
         rationale="Deepest capitulation close.", logic_score=72),
    dict(name="c_vwapdev", expr=f"-TsMean({_AGG}, 10)", family="aggression",
         rationale="Persistent close-vs-vwap premium.", logic_score=70),
    dict(name="c_aggr_burst", expr=f"-TsCount(({_AGG}) > 2 * TsStd({_AGG}, 60), 60)", family="aggression",
         rationale="Aggressive-close-day frequency.", logic_score=71),
    # ------------------------------------------------ volume structures
    dict(name="c_volclock", expr="-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))", family="volume",
         rationale="Volume clock: month's share of annual volume (holdout 0.085).", logic_score=80),
    dict(name="c_pvcorr", expr="-TsCorr(CsRank(CLOSE), CsRank(VOLUME), 10)", family="volume",
         rationale="Price-volume agreement (R1 best-ICIR construct).", logic_score=76),
    dict(name="c_amt_selfrank", expr="-TsRank(Log(AMOUNT), 120)", family="volume",
         rationale="Dollar-volume self-rank: attention state vs own history.", logic_score=74),
    dict(name="c_volcv", expr="-(TsStd(VOLUME, 20) / TsMean(VOLUME, 20))", family="volume",
         rationale="Volume CV: erratic interest.", logic_score=71),
    dict(name="c_ret_nvol_corr", expr=f"-TsCorr(RET, {_NVOL}, 20)", family="volume",
         rationale="Return-attention coupling with normalized volume (turnover-free re-expression).", logic_score=75),
    dict(name="c_lagchase", expr=f"-TsCorr({_NVOL}, Delay(RET, 1), 20)", family="volume",
         rationale="Volume chasing yesterday's return.", logic_score=73),
    dict(name="c_elasticity", expr=f"-RegBeta({_NVOL}, Abs(RET), 20)", family="volume",
         rationale="Volume elasticity to |return| (main-set ICIR 0.83 as turnover).", logic_score=76),
    dict(name="c_fragility", expr=f"-RegBeta(Abs(RET), {_NVOL}, 20)", family="volume",
         rationale="Price response per unit volume.", logic_score=71),
    dict(name="c_amihud_sr", expr="TsRank(TsMean(Abs(RET) / AMOUNT, 20), 120)", family="liquidity",
         rationale="Amihud illiquidity self-rank.", logic_score=73),
    dict(name="c_zeroret", expr="-TsCount(Abs(RET) < 0.001, 60)", family="liquidity",
         rationale="Zero-return days (Lesmond).", logic_score=72),
    # ------------------------------------------------ conditionals / asymmetries
    dict(name="c_ret_on_hivol60", expr="-TsSum(RET * (VOLUME > TsMean(VOLUME, 60)), 60)", family="conditional",
         rationale="Returns earned on high-volume days (main-set star at 0.082 OOS).", logic_score=76),
    dict(name="c_vol_updown", expr=f"-(TsStd(({_NVOL}) * (RET > 0), 20) - TsStd(({_NVOL}) * (RET < 0), 20))",
         family="asymmetry", rationale="Volume-vol asymmetry across up/down days.", logic_score=74),
    dict(name="c_hl_updown", expr=f"-(TsStd(({_HL}) * (RET > 0), 20) - TsStd(({_HL}) * (RET < 0), 20))",
         family="asymmetry", rationale="Range-vol asymmetry across up/down days (amp flavor was ICIR 0.94).", logic_score=75),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
