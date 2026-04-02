# Troubleshooting

## I ran `audit.py --mode deep-review` but did not get `final_issues.json`

That command only runs Phase 0 automated audit.

To complete deep review, you still need:

1. workspace preparation
2. reviewer lanes
3. consolidation
4. quote verification
5. final report rendering

## I only have a PDF

This is supported, but less reliable for:

- formulas
- notation-heavy derivations
- fine-grained structure

Use `.tex` or `.typ` when possible.

## Why does deep review still show score summaries if scores are no longer the main product?

Scores are retained as summary indicators and for compatibility. The primary product is the structured issue bundle and roadmap.

## When should I use `quick-audit` instead of `deep-review`?

Use `quick-audit` when:

- you want a fast readiness pass
- you only need script-backed findings
- you want to decide whether a deeper review is worth running

Use `deep-review` when:

- you need reviewer-style critique
- you care about claim validity and comparison fairness
- you need revision planning, not just diagnostics

## Why are `self-check` and `review` still accepted?

They are compatibility aliases:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

Use canonical names in all new commands and docs.

## The report is missing reviewer lanes

This usually means the outer skill workflow did not dispatch section or cross-cutting lanes, or their JSON outputs were never written into `comments/`.

## I do not see `committee/consensus.md` in deep-review outputs

Deep-review now writes `committee/consensus.md` automatically.

If it is missing, check:

- whether the run completed (not interrupted mid-workflow)
- whether the workspace path is the one you are inspecting
- whether file permissions blocked writing under `committee/`

## Why is my committee score capped at `4.0`?

If editor verdict is `Desk Reject`, the score is intentionally capped at `4.0` even if issue deductions alone would be higher.
This is a policy guardrail to keep desk-reject signals visible in the final consensus.

## Quote verification failed

Check:

- whether the quote came from OCR noise
- whether the reviewer paraphrased instead of quoting exactly
- whether the paper text in the workspace matches the paper the reviewer read
