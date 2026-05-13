---
name: paper-audit
description: Reviewer-style audit and submission gate for Chinese and English academic papers across LaTeX, Typst, and PDF formats. Use whenever the user wants peer-review critique, pre-submission readiness checks, pass/fail gate decisions, blocker triage, structured revision roadmaps, journal-style peer review reports, or re-audits of revised manuscripts. Trigger for prompts like "review my paper", "act as a reviewer", "simulate peer review", "audit this PDF", "is this ready to submit", "gate-check before submission", "find the biggest problems in this manuscript", "write a SCI review report", "give me Summary / Major Issues / Minor Issues / Recommendation", "re-check whether I fixed the review issues", and Chinese variants such as "审稿", "帮我审稿", "投稿门控", "挡稿", "投稿前体检", "把把关", "重新审一遍", "看看能不能投", "出审稿意见", "重大/次要问题清单". Do not use for direct source editing, polishing, or compilation-heavy repair; route those to the format-specific writing skills instead.
metadata:
  category: academic-writing
  tags: [audit, deep-review, paper, pdf, latex, typst, chinese, english, reviewer, gate, re-audit]
  version: "4.5"
  last_updated: "2026-04-27"
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode quick-audit|deep-review|gate|re-audit|polish] [--report-style deep-review|peer-review] [--focus full|editor|theory|literature|methodology|logic] [--venue VENUE] [--previous-report PATH] [--literature-search] [--scholar-eval] [--format md|json]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Task
---

# Paper Audit Skill v4.5

`paper-audit` is **deep-review-first**. Its core job is to behave like a
serious reviewer: find technical, methodological, claim-level, and
cross-section issues; keep script-backed findings separate from reviewer
judgment; and return a structured issue bundle plus a revision roadmap.

Version 4.5 adds a script-backed `PRESUBMISSION` layer for final-week
mechanical checks (em dashes, AI-tone term frequency, abstract completeness,
LaTeX citation/label/equation hygiene, paragraph-shape weak signals, concrete
captions). It plugs into existing modes; it is not a separate public mode.
See `references/PRESUBMISSION_GUIDE.md` for mode integration.

Use it for audit and review. Do not use it as the first tool for source
editing, sentence rewriting, or build fixing.

## What This Skill Produces

- `quick-audit`: fast submission-readiness screen with script-backed findings,
  including `PRESUBMISSION`
- `deep-review`: reviewer-style structured issue bundle with major/moderate/
  minor findings
- `gate`: PASS/FAIL decision calibrated for submission blockers;
  `PRESUBMISSION` Major/Minor findings remain advisory
- `re-audit`: compare current issue bundle against a previous audit, including
  mechanical regression findings
- `polish`: precheck-only handoff into a polishing workflow

The primary product is no longer just a score. For `deep-review`, the main
outputs are:

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `peer_review_report.md`
- `revision_roadmap.md`

## Do Not Use

- direct source surgery on `.tex` / `.typ`
- compilation debugging as the main task
- free-form literature survey writing
- paragraph-level related-work rewriting
- cosmetic grammar cleanup without an audit goal

## Critical Rules

- Don't rewrite the paper source — `paper-audit` is a reviewer, not an editor; switch skills explicitly if the user wants prose changes, so review evidence stays separable from edits.
- Don't fabricate references, baselines, or reviewer evidence — invented citations and made-up reviewer voices undermine every other finding in the bundle.
- Distinguish `[Script]` from `[LLM]` findings — script-backed items have a deterministic anchor the user can rerun, while LLM findings need a quote or section to be falsifiable.
- Anchor every reviewer finding to a quote, section, or exact textual location — unanchored complaints become impossible to audit on a re-pass.
- Be conservative with OCR noise, formatting quirks, and copy-editing trivia — flagging cosmetic noise inflates the report and buries the real issues.
- Read like a careful reader before flagging — understand the author's intended meaning first so the issue captures a real misread, not a strawman.
- For literature findings, judge whether the gap is evidence-backed and fairly positioned, and don't rewrite the prose inside `paper-audit` — keep prose rewrites in the format-specific writing skills where they can be reviewed in isolation.
- For `PRESUBMISSION`, map CRITICAL / MAJOR / MINOR to Critical / Major / Minor script severities; only Critical or failed checklist items can fail `gate` — otherwise mechanical findings drown out the substantive ones.
  Full mode-integration matrix lives in `references/PRESUBMISSION_GUIDE.md`.
- In PDF mode, do not guess source-only hygiene. Report text-proven items
  and note that LaTeX/Typst source checks were skipped.

## Mode Selection

| Requested intent | Mode |
|---|---|
| "check my paper", "quick audit", "submission readiness", "pre-submission review", "投稿前检查" | `quick-audit` |
| "review my paper", "simulate peer review", "harsh review", "deep review" | `deep-review` |
| "is this ready to submit", "gate this submission", "blockers only" | `gate` |
| "did I fix these issues", "re-audit", "compare against old review" | `re-audit` |
| "polish the writing, but only if safe" | `polish` |

Legacy aliases still work for one compatibility cycle:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

For per-mode workflow steps, input resolution rules, presentation surface
rules, and committee focus routing, see `references/MODE_GUIDE.md`.

## Review Standard

Read these references before running reviewer-style work:

1. `references/REVIEW_CRITERIA.md`
2. `references/DEEP_REVIEW_CRITERIA.md`
3. `references/CHECKLIST.md`
4. `references/CONSOLIDATION_RULES.md`
5. `references/ISSUE_SCHEMA.md`
6. `references/PRE_SUBMISSION_RULES.md`
7. `references/PRESUBMISSION_GUIDE.md`
8. `references/MODE_GUIDE.md`

The deep-review workflow uses a 16-part issue taxonomy:

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
11. table structure violations
12. abstract structural incompleteness
13. theory contribution deficiency
14. qualitative methodology opacity
15. pseudo-innovation / straw man
16. paragraph-level argument incoherence

## Workflow

Each mode has the same shape: parse `$ARGUMENTS`, lock the paper path, infer
mode/report-style/focus/language if not provided, then run the canonical
command. Detailed phase steps are in `references/MODE_GUIDE.md`.

### `quick-audit`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode quick-audit ...
```

Present `Submission Blockers` -> `Quality Improvements` -> checklist; call
out `PRESUBMISSION` mechanical findings with `[Script]` provenance. Escalate
to `deep-review` when the user wants reviewer-depth critique.

### `deep-review`

Five phases (see `references/MODE_GUIDE.md` for full detail):

1. **Workspace prep**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" <paper> --output-dir ./review_results
   ```
2. **Phase 0 automated audit**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode deep-review ...
   ```
3. **Phase 3A committee** — dispatch 5 committee agents (editor, theory,
   literature, methodology, logic) and write `committee/consensus.md`.
4. **Phase 3B section + cross-cutting lanes** — section, claims-vs-evidence,
   notation, evaluation fairness, self-consistency, prior-art, and
   pre-submission readiness (full/editor focus only).
5. **Consolidation**:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
   uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
   uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir>
   ```

When the user explicitly asks for journal-review prose, set
`--report-style peer-review` so `peer_review_report.md` becomes the **Primary
View** while `review_report.md` stays as the richer evidence bundle.

### `gate`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode gate ...
```

Run **EIC Screening** (Phase 0.5) using `agents/editor_in_chief_agent.md`
first; report PASS/FAIL; verdict -> EIC -> blockers -> advisory. A desk-reject
verdict is a gate blocker. Critical `PRESUBMISSION` only blocks the gate.

### `re-audit`

Requires `--previous-report PATH`.

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode re-audit --previous-report <path> ...
uv run python -B "$SKILL_DIR/scripts/diff_review_issues.py" <old_final_issues.json> <new_final_issues.json>
```

Present root-cause-aware status labels: `FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

### `polish`

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode polish ...
```

If blockers exist, stop and report them. Only proceed into polishing if the
precheck is safe.

## Output Contract

For `deep-review`, the final issue schema is:

```json
{
  "title": "short issue title",
  "quote": "exact quote from paper",
  "explanation": "why this matters and what remains problematic",
  "comment_type": "methodology|claim_accuracy|presentation|missing_information",
  "severity": "major|moderate|minor",
  "confidence": "high|medium|low|unverified",
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
| `references/MODE_GUIDE.md` | per-mode workflow detail, phase steps, committee focus routing |
| `references/PRESUBMISSION_GUIDE.md` | `PRESUBMISSION` mode-integration behavior matrix |
| `references/REVIEW_CRITERIA.md` | top-level audit scoring and mapping |
| `references/DEEP_REVIEW_CRITERIA.md` | deep-review-specific issue taxonomy and leniency rules |
| `references/CONSOLIDATION_RULES.md` | deduplication and root-cause merge policy |
| `references/ISSUE_SCHEMA.md` | canonical JSON schema |
| `references/REVIEW_LANE_GUIDE.md` | section lanes and cross-cutting lanes |
| `references/PRE_SUBMISSION_RULES.md` | final-week mechanical audit rules and term list |
| `references/SUBAGENT_TEMPLATES.md` | reviewer task templates |
| `references/QUICK_REFERENCE.md` | CLI and mode cheat sheet |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/audit.py` | Phase 0 audit and mode entrypoint |
| `scripts/pre_submission_check.py` | deterministic `PRESUBMISSION` mechanical audit layer |
| `scripts/prepare_review_workspace.py` | create deep-review workspace |
| `scripts/build_claim_map.py` | extract headline claims and closure targets |
| `scripts/consolidate_review_findings.py` | deduplicate comment JSONs |
| `scripts/verify_quotes.py` | verify exact quote presence |
| `scripts/render_deep_review_report.py` | render final Markdown report |
| `scripts/diff_review_issues.py` | compare old vs new issue bundles |

## Reviewer Lanes

Committee agents (deep-review default):

- `committee_editor_agent.md`
- `committee_theory_agent.md`
- `committee_literature_agent.md`
- `committee_methodology_agent.md`
- `committee_logic_agent.md`

Default deep-review lanes live in `agents/`:

- `section_reviewer_agent.md`
- `claims_evidence_reviewer_agent.md`
- `notation_consistency_reviewer_agent.md`
- `evaluation_fairness_reviewer_agent.md`
- `self_consistency_reviewer_agent.md`
- `prior_art_reviewer_agent.md`
- `synthesis_agent.md`
- `editor_in_chief_agent.md` — EIC desk-reject screener (used in `gate` mode)

Specialized deep-review agents (read their files for activation criteria):

- `critical_reviewer_agent.md` — devil's advocate with C3-C5 checks
- `domain_reviewer_agent.md` — domain expertise with A1-A7 assessments
- `methodology_reviewer_agent.md` — methodology rigor with B3-B10 checks
- `literature_reviewer_agent.md` — evidence-based literature verification
  (optional, `--literature-search`)

## Examples

- "Review this manuscript like a serious conference reviewer and tell me the
  biggest validity risks."
- "Run a quick audit on `paper.tex` and tell me what blocks submission."
- "Gate this IEEE submission and separate blockers from recommendations."
- "Re-audit this revision against my previous report."
- "Audit only the literature positioning and tell me whether the claimed gap
  is real or fabricated by selective citation."
