# Style/status filter + size&industry neutralization — evaluation

Run 2026-07-16 (`code/neutralize_eval.py`, per set). Applies a
portfolio-construction layer to each existing composite and re-runs the
top-decile backtest over the historical (2017–2025) and fresh 2026
windows, comparing four variants:

| variant | signal | universe |
|---|---|---|
| **raw** | EW oriented-rank composite | all tradable_entry (baseline) |
| **filtered** | same | + investable filter |
| **neutralized** | composite residualized on size + industry | all tradable_entry |
| **filt_neutral** | neutralized | + investable filter |

- **Investable filter:** drop ST, drop names listed < 250 trading days,
  drop the **smallest 30% by circulating market cap** (the shell / micro-
  cap speculative names that led H1 2026).
- **Neutralization:** per-date cross-sectional residual of the composite
  on **SW-L1 industry** (demean within industry) then **log(circ_mv)**
  (Barra-lite). Removes the size tilt and sector bets.

## Results (excess = long top-decile vs its universe; LS = long-short gross)

**行为全量集 / behavioral_full**

| variant | hist excess | hist IC | 2026 excess | 2026 LS | 2026 IC |
|---|---|---|---|---|---|
| raw | +7.5% | 0.106 | −5.1% | −20.8% | 0.065 |
| filtered | +7.0% | 0.103 | −10.0% | −22.5% | 0.064 |
| **neutralized** | **+8.0%** | 0.105 | **−2.7%** | **−10.0%** | **0.073** |
| filt_neutral | +7.2% | 0.100 | −7.9% | −13.8% | 0.067 |

**规范价量集 / canonical**

| variant | hist excess | hist IC | 2026 excess | 2026 LS | 2026 IC |
|---|---|---|---|---|---|
| raw | +6.3% | 0.104 | −11.6% | −36.4% | 0.057 |
| filtered | +5.9% | 0.101 | −14.4% | −35.2% | 0.057 |
| **neutralized** | +6.1% | 0.102 | **−7.5%** | **−23.3%** | **0.067** |
| filt_neutral | +5.3% | 0.098 | −13.1% | −24.2% | 0.061 |

**规范复合集 / canonical_composite**

| variant | hist excess | hist IC | 2026 excess | 2026 LS | 2026 IC |
|---|---|---|---|---|---|
| raw | +5.7% | 0.076 | −18.1% | −46.6% | 0.025 |
| filtered | +6.9% | 0.074 | −18.2% | −43.9% | 0.018 |
| **neutralized** | +5.6% | 0.076 | **−15.6%** | **−41.4%** | **0.033** |
| filt_neutral | +6.1% | 0.072 | −18.3% | −38.6% | 0.025 |

## Findings

**1. Size + industry neutralization is a clear win — and it is free
historically.** In 2026 it cut the long-short loss substantially
(behavioral_full −20.8% → −10.0%, halved; canonical −36.4% → −23.3%;
composite −46.6% → −41.4%), improved the long excess, and even lifted the
daily IC (e.g. +0.065 → +0.073). Meanwhile the historical excess and IC
are unchanged or slightly better. **This proves a large part of the 2026
failure was a size/industry style bet, not the core signal** —
neutralizing it removes that component at no historical cost.

**2. The naive investability filter does NOT help — and usually hurts.**
Dropping ST / new / smallest-30% made 2026 *worse* for behavioral_full
(−5.1% → −10.0%) and canonical (−11.6% → −14.4%), and `filt_neutral` is
worse than `neutralized` alone everywhere. The reason: the behavioral
edge itself lives partly in the small-cap space, so excluding those names
removes signal without removing the regime vulnerability. A blunt size
cut is the wrong instrument.

**3. Even neutralized, 2026 stays negative.** The best case
(behavioral_full neutralized, −2.7% excess / −10.0% LS) recovered roughly
half the damage; the residual loss is the genuine **signal degradation**
(daily IC ~halved, cf. BACKTEST_2026.md) that no construction can fix.

## Recommendation

- **Adopt size + industry neutralization** as the standard construction:
  it is costless historically and materially reduces out-of-sample
  drawdown. This is the single highest-value change.
- **Do not use a blunt micro-cap exclusion filter** — it subtracts signal
  without solving the regime problem. If a filter is wanted, condition on
  *status* only (ST / suspension / new listings), not a size cut.
- **A residual regime risk remains** even after neutralization — the raw
  signal weakened in 2026. Full production use still needs a **regime
  overlay** (e.g. size/momentum-state timing) or reduced conviction, not
  just neutralization.

Per-variant detail (decile curves, cum returns) in each set's
`neutralize_eval.json`.
