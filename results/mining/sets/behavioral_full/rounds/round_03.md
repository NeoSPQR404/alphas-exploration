# Round 3 — 2026-07-07

Memory-guided: interaction template on new parent pairs, announcement-dated
earnings revisions, overnight-leg refinements, turnover shape, quality,
short-band reversal, probes.

**Funnel: 13 → S1 6 → S2 6 → S3 6 → S4 4 accepted.**
Alpha set: 24 factors, diversity eigen-entropy **0.866**. Runtime 11 min.

**Stage 4 killed factors for the first time** — exactly the "not by
chance" robustness role the prompt assigns it:

- `gapvol_x_turn` — IS/OOS IC fine (−0.025/−0.026) but only **1/3
  sub-universes**: a full-A-only effect, i.e. small-cap artifact.
- `earn_rev60` — IS 0.022/0.34 but **OOS collapsed to −0.003**, year-sign
  rate 0.57: announcement-dated earnings revision momentum is regime-dead
  post-2021.

## Accepted factors

| name | expression | dir | IS IC / ICIR | OOS22-23 IC / ICIR | IS LS | OOS LS | rank-AC 10d | PFS | decay 1/5/10/20d |
|---|---|---|---|---|---|---|---|---|---|
| alpha_0021 | `-TsCount(RET > 2·TsStd(RET,60), 60)` | + | 0.047 / 0.52 | 0.046 / 0.50 | 0.89% | 0.46% | 0.82 | 0.96 | .027/.041/.047/.053 |
| alpha_0022 | `-TsRank(TURN_F, 120)` | + | 0.051 / 0.52 | **0.052 / 0.47** | 0.77% | 0.50% | 0.37 | 0.91 | .039/.050/.051/.056 |
| alpha_0023 | `-DecayLinear(CLOSE/OPEN−1, 7)` | + | 0.041 / 0.37 | **0.052 / 0.43** | 1.11% | 0.81% | 0.01 | 0.98 | .042/.043/.044/.049 |
| alpha_0024 | `-RegBeta(TURN_F, Abs(RET), 20)` | + | **0.065 / 0.83** | 0.046 / 0.60 | 1.20% | 0.68% | 0.58 | 0.95 | .034/.051/.060/.070 |

Highlights: `volresp_beta` (alpha_0024) is the round's best — turnover
*elasticity to moves*, not volume level, ICIR 0.83 IS. `turn_selfrank`
and `rev5_decay` are OOS-stronger than IS. `rev5_decay` has ~zero 10d
rank-autocorrelation (fast factor — high turnover cost, mind it in
portfolio use).

## Rejected

- **S1 (7)** — `semivol_x_cfp` (−0.36 but |IC| 0.011 < 0.02), `exp_growth`
  (cov 0.70 usable, ICIR 0.21 weak), `gap_asym` (−0.04: asymmetry doesn't
  transfer to the overnight leg), `leg_vol_ratio` (−0.31, |IC| under),
  `turn_skew` (0.01), `accruals` (0.20), `price_nominal` (0.07).
- **S4 (2)** — `gapvol_x_turn` (sub-universe fail), `earn_rev60` (OOS
  collapse). Details above.

## Distilled

**Successful:** turnover elasticity to |ret| (volume-price family, 3
rounds productive); self-relative TS framing dodges saturated
cross-sectional families; extreme-day frequency complements magnitude;
weekly/monthly reversal bands are separable.

**Forbidden:** interaction template is *not* universal — behavioral-flow
parents only, and expect sub-universe fragility; earnings *momentum* in
any form at 10d (levels EP/CFP survive, changes don't); composing two
winners ≠ winner; turnover skew, accruals, nominal price dead.

## Notes for Round 4

- Turnover axis now 5 factors — **stop**; volume-price axis 4 — near cap.
- The set is heavy on flow/behavioral 10d signals. Two structural moves
  now likely beat another formula round: (a) extend the base with
  moneyflow / hk_hold (northbound) / margin_detail for genuinely new
  information; (b) start a combined-alpha artifact (equal-weight rank
  composite + per-family concentration report) to see set-level OOS
  behavior and where marginal diversity actually is.
- Consider a 20d-label sub-track for slower ideas (value/quality axes
  keep half-passing at 10d).
