# Turnover-reduction overlay (hysteresis / buffer bands)

Run 2026-07-21 (`code/turnover_overlay.py`). COST_ANALYSIS showed cost binds at
the composite (turnover ~0.45/rebalance). This overlay adds **hysteresis** to the
top-decile long book: a name **enters** only in the top decile (rank > 1−1/Q) but
is **held** until it falls out of a wider band (rank > 1 − buffer/Q), so names
hovering near the boundary don't churn every rebalance. Neutralized composite,
stored values, full history (2017-25), 10-day rebalance.

## robust_2026 (25 factors)

| buffer | turnover | book | gross excess | net@15bp | net@30bp |
|---|---|---|---|---|---|
| **1.0 (none)** | 0.44 | 410 | +9.9% | +6.3% | +2.9% |
| 1.5 | 0.35 | 466 | +9.5% | +6.7% | +4.0% |
| **2.0** | 0.29 | 517 | +9.5% | **+7.2%** | +4.9% |
| 2.5 | 0.25 | 565 | +9.2% | +7.1% | +5.2% |
| 3.0 | 0.22 | 610 | +8.7% | +6.9% | +5.2% |

## behavioral_full (112 factors)

| buffer | turnover | book | gross excess | net@15bp | net@30bp |
|---|---|---|---|---|---|
| **1.0 (none)** | 0.45 | 409 | +8.1% | +4.5% | +1.0% |
| 2.0 | 0.30 | 512 | +7.6% | +5.2% | +2.9% |
| 2.5 | 0.26 | 556 | +7.6% | +5.5% | +3.5% |
| 3.0 | 0.23 | 597 | +7.6% | +5.7% | +3.9% |
| 4.0 | 0.19 | 679 | +7.5% | +6.0% | +4.5% |

## Finding — nearly-free carry

The buffer is a **large, almost-free improvement**:

- **Turnover falls ~35-58%** (0.45 → 0.19-0.29) while **gross excess barely moves**
  (robust_2026 −0.4pp at buffer 2.0; behavioral_full only −0.6pp even at 4.0) —
  the signal is persistent, so held boundary names stay good.
- **Net-of-cost rises materially, most at stress cost.** robust_2026 net@30bp
  +2.0pp (2.9%→4.9%); behavioral_full net@30bp **+3.5pp (1.0%→4.5%, ~4.5×)**.
- behavioral_full's gross is so stable that wider is monotonically better; the
  more concentrated robust_2026 peaks around buffer 2.0-2.5.

## Recommendation

- **Adopt buffer ≈ 2.5 as the default book construction** (hold top-decile names
  down to the top ~25%). It is near-optimal for both sets at both cost levels
  (robust_2026 net15 +7.1% / net30 +5.2%; behavioral_full net15 +5.5% / net30
  +3.5%), roughly halving turnover.
- For a cost-sensitive / larger-AUM mandate, go wider (3.0-4.0): net@30bp keeps
  improving as turnover drops further.
- This is the single highest-value construction change after neutralization, and
  it composes with it (both applied to the same neutralized composite). Next: wire
  the buffer into `backtest_composite.py` for full Sharpe/drawdown/yearly stats of
  the buffered deployable book, and feed the ~2.5-buffer turnover into the
  capacity/impact cost model.

Graph: `figs/fig_turnover_overlay.png`. Data: each set's `turnover_overlay.json`.
