# robust_2026 — Round 4 (value family, second attempt)

**Goal:** R3 showed standalone value is orthogonal but weak at 10d. Try the forms
with the best remaining shot: value INTERACTED with the working behavioral signals,
value+quality composites, deep/contrarian value, earnings-stability quality. 13
candidates.

## Funnel

| stage | pass | note |
|---|---|---|
| candidates | 13 | — |
| S1 | 4 | **value interactions FAIL** (demeaned-rank value×behavioral all negative IC — as memory predicted); value COMPOSITES clear: value_quality_both (0.037), value_cheap_book (0.044), value_minus_mom (0.043), value_z (0.032) |
| S2 | 4 | all pass (corr −0.23 … −0.30) — orthogonal |
| S3 | 3 | value_cheap_book dup of value_quality_both |
| S4 | **2** | value_quality_both (OOS 0.039, mono 0.99, net +0.031) & value_minus_mom (OOS 0.054); value_z OOS 0.029 just misses |

Accepted → ralpha_0032 `CsRank(EP)*CsRank(CFP)`, ralpha_0033
`CsRank(EP)-CsRank(TsSum(RET,120))`.

## 2026 — UNTESTABLE (data gap), factors retired

Both value composites are robust in 2017-25 and orthogonal, but their 2026
signed-IC and net came back **NaN**: the 2026 panel has **~zero EP/CFP coverage**
(the 2026 fetch was daily + flow endpoints only; TTM fundamentals were never built
for 2026). So they cannot be shown robust-in-both, the set's defining criterion.

Both were **retired** (preserved in the retired list, re-addable). This is a data
gap, not a factor failure.

## Outcome (value-family campaign, R3+R4)

29 value/quality/size candidates → **2 cleared 2017-25** (value composites EP×CFP
and contrarian value), **0 confirmed for the set**. Two honest results:
1. **Value is genuinely orthogonal** (every value factor passes S2) — it *would*
   diversify the all-behavioral set. But it is **weak at 10d** (only composites
   clear; interactions and levels die).
2. **2026 can't be tested without fundamentals.** **Action to actually add value:**
   fetch 2026 income/balancesheet/cashflow + daily_basic, rebuild EP/CFP for 2026,
   then re-screen ralpha_0032/0033 (and likely mine at a 20d label where value has
   more punch). robust_2026 stays at **25**.
