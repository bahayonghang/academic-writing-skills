# CLI and Examples

All repository-local commands use:

```bash
uv run python ...
```

## Quick Audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
```

Use when you want a fast answer to:

- what blocks submission?
- what should I fix before a full review?
- are there final-week mechanical issues such as em dashes, AI-tone vocabulary, abstract result gaps, or LaTeX hygiene problems?

Direct mechanical checker:

```bash
uv run python academic-writing-skills/paper-audit/scripts/pre_submission_check.py paper.tex --json
```

## Deep Review

Minimal Phase 0 command:

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
```

Single-focus committee command:

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus methodology
```

Full deep-review sequence:

```bash
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex --output-dir ./review_results
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
uv run python academic-writing-skills/paper-audit/scripts/consolidate_review_findings.py ./review_results/paper-slug
uv run python academic-writing-skills/paper-audit/scripts/verify_quotes.py ./review_results/paper-slug --write-back
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py ./review_results/paper-slug
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py ./review_results/paper-slug --style peer-review
```

Reviewer-report-first natural-language request:

```text
Review this manuscript like an SCI journal reviewer and give me Summary, Major Issues, Minor Issues, and Recommendation.
```

The final reader-facing artifact for that request is `peer_review_report.md`, while `review_report.md` remains the richer evidence bundle.

Focused deep-review note: `PRESUBMISSION` findings stay in Phase 0 context for
`--focus methodology|theory|literature|logic` and do not pollute the focused
issue bundle.

## IEEE Gate

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
```

Use when you want:

- PASS / FAIL
- hard blockers
- advisory pseudocode guidance separated from blockers
- advisory `PRESUBMISSION` Major/Minor findings separated from blockers

## Re-Audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md
```

If you have old and new issue bundles:

```bash
uv run python academic-writing-skills/paper-audit/scripts/diff_review_issues.py old_final_issues.json new_final_issues.json
```

## PDF-Only Scenario

If source is unavailable:

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode quick-audit
```

Prefer source files when possible. PDF deep review is still useful, but OCR / extraction limitations reduce confidence for formula and notation-heavy papers.
PDF input runs text-only `PRESUBMISSION` checks and skips LaTeX/Typst source
hygiene.

## Example Natural-Language Requests

```text
Run a quick-audit on paper.tex and list blockers first.
```

```text
Run a pre-submission mechanical check three days before the deadline and flag AI-tone or em-dash issues.
```

```text
Deep-review this manuscript like a serious conference reviewer and focus on claim-evidence mismatch.
```

```text
Deep-review this manuscript with the full Academic Pre-Review Committee and rank the top 3 fixes first.
```

```text
Deep-review this manuscript but focus only on logic-chain breakpoints and causal inversions.
```

```text
Gate this IEEE paper and tell me whether the pseudocode still has hard violations.
```

```text
Re-audit this revised manuscript against my last report.
```
