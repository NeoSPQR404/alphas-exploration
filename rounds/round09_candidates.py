# Round 9 candidates (40) — generated 2026-07-07 by the mining agent.
#
# Retrieve: interactions 6/8 in R8 (avoid turn_low-type small-cap parents;
# different families); robust/median first-class (median drift beats
# moment drift OOS); MAX-of-quantity works (aggr_max OOS 0.083); bands
# separable incl. RegBeta; HK/margin closed at 10d; one representative
# per event/quantity.

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"

def _ix(a, b):
    return f"(CsRank({a}) - 0.5) * (CsRank({b}) - 0.5)"

CANDIDATES = [
    # ------------------------------------------------ interactions (15)
    dict(name="ix_volclock_maxfreq", expr=_ix("-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))", "-TsCount(RET > 2 * TsStd(RET, 60), 60)"),
         family="interaction", rationale="Volume clock x lottery frequency.", logic_score=69),
    dict(name="ix_medband_gapvol", expr=_ix("-(CLOSE / TsMed(CLOSE, 60) - 1)", f"-TsStd({_GAP}, 20)"),
         family="interaction", rationale="Quarterly stretch x overnight risk.", logic_score=69),
    dict(name="ix_aggrmax_turnself", expr=_ix(f"-TsMax({_AGG}, 20)", "-TsRank(TURN_F, 120)"),
         family="interaction", rationale="Peak aggression x self-relative attention.", logic_score=69),
    dict(name="ix_retvr_medband", expr=_ix("-TsCorr(RET, VR, 20)", "-(CLOSE / TsMed(CLOSE, 60) - 1)"),
         family="interaction", rationale="Attention coupling x quarterly stretch.", logic_score=68),
    dict(name="ix_volterm_limit", expr=_ix("-(TsStd(RET, 5) / TsStd(RET, 60))", "-TsCount(limit_up_touch > 0.5, 60)"),
         family="interaction", rationale="Vol regime x mania events.", logic_score=68),
    dict(name="ix_mfret_gapvol", expr=_ix("-TsCorr(MF_LG_NET, RET, 20)", f"-TsStd({_GAP}, 20)"),
         family="interaction", rationale="Flow coupling x overnight risk.", logic_score=68),
    dict(name="ix_ampburst_rev", expr=_ix("-TsCount(AMP > 2 * TsMean(AMP, 60), 60)", f"-TsSum({_ID}, 20)"),
         family="interaction", rationale="Range-burst habit x intraday reversal.", logic_score=68),
    dict(name="ix_fragility_medband", expr=_ix("-RegBeta(Abs(RET), TURN_F, 20)", "-(CLOSE / TsMed(CLOSE, 60) - 1)"),
         family="interaction", rationale="Fragile books x quarterly stretch.", logic_score=68),
    dict(name="ix_mineff_volclock", expr=_ix("-TsMin(RET, 20)", "-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))"),
         family="interaction", rationale="Crash profile x volume clock.", logic_score=68),
    dict(name="ix_semivol_limit", expr=_ix("-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))", "-TsCount(limit_up_touch > 0.5, 60)"),
         family="interaction", rationale="Vol shape x mania count.", logic_score=67),
    dict(name="ix_lagchase_ampself", expr=_ix("-TsCorr(TURN_F, Delay(RET, 1), 20)", "-TsRank(AMP, 120)"),
         family="interaction", rationale="Chase coupling x range state.", logic_score=67),
    dict(name="ix_ovnmom_vrburst", expr=_ix(f"TsSum({_GAP}, 60)", "-TsCount(VR > 2, 60)"),
         family="interaction", rationale="Overnight momentum x attention bursts.", logic_score=67),
    dict(name="ix_rsq_medband", expr=_ix("-(TsCorr(RET, BENCH_RET, 60) * TsCorr(RET, BENCH_RET, 60))", "-(CLOSE / TsMed(CLOSE, 60) - 1)"),
         family="interaction", rationale="Systematic share x quarterly stretch.", logic_score=67),
    dict(name="ix_volclock_gapmed", expr=_ix("-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))", f"TsMed({_GAP}, 60)"),
         family="interaction", rationale="Volume clock x median overnight drift.", logic_score=67),
    dict(name="ix_amtburst_medband", expr=_ix("-TsCount(Log(AMOUNT) > TsMean(Log(AMOUNT), 60) + 2 * TsStd(Log(AMOUNT), 60), 60)", "-(CLOSE / TsMed(CLOSE, 60) - 1)"),
         family="interaction", rationale="Dollar-burst habit x quarterly stretch.", logic_score=66),
    # ------------------------------------------------ robust / median / MAX (9)
    dict(name="id_med60", expr=f"TsMed({_ID}, 60)", family="robust",
         rationale="Median intraday drift: robust mirror of the accepted median gap drift — but intraday sums are REVERSAL, so the median may flip too (data decides).", logic_score=70),
    dict(name="aggr_med60", expr=f"TsMed({_AGG}, 60)", family="robust",
         rationale="Median aggression drift: persistent (not burst) closing strength.", logic_score=69),
    dict(name="ret_med60", expr="TsMed(RET, 60)", family="robust",
         rationale="Median total drift: outlier-proof momentum/reversal arbiter.", logic_score=68),
    dict(name="amp_med_dev", expr="-(AMP / TsMed(AMP, 60) - 1)", family="robust",
         rationale="Today's range vs own median range: robust range state.", logic_score=67),
    dict(name="hl_med60", expr="-TsMed(HIGH / LOW - 1, 60)", family="robust",
         rationale="Median daily range: robust calm-name premium (corr vs amp-family arbitrates).", logic_score=67),
    dict(name="mf_med60", expr="TsMed(MF_LG_NET, 60)", family="robust",
         rationale="Median institutional stance: the robust rescue attempt for dead flow levels.", logic_score=68),
    dict(name="vr_max", expr="-TsMax(VR, 20)", family="tail_event",
         rationale="Biggest attention day: MAX-of-quantity trick on VR.", logic_score=68),
    dict(name="mf_max", expr="TsMax(MF_LG_NET, 20)", family="tail_event",
         rationale="Biggest institutional buy day: MAX on flow.", logic_score=67),
    dict(name="aggr_min", expr=f"TsMin({_AGG}, 20)", family="tail_event",
         rationale="Deepest capitulation close: MIN on aggression.", logic_score=67),
    # ------------------------------------------------ bands (8)
    dict(name="mf_amp_corr60", expr="-TsCorr(MF_LG_NET, AMP, 60)", family="corr_band",
         rationale="Quarterly band of flow-range coupling.", logic_score=68),
    dict(name="mf_vwap_corr60", expr=f"-TsCorr(MF_LG_NET, {_AGG}, 60)", family="corr_band",
         rationale="Quarterly band of flow-aggression coupling.", logic_score=68),
    dict(name="vol_term_slow", expr="-(TsStd(RET, 60) / TsStd(RET, 250))", family="volatility",
         rationale="Slow vol term structure (5/60 and 20/120 both accepted).", logic_score=67),
    dict(name="semivol60", expr="-(TsStd((RET + Abs(RET)) / 2, 60) - TsStd((RET - Abs(RET)) / 2, 60))", family="volatility",
         rationale="Quarterly semivol asymmetry band.", logic_score=67),
    dict(name="overnight_share60", expr=f"-TsMean(Abs({_GAP}) / AMP, 60)", family="overnight",
         rationale="Quarterly band of overnight price-discovery share.", logic_score=67),
    dict(name="gapvol60", expr=f"-TsStd({_GAP}, 60)", family="overnight",
         rationale="Quarterly overnight-risk band (within-construct: corr gate arbitrates).", logic_score=66),
    dict(name="signed_vr60", expr="-TsMean(Sign(RET) * VR, 60)", family="attention",
         rationale="Quarterly signed-attention band.", logic_score=66),
    dict(name="rsq_bench120", expr="-(TsCorr(RET, BENCH_RET, 120) * TsCorr(RET, BENCH_RET, 120))", family="divergence",
         rationale="Semi-annual systematic-share band.", logic_score=66),
    # ------------------------------------------------ event structures (5)
    dict(name="aggr_burst_rec", expr=f"CsRank(HighDay({_AGG}, 120))", family="event_freq",
         rationale="Days since the aggression peak (freq version accepted in R7).", logic_score=67),
    dict(name="mf_dump_freq", expr="-TsCount(MF_LG_NET < -2 * TsStd(MF_LG_NET, 60), 60)", family="flow_event",
         rationale="Institutional dump-day frequency: sell-side event trick on flows.", logic_score=68),
    dict(name="doji_freq", expr="-TsCount(Abs(CLOSE - OPEN) / (HIGH - LOW) < 0.1, 60)", family="event_freq",
         rationale="Indecision-day frequency (body-share LEVEL died; the event-frequency framing is the rescue pattern).", logic_score=66),
    dict(name="vol_peak_rec", expr="CsRank(HighDay(TsStd(RET, 5), 120))", family="event_freq",
         rationale="Days since the volatility peak: risk-event recency.", logic_score=67),
    dict(name="flat_open_freq", expr=f"-TsCount(Abs({_GAP}) < 0.001, 60)", family="event_freq",
         rationale="Flat-open frequency: no-overnight-interest habit (attention void probe).", logic_score=64),
    # ------------------------------------------------ probes (3)
    dict(name="vwap_gap", expr="-TsMean(OPEN / Delay(VWAP, 1) - 1, 20)", family="overnight",
         rationale="Open vs yesterday's VOLUME-WEIGHTED anchor: gap against where money actually traded.", logic_score=68),
    dict(name="mf_lg_med_dev", expr="MF_LG_NET - TsMed(MF_LG_NET, 60)", family="probe",
         rationale="Today's flow vs own median stance: flow surprise (robust demeaning).", logic_score=66),
    dict(name="amp_min20", expr="TsMin(AMP, 20)", family="probe",
         rationale="Quietest day in the month: minimum-range state (direction to data).", logic_score=64),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
