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

## 2026 — tested (after a stale-cache fix): value fails, retired

First pass returned **NaN** on 2026 — but the data was there. Root cause was a
**stale wide-frame cache**: when 2026 was added, the daily fields
(`close_hfq`/`circ_mv`) rebuilt through 2026-07, but the fundamental inputs
(`total_mv`, `n_income_attr_p_ttm`, `revenue_ttm`, `pb`, …) stayed frozen at
2025-12-31. EP uses `total_mv` (stale) → NaN in 2026. **No fetch needed** — the
2026 base already had the fundamentals (98% coverage). Cleared the 13 stale caches
(fundamentals, valuations, non-10d labels, bench_close); EP/CFP/BP/SP now cover
2026 (~5170 names/date).

Re-screened with proper 2026 data:

| factor | 2026 IC | 2026 long-excess net@15bp | turn | verdict |
|---|---|---|---|---|
| ralpha_0032 `CsRank(EP)*CsRank(CFP)` | +0.032 | **−11.9%** | 0.17 | weakly valid, NOT efficient |
| ralpha_0033 `CsRank(EP)−CsRank(TsSum(RET,120))` | +0.021 | −23.4% | 0.34 | neither |

**0/2 valid+efficient.** Value stocks *underperformed* in H1 2026 (negative
long-excess despite a weakly-positive IC), so value does not clear the set's
robust-in-both bar. Both stay **retired**. This confirms — now with real 2026
data — that value is orthogonal but weak at 10d and did not work in 2026.

## Outcome (value-family campaign, R3+R4)

29 value/quality/size candidates → **2 cleared 2017-25** (value composites EP×CFP
and contrarian value), **0 robust+efficient in 2026**. Findings:
1. **Value is genuinely orthogonal** (every value factor passes S2) — it *would*
   diversify the all-behavioral set. But it is **weak at 10d** (only composites
   clear; interactions and levels die).
2. **Value did not work in 2026** (after the stale-cache fix): weak IC (≤0.032)
   and *negative* long-excess — value stocks lagged in H1 2026.
3. **Data-pipeline lesson:** extending the panel to a new year only refreshed the
   daily-field caches; fundamental/valuation/label caches went stale. Invalidate
   `data/_wide_cache/` (or any cache ending at the prior year-end) after adding a
   year. `fwd_ret_20d` is now rebuilt too — value likely has more punch there, so
   a **20d value sleeve** remains the promising direction. robust_2026 stays **25**.
