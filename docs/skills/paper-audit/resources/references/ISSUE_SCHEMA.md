# Issue Schema

Canonical schema for `deep-review` findings.

```json
{
  "title": "short issue title",
  "quote": "exact quote from paper",
  "explanation": "reasoned explanation",
  "comment_type": "methodology|claim_accuracy|presentation|missing_information",
  "severity": "major|moderate|minor",
  "confidence": "high|medium|low|unverified",
  "source_kind": "script|llm",
  "source_section": "methods",
  "related_sections": ["results", "appendix"],
  "root_cause_key": "normalized-shared-key",
  "review_lane": "claims_vs_evidence",
  "evidence_anchor": [
    {"type": "citation|figure_or_table|metric|section|analysis_artifact", "text": "visible anchor"}
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific support that is absent or unverified"],
  "allowed_wording": "bounded wording that stays within the evidence",
  "forbidden_wording": ["unbounded wording that would require stronger evidence"],
  "gate_blocker": false,
  "quote_verified": true
}
```

## Required fields

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `source_kind`

## Guidance

- `root_cause_key` should stay stable across re-audits when the same issue persists.
- `gate_blocker` is only for issues that should fail a submission gate.
- `quote_verified` should be added after running `verify_quotes.py`.
- `evidence_anchor`, `claim_strength`, `missing_evidence`, `allowed_wording`, and
  `forbidden_wording` are optional claim-evidence fields. Add them when the issue
  is about claim accuracy, citation support, figure/table evidence, or data
  availability. Do not make them required until downstream consumers explicitly
  version the schema.
- `confidence` follows an ordered ladder `high > medium > low > unverified`.
  `unverified` is reserved for findings whose anchor quote could not be located
  in the source. Running `verify_quotes.py --write-back` will demote any issue
  with `quote_verified=false` to `confidence: unverified` so downstream
  consolidation and reporting can treat it as evidence-deficient rather than
  silently keeping the original confidence label.

## Optional Bundle Wrapping

`final_issues.json` is normally a top-level list of the records above
(legacy schema, still the default produced by `consolidate_review_findings.py`).
For re-audit score tracking it MAY instead be a dict that wraps the same list
together with optional round-level metadata:

```json
{
  "issues": [ /* records as defined above */ ],
  "round_scores": {
    "quality": 78,
    "clarity": 73,
    "significance": 70,
    "originality": 75
  }
}
```

- `issues` is required when the dict form is used; consumers fall back to an
  empty list if absent.
- `round_scores` is optional. Keys are free-form dimension names (the
  4-dimension summary or the 9-dimension ScholarEval layer both work).
  Values must be numeric.
- `scripts/diff_review_issues.py` and `scripts/render_revision_trajectory.py`
  detect the dict form automatically. When neither bundle exposes
  `round_scores`, trajectory rendering is silently skipped instead of erroring.
