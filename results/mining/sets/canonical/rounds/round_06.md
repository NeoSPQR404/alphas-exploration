# Canonical set — Round 6 — 2026-07-08 (18 candidates)

Band-jitter retries of near-misses, extensions of the ret_on_hiHL star,
tail-ratio forms.

**Funnel: 18 → S1 11 → S2 4 → S3 4 → S4 1 accepted.**
Canonical set: **79 factors**, diversity **0.754**. Runtime 16 min.

## Accepted (1)

| construct | OOS IC | note |
|---|---|---|
| c_ret_on_hiHL250 `-TsSum(RET·(H/L−1 > mean250), 250)` | **0.082** | annual band of the set's best construct family |

## Rejected (17)

- **S1 (7)** — jitter retries fell back (ret_asym_cnt120 0.16,
  aggr_sum120 0.15, updn_freq_hl120 0.26, vwap_gap_med120 ICIR 0.30 a
  third time); gap_tail_ratio 0.04, hl_spike_ratio 0.18, drift_state 0.21.
- **S2 (8)** — ret_on_hiHL60~rev60 0.72, id_on_hiHL120 0.81,
  wma_cross_slow~rev20 0.75, ovnmom40~ovnmom60 0.84,
  vol_on_down120~signed_nvol −0.94, tail_ratio~aggr_min 0.75,
  min_gap120 0.71.
- **S4 (3)** — hl_cv120 0.015, att_autocorr60 0.021, nvol_burst250 0.020.

## Saturation declared

Rounds 5–6 yielded 2 then 1 — the trigger set in round_05.md. The
canonical vocabulary against this set at corr<0.70 is exhausted;
escalated to the user with options (grind on, relax the intra-set corr
ceiling + salvage round, or freeze at 79).
