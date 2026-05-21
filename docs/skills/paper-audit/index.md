# `paper-audit`

Deep-review-first academic paper audit for LaTeX, Typst, and PDF documents.

## Use It For

- quick readiness screening before submission
- final-week mechanical checks for em dashes, AI-tone vocabulary, abstract result gaps, and LaTeX hygiene
- reviewer-style deep critique
- pass/fail submission gating
- revision verification against an older audit
- polish precheck before style-focused editing

## Do Not Use It For

- direct source editing as the first step
- compilation debugging as the main task
- free-form literature survey writing
- related-work paragraph rewriting
- purely cosmetic copy-editing without an audit goal

## Modes

| Mode | Use when | Script |
| --- | --- | --- |
| `quick-audit` | you want a fast readiness pass | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit` |
| `deep-review` | you want a reviewer-style issue bundle and roadmap; Phase 0 includes `PRESUBMISSION` context | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review` |
| `gate` | you want pass/fail blockers only; Major/Minor mechanical findings stay advisory | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate` |
| `polish` | you want a precheck before polishing | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | you want to compare against a previous report | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report.md` |

Legacy aliases:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

## How to Choose a Mode

- choose `quick-audit` if you want a fast script-backed screen
- choose `quick-audit` for "pre-submission review" or "submission in three days" requests
- choose `deep-review` if you want reviewer-style critique and a roadmap
- choose `gate` if you only care about blockers
- choose `re-audit` if you already have an older report
- choose `polish` only when you need a pre-polish safety check

## Deep-review at a Glance

1. Prepare workspace with `prepare_review_workspace.py`
2. Run Phase 0 automated audit with `audit.py --mode deep-review`
3. Keep `PRESUBMISSION` findings as Phase 0 context; full/editor focus can promote high-signal mechanical findings into `pre_submission_readiness`
4. Run Academic Pre-Review Committee by default:
   - Editor -> Theory -> Literature -> Methodology -> Logic
   - or restrict with `--focus editor|theory|literature|methodology|logic`
5. Dispatch section and cross-cutting review lanes
6. Consolidate comment JSONs
7. Verify quotes
8. Render `review_report.md` and `peer_review_report.md`

## Main outputs

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `peer_review_report.md`
- `revision_roadmap.md`
- `committee/consensus.md`
- optional committee notes under `committee/*.md`

## Read This Next

- [Workflow](./resources/WORKFLOW.md)
- [Modes](./resources/MODES.md)
- [Outputs](./resources/OUTPUTS.md)
- [CLI and Examples](./resources/CLI_AND_EXAMPLES.md)
- [Deep Review Criteria](./resources/DEEP_REVIEW_CRITERIA.md)
- [Pre-Submission Rules](./resources/PRE_SUBMISSION_RULES.md)
- [Checklist](./resources/CHECKLIST.md)
- [Qualitative Standards](./resources/QUALITATIVE_STANDARDS.md)
- [Editor-in-Chief Agent](./resources/editor_in_chief_agent.md)
- [Troubleshooting](./resources/TROUBLESHOOTING.md)

## Good First Requests

```text
Run a quick-audit on paper.tex and tell me what blocks submission.
```

```text
Deep-review this manuscript like a conference reviewer and give me a revision roadmap.
```

```text
Deep-review this manuscript with the full Academic Pre-Review Committee and give me the top 3 fixes first.
```

```text
Deep-review this manuscript but focus only on methodology transparency and SRQR gaps.
```

```text
Audit only the literature positioning and tell me whether the claimed gap is real or manufactured by selective citation.
```

```text
Gate this IEEE paper and separate hard blockers from advisory pseudocode recommendations.
```

```text
Re-audit this revision against the previous report.
```

## Important Notes

- `audit.py --mode deep-review` is only Phase 0, not the full reviewer workflow.
- `PRESUBMISSION` is a mechanical layer inside existing modes, not a new public mode.
- The primary deep-review product is the structured issue bundle, not the score summary.
- `claim_map.json` now keeps legacy headline/closure fields and adds advisory
  claim candidates with evidence anchors, support strength, missing evidence,
  and bounded wording fields.
- Data availability checks are advisory unless a venue-required central source
  data gap should block submission.
- Use source files when possible; PDF input runs text-only pre-submission checks and skips LaTeX/Typst source hygiene.
- `--focus literature` is critique-only: it checks synthesis quality, contradiction handling, and gap legitimacy, but does not rewrite the related-work prose.
