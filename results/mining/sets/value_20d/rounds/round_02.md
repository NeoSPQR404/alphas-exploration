# value_20d — Round 2

**Goal:** R1 kept one value-level factor; raw yields collapse into it. Mine
constructs DISTINCT from value-level: value×behavioral interactions, value/quality
change, value+size/growth blends. 13 candidates, HORIZON=20.

## Funnel

| stage | pass | note |
|---|---|---|
| candidates | 13 | — |
| S1 | 6 | value×behavioral interactions all **fail** (negative IC, as at 10d); value blends clear: sales_growth_cheap 0.040, quality_x_value 0.044, cheap_small 0.045, value_minus_shortmom 0.072, value_rerate_indneut 0.031 |
| S2 | 5 | quality_x_value locks (0.92 vs valpha_0001 — ROE×CFP ≈ value agreement) |
| S3 | 5 | — |
| S4 | **3** | value_rerate_indneut OOS 0.007 & ep_rerate_accel (OOS 0.002, mono −0.93) fail |

Accepted → valpha_0002 `CsRank(SP)+CsRank(Delta(SP,120))` (cheap+growing sales,
OOS 0.069), valpha_0003 `CsRank(EP)-CsRank(Log(CMV))` (cheap+small, OOS 0.067),
valpha_0004 `CsRank(EP)-CsRank(TsSum(RET,20))` (contrarian value, OOS 0.057).
Set 1 → **4**, diversity 0.83.

## 2026 cross-check (daily IC; efficiency unreliable at 20d)

| factor | IS | OOS | **2026 IC** |
|---|---|---|---|
| valpha_0001 | +0.052 | +0.024 | +0.023 |
| valpha_0002 | +0.044 | +0.069 | −0.013 |
| valpha_0003 | +0.029 | +0.067 | −0.007 |
| valpha_0004 | +0.078 | +0.057 | +0.006 |

**All four are strong 2017-25 but weak-to-negative in H1 2026** — value had a bad
2026 in A-shares (matches the 10d value result). Kept all 4: this is a value
sleeve (defined by 20d value strength), the 2026 window is only ~4 rebalances / 85
days, and value is cyclical — informative, not disqualifying.

## Outcome

`value_20d` = 4 distinct, historically-strong value factors at the 20d horizon
(value agreement, cheap-growth, cheap-small, contrarian value). Value is
genuinely orthogonal to the behavioral book and much stronger at 20d than 10d —
but currently in a value-unfriendly regime (2026). A promising diversifier to
blend with the behavioral sleeve over full history.
