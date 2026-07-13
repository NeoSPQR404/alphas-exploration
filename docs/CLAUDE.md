# docs/ — methodology notes

- `STEP1_DATA_AUDIT.md` — the Step-1 data build: tushare endpoint audit,
  gap-filling, the cleaned 2017–2025 mining base (10.6M rows × 89 cols),
  suspension-aware PIT labels, tradability flags.
- `STEP2_MINING_SYSTEM.md` — the mining system design: operator set,
  AlphasEval metrics, the 4-stage pipeline with all gate thresholds
  (incl. the rolling + bootstrap stage-4 additions), holdout policy,
  the flow-field base extension, and known caveats.

These are the authoritative design references. When the pipeline gates
or stage definitions change, update `STEP2_MINING_SYSTEM.md` to match.
