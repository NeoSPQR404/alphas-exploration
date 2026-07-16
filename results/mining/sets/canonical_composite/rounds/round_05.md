# canonical_composite (fresh) — Round 5 — 2026-07-10 (34 candidates) — TARGET MET

Pure exploitation of the threeway tier to close from 88 to ≥100.
generation_plan: pairs/four-ways forbidden, both insights refuted → all
34 candidates are fresh strong-parent three-ways.

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2 |corr|<0.70 vs
residents, replace ≥1.3× · S3 dedup 0.70 · S4: OOS same-sign ≥max(0.03,
0.4×IS); ≥2/3 {HS300,CSI500,CSI1000} ≥0.005; yearly ≥0.60; rolling
120d/20 ≥0.70; bootstrap B=1000, block=10, seed=11, p≤0.05.

**Funnel: 34 → S1 33 → S2 31 → S3 31 → S4 31 accepted.**
Set: **119 factors** (cxalpha_0089–0119) — **target 100 exceeded.**
Runtime ~48 min.

## Accepted (31) — all three-ways

Led by cxalpha_0090 (OOS 0.070) and cxalpha_0096 (0.068). Novel
cross-family triples (two novel parents + one anchor, and novel + fresh
anchor-pair) all cleared.

## Rejected (3)

- **S2 corr = 1.00** (×2): semivol×volclock×rev60 and aggrmax×volclock×
  rev60 are *exact duplicates* of earlier accepted triples — rank
  products commute, so parent-set collisions surface as perfect
  correlation. The binding limit is now combinatorial exhaustion of
  fresh strong-parent triples, not signal.
- **S1** (×1): one weak-parent triple.

## Campaign summary (canonical_composite, fresh)

**119 composite factors in 5 rounds** (24, 22, 25, 17, 31), all
three-way and pair rank-products of the 105 canonical individual parents.

Distilled laws (in experience_memory.json, schema v2):
- **threeway** family: 0.82 success — the productive tier.
- **pair**: undetermined→declining; new-class parent pairs fail (strong
  ICIR, IC under bar); only legacy strong-parent pairs cleared (early).
- **fourway**: forbidden; insight `four-way-products` refuted (1/9).
- `sign-conditioned-composition` insight refuted (0/3).
- Parents below ~0.05 IS IC don't compose; sign parity (pairs negative,
  3-ways positive); commutativity now caps fresh triples.

This campaign was the first driven end-to-end by `Memory.generation_plan`
— the exploit/probe/explore budget and the auto-refuted insights steered
every round from R3 on.
