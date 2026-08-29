# EN density conversion contract

## Canonical denominator

The C1 runtime counts visible English words with `\b[A-Za-z][A-Za-z'-]*\b` after parser-based
visible-prose extraction. Hyphenated and apostrophe words count as one token. `\S+` is not an
accepted alternate denominator.

## Baseline conversion

For a legacy per-document cap `A`, C3 stores density `2A` per 10,000 visible words:

| Visible words | Effective words | Allowance | Interpretation |
| ---: | ---: | ---: | --- |
| 1499 | 1500 | `ceil(0.3A)` | short-document fallback |
| 1500 | 1500 | `ceil(0.3A)` | fallback boundary |
| 5000 | 5000 | `A` | only exact legacy-equivalence point |
| 10000 | 10000 | `2A` | intentional density scaling |

The regression must check both `count == allowance` and `count == allowance + 1`. It must not claim
that arbitrary documents retain legacy behavior.

The old throat-clearing allowance 1 is converted by the same 5000-word baseline to 2.0/10k words,
with `min_budget=1`.

## Missing evidence

No 5–10-paper target-venue corpus is available. Density values are baseline conversions, not corpus
calibration. The borrowed organization factor, P-ARC N/τ, and all real-paper precision/recall claims
remain **UNVERIFIED** until the author supplies a suitable corpus.
