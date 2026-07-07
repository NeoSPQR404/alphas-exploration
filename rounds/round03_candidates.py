# Round 3 candidates — generated 2026-07-07 by the mining agent.
#
# Retrieve: memory (rounds 1-2) says —
#   successful: demeaned-rank interaction template (agreement is bearish);
#     leg decomposition (gap_vol OOS>IS) but not for MAX; semivol asymmetry;
#     attention duration; CFP>EP; tail beats dispersion; pv-corr high ICIR.
#   forbidden: path-shape family; beta/size/amihud at 10d; kurt; rolling-TTM
#     SUE (needs announcement-dated revisions); plain vol; whole-return
#     reversal; BP; >2 per family.
#
# Generate: interactions with new parent pairs; announcement-dated earnings
# revision (jump-detection via PctChange(ttm,1) summed 60d); overnight-leg
# refinements; extreme-day frequency; turnover distribution shape;
# accruals quality; short-band intraday reversal; nominal price probe.

CANDIDATES = [
    # ------------------------------------------------ interactions
    dict(
        name="gapvol_x_turn",
        expr="(CsRank(-TsStd(OPEN / Delay(CLOSE, 1) - 1, 20)) - 0.5) * (CsRank(-TsMean(TURN_F, 20)) - 0.5)",
        family="interaction",
        rationale="Interaction of the two strongest axes (overnight-gap "
                  "vol x turnover level) using the demeaned-rank template; "
                  "R2 found agreement between bullish signals is bearish.",
        logic_score=72,
    ),
    dict(
        name="semivol_x_cfp",
        expr="(CsRank(-(TsStd((RET + Abs(RET)) / 2, 20) - TsStd((RET - Abs(RET)) / 2, 20))) - 0.5) * (CsRank(CFP) - 0.5)",
        family="interaction",
        rationale="Risk-shape x value: does the semivol premium "
                  "concentrate in cheap or expensive names?",
        logic_score=70,
    ),
    # ------------------------------------------------ fundamental events
    dict(
        name="earn_rev60",
        expr="CsIndNeutralize(CsRank(TsSum(PctChange(n_income_attr_p_ttm, 1), 60)), IND)",
        family="fundamental_momentum",
        rationale="Announcement-dated earnings revision: PctChange(ttm,1) "
                  "is zero except on statement-update days, so the 60d sum "
                  "captures the size/sign of the latest announced revision "
                  "— the event-based fix memory demanded after rolling-TTM "
                  "SUE failed.",
        logic_score=83,
    ),
    dict(
        name="exp_growth",
        expr="CsIndNeutralize(CsRank(exp_yoy_net_profit), IND)",
        family="fundamental_momentum",
        rationale="Express-report YoY net-profit growth (PIT). Coverage "
                  "probe: express reports are sparse; S1 coverage gate "
                  "will tell us if this data is usable at all.",
        logic_score=75,
    ),
    # ------------------------------------------------ overnight/leg
    dict(
        name="gap_asym",
        expr="-(TsStd((OPEN / Delay(CLOSE, 1) - 1 + Abs(OPEN / Delay(CLOSE, 1) - 1)) / 2, 20) - TsStd((OPEN / Delay(CLOSE, 1) - 1 - Abs(OPEN / Delay(CLOSE, 1) - 1)) / 2, 20))",
        family="overnight",
        rationale="Compose two winners: up/down asymmetry applied to the "
                  "overnight-gap leg. Gap-up-dominated vol = sentiment "
                  "chasing (fade); gap-down-dominated = distress premium.",
        logic_score=74,
    ),
    dict(
        name="leg_vol_ratio",
        expr="-(TsStd(CLOSE / OPEN - 1, 20) / TsStd(OPEN / Delay(CLOSE, 1) - 1, 20))",
        family="overnight",
        rationale="Where does risk live within the day? Intraday-heavy "
                  "vol = speculative churn (fade); overnight-heavy vol = "
                  "news-driven repricing.",
        logic_score=69,
    ),
    # ------------------------------------------------ lottery/tail
    dict(
        name="max_freq",
        expr="-TsCount(RET > 2 * TsStd(RET, 60), 60)",
        family="lottery",
        rationale="Frequency (not magnitude) of extreme up days: repeat "
                  "lottery events attract retail; complements TsMax which "
                  "only sees the single best day.",
        logic_score=76,
    ),
    # ------------------------------------------------ turnover shape
    dict(
        name="turn_skew",
        expr="-TsSkew(TURN_F, 60)",
        family="turnover_shape",
        rationale="Turnover skewness: bursty attention (occasional huge "
                  "spikes) vs steady interest — distribution shape, not "
                  "level, so it may dodge the saturated level family.",
        logic_score=71,
    ),
    dict(
        name="turn_selfrank",
        expr="-TsRank(TURN_F, 120)",
        family="turnover_shape",
        rationale="Turnover in own 6-month history: self-relative "
                  "attention (hot vs own normal) instead of cross-"
                  "sectional level.",
        logic_score=73,
    ),
    # ------------------------------------------------ quality
    dict(
        name="accruals",
        expr="CsIndNeutralize(CsRank((n_cashflow_act_ttm - n_income_attr_p_ttm) / total_assets), IND)",
        family="quality",
        rationale="Cash-minus-earnings scaled by assets (inverse "
                  "accruals): earnings backed by cash are higher quality; "
                  "accrual-heavy earnings revert.",
        logic_score=81,
    ),
    # ------------------------------------------------ reversal (short band)
    dict(
        name="rev5_decay",
        expr="-DecayLinear(CLOSE / OPEN - 1, 7)",
        family="reversal",
        rationale="Weekly-band intraday-leg reversal with linear decay: "
                  "different frequency band from the accepted 20d sum; "
                  "corr gate arbitrates.",
        logic_score=72,
    ),
    # ------------------------------------------------ probes
    dict(
        name="price_nominal",
        expr="-CsRank(close)",
        family="anti_intuitive",
        rationale="Nominal (unadjusted) price level: A-share retail "
                  "prefers low-priced 'cheap' tickets — money illusion. "
                  "Uses the raw close column, not hfq.",
        logic_score=64,
    ),
    dict(
        name="volresp_beta",
        expr="-RegBeta(TURN_F, Abs(RET), 20)",
        family="volume_price",
        rationale="Turnover elasticity to |return|: names whose volume "
                  "explodes on moves are speculation-prone; low-response "
                  "names have sticky holders.",
        logic_score=70,
    ),
]
