# Round 12 candidates (40) — generated 2026-07-08 by the mining agent.
#
# Set at 95/100. Retrieve: 120d tier is a full vein; masked-asym
# generalizes across quantities; only reversal transfers to residuals;
# 60d conditional return sums are intr_mom60 in disguise (120d escapes).
# New theory-backed probe: zero-return frequency (Lesmond illiquidity).

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_RESID = "RegResi(RET, BENCH_RET, 60)"

CANDIDATES = [
    # ------------------------------------------------ masked asymmetries (6)
    dict(name="gap_updown_asym", expr=f"-(TsStd(({_GAP}) * (RET > 0), 20) - TsStd(({_GAP}) * (RET < 0), 20))",
         family="asymmetry", rationale="Overnight-gap vol asymmetry across up/down days.", logic_score=68),
    dict(name="aggr_updown_asym", expr=f"-(TsStd(({_AGG}) * (RET > 0), 20) - TsStd(({_AGG}) * (RET < 0), 20))",
         family="asymmetry", rationale="Aggression-vol asymmetry across up/down days.", logic_score=68),
    dict(name="amp_updown_60", expr="-(TsStd(AMP * (RET > 0), 60) - TsStd(AMP * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly band of the R11 amp-asymmetry winner.", logic_score=68),
    dict(name="vr_updown_60", expr="-(TsStd(VR * (RET > 0), 60) - TsStd(VR * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly VR asymmetry (20d died at 0.71 corr; band may escape).", logic_score=67),
    dict(name="turn_updown_120", expr="-(TsStd(TURN_F * (RET > 0), 120) - TsStd(TURN_F * (RET < 0), 120))",
         family="asymmetry", rationale="Semi-annual turnover asymmetry (20d and 60d both accepted).", logic_score=67),
    dict(name="amp_updown_120", expr="-(TsStd(AMP * (RET > 0), 120) - TsStd(AMP * (RET < 0), 120))",
         family="asymmetry", rationale="Semi-annual amp asymmetry.", logic_score=67),
    # ------------------------------------------------ zero-return illiquidity (3)
    dict(name="zeroret_freq", expr="-TsCount(Abs(RET) < 0.001, 60)", family="liquidity",
         rationale="Lesmond zero-return days: transaction-cost illiquidity (untested classic; direction to data).", logic_score=74),
    dict(name="zeroret_freq120", expr="-TsCount(Abs(RET) < 0.001, 120)", family="liquidity",
         rationale="Semi-annual zero-return count.", logic_score=71),
    dict(name="flatclose_freq", expr=f"-TsCount(Abs({_ID}) < 0.001, 60)", family="liquidity",
         rationale="Flat intraday days: no intraday price discovery.", logic_score=68),
    # ------------------------------------------------ conditionals 120 tier (5)
    dict(name="ret_on_hivr120", expr="-TsSum(RET * (VR > 1), 120)", family="conditional",
         rationale="Semi-annual returns on high-VR days (60d died vs intr_mom60; 120d tier escapes).", logic_score=69),
    dict(name="id_on_hivol120", expr="-TsSum((CLOSE / OPEN - 1) * (TURN_F > TsMean(TURN_F, 120)), 120)", family="conditional",
         rationale="Semi-annual intraday leg on high-attention days.", logic_score=68),
    dict(name="attn_up_cnt120", expr="-TsCount(((VR > 1) * (RET > 0)) > 0.5, 120)", family="conditional",
         rationale="Semi-annual attention-up-day count (60d accepted).", logic_score=67),
    dict(name="attn_dn_cnt", expr="-TsCount(((VR > 1) * (RET < 0)) > 0.5, 60)", family="conditional",
         rationale="Attention-down-day count: crowded selling events (mirror of the accepted up version).", logic_score=67),
    dict(name="ret_on_hiamp120", expr="-TsSum(RET * (AMP > TsMean(AMP, 120)), 120)", family="conditional",
         rationale="Semi-annual returns on wide-range days.", logic_score=67),
    # ------------------------------------------------ idio structures (4)
    dict(name="idio_rev60", expr=f"-TsSum({_RESID}, 60)", family="idio",
         rationale="Quarterly idiosyncratic reversal (20d accepted; reversal transfers to residuals).", logic_score=69),
    dict(name="idio_min", expr=f"-TsMin({_RESID}, 20)", family="idio",
         rationale="Idio crash magnitude (MIN transfers where MAX collided with max_eff?).", logic_score=66),
    dict(name="idio_med_rev", expr=f"-({_RESID} * 0 + CLOSE / TsMed(CLOSE, 20) - 1) * (-1)", family="probe",
         rationale="Placeholder-free robust idio: skip — replaced by direct construct below.", logic_score=50),
    dict(name="idio_hivol", expr=f"-TsSum(({_RESID}) * (TURN_F > TsMean(TURN_F, 60)), 60)", family="idio",
         rationale="Idio returns earned on high-attention days: conditional + residual combined.", logic_score=68),
    # ------------------------------------------------ coupling bands (6)
    dict(name="mf_amp_corr120", expr="-TsCorr(MF_LG_NET, AMP, 120)", family="corr_band",
         rationale="Semi-annual flow-range coupling (20d and 60d accepted).", logic_score=67),
    dict(name="mf_vwap_corr120", expr=f"-TsCorr(MF_LG_NET, {_AGG}, 120)", family="corr_band",
         rationale="Semi-annual flow-aggression coupling.", logic_score=67),
    dict(name="ret_amp_corr120", expr="-TsCorr(RET, AMP, 120)", family="corr_band",
         rationale="Semi-annual return-range coupling (60d accepted).", logic_score=67),
    dict(name="aggr_amp_corr60", expr=f"-TsCorr({_AGG}, AMP, 60)", family="corr_band",
         rationale="Quarterly aggression-range coupling (20d accepted at OOS 0.050).", logic_score=67),
    dict(name="lag_chase250", expr="-TsCorr(TURN_F, Delay(RET, 1), 250)", family="corr_band",
         rationale="Annual lagged-chase band (20/60/120 all accepted — deepest band test).", logic_score=66),
    dict(name="mf_ret_corr250", expr="-TsCorr(MF_LG_NET, RET, 250)", family="corr_band",
         rationale="Annual flow coupling.", logic_score=66),
    # ------------------------------------------------ term ratios (4)
    dict(name="amp_term_med", expr="-(TsMed(AMP, 20) / TsMed(AMP, 120))", family="volatility",
         rationale="Median-amp term ratio (hl_term flavor, accepted R11).", logic_score=67),
    dict(name="aggr_vol_term", expr=f"-(TsStd({_AGG}, 5) / TsStd({_AGG}, 60))", family="volatility",
         rationale="Aggression-vol term structure.", logic_score=66),
    dict(name="gapvol_term_slow", expr=f"-(TsStd({_GAP}, 20) / TsStd({_GAP}, 120))", family="volatility",
         rationale="Slow overnight-risk term (5/60 version failed at S1; slower may hold).", logic_score=66),
    dict(name="turn_term_med", expr="-(TsMed(TURN_F, 20) / TsMed(TURN_F, 120))", family="attention",
         rationale="Median-turnover term ratio: robust attention regime.", logic_score=66),
    # ------------------------------------------------ event tier fills (6)
    dict(name="aggr_burst120", expr=f"-TsCount(({_AGG}) > 2 * TsStd({_AGG}, 60), 120)", family="event_freq",
         rationale="Semi-annual aggression-burst count (60d accepted).", logic_score=66),
    dict(name="max_eff120", expr="-TsMax(RET, 120)", family="lottery",
         rationale="Semi-annual MAX (20d and 60d both strong).", logic_score=67),
    dict(name="min_eff120", expr="-TsMin(RET, 120)", family="lottery",
         rationale="Semi-annual MIN mirror.", logic_score=66),
    dict(name="aggr_max120", expr=f"-TsMax({_AGG}, 120)", family="tail_event",
         rationale="Semi-annual peak aggression.", logic_score=66),
    dict(name="gap_max60", expr=f"-TsMax({_GAP}, 60)", family="tail_event",
         rationale="Quarterly biggest gap-up (20d died vs gap_vol; quarterly may escape).", logic_score=65),
    dict(name="limit_up_close_ratio", expr="-(TsCount(limit_up_close > 0.5, 60) / (TsCount(limit_up_touch > 0.5, 60) + 1))",
         family="limit_board",
         rationale="Share of limit touches that HELD to close: mania conviction ratio (ratio breaks the level corr that killed limit_close_cnt).", logic_score=69),
    # ------------------------------------------------ misc probes (6)
    dict(name="med_dev_vwap", expr="-(VWAP / TsMed(VWAP, 60) - 1)", family="reversal_band",
         rationale="VWAP vs own median: volume-weighted quarterly stretch (close flavor is the med_band60 champion).", logic_score=67),
    dict(name="signed_amp60", expr="-TsMean(Sign(RET) * AMP, 60)", family="probe",
         rationale="Quarterly direction-weighted range (20d died vs intraday_rev; band may escape).", logic_score=65),
    dict(name="updn_vol_ratio", expr="-(TsStd((RET + Abs(RET)) / 2, 60) / TsStd((RET - Abs(RET)) / 2, 60))",
         family="volatility",
         rationale="Up/down vol RATIO (difference form accepted; ratio is scale-free).", logic_score=66),
    dict(name="turn_med_dev", expr="-(TURN_F / TsMed(TURN_F, 60) - 1)", family="attention",
         rationale="Today's attention vs own median: robust spike measure.", logic_score=66),
    dict(name="mf_abs_med", expr="-TsMed(Abs(MF_NET), 60)", family="probe",
         rationale="Median flow imbalance magnitude: chronic one-sidedness.", logic_score=64),
    dict(name="gap_sign_bal", expr=f"-Abs(TsMean(Sign({_GAP}), 60))", family="probe",
         rationale="One-sidedness of gap directions (magnitude-free balance probe).", logic_score=63),
]

CANDIDATES = [c for c in CANDIDATES if c["name"] != "idio_med_rev"]
assert len(CANDIDATES) == 39, len(CANDIDATES)
