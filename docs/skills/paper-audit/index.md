# `paper-audit`

Unified academic paper audit for LaTeX, Typst, and PDF documents.

## Use It For

- pre-submission checks
- structured self-review
- simulated peer review
- gate-style readiness decisions
- post-revision re-audits

## Modes

| Mode | Use when | Script |
| --- | --- | --- |
| `self-check` | you want a full readiness pass | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode self-check` |
| `review` | you want a review-oriented report | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode review` |
| `gate` | you want pass or fail style blocking issues | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate` |
| `polish` | you want style-targeted follow-up work | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | you want to compare against a previous report | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report.md` |

## Supported Inputs

- `.tex`
- `.typ`
- `.pdf`

## Key Capabilities

- reference integrity checks
- PDF visual layout checks
- severity and priority reporting
- 4-dimension scoring
- citation stacking detection (flags 3+ clustered citations without individual discussion as AI writing traces)
- optional ScholarEval-style assessment
- optional online bibliography verification

## Good First Requests

```text
Run a self-check audit on paper.tex.
```

```text
Tell me whether paper.pdf is submission-ready.
```

```text
Re-audit this paper against the previous report.
```

```text
Check paper.tex for citation stacking in the introduction and related work.
```

## Notes

- `paper-audit` is for reports and scoring, not for being your first compiler.
- Use the sibling writing skill first if the source still does not build.
- Citation stacking detection checks Introduction and Related Work sections for sentences with 3+ clustered citations that lack individual discussion — a common AI writing pattern flagged by reviewers.
