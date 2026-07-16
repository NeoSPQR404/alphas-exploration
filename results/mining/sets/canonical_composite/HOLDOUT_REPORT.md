# canonical_composite — honest test (2024–2025 holdout)

Run 2026-07-10, `python3 code/holdout_eval.py canonical_composite` (119
rank-product compositions).

## Caveat — NOT an independent test

The composites are demeaned-rank products of the **canonical individual
factors, whose 2024–25 holdout was already read** (2026-07-09). A product
of parents whose out-of-sample behavior is known is not itself pristine
out-of-sample. Read this as a *mechanical consistency check* — "do the
compositions inherit their parents' holdout stability?" — not as new
evidence. The genuine out-of-sample test for any factor in this repo is
now live data.

## Result (119 factors, 2024–25)

| metric | value |
|---|---|
| sign-consistent (holdout vs IS) | **119/119 = 100%** |
| median holdout rank IC | 0.050 |
| share \|IC\| ≥ 0.03 | 92% |
| median holdout/OOS ratio | 1.04 |
| **EW composite holdout IC / ICIR** | **0.087 / 0.91** |
| EW composite t-stat / yearly | 19.8 / 2024 0.088 · 2025 0.086 |

The composite's per-factor IC (0.050 median) is *lower* than the
individual canonical set (compositions are diluted signals), but its
**composite ICIR 0.91 and t 19.8 are the highest of any set** — the
rank-products are more stable and mutually orthogonal, so they aggregate
into a smoother combined signal. Sign consistency is perfect, as expected
for products of already-consistent parents.
