# Rolling-IC decay monitor

Run 2026-07-20 (`code/monitor_ic.py`). A first-class health artifact that
operationalizes *reduce conviction when the signal weakens* instead of
leaving it as a footnote. For each set it builds the recommended production
signal — the size+industry **neutralized** EW-rank composite — and tracks a
**120-trading-day trailing rank IC** against the in-sample (2017–21)
baseline, classifying the signal into health bands. The fresh-2026 reading
is the neutralized 2026 window IC from `NEUTRALIZE_REPORT.md`.

Built from the stored registry values (fast); IC series covers 2017–2025.

## Health bands (trailing IC ÷ baseline)

| band | ratio | action |
|---|---|---|
| **HEALTHY** | ≥ 0.60× | deploy at full conviction |
| **WATCH** | 0.30–0.60× | reduce conviction; investigate regime |
| **IMPAIRED** | 0–0.30× | halve/pause; signal barely predictive |
| **BROKEN** | ≤ 0 | stop; IC has flipped sign |

## Current state

| set | baseline IC | trailing IC (2025-12-31) | state | 2026 IC | 2026 state |
|---|---|---|---|---|---|
| **behavioral_full** | 0.105 | 0.087 (0.83×) | **HEALTHY** | 0.073 (0.70×) | **HEALTHY** |
| canonical | 0.100 | 0.075 (0.75×) | HEALTHY | 0.067 (0.67×) | HEALTHY |
| canonical_composite | 0.069 | 0.066 (0.97×) | HEALTHY | 0.033 (0.47×) | **WATCH** |

## Per-year mean IC (the decay table)

| set | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | **2026** |
|---|---|---|---|---|---|---|---|---|---|---|
| behavioral_full | .115 | .115 | .107 | .089 | .098 | .114 | .095 | .103 | .110 | **.073** |
| canonical | .107 | .106 | .097 | .088 | .102 | .111 | .105 | .103 | .101 | **.067** |
| canonical_composite | .053 | .069 | .081 | .058 | .079 | .094 | .080 | .070 | .091 | **.033** |

## Reading

1. **No secular decay through 2025.** The neutralized IC is flat-to-strong
   across 2017–2025 (behavioral_full 0.089–0.115, never trending down). The
   spent-holdout ICs were not a fluke of one regime — the *neutralized*
   signal held up in-sample every year.
2. **2026 is the first genuine below-baseline year, but not a break.** At
   0.70× / 0.67× baseline the two price/volume sets are degraded yet still
   in the HEALTHY band; **canonical_composite (0.47×) is the one in WATCH** —
   consistent with it being the weakest, most concentrated construction
   (worst 2026 backtest too).
3. **The signal has hit WATCH before and recovered.** Worst trailing IC was
   during COVID (2020-02, 0.45× baseline) and again in the 2022–23 bear
   (first WATCH breach 2023-06) — both transient dips that recovered to
   baseline. So a single soft reading is not an exit signal; a *sustained*
   sub-WATCH trajectory is.

## How to use it

- **behavioral_full / canonical:** deploy, but at **reduced conviction** —
  2026 sits at ~0.70× baseline, degraded but predictive. Full size only if
  the trailing IC climbs back above ~0.85× and holds.
- **canonical_composite:** **cut conviction now** (WATCH). Do not run it
  standalone at full size until it recovers above the 0.60× line.
- **Hard stop for any set:** trailing/window IC falls below the WATCH line
  (0.30× baseline) for a sustained stretch, or flips sign (BROKEN).
- **Re-run each rebalance** (`python3 code/monitor_ic.py [set]`); the 2026
  point should be refreshed from the latest neutralized window IC as new
  data lands.

Graph: `results/mining/figs/fig_ic_monitor.png`. Machine-readable state per
set: `results/mining/ic_monitor/<set>.json` (+ `summary.json`).
