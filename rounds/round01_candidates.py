# Round 1 candidates — generated 2026-07-06 by the mining agent.
# Retrieve step: experience memory is empty (first round), so this batch
# spans a wide spread of families to seed both pattern buckets:
# reversal, turnover/liquidity, volume-price interaction, volatility
# structure, lottery/tail, value, overnight/intraday split, trend
# structure, and deliberately anti-intuitive probes.
#
# logic_score: agent's 50-100 rating of financial-logic coherence
# (AlphaEval "Logic" dimension). Direction is auto-detected by the
# pipeline; rationales state the expected sign.

CANDIDATES = [
    # ---------------------------------------------------------- reversal
    dict(
        name="rev20",
        expr="-PctChange(CLOSE, 20)",
        family="reversal",
        rationale="Classic 1-month price reversal: A-share retail flow "
                  "overreacts; last month's losers outperform.",
        logic_score=85,
    ),
    dict(
        name="rev20_ind",
        expr="CsIndNeutralize(-PctChange(CLOSE, 20), IND)",
        family="reversal",
        rationale="Same reversal but industry-demeaned, removing sector "
                  "momentum contamination.",
        logic_score=88,
    ),
    dict(
        name="rev_path",
        expr="-TsSum(Sign(RET), 20)",
        family="reversal",
        rationale="Path-based reversal: count of up-days minus down-days; "
                  "streaky gainers revert regardless of magnitude.",
        logic_score=75,
    ),
    # ---------------------------------------------------- turnover/liquidity
    dict(
        name="turn_low",
        expr="-TsMean(TURN_F, 20)",
        family="turnover",
        rationale="Low-turnover premium: neglected, low-churn names earn "
                  "more; hot high-turnover names are crowded and overpriced.",
        logic_score=85,
    ),
    dict(
        name="turn_spike",
        expr="-(TsMean(TURN_F, 5) / TsMean(TURN_F, 60))",
        family="turnover",
        rationale="Relative turnover spike: recent churn vs own baseline; "
                  "attention spikes mark local tops.",
        logic_score=80,
    ),
    dict(
        name="turn_cv",
        expr="-(TsStd(TURN_F, 20) / TsMean(TURN_F, 20))",
        family="turnover",
        rationale="Turnover coefficient of variation: erratic trading "
                  "interest signals speculative churn; stable interest is "
                  "healthier.",
        logic_score=70,
    ),
    # ---------------------------------------------------- volume-price
    dict(
        name="pv_corr",
        expr="-TsCorr(CsRank(CLOSE), CsRank(VOLUME), 10)",
        family="volume_price",
        rationale="Price-volume agreement: rallies confirmed by volume are "
                  "crowded retail chases in A-shares; fade them.",
        logic_score=72,
    ),
    dict(
        name="pv_corr_ts",
        expr="-TsCorr(TsRank(CLOSE, 10), TsRank(VOLUME, 10), 10)",
        family="volume_price",
        rationale="Time-series variant of price-volume agreement using own "
                  "history ranks instead of cross-sectional ranks.",
        logic_score=72,
    ),
    dict(
        name="smart_flow",
        expr="-TsCorr(TURN_F, RET, 20)",
        family="volume_price",
        rationale="Smart-money proxy: if turnover concentrates on up-days, "
                  "retail is chasing; institutions accumulate quietly on "
                  "down days.",
        logic_score=74,
    ),
    # ---------------------------------------------------- volatility structure
    dict(
        name="lowvol",
        expr="-TsStd(RET, 20)",
        family="volatility",
        rationale="Low-volatility anomaly: high-vol names are lottery-like "
                  "and overpriced by leverage-constrained retail.",
        logic_score=82,
    ),
    dict(
        name="ivol",
        expr="-TsStd(RegResi(RET, BENCH_RET, 60), 60)",
        family="volatility",
        rationale="Idiosyncratic vol vs CSI300: purer mispricing signal "
                  "than raw vol (Ang et al.), strong in A-shares.",
        logic_score=84,
    ),
    dict(
        name="amp_low",
        expr="-TsMean(AMP, 20)",
        family="volatility",
        rationale="Average daily amplitude: intraday range proxies retail "
                  "speculation intensity; calm names outperform.",
        logic_score=76,
    ),
    # ---------------------------------------------------- lottery / tail
    dict(
        name="max_eff",
        expr="-TsMax(RET, 20)",
        family="lottery",
        rationale="MAX effect (Bali et al.): the best single day in the "
                  "past month proxies lottery demand; overpriced afterwards.",
        logic_score=83,
    ),
    dict(
        name="skew",
        expr="-TsSkew(RET, 60)",
        family="lottery",
        rationale="Return skewness: right-skewed lottery payoffs are "
                  "overvalued; negative-skew names carry a premium.",
        logic_score=78,
    ),
    # ---------------------------------------------------- value
    dict(
        name="ep_ind",
        expr="CsIndNeutralize(CsRank(EP), IND)",
        family="value",
        rationale="Earnings yield (PIT TTM net income / market cap), "
                  "ranked and industry-neutralized; within-sector cheapness.",
        logic_score=86,
    ),
    dict(
        name="bp_ind",
        expr="CsIndNeutralize(CsRank(BP), IND)",
        family="value",
        rationale="Book-to-price, industry-neutralized: balance-sheet "
                  "value tilt orthogonal to sector composition.",
        logic_score=82,
    ),
    # ---------------------------------------------------- overnight/intraday
    dict(
        name="overnight",
        expr="-TsSum(OPEN / Delay(CLOSE, 1) - 1, 20)",
        family="overnight",
        rationale="Cumulative overnight gap: A-share overnight returns are "
                  "retail-sentiment-driven and revert; persistent gappers "
                  "underperform.",
        logic_score=80,
    ),
    dict(
        name="intraday_rev",
        expr="-TsSum(CLOSE / OPEN - 1, 20)",
        family="overnight",
        rationale="Cumulative intraday return: the intraday leg carries "
                  "the speculative push that mean-reverts at monthly scale.",
        logic_score=74,
    ),
    # ---------------------------------------------------- trend structure
    dict(
        name="highday",
        expr="CsRank(HighDay(CLOSE, 60))",
        family="trend_structure",
        rationale="Days since the 60d high: fresher highs mean crowded "
                  "chasing (reversal risk); stale highs mean capitulation "
                  "has run its course.",
        logic_score=68,
    ),
    # ---------------------------------------------------- anti-intuitive probes
    dict(
        name="vwap_dev",
        expr="-TsMean(CLOSE / VWAP - 1, 10)",
        family="anti_intuitive",
        rationale="Close-vs-VWAP persistent premium: closing auctions "
                  "pushed above the day's average price signal aggressive "
                  "late buying that fades. Probe: microstructure, not "
                  "standard intuition.",
        logic_score=65,
    ),
]
