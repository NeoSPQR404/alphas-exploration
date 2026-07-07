# Round 11 candidates (40) — generated 2026-07-07 by the mining agent.
#
# Retrieve (0.03 standard, set 81): fresh veins = quarterly conditional
# aggregations (ret_on_hivol60 OOS 0.082) and masked-std asymmetries
# (turn_updown_asym OOS 0.068). 60d tails decorrelate from 20d siblings.
# Dead: shape/term variants of residents (S2), champion interactions (S1),
# 250d event counts (OOS bar). This round: push conditionals and
# masked-asymmetry across quantities, idiosyncratic (RegResi) structures,
# robust midrange-tail measures, remaining bands.

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_RESID = "RegResi(RET, BENCH_RET, 60)"

CANDIDATES = [
    # ---------------------------------------- conditional aggregations (10)
    dict(name="ret_on_hivr60", expr="-TsSum(RET * (VR > 1), 60)", family="conditional",
         rationale="Returns earned on high-VR days, quarterly (turnover flavor OOS 0.082).", logic_score=73),
    dict(name="id_on_hivol60", expr="-TsSum((CLOSE / OPEN - 1) * (TURN_F > TsMean(TURN_F, 60)), 60)", family="conditional",
         rationale="Intraday leg harvested on high-attention days, quarterly.", logic_score=71),
    dict(name="gap_on_hivr60", expr=f"TsSum(({_GAP}) * (VR > 1), 60)", family="conditional",
         rationale="Overnight momentum conditional on attention (gaps with eyeballs persist).", logic_score=70),
    dict(name="aggr_on_down60", expr=f"-TsMean(({_AGG}) * (RET < 0), 60)", family="conditional",
         rationale="Defiant closes on down days, quarterly (20d failed ICIR; longer window smooths).", logic_score=69),
    dict(name="mf_on_down60", expr="TsMean(MF_LG_NET * (RET < 0), 60)", family="conditional",
         rationale="Quarterly institutional dip-buying (20d was 0.22 ICIR; band may lift).", logic_score=69),
    dict(name="ret_on_hivol120", expr="-TsSum(RET * (TURN_F > TsMean(TURN_F, 120)), 120)", family="conditional",
         rationale="Semi-annual band of the R10 star.", logic_score=70),
    dict(name="amp_on_down", expr="-TsMean(AMP * (RET < 0), 20)", family="conditional",
         rationale="Range on down days: crash texture.", logic_score=68),
    dict(name="ret_on_hiamp60", expr="-TsSum(RET * (AMP > TsMean(AMP, 60)), 60)", family="conditional",
         rationale="Returns earned on wide-range days.", logic_score=69),
    dict(name="gap_after_down", expr=f"-TsSum(({_GAP}) * (Delay(RET, 1) < 0), 20)", family="conditional",
         rationale="Overnight response to yesterday's losses: disagreement bounce.", logic_score=67),
    dict(name="attn_up_cnt", expr="-TsCount(((VR > 1) * (RET > 0)) > 0.5, 60)", family="conditional",
         rationale="Count of attention-up days: crowd-chase event count.", logic_score=68),
    # ---------------------------------------- masked-std asymmetries (4)
    dict(name="vr_updown_asym", expr="-(TsStd(VR * (RET > 0), 20) - TsStd(VR * (RET < 0), 20))", family="asymmetry",
         rationale="VR-vol asymmetry across up/down days (turnover flavor OOS 0.068 in R10).", logic_score=69),
    dict(name="amp_updown_asym", expr="-(TsStd(AMP * (RET > 0), 20) - TsStd(AMP * (RET < 0), 20))", family="asymmetry",
         rationale="Range-vol asymmetry across up/down days.", logic_score=69),
    dict(name="turn_updown_60", expr="-(TsStd(TURN_F * (RET > 0), 60) - TsStd(TURN_F * (RET < 0), 60))", family="asymmetry",
         rationale="Quarterly band of the new asymmetry winner.", logic_score=68),
    dict(name="mf_updown_asym", expr="-(TsStd(MF_LG_NET * (RET > 0), 20) - TsStd(MF_LG_NET * (RET < 0), 20))", family="asymmetry",
         rationale="Flow-vol asymmetry across up/down days.", logic_score=67),
    # ---------------------------------------- robust midrange tails (4)
    dict(name="midrange_med", expr="-((TsMax(RET, 60) + TsMin(RET, 60)) / 2 - TsMed(RET, 60))", family="robust",
         rationale="Midrange minus median: robust tail-asymmetry (new robust construct).", logic_score=69),
    dict(name="gap_midrange", expr=f"-((TsMax({_GAP}, 60) + TsMin({_GAP}, 60)) / 2 - TsMed({_GAP}, 60))", family="robust",
         rationale="Overnight tail asymmetry, robust form.", logic_score=68),
    dict(name="aggr_midrange", expr=f"-((TsMax({_AGG}, 60) + TsMin({_AGG}, 60)) / 2 - TsMed({_AGG}, 60))", family="robust",
         rationale="Aggression tail asymmetry, robust form.", logic_score=68),
    dict(name="hl_med250", expr="-TsMed(HIGH / LOW - 1, 250)", family="robust",
         rationale="Annual median range (champion at 60d; annual may decorrelate enough).", logic_score=68),
    # ---------------------------------------- idiosyncratic structures (3)
    dict(name="idio_rev", expr=f"-TsSum({_RESID}, 20)", family="idio",
         rationale="Reversal on the CSI300-residual: strips market moves from the signal.", logic_score=71),
    dict(name="idio_max", expr=f"-TsMax({_RESID}, 20)", family="idio",
         rationale="Idiosyncratic MAX effect: lottery in the residual.", logic_score=69),
    dict(name="idio_med", expr=f"TsMed({_RESID}, 60)", family="idio",
         rationale="Median idiosyncratic drift.", logic_score=68),
    # ---------------------------------------- coupling leftovers (6)
    dict(name="gapabs_turn_corr60", expr=f"-TsCorr(Abs({_GAP}), TURN_F, 60)", family="corr_band",
         rationale="Quarterly shock-chasing coupling (20d purged for low IC; band was often stronger).", logic_score=68),
    dict(name="gap_vr_corr60", expr=f"TsCorr({_GAP}, VR, 60)", family="corr_band",
         rationale="Signed-gap attention coupling, quarterly.", logic_score=67),
    dict(name="turn_gap_corr", expr=f"-TsCorr(TURN_F, {_GAP}, 20)", family="cross_corr",
         rationale="Attention responding to signed gaps.", logic_score=67),
    dict(name="mf_sm_amp_corr", expr="TsCorr(MF_SM_NET, AMP, 20)", family="flow_coupling",
         rationale="Retail flow on wide-range days: panic vs greed texture.", logic_score=67),
    dict(name="aggr_attn_corr120", expr=f"-TsCorr({_AGG}, TURN_F, 120)", family="corr_band",
         rationale="Semi-annual aggression-attention band (60d active).", logic_score=67),
    dict(name="mf_ret_corr120", expr="-TsCorr(MF_LG_NET, RET, 120)", family="flow_coupling",
         rationale="Semi-annual flow coupling (60d died at 0.76 vs 20d; 120d decorrelates further).", logic_score=67),
    # ---------------------------------------- bands (7)
    dict(name="hl_term", expr="-(TsMed(HIGH / LOW - 1, 20) / TsMed(HIGH / LOW - 1, 120))", family="volatility",
         rationale="Median-range term structure: robust vol regime (ratio breaks level corr).", logic_score=69),
    dict(name="vol_term_extreme", expr="-(TsStd(RET, 5) / TsStd(RET, 250))", family="volatility",
         rationale="Fastest/slowest vol term.", logic_score=67),
    dict(name="semivol120", expr="-(TsStd((RET + Abs(RET)) / 2, 120) - TsStd((RET - Abs(RET)) / 2, 120))", family="volatility",
         rationale="Semi-annual semivol asymmetry.", logic_score=67),
    dict(name="gap_med120", expr=f"TsMed({_GAP}, 120)", family="overnight",
         rationale="Semi-annual median overnight drift.", logic_score=67),
    dict(name="signed_vr120", expr="-TsMean(Sign(RET) * VR, 120)", family="attention",
         rationale="Semi-annual signed attention.", logic_score=66),
    dict(name="aggr_hi_vr120", expr=f"-TsMean(({_AGG}) * (VR > 1), 120)", family="conditional",
         rationale="Semi-annual conditional aggression.", logic_score=66),
    dict(name="flat_open120", expr=f"-TsCount(Abs({_GAP}) < 0.001, 120)", family="event_freq",
         rationale="Semi-annual attention-void count (60d version OOS 0.047).", logic_score=66),
    # ---------------------------------------- event bands (6)
    dict(name="maxfreq120", expr="-TsCount(RET > 2 * TsStd(RET, 60), 120)", family="lottery",
         rationale="Semi-annual lottery-day count (60d active; 250d failed OOS bar — test the middle).", logic_score=67),
    dict(name="vr_burst120", expr="-TsCount(VR > 2, 120)", family="attention",
         rationale="Semi-annual attention-burst count.", logic_score=66),
    dict(name="amp_burst120", expr="-TsCount(AMP > 2 * TsMean(AMP, 60), 120)", family="event_freq",
         rationale="Semi-annual range-burst count.", logic_score=66),
    dict(name="gapdn_freq120", expr=f"-TsCount(({_GAP}) < -2 * TsStd({_GAP}, 60), 120)", family="event_freq",
         rationale="Semi-annual gap-down habit (60d purged at 0.026 IC; longer count may clear).", logic_score=66),
    dict(name="limit_touch120", expr="-TsCount(limit_up_touch > 0.5, 120)", family="limit_board",
         rationale="Semi-annual mania count (60d strong, 250d OOS-failed; middle band).", logic_score=67),
    dict(name="aggr_min60", expr=f"TsMin({_AGG}, 60)", family="tail_event",
         rationale="Quarterly deepest capitulation close (20d active at OOS 0.059).", logic_score=66),
]

assert len(CANDIDATES) == 40, len(CANDIDATES)
