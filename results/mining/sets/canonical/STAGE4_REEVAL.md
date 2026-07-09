# canonical — upgraded stage-4 re-evaluation

Run 2026-07-09, `python3 code/reevaluate_stage4.py` — full stage-4
re-run for all 105 active factors after adding the rolling-window and
bootstrap tests. **Report only: nothing was retired.**

## Evaluation parameters (complete)

| parameter | value |
|---|---|
| label | fwd_ret_10d (entry t+1 vwap → exit t+11 vwap, suspension-aware) |
| universe / mask | full-A `tradable_entry`, min 50 names per date |
| IC definition | daily cross-sectional Spearman rank IC, oriented by stored factor direction |
| IS window | 2017-01-01 … 2021-12-31 |
| OOS-gate window | 2022-01-01 … 2023-12-31 |
| test span (yearly / rolling / bootstrap) | 2017-01-01 … 2023-12-31 |
| **T1 OOS test** | same sign as IS and \|OOS IC\| ≥ max(0.03, 0.40 × \|IS IC\|) |
| **T2 universes test** | ≥ 2 of {HS300, CSI500, CSI1000} with same-sign IC ≥ 0.005 over IS+OOS |
| **T3 yearly test** | ≥ 60% of 2017–2023 yearly ICs same-sign |
| **T4 rolling test (new)** | window 120 trading days, step 20 (79 windows/factor); ≥ 70% of windows with positive mean oriented IC |
| **T5 bootstrap test (new)** | moving-block bootstrap of mean daily oriented IC; B = 1000, block = 10 days (= label horizon, preserves overlap autocorrelation), seed = 11; one-sided H0: mean ≤ 0; reject at p ≤ 0.05 |
| (context) S1 gates at acceptance | \|IS rank IC\| ≥ 0.03, \|IS ICIR\| ≥ 0.30, coverage ≥ 0.60 |
| (context) S2/S3 gates | \|cross-factor Spearman corr\| < 0.70, replacement at ≥ 1.3× \|IS IC\| |

## Result: 105 / 105 pass all five sub-tests

| sub-test | failures |
|---|---|
| T1 OOS | 0 |
| T2 universes | 0 |
| T3 yearly | 0 |
| T4 rolling (new) | 0 |
| T5 bootstrap (new) | 0 |

Distributional detail:

- **Rolling**: minimum sign-rate across the set 0.89 (bar: 0.70);
  median 1.00; 74% of factors positive in *all 79* windows. Median
  worst-window IC +0.0097; single worst window in the set −0.0369.
- **Bootstrap**: every factor has p = 0.000 (no resample of 1000 put the
  mean at or below zero); minimum 5th-percentile CI bound +0.0257,
  median +0.0369 — i.e. even the weakest factor's bootstrap CI floor
  sits near the 0.03 acceptance bar.
- Weakest by rolling sign-rate: calpha_0067 (range-burst 120d, 0.89), calpha_0066 (range-burst 60d, 0.90), calpha_0080 (3-way composition, 0.92) — all comfortably above the bar.

## Reading

The new tests bind on exactly the pathology they target — factors that
earn their mean IC in a few concentrated episodes — and find none: the
existing gates (0.03 both-window IC, 7-year sign consistency, three
sub-universes) had already selected for temporal stability. The tests
now guard all future rounds at stage 4, where candidates will face them
before acceptance rather than after.

Full per-factor detail: `stage4_reeval.json` in this directory.
