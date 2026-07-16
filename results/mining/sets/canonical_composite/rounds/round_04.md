# canonical_composite (fresh) — Round 4 — 2026-07-10 (40 candidates)

generation_plan-driven (rich vein 0.588 → 70/15/15): exploit fresh
three-ways (28), probe strong-parent pairs (6), explore four-way-products
insight (6).

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2 |corr|<0.70 vs
this set's residents, replacement ≥1.3× · S3 dedup 0.70 · S4: OOS
same-sign ≥max(0.03, 0.4×IS); ≥2/3 {HS300,CSI500,CSI1000} same-sign
≥0.005; yearly ≥0.60; rolling 120d/20 ≥0.70; bootstrap B=1000, block=10,
seed=11, p≤0.05.

**Funnel: 40 → S1 18 → S2 17 → S3 17 → S4 17 accepted.**
Set: **88 factors** (cxalpha_0072–0088), diversity ~0.80. Runtime ~58 min.

## Accepted (17) — all three-ways

Led by semivol60×med60×volclock (0.060), nvolspike×rev60×volclock
(0.056), retonhiHL×med60×volclock (0.054), semivol60×rev60×amtself
(0.054), aggrmax60×med60×volclock (0.053). Every accept was a three-way
of strong parents crossed with the stretch/state/clock backbone.

## Rejected (23) — the tier is narrowing

- **Pairs 0/6** (S1): all strong-parent pairs (aggrmax60/semivol60/
  retonhiHL/aggrmin60 × amtself) have strong ICIR (−0.31 to −0.72) but
  IC 0.014–0.026 — a 2-product dilutes even strong parents below the bar.
- **Four-ways 0/6** (5 S1, 1 S4): the four-way-products insight is now
  1/9 across R3–R4 → **REFUTED**; `fourway` family classified forbidden.
- **Weak-parent three-ways** (10 S1): min60, gapmed-drift, aggr-asymmetry,
  retvrcorr as the novel leg all left IC 0.020–0.028 — confirms the
  parent-quality law (parents below ~0.05 IS IC don't compose).

## Distilled (memory updated)

Three-ways of strong parents remain the only productive tier. Family
stats merged (threeway 0.82 success; pair→undetermined 0.30 declining;
fourway→forbidden). Insight `four-way-products` refuted;
`sign-conditioned-composition` was refuted in R3. Set 88 → Round 5 (pure
strong-parent three-ways) closes to 100.
