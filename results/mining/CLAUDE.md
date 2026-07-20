# results/mining/ — factor sets and evaluation artifacts

Everything lives under `sets/`. Each set is self-contained: registry,
experience memory, per-round reports, holdout snapshots, and evaluation
reports. (Root-level result files were consolidated into
`sets/behavioral_full/` on 2026-07-09.)

| set | factors | vocabulary | code arg |
|---|---|---|---|
| `sets/behavioral_full/` | 105 | full (OHLCV + turnover/VR/amp + limit boards + moneyflow/northbound/margin + valuation + industry) | `"main"` |
| `sets/canonical/` | 105 individual | OHLCV/VWAP/AMOUNT/RET only (AST-enforced) | `"canonical"` |
| `sets/canonical_composite/` | 119 | rank-product compositions of canonical parents | `"canonical_composite"` |

Per-set files: `alpha_set.json` (+`.csv`), `experience_memory.json`,
`rounds/round_NN.{md,json}`, `holdout/round_NN.json` +
`full_set_eval.json`, and reports (`HOLDOUT_REPORT.md`,
`BACKTEST_REPORT.md`, `STAGE4_REEVAL.md`) where run.

Also here: `step1_audit.json`, `step1_base_validation.json` (data-build
artifacts). Factor values are NOT here — they live in
`data/mining/alpha_values*/` (git-ignored, float32, rebuildable).

Cross-cutting evaluation artifacts (all sets): `NEUTRALIZE_REPORT.md` +
`sets/*/neutralize_eval.json` (size+industry neutralization), `BACKTEST_2026.md`
+ `analysis_2026.json` (fresh-2026 OOS), `META_COMPOSITE.md` +
`meta_composite.json` (cross-set blend — negative result), `IC_MONITOR.md` +
`ic_monitor/<set>.json` (rolling-IC decay monitor), `figs/` (report graphs).

**Invariant:** every factor clears |rank IC| ≥ 0.03 in IS (2017–21) AND
OOS-gate (2022–23). The 2024–25 holdout is spent for behavioral_full and
canonical — never re-tune against it.
