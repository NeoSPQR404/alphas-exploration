# Canonical set — Round 1 — 2026-07-08 (40 candidates)

First round of the independent **canonical set**: generation restricted
to OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT, VWAP, RET (AST-enforced
whitelist). Same 0.03 gates and windows as the main set; registry, memory,
and values fully separate (prefix `calpha_`). This round transferred the
main set's proven constructs into the restricted vocabulary; turnover-
based winners were re-expressed with normalized volume
(`nvol = VOLUME/TsMean(VOLUME,60)`).

**Funnel: 40 → S1 37 → S2 37 (set empty) → S3 36 → S4 34 accepted.**
Canonical set: **34 factors**, diversity **0.781**. Runtime 57 min.

## Accepted (34) — highlights

| construct | OOS IC | note |
|---|---|---|
| c_hlmed60 `-TsMed(HIGH/LOW−1,60)` | **0.094** | champion transfers intact |
| c_max20 `-TsMax(RET,20)` | 0.091 | |
| c_gapvol `-TsStd(gap,20)` | 0.085 | |
| c_aggrmax `-TsMax(CLOSE/VWAP−1,20)` | 0.083 | |
| c_ret_on_hivol60 (VOLUME-conditioned) | 0.082 | turnover condition → volume condition works |
| c_max60 / c_semivol120 / c_volclock | 0.080 / 0.079 / 0.076 | |
| c_rev20 / c_rev60 / c_med60 | 0.071 / 0.072 / 0.070 | reversal family |
| c_hl_updown (range asym) | 0.071 | masked-asym translates |
| c_flatopen / c_zeroret | −0.047 / −0.039 | liquidity-void probes hold |

Full list: reversal ×6, overnight ×5, lottery ×5, volatility ×5,
aggression ×3, volume ×5, liquidity ×2, conditional/asym ×3.

## Rejected (6) — the transfer lessons

- **c_elasticity ICIR 0.03, c_fragility −0.07** (turnover versions: 0.83
  / 0.65): RegBeta constructs die on self-normalized volume — turnover's
  free-float (cross-sectional) normalization was load-bearing.
  Correlation-style couplings survive; regression betas don't.
- c_ret_nvol_corr → dup of c_vol_updown at S3.
- c_volterm IC 0.027 (under the modern 0.03 bar), c_ovnshare OOS 0.018,
  c_vwapdev 2/3 universes.

## Next

Round 2: novel canonical-only constructs (leg couplings, candle-derived
quantities not tried before, AMOUNT structures, deeper conditional/asym
tiers) to push the set beyond pure transfer.
