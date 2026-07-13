# rounds/ — per-round candidate files (the Generate step)

Each file defines `CANDIDATES = [{name, expr, family, rationale,
logic_score}, ...]`, plus optional `SET_NAME` and `FIELD_WHITELIST`.
Run with `python3 code/mining/round.py rounds/<file>.py`.

## Naming → which set
| pattern | set (`SET_NAME`) |
|---|---|
| `roundNN_candidates.py` | behavioral_full (`"main"`, full vocabulary) |
| `canonical_roundNN_candidates.py` | canonical (individual, 8-field whitelist) |
| `composite_roundNN_candidates.py` | canonical_composite (rank products of canonical parents) |

## Current state
- `round01`–`round12` → behavioral_full (105 factors, campaign complete).
- `canonical_round01`–`18` → canonical (105 factors: transfer, novel,
  composition, then the day-type / pin / true-gap / at-extreme novelty
  runs).
- `composite_round01`+ → canonical_composite (fresh campaign, 24 factors).

Expressions eval in a sandbox of `operators.OPERATORS` + panel fields;
`FIELD_WHITELIST` (when set) is AST-enforced so a canonical candidate
cannot touch turnover/flow/limit fields. Write candidates AFTER reading
the target set's experience_memory.json.
