# Round 2 candidates — generated 2026-07-07 by the mining agent.
#
# Retrieve: experience memory (round 1) says —
#   successful: leg decomposition (intraday=reversal, overnight=momentum);
#     tail/lottery > plain vol; price-volume agreement corr; turnover axis
#     strong but NEAR SATURATION; within-industry EP thin but alive.
#   forbidden: sign-only reversal; BP; standalone vol/amp/ivol variants;
#     whole-return 1-month reversal; >2 candidates per family per round.
#
# Generate: push successful patterns into NEW structures (legs applied to
# vol and MAX; pure interaction terms; trend residuals), probe untouched
# axes (beta, size shape, fundamentals momentum, illiquidity), cap every
# family at 2.

CANDIDATES = [
    # ------------------------------------------------ overnight/leg family
    dict(
        name="overnight_mom60",
        expr="TsSum(OPEN / Delay(CLOSE, 1) - 1, 60)",
        family="overnight",
        rationale="R1 found overnight gaps are momentum (sign flip); "
                  "express it directly at quarterly scale, longer than the "
                  "accepted 20d version to reduce overlap.",
        logic_score=78,
    ),
    dict(
        name="gap_vol",
        expr="-TsStd(OPEN / Delay(CLOSE, 1) - 1, 20)",
        family="overnight",
        rationale="Leg-decomposed volatility: overnight-gap vol isolates "
                  "news/sentiment risk; calm-overnight names should carry "
                  "the low-vol premium more purely than whole-day vol.",
        logic_score=74,
    ),
    # ------------------------------------------------ lottery/tail
    dict(
        name="max_intraday",
        expr="-TsMax(CLOSE / OPEN - 1, 20)",
        family="lottery",
        rationale="Leg-decomposed MAX effect: the lottery chase happens "
                  "intraday in A-shares; strip the overnight component "
                  "from the best-day signal.",
        logic_score=80,
    ),
    dict(
        name="kurt",
        expr="-TsKurt(RET, 60)",
        family="lottery",
        rationale="Tail thickness: fat-tailed return distributions are "
                  "lottery-like; memory says tail shape beats dispersion.",
        logic_score=72,
    ),
    # ------------------------------------------------ volatility structure
    dict(
        name="vol_of_vol",
        expr="-TsStd(TsStd(RET, 5), 20)",
        family="volatility",
        rationale="Vol-of-vol: uncertainty about risk itself; structurally "
                  "different from level vol per memory guidance.",
        logic_score=73,
    ),
    dict(
        name="updown_asym",
        expr="-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))",
        family="volatility",
        rationale="Up/down semivol asymmetry: upside-dominated vol = "
                  "lottery payoffs (fade), downside-dominated vol = "
                  "distress premium (hold).",
        logic_score=76,
    ),
    # ------------------------------------------------ volume-price
    dict(
        name="turn_amp_corr",
        expr="-TsCorr(TURN_F, AMP, 20)",
        family="volume_price",
        rationale="Speculation co-movement: turnover chasing intraday "
                  "range marks retail frenzy; memory says price-volume "
                  "interactions carry the best ICIR.",
        logic_score=74,
    ),
    dict(
        name="ret_autocorr",
        expr="-TsCorr(RET, Delay(RET, 1), 20)",
        family="volume_price",
        rationale="Return autocorrelation as a characteristic: positively "
                  "autocorrelated (trending) names are crowded momentum "
                  "chasing; anti-intuitive probe.",
        logic_score=65,
    ),
    # ------------------------------------------------ liquidity (new axis)
    dict(
        name="amihud",
        expr="Log(TsMean(Abs(RET) / AMOUNT, 20))",
        family="liquidity",
        rationale="Amihud illiquidity: price impact per unit traded; "
                  "illiquid names earn a premium. Distinct construct from "
                  "the (near-saturated) turnover family — let the corr "
                  "gate arbitrate.",
        logic_score=84,
    ),
    dict(
        name="turn_dur",
        expr="CsRank(HighDay(TURN_F, 60))",
        family="liquidity",
        rationale="Days since the turnover peak: fresh attention spikes "
                  "mark tops; long-faded attention marks neglect premium.",
        logic_score=70,
    ),
    # ------------------------------------------------ pure interactions
    dict(
        name="rev_x_lowturn",
        expr="(CsRank(-TsSum(CLOSE / OPEN - 1, 20)) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
        family="interaction",
        rationale="Demeaned-rank interaction (low corr with both parents "
                  "by construction): is intraday reversal stronger among "
                  "low-turnover neglected names?",
        logic_score=71,
    ),
    dict(
        name="max_x_spike",
        expr="(CsRank(-TsMax(RET, 20)) - 0.5) * (CsRank(-(TsMean(TURN_F, 5) / TsMean(TURN_F, 60))) - 0.5)",
        family="interaction",
        rationale="Lottery conditioned on attention: MAX effect should be "
                  "strongest where turnover just spiked (retail arrived).",
        logic_score=71,
    ),
    # ------------------------------------------------ fundamentals
    dict(
        name="sue_ttm",
        expr="CsIndNeutralize(CsRank(PctChange(n_income_attr_p_ttm, 120)), IND)",
        family="fundamental_momentum",
        rationale="TTM earnings momentum (~2 quarters), PIT column, "
                  "industry-neutral: post-earnings drift at the pace "
                  "fundamentals actually update.",
        logic_score=82,
    ),
    dict(
        name="cfp_ind",
        expr="CsIndNeutralize(CsRank(CFP), IND)",
        family="value",
        rationale="Operating-cash-flow yield, industry-neutral: harder to "
                  "manage than earnings; memory says EP survived where BP "
                  "died, so test the cash version of E.",
        logic_score=80,
    ),
    # ------------------------------------------------ beta
    dict(
        name="low_beta",
        expr="-RegBeta(RET, BENCH_RET, 60)",
        family="beta",
        rationale="Betting-against-beta: leverage-constrained investors "
                  "overpay for high-beta names; untested axis in the set.",
        logic_score=79,
    ),
    # ------------------------------------------------ trend structure
    dict(
        name="resi_trend",
        expr="-TsResi(Log(CLOSE), 20)",
        family="trend_structure",
        rationale="Deviation from own 20d log-price trend: stretch above "
                  "trend reverts — reversal measured against trend, not "
                  "against level (whole-return reversal is forbidden).",
        logic_score=73,
    ),
    dict(
        name="rsq_choppy",
        expr="-TsRSquare(Log(CLOSE), 20)",
        family="trend_structure",
        rationale="Trendiness penalty: high R² price paths are momentum "
                  "crowding; choppy paths are underpriced. Anti-intuitive "
                  "probe of path shape.",
        logic_score=66,
    ),
    # ------------------------------------------------ size shape
    dict(
        name="size_nl",
        expr="-Abs(CsZscore(Log(CMV)))",
        family="size",
        rationale="Nonlinear size: mid-caps over both extremes (mega-cap "
                  "drag, micro-cap shell risk post-2017 delisting reform).",
        logic_score=68,
    ),
    # ------------------------------------------------ microstructure
    dict(
        name="close_pos",
        expr="-TsMean((CLOSE - LOW) / (HIGH - LOW), 10)",
        family="anti_intuitive",
        rationale="Average close position within the daily range: "
                  "persistent strong closes = late-day aggression that "
                  "fades (cousin of the accepted close/vwap premium — "
                  "corr gate arbitrates).",
        logic_score=67,
    ),
]
