# Round 6 — 2026-07-07 (40 candidates, first flow-data round)

28/40 candidates targeted the new flow fields (moneyflow, northbound,
margin); 12 OHLCV leftovers.

**Funnel: 40 → S1 11 → S2 8 → S3 8 → S4 6 accepted.**
Alpha set: **56 factors** (+6, −1 replaced), diversity **0.841**. 22 min.

## The flow verdict

**Levels are dead, coupling is alive.** All 11 moneyflow level/mean
constructs, all 7 northbound deltas/levels, and all margin balances died
at S1 (ICIR ≤ 0.29). The two survivors from flow data are correlation
structures: `mf_ret_corr` (big-order flow chasing same-day returns →
fade) at **OOS 0.070 / ICIR 0.75**, best of round. Two technical traps
recorded: TsCorr on 0-filled eligibility fields craters coverage
(hk_ret_corr 0.42, rz_ret_corr 0.37), and interactions with HK fields
fail sub-universes (hk_x_lottery 0/3 at S4).

## First replacement executed

`ret_vr_corr` (−TsCorr(RET, VR, 20)) correlated 0.85 with alpha_0006
(smart_flow) at 1.58× its |IS IC| → alpha_0006 retired with provenance,
registry consistent (56 active = 51 + 6 − 1).

## Accepted (6)

| name | expression | dir | IS IC / ICIR | OOS IC / ICIR |
|---|---|---|---|---|
| alpha_0052 | `-TsCorr(MF_LG_NET, RET, 20)` | + | 0.053 / 0.59 | **0.070 / 0.75** |
| alpha_0053 | `CsRank(HighDay(AMP, 120))` | + | 0.038 / 0.63 | 0.022 / 0.31 |
| alpha_0054 | `-TsCount(VR > 2, 60)` | + | 0.044 / 0.61 | 0.044 / 0.58 |
| alpha_0055 | `-TsCorr(RET, VR, 20)` (replaces 0006) | + | 0.051 / 0.59 | 0.049 / 0.57 |
| alpha_0056 | `-TsMean((CLOSE/VWAP−1)·(VR>1), 20)` | + | 0.054 / 0.69 | 0.043 / 0.60 |
| alpha_0057 | `-TsRank(AMP, 120)` | + | 0.034 / 0.41 | 0.034 / 0.35 |

## Notable rejections

- `limit_close_cnt` — standalone IS 0.075/0.76 (!) but 0.87 corr vs the
  limit_touch incumbent, and only 1.16× its IC (below the 1.3× bar).
  One representative per event type.
- `hk_d20` 0.29 ICIR — northbound accumulation is *close* but under the
  gate at 10d; plausibly a 20d-label factor.
- `ix_mf_hk` 0.04 — institutional-pair interaction carries nothing
  (the template's edge is behavioral crowding, not information overlap).

## Distilled

**Successful:** flow-return coupling; the trick portfolio {count,
recency, self-rank, conditional-mean} × {new quantity}. **Forbidden:**
flow levels at 10d; TsCorr on 0-filled fields; >1 factor per event type.
