# canonical_composite (fresh) — Round 1 — 2026-07-10 (40 candidates)

First round of the reset campaign: compositions over the current 105
individual canonical factors. 18 prior-winner re-derivations + 22
new-parent combinations.

## Evaluation parameters (complete)

Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50 names/date ·
daily Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…
2023-12-31 · S1 |IC|≥0.03, |ICIR|≥0.30, cov≥0.60 · S2 |corr|<0.70 vs
THIS set's residents (set empty at start), replacement ≥1.3× · S3
intra-round dedup 0.70, keep-best by |ICIR| · S4: OOS same-sign
≥max(0.03, 0.4×IS); ≥2/3 of {HS300,CSI500,CSI1000} same-sign ≥0.005;
yearly sign-rate ≥0.60; rolling 120d/step 20 sign-rate ≥0.70;
moving-block bootstrap B=1000, block=10, seed=11, p≤0.05.

**Funnel: 40 → S1 31 → S2 31 (empty set) → S3 31 → S4 24 accepted.**
Set: **24 factors** (cxalpha_0001–0024), diversity **0.806**. Runtime 61 min.

## Accepted (24)

**Replication (18/18):** every prior-winner re-derivation re-passed all
five stage-4 tests — 10 pairs (OOS −0.032 to −0.044) and 8 three-ways
(OOS +0.042 to +0.058, led by rev60×volclock×amtself at 0.058). A clean
validation that the reset changed provenance, not substance.

**New-parent compositions (6/22):**

| construct | OOS IC |
|---|---|
| x3_aggrhigh_med_volclock (aggression-at-highs × stretch × clock) | +0.053 |
| x3_gapdipmag_volclock_amtself (dip-depth magnitude × clock × state) | +0.049 |
| x3_hlbest_rev60_amtself (best-day texture × reversal × state) | +0.046 |
| x_dipbuy_med (absorption × stretch) | +0.036 |
| x3_dipbuy_med_volclock / x3_dipbuy_maxfreq_med | −0.034 each |

Sign note: dip-buy compositions come out negative — the absorption
count's own bearish direction propagates through the product.

## Rejected (16)

- **S1 (9)**: weak parents don't compose — every pin/doji/island
  combination (ICIR up to −0.53 but IC under 0.03) and the volaccel
  3-way (0.028). Parent quality gates composition quality: parents
  below ~0.05 IS IC as standalone factors fail as composition inputs.
- **S4 (7)**: the count×count control probe (dipbuy×maxfreq) failed OOS
  at 0.021, exactly as the prior campaign's template law predicted;
  truegapdn pairs 0.014–0.018; dipbuy×gapvol / dipbuy×amtself just
  under the 0.03 bar.

## Distilled

Templates transfer to the 105-parent pool intact (count/magnitude/
texture parent × stretch/state parent; 3-ways with volclock strongest);
parent quality gates composition quality; the count×count prohibition
replicated on fresh parents.
