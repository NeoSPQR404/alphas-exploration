# canonical_composite — composition factors split from canonical

Created 2026-07-09 by splitting the canonical set: all factors with
family `composition` (11 demeaned-rank pair products) or `composition3`
(15 three-way products) — 26 total, accepted in canonical rounds 7–9.
The parent individual factors remain in `sets/canonical/` (80 factors).

## Contents

| file | what |
|---|---|
| `alpha_set.json` / `.csv` | 26 factors (names keep original `calpha_NNNN` ids; `next_id` = 1000 to avoid collisions) |
| `experience_memory.json` | composition round logs 7–9 + the 5 composition patterns, split from canonical's memory (stubs left there to preserve round numbering) |
| `rounds/round_07..09.{md,json}` | the composition rounds' full reports |
| `holdout/round_07..09.json` | per-round holdout snapshots at acceptance |

Values: `data/mining/alpha_values_canonical_composite/` (local).
Round numbering follows the original canonical sequence (7–9).
The pre-split canonical honest test (`sets/canonical/holdout/
full_set_eval.json`) covered all 105 factors including these 26 —
headline there: 3-way products were the STRONGER tier on 2024–25
(median |IC| 0.058 vs 0.052 set-wide).
