# Canonical set — Round 2 (32 candidates) — generated 2026-07-08.
#
# Retrieve (canonical memory): transfer worked 34/40; RegBeta on
# self-normalized volume is dead (corr couplings fine); conditionals and
# masked-asym translate with VOLUME conditions. This round: novel
# canonical-only constructs — nvol couplings, deeper conditional/asym
# tiers, volume-event structures — not straight re-expressions.

SET_NAME = "canonical"
FIELD_WHITELIST = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME", "AMOUNT",
                   "VWAP", "RET"]

_GAP = "OPEN / Delay(CLOSE, 1) - 1"
_ID = "CLOSE / OPEN - 1"
_AGG = "CLOSE / VWAP - 1"
_HL = "HIGH / LOW - 1"
_NVOL = "VOLUME / TsMean(VOLUME, 60)"
_NAMT = "AMOUNT / TsMean(AMOUNT, 60)"

CANDIDATES = [
    # ------------------------------------------------ nvol couplings (10)
    dict(name="c_hl_nvol_corr", expr=f"-TsCorr({_HL}, {_NVOL}, 20)", family="coupling",
         rationale="Range-attention coupling (attn-risk analog, canonical).", logic_score=72),
    dict(name="c_gap_nvol_corr", expr=f"-TsCorr(Abs({_GAP}), {_NVOL}, 20)", family="coupling",
         rationale="Overnight-shock chasing crowd.", logic_score=70),
    dict(name="c_aggr_nvol_corr", expr=f"-TsCorr({_AGG}, {_NVOL}, 20)", family="coupling",
         rationale="Late-day aggression arriving with attention (main-set analog accepted).", logic_score=72),
    dict(name="c_ret_namt_corr", expr=f"-TsCorr(RET, {_NAMT}, 20)", family="coupling",
         rationale="Return-attention coupling in dollar terms.", logic_score=70),
    dict(name="c_id_nvol_corr", expr=f"-TsCorr({_ID}, {_NVOL}, 20)", family="coupling",
         rationale="Intraday leg vs attention.", logic_score=69),
    dict(name="c_nvol_std_corr", expr=f"-TsCorr({_NVOL}, TsStd(RET, 5), 20)", family="coupling",
         rationale="Attention-risk coupling (main ICIR 0.61 as turnover).", logic_score=72),
    dict(name="c_nvol_std_corr60", expr=f"-TsCorr({_NVOL}, TsStd(RET, 5), 60)", family="coupling",
         rationale="Quarterly attention-risk band.", logic_score=70),
    dict(name="c_ret_hl_corr60", expr=f"-TsCorr(RET, {_HL}, 60)", family="coupling",
         rationale="Return-range coupling, quarterly.", logic_score=70),
    dict(name="c_ret_hl_corr120", expr=f"-TsCorr(RET, {_HL}, 120)", family="coupling",
         rationale="Return-range coupling, semi-annual (main OOS 0.067).", logic_score=70),
    dict(name="c_lagchase60", expr=f"-TsCorr({_NVOL}, Delay(RET, 1), 60)", family="coupling",
         rationale="Quarterly lagged chase.", logic_score=70),
    # ------------------------------------------------ bands / self-ranks (6)
    dict(name="c_lagchase120", expr=f"-TsCorr({_NVOL}, Delay(RET, 1), 120)", family="coupling",
         rationale="Semi-annual lagged chase.", logic_score=69),
    dict(name="c_gapvol_sr", expr=f"-TsRank(TsStd({_GAP}, 20), 120)", family="overnight",
         rationale="Overnight risk vs own history.", logic_score=71),
    dict(name="c_idmed60", expr=f"TsMed({_ID}, 60)", family="reversal",
         rationale="Quarterly median intraday drift (reversal direction).", logic_score=70),
    dict(name="c_gapmed120", expr=f"TsMed({_GAP}, 120)", family="overnight",
         rationale="Semi-annual median overnight drift.", logic_score=69),
    dict(name="c_volmed_term", expr="-(TsMed(VOLUME, 20) / TsMed(VOLUME, 120))", family="volume",
         rationale="Median-volume term ratio: robust attention regime.", logic_score=69),
    dict(name="c_hlmed20", expr=f"-TsMed({_HL}, 20)", family="volatility",
         rationale="Fast median range (no turnover family here to collide with).", logic_score=69),
    # ------------------------------------------------ conditionals / asym (10)
    dict(name="c_aggr_hi_nvol", expr=f"-TsMean(({_AGG}) * ({_NVOL} > 1), 20)", family="conditional",
         rationale="Aggression on high-attention days (main analog ICIR 0.69).", logic_score=73),
    dict(name="c_aggr_hi_nvol60", expr=f"-TsMean(({_AGG}) * ({_NVOL} > 1), 60)", family="conditional",
         rationale="Quarterly band of the above.", logic_score=71),
    dict(name="c_ret_on_hivol120", expr="-TsSum(RET * (VOLUME > TsMean(VOLUME, 120)), 120)", family="conditional",
         rationale="Semi-annual returns on high-volume days (main OOS 0.083).", logic_score=73),
    dict(name="c_id_on_hivol120", expr=f"-TsSum(({_ID}) * (VOLUME > TsMean(VOLUME, 120)), 120)", family="conditional",
         rationale="Semi-annual intraday leg on high-volume days.", logic_score=70),
    dict(name="c_attn_up_cnt", expr=f"-TsCount((({_NVOL} > 1) * (RET > 0)) > 0.5, 60)", family="conditional",
         rationale="Attention-up-day count.", logic_score=70),
    dict(name="c_attn_up_cnt120", expr=f"-TsCount((({_NVOL} > 1) * (RET > 0)) > 0.5, 120)", family="conditional",
         rationale="Semi-annual attention-up count.", logic_score=69),
    dict(name="c_signed_nvol", expr=f"-TsMean(Sign(RET) * ({_NVOL}), 20)", family="conditional",
         rationale="Direction-weighted attention (signed_attn analog).", logic_score=71),
    dict(name="c_signed_nvol120", expr=f"-TsMean(Sign(RET) * ({_NVOL}), 120)", family="conditional",
         rationale="Semi-annual signed attention.", logic_score=69),
    dict(name="c_vol_updown60", expr=f"-(TsStd(({_NVOL}) * (RET > 0), 60) - TsStd(({_NVOL}) * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly volume asymmetry.", logic_score=70),
    dict(name="c_hl_updown60", expr=f"-(TsStd(({_HL}) * (RET > 0), 60) - TsStd(({_HL}) * (RET < 0), 60))",
         family="asymmetry", rationale="Quarterly range asymmetry (20d version ICIR 0.94 as amp in main).", logic_score=72),
    # ------------------------------------------------ volume events (4)
    dict(name="c_nvol_burst", expr=f"-TsCount({_NVOL} > 2, 60)", family="volume",
         rationale="Attention-burst days (vr_burst analog).", logic_score=71),
    dict(name="c_nvol_burst120", expr=f"-TsCount({_NVOL} > 2, 120)", family="volume",
         rationale="Semi-annual attention-burst habit.", logic_score=69),
    dict(name="c_amt_burst", expr="-TsCount(Log(AMOUNT) > TsMean(Log(AMOUNT), 60) + 2 * TsStd(Log(AMOUNT), 60), 60)",
         family="volume", rationale="Dollar-volume burst frequency (accepted in main).", logic_score=69),
    dict(name="c_reject_freq", expr=f"-TsCount((HIGH - (OPEN + CLOSE + Abs(OPEN - CLOSE)) / 2) / (HIGH - LOW) > 0.5, 60)",
         family="candle", rationale="Rejection-day frequency (upper shadow dominating the bar): event-framing of the dead candle levels.", logic_score=68),
    # ------------------------------------------------ probes (2)
    dict(name="c_gap_hl_corr", expr=f"-TsCorr(Abs({_GAP}), {_HL}, 20)", family="coupling",
         rationale="Overnight shock coupled with day range: news digestion texture.", logic_score=67),
    dict(name="c_aggr_min60", expr=f"TsMin({_AGG}, 60)", family="aggression",
         rationale="Quarterly deepest capitulation close (main OOS 0.063).", logic_score=69),
]

assert len(CANDIDATES) == 32, len(CANDIDATES)
