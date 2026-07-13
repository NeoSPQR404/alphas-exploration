# canonical_composite (fresh) — Round 2 — 2026-07-10 (40 candidates)

Exploit the strong new-class parents Round 1 confirmed; expand the 3-way
grid; control probes. (Candidates file initially miscounted at 34 —
`assert len == 40` caught it before any run; corrected to 40.)

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2 |corr|<0.70 vs
this set's residents, replacement ≥1.3× · S3 intra-round dedup 0.70 ·
S4: OOS same-sign ≥max(0.03, 0.4×IS); ≥2/3 of {HS300,CSI500,CSI1000}
same-sign ≥0.005; yearly ≥0.60; rolling 120d/20 ≥0.70; bootstrap
B=1000, block=10, seed=11, p≤0.05.

**Funnel: 40 → S1 23 → S2 22 → S3 22 → S4 22 accepted.**
Set: **46 factors** (cxalpha_0025–0046), diversity **0.807** (rose from
0.806). Runtime 58 min.

## Accepted (22)

**3-way products (19)** — the productive tier for new-class parents:

| construct | OOS IC |
|---|---|
| x3_gapvol_med_amtself | **+0.059** |
| x3_hlmed_volclock_amtself | +0.058 |
| x3_aggrmax_rev60_volclock | +0.056 |
| x3_nvoldip_med_volclock | +0.054 |
| x3_nvoldip_rev60_amtself | +0.054 |
| x3_semivol_volclock_amtself · x3_nvolburst_volclock_amtself | +0.052 / +0.052 |
| (12 more, OOS +0.034 to +0.049) | |

**Legacy strong-parent pairs (3):** semivol×amtself (−0.036),
aggrmax×rev60 (−0.036), aggrmax×amtself (−0.031).

## Rejected (18)

- **S1 (16)** — every NEW-class parent PAIR: gapdipmag / gapcapmag /
  aggrhigh / hlbest / nvoldip × {med, amtself} all have strong ICIR
  (−0.42 to −0.68) but IC 0.010–0.027, just under the bar. A 2-product
  dilutes these parents' IC too far; they need the extra 3rd factor's
  cross-sectional lift.
- **S4 (1)** — maxfreq×hlburst (count×count control): OOS −0.025,
  replicating the prohibition a third time.
- **S2 (1)** — hlburst_med_amtself 0.71 vs its Round-1 sibling.

## Distilled

For new-class parents the productive tier is the 3-way, not the pair
(pairs land just under IC even with strong ICIR); legacy strong-parent
pairs still clear; count×count keeps failing. Set at 46, diversity
holding at 0.807 — compositions remain near-orthogonal.
