# Workflow Detail

Per-step detail that supplements `references/MODE_GUIDE.md`. `SKILL.md`
keeps the step skeleton; read this file when actually running a mode.

## Workspace overwrite protection (deep-review Phase 1)

If the target review workspace already exists, stop and ask before replacing
it. Use `prepare_review_workspace.py --overwrite` only after the user confirms
the existing artifacts can be discarded; for the all-in-one
`audit.py --mode deep-review` path, use `--overwrite-workspace` after the same
confirmation.

## No-write review path (delivery level `T3`)

`SKILL.md` defines the three delivery levels. This section covers `T3`, where
nothing may be written to disk.

Write behavior for `quick-audit`, `gate`, `re-audit`, and `polish` was measured
on 2026-09-06 by running each in a directory holding only the paper file and
comparing the listing before and after. Every run finished and printed its
report on stdout, so "nothing" below means the run completed and left no file —
not that it failed to start. The `deep-review` row was not measured; it comes
from reading `scripts/audit.py` and `scripts/prepare_review_workspace.py`:

| Mode          | Writes                                                                                                        | `T3`                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `quick-audit` | nothing                                                                                                       | available                                    |
| `gate`        | nothing                                                                                                       | available                                    |
| `re-audit`    | nothing from `audit.py`; `diff_review_issues.py` may write `revision_trajectory.md` beside the current bundle | `T1` plain; `T2`/`T3` need `--no-trajectory` |
| `polish`      | `.polish-state/` next to the paper file                                                                       | unavailable                                  |
| `deep-review` | the review workspace                                                                                          | unavailable                                  |

`polish` also fails delivery level `T2` whenever the paper sits inside a
repository, because it writes beside the paper rather than in the current
working directory.

At `T3`, run `quick-audit` or `gate` and read the report from stdout. Do not
redirect stdout to a file, and do not pass `--output` / `-o` — that flag writes
a report file in every mode, not only in the ones listed as writing.

Set `PYTHONDONTWRITEBYTECODE=1` in the environment before the run. The table
above counts report and workspace files only. `audit.py` starts each check
script as a subprocess without `-B`, and `-B` on the parent does not propagate,
so without that variable Python writes `__pycache__/` into the skill's own
`scripts/` directories — a write inside this repository, which `T2` forbids,
and a write at all, which `T3` forbids.

`deep-review` cannot be degraded into `T3` — offer `quick-audit` or `gate`
instead and state what is lost: no committee multi-perspective pass, no
section or cross-cutting lanes, no consolidation dedup or root-cause merge, no
quote verification.

Name the scripts that could not run. Keep the two groups apart — conflating
them tells the reader that review evidence is missing when only an output file
is missing.

Scripts whose absence removes review evidence — mark each `missing evidence`:

- `prepare_review_workspace.py` — section index and paper summary
- `build_claim_map.py` — headline claims and claim candidates
- `consolidate_review_findings.py` — dedup and root-cause merge
- `verify_quotes.py` — quote verification against the source

Renderers whose absence removes only the written report, which `T3` forbids by
design — report them as not produced, not as `missing evidence`:

- `render_deep_review_report.py` — Markdown report render
- `render_html_report.py` — HTML report render

Do not describe any of these as completed by another means, and do not tag
anything `[Script]` on their behalf. The checkers that `quick-audit` and `gate`
do run at `T3` still produce genuine `[Script]` findings; only the
evidence-losing scripts in the first list above are `missing evidence`.

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
