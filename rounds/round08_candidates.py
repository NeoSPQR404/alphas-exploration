# Round 8 candidates (40) — generated 2026-07-07 by the mining agent.
#
# Retrieve: corr constructs band-separable; MF coupling needs price-action
# partners; burst freq+recency mintable per quantity; interactions
# (behavioral) the biggest open pool; lead-lag dead; crash-frequency dead;
# one representative per event type.
#
# Special: alpha_0006 was retired in R6, so ret_amp_corr (rejected R5 only
# for correlating with it) gets a clean retry.

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"

CANDIDATES = [
    # ------------------------------------------------ interactions (10)
    dict(name="ix_medband_volclock", expr=f"(CsRank(-(CLOSE / TsMed(CLOSE, 60) - 1)) - 0.5) * (CsRank(-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))) - 0.5)",
         family="interaction", rationale="Quarterly median reversal x volume clock (two strongest recent OOS factors).", logic_score=71),
    dict(name="ix_maxeff_lowturn", expr="(CsRank(-TsMax(RET, 20)) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
         family="interaction", rationale="Lottery x neglect: the two R1 anchors, never interacted.", logic_score=71),
    dict(name="ix_fragility_vrburst", expr="(CsRank(-RegBeta(Abs(RET), TURN_F, 20)) - 0.5) * (CsRank(-TsCount(VR > 2, 60)) - 0.5)",
         family="interaction", rationale="Fragile books x attention bursts.", logic_score=69),
    dict(name="ix_limit_turnself", expr="(CsRank(-TsCount(limit_up_touch > 0.5, 60)) - 0.5) * (CsRank(-TsRank(TURN_F, 120)) - 0.5)",
         family="interaction", rationale="Mania events x self-relative attention state.", logic_score=69),
    dict(name="ix_semivol_volclock", expr="(CsRank(-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))) - 0.5) * (CsRank(-(TsSum(VOLUME, 20) / TsSum(VOLUME, 250))) - 0.5)",
         family="interaction", rationale="Vol-shape x long-band attention.", logic_score=68),
    dict(name="ix_mfvwap_rev", expr=f"(CsRank(-TsCorr(MF_LG_NET, {_AGG}, 20)) - 0.5) * (CsRank(-TsSum({_ID}, 20)) - 0.5)",
         family="interaction", rationale="Flow-aggression coupling x intraday reversal.", logic_score=68),
    dict(name="ix_gapvol_maxfreq", expr=f"(CsRank(-TsStd({_GAP}, 20)) - 0.5) * (CsRank(-TsCount(RET > 2 * TsStd(RET, 60), 60)) - 0.5)",
         family="interaction", rationale="Overnight risk x lottery frequency.", logic_score=68),
    dict(name="ix_rsq_turnlow", expr="(CsRank(-(TsCorr(RET, BENCH_RET, 60) * TsCorr(RET, BENCH_RET, 60))) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
         family="interaction", rationale="Idiosyncratic stories x neglect (rsq direction is flipped in the accepted factor — template handles either).", logic_score=67),
    dict(name="ix_mineff_vrmean", expr="(CsRank(-TsMin(RET, 20)) - 0.5) * (CsRank(-TsMean(VR, 20)) - 0.5)",
         family="interaction", rationale="Crash profile x attention level.", logic_score=67),
    dict(name="ix_ampself_medband", expr="(CsRank(-TsRank(AMP, 120)) - 0.5) * (CsRank(-(CLOSE / TsMed(CLOSE, 60) - 1)) - 0.5)",
         family="interaction", rationale="Range state x quarterly stretch.", logic_score=67),
    # ------------------------------------------------ RegBeta / corr bands (4)
    dict(name="fragility60", expr="-RegBeta(Abs(RET), TURN_F, 60)", family="corr_band",
         rationale="Quarterly fragility band (corr bands proved separable; test RegBeta).", logic_score=70),
    dict(name="volresp60", expr="-RegBeta(TURN_F, Abs(RET), 60)", family="corr_band",
         rationale="Quarterly elasticity band.", logic_score=70),
    dict(name="lag2_60", expr="-TsCorr(TURN_F, Delay(RET, 2), 60)", family="corr_band",
         rationale="Quarterly band of the 2-day-lag chase.", logic_score=67),
    dict(name="aggr_attn_corr60", expr=f"-TsCorr({_AGG}, TURN_F, 60)", family="corr_band",
         rationale="Quarterly band of aggression-attention coupling.", logic_score=67),
    # ------------------------------------------------ retired-incumbent retry (2)
    dict(name="ret_amp_corr", expr="-TsCorr(RET, AMP, 20)", family="cross_corr",
         rationale="R5 reject was solely 0.76 corr vs alpha_0006 — which R6 retired. Clean retry of a 1.65x-stronger construct.", logic_score=72),
    dict(name="ret_amp_corr60", expr="-TsCorr(RET, AMP, 60)", family="cross_corr",
         rationale="Its quarterly band.", logic_score=69),
    # ------------------------------------------------ new corr pairs (4)
    dict(name="mf_id_corr", expr=f"-TsCorr(MF_LG_NET, {_ID}, 20)", family="flow_coupling",
         rationale="Flow vs the intraday leg (price-action partner per the R7 rule).", logic_score=71),
    dict(name="gap_aggr_corr", expr=f"-TsCorr({_GAP}, {_AGG}, 20)", family="cross_corr",
         rationale="Overnight gap vs late-day aggression: within-day sentiment relay.", logic_score=69),
    dict(name="aggr_vr_corr", expr=f"-TsCorr({_AGG}, VR, 20)", family="cross_corr",
         rationale="Aggression-attention with VR instead of turnover.", logic_score=67),
    dict(name="std_gap_corr", expr=f"-TsCorr(TsStd(RET, 5), Abs({_GAP}), 20)", family="cross_corr",
         rationale="Short-run risk coupled with overnight shock size.", logic_score=66),
    # ------------------------------------------------ median/robust bands (3)
    dict(name="med_band120", expr="-(CLOSE / TsMed(CLOSE, 120) - 1)", family="reversal_band",
         rationale="Semi-annual median reversal (60d version just posted OOS 0.070).", logic_score=70),
    dict(name="mean_med_gap60", expr="-(TsMean(RET, 60) - TsMed(RET, 60))", family="reversal_band",
         rationale="Quarterly mean-median gap (20d version accepted).", logic_score=67),
    dict(name="gap_med60", expr=f"TsMed({_GAP}, 60)", family="overnight",
         rationale="Robust median overnight drift: outlier-proof overnight momentum.", logic_score=69),
    # ------------------------------------------------ conditional means (5)
    dict(name="aggr_on_down", expr=f"-TsMean(({_AGG}) * (RET < 0), 20)", family="conditional",
         rationale="Defiant strong closes on down days: dip-buying aggression.", logic_score=69),
    dict(name="vr_on_limit", expr="-TsSum(VR * (limit_up_touch > 0.5), 60)", family="conditional",
         rationale="Attention intensity at mania events.", logic_score=68),
    dict(name="amp_share_up", expr="-(TsSum(AMP * (RET > 0), 20) / TsSum(AMP, 20))", family="conditional",
         rationale="Range share spent on up days.", logic_score=67),
    dict(name="intr_on_hiamp", expr=f"-TsSum(({_ID}) * (AMP > TsMean(AMP, 20)), 20)", family="conditional",
         rationale="Intraday reversal harvested on wide-range days only.", logic_score=68),
    dict(name="mf_on_shock", expr=f"TsSum(MF_LG_NET * (Abs({_GAP}) > TsStd({_GAP}, 60)), 60)", family="conditional",
         rationale="Institutional flow on overnight-shock days: crisis-response direction.", logic_score=69),
    # ------------------------------------------------ HK / margin level-safe retries (4)
    dict(name="hk_dip", expr="TsSum(Delta(HK_RATIO, 1) * (RET < 0), 20)", family="northbound",
         rationale="Northbound dip-buying: accumulation into weakness (level-safe, 0-fill compatible).", logic_score=73),
    dict(name="hk_d20_ind", expr="CsIndNeutralize(CsRank(Delta(HK_RATIO, 20)), IND)", family="northbound",
         rationale="Industry-neutral northbound accumulation (raw version was 0.29 ICIR, just under — sector flows may be the noise).", logic_score=72),
    dict(name="rz_burst", expr="-TsCount(RZ_NET > 2 * TsStd(RZ_NET, 60), 60)", family="margin",
         rationale="Leveraged-buying burst days (count is 0-fill safe unlike TsCorr).", logic_score=69),
    dict(name="hk_burst", expr="TsCount(Delta(HK_RATIO, 1) > 2 * TsStd(Delta(HK_RATIO, 1), 60), 60)", family="northbound",
         rationale="Northbound buying-burst days.", logic_score=68),
    # ------------------------------------------------ tail / extreme events (4)
    dict(name="max_gap", expr=f"-TsMax({_GAP}, 20)", family="tail_event",
         rationale="Biggest single gap-up: overnight lottery magnitude (gap flavor of MAX — corr gate arbitrates).", logic_score=67),
    dict(name="aggr_max", expr=f"-TsMax({_AGG}, 20)", family="tail_event",
         rationale="Biggest close-vs-vwap push: peak late-day aggression.", logic_score=66),
    dict(name="lowmake_freq", expr="-TsCount(CLOSE <= TsMin(CLOSE, 60), 60)", family="tail_event",
         rationale="Frequency of making new 60d lows: persistent-loser habit.", logic_score=67),
    dict(name="himake_freq", expr="-TsCount(CLOSE >= TsMax(CLOSE, 60), 60)", family="tail_event",
         rationale="Frequency of making new 60d highs: breakout habit (direction to data).", logic_score=67),
    # ------------------------------------------------ probes (4)
    dict(name="vol_term_mid", expr="-(TsStd(RET, 20) / TsStd(RET, 120))", family="volatility",
         rationale="Mid-band vol term structure (5/60 version accepted).", logic_score=67),
    dict(name="skew20", expr="-TsSkew(RET, 20)", family="lottery",
         rationale="Fast skew band (60d accepted; band separability test on moments).", logic_score=66),
    dict(name="vr_medmean", expr="-(TsMed(VR, 20) / TsMean(VR, 20))", family="attention",
         rationale="VR median/mean: attention burst share (robust shape).", logic_score=66),
    dict(name="amt_burst_freq", expr="-TsCount(Log(AMOUNT) > TsMean(Log(AMOUNT), 60) + 2 * TsStd(Log(AMOUNT), 60), 60)", family="event_freq",
         rationale="Dollar-volume burst frequency (money version of vr_burst — corr gate arbitrates).", logic_score=66),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
