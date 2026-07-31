# Walk-forward validation of factor selection

Run 2026-07-21 (`code/walkforward.py`). The EW composite has no fitted weights, so
the only overfitting source is **factor selection** (which factors are in the
set). This simulates production honestly: at each yearly test block, select the
top-K factors by IC on the **expanding, past-only** training window (oriented by
the *train-window* sign — never the stored full-sample direction), then measure
their IC on the **never-seen** test year. Pool: behavioral_full (112, stored raw
values); test years 2019–2025.

## Result — selection generalizes; small haircut; positive every year

| K | mean IS IC | mean OOS IC | haircut | positive years |
|---|---|---|---|---|
| 10 | +0.0799 | **+0.0700** | 0.88 | **7/7** |
| 20 | +0.0745 | +0.0667 | 0.90 | 7/7 |
| 30 | +0.0700 | +0.0624 | 0.89 | 7/7 |
| 50 | +0.0634 | +0.0576 | 0.91 | 7/7 |
| all 112 | +0.0508 | +0.0491 | 0.97 | 7/7 |

Per-year OOS IC (K=30): 2019 +0.062 · 2020 +0.056 · 2021 +0.057 · 2022 **+0.071**
· 2023 +0.066 · 2024 +0.069 · 2025 +0.057.

**Three clean conclusions:**

1. **The selection process generalizes.** Realized OOS IC is **88–97% of
   in-sample** — only a ~10% overfit haircut. Selecting factors by past IC
   produces genuine forward edge, not noise-chasing.
2. **Positive in every test year (7/7)**, including the 2022–23 bear (2022 OOS IC
   +0.071 even *exceeded* its in-sample). Remarkably stable.
3. **Selection adds value.** Top-10 factors realize OOS IC **+0.070** vs +0.049
   for all 112 — the best-on-past factors stay best forward; picking a tight set
   improves the realized signal.

## Why this matters — the bias-free number

This is the trustworthy forward estimate the selection-biased artifacts lacked.
Recall robust_2026's 2026 +23% was inflated because factors were picked *using*
2026 data. Here nothing is ever tested on its selection window, so **~0.06–0.07
OOS IC (top-K) is the honest expectation** for the selection process.

**Reconciliation with 2026:** the walk-forward OOS IC (~0.06) is fully consistent
with the *neutralized* composite's actual 2026 IC (+0.073, IC_MONITOR/NEUTRALIZE).
So the signal's IC generalized even into 2026 — the 2026 *portfolio* loss was a
construction/tail/regime effect (which neutralization halved), **not** IC decay.
The walk-forward confirms the underlying edge is real and stable.

## Caveats

- Measures selection generalization at the **factor-IC** level; a composite of the
  correlated top-K realizes somewhat lower diversified IC (redundancy), but the
  sign, stability, and haircut conclusions hold.
- Expanding window; all test years are pre-2026 (stored values stop at 2025). The
  genuine forward test remains 2026 H2 / 2027 on the frozen sets.
- Rolling (trailing-window) and composite-level walk-forward are natural
  extensions.

Graph: `figs/fig_walkforward.png`. Data: `walkforward.json`.
