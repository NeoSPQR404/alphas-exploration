# Canonical set — Round 4 — 2026-07-08 (28 candidates)

Overnight-momentum bands, conditional RANGE (novel class), robust
deviation constructs, studentized range, 250d tier tests, remaining
fills. (This report was initially skipped due to a tooling interruption
and backfilled the same day — the run itself completed cleanly.)

**Funnel: 28 → S1 16 → S2 10 → S3 10 → S4 7 accepted.**
Canonical set: **76 factors**, diversity **0.758**. Runtime 34 min.

## Accepted (7) — highlights

| construct | OOS IC | note |
|---|---|---|
| c_hl_on_hivol60 `-TsMean((H/L−1)·(nvol>1), 60)` | **0.081** | **conditional range: novel first-class construct** — range on high-attention days |
| c_hl_on_hivol (20d) | **0.078** | passed despite the median-range champion resident: conditional masking decorrelates from the level |
| c_semivol250 | 0.072 | annual semivol asymmetry (all four bands now coexist) |
| c_id_on_hivol250 | 0.064 | annual conditional (intraday leg on high-volume days) |
| c_maxfreq20 | 0.045 | fast lottery-day count |
| c_id_nvol_corr60 | 0.042 | quarterly intraday-attention coupling |
| c_ovn_rev7 | 0.032 | weekly decayed overnight band |

## Rejected (21)

- **S1 (12)** — robust-deviation class under the bar: hl_med_dev 0.026,
  nvol_med_dev 0.021; range_stud −0.021, gap_updown60 0.010,
  close_pos_med 0.012 (candle book closed), min120 / zeroret250
  (ICIR < 0.3); near-misses recorded for band-jitter retries: ovnmom20
  0.028, vwap_gap_med 0.032 / ICIR 0.29, aggr_sum60 0.028,
  updn_freq_hl 0.027 / 0.30.
- **S2 (6)** — ovnmom120~ovnmom60 0.75, hl_updown250 0.73,
  aggrmin120 0.76, aggr_hi_nvol120 0.74, idvol60~max20 0.76,
  hi_nvol_vol 0.73.
- **S4 (3)** — vol_on_downdays OOS 0.026, gap_share60 0.018,
  zeroret20 0.029 (just under the bar).

## Distilled

**Successful:** conditional-X-on-attention generalizes — pursue
conditional gap-vol, directional range, quiet-day complements (done in
Round 5). **Forbidden:** robust-deviation (X vs own median) class;
gap asymmetry at every band; candle constructs in any framing.
