# value_20d backtest + behavioral×value blend

Run 2026-07-21. (1) The value_20d composite at its native 20-day horizon, and
(2) whether adding the value sleeve improves the behavioral book.

## 1. value_20d composite @ 20d (neutralized + investable)

`code/backtest_composite.py value_20d neutral` with `cfg.HORIZON=20`.

| window | excess vs universe (ann / IR) | LS gross Sharpe | turnover |
|---|---|---|---|
| **full 2017-25** | **+3.4% / 0.42** | 1.22 | 0.44 |
| IS 2017-21 | +2.4% / 0.35 | 1.12 | 0.45 |
| OOS 2022-23 | +9.8% / 0.99 | 1.98 | 0.43 |
| holdout 2024-25 | −0.5% / −0.06 | 0.80 | 0.42 |

Decile monotone (`−0.41 … +0.98` %/20d), LS gross **positive every year**
(+2%…+31%). A modest but real value book — strongest in 2022-23 (value's good
run), flat in 2024-25. Long-only gross +10.9%/yr (Sharpe 0.57), net@15bp +9.1%.

## 2. Behavioral × value blend — does value diversify?

Neutralized behavioral composite **B** (behavioral_full, 112) blended with the
value composite **V** (value_20d, 4): `blend = (1−wV)·rank(B) + wV·rank(V)`,
swept over the two horizons on full history.

**corr(B, V) = +0.386 cross-sectional; IC-series corr = +0.71.** Once both are
size+industry neutralized, value and behavioral share substantial common
variance and work in the **same regimes** — limited timing diversification.

| horizon | wV | mean IC | ICIR | excess ann |
|---|---|---|---|---|
| 10d | **0.0** | 0.105 | **0.85** | **+8.0%** |
| 10d | 0.2 | 0.106 | 0.83 | +6.3% |
| 10d | 0.5 | 0.098 | 0.75 | +5.3% |
| 10d | 1.0 | 0.061 | 0.52 | +4.8% |
| 20d | **0.0** | 0.119 | **0.94** | **+5.2%** |
| 20d | 0.2 | 0.120 | 0.91 | +3.8% |
| 20d | 0.5 | 0.111 | 0.81 | +3.5% |
| 20d | 1.0 | 0.071 | 0.56 | +3.3% |

**Every positive value weight lowers ICIR and long-excess** at both horizons. The
blend's mean IC ticks up trivially at wV=0.2 (0.105→0.106 / 0.119→0.120) but
risk-adjusted quality and returns both decline monotonically.

## Conclusion — the diversifier thesis did not pan out

- **Value does not diversify the behavioral book.** After neutralization the two
  are 0.39 cross-sectionally and 0.71 in IC-timing correlated; value's standalone
  Sharpe is lower; so blending a lower-Sharpe, highly-timing-correlated sleeve
  dilutes rather than diversifies. **Behavioral-alone (wV=0) is the best
  risk-adjusted config at both horizons.**
- Side-finding: the **behavioral book is *cleaner* at 20d** (ICIR 0.94 vs 0.85 at
  10d), but 10d extracts more tradable excess (8.0% vs 5.2%) — behavioral alpha is
  fast/reversal-driven.
- Value remains a legitimate standalone book (§1) for an explicitly value-tilted
  mandate, and could still help in a genuine value regime (both were weak in
  2026). But as a bolt-on diversifier to the behavioral book, it does not earn its
  weight. A real diversifier would need **low IC-timing correlation**, which this
  value sleeve does not provide.

Graph: `figs/fig_blend.png`. Data: `blend_behavioral_value.json`,
`sets/value_20d/backtest_neutral.json`.
