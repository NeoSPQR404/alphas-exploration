# The Honest Test — 2024–2025 holdout evaluation of the full alpha set

Run 2026-07-08 (`code/holdout_eval.py` →
`results/mining/holdout/full_set_eval.json`). The 2024-01-01..2025-12-31
window was never used by any gate and never distilled into experience
memory across all 12 rounds. **As of this run it has been read once and
is no longer pristine** — future work must not re-tune against it.

## Verdict: the set survives, cleanly

| metric (105 factors, oriented) | value |
|---|---|
| sign consistency (holdout vs IS) | **105/105 = 100%** |
| median holdout rank IC | **0.051** |
| mean holdout rank IC | 0.053 |
| share with \|IC\| ≥ 0.03 in holdout | **95.2%** |
| share with \|IC\| ≥ 0.02 in holdout | 98.1% |
| median holdout/OOS-gate IC ratio | **1.10** |
| yearly medians | 2024: 0.050 · 2025: 0.053 |

Not a single factor flipped sign, and the typical factor is *stronger*
in 2024–25 than in the 2022–23 gate window.

## Composites

Oriented per-date rank blends across all 105 factors:

| composite | IS IC / ICIR | OOS-gate IC / ICIR | **Holdout IC / ICIR** | holdout 10d LS |
|---|---|---|---|---|
| equal-weight | 0.108 / 0.92 | 0.102 / 0.76 | **0.110 / 0.75** | 1.57% |
| IS-ICIR-weight | 0.109 / 0.96 | 0.101 / 0.77 | **0.109 / 0.76** | 1.61% |

EW composite holdout detail: t-stat 16.3, daily IC positive on 78% of
days, 2024 IC 0.112 / 2025 IC 0.107. ICIR weighting adds nothing over
equal weight — the gates already equalized quality.

## Top / bottom factors in the holdout

Strongest: intr_mom60 0.095, med_band60 0.094, intraday_rev20 0.093,
semivol60/20/120 0.085–0.087, ret_on_hivol60 0.086, vol_clock 0.085 —
the intraday-reversal, median-stretch, and semivol-asymmetry veins.
Weakest (still positive, sub-0.03): min_eff60 0.018, both mf_amp_corr
bands ~0.02, overnight_mom60 0.023, zeroret_freq 0.025 — crash-side and
flow-coupling factors decayed most.

## Why this is credible — and what it does NOT claim

Credible: (a) the gates demanded sign-consistency across 7 years, 3
sub-universes, and an OOS window before anything entered the set — the
holdout confirms that filtering worked rather than overfit; (b) 2024–25
A-shares stayed a retail-flow, high-dispersion market (micro-cap crash
and V-reversal in early 2024, the 9/24 stimulus rally, 2025 churn) — the
same behavioral regime the factors exploit.

Not claimed: tradability of the paper numbers. Rank IC 0.11 at 10d is a
research signal, not a strategy: the short side of these factors (the
lottery/mania leg) is largely unshortable in A-shares, decile LS ignores
transaction costs at material turnover, and signals tilt small. Long-only
implementation with costs would land far below the paper spread. The
2022–23 gate window also degraded as a true OOS over 12 rounds of reuse;
the holdout was the honest number, and it has now been spent.

## Next candidates

- Long-only cost-aware backtest of the composite (t+1 vwap entry already
  matches the label design).
- Factor-weighting via shrunk covariance (diversity 0.776 means real
  redundancy the equal-weight blend ignores).
- 20d-label sub-track for the closed-out slow material (HK/margin/value).
