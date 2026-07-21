# robust_2026 — curated cross-period, cost-aware, non-overnight set

A hand-curated set (not a mining campaign) of factors that are **robust in BOTH
2017-2025 and the fresh 2026 window, tradable net of cost, and NOT overnight-gap.**
Prefix `ralpha_`. Built by `code/build_robust_2026_set.py` from the 2026
per-factor screen ([[VALID_2026.md]]) + Rounds 13-14.

## Membership (24)

| provenance | n | what |
|---|---|---|
| `mined_R13-14` | 5 | newly-mined robust+efficient factors, **MOVED** out of behavioral_full (retired there; they live only here): ralpha_0001-0005 = alpha_0155/0144/0152/0146/0153 |
| `past_valid_2026` | 19 | distinct factors that were valid AND efficient in the 2026 screen, **excluding overnight-gap**, deduped cross-set (behavioral_full preferred over its 0.96-correlated canonical twins): 14 from behavioral_full + 5 from canonical |

Each entry keeps `source_set` / `source_name` provenance and its 2026
`signed_ic_2026` / `net_excess_15bp_2026`. Values were copied from the source
sets' stored parquets (2017-2025); rebuildable from expressions for 2026.

## The vein

The set is dominated by **activity-stability / liquidity-shape** (CV + median/mean
ratios of volume-like quantities: range-CV, relative-amount CV, VR/AMOUNT median-
mean) and **event-rarity** ("calm stocks outperform"), plus flow-divergence
couplings and low-idio/systematic-share — the low-turnover veins that survive
2026 costs. Top by 2026 net-of-cost: ralpha_0001 `-TsStd(AMP,120)/TsMed(AMP,120)`
(+22.7%), calpha-derived event-rarity, and turnover-spike rarity.

## Notes

- **Overnight-gap is deliberately excluded** (per the mining directive) even
  though it was the single best 2026 vein — filtered by expression
  (`OPEN/Delay(CLOSE,1)`), not just the family label (alpha_0110 was mislabeled
  "robust").
- Empty `experience_memory.json` seeded for future mining rounds against this set
  (`SET_NAME="robust_2026"`).
- Not holdout-tested as a set; the 2024-25 holdout is spent for the source sets.
