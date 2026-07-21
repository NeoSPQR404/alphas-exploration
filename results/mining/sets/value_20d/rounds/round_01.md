# value_20d — Round 1

**Goal:** spin up a 20-day value sleeve (value is too weak at 10d). 18 core
value/quality candidates gated on `fwd_ret_20d` (HORIZON=20), size+industry
neutralized. Fresh set → S2 is vacuous.

## Funnel

| stage | pass | note |
|---|---|---|
| candidates | 18 | — |
| S1 | 8 | value clears at 20d: EP 0.039, CFP 0.037, value_combo 0.041, value_composite 0.051, value_agree 0.046, ep_rerate 0.047, value_minus_mom 0.047, quality_value 0.045 (vs ~0.03 at 10d). SP/BP/ROE/accruals/size/cheap-book below |
| S2 | 8 | fresh set (corr 0.00) |
| S3 | 3 | EP/CFP/combo/composite/quality_value all **collapse into value_agree** — value is one signal; only value_agree, ep_rerate, value_minus_mom distinct |
| S4 | **1** | ep_rerate OOS 0.010 (year-rate 0.86); value_minus_mom mono 0.43 — both fail |

Accepted → **valpha_0001** `CsRank(EP)*CsRank(CFP)` (OOS 0.046, mono 0.98, net +0.038).

## Finding

Value **clears comfortably at 20d** where it failed at 10d — the horizon was the
issue. The raw value yields are one signal (S3 collapse); the value-agreement
composite is the strongest single representative.
