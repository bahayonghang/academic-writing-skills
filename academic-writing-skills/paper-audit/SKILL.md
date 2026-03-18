---
name: paper-audit
description: Unified paper audit for Chinese and English academic papers across LaTeX, Typst, and PDF formats. Use when reviewing paper quality, running pre-submission checks, simulating peer review, making pass/fail gate decisions, polishing writing, re-auditing revisions, or scoring with ScholarEval dimensions. Trigger when the user says "check my paper", "is this ready to submit", "score my paper", "review like a reviewer", "find missing references", "literature search", "re-audit", or wants a CI/CD quality gate. Do not use for direct source editing or compiling — use the format-specific writing skills instead.
metadata:
  category: academic-writing
  tags: [audit, review, paper, pdf, latex, typst, chinese, english, scoring, checklist]
  version: "3.0"
  last_updated: "2026-03-16"
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode MODE] [--pdf-mode MODE] [--style STYLE] [--journal VENUE] [--previous-report PATH] [--literature-search] [--tavily-key KEY] [--s2-key KEY] [--regression]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Task
---

# Paper Audit Skill v3.0

Unified academic paper auditing across formats (LaTeX, Typst, PDF) and languages (English, Chinese). Runs automated checks, computes dimension scores, and optionally dispatches multi-perspective review agents.

---

## Capability Summary

- Run automated paper checks across `.tex`, `.typ`, and `.pdf` inputs.
- Produce self-check, peer-review, gate, polish, and re-audit outputs with explicit severity and priority labels.
- Combine script findings, venue-specific checklist items, and optional agent synthesis into one report flow.
- Reuse sibling writing-skill scripts for LaTeX and Typst inputs instead of re-implementing duplicate checks.
- Audit IEEE-style pseudocode blocks for float usage, caption/label/reference hygiene, and advisory readability issues.

## Triggering

Use this skill when the user wants to:

- run a pre-submission readiness audit
- simulate a reviewer-style critique
- make a pass/fail submission gate decision
- compare a revised paper against a previous audit
- audit a PDF when the source format is unavailable

Trigger it even when the user only says “check my paper”, “review this submission”, “is this ready to submit?”, or “re-audit against the old report”.

## Do Not Use

- fixing the paper source as the first step when the project still fails to compile badly
- full literature research or survey drafting
- writing a paper from scratch
- template-specific LaTeX or Typst editing when the user wants direct source surgery instead of an audit report
- direct source editing, grammar fixing, or expression polishing on individual sections (use `latex-paper-en`, `latex-thesis-zh`, or `typst-paper` based on format and language)
- fixing compilation errors as the primary task (use the format-specific skill first)

## Critical Rules

- **NEVER** modify `\cite{}`, `\ref{}`, `\label{}`, math environments, or any content listed in `$SKILL_DIR/references/FORBIDDEN_TERMS.md`
- **NEVER** fabricate bibliography entries; only verify existing `.bib` or `.yml` files
- **NEVER** change domain terminology without explicit user confirmation
- **ALWAYS** distinguish `[Script]` (automated) findings from `[LLM]` (agent judgment) assessments in output
- **ALWAYS** distinguish IEEE hard pseudocode violations from IEEE-safe default recommendations
- All dimension scores from scripts are **indicators**, not definitive judgments

---

## Mode Selection Guide

| Mode | When to Use | Output | Speed |
|------|-------------|--------|-------|
| `self-check` | Pre-submission readiness check | Scores + issues + checklist | ~30s |
| `review` | Simulate multi-perspective peer review | Agent review reports + synthesis + revision roadmap | ~2min |
| `gate` | CI/CD quality gate, binary pass/fail | PASS/FAIL verdict + blocking issues | ~15s |
| `polish` | Expression refinement via agents | Precheck JSON + Critic/Mentor agent dispatch | ~1min+ |
| `re-audit` | Verify revisions against prior report | Verification checklist + new issues + score delta | ~1min |

### Mode Selection Logic

```
"Check my paper"                         -> self-check
"Review my paper" / "peer review"        -> review
"Is this ready to submit?"               -> gate
"Polish the writing"                     -> polish
"Did I fix the issues?" / "re-check"     -> re-audit
```

---

## Steps

### All Modes (Common)

1. Parse `$ARGUMENTS` for file path and mode. If missing, ask the user for the target `.tex`, `.typ`, or `.pdf` file.
2. Read `$SKILL_DIR/references/REVIEW_CRITERIA.md` for scoring framework.
3. Read `$SKILL_DIR/references/CHECKLIST.md` for universal + venue-specific checklist items.
4. Run the orchestrator: `uv run python -B "$SKILL_DIR/scripts/audit.py" $ARGUMENTS`.
5. Present the Markdown report directly to the user.

### Self-Check Mode

6. Review scores and highlight any Critical/P0 issues that block submission.
7. If `--scholar-eval` is present, read `$SKILL_DIR/references/SCHOLAR_EVAL_GUIDE.md` and formulate LLM assessments for Novelty, Significance, Ethics, and Reproducibility. Provide as `--llm-json` on a second run.

### Review Mode (Multi-Perspective)

6. Read `$SKILL_DIR/references/SCHOLAR_EVAL_GUIDE.md` for LLM assessment dimensions.
7. Read `$SKILL_DIR/references/quality_rubrics.md` for scoring anchors and decision mapping.
8. **Phase 0** (automated): The script output provides automated findings and scores.
   - When `--literature-search` is enabled, Phase 0 also includes literature search results and grounding score.
   - `audit.py --mode review` by itself runs Phase 0 only. Full multi-perspective review happens after the skill dispatches Phase 1 reviewer tasks.
   - In Phase 0, literature-review enumeration/gap checks, experiment-section structure checks, and cross-section closure are script-backed; A2/A4 style judgments remain reviewer/LLM work unless future heuristics are added.
9. **Phase 1** (agents): For each agent in `$SKILL_DIR/agents/`:
   - Read the agent definition file for persona and protocol.
   - Dispatch a `Task` with: agent definition + paper content + Phase 0 results as context.
   - Agents: `methodology_reviewer_agent.md`, `domain_reviewer_agent.md`, `critical_reviewer_agent.md`.
   - When `--literature-search` is enabled, also dispatch `literature_reviewer_agent.md` (optional).
10. **Phase 2** (synthesis): Read `$SKILL_DIR/agents/synthesis_agent.md` and dispatch a `Task` to consolidate all reviews.
    - Input: Phase 0 automated results + Phase 1 agent reviews.
    - Output: Consensus classification, merged scores, final review report, revision roadmap.
11. Read `$SKILL_DIR/templates/review_report_template.md` for output structure.
12. Present synthesized report following the template format.

### Gate Mode

6. Report PASS or FAIL based on: zero Critical issues AND all checklist items pass.
7. List blocking issues (Critical only) and failed checklist items.

### Polish Mode

6. Read `.polish-state/precheck.json` generated by the script.
7. If blockers detected, report them and ask user to resolve before polishing.
8. Read `$SKILL_DIR/references/POLISH_GUIDE.md` for style targets and critic protocol.
9. Spawn nested tasks for the Critic Agent and Mentor Agents as defined in the polish workflow.

### Re-Audit Mode

6. Requires `--previous-report PATH` pointing to a prior audit report.
7. Script runs fresh checks and compares against previous findings.
8. Present verification checklist: each prior issue classified as `FULLY_ADDRESSED` / `PARTIALLY_ADDRESSED` / `NOT_ADDRESSED`.
9. Report any `NEW` issues introduced during revision.
10. Show score comparison (before vs after).

## Required Inputs

- A target `.tex`, `.typ`, or `.pdf` file.
- An audit mode, or enough intent to infer one from the mode-selection guide.
- Optional venue or journal context when the checklist should be venue-specific.
- Optional `--previous-report PATH` for `re-audit`.

If the user omits the mode, infer it using the selection guide and state the assumption before running the audit.

## Output Contract

- Always return a report, not raw script output.
- Keep `[Script]` and `[LLM]` findings visibly separated.
- Include the selected mode, target file, and venue context near the top of the report.
- For blocking failures, list the exact blocking issue(s) and failed checklist items first.
- When a script or nested agent step fails, report the command, exit code, and what coverage was skipped.
- Preserve the source; this skill audits and synthesizes, it does not rewrite the paper by default.

---

## Venue-Specific Behavior

> Venue-specific rules: see [`references/VENUE_RULES.md`](references/VENUE_RULES.md) for per-venue behavior adjustments.

For IEEE pseudocode:
- hard gate rules: no floating `algorithm` / `algorithm2e`; pseudocode blocks need caption, label, and text reference
- advisory rules: line numbers, explicit input/output markers, short comments, concise step text

## Output Protocol

### Issue Format
```
[Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: message (Line N)
```

### Severity Definitions
| Severity | Impact | Score Deduction (4-dim) |
|----------|--------|----------------------|
| Critical | Blocks submission | -1.5 per issue |
| Major | Significant quality concern | -0.75 per issue |
| Minor | Style/formatting improvement | -0.25 per issue |

### Source Labeling
- `[Script]` — Automated check result (objective, reproducible)
- `[LLM]` — Agent/LLM judgment (subjective, evidence-based)

---

## Scoring Systems

> Scoring rubrics: see [`references/SCORING_SYSTEMS.md`](references/SCORING_SYSTEMS.md) for the full 4-dim and 9-dim ScholarEval scoring tables.

## Integration with Sibling Skills

Paper-audit reuses check scripts from sibling skills via format-based routing:

| Format | Script Source | Checks Available |
|--------|-------------|-----------------|
| `.tex` (English) | `latex-paper-en/scripts/` | format, grammar, logic, experiment, sentences, deai, bib, figures |
| `.tex` / `.typ` pseudocode | sibling `check_pseudocode.py` | IEEE-safe algorithm float, caption, label, reference, and advisory checks |
| `.tex` (Chinese) | `latex-thesis-zh/scripts/` (primary), `latex-paper-en/scripts/` (fallback) | + experiment, consistency, gbt7714 |
| `.typ` | `typst-paper/scripts/` | format, grammar, logic, experiment, sentences, deai |
| `.pdf` | `paper-audit/scripts/` only | visual, pdf_parser (no format/bib/figures checks) |

Scripts that live in paper-audit itself: `audit.py`, `check_references.py`, `check_citations.py`, `visual_check.py`, `pdf_parser.py`, `detect_language.py`, `parsers.py`, `report_generator.py`, `scholar_eval.py`, `literature_search.py`, `literature_compare.py`, `scoring_model.py`.

> `check_citations.py` detects citation stacking (3+ clustered citations without individual discussion). `check_references.py` validates figure/table/equation label-ref integrity.

---

## Literature Search Integration (NEW in v3.0)

When `--literature-search` is enabled, the audit pipeline adds external literature verification:

### How It Works

1. **Metadata Extraction**: Extracts title, abstract, keywords, and method names from the paper.
2. **Query Generation**: Generates 5 search strategies (title-based, method-based, problem-based, keyword combos, negation-aware).
3. **Multi-Source Search**: Queries Semantic Scholar, arXiv, and optionally Tavily in parallel.
4. **Relevance Filtering**: Deduplicates and filters results by relevance to the paper (TF-IDF word overlap).
5. **Literature Comparison**: Compares found literature against the paper's bibliography.
6. **Grounding Score**: Computes a Literature Grounding score (1-10) based on coverage, recency, missing refs, and freshness.

### API Keys

| Source | Key | Required? |
|--------|-----|-----------|
| Semantic Scholar | `--s2-key` or `S2_API_KEY` env var | Optional (works without key at lower rate limit) |
| arXiv | None | Free, no key needed |
| Tavily | `--tavily-key` or `TAVILY_API_KEY` env var | Required for Tavily source |

### Regression Scoring Model

When `--regression` is enabled with `--scholar-eval`, uses a Ridge regression model instead of weighted average for the overall score prediction. The model considers:
- 9 base dimension scores
- 3 interaction terms (soundness×novelty, clarity×significance, literature_grounding×novelty)
- 2 meta features (critical issue count, dimensions below 5.0)

Default model coefficients approximate the weighted-average behavior. Custom trained models can be placed at `$SKILL_DIR/scripts/models/scoring_model.json`.

---

## Agent References

| Agent | Definition File | Role |
|-------|----------------|------|
| Methodology Reviewer | `$SKILL_DIR/agents/methodology_reviewer_agent.md` | Research design, statistical rigor, reproducibility |
| Domain Reviewer | `$SKILL_DIR/agents/domain_reviewer_agent.md` | Literature coverage, theoretical framework, contribution |
| Critical Reviewer | `$SKILL_DIR/agents/critical_reviewer_agent.md` | Core argument challenges, logical fallacies, overclaims |
| Synthesis Agent | `$SKILL_DIR/agents/synthesis_agent.md` | Consolidate reviews, consensus classification, revision roadmap |
| Literature Reviewer | `$SKILL_DIR/agents/literature_reviewer_agent.md` | External literature verification (optional, with `--literature-search`) |

---

## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `references/REVIEW_CRITERIA.md` | 4-dimension scoring framework | All modes |
| `references/CHECKLIST.md` | Universal + venue-specific checklists | self-check, gate |
| `references/SCHOLAR_EVAL_GUIDE.md` | 8-dimension ScholarEval scoring guide | review (with --scholar-eval) |
| `references/quality_rubrics.md` | Score-level descriptors and decision mapping | review, self-check |
| `references/AUDIT_GUIDE.md` | User guide for modes and report interpretation | Reference |
| `references/POLISH_GUIDE.md` | Style targets and critic/mentor protocol | polish |
| `references/FORBIDDEN_TERMS.md` | Protected content (citations, math, terminology) | All modes |
| `references/QUICK_REFERENCE.md` | Check support matrix and CLI quick reference | Reference |
| `references/editorial_decision_standards.md` | Consensus rules and decision matrix | review (synthesis) |
| `references/LITERATURE_GROUNDING_GUIDE.md` | Literature Grounding dimension scoring rubric (NEW v3.0) | review, self-check (with --literature-search) |

## Example Requests

- “Run a self-check on `paper.tex` and tell me what blocks submission.”
- “Review this paper like a harsh reviewer and give me a revision roadmap.”
- “Is `paper.pdf` ready to submit to IEEE, or does it fail the gate?”
- “Check whether the IEEE pseudocode in `paper.tex` still uses a floating `algorithm` block.”
- “Re-audit this revision against my previous report and tell me which issues are still open.”

## Templates

| Template | Purpose |
|----------|---------|
| `templates/audit_report_template.md` | Output structure for self-check/gate |
| `templates/review_report_template.md` | Output structure for multi-perspective review |
| `templates/revision_roadmap_template.md` | Prioritized revision action plan |

## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Evidence-based | Every weakness must cite specific text, line, or section from the paper |
| Specificity | Avoid vague comments; provide exact locations and concrete suggestions |
| Balance | Report both strengths and weaknesses; never only criticize |
| Actionability | Each issue must include a specific improvement suggestion |
| Source transparency | Always label findings as [Script] or [LLM] |
| Format consistency | All reports follow the corresponding template structure |
| Constructive tone | Professional and helpful; avoid dismissive language |

## Examples

### Self-Check
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode self-check
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode self-check --journal neurips
```

### Review (Multi-Perspective)
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode review --scholar-eval
```
Then follow Steps 8-12 to dispatch review agents.

### Gate (CI/CD)
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode gate --journal ieee --format json
```

### Polish
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode polish
```

### Re-Audit
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode re-audit --previous-report report_v1.md
```

### PDF Input
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.pdf --mode self-check --pdf-mode enhanced
```

### Literature Search (NEW v3.0)
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode review --scholar-eval --literature-search
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode self-check --scholar-eval --literature-search --tavily-key $TAVILY_API_KEY
```

### Regression Scoring (NEW v3.0)
```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode self-check --scholar-eval --regression
```

See `$SKILL_DIR/examples/` for complete output examples.

---

## Troubleshooting

> Troubleshooting: see [`references/TROUBLESHOOTING.md`](references/TROUBLESHOOTING.md).

## Changelog

> Version history: see [`references/CHANGELOG.md`](references/CHANGELOG.md).
