# Canonical set — the honest test (2024–2025 holdout)

Run 2026-07-09 (`python3 code/holdout_eval.py canonical` →
`results/mining/sets/canonical/holdout/full_set_eval.json`). This was the
canonical set's first and only read of the holdout window — **it is now
spent for this set too.**

## Verdict: passes as cleanly as the full-vocabulary set

| metric (105 factors, oriented) | canonical | behavioral_full (ref) |
|---|---|---|
| sign consistency vs IS | **105/105** | 105/105 |
| median holdout rank IC | **0.052** | 0.051 |
| share \|IC\| ≥ 0.03 | 93.3% | 95.2% |
| share \|IC\| ≥ 0.02 | 98.1% | 98.1% |
| median holdout/OOS ratio | 1.08 | 1.10 |
| EW composite holdout IC / ICIR | **0.112 / 0.76** | 0.110 / 0.75 |
| EW composite t-stat / pos-rate / 10d LS | 16.5 / 78% / 1.65% | 16.3 / 78% / 1.57% |
| composite yearly IC | 2024: 0.120 · 2025: 0.103 | 0.112 / 0.107 |

**The 8-field canonical set fully recovers — indeed slightly exceeds —
the 105-factor full-vocabulary composite on the untouched window**
(0.112 vs 0.110). Everything the turnover, limit-board, moneyflow,
northbound, valuation, and industry data added to the main set was,
at the composite level, recoverable from OHLCV + VWAP + AMOUNT alone.

## Composition tiers held up

The late-campaign composition factors — the ones most at risk of being
process artifacts — are the *stronger* tier out-of-time: 3-way products
median holdout |IC| **0.058** (n=15), pairs 0.035 (n=11), vs 0.052 for
the set overall.

## Top / bottom

Strongest: intraday reversal bands (0.093–0.095), quarterly median
stretch (0.094), semivol asymmetries (0.087), dollar-attention self-rank
(0.086). Weakest (all still positive): min-family crash factors (~0.02),
overnight momentum 60d (0.023), two burst-pair compositions (~0.02).

## Caveats (same as the main set's report)

Paper rank ICs, not tradable returns: the short leg is largely
unshortable in A-shares, costs at this turnover are material, signals
tilt small. And with both holdouts now read, 2024–25 is no longer an
honest window for anything in this repo — the next true test is live
data.

---

## Addendum — re-read 2026-07-10 (NOT a pristine test)

**Caveat: the 2024–25 holdout was already spent on this set (first read
2026-07-09).** This re-read is NOT an independent honest test — the window
is no longer pristine. It was run at the user's request to cover the ~22
factors accepted after cR10 that had never been individually holdout-read,
and to refresh the composite on the full 105-factor set.

Result (105 factors, 2024–25): 100% sign-consistent · median holdout rank
IC 0.050 · 91% ≥ 0.03 · median holdout/OOS ratio 1.02. EW rank composite:
holdout IC **0.105**, ICIR 0.66, t 14.4, yearly 2024 0.110 / 2025 0.100.
Consistent with the first read (median 0.052 → 0.050 as the set grew).
Treat as a consistency check, not new out-of-sample evidence.
