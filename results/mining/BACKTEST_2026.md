# The 2026 out-of-sample test — the factor edge REVERSED

Run 2026-07-16 on **genuinely unseen data**: the 2026 window (Jan 5 →
Jun 24, 10 rebalances) was fetched fresh from tushare and had never
touched any gate, distill, holdout, or backtest. Unlike the spent
2024–25 holdout, this is the first real out-of-sample evidence in the
project. `code/backtest_2026.py` recomputes every factor from its stored
expression over the 2017–2026 panel and evaluates each set's EW
oriented-rank composite on 2026 only. Same design as the historical
backtest (10-day rebalance, t+1 vwap, 15bp costs, full-A tradable_entry).

## Verdict: the 2017–2025 behavioral edge did not survive — it inverted.

Decile mean 10-day return (%), D1 = composite's WORST-ranked, D10 = top:

| set | D1 | D2 | … | D9 | D10 | shape |
|---|---|---|---|---|---|---|
| behavioral_full | 0.70 | 0.77 | … | −0.27 | 0.01 | broken, mildly inverted |
| canonical | 1.22 | 0.61 | … | −0.15 | −0.27 | **clean monotone inversion** |
| canonical_composite | 1.57 | 1.13 | … | −0.34 | −0.58 | **steep monotone inversion** |

Portfolio results (2026, market EW +3.0%/yr, CSI300 −5.8%/yr):

| set | LO net-15bp | excess-vs-universe | long-short gross | turnover |
|---|---|---|---|---|
| behavioral_full | −4.3%/yr (S −0.28) | −5.1%/yr | −20.8%/yr | 0.48 |
| canonical | −10.6%/yr (S −0.73) | −11.6%/yr | −36.4%/yr | 0.46 |
| canonical_composite | −18.2%/yr (S −1.10) | −18.1%/yr | −46.6%/yr | 0.57 |

The composite's long-short lost **−22% cumulatively in six months.**

## This is a regime flip, not noise — and the clean monotonicity proves it.

A *dead* signal gives a flat decile curve. What we see is a **cleanly
reversed monotone** curve (most perfect in canonical/composite): the
factors still have real cross-sectional predictive power — it pointed the
**opposite** direction in H1 2026. The market context confirms the
mechanism: CSI300 (large caps) −5.8% while the equal-weight universe
+3.0% → a **small-cap / speculative regime** in which the recent-winner,
high-lottery, high-turnover, low-value names that every one of these
factors is built to FADE were exactly what led the market. The reversal /
anti-lottery / low-turnover theses reversed together.

The inversion **strengthens with signal concentration**: behavioral_full
(broadest, includes some value/quality) is least inverted; canonical
(pure price-volume reversal/lottery) more; composite (rank-products that
concentrate the behavioral signal) most. The purer the behavioral bet,
the harder the regime flip hurt.

## Honest caveats (cutting both ways)

- **Small sample.** 10 rebalances (~6 months) is very noisy; one adverse
  regime dominates. This does NOT prove the factors are permanently
  broken — it proves they **did not confirm** out-of-sample, and in fact
  reversed, in the one fresh window available.
- **Fundamentals carried forward** from end-2025 (Q1-2026 reports not
  incorporated) — affects only the handful of value/quality factors, not
  the price/volume majority driving the result.
- **The spent-holdout numbers are now reframed.** The composite ICs of
  0.10–0.11 on 2024–25 (and the strong 2017–2021 IS) came from
  reversal-friendly regimes. 2024–25 and the mining window were NOT
  independent of the behavioral thesis; H1 2026 was the first test of a
  different regime, and the edge did not generalize.

## Implication

The honest bottom line for the whole project: **these factors encode a
real but regime-contingent behavioral signal, not a robust all-weather
alpha.** They worked when reversal/anti-speculation paid (most of
2017–2025) and reversed when it didn't (H1 2026). Any live use needs a
regime filter or a market-neutral construction that does not bet the
whole book on the behavioral direction — and far more than 6 months of
live data before trusting the direction again.
