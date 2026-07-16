# canonical — composite backtest (2017–2025)

Run 2026-07-10, `python3 code/backtest_composite.py canonical` (105
individual factors). Design mirrors the label: EW oriented-rank composite
→ 10-day rebalance → top-decile long among `tradable_entry` names, t+1
vwap entry → costs 15/30bp per side. Benchmarks: EW tradable universe,
CSI300.

## Decile curve (mean 10-day return by decile, %)

−0.81, −0.01, 0.29, 0.44, 0.50, 0.54, 0.65, 0.67, 0.65, 0.63

Monotone through D8, then a mild **top-decile rolloff** (D10 0.63 < D8
0.67) — the 8-field composite discriminates the bottom strongly but its
very top names blur slightly. Most of the edge is still in avoiding D1.

## Headline (full period 2017–2025)

| metric | value |
|---|---|
| long-only gross | +14.5%/yr, Sharpe 0.68, max DD −35% |
| long-only net 15bp | **+11.0%/yr, Sharpe 0.52** |
| long excess vs own universe | **+6.8%/yr, IR 0.87** |
| long-short gross | +40.5%/yr, Sharpe 2.08 |
| long turnover / rebalance | 0.42 |
| market EW / CSI300 | +6.4% / +3.9% |

Holdout window (2024–25, note the caveat below): LO net-15bp +25.9%/yr
Sharpe 1.11; excess-mkt only +1.6% (2024–25 was a strong beta year, so
the long-only rode the market more than it out-picked).

## Reading

Essentially matches the full-vocabulary set: +6.8%/yr excess with IR
0.87 is real stock-picking alpha, positive across windows; the long-only
wrapper is beta-dominated (35% DD, 22% vol) and the LS Sharpe is a
research number (the D1 short leg — the −0.81% names — is largely
unshortable in A-shares). Same caveats as behavioral_full: paper ICs,
not tradable returns; costs at 42% turnover eat ~3.5%/yr.
