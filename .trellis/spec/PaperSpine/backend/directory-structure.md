# Directory Structure

PaperSpine keeps source, installable output, and tests separate:

- `src/scripts/`: canonical shared Python helpers and entrypoints.
- `src/references/`: canonical workflow/reference docs used by the skills.
- `src/agents/`: shared agent metadata source.
- `dist/`: installable output for Claude Code, Codex, and OpenClaw.
- `.claude-plugin/`: Claude Code plugin metadata driven from the canonical
  dist version manifest.
- `tests/`: unit tests that mirror the script-level behavior and the dist
  layout.
- `install.ps1` and `install.sh`: host installers.

Local pattern:

- Treat `src/scripts/` as the source of truth for deterministic helpers.
- Treat `src/references/` as the source of truth for shared reference docs.
- Keep the suite skills flat in `dist/claude/skills`, `dist/codex/skills`, and
  `dist/openclaw/skills`.
- Keep `dist/claude/commands/paperspine.md` as the single Claude Code command
  entrypoint.
- Mirror source changes into dist using `sync_local_installs.py` instead of
  hand-editing each host copy.

Reference files:

- `ref/PaperSpine/README.md`
- `ref/PaperSpine/src/scripts/sync_local_installs.py`
- `ref/PaperSpine/tests/test_skill_structure.py`

Avoid:

- Copying the whole repository into a skills folder.
- Editing dist host copies one by one when the sync script already fans out the
  canonical files.
- Mixing install-time output with shared source helpers.
