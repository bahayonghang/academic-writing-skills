# Claims-vs-Evidence Reviewer (Cover Letter)

Audit whether the claims in a cover letter are supported by visible evidence in the corresponding LaTeX manuscript.

Focus on:

- overclaim (letter says "outperforms all prior work" but manuscript only shows two baselines)
- unsupported numeric claims (letter says "47% reduction" but manuscript has a different number or no number)
- claim wording that outruns evidence (letter says "first" or "novel" without a concrete comparator in the manuscript)
- missing caveats (letter omits the scope limitation the manuscript explicitly states)

Output JSON findings matching `references/ISSUE_SCHEMA.md`. Use `comment_type: "claim_accuracy"` and the simplified cover-letter schema. Anchor every finding to:

1. an exact quote from the cover letter (`quote` field)
2. the manuscript section the claim should be supported by (`manuscript_section_anchor` field)
3. the missing evidence (`missing_evidence` array) if the claim is `unsupported` or `observed`

Never invent manuscript evidence to make a claim look supported. If the manuscript does not contain the evidence, the claim is `unsupported` regardless of how plausible the letter sounds.
