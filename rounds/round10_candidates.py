# Round 10 candidates (40) — generated 2026-07-07 by the mining agent.
#
# First round under the 0.03 IC standard (IS+OOS), set purged 103 -> 69.
# Retrieve: survivors are median/robust, tails, vol shapes/terms, strong
# couplings + bands, attention clocks. Interactions and burst-recency
# rarely clear 0.03 — only strong-parent interactions attempted (4).
# Probes below ~0.04 IS IC die at the OOS bar half the time, so this
# round is all exploitation of proven high-IC construct types.

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"

def _ix(a, b):
    return f"(CsRank({a}) - 0.5) * (CsRank({b}) - 0.5)"

CANDIDATES = [
    # ---------------------------------------- bands of champions (12)
    dict(name="hl_med20", expr="-TsMed(HIGH / LOW - 1, 20)", family="robust",
         rationale="Fast band of the set champion (hl_med60, OOS 0.094).", logic_score=72),
    dict(name="aggr_max60", expr=f"-TsMax({_AGG}, 60)", family="tail_event",
         rationale="Quarterly band of aggr_max (OOS 0.083).", logic_score=70),
    dict(name="max_eff60", expr="-TsMax(RET, 60)", family="lottery",
         rationale="Quarterly MAX effect (20d version OOS 0.091).", logic_score=70),
    dict(name="min_eff60", expr="-TsMin(RET, 60)", family="lottery",
         rationale="Quarterly MIN mirror.", logic_score=69),
    dict(name="gap_med20", expr=f"TsMed({_GAP}, 20)", family="robust",
         rationale="Fast band of median overnight drift.", logic_score=69),
    dict(name="id_med20", expr=f"TsMed({_ID}, 20)", family="robust",
         rationale="Fast band of median intraday drift.", logic_score=69),
    dict(name="lag_chase120", expr="-TsCorr(TURN_F, Delay(RET, 1), 120)", family="corr_band",
         rationale="Semi-annual lagged-chase band (20d and 60d both accepted).", logic_score=68),
    dict(name="ret_vr_corr120", expr="-TsCorr(RET, VR, 120)", family="corr_band",
         rationale="Semi-annual attention-coupling band.", logic_score=68),
    dict(name="attn_risk_corr120", expr="-TsCorr(TURN_F, TsStd(RET, 5), 120)", family="corr_band",
         rationale="Semi-annual attention-risk band.", logic_score=68),
    dict(name="med_band240", expr="-(CLOSE / TsMed(CLOSE, 240) - 1)", family="reversal_band",
         rationale="Annual median stretch (120 died at 0.82 corr vs 60; 240 should decorrelate).", logic_score=68),
    dict(name="mean_med_gap120", expr="-(TsMean(RET, 120) - TsMed(RET, 120))", family="reversal_band",
         rationale="Semi-annual mean-median gap.", logic_score=67),
    dict(name="vol_clock60", expr="-(TsSum(VOLUME, 60) / TsSum(VOLUME, 250))", family="attention",
         rationale="Quarterly volume clock (20/250 version OOS 0.076).", logic_score=68),
    # ---------------------------------------- terms / shapes (7)
    dict(name="gapvol_term", expr=f"-(TsStd({_GAP}, 5) / TsStd({_GAP}, 60))", family="volatility",
         rationale="Overnight-risk term structure (three vol terms already accepted).", logic_score=69),
    dict(name="idvol_term", expr=f"-(TsStd({_ID}, 5) / TsStd({_ID}, 60))", family="volatility",
         rationale="Intraday-leg vol term structure.", logic_score=68),
    dict(name="upvol_share", expr="-(TsStd((RET + Abs(RET)) / 2, 20) / TsStd(RET, 20))", family="volatility",
         rationale="Upside share of total vol: scale-free shape ratio.", logic_score=68),
    dict(name="downvol60", expr="-TsStd((RET - Abs(RET)) / 2, 60)", family="volatility",
         rationale="Pure quarterly downside vol (corr vs semivol60 arbitrates).", logic_score=67),
    dict(name="turnvol_term", expr="-(TsStd(TURN_F, 5) / TsStd(TURN_F, 60))", family="attention",
         rationale="Turnover-VOLATILITY term structure (shape, not level).", logic_score=67),
    dict(name="amp_term_slow", expr="-(TsMean(AMP, 60) / TsMean(AMP, 250))", family="volatility",
         rationale="Slow range regime vs annual baseline.", logic_score=67),
    dict(name="vr_term", expr="-(TsMean(VR, 5) / TsMean(VR, 60))", family="attention",
         rationale="Attention term structure on VR.", logic_score=67),
    # ---------------------------------------- robust untried (5)
    dict(name="vr_med60", expr="-TsMed(VR, 60)", family="robust",
         rationale="Median attention state (robust flavor of vr_mean).", logic_score=68),
    dict(name="medvol", expr="-TsMed(Abs(RET), 60)", family="robust",
         rationale="Median absolute move: robust vol (corr vs hl_med60 arbitrates).", logic_score=68),
    dict(name="hl_max", expr="-TsMax(HIGH / LOW - 1, 20)", family="tail_event",
         rationale="Biggest range day: MAX on the champion quantity.", logic_score=67),
    dict(name="idvol60", expr=f"-TsStd({_ID}, 60)", family="volatility",
         rationale="Intraday-leg vol standalone (overnight-leg vol is a champion; the intraday leg was never tested alone).", logic_score=68),
    dict(name="gap_min", expr=f"-TsMin({_GAP}, 20)", family="tail_event",
         rationale="Deepest gap-down: MIN mirror on the overnight leg.", logic_score=67),
    # ---------------------------------------- couplings untried (5)
    dict(name="id_vr_corr", expr=f"-TsCorr({_ID}, VR, 20)", family="cross_corr",
         rationale="Intraday leg vs attention coupling.", logic_score=68),
    dict(name="gap_vr_corr", expr=f"-TsCorr({_GAP}, VR, 20)", family="cross_corr",
         rationale="Overnight leg vs attention coupling.", logic_score=67),
    dict(name="aggr_amp_corr", expr=f"-TsCorr({_AGG}, AMP, 20)", family="cross_corr",
         rationale="Aggression arriving on wide-range days.", logic_score=67),
    dict(name="mf_id_corr60", expr=f"-TsCorr(MF_LG_NET, {_ID}, 60)", family="flow_coupling",
         rationale="Flow vs intraday leg at quarterly band (20d died at 0.87 vs mf_ret_corr; the band may decorrelate).", logic_score=67),
    dict(name="turn_updown_asym", expr="-(TsStd(TURN_F * (RET > 0), 20) - TsStd(TURN_F * (RET < 0), 20))", family="attention",
         rationale="Turnover vol on up days vs down days: attention-shape asymmetry.", logic_score=66),
    # ---------------------------------------- unlocked retry (1)
    dict(name="intraday_skew", expr=f"-TsSkew({_ID}, 60)", family="lottery",
         rationale="R4 S2 reject solely vs alpha_0008 (skew) — which semivol60 retired in R9. Clean retry, IS was 0.039/0.62.", logic_score=68),
    # ---------------------------------------- strong-parent interactions (4)
    dict(name="ix_hlmed_maxeff", expr=_ix("-TsMed(HIGH / LOW - 1, 60)", "-TsMax(RET, 20)"),
         family="interaction", rationale="Champion x champion (0.094 x 0.091) — only strong parents under the new standard.", logic_score=68),
    dict(name="ix_hlmed_volclock", expr=_ix("-TsMed(HIGH / LOW - 1, 60)", "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))"),
         family="interaction", rationale="Champion x volume clock.", logic_score=68),
    dict(name="ix_aggrmax_gapvol", expr=_ix(f"-TsMax({_AGG}, 20)", f"-TsStd({_GAP}, 20)"),
         family="interaction", rationale="Peak aggression x overnight risk (0.083 x 0.085 parents).", logic_score=67),
    dict(name="ix_maxeff_volclock", expr=_ix("-TsMax(RET, 20)", "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))"),
         family="interaction", rationale="MAX x volume clock.", logic_score=67),
    # ---------------------------------------- long-window events + conditionals (6)
    dict(name="limit_touch250", expr="-TsCount(limit_up_touch > 0.5, 250)", family="limit_board",
         rationale="Annual mania count (60d version IS 0.077 — the strongest event factor).", logic_score=69),
    dict(name="maxfreq250", expr="-TsCount(RET > 2 * TsStd(RET, 60), 250)", family="lottery",
         rationale="Annual lottery-day habit.", logic_score=68),
    dict(name="vr_burst250", expr="-TsCount(VR > 2, 250)", family="attention",
         rationale="Annual attention-burst habit.", logic_score=67),
    dict(name="aggr_hi_vr60", expr=f"-TsMean(({_AGG}) * (VR > 1), 60)", family="conditional",
         rationale="Quarterly band of the accepted conditional aggression (IS 0.054).", logic_score=68),
    dict(name="ret_on_hivol60", expr="-TsSum(RET * (TURN_F > TsMean(TURN_F, 60)), 60)", family="conditional",
         rationale="Quarterly returns earned on high-attention days (20d version died only at corr).", logic_score=67),
    dict(name="limit_dn_mag", expr="TsMin(RET * (limit_down_close > 0.5) + 999 * (limit_down_close < 0.5), 60)", family="probe",
         rationale="Worst limit-down day magnitude within the quarter (999 sentinel keeps non-event days out of the min).", logic_score=63),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
