# Round 7 candidates (40) — generated 2026-07-07 by the mining agent.
#
# Retrieve: R6 verdict — flow LEVELS dead, flow-return COUPLING alive
# (mf_ret_corr OOS 0.070). Cross-quantity correlations have minted in 3
# straight rounds. Trick portfolio {count, recency, self-rank,
# conditional-mean} x {new quantity} keeps working. One representative
# per event type. No TsCorr on 0-filled HK/RZ fields.
#
# Generate: lead-lag flow correlations, unexplored corr pairs, MF event
# structures, bands of accepted corr constructs, behavioral interactions.

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"

CANDIDATES = [
    # ------------------------------------------------ lead-lag flow coupling
    dict(name="mf_lead", expr="TsCorr(Delay(MF_LG_NET, 1), RET, 20)", family="flow_coupling",
         rationale="Institutional flow LEADING next-day returns: informed-money detection (lag breaks same-day mechanics).", logic_score=78),
    dict(name="mf_lag_chase", expr="-TsCorr(MF_LG_NET, Delay(RET, 1), 20)", family="flow_coupling",
         rationale="Big orders chasing yesterday's move: momentum-money crowding.", logic_score=74),
    dict(name="mf_sm_ret_corr", expr="TsCorr(MF_SM_NET, RET, 20)", family="flow_coupling",
         rationale="Retail chase coupling — mirror of the accepted large-order version (corr gate arbitrates the mechanical anti-correlation).", logic_score=70),
    dict(name="mf_turn_corr", expr="-TsCorr(MF_LG_NET, TURN_F, 20)", family="flow_coupling",
         rationale="Institutional flow arriving WITH the crowd vs quietly.", logic_score=73),
    dict(name="mf_gap_corr", expr=f"-TsCorr(MF_LG_NET, {_GAP}, 20)", family="flow_coupling",
         rationale="Big money positioned with overnight gaps: news-chasing institutions.", logic_score=71),
    dict(name="mf_amp_corr", expr="-TsCorr(MF_LG_NET, AMP, 20)", family="flow_coupling",
         rationale="Institutions active on wide-range days: urgency signature.", logic_score=70),
    dict(name="mf_vwap_corr", expr=f"-TsCorr(MF_LG_NET, {_AGG}, 20)", family="flow_coupling",
         rationale="Large orders coupled with late-day aggression: closing-auction pushers.", logic_score=71),
    # ------------------------------------------------ other corr pairs
    dict(name="aggr_ret_corr", expr=f"-TsCorr({_AGG}, RET, 20)", family="cross_corr",
         rationale="Late-day aggression coupled with the day's direction: chase conviction.", logic_score=70),
    dict(name="gapabs_turn_corr", expr=f"-TsCorr(Abs({_GAP}), TURN_F, 20)", family="cross_corr",
         rationale="Do overnight shocks draw the day crowd? Shock-chasing habitat.", logic_score=70),
    dict(name="vr_lead", expr="-TsCorr(Delay(VR, 1), RET, 20)", family="cross_corr",
         rationale="Yesterday's attention spike vs today's return: stale-attention fade.", logic_score=69),
    dict(name="std_vr_corr", expr="-TsCorr(TsStd(RET, 5), VR, 20)", family="cross_corr",
         rationale="Short-run risk attracting attention (VR flavor of the accepted TURN version — corr gate decides).", logic_score=68),
    dict(name="amp_vr_corr", expr="-TsCorr(AMP, VR, 20)", family="cross_corr",
         rationale="Range expansion coupled with attention bursts.", logic_score=68),
    # ------------------------------------------------ MF event structures
    dict(name="mf_ret_corr60", expr="-TsCorr(MF_LG_NET, RET, 60)", family="flow_band",
         rationale="Quarterly band of the R6 winner (bands proved separable for reversal; test for coupling).", logic_score=72),
    dict(name="mf_sm_burst", expr="-TsCount(MF_SM_NET > 2 * TsStd(MF_SM_NET, 60), 60)", family="flow_event",
         rationale="Retail-frenzy-day frequency: extreme small-order buying days.", logic_score=74),
    dict(name="mf_lg_rec", expr="CsRank(HighDay(MF_LG_NET, 120))", family="flow_event",
         rationale="Days since the biggest institutional buy: flow-event recency.", logic_score=71),
    dict(name="mf_on_limit", expr="-TsSum(MF_SM_NET * (limit_up_touch > 0.5), 60)", family="flow_event",
         rationale="Retail net buying specifically at limit-up events: mania participation.", logic_score=73),
    dict(name="mf_lg_on_amp", expr="TsSum(MF_LG_NET * (AMP > TsMean(AMP, 20)), 20)", family="flow_event",
         rationale="Institutional net flow on volatile days only: conviction under stress.", logic_score=72),
    dict(name="mf_sm_selfrank", expr="-TsRank(TsMean(MF_SM_NET, 20), 120)", family="flow_event",
         rationale="Retail flow vs own history (self-rank rescued the Amihud level in R4 — one retry slot for a dead flow level).", logic_score=69),
    # ------------------------------------------------ attention / aggression events
    dict(name="vr_on_up", expr="-(TsSum(VR * (RET > 0), 20) / TsSum(VR, 20))", family="attention",
         rationale="Attention share spent on up days (VR flavor of crowding aggregation).", logic_score=69),
    dict(name="vr_selfrank", expr="-TsRank(VR, 120)", family="attention",
         rationale="Attention state vs own history: the framing that dodges the level family.", logic_score=69),
    dict(name="vr_burst_rec", expr="CsRank(HighDay(VR, 120))", family="attention",
         rationale="Days since the attention explosion: recency complement of the accepted burst count.", logic_score=69),
    dict(name="aggr_burst_freq", expr=f"-TsCount(({_AGG}) > 2 * TsStd({_AGG}, 60), 60)", family="aggression",
         rationale="Aggressive-close-day frequency: repeat late-day pushers.", logic_score=70),
    dict(name="aggr_band7", expr=f"-DecayLinear({_AGG}, 7)", family="aggression",
         rationale="Fast band of close-vs-vwap aggression (weekly decay).", logic_score=68),
    # ------------------------------------------------ tail events on legs
    dict(name="min_freq", expr="-TsCount(RET < -2 * TsStd(RET, 60), 60)", family="tail_event",
         rationale="Extreme down-day frequency: crash habit (mirror of accepted max_freq; MIN mirror worked).", logic_score=71),
    dict(name="intr_burst_freq", expr=f"-TsCount(({_ID}) > 2 * TsStd({_ID}, 60), 60)", family="tail_event",
         rationale="Intraday-leg extreme frequency (leg flavor of max_freq — corr gate arbitrates).", logic_score=67),
    dict(name="gap_burst_rec", expr=f"CsRank(HighDay(Abs({_GAP}), 120))", family="tail_event",
         rationale="Days since the biggest overnight shock: gap-event recency.", logic_score=68),
    dict(name="limit_dn_rec", expr="CsRank(HighDay(limit_down_close, 120))", family="tail_event",
         rationale="Days since the last limit-down close: crash recency (count version just missed at S1 in R5).", logic_score=69),
    dict(name="one_word_rec", expr="CsRank(HighDay(one_word_board, 120))", family="tail_event",
         rationale="Days since the last one-word board: hardest-mania recency.", logic_score=68),
    # ------------------------------------------------ bands of accepted couplings
    dict(name="ret_vr_corr60", expr="-TsCorr(RET, VR, 60)", family="corr_band",
         rationale="Quarterly band of the R6 replacement winner.", logic_score=68),
    dict(name="attn_risk_corr60", expr="-TsCorr(TURN_F, TsStd(RET, 5), 60)", family="corr_band",
         rationale="Quarterly band of attention-risk coupling.", logic_score=68),
    dict(name="lag_chase60", expr="-TsCorr(TURN_F, Delay(RET, 1), 60)", family="corr_band",
         rationale="Quarterly band of the lagged chase.", logic_score=67),
    dict(name="med_band60", expr="-(CLOSE / TsMed(CLOSE, 60) - 1)", family="reversal_band",
         rationale="Quarterly median reversal (20d version accepted; band trick).", logic_score=69),
    # ------------------------------------------------ interactions (behavioral)
    dict(name="ix_volclock_rev", expr=f"(CsRank(-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))) - 0.5) * (CsRank(-TsSum({_ID}, 20)) - 0.5)",
         family="interaction",
         rationale="Volume clock x intraday reversal: quiet-year names reverting.", logic_score=70),
    dict(name="ix_mfcorr_turnself", expr="(CsRank(-TsCorr(MF_LG_NET, RET, 20)) - 0.5) * (CsRank(-TsRank(TURN_F, 120)) - 0.5)",
         family="interaction",
         rationale="Flow-coupling x self-relative attention (both accepted, low mutual corr).", logic_score=69),
    dict(name="ix_minmax", expr="(CsRank(-TsMax(RET, 20)) - 0.5) * (CsRank(-TsMin(RET, 20)) - 0.5)",
         family="interaction",
         rationale="Both tails at once: lottery AND crash profile agreement.", logic_score=69),
    dict(name="ix_vrburst_gapvol", expr=f"(CsRank(-TsCount(VR > 2, 60)) - 0.5) * (CsRank(-TsStd({_GAP}, 20)) - 0.5)",
         family="interaction",
         rationale="Attention bursts x overnight risk.", logic_score=68),
    # ------------------------------------------------ probes
    dict(name="vr_skew", expr="-TsSkew(VR, 60)", family="probe",
         rationale="Attention skewness (turnover skew died; VR is burst-native — one probe).", logic_score=65),
    dict(name="signed_amp", expr="-TsMean(Sign(RET) * AMP, 20)", family="probe",
         rationale="Direction-weighted range: which side owns the wide days.", logic_score=67),
    dict(name="mf_net_abs", expr="-TsMean(Abs(MF_NET), 20)", family="probe",
         rationale="Magnitude of net flow imbalance (either direction): one-sided books fade.", logic_score=66),
    dict(name="gap_asym_cnt", expr=f"-(TsCount(({_GAP}) > 2 * TsStd({_GAP}, 60), 60) - TsCount(({_GAP}) < -2 * TsStd({_GAP}, 60), 60))",
         family="probe",
         rationale="Extreme gap-up minus gap-down counts: net shock direction habit.", logic_score=66),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
