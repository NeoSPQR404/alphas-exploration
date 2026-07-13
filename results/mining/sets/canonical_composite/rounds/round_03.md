# canonical_composite (fresh) — Round 3 — 2026-07-10 (40 candidates)

**First round generated from the memory `generation_plan(40)`** — a
demonstration of the v2 memory system driving candidate allocation.

## Generation plan followed
Recent accept rate 0.575 → rich vein → weights 70/15/15.
- **exploit (28)**: `threeway` family (0.82 success rate) — new
  fresh-parent triples.
- **probe (6)**: `pair` family (undetermined) — legacy strong-parent pairs.
- **explore (6)**: insights `four-way-products` (3) + `sign-conditioned-
  composition` (3).
- **avoid**: the two forbidden patterns (new-class parent pairs, weak
  parents) — none proposed.

## Evaluation parameters (complete)
Whitelist OPEN,HIGH,LOW,CLOSE,VOLUME,AMOUNT,VWAP,RET (AST-enforced) ·
label fwd_ret_10d (t+1 vwap) · full-A tradable_entry, ≥50/date · daily
Spearman rank IC · IS 2017-01-01…2021-12-31 · OOS 2022-01-01…2023-12-31 ·
S1 |IC|≥0.03,|ICIR|≥0.30,cov≥0.60 · S2 |corr|<0.70 vs this set's
residents, replace ≥1.3× · S3 dedup 0.70 · S4: OOS same-sign
≥max(0.03,0.4×IS); ≥2/3 {HS300,CSI500,CSI1000} same-sign ≥0.005; yearly
≥0.60; rolling 120d/20 ≥0.70; bootstrap B=1000,block=10,seed=11,p≤0.05.

**Funnel: 40 → S1 28 → S2 28 → S3 26 → S4 25 accepted.**
Set: **71 factors** (cxalpha_0047–0071), diversity **0.784**. Runtime 76 min.

## Accepted (25)
**Exploit 23/28** — fresh-parent three-ways all compose:

| construct | OOS IC |
|---|---|
| x3_max20_med_amtself | +0.065 |
| x3_max20_volclock_amtself | +0.062 |
| x3_retonhivol_volclock_amtself | +0.062 |
| x3_retonhivol_med_volclock | +0.061 |
| x3_hlonhivol_med_volclock · x3_gapdipmag_rev60_volclock | +0.060 / +0.059 |
| (17 more, OOS +0.040 to +0.059; mingap triples −0.042) | |

**Probe 1/6**: x_max20_amtself pair (−0.034). **Explore 1/6**:
x4_med_volclock_amtself_maxfreq (−0.031).

## Insight outcomes (recorded via `record_insight`)
- **four-way-products → "testing"** (1/3): four-way products *do* clear
  but at a lower rate than 3-ways; **parity sign rule** confirmed — odd
  number of rank-factors → positive IC, even (pairs, four-ways) →
  negative. Needs more trials to promote.
- **sign-conditioned-composition → "refuted"** (0/3): gating A by the
  sign of B either duplicates the plain pair (xsg_max20_by_amtself dup
  of x_max20_amtself) or dilutes below the bar. Symmetric rank products
  dominate.

## Rejected (15)
- S1 (12): all 4 **hlmed60-anchored triples** (0.025–0.029, just under —
  the strongest individual factor does NOT compose, its range signal
  overlaps med60/gapvol); 5 probe pairs; 1 four-way; 2 sign-gates.
- S3 (2): nvolburst_rev60_amtself dup of hlburst_rev60_amtself;
  xsg_max20_by_amtself dup of the max20 pair.
- S4 (1): x4_aggrmax_med_volclock_amtself OOS −0.029 (just under).

## Distilled
Fresh-parent 3-ways keep clearing ~0.85; parity sign rule confirmed;
hlmed60 doesn't compose (new forbidden pattern); sign-gating refuted;
four-ways in testing.
