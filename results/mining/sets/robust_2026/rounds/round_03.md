# robust_2026 — Round 3 (new data family: value / fundamentals)

**Goal:** mine an orthogonal data family — value/fundamentals — into the curated
set (whose 25 residents are all price/volume/flow). 16 candidates: industry-neutral
value yields (EP/CFP/SP/BP), ROE-from-yields quality, value composites, value
re-rating, valuation inverses, size.

## Funnel — 0 accepted

| stage | pass | note |
|---|---|---|
| candidates | 16 | — |
| S1 | 5 | value is weak: only ep_indneut (0.032), value_combo (0.033), value_composite (0.041), ep_rerate (0.040), quality_value (0.036) clear 0.03; CFP/SP/BP/ROE/size all below |
| S2 | 5 | **all pass easily (corr −0.26 … +0.24)** — value is genuinely orthogonal to the price/volume set (real diversification) |
| S3 | 3 | value_combo & composite dup quality_value |
| S4 | **0** | OOS IC decays below the bar: ep_indneut OOS 0.029, quality_value 0.017, ep_rerate 0.008 |

## Finding

**Value is orthogonal but too weak at the 10-day horizon.** It sails through the
correlation gate (would diversify) but fails the IC bar — IS ~0.03-0.04 decaying
to OOS 0.008-0.029. Under `GATE_ON_NEUTRALIZED` the size component is also
stripped, removing part of value's edge. Confirms the project-wide result:
fundamentals are dead at 10d. Value belongs at a longer (monthly/quarterly)
horizon, not this set's 10d label.
