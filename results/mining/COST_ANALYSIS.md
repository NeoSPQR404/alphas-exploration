# Turnover / cost-aware scoring

Run 2026-07-20 (`code/mining/alphaseval.py::cost_aware`, wired into the
evaluation gates and stored metrics). Every factor now carries a
**cost_aware_score**: its top-decile long-excess-vs-universe, net of the
factor's OWN decile-membership turnover, at 15 and 30 bp per side. A-share
short legs are effectively untradable, so long-excess-net is the headline
tradable number; LS-net is reported for completeness.

Cost model matches the composite backtest: per-rebalance drag =
turnover × 2 (round-trip) × cost, subtracted before annualizing. Horizon 10d,
top decile, IS+OOS window (2017–2023). Signals are size+industry neutralized
(the production construction).

## Single factors are turnover-heavy and mostly untradable *standalone*

Scored 30 behavioral_full factors (neutralized, oriented):

| metric | median | range |
|---|---|---|
| gross long-excess (ann) | +3.7% | −2.1% … +7.3% |
| **net @15bp (ann)** | **−1.6%** | −7.6% … +3.1% |
| top-decile turnover / rebalance | 0.65 | 0.36 … 0.88 |

A single-factor `net@15bp > 0` gate would **reject 21 of 30 (70%)** of the
existing corpus. Individual short-horizon behavioral factors churn ~65% of
the top decile every 10 days; their modest gross edge is eaten by costs when
traded alone.

## …but the COMPOSITE is strongly tradable

The factors deploy as an equal-weight rank composite. Averaging cuts turnover
and lifts gross edge, so net-of-cost flips positive:

| set | gross exc | **net @15bp** | net @30bp | turnover | LS gross | LS net@15bp |
|---|---|---|---|---|---|---|
| **behavioral_full** | +9.0% | **+5.1%** | +1.4% | 0.48 | +48.3% | +38.1% |
| canonical | +7.6% | +4.0% | +0.6% | 0.45 | +43.6% | +34.7% |
| canonical_composite | +6.1% | +1.7% | −2.5% | 0.57 | +33.1% | +23.3% |

Diversification does two things at once for behavioral_full: gross excess
rises **3.7% → 9.0%** and turnover falls **0.65 → 0.48**, so net@15bp goes
from a −1.6% single-factor median to **+5.1%** at the composite.

## Findings

1. **Cost-awareness binds at the composite (deployment) level, not per
   factor.** A hard per-factor net-cost gate is miscalibrated — it would gut
   valuable turnover-heavy factors that are only meant to be averaged. So
   `GATE_ON_NET_COST` is **off by default**; the `cost_aware_score` is
   computed, stored, and printed for every factor as a *reported* quality
   signal (useful for preferring lower-turnover candidates), not a reject.
2. **behavioral_full / canonical composites are comfortably tradable** at
   15bp (+5.1% / +4.0% long-excess net) and still positive at 30bp.
3. **canonical_composite is the marginal one:** +1.7% net@15bp but **−2.5%
   at 30bp** — its higher turnover (0.57) and lower gross edge make it
   cost-fragile. Do not trade it standalone at stress costs.

## Recommendation

- **Keep the per-factor gate off**; use `cost_aware_score` to *rank/prefer*
  lower-turnover factors during generation, not to reject.
- **The real cost lever is composite turnover**, not factor selection. Next
  step (highest value): a turnover-reduction overlay on the composite —
  hysteresis / buffer bands on decile membership, or a longer rebalance
  horizon — targeted first at canonical_composite, which loses money at 30bp.
- Re-score with `python3 code/backtest_composite.py <set> neutral` (composite
  net columns) and the stored per-factor `cost_aware` metrics.
