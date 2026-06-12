# Directory Structure

PaperSpine distributes the same skill suite across three hosts:

- `dist/claude/skills/*`: Claude Code flat skill suite.
- `dist/claude/commands/*.md`: Claude Code slash-command entrypoint.
- `dist/codex/skills/*`: Codex flat skill suite.
- `dist/codex/paper-spine`: legacy Codex bundled fallback.
- `dist/openclaw/skills/*`: OpenClaw flat skill suite.
- `.claude-plugin/`: Claude Code plugin metadata.
- `src/`: canonical shared scripts, references, and agent metadata.

Local pattern:

- Keep the suite flat per host so the agent tool can discover each skill
  directly.
- Keep `paper-spine` as the orchestrator skill and the `paper-spine-*` folders
  as branch skills.
- Keep `paperspine.md` as the single Claude Code command entrypoint.
- Treat `dist/claude/skills` as the canonical skill source for the sync script.

Reference files:

- `ref/PaperSpine/README.md`
- `ref/PaperSpine/src/scripts/sync_local_installs.py`
- `ref/PaperSpine/tests/test_skill_structure.py`

Avoid:

- Copying the whole repository into a skills directory.
- Adding nested skill layouts that break flat discovery.
- Letting Codex, Claude, and OpenClaw drift into different skill sets.
