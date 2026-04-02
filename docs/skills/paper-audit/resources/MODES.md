# Modes

## `quick-audit`

Use when:

- you want a fast readiness screen
- you want checklist, severity, and score indicators
- you are not ready to invest in a full reviewer workflow

Main output:

- script-backed audit report
- checklist items
- score summary

Recommended command:

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
```

## `deep-review`

Use when:

- you want reviewer-style critique
- you care about claim accuracy, methodology, fairness, and cross-section consistency
- you want a revision roadmap rather than only a score
- you want committee-style pre-review (`Editor -> Theory -> Literature -> Methodology -> Logic`)

Main output:

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `revision_roadmap.md`
- `committee/consensus.md`

Recommended command:

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review
```

Focus command (single dimension):

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus methodology
```

Important note:

`audit.py --mode deep-review` is Phase 0 only. Complete deep review also needs workspace prep, reviewer lanes, consolidation, and final rendering.

## `gate`

Use when:

- you want PASS / FAIL
- you only care about blockers
- you are running a submission gate or CI check

Main output:

- gate verdict
- blocker list
- advisory items separated from blockers

## `re-audit`

Use when:

- you already have a previous report
- you want to know what was fixed versus what is still open
- you need regression detection after revisions

Main output:

- `FULLY_ADDRESSED`
- `PARTIALLY_ADDRESSED`
- `NOT_ADDRESSED`
- `NEW`

## `polish`

Use when:

- you want a pre-polish safety check
- you need to know whether polishing is premature because of logic or structural blockers

Main output:

- precheck state
- blocker assessment
- safe/unsafe-to-polish signal

## Legacy Aliases

These aliases are still accepted for one compatibility cycle:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

Use the canonical names in all new docs, scripts, and examples.
