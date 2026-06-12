# Component Guidelines

PaperSpine components are skill and command Markdown files.

Skill patterns:

- Use YAML frontmatter with a short `name` and a trigger-rich `description`.
- Keep the main orchestrator and worker skills discoverable in every host.
- Keep worker skill descriptions under the portable length limit the tests
  enforce.
- The orchestrator should route by stage instead of patching prose directly.

Command patterns:

- `dist/claude/commands/paperspine.md` is the one Claude Code command entrypoint.
- Commands should point to the orchestrator skill and not duplicate the full
  workflow text.
- Keep command frontmatter portable and explicit.

Reference files:

- `ref/PaperSpine/dist/claude/skills/paper-spine/SKILL.md`
- `ref/PaperSpine/dist/claude/skills/paper-spine-ui/SKILL.md`
- `ref/PaperSpine/dist/claude/commands/paperspine.md`
- `ref/PaperSpine/tests/test_cross_platform_and_ui.py`

Avoid:

- Descriptions that hide the skill behind internal terminology.
- Skill files that are longer than necessary for the host to discover the right
  branch.
- Worker skills that try to replace the orchestrator.
