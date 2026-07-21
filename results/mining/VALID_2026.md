# Which alphas are valid AND efficient in 2026 — per-factor screen

Run 2026-07-21 (`code/valid_2026_screen.py`). Every active factor in all three
sets (329 total) was recomputed from its expression over the 2017-2026 panel
(stored values stop at 2025) and scored on the genuinely-unseen 2026 window
(H1 2026, 115 trading days, ~11 rebalances):

- **valid** — still predicts in its stored direction: `sign(IC_2026) ==
  direction` AND `|IC_2026| >= 0.03` (the project's IC bar).
- **efficient** — survives its OWN turnover cost *standalone*: top-decile
  long-excess-vs-universe net of 15bp round-trip turnover cost > 0 (the
  tradable leg; A-share short leg is unshortable). This is the
  `cost_aware` metric — measured on the raw factor, since neutralization is a
  composite overlay, not a per-factor property.

## Headline

| | count |
|---|---|
| factors screened | 329 |
| **valid** (still predictive in 2026) | 111 (34%) |
| **efficient** (tradable net of cost) | 34 (10%) |
| **valid AND efficient** | **29** → **24 distinct signals** |

Validity is common (a third of factors still predict); **efficiency is the
binding constraint** — most valid factors churn too much to survive costs
standalone. The screen's real job is the efficiency filter.

| set | n | valid | efficient | both |
|---|---|---|---|---|
| behavioral_full | 105 | 49 | 20 | **18** |
| canonical | 105 | 57 | 12 | 11 |
| canonical_composite | 119 | 5 | 2 | **0** |

behavioral_full and canonical overlap heavily (cross-set rank corr 0.96, see
META_COMPOSITE.md) — the same overnight/event signals appear in both, so 29
survivors collapse to **~24 distinct signals**. **The rank-product composites
(canonical_composite) have zero survivors** — high turnover + weak 2026 IC make
them cost-fragile, consistent with COST_ANALYSIS.md.

## The valid + efficient alphas (distinct, by 2026 net-of-cost excess)

| 2026 sIC | net@15bp | turn | family | expression |
|---|---|---|---|---|
| +0.072 | **+46.6%** | 0.67 | overnight | `TsMed(OPEN/Delay(CLOSE,1)-1, 20)` |
| +0.050 | +31.2% | 0.41 | overnight | `TsSum(OPEN/Delay(CLOSE,1)-1, 60)` |
| +0.051 | +19.5% | 0.42 | overnight | `TsMed(OPEN/Delay(CLOSE,1)-1, 60)` |
| +0.077 | +19.3% | 0.38 | event | `-TsCount((HIGH/LOW-1) > 2*TsMean(HIGH/LOW-1,60), 120)` |
| +0.077 | +17.2% | 0.38 | event_freq | `-TsCount(AMP > 2*TsMean(AMP,60), 120)` |
| +0.064 | +14.6% | 0.44 | event_freq | `-TsCount(VR > 2, 60)` |
| +0.077 | +12.0% | 0.36 | volume | `-TsCount(VOLUME/TsMean(VOLUME,60) > 2, 120)` |
| +0.053 | +8.3% | 0.60 | flow | `-TsCorr(MF_LG_NET, CLOSE/VWAP-1, 20)` |
| +0.042 | +7.7% | 0.46 | divergence | `-TsCorr(RET, BENCH_RET, 60)^2` |
| +0.049 | +7.5% | 0.30 | overnight | `TsMed(OPEN/Delay(CLOSE,1)-1, 120)` |
| +0.053 | +6.8% | 0.36 | flow | `-TsCorr(MF_LG_NET, CLOSE/VWAP-1, 60)` |
| +0.068 | +6.4% | 0.74 | volume | `-(TsStd(VOLUME,20)/TsMean(VOLUME,20))` |
| +0.059 | +4.8% | 0.48 | event | `-TsCount((HIGH/LOW-1) > 2*TsMean(HIGH/LOW-1,60), 60)` |
| +0.065 | +4.7% | 0.75 | turnover | `-(TsStd(TURN_F,20)/TsMean(TURN_F,20))` |
| +0.060 | +3.0% | 0.52 | moneyflow | `-TsCorr(MF_LG_NET, RET, 20)` |

(Full 24 in `valid_2026_screen.json` → `survivors`.) Scatter:
`figs/fig_valid_2026.png`.

## What survives, and why

1. **The single best alpha in 2026 is overnight-gap persistence.**
   `TsMed(OPEN/Delay(CLOSE,1)-1, 20)` — the median close-to-open return over
   20 days — is #1 (net +46.6%/yr), and four of the top ten are the same
   `OPEN/Delay(CLOSE,1)-1` signal at different windows. **This directly
   confirms the GTJA-191 finding** ([[project_gtja191_research_tushare]]): the
   A-share price-volume edge is fundamentally an *overnight* effect. Trading
   the *persistence* of the overnight gap is both predictive and tradable
   (turnover 0.30-0.67), unlike trading the gap itself.

2. **Event-rarity / "calm" signals are the other robust, low-turnover
   winners.** `-TsCount(...spike... , 120)` families (extreme range, amplitude,
   volume, volume-ratio spikes) say *stocks without recent extreme events
   outperform*. Low turnover (0.36-0.44), high validity (sIC 0.064-0.077) →
   very efficient.

3. **Efficiency, not validity, is the filter.** Among *all* valid factors the
   biggest families are asymmetry (13) and lottery (12) — but those churn hard
   (turnover 0.7-0.8) and are eaten by costs, so almost none are efficient.
   The efficiency screen shifts the winners decisively toward
   **overnight + event-rarity + moneyflow-divergence**, the low-turnover veins.

## Recommendation

- **A deployable 2026 book is the ~10-12 low-turnover survivors** — overnight-gap
  persistence + event-rarity + large-order-flow divergence — equal-weighted.
  These are the alphas that are simultaneously still predictive and still
  tradable after costs.
- **Drop the rank-product composites for standalone trading** (0 survivors).
- **Overnight gap is the thesis to build the next round around** — it is the
  most robust vein across both this screen and the GTJA-191 reproduction.
- Re-run each period: `python3 code/valid_2026_screen.py` (screen) +
  `python3 code/fig_valid_2026.py` (scatter).
