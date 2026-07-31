# rounds/ — per-round candidate files (the Generate step)

Each file defines `CANDIDATES = [{name, expr, family, rationale,
logic_score}, ...]`, plus optional `SET_NAME` and `FIELD_WHITELIST`.
Run with `python3 code/mining/round.py rounds/<file>.py`.

## Naming → which set
The **`SET_NAME` inside the file** is authoritative; the filename is just a
convention. Newer files set it explicitly (and 20d files also set `cfg.HORIZON=20`).
| pattern | set (`SET_NAME`) |
|---|---|
| `roundNN_candidates.py` | behavioral_full (`"main"`, full vocabulary) |
| `canonical_roundNN_candidates.py` | canonical (individual, 8-field whitelist) |
| `composite_roundNN_candidates.py` | canonical_composite (rank products) |
| `robust2026_rN_candidates.py` | robust_2026 (curated non-overnight set) |
| `value20dN_r{1,2}_candidates.py` | value_20d (20d value sleeve; sets `cfg.HORIZON=20`) |

## Current state
- `round01`–`round14` → behavioral_full (112 factors). R13-14 mined non-overnight
  veins (event-rarity, robust median/mean ratio); 5 winners moved to robust_2026.
- `canonical_round01`–`18` → canonical (105 factors).
- `composite_round01`+ → canonical_composite (119 factors).
- `robust2026_r1/r2` → robust_2026 (near-optimal; 2 rounds added only 1 factor).
- `value20d_r1/r2` → value_20d (4 value factors at 20d).

Expressions eval in a sandbox of `operators.OPERATORS` + panel fields;
`FIELD_WHITELIST` (when set) is AST-enforced so a canonical candidate
cannot touch turnover/flow/limit fields. Write candidates AFTER reading
the target set's experience_memory.json.
