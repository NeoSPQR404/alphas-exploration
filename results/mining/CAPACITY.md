# Capacity-aware cost model

Run 2026-07-21 (`code/capacity_model.py`). Turns the deployable book's IR 1.69 /
+9% gross excess into a **deployable-AUM** number by modelling market impact that
scales with position size vs liquidity.

Book = robust_2026 neutralized composite, buffer 2.5, top-decile EW **long** (565
names avg, turnover 0.25). Frictionless gross long-excess **+9.2%/yr**.

## Cost model (transparent, recalibratable)

| component | assumption |
|---|---|
| commission | 2.5 bp / side |
| half-spread | 5 bp / side |
| stamp duty | 5 bp, **sell-side only** (A-share 印花税) |
| market impact | **square-root law**: impact_bp = Y·√(trade_value / ADV), capped 300bp |
| impact coef Y | **120bp** base (80 optimistic / 180 pessimistic) at 100% ADV participation |
| ADV | trailing-20d median dollar volume per name |

Position = AUM / N (EW); at each rebalance we buy the entries and sell the exits.
Cost is aggregated per-name, so the **least-liquid holdings dominate** as AUM grows.

## Capacity curve — net long-excess (ann) vs AUM

| AUM (CNY) | optimistic | **base** | pessimistic |
|---|---|---|---|
| 0.1B | +7.0% | **+6.6%** | +6.1% |
| 0.3B | +6.4% | +5.8% | +4.8% |
| **1B** | +5.4% | **+4.2%** | +2.5% |
| **3B** | +3.7% | **+1.7%** | −1.2% |
| 10B | +0.4% | −3.0% | −7.9% |
| 30B | −4.6% | −10.0% | −16.0% |
| 100B | −12.9% | −18.5% | −22.4% |

## Findings

- **Fixed costs alone take +9.2% gross → +6.6% net** at tiny AUM (commission +
  spread + stamp at turnover 0.25). That is the realistic small-book ceiling.
- **Half-alpha capacity ≈ 3B CNY** (base impact); **net-excess breakeven ≈ 4–5B**.
  Sensitivity: breakeven ~2–3B (pessimistic) to ~10B (optimistic).
- **Comfortably deployable to ~1–3B CNY** (net +4.2% at 1B, +1.7% at 3B base). At
  institutional scale (>10B) the impact — dominated by the small-cap holdings —
  turns the alpha negative.

## Caveats & levers

- **Capacity is limited by the small-cap holdings.** The size filter was dropped
  because the edge lives partly in small caps (NEUTRALIZE_REPORT); that same
  choice caps capacity. A capacity-conscious variant — position-size caps at
  x% of ADV, or a mild size tilt — trades some alpha for materially more
  capacity, and is the natural next study.
- **Long-only** (A-share short leg untradable); this is the long-book capacity.
- **Y (impact coef) is the key uncertain input** — the band shows its effect;
  recalibrate with real fills / broker TCA before sizing.
- Turnover 0.25 already reflects the buffer overlay (TURNOVER_OVERLAY); without it
  turnover ~0.45 would roughly halve every capacity figure.

## Bottom line

IR 1.69 is real but **capacity-limited to ~1–3B CNY** for this small-cap-inclusive
long book. It suits a boutique / early-stage mandate; scaling past ~5B needs a
capacity-conscious construction (ADV-capped weights or a size tilt), an
index-futures-hedged variant, or accepting a lower net alpha.

Graph: `figs/fig_capacity.png`. Data: `capacity_model.json`.
