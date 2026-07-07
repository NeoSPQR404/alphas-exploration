# Round 8 — 2026-07-07 (40 candidates)

Exploit round: 10 interactions, RegBeta/corr bands, retired-incumbent
retry, robust/median constructs, HK/margin level-safe retries.

**Funnel: 40 → S1 29 → S2 21 (+1 replacement) → S3 21 → S4 18 accepted.**
Best round since R1. Alpha set: **84 factors**, diversity **0.831**. 64 min.

## Highlights

- **aggr_max** (`-TsMax(CLOSE/VWAP−1, 20)`, peak late-day aggression):
  OOS **0.083**, best of round.
- **ret_amp_corr60** OOS 0.062 — the construct alpha_0006's retirement
  freed up; its 20d version still died vs semivol_asym (0.74), the 60d
  band cleared.
- **Robust/median family**: gap_med60 (median overnight drift, OOS
  0.051), mean_med_gap60 (OOS 0.049) — outlier-proof constructs keep
  beating their moment-based cousins OOS.
- **Interactions 6/8** — template scales when parents are accepted
  behavioral factors from different families; both failures were
  sub-universe fails involving turn_low (small-cap-leaning parent).
- **2nd replacement**: aggr_vr_corr displaced alpha_0042 (0.84 corr,
  ≥1.3×).
- Bands: volresp60, lag2_60, aggr_attn_corr60, vol_term_mid in;
  fragility60 died at the S4 OOS-ratio bar.

## The HK/margin book is closed

hk_dip 0.02, hk_d20_ind 0.26, rz_burst −0.06, hk_burst 0.14 — after R6's
level slaughter and R7's coverage trap, no structural form of northbound
or margin data clears the 10d full-A gates. Recorded as forbidden;
plausibly 20d-label or subset-universe material for a later track.

## Distilled

**Successful:** interaction template scales (6/8); robust/median as a
first-class family; band separation extends to RegBeta. **Forbidden:**
HK/margin in any 10d form; high/low-making frequency; conditional
aggression splits.
