# Canonical set — Round 15 — 2026-07-09 (12 candidates, novelty run 5/5)

Final experiment run: normalized typed textures (S2-lock breakers),
remaining vein corners, non-vein wildcards. Individual only; thresholds
unchanged (parameter block identical to round_11.md: 8-field whitelist;
fwd_ret_10d t+1 vwap; tradable_entry ≥50; S1 0.03/0.30/0.60; S2/S3
corr<0.70 + 1.3×; S4 OOS ≥max(0.03,0.4×IS) + ≥2/3 universes + yearly
≥0.60 + rolling 120/20 ≥0.70 + bootstrap 1000/10/seed 11 p≤0.05).

**Funnel: 12 → S1 3 → S2 2 → S3 2 → S4 1 accepted.**
Canonical set: **88 factors**, diversity 0.745. Runtime 9 min.

## Accepted (1)

| name | expression | IS IC / ICIR | OOS IC | S4 |
|---|---|---|---|---|
| calpha_0114 | `-TsMean(nvol · capit_day, 60)` (crowd size at capitulations) | 0.043 / 0.55 | **0.055** | 3/3, 1.00, roll ✓, p=0.000 |

## Rejected (11)

- S2 (1): hl_dipbuy_norm — ICIR **0.93** but 0.85 corr vs dipbuy_freq:
  normalizing by own median range does NOT break the lock.
- S4 (1): range_eff_med OOS 0.019.
- S1 (9): capit_rel_depth, recover_eff, amihud_dipbuy (0.04),
  dipbuy_rec, bigdip_vwap_mag, and all wildcards (dollar_depth 0.17,
  gap_kurt 0.05, aggr_med_dev 0.20, hl_capit_norm 0.18).

## EXPERIMENT VERDICT (5 runs, 73 candidates, rounds 11–15)

**Yes — novel ideas were still findable, and the experiment found
exactly one new vein.** 8 factors accepted (11% hit rate), every single
one from the joint-condition day-type class that run 1 surfaced:

| factor | OOS IC |
|---|---|
| gap_dipmag (depth of bought dips) | +0.082 |
| gap_capitmag (capitulation-gap depth) | +0.078 |
| nvol_dipbuy (crowd at absorption) | +0.070 |
| aggr_dipbuy (aggression on dip-bought days) | +0.068 |
| dipbuy_freq 60d / aggr_capit / nvol_capit / dipbuy_freq 20d | −0.064 / −0.064 / +0.055 / −0.053 |

The generator pattern: define day TYPES from joint gap×intraday
conditions, then aggregate {count, magnitude, aggression, attention}
over typed days. Outside the vein: 0-for-30+ (elasticities, shape
ratios, bar patterns, clustering, durations, all wildcards). By run 5
the vein itself self-locks at S2 and its ratios/normalizations don't
decorrelate — harvested. A sixth run would need yet another untouched
structural class; the marginal cost per factor roughly tripled across
the experiment (1, 1, 2, 3, 1 accepts on shrinking candidate quality).
