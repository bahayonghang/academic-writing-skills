# Workflow

`paper-audit` now has two distinct layers:

- **script-first screening** for `quick-audit`, `gate`, and `polish` precheck
- **reviewer-style deep review** for `deep-review`

The main mistake to avoid is treating `audit.py --mode deep-review` as the entire deep review. It is only the Phase 0 automated layer.

## End-to-End Deep Review

### Phase 1: Prepare the workspace

```bash
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex --output-dir ./review_results
```

This creates a workspace with:

- `full_text.md`
- `metadata.json`
- `section_index.json`
- `claim_map.json`
- `paper_summary.md`
- `sections/*.md`
- `comments/`
- `references/` (minimal reviewer references)
- `committee/` (committee reviewer notes and consensus)

Use this when you want a reviewer-style audit with traceable intermediate artifacts.

### Phase 2: Run Phase 0 automated audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
```

What this phase gives you:

- script-backed checks
- score indicators
- venue and checklist context
- inputs for later reviewer lanes

What it does **not** give you:

- the final structured issue bundle
- major / moderate / minor reviewer findings
- final roadmap

### Phase 3: Run committee review (default for deep-review)

Default sequence:

1. Editor pre-screen
2. Theory contribution review
3. Literature dialogue review
4. Methodology transparency review
5. Logic-chain review

Optional focus:

- `--focus full` (default)
- `--focus editor|theory|literature|methodology|logic`

At this phase, the workflow should write committee notes into `committee/*.md`.

### Phase 4: Run section review lanes

Typical section lanes:

- introduction / related work
- methods
- results
- discussion / conclusion
- appendix when present

These lanes inspect local correctness and local clarity.

### Phase 5: Run cross-cutting lanes

Typical cross-cutting lanes:

- claims vs evidence
- notation and numeric consistency
- evaluation fairness and reproducibility
- self-consistency of standards
- prior-art and novelty grounding

These lanes inspect global consistency and paper-level validity threats.

### Phase 6: Consolidate and verify

```bash
uv run python academic-writing-skills/paper-audit/scripts/consolidate_review_findings.py ./review_results/paper-slug
uv run python academic-writing-skills/paper-audit/scripts/verify_quotes.py ./review_results/paper-slug --write-back
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py ./review_results/paper-slug
```

This phase:

- merges true duplicates
- keeps distinct paper-level consequences separate
- verifies exact quotes
- produces the final Markdown report
- writes `committee/consensus.md` (score + top 3 priorities)

## Quick-Audit Workflow

Use `quick-audit` when you want a fast readiness pass and do not need the full reviewer workflow.

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit --venue neurips
```

Best for:

- final-day submission checks
- initial screening before deeper review
- CI-friendly script-based reporting

## Gate Workflow

Use `gate` when you only care about blockers.

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate --venue ieee
```

Best for:

- PASS / FAIL decisions
- venue gate checks
- IEEE pseudocode hard-rule review

## Re-Audit Workflow

Use `re-audit` when a paper has already been reviewed once and you want to verify whether issues were fixed.

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md
```

If both old and new `final_issues.json` bundles are available, compare them directly:

```bash
uv run python academic-writing-skills/paper-audit/scripts/diff_review_issues.py old_final_issues.json new_final_issues.json
```

## Polish Workflow

Use `polish` only after the paper is structurally safe to polish.

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish
```

This is a precheck, not a full edit pass. If blockers appear, fix those before polishing.
