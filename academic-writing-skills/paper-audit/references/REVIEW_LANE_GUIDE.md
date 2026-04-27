# Review Lane Guide

Default `deep-review` lanes:

## Section lanes

- `section_intro_related`
  - check framing, novelty positioning, and promises made early in the paper
- `section_methods`
  - check definitions, assumptions, derivations, and method detail
- `section_results`
  - check metric computation, evidence sufficiency, and comparison fairness
- `section_discussion_conclusion`
  - check interpretation, limitation handling, and claim closure
- `section_appendix`
  - check whether appendix material supports or contradicts headline claims

## Cross-cutting lanes

- `claims_vs_evidence`
- `notation_and_numeric_consistency`
- `evaluation_fairness_and_reproducibility`
- `self_standard_consistency`
- `prior_art_and_novelty_grounding`
- `pre_submission_readiness` (full/editor focus only; populated from high-signal
  `PRESUBMISSION` script findings)

## Output rule

Every lane must output JSON findings matching `ISSUE_SCHEMA.md`.

`pre_submission_readiness` is intentionally narrow. It can contain Critical or
Major mechanical issues such as em dashes, repeated AI-tone vocabulary,
abstract result gaps, or source hygiene problems, but it must not absorb
methodology, theory, literature, or claim-validity reviewer work. When
`--focus methodology|theory|literature|logic` is selected, keep these findings
only in Phase 0 automated context.
