# behavioral_full — composite backtest (2017–2025)

Run 2026-07-09, `python3 code/backtest_composite.py main`
(main registry = frozen behavioral_full membership, 105 factors).
Design mirrors the label construction exactly: EW oriented-rank
composite → rebalance every 10 trading days → top-decile long among
`tradable_entry` names, equal weight → entry/exit at t+1 vwap (the 10d
grid chains the vwap-to-vwap label legs) → costs = turnover × per-side
bp (15bp base / 30bp stress). Benchmarks: equal-weight tradable
universe ("mkt EW") and CSI300.

## The decile curve

Mean 10-day return by composite decile (%):
−0.95, 0.06, 0.29, 0.47, 0.51, 0.55, 0.61, 0.66, 0.67, 0.68

Monotone — but the striking feature is D1: the bottom decile loses
~0.95%/period while D10 makes +0.68%. **Roughly half the paper alpha
lives in the short side, which is largely unshortable in A-shares.**

## Headline numbers

| window | LO gross | LO net 15bp | LO net 30bp | LO excess-mkt (IR) | LS gross | LS net 15bp |
|---|---|---|---|---|---|---|
| full 2017–25 | +15.6%/yr, S 0.71 | **+11.8%, S 0.54** | +8.1%, S 0.37 | **+8.0%/yr, IR 1.09** | +47.1%, S 2.58 | +37.4%, S 2.05 |
| IS 2017–21 | +13.2% | +9.4% | +5.7% | +9.0%, IR 1.40 | +51.8%, S 3.30 | +41.5% |
| OOS 2022–23 | +5.3% | +2.0% | −1.2% | +8.2%, IR 1.06 | +39.1%, S 1.79 | +30.4% |
| holdout 2024–25 | +34.2%, S 1.43 | +30.1%, S 1.26 | +26.0% | +5.5%, IR 0.60 | +43.9%, S 2.13 | +34.8% |

Market EW: +6.4%/yr full period; CSI300: +3.9%. Long book turnover:
~44% per rebalance (≈11× annual one-way — the costs above price this).
Long-only max drawdown −34.6% (2018); LS max drawdown −15.9%.

## Yearly (long-only net 15bp | mkt EW | CSI300 | LS gross)

2017: −2.4 | −9.1 | +25.9 | +50.6 · 2018: −20.4 | −28.6 | −27.5 | +68.4
2019: +32.8 | +28.7 | +36.1 | +50.5 · 2020: +7.8 | +7.1 | +34.4 | +40.3
2021: +38.8 | +32.4 | −13.2 | +40.9 · 2022: −0.9 | −7.5 | −18.1 | +56.9
2023: +4.9 | +1.6 | −16.8 | +21.7 · 2024: +20.2 | +7.4 | +15.7 | +61.8
2025: +36.3 | +43.5 | +21.5 | +22.5 (%)

## Reading

- **The stock-picking alpha is real and stable**: long-book excess over
  its own universe is +8%/yr with IR ~1.1, positive in every window
  including the 2022–23 bear (where it also beat CSI300 by 27%/yr).
- **But the long-only product is beta-dominated**: 22% vol, −35% max
  drawdown, and net Sharpe 0.54 — the composite tilts small/illiquid
  and inherits full-A drawdowns. 2017/2021 divergences vs CSI300 show
  the small-cap style exposure both ways.
- **The paper LS Sharpe (2.0+ net) is not capturable**: D1 shorts are
  lottery/mania names — precisely the least borrowable stock in China.
  Index-hedged long-top-decile would land between the LO-excess and LS
  rows, minus basis and futures costs (CSI500/1000 futures discount is
  chronic).
- Costs matter at this turnover: 15bp/side eats ~3.8%/yr; 30bp ~7.5%/yr.
  A turnover-regularized rebalance (buffer bands) is the obvious next
  engineering win.
