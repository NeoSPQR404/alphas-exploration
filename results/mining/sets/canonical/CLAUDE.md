# canonical — individual factors, 8-field vocabulary (code arg `"canonical"`)

105 individual factors using **only** OPEN/HIGH/LOW/CLOSE/VOLUME/AMOUNT/
VWAP/RET (AST-enforced whitelist). Composition factors were split out to
`../canonical_composite/`; this set holds single-expression factors only.

## Campaign arc (rounds 1–18)
- **1–9**: transfer from behavioral_full + novel canonical constructs +
  composition (later split out).
- **10**: individual-only after the split; suggested exhaustion.
- **11–15** (novelty experiment): found ONE new vein — joint-condition
  **day-types** (dip-buy/capitulation), 8 accepts.
- **16–18** (extended, 40/round, terminated early): 17 accepts across new
  classes — vwap-pins/dojis, true gaps/islands, at-extreme textures,
  acceleration, dollar-share.

## Headline results
- **Honest test** (2024–25, spent as of cR9 — factors accepted after
  cR10 are NOT holdout-tested): median IC 0.052, EW composite 0.112 —
  slightly EXCEEDS the full-vocabulary set; 3-way compositions were the
  strongest tier out-of-time.

## Generator laws (in experience_memory.json)
Novelty = untouched structural CLASS, not new formulas in old classes.
Jitter thresholds not just windows. Magnitude-on-type > count-of-type.
One representative per event type; monotone transforms of residents
corr-lock.
