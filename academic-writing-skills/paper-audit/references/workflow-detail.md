# Workflow Detail

Per-step detail that supplements `references/MODE_GUIDE.md`. `SKILL.md`
keeps the step skeleton; read this file when actually running a mode.

## Workspace overwrite protection (deep-review Phase 1)

If the target review workspace already exists, stop and ask before replacing
it. Use `prepare_review_workspace.py --overwrite` only after the user confirms
the existing artifacts can be discarded; for the all-in-one
`audit.py --mode deep-review` path, use `--overwrite-workspace` after the same
confirmation.

## Consolidation command sequence (deep-review Phase 4/5)

```bash
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir> --lang $LANG
uv run python -B "$SKILL_DIR/scripts/render_html_report.py" <review_dir> --lang $LANG
```

Note the `--lang $LANG` flags on both renderers — pass the locked report
language so Markdown and HTML twins render consistently.

## Peer-review report style

When the user explicitly asks for journal-review prose, set
`--report-style peer-review`. `review_report.md` remains the primary
artifact in the workspace root; `peer_review_report.md` is generated as
a companion under `artifacts/summary/` for that style.

## Revision suggestions (optional post-consolidation step)

After consolidation, the deep-review workflow optionally invokes
`agents/revision_suggestion_agent.md` to produce
`artifacts/data/revision_suggestions.json` with concrete original/suggested
text pairs and additional actions. When the file is present,
`revision_suggestions.md` and its HTML twin pick it up automatically; when
absent, both fall back to the priority/section roadmap skeleton.

## Gate presentation order

Run **EIC Screening** (Phase 0.5) using `agents/editor_in_chief_agent.md`
first; report PASS/FAIL; present verdict -> EIC -> blockers -> advisory. A
desk-reject verdict is a gate blocker. Only Critical `PRESUBMISSION` findings
block the gate.

## Re-audit status labels

Present root-cause-aware status labels: `FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

## Polish safety stop

If the audit precheck reports blockers, stop and report them. Only proceed
into polishing if the precheck is safe.
