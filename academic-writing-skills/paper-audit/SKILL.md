---
name: paper-audit
description: Deep-review-first audit for Chinese and English academic papers across LaTeX, Typst, and PDF formats. Use whenever the user wants reviewer-style paper critique, pre-submission readiness checks, pass/fail gate decisions, structured revision roadmaps, or re-audits of revised manuscripts. Trigger even if the user only says "review my paper", "check if this is ready to submit", "audit this PDF", "simulate peer review", "find the biggest problems in this manuscript", or "re-check whether I fixed the review issues". Do not use for direct source editing or compilation-heavy repair; route those to the format-specific writing skills instead.
metadata:
  category: academic-writing
  tags: [audit, deep-review, paper, pdf, latex, typst, chinese, english, reviewer, gate, re-audit]
  version: "4.0"
  last_updated: "2026-03-19"
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode quick-audit|deep-review|gate|re-audit|polish] [--venue VENUE] [--previous-report PATH] [--literature-search] [--scholar-eval] [--format markdown|json]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Task
---

# Paper Audit Skill v4.0

`paper-audit` is now **deep-review-first**. Its core job is to behave like a serious reviewer: find technical, methodological, claim-level, and cross-section issues; keep script-backed findings separate from reviewer judgment; and return a structured issue bundle plus a revision roadmap.

Use it for audit and review. Do not use it as the first tool for source editing, sentence rewriting, or build fixing.

## What This Skill Produces

- `quick-audit`: fast submission-readiness screen with script-backed findings
- `deep-review`: reviewer-style structured issue bundle with major/moderate/minor findings
- `gate`: PASS/FAIL decision calibrated for submission blockers
- `re-audit`: compare current issue bundle against a previous audit
- `polish`: precheck-only handoff into a polishing workflow

The primary product is no longer just a score. For `deep-review`, the main outputs are:

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `revision_roadmap.md`

## Do Not Use

- direct source surgery on `.tex` / `.typ`
- compilation debugging as the main task
- free-form literature survey writing
- cosmetic grammar cleanup without an audit goal

## Critical Rules

- Never rewrite the paper source unless the user explicitly switches to an editing skill.
- Never fabricate references, baselines, or reviewer evidence.
- Always distinguish `[Script]` from `[LLM]` findings.
- Always anchor reviewer findings to a quote, section, or exact textual location.
- Be conservative with OCR noise, formatting quirks, and obvious copy-editing trivia.
- Review like a careful reader: understand the author's intended meaning before flagging an issue.

## Mode Selection

| Requested intent | Mode |
|---|---|
| "check my paper", "quick audit", "submission readiness" | `quick-audit` |
| "review my paper", "simulate peer review", "harsh review", "deep review" | `deep-review` |
| "is this ready to submit", "gate this submission", "blockers only" | `gate` |
| "did I fix these issues", "re-audit", "compare against old review" | `re-audit` |
| "polish the writing, but only if safe" | `polish` |

Legacy aliases still work for one compatibility cycle:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

## Review Standard

Read these references before running reviewer-style work:

1. `references/REVIEW_CRITERIA.md`
2. `references/DEEP_REVIEW_CRITERIA.md`
3. `references/CHECKLIST.md`
4. `references/CONSOLIDATION_RULES.md`
5. `references/ISSUE_SCHEMA.md`

The deep-review workflow uses a 10-part issue taxonomy:

1. formula / derivation errors
2. notation inconsistency
3. prose vs formal object mismatch
4. numerical inconsistency
5. missing justification
6. overclaim or claim inaccuracy
7. ambiguity that can mislead a careful reader
8. underspecified methods / missing information
9. internal contradiction
10. self-consistency of standards

## Workflow

### Common Step 0

Parse `$ARGUMENTS` and infer the mode if the user did not provide one. State the inferred mode before running commands if you had to infer it.

### `quick-audit`

1. Run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode quick-audit ...
   ```
2. Present a concise report:
   - `Submission Blockers` first
   - then `Quality Improvements`
   - then checklist items
   - mark quick-audit findings with `[Script]` provenance
3. If the user clearly wants reviewer-depth critique after the quick screen, escalate to `deep-review`.

### `deep-review`

Use this as the default reviewer-style path.

#### Phase 1: Prepare workspace

Run:

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" <paper> --output-dir ./review_results
```

This creates:

- `full_text.md`
- `metadata.json`
- `section_index.json`
- `claim_map.json`
- `paper_summary.md`
- `sections/*.md`
- `comments/`

#### Phase 2: Phase 0 automated audit

Run:

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode deep-review ...
```

Treat this as **Phase 0 only**. It supplies script-backed context and scores, not the final review.

#### Phase 3: Section and cross-cutting review lanes

Read:

- `references/SUBAGENT_TEMPLATES.md`
- `references/REVIEW_LANE_GUIDE.md`

Then dispatch reviewer tasks for:

- section lanes
  - introduction / related work
  - methods
  - results
  - discussion / conclusion
  - appendix, if present
- cross-cutting lanes
  - claims vs evidence
  - notation and numeric consistency
  - evaluation fairness and reproducibility
  - self-standard consistency
  - prior-art and novelty grounding

Each lane writes a JSON array into `comments/`.

If subagents are unavailable, use the built-in deterministic fallback lane pass in `scripts/audit.py` so the workflow still writes lane-compatible JSON into `comments/` before consolidation.

#### Phase 4: Consolidation

Run:

```bash
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir>
```

Consolidation rules:

- merge exact duplicates
- keep distinct paper-level consequences separate even if they share a root cause
- preserve singleton findings unless clearly false positive
- assign `comment_type`, `severity`, `confidence`, and `root_cause_key`

#### Phase 5: Present result

Summarize:

- 1 short paragraph overall assessment
- counts of major / moderate / minor issues
- 3 highest-priority revision items
- path to `review_report.md` and `final_issues.json`

### `gate`

1. Run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode gate ...
   ```
2. Report PASS/FAIL.
3. List blockers first.
4. Keep advisory items separate from blockers.
5. For IEEE pseudocode checks, make it explicit which issues are mandatory and which are only IEEE-safe recommendations.

### `re-audit`

1. Requires `--previous-report PATH`.
2. Run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode re-audit --previous-report <path> ...
   ```
3. If both old and new `final_issues.json` bundles are available, also run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/diff_review_issues.py" <old_final_issues.json> <new_final_issues.json>
   ```
4. Present:
   - root-cause-aware status labels: `FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`
   - use structured prior issue bundles when available, but still accept Markdown previous reports

### `polish`

1. Run the audit precheck:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode polish ...
   ```
2. If blockers exist, stop and report them.
3. Only proceed into polishing if the precheck is safe.

## Output Contract

For `deep-review`, the final issue schema is:

```json
{
  "title": "short issue title",
  "quote": "exact quote from paper",
  "explanation": "why this matters and what remains problematic",
  "comment_type": "methodology|claim_accuracy|presentation|missing_information",
  "severity": "major|moderate|minor",
  "confidence": "high|medium|low",
  "source_kind": "script|llm",
  "source_section": "methods",
  "related_sections": ["results", "appendix"],
  "root_cause_key": "shared-normalized-key",
  "review_lane": "claims_vs_evidence",
  "gate_blocker": false,
  "quote_verified": true
}
```

Always prefer:

- exact quotes over vague paraphrase
- evidence-backed findings over style commentary
- issue bundle + roadmap over raw script dumps

## References

| File | Purpose |
|---|---|
| `references/REVIEW_CRITERIA.md` | top-level audit scoring and mapping |
| `references/DEEP_REVIEW_CRITERIA.md` | deep-review-specific issue taxonomy and leniency rules |
| `references/CONSOLIDATION_RULES.md` | deduplication and root-cause merge policy |
| `references/ISSUE_SCHEMA.md` | canonical JSON schema |
| `references/REVIEW_LANE_GUIDE.md` | section lanes and cross-cutting lanes |
| `references/SUBAGENT_TEMPLATES.md` | reviewer task templates |
| `references/QUICK_REFERENCE.md` | CLI and mode cheat sheet |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/audit.py` | Phase 0 audit and mode entrypoint |
| `scripts/prepare_review_workspace.py` | create deep-review workspace |
| `scripts/build_claim_map.py` | extract headline claims and closure targets |
| `scripts/consolidate_review_findings.py` | deduplicate comment JSONs |
| `scripts/verify_quotes.py` | verify exact quote presence |
| `scripts/render_deep_review_report.py` | render final Markdown report |
| `scripts/diff_review_issues.py` | compare old vs new issue bundles |

## Reviewer Lanes

Default deep-review lanes live in `agents/`:

- `section_reviewer_agent.md`
- `claims_evidence_reviewer_agent.md`
- `notation_consistency_reviewer_agent.md`
- `evaluation_fairness_reviewer_agent.md`
- `self_consistency_reviewer_agent.md`
- `prior_art_reviewer_agent.md`
- `synthesis_agent.md`

Legacy persona agents remain for compatibility but are no longer the default backbone of `deep-review`.

## Examples

- “Review this manuscript like a serious conference reviewer and tell me the biggest validity risks.”
- “Run a quick audit on `paper.tex` and tell me what blocks submission.”
- “Gate this IEEE submission and separate blockers from recommendations.”
- “Re-audit this revision against my previous report.”
