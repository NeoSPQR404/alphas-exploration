# Canonical set — Round 18 — 2026-07-09 (40 candidates, extended run 3/5 — FINAL, campaign terminated by user)

Systematic threshold/window jitters + at-event textures + acceleration
variants. Individual only; thresholds unchanged (parameter block
identical to round_16.md: 8-field whitelist; fwd_ret_10d t+1 vwap;
tradable_entry ≥50; S1 0.03/0.30/0.60; S2/S3 corr<0.70 + 1.3×; S4 OOS
≥max(0.03,0.4×IS) + ≥2/3 universes + yearly ≥0.60 + rolling 120/20
≥0.70 + bootstrap 1000/10/seed 11 p≤0.05).

**Funnel: 40 → S1 14 → S2 5 → S3 5 → S4 5 accepted.**
Canonical set: **105 individual factors**, diversity 0.744. Runtime 26 min.

## Accepted (5)

| name | expression | IS IC / ICIR | OOS IC |
|---|---|---|---|
| calpha_0127* | `-TsMean((H/L−1)·(RET≥TsMax(RET,20)), 60)` (range on the best day) | 0.065 / **0.75** | **0.070** |
| calpha_0128* | `-(TsSum(AMT·(RET>0),60)/TsSum(AMT,60))` (dollar share on up days) | 0.042 / 0.42 | 0.047 |
| calpha_0129* | aggression at highs − at lows | 0.049 / 0.36 | 0.046 |
| calpha_0130* | `-TsCount(|CLOSE/OPEN−1|<0.002, 60)` (doji count) | −0.033 / −0.33 | −0.048 |
| calpha_0131* | `-TsMean(nvol·(RET≥TsMax(RET,20)), 60)` (crowd on the best day) | 0.040 / 0.54 | 0.035 |

(*ids by acceptance order)

## Rejected (35)

- S2 (9): pin threshold variants lock to the parent pin (tight/loose);
  acceleration variants collapse into vol_accel60; max_fortnight_run,
  vol_at_high10, id_at_high, vwap_drift 0.70+.
- S1 (26): re-jitters of dead classes stay dead (occupancy, roundtrip,
  MA-band); amihud_asym60, range_per_vol, quiet/loud day-types,
  remaining wildcards.

## EXTENDED CAMPAIGN VERDICT (rounds 16–18, 120 candidates, terminated after run 3 of 5 by user)

**17 accepts (14%) — the 40/round format out-produced the small-round
format** (5-run experiment: 8/73 = 11%) because parallel class-hunting
finds veins faster. Classes minted: vwap-pin/doji stalemates (−0.048 to
−0.070), true gaps/islands, at-extreme/at-event textures (the deepest:
7 factors incl. hl_at_best 0.070), attention acceleration, dollar-share.
Steady state: ~one new class per 40-candidate sweep, worth 2–5 factors
before self-locking. Set: 105 individual + 26 composite canonical
factors; 236 factors across all three sets.
