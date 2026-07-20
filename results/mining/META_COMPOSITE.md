# Cross-set meta-composite — evaluation

Run 2026-07-20 (`code/meta_composite.py`). Blends the three sets'
**size+industry neutralized** EW-rank composites into a meta-signal, to test
whether the sets are diverse enough that combining them beats the best
single set. Backtest is the same neutralized construction as
`NEUTRALIZE_REPORT.md` (top-decile long over full-A tradable, per-date
neutralized signal), on the full 2017–25 and fresh 2026 windows.

## Verdict: the meta-composite does NOT help — the sets are too correlated

Blending dilutes the strongest set (behavioral_full) toward the weaker ones
instead of diversifying. **Use `behavioral_full` neutralized alone; do not
deploy a cross-set blend.**

## 1. The sets are not diverse

| pair | cross-sectional rank corr | daily-IC-series corr |
|---|---|---|
| behavioral_full ~ canonical | **+0.962** | **+0.979** |
| behavioral_full ~ canonical_composite | +0.645 | +0.889 |
| canonical ~ canonical_composite | +0.638 | +0.860 |

- **behavioral_full and canonical are the same signal** (+0.96 cross-
  section, +0.98 IC-timing). Canonical is the OHLCV-only reconstruction of
  the behavioral edge — it carries almost no independent information.
- **canonical_composite is only moderately decorrelated cross-sectionally
  (+0.64) but +0.86–0.89 correlated in IC *timing*** — it is built from the
  same parents, so it wins and loses on the same days. It cannot hedge the
  regime risk; it *amplifies* it (worst 2026 drawdown of the three).

Diversification requires low IC-timing correlation. None of these pairs has
it. The best pair (composite vs the others) still co-times at ~0.87.

## 2. The blend underperforms the best single set

full = 2017–25 (218 rebalances); 2026 = Jan–Jun (10 rebalances). exc =
top-decile long vs universe, ann; LS = long-short gross, ann; IC = daily
rank IC.

| variant | full exc | full IC | full ICIR | 2026 exc | 2026 LS | 2026 IC |
|---|---|---|---|---|---|---|
| **behavioral_full** | **+8.0%** | **0.105** | **0.86** | **−2.7%** | **−10.0%** | **0.073** |
| canonical | +6.1% | 0.102 | 0.79 | −7.5% | −23.3% | 0.067 |
| canonical_composite | +5.6% | 0.076 | 0.77 | −15.6% | −41.4% | 0.033 |
| meta (equal-weight) | +7.5% | 0.102 | — | −10.5% | −30.0% | 0.062 |
| meta (IR-weighted) | +7.5% | 0.102 | — | −10.4% | −29.9% | 0.063 |

- **Historically**, the meta (+7.5% exc / 0.102 IC) is *below*
  behavioral_full alone (+8.0% / 0.105). Averaging a strong signal with two
  correlated weaker ones can only pull it down.
- **In 2026**, the meta is *much worse* than behavioral_full alone (−10.5%
  vs −2.7% excess; −30.0% vs −10.0% LS). The blend imports
  canonical_composite's −41% collapse.
- **IR-weighting changes nothing**: the three sets have near-identical full
  ICIR (0.86 / 0.79 / 0.77), so the IR weights ≈ equal, and no weighting
  scheme can help when the components co-time.

## Why the ensemble intuition failed here

Ensembling diversifies only when components have **independent errors**.
These three sets were mined from overlapping vocabularies on the same panel
with the same label and gates, so they encode one underlying behavioral
factor (short-horizon reversal / small-cap-liquidity). Their IC series move
together (+0.86 to +0.98), so the blend has the *same* Sharpe and the *same*
regime exposure as its parts, minus the drag of averaging in the weaker
members.

## Recommendation

- **Do not deploy a cross-set meta-composite.** Ship `behavioral_full`
  neutralized as the single production signal — it dominates on every metric
  and window here.
- **canonical is redundant with behavioral_full** (+0.96); keep it only as
  the AST-clean research control, not as a diversifier.
- Real diversification needs a signal with **low IC-timing correlation** to
  the behavioral factor — a different *economic* family (quality/value,
  longer horizon, or a fundamentally-driven signal), not another
  price/volume recombination. That, plus the regime overlay from
  `NEUTRALIZE_REPORT.md`, is where independent risk would actually come
  from.

Detail (decile curves, cum returns, per-variant windows) in
`results/mining/meta_composite.json`.
