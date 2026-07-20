# The 2026 out-of-sample test — the factor edge DEGRADED sharply (not a clean reversal)

Run 2026-07-16 on **genuinely unseen data**: the 2026 window (Jan 5 →
Jun 24, 10 rebalances) was fetched fresh from tushare and had never
touched any gate, distill, holdout, or backtest. Unlike the spent
2024–25 holdout, this is the first real out-of-sample evidence in the
project. `code/backtest_2026.py` recomputes every factor from its stored
expression over the 2017–2026 panel and evaluates each set's EW
oriented-rank composite on 2026 only.

> **CORRECTION (2026-07-16, after computing daily IC).** An earlier
> version of this note titled the finding a "reversal / inversion" based
> only on the decile backtest. Computing the composite's **daily rank IC**
> shows it stayed **weakly POSITIVE** in 2026 (behavioral_full +0.065,
> canonical +0.057, composite +0.025) vs ~0.10 historically. So the signal
> **degraded ~40–75% but did not cleanly reverse**. The decile inversion
> below is real on the sparse 10-rebalance grid but is dominated by the
> noisiest extreme deciles and a tiny sample; the daily IC (115 overlapping
> days) is the more reliable estimate. Reconciled verdict: **sharp
> degradation + failure to deliver tradable returns out-of-sample**, not a
> sign flip. Figures: `results/mining/figs/fig_ic_trajectory.png` (IC),
> `fig_decile_2026.png`, `fig_equity_2026.png`, `fig_excess_contrast.png`.

## Composite daily rank IC by window (the reliable estimate)

| set | IS 2017–21 | OOS 2022–23 | holdout 2024–25 | **2026** |
|---|---|---|---|---|
| behavioral_full | 0.108 | 0.102 | 0.106 | **+0.065** |
| canonical | 0.105 | 0.107 | 0.100 | **+0.057** |
| canonical_composite | 0.070 | 0.081 | 0.085 | **+0.025** |

## The tradable backtest (10 non-overlapping rebalances) nonetheless lost / inverted

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

## Reconciling the two metrics: degradation + a small-sample inversion

The daily IC (positive) and the decile backtest (inverted) disagree
because they measure different things. The daily IC uses all ~115
overlapping days and is the statistically reliable estimate — it says the
broad rank ordering kept weak positive power (~half of historical). The
decile/portfolio numbers use only the **10 non-overlapping rebalance
dates** and are driven by the **extreme deciles** (D1/D10), which are the
noisiest cells; on that sparse grid the tradable book lost and the deciles
inverted. Both are "true," but the honest headline is **sharp degradation
that failed to deliver tradable returns**, not a clean sign flip.

The market context explains the degradation: CSI300 (large caps) −5.8%
while the equal-weight universe +3.0% → a **small-cap / speculative
regime** in which the recent-winner, high-lottery, high-turnover names
these factors FADE were what led. The effect **strengthens with signal
concentration**: behavioral_full (broadest, some value/quality) degraded
least; canonical more; composite (rank-products concentrating the
behavioral bet) most (IC 0.085 → 0.025, and the worst tradable loss).

## Honest caveats (cutting both ways)

- **Small sample.** 10 rebalances (~6 months) is very noisy; one adverse
  regime dominates. This does NOT prove the factors are permanently
  broken — it proves they **did not confirm** out-of-sample (IC roughly
  halved) and **failed to deliver tradable returns** in the one fresh
  window available.
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
2017–2025) and degraded sharply — losing tradable value — when it didn't
(H1 2026), though without a clean daily-IC sign flip. Any live use needs a
regime filter or a market-neutral construction that does not bet the
whole book on the behavioral direction — and far more than 6 months of
live data before trusting the direction again.
