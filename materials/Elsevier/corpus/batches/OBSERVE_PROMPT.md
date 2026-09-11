# Observation-only batch

Write only `materials/Elsevier/observations/<KEY>.md`. Do not edit TSV, inventory, scripts, SKILL.md, README, `materials/IEEE/`, or `academic-writing-skills/`. Do not git commit. Do not spawn subagents.

## For each key in your batch JSON

1. Skip if `materials/Elsevier/observations/<KEY>.md` already exists.
2. `zot --json item get <KEY>`
3. `zot --json item pdf <KEY> --pages 1-3`, then more pages for method / experiments / conclusion.
4. Follow `materials/Elsevier/observations/_schema.md`.
5. `status: complete`, `has_pdf: true`, `date_observed: 2026-09-11`.
6. `story_pattern`: `SP-ELS-001` if independent Related Work; `SP-ELS-002` if related work is inlined in Introduction.
7. At least 3 writing observations with verbatim PDF quotes. Join `U+0002` hyphenation.
8. Do not use Zotero AI interpretation notes as evidence.
9. `In this paper` / `this paper proposes` / `this study proposes` belong in House style / phrases, not anti-AI.

Finish every key. Report written / skipped / failed.
