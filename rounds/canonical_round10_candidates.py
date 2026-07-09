# Canonical set — Round 10 (19 candidates) — generated 2026-07-09.
#
# INDIVIDUAL factors only (user directive): no demeaned-rank products or
# any composition of existing factors — every candidate is a single
# expression over raw fields. The 26 composition factors were split out
# to sets/canonical_composite/ before this round; the set is 79.
#
# Sources: (a) recorded near-misses re-tried at jittered bands
# (vwap_gap_med 0.032/ICIR 0.29 @60d; zeroret250 0.035/0.30;
# updn_freq_hl 0.027/0.30; ovnmom20 0.028; aggr_sum60 0.028;
# hl_med_dev 0.026), (b) novel single-expression constructs: asymmetric
# price impact (Amihud by direction), overnight-share asymmetry,
# range-regime slope/persistence, attention-weighted volatility.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_ILLIQ = "Abs(RET) / AMOUNT"

CANDIDATES = [
    # ---------------- novel single-expression constructs (9)
    dict(name="c_amihud_updown", expr=f"-(TsMean(({_ILLIQ}) * (RET > 0), 20) - TsMean(({_ILLIQ}) * (RET < 0), 20))",
         family="liquidity", rationale="Asymmetric price impact: up-day vs down-day Amihud — one-sided liquidity is a distress/mania marker.", logic_score=73),
    dict(name="c_amihud_updown60", expr=f"-(TsMean(({_ILLIQ}) * (RET > 0), 60) - TsMean(({_ILLIQ}) * (RET < 0), 60))",
         family="liquidity", rationale="Quarterly band of asymmetric impact.", logic_score=71),
    dict(name="c_ovnshare_updown", expr=f"-(TsMean((Abs({_GAP}) / ({_HL})) * (RET > 0), 20) - TsMean((Abs({_GAP}) / ({_HL})) * (RET < 0), 20))",
         family="overnight", rationale="Overnight share of range on up vs down days: where price discovery happens by direction.", logic_score=70),
    dict(name="c_hl_slope", expr=f"-TsSlope({_HL}, 20)", family="volatility",
         rationale="Range-regime trend: expanding vs contracting daily ranges (path test on range, never tried).", logic_score=69),
    dict(name="c_hl_persist", expr=f"-TsCorr({_HL}, Delay({_HL}, 1), 20)", family="volatility",
         rationale="Range persistence: sticky vs episodic volatility regimes.", logic_score=68),
    dict(name="c_awvol", expr=f"-TsStd(RET * ({_NVOL}), 20)", family="volatility",
         rationale="Attention-weighted volatility: moves that happened while the crowd watched count more.", logic_score=70),
    dict(name="c_awmove", expr=f"-TsMean(Abs(RET) * ({_NVOL}), 20)", family="volatility",
         rationale="Attention-weighted absolute movement.", logic_score=68),
    dict(name="c_att_span", expr=f"-TsCount({_NVOL} > 1, 20)", family="volume",
         rationale="Breadth of attention: share of above-normal-volume days (span, not burst).", logic_score=68),
    dict(name="c_intr_share", expr=f"-TsMean(Abs({_ID}) / ({_HL}), 20)", family="volatility",
         rationale="Intraday displacement share of range: trend-within-day vs churn-within-day.", logic_score=67),
    # ---------------- near-miss band jitters (7)
    dict(name="c_vwapgap_med40", expr="TsMed(OPEN / Delay(VWAP, 1) - 1, 40)", family="overnight",
         rationale="VWAP-anchored median gap at 40d (60d was 0.032 IC / ICIR 0.29 — just under both bars).", logic_score=68),
    dict(name="c_zeroret180", expr="-TsCount(Abs(RET) < 0.001, 180)", family="liquidity",
         rationale="Zero-return habit at 180d (250d was 0.035/0.30 with coverage 0.88; 180 keeps coverage).", logic_score=68),
    dict(name="c_ovnmom30", expr=f"TsSum({_GAP}, 30)", family="overnight",
         rationale="Overnight momentum at 30d (20d IC 0.028 just under; 60d resident).", logic_score=66),
    dict(name="c_aggr_sum90", expr=f"-TsSum({_AGG}, 90)", family="aggression",
         rationale="Cumulative aggression at 90d (60d was 0.028/0.24).", logic_score=66),
    dict(name="c_updn_freq_hl90", expr=f"-(TsCount(({_HL}) > 2 * TsMean({_HL}, 60), 90) - TsCount(({_HL}) < 0.5 * TsMean({_HL}, 60), 90))",
         family="event", rationale="Burst-minus-collapse balance at 90d (60d was 0.027/0.30).", logic_score=66),
    dict(name="c_hl_med_dev_sm", expr=f"-TsMean(({_HL}) / TsMed({_HL}, 60) - 1, 10)", family="volatility",
         rationale="Smoothed robust range deviation (daily version was 0.026 — smoothing may lift IC above the bar).", logic_score=67),
    dict(name="c_gapdn_freq120", expr=f"-TsCount(({_GAP}) < -2 * TsStd({_GAP}, 60), 120)", family="overnight",
         rationale="Semi-annual gap-down habit (never tested in canonical; gapdn_freq60 accepted in main pre-0.03).", logic_score=66),
    # ---------------- robust variants (3)
    dict(name="c_gap_abs_med", expr=f"-TsMed(Abs({_GAP}), 60)", family="overnight",
         rationale="Median absolute gap: robust overnight risk (corr vs gapvol arbitrates).", logic_score=67),
    dict(name="c_vwapgap_vol", expr="-TsStd(OPEN / Delay(VWAP, 1) - 1, 20)", family="overnight",
         rationale="VWAP-anchored gap volatility.", logic_score=66),
    dict(name="c_idmed5", expr=f"TsMed({_ID}, 5)", family="reversal",
         rationale="Weekly median intraday drift (20/60 resident; fastest robust band).", logic_score=66),
]

assert len(CANDIDATES) == 19, len(CANDIDATES)
