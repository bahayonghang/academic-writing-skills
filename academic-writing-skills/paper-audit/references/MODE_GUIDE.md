# Mode Guide

Detailed workflow for each `paper-audit` mode. The top-level `SKILL.md` keeps
the routing table; this file holds the per-mode steps, phase ordering, and
committee dispatch rules.

Read next:
- `references/PRESUBMISSION_GUIDE.md` for the `PRESUBMISSION` mode-integration layer.
- `references/REVIEW_LANE_GUIDE.md` for section and cross-cutting lane definitions.
- `references/SUBAGENT_TEMPLATES.md` for reviewer task templates.

## Input Resolution

- Resolve the paper path first and keep the user-provided relative path when it
  already works.
- Infer the paper format from the extension (`.tex`, `.typ`, `.pdf`) before
  choosing checks or parser behavior.
- Infer `report-style` from the request: use `peer-review` when the user asks
  for journal-review prose such as Summary / Major Issues / Minor Issues /
  Recommendation; otherwise default to `deep-review`.
- Infer output language from the request first, then fall back to the paper
  language when the request is ambiguous.
- For `re-audit`, require `--previous-report PATH`. If it is missing, stop
  immediately and ask only for that path instead of running a fresh audit.
- State the locked mode, report style, focus, language, and venue (if known)
  before running commands when any of them were inferred rather than explicitly
  provided.

### Auto-Detection at Intake

Surface these conditions to the user as a prompt; never auto-switch modes
without confirmation. The goal is to catch obvious mode mismatches before
running a wrong workflow.

- **Previous report present**: if a file named `*audit_report*`,
  `*review_report*`, `*final_issues*.json`, or matching `--previous-report`
  semantics is present in the paper's directory or the current working
  directory, ask whether the user wants `re-audit` mode.
- **Revision markers in the paper**: if the source contains
  `\latextrackchanges`, `changes` package macros, `track-changes`,
  `changeBars`, `\added{`, `\deleted{`, `\replaced{`, `<changes>`, or a
  `Revision History` section, ask whether this is a revised submission and
  whether `re-audit` is intended.
- **Polish mode on a long paper**: if mode is `polish` but the paper exceeds
  30 pages or 25k words, ask whether `deep-review` is more appropriate before
  proceeding.
- **Reviewer letter detected**: if the input or working directory contains a
  reviewer-letter-shaped file (markers: `Reviewer 1`, `R1:`, `审稿人 1`,
  `Editor's Comments`, `Decision Letter`), dispatch
  `agents/revision_coach_agent.md` first to parse it into a structured
  roadmap, then feed the roadmap into `re-audit`.

Always present the detected signal in plain language ("found
`final_issues.old.json` next to the paper — this looks like a re-audit") and
let the user confirm or decline.

## Presentation Surface

- `deep-review`: make the issue bundle, revision roadmap, and artifact paths
  the primary summary surface. It is acceptable to mention schema-level fields
  such as review lanes or source provenance here.
- `peer-review`: make reviewer prose the primary summary surface. Do not expose
  raw internal keys like `review_lane`, `source_kind`, or `root_cause_key` in
  the top-level prose summary; keep them inside the artifact bundle.
- `gate`: show verdict first, then EIC screening, then blockers, then advisory
  recommendations.
- `re-audit`: show status buckets (`FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`,
  `NOT_ADDRESSED`, `NEW`) before any new audit commentary.

## Common Step 0

Parse `$ARGUMENTS`, lock the paper path, and infer the mode if the user did
not provide one. State the inferred mode before running commands if you had to
infer it.

## `quick-audit`

1. Run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode quick-audit ...
   ```
2. Present a concise report:
   - `Submission Blockers` first
   - then `Quality Improvements`
   - then checklist items
   - call out `PRESUBMISSION` mechanical findings separately when they matter
   - mark quick-audit findings with `[Script]` provenance
3. If the user clearly wants reviewer-depth critique after the quick screen,
   escalate to `deep-review`.

## `deep-review`

Use this as the default reviewer-style path.

If the user explicitly wants a submission-style reviewer report (for example:
"SCI reviewer", "journal review report", "Summary / Major Issues / Minor
Issues / Recommendation", or "审稿报告"), keep the same deep-review evidence
pipeline but make `peer_review_report.md` the **Primary View** in the combined
CLI summary while keeping `review_report.md` as the richer evidence bundle. In
this path, keep raw schema fields inside artifacts rather than the
reviewer-facing prose.

### Phase 1: Prepare workspace

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" <paper> --output-dir ./review_results
```

This creates:

- `artifacts/meta/full_text.md`
- `artifacts/meta/metadata.json`
- `artifacts/data/section_index.json`
- `artifacts/data/claim_map.json`
- `artifacts/summary/paper_summary.md`
- `artifacts/sections/*.md`
- `artifacts/comments/`
- `artifacts/references/` (minimal copies for reviewer agents)
- `artifacts/committee/` (committee reviewer artifacts)

### Phase 2: Phase 0 automated audit

```bash
uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode deep-review ...
```

Treat this as **Phase 0 only**. It supplies script-backed context and scores,
not the final review. `PRESUBMISSION` findings stay here for focused
theory/literature/methodology/logic reviews; only full/editor deep-review can
promote high-signal mechanical findings into the `pre_submission_readiness`
lane (see `PRESUBMISSION_GUIDE.md`).

### Phase 3A: Academic Pre-Review Committee (default)

Decide committee focus:
- If `--focus ...` is provided, use it.
- Otherwise infer from the user request using the keyword map below.
- If nothing matches, default to `full` (all five roles).

Dispatch the committee reviewers (in this exact order) and have them write
artifacts into the workspace:

1. `agents/committee_editor_agent.md`
   - write: `committee/editor.md`
   - write: `comments/committee_editor.json`
2. `agents/committee_theory_agent.md`
   - write: `committee/theory.md`
   - write: `comments/committee_theory.json`
3. `agents/committee_literature_agent.md`
   - write: `committee/literature.md`
   - write: `comments/committee_literature.json`
4. `agents/committee_methodology_agent.md`
   - write: `committee/methodology.md`
   - write: `comments/committee_methodology.json`
5. `agents/committee_logic_agent.md`
   - write: `committee/logic.md`
   - write: `comments/committee_logic.json`

If subagents are unavailable, run the committee reviewers inline, but keep the
same file outputs.

Then write: `committee/consensus.md`
- include: overall score (1-10), ordered priorities, and the top 3 issues to
  fix first
- scoring formula:
  - start at 9.0
  - subtract: `1.5 * (# major) + 0.7 * (# moderate) + 0.2 * (# minor)`
  - floor at 1.0
  - if Editor verdict is Desk Reject, cap at 4.0

`render_deep_review_report.py` automatically embeds `committee/*.md` into
`review_report.md` when present.

### Phase 3B: Section and cross-cutting review lanes (coverage)

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
  - pre-submission readiness (full/editor focus only)

Each lane writes a JSON array into `comments/`.

If subagents are unavailable, use the built-in deterministic fallback lane
pass in `scripts/audit.py` so the workflow still writes lane-compatible JSON
into `comments/` before consolidation.

### Phase 4: Consolidation

```bash
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir>
```

Consolidation rules:

- merge exact duplicates
- keep distinct paper-level consequences separate even if they share a root
  cause
- preserve singleton findings unless clearly false positive
- assign `comment_type`, `severity`, `confidence`, and `root_cause_key`

### Phase 5: Present result

Summarize:

- 1 short paragraph overall assessment
- counts of major / moderate / minor issues
- 3 highest-priority revision items
- identify the **Primary View** selected by `--report-style`
- path to `review_report.md`, `revision_suggestions.md` (root), and
  `artifacts/data/final_issues.json` / `artifacts/summary/peer_review_report.md`

## `gate`

1. Run:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode gate ...
   ```
2. **EIC Screening** (Phase 0.5): Read `agents/editor_in_chief_agent.md` and
   perform the editor-in-chief desk-reject screening on the paper's title,
   abstract, and introduction. This evaluates pitch quality, venue fit, fatal
   flaws, and presentation baseline. A desk-reject verdict is a gate blocker.
3. Report PASS/FAIL.
4. Present EIC screening results first (verdict + score + justification).
5. List blockers next.
6. Keep advisory items separate from blockers.
7. Keep `PRESUBMISSION` Major/Minor items advisory; only Critical mechanical
   findings can block the gate.
8. For IEEE pseudocode checks, make it explicit which issues are mandatory and
   which are only IEEE-safe recommendations.

## Resume Protocol

Deep-review writes a `checkpoint.json` at the workspace root so a session that
got interrupted (token budget, agent timeout, user `Ctrl-C`) can pick up where
it left off instead of restarting Phase 1.

### Files

- `<review_dir>/checkpoint.json` — schema defined in `scripts/checkpoint.py`.
- Status lifecycle: `prepared` -> `in_progress` -> `suspended` -> `completed`.
- Phase list mirrors Phase 1-5: `prepare`, `phase0_audit`, `committee`,
  `lanes`, `consolidation`, `present`.

### Reading

- `scripts/audit.py --review-dir <review_dir>` prints
  `[checkpoint] status=... lanes_completed=N lanes_suspended=M` on launch
  before running Phase 0. When the user types "continue" / "继续", treat
  any entry in `completed_lanes` as already done and dispatch only the
  remaining `lanes` / `committee` agents.

### Updating

When dispatching a lane or committee agent, instruct it to call
`checkpoint.mark_lane_completed(<review_dir>, <lane_name>)` (or
`mark_lane_suspended` on partial failure). Phase 3B lane templates should use
the `review_lane` value (e.g. `claims_vs_evidence`,
`notation_and_numeric_consistency`) as the lane identifier so consolidation
can correlate.

### Reset

- `scripts/audit.py --review-dir <review_dir> --no-resume` calls
  `checkpoint.reset_checkpoint`, restoring the checkpoint to its initial
  `prepared` state without deleting any workspace artifacts. Use it when the
  user explicitly asks for a clean rerun.

### Workspace boundary

The checkpoint lives only inside `<review_dir>/`. The audit tool does not
touch the user's working directory and does not delete other files inside the
workspace. Resuming is non-destructive.

## `re-audit`

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
   - root-cause-aware status labels: `FULLY_ADDRESSED`, `PARTIALLY_ADDRESSED`,
     `NOT_ADDRESSED`, `NEW`
   - use structured prior issue bundles when available, but still accept
     Markdown previous reports

## `polish`

1. Run the audit precheck:
   ```bash
   uv run python -B "$SKILL_DIR/scripts/audit.py" <paper> --mode polish ...
   ```
2. If blockers exist, stop and report them.
3. Only proceed into polishing if the precheck is safe.

## Committee Focus Routing (deep-review)

For `deep-review`, use the **Academic Pre-Review Committee** by default. This
is a 5-role review pass:

1. Editor (desk-reject screen)
2. Reviewer 1 (theory contribution)
3. Reviewer 3 (literature dialogue / gap)
4. Reviewer 2 (methodology transparency)
5. Reviewer 4 (logic chain)

If the user requests a single dimension, run only the matching committee
role(s).

Literature focus means:
- verify whether the literature is thematically synthesized or merely
  enumerated
- verify whether contradictions are acknowledged rather than flattened
- verify whether the claimed gap is genuine instead of manufactured by
  selective citation
- do **not** rewrite the related-work prose; hand that off to the
  format-specific writing skill when needed

If `--focus ...` is provided, it overrides keyword inference:

- `--focus full` (default)
- `--focus editor|theory|literature|methodology|logic`

### Keyword Map (English + Chinese)

| Focus | Keywords |
|---|---|
| editor | "desk reject", "pre-screen", "editor", "EIC", "主编", "预筛", "初筛" |
| theory | "theory", "contribution", "novelty", "theoretical dialogue", "理论", "贡献", "创新性" |
| literature | "related work", "literature", "research gap", "citation", "文献", "综述", "Research Gap", "引用", "gap is fake", "选择性引用" |
| methodology | "methods", "sample", "coding", "data", "design", "SRQR", "方法", "样本", "编码", "数据", "研究设计", "透明度" |
| logic | "logic", "argument", "causal", "structure", "论证", "因果", "逻辑", "结构" |

Output language: match the user's request language. If ambiguous, match the
paper language.
