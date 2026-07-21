# robust_2026 — backtest

Run 2026-07-21. EW rank composite of the 24 curated factors, size+industry
**neutralized**, status-only investable universe, 10-day rebalance, t+1 vwap
entry, 15/30bp costs. Historical from `backtest_composite.py robust_2026 neutral`
(stored values, 2017-25); 2026 from `neutralize_eval.py robust_2026` (recomputed
2017-2026).

## Historical (2017-2025) — the fair estimate

| window | excess vs universe (ann / IR) | long-only net@15bp (ann / Sharpe / maxDD) | LS gross Sharpe |
|---|---|---|---|
| **full** | **+10.2% / 1.74** | +14.2% / 0.62 / −35% | 2.58 |
| IS 2017-21 | +11.7% / 2.12 | +11.4% / 0.56 | 3.45 |
| OOS 2022-23 | +11.3% / 1.67 | +4.4% / 0.17 | 1.79 |
| holdout 2024-25 | +5.5% / 0.95 | +33.3% / 1.26 | 1.79 |

- Decile curve monotone: `−0.47 … +0.77` (%/rebalance). Turnover ~45%/rebalance.
- LS gross **positive every single year** (2017-2025, +14% to +48%).
- Excess-vs-universe IR **1.74** — meaningfully sharper than the full
  behavioral_full set (IR 1.09): the curated book is the cream.

## 2026 (fresh window, 10 rebalances)

| variant | 2026 long excess | 2026 LS gross | 2026 daily IC |
|---|---|---|---|
| raw | +27.5% | +83.7% | +0.116 |
| **neutralized** | **+23.4%** | +69.2% | **+0.111** |

vs the source sets in 2026 (neutralized): behavioral_full **−2.7%** (IC 0.073),
canonical −7.5%, canonical_composite −15.6%. The curated book turns the parent's
2026 loss into a large gain.

## ⚠️ Read the 2026 number honestly — selection bias

**The +23.4% 2026 figure is optimistically biased and is NOT a forward
expectation.** 19 of the 24 factors were *selected because* they were valid and
efficient in 2026 (the VALID_2026 screen used 2026 data). Measuring them back on
2026 is in-sample to that selection. The tell-tale sign: the set's **2026 IC
(0.111) exceeds its historical IC (0.081)** — a genuinely robust set holds or
decays out-of-sample, it does not improve. That lift is the selection.

What is genuinely out-of-sample:
- The **5 newly-mined factors** (ralpha_0001-0005) were gated on 2017-25 only,
  then independently found robust in 2026 — a real (if small) OOS validation.
- The **historical +10.2% excess / IR 1.74** is the unbiased quality estimate,
  since selection used 2026, not the 2017-25 portfolio path.

**Bottom line:** robust_2026 is a genuinely strong, sharp historical book
(IR 1.74, monotone, LS positive every year) and its construction principle —
low-turnover activity-stability + event-rarity, cost-aware, non-overnight — is
sound. But treat the forward expectation as the **historical ~+10% excess,
haircut for the general post-2017 decay**, not the selection-inflated +23%. The
clean forward test is the *next* fresh window (2026 H2 / 2027), on this frozen
set.

Graph: `results/mining/figs/fig_robust_2026_backtest.png`. Detail:
`backtest_neutral.json`, `neutralize_eval.json`.
