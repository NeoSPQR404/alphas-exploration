# canonical_composite — composite backtest (2017–2025)

Run 2026-07-10, `python3 code/backtest_composite.py canonical_composite`
(119 rank-product compositions). Same design as the other sets: EW
oriented-rank composite → 10-day rebalance → top-decile long, t+1 vwap,
15/30bp costs.

## Decile curve (mean 10-day return by decile, %)

−0.71, 0.09, 0.38, 0.45, 0.53, 0.51, 0.49, 0.47, 0.52, 0.57

**Non-monotone in the middle/top** — D6–D9 flatten (~0.47–0.53) and D10
(0.57) barely tops D5 (0.53). The composite's edge lives almost entirely
in **avoiding the bottom decile** (−0.71%), not in a strong top. As a
long-only signal this is weaker than the individual sets; as a
market-neutral/ranking signal it is competitive.

## Headline (full period 2017–2025)

| metric | value |
|---|---|
| long-only gross | +12.2%/yr, Sharpe 0.52, max DD −43% |
| long-only net 15bp | +7.7%/yr, Sharpe 0.33 |
| long excess vs own universe | **+6.0%/yr, IR 0.90** |
| long-short gross | +35.2%/yr, Sharpe 1.94 |
| long turnover / rebalance | **0.55** (higher than individual sets) |
| market EW / CSI300 | +5.7% / +3.5% |

Holdout (2024–25, see caveat): LO net-15bp +29.1%/yr Sharpe 1.15;
excess-mkt +6.3%/yr IR 0.89; LS gross Sharpe 2.50.

## Reading

The composite set is a **better ranking signal than long-only product**:
excess-vs-universe IR 0.90 and holdout ICIR 0.91 are strong, but the
long-only net Sharpe (0.33 full) is the weakest of the three sets because
(a) higher turnover 0.55 costs ~5%/yr at 15bp and (b) the flat top decile
gives the long book little to grab. The non-monotone top is the honest
weakness. Best use: as an orthogonal block in a combined/hedged ranking,
not as a standalone long portfolio.
