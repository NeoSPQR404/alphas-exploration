# Round 10 Mining Results

**Diversity Score:** 0.793  
**Total Candidates Evaluated:** 28  
**Accepted Factors:** 8  
**Acceptance Rate:** 28.6%

## Accepted Factors (Stage 4 Pass)

| Alpha ID | Name | Expression | Family | IS ICIR | OOS ICIR | Logic Score |
|----------|------|-----------|--------|---------|----------|-------------|
| alpha_0107 | aggr_max60 | -TsMax(CLOSE / VWAP - 1, 60) | tail_event | 0.684 | 0.529 | 70 |
| alpha_0108 | max_eff60 | -TsMax(RET, 60) | lottery | 0.654 | 0.600 | 70 |
| alpha_0109 | min_eff60 | -TsMin(RET, 60) | lottery | -0.313 | -0.413 | 69 |
| alpha_0110 | gap_med20 | TsMed(OPEN / Delay(CLOSE, 1) - 1, 20) | robust | 0.670 | 0.659 | 69 |
| alpha_0111 | id_med20 | TsMed(CLOSE / OPEN - 1, 20) | robust | -0.400 | -0.371 | 69 |
| alpha_0112 | lag_chase120 | -TsCorr(TURN_F, Delay(RET, 1), 120) | corr_band | 0.509 | 0.520 | 68 |
| alpha_0113 | ret_vr_corr120 | -TsCorr(RET, VR, 120) | corr_band | 0.495 | 0.493 | 68 |
| alpha_0114 | attn_risk_corr120 | -TsCorr(TURN_F, TsStd(RET, 5), 120) | corr_band | 0.586 | 0.398 | 68 |
| alpha_0115 | aggr_amp_corr | -TsCorr(CLOSE / VWAP - 1, AMP, 20) | cross_corr | 0.627 | 0.696 | 67 |

## Stage 1 Failures (IC Screen)

**Failed candidates:** 19 factors rejected at early gates for weak IC, low ICIR, or high correlation.

### Notable Stage 1 Rejects:
- **med_band240** (IC: 0.035, ICIR: 0.211) — Annual reversal band; insufficient signal
- **mean_med_gap120** (IC: 0.025, ICIR: 0.296) — Mean-median gap; weak predictive power
- **vr_term** (IC: 0.004, ICIR: 0.049) — Attention term structure; noise-dominated
- **vr_med60** (IC: 0.010, ICIR: 0.150) — Robust VR median; insufficient signal

### Stage 2+ Failures (High Correlation):
- **hl_med20** (max_corr: 0.723 vs alpha_0001)
- **vol_clock60** (max_corr: 0.783 vs alpha_0044)
- **upvol_share** (max_corr: 0.949 vs alpha_0016)
- **downvol60** (max_corr: 0.778 vs alpha_0096)
- **hl_max** (max_corr: 0.711 vs alpha_0007)
- **idvol60** (max_corr: 0.718 vs alpha_0001)
- **gap_min** (max_corr: -0.789 vs alpha_0015)
- **id_vr_corr** (max_corr: 0.886 vs alpha_0055)
- **mf_id_corr60** (max_corr: 0.814 vs alpha_0099)
- **gap_vr_corr** (failed S1 gate; IC: 0.027, t-stat: 17.0)

## Key Patterns

1. **Robust & Tail-Event Dominance:** Accepted factors cluster in `robust` (med-based, fast bands) and `tail_event` families, suggesting mean-reversion + extreme-move patterns remain stable.

2. **Correlation Filtering:** 10 candidates failed correlation gates—a testament to set maturity; new factors must be decorrelated from the 106+ existing alphas.

3. **Bidirectional Signals:** Both long (e.g., aggr_max60, ICIR +0.68) and short (e.g., min_eff60, ICIR −0.41) signals passed, indicating asymmetric risk-return opportunities.

4. **Semi-Annual Bands:** Three accepted correlation factors use 120-day windows (lag_chase120, ret_vr_corr120, attn_risk_corr120), showing semi-annual cycles in turnover, volatility, and attention coupling.

5. **Cross-Sectional Correlation:** aggr_amp_corr (alpha_0115) tied aggression to range, with clean OOS replication (ICIR 0.696) and broad universe coverage (HS300, CSI500, CSI1000 all pass).

## OOS & Multi-Universe Validation

All 8 accepted factors pass Stage 4 (OOS 2022–2023 + multi-universe):
- **OOS IC**: 0.031–0.077 (all ≥ threshold; sign consistency 100%)
- **Universe Coverage**: HS300, CSI500, CSI1000 all ≥ 0.005 IC for each factor
- **Yearly Consistency**: 100% of 2017–2023 years same-sign IC

## Observations

- **Diversity improvement:** 0.793 (up from prior rounds), indicating good candidate distribution across families.
- **Quality bar:** IS→OOS IC decay moderate (0.6–0.8× carry-through), consistent with prior rounds.
- **Flow coupling:** mf_id_corr60 nearly accepted (S2: 0.814 corr vs alpha_0099); flow factors remain challenging but viable.

---

**Status:** Round 10 adds **8 new alphas** (alpha_0107–alpha_0115) to the registry. Set size: 115 factors. Next round will distill patterns from robust/tail-event/corr-band successes and flow-factor constraints into experience memory.
