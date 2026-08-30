# `paper-audit`

Deep-review-first academic paper audit for LaTeX, Typst, and PDF documents. It is a reviewer and gate-checking workflow, not a source editor.

## Use It For

- Quick submission-readiness screening.
- Final-week mechanical checks for em dashes, AI-tone vocabulary, abstract result gaps, citation/label/equation hygiene, and paragraph-shape weak signals.
- Reviewer-style deep critique with major/moderate/minor findings.
- PASS/FAIL gate decisions calibrated for submission blockers.
- Re-audits that compare a revision against a previous audit.
- Review workspaces with traceable artifacts, claim maps, quote checks, and revision trajectories.

## Do Not Use It For

- Direct `.tex` or `.typ` source editing as the first step.
- Compilation repair as the main task.
- Paragraph-level polishing without an audit goal.
- Free-form literature survey writing.
- Cover-letter generation or claim alignment; use `cover-letter`.

## Mode Router

| Mode | Use when | Primary command |
| --- | --- | --- |
| `quick-audit` | You want a fast script-backed readiness screen | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit` |
| `deep-review` | You need reviewer-style findings, workspace artifacts, and a revision roadmap | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus full` |
| `gate` | You only care about hard submission blockers | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee` |
| `polish` | You want precheck-only handoff, including source-coordinate subsection windows when available, before style editing | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | You have a previous report and need regression comparison | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md` |

Compatibility aliases: `self-check` -> `quick-audit`; `review` -> `deep-review`.

Deep-review dispatches five committee agents and six or more lane agents, then uses
`synthesis_agent.md`. Mode-specific agents cover `gate`, `re-audit`, and post-consolidation
revision suggestions. Specialized reviewer playbooks under `agents/` are reference material,
not auto-dispatched; see the [agent roster](./resources/references/agent-roster.md).

## Minimum Inputs

- `paper.tex`, `paper.typ`, or `paper.pdf`.
- Optional `--venue`, `--lang en|zh`, and `--report-style deep-review|peer-review`.
- Optional `--focus full|editor|theory|literature|methodology|logic` for deep-review.
- `--previous-report` for `re-audit`.
- `--review-dir` when continuing or rendering an existing review workspace.

## Script Entry Points

| Script | Purpose |
| --- | --- |
| `audit.py` | Public mode router for quick-audit, deep-review, gate, polish, and re-audit |
| `prepare_review_workspace.py` | Creates the review workspace for deep review |
| `build_claim_map.py` | Extracts headline claims, closure targets, and claim candidates |
| `check_citations.py` / `check_references.py` | Citation and reference hygiene checks |
| `verify_quotes.py` | Verifies report quotes against source text |
| `render_deep_review_report.py` | Renders Markdown deep-review reports |
| `render_html_report.py` | Renders bilingual HTML report twins |
| `render_revision_trajectory.py` | Produces the revision trajectory artifact |
| `diff_review_issues.py` | Supports re-audit comparison |

## Output Artifacts

For `deep-review`, the workspace root is reader-facing:

- `review_report.md` and `review_report.html`
- `revision_suggestions.md` and `revision_suggestions.html`

Supporting artifacts live under `artifacts/`:

- `artifacts/summary/paper_summary.md`, `overall_assessment.txt`, `peer_review_report.md`
- `artifacts/data/final_issues.json`, `all_comments.json`, `claim_map.json`, `section_index.json`, `revision_suggestions.json`, `revision_trajectory.md`
- `artifacts/meta/metadata.json`, `checkpoint.json`, `phase0_context.md`, `full_text.md`
- `artifacts/sections/`, `artifacts/comments/`, `artifacts/committee/`, and `artifacts/references/`

The report language is controlled by `--lang en|zh`. Headings and labels switch language; issue quotes, source tags, and structured field values stay faithful to the source.

## Public Resources

### References

- [Agent Roster](./resources/references/agent-roster.md)
- [Audit Guide](./resources/references/AUDIT_GUIDE.md)
- [Changelog](./resources/references/CHANGELOG.md)
- [Pre-Submission Checklists](./resources/references/CHECKLIST.md)
- [Claim-Evidence Contract](./resources/references/CLAIM_EVIDENCE_CONTRACT.md)
- [Consolidation Rules](./resources/references/CONSOLIDATION_RULES.md)
- [Data Availability Advisory](./resources/references/DATA_AVAILABILITY_ADVISORY.md)
- [Deep Review Criteria](./resources/references/DEEP_REVIEW_CRITERIA.md)
- [Editorial Decision Standards](./resources/references/editorial_decision_standards.md)
- [FORBIDDEN_TERMS.md](./resources/references/FORBIDDEN_TERMS.md)
- [Issue Schema](./resources/references/ISSUE_SCHEMA.md)
- [Literature Grounding Scoring Guide](./resources/references/LITERATURE_GROUNDING_GUIDE.md)
- [Mode Guide](./resources/references/MODE_GUIDE.md)
- [Output Layout](./resources/references/output-layout.md)
- [Over-Claim Guard (Audit Lane Reference)](./resources/references/OVER_CLAIM_GUARD.md)
- [Polish Guide](./resources/references/POLISH_GUIDE.md)
- [Pre-Submission Mechanical Rules](./resources/references/PRE_SUBMISSION_RULES.md)
- [PRESUBMISSION Mode Integration](./resources/references/PRESUBMISSION_GUIDE.md)
- [Qualitative Research Standards Reference](./resources/references/QUALITATIVE_STANDARDS.md)
- [Quality Rubrics for Paper Audit](./resources/references/quality_rubrics.md)
- [Quick Reference](./resources/references/QUICK_REFERENCE.md)
- [Review Criteria](./resources/references/REVIEW_CRITERIA.md)
- [Review Lane Guide](./resources/references/REVIEW_LANE_GUIDE.md)
- [Reviewer Psychology](./resources/references/REVIEWER_PSYCHOLOGY.md)
- [ScholarEval 9-Dimension Scoring Guide](./resources/references/SCHOLAR_EVAL_GUIDE.md)
- [Scoring Systems](./resources/references/SCORING_SYSTEMS.md)
- [Scripts Map](./resources/references/scripts-map.md)
- [Reviewer Lane Templates](./resources/references/SUBAGENT_TEMPLATES.md)
- [Troubleshooting](./resources/references/TROUBLESHOOTING.md)
- [Venue-Specific Rules](./resources/references/VENUE_RULES.md)
- [Workflow Detail](./resources/references/workflow-detail.md)

### Templates

- [Audit Report Template](./resources/templates/audit_report_template.md)
- [Deep Review Report Template](./resources/templates/review_report_template.md)
- [Revision Roadmap Template](./resources/templates/revision_suggestions_template.md)

### Examples

- [Gate Mode Example Output](./resources/examples/gate_example.md)
- [Peer-Review Primary View Example](./resources/examples/peer_review_primary_view.md)
- [Deep Review Example Output](./resources/examples/review_example.md)
- [Self-Check Example Output](./resources/examples/self_check_example.md)

### Agent Contracts

- [Claims vs Evidence Reviewer Agent](./resources/agents/claims_evidence_reviewer_agent.md)
- [Committee Editor Agent (Pre-Review Screen)](./resources/agents/committee_editor_agent.md)
- [Committee Reviewer 3 (Literature Dialogue Auditor)](./resources/agents/committee_literature_agent.md)
- [Committee Reviewer 4 (Logic Chain Auditor)](./resources/agents/committee_logic_agent.md)
- [Committee Reviewer 2 (Methodology Transparency Inspector)](./resources/agents/committee_methodology_agent.md)
- [Committee Reviewer 1 (Theory Contribution Interrogator)](./resources/agents/committee_theory_agent.md)
- [Critical Reviewer Agent (Devil's Advocate)](./resources/agents/critical_reviewer_agent.md)
- [Domain Reviewer Agent](./resources/agents/domain_reviewer_agent.md)
- [Editor-in-Chief Agent (Desk Reject Screener)](./resources/agents/editor_in_chief_agent.md)
- [Evaluation Fairness Reviewer Agent](./resources/agents/evaluation_fairness_reviewer_agent.md)
- [Literature Reviewer Agent](./resources/agents/literature_reviewer_agent.md)
- [Methodology Reviewer Agent](./resources/agents/methodology_reviewer_agent.md)
- [Notation and Numeric Consistency Reviewer Agent](./resources/agents/notation_consistency_reviewer_agent.md)
- [Prior-Art Reviewer Agent](./resources/agents/prior_art_reviewer_agent.md)
- [Revision Coach Agent](./resources/agents/revision_coach_agent.md)
- [Revision Suggestion Agent](./resources/agents/revision_suggestion_agent.md)
- [Section Reviewer Agent](./resources/agents/section_reviewer_agent.md)
- [Self-Consistency Reviewer Agent](./resources/agents/self_consistency_reviewer_agent.md)
- [Synthesis Agent](./resources/agents/synthesis_agent.md)

## Common Requests

```text
Run a quick-audit on paper.tex and tell me what blocks submission.
```

```text
Deep-review this manuscript like a journal reviewer and produce the review workspace plus HTML report.
```

```text
Gate this IEEE paper and separate hard blockers from advisory pseudocode recommendations.
```

```text
Audit only the literature positioning and tell me whether the claimed gap is real or selectively framed.
```

```text
Re-audit this revised manuscript against report_v1.md and summarize resolved vs unresolved issues.
```

## Important Notes

- `PRESUBMISSION` is an internal mechanical layer plugged into existing modes, not a separate public mode.
- Full/editor deep-review may promote high-signal pre-submission findings into `pre_submission_readiness`; other focused reviews keep them as Phase 0 context.
- `claim_map.json` distinguishes visible anchors from support strength; a citation key alone does not prove support.
- Data availability findings are advisory unless a venue-required central source gap should block submission.
- PDF input runs text-only checks and skips LaTeX/Typst source hygiene.
