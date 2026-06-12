# Hook Guidelines

PaperSpine does not define repo-local hooks. In this layer, use the file for
launcher and host-integration docs that affect what the user sees.

Local pattern:

- The UI launcher must be referenced by absolute installed paths in the skill
  docs.
- The Windows launcher must force UTF-8 and the macOS/Linux launcher must cover
  at least one terminal emulator path.
- The intake skill should point users to the UI first when it is available.
- Avoid relative launcher examples in reusable docs.

Reference files:

- `ref/PaperSpine/src/scripts/launch_paperspine_ui.ps1`
- `ref/PaperSpine/src/scripts/launch_paperspine_ui.sh`
- `ref/PaperSpine/tests/test_cross_platform_and_ui.py`
- `ref/PaperSpine/dist/claude/skills/paper-spine-ui/SKILL.md`

Avoid:

- Relative launcher invocations in skill docs.
- UI docs that fail to mention the host-specific launcher path.
- Promising automatic behavior that the host skill does not actually trigger.
