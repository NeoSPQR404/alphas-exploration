# Canonical set — Round 5 — 2026-07-08 (16 candidates)

Conditional-on-attention family pushed across quantities and directions
(per the Round-4 discovery), plus the last novel forms (attention
persistence, range CV, movement efficiency, tail-count asymmetry).

**Funnel: 16 → S1 11 → S2 4 → S3 4 → S4 2 accepted.**
Canonical set: **78 factors**, diversity **0.755**. Runtime 16 min.

## Accepted (2) — highlights

| construct | OOS IC | note |
|---|---|---|
| c_ret_on_hiHL120 `-TsSum(RET·(H/L−1 > mean120), 120)` | **0.092** | **best factor in the canonical set** — returns earned on wide-range days; the condition variable matters: range-conditioned beats volume-conditioned (0.092 vs 0.081) |
| c_aggr_updown120 | 0.052 | aggression asymmetry completes the 20/60/120 ladder |

## Rejected (14)

- **S1 (5)** — hl_on_lovol 0.008/0.08 (quiet-day complement dead),
  nvol_min −0.010/−0.10, travel_eff 0.006/0.06 (last path-shape test),
  ret_asym_cnt 0.032/ICIR 0.30 borderline, wma_cross 0.040/ICIR 0.30
  borderline (twice now — one final jitter retry earned).
- **S2 (7)** — the conditional family now collides with its own
  residents: hl_on_down~hlmed60 0.76, hl_on_hivol250~hlmed60 0.79,
  max_on_hivol~max20 0.85, id_on_hiHL60~rev20 0.84,
  gapvol_on_hivol~gapvol 0.71, id_updown60 0.73, gapmax120 0.71.
- **S4 (2)** — hl_cv OOS 0.023 and att_autocorr 0.028: near-misses,
  eligible for longer-band jitter retries.

## Distilled

**Successful:** range-conditioned returns > volume-conditioned; the
conditional class is the canonical set's main alpha source.
**Forbidden:** conditional variants against resident levels (S2 wall
arriving); quiet-day complements; drought/efficiency probes.

## Saturation watch

Acceptance: 34 → 21 → 16 → 7 → 2. The canonical vocabulary against 78
residents is close to exhausted; Round 6 = band-jitter retries of
recorded near-misses + tail-ratio forms. If two consecutive rounds
yield < 5, escalate to the user with options (relax novelty via
replacements, accept a sub-100 canonical set, or widen the vocabulary).
