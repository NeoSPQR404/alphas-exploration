# value_20d — 20-day value/fundamental sleeve

A dedicated **20-day-horizon** value set (prefix `valpha_`), separate from the
10d behavioral sets. Motivation: value/fundamentals are too weak at 10d
(robust_2026 R3-R4: orthogonal but sub-bar) but have real punch at a monthly
horizon. **This is the one place in the repo that gates on `fwd_ret_20d`.**

## Horizon mechanism

Each candidates file sets `cfg.HORIZON = 20` at module load. `round.py` runs the
candidates file (via `runpy`) *before* it reads `cfg.HORIZON`, and each round is a
separate process, so this scopes the 20d horizon to this sleeve without touching
the 10d sets. Any re-evaluation/backtest of this set must likewise set
`cfg.HORIZON = 20` first.

## Membership (4)

| factor | expr | IS IC | OOS IC | angle |
|---|---|---|---|---|
| valpha_0001 | `CsRank(EP) * CsRank(CFP)` | +0.052 | +0.024 | value agreement (cheap on E and CF) |
| valpha_0002 | `CsRank(SP) + CsRank(Delta(SP,120))` | +0.044 | +0.069 | cheap + growing sales |
| valpha_0003 | `CsRank(EP) - CsRank(Log(CMV))` | +0.029 | +0.067 | value + small size |
| valpha_0004 | `CsRank(EP) - CsRank(TsSum(RET,20))` | +0.078 | +0.057 | contrarian value (cheap, not run up) |

Gated on fwd_ret_20d, `GATE_ON_NEUTRALIZED` on (so these are size+industry-neutral
*residual* value), full S1-S4 suite, monotonicity ≥0.60. Diversity 0.83 — the four
are distinct value blends (raw yields all S3-collapse into one value signal).

## Findings

- **Value is much stronger at 20d than 10d** (IS/OOS 0.024-0.078 vs ~0.03), even
  after size+industry neutralization. It is genuinely orthogonal to the behavioral
  sets → a real diversifier.
- **But value lagged in H1 2026**: all four are weak-to-negative in the fresh 2026
  window (2026 daily IC +0.023 … -0.013). A-share value had a bad 2026 (matches the
  10d value result). Caveat: 2026 at 20d is a very short window (~4 rebalances / 85
  days) — informative but not a verdict; value is cyclical.
- Value × behavioral interactions (demeaned-rank) fail at 20d, same as 10d.

## Status / next

A legitimate historical value sleeve, currently in a value-unfriendly regime.
Natural next: an EW composite backtest at 20d (set `cfg.HORIZON=20` first), and a
behavioral+value blend to test whether the orthogonal value sleeve improves the
combined book's risk-adjusted return over full history.
