# Round 9 — 2026-07-07 (40 candidates) — TARGET REACHED

Exploit round: 15 interactions, robust/median + MAX-of-quantity, slow
bands, event structures.

**Funnel: 40 → S1 27 → S2 22 (+1 replacement) → S3 21 → S4 20 accepted.**
Alpha set: **103 factors** (target 100 reached), diversity **0.827**.
Runtime 83 min (S2 now checks ~84 incumbents per survivor).

## Highlights

- **hl_med60** (`-TsMed(HIGH/LOW−1, 60)`, median daily range): OOS
  **0.094 — the best OOS factor in the entire set.**
- **semivol60** replaced alpha_0008 (3rd replacement; skew is now
  spanned by the quarterly semivol band at 1.9× the IC).
- **aggr_min** (deepest capitulation close) OOS 0.059; vol_term_slow
  0.052; mf_vwap_corr60 0.051; **flat_open_freq** — the attention-void
  probe — OOS |0.047| with the anti-intuitive sign (neglected opens
  outperform).
- **Interactions 8/15** at scale. New failure signatures: corr-construct
  parents die at S1 (5/5); one 1/3-universe kill; first year-consistency
  S4 kill (ix_ovnmom_vrburst, 0.71).
- Flow book fully closed: median/MAX/dump/med-dev framings all dead —
  only TsCorr(MF_LG_NET, price-action, {20,60}) survives, all 6 variants
  of which are now in the set.

## Set at 103

Acceptance by round: 11, 7, 4, 12, 14, 6, 11, 18, 20 (three retired:
alpha_0006, alpha_0042, alpha_0008). Top OOS: hl_med60 0.094, max_eff
0.091, gap_vol 0.085, aggr_max 0.083, turn_low 0.080, vol_clock 0.076.
Diversity drifted 0.90 → 0.827 over 9 rounds — still high, but marginal
candidates increasingly pay corr rent to the incumbent set.
