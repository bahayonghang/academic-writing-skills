# Component Guidelines

Components are Markdown packages consumed by agents. Write them as executable
instructions, not marketing copy.

Skill files:

- Use YAML frontmatter with at least `name` and a trigger-rich `description`.
- Keep the first body section as the operational entrypoint.
- Add `references/` only for material that should be loaded on demand.
- Add `examples/` for concrete reusable patterns.

Command files:

- Commands are instructions for Claude, not messages to the user.
- Include `description` and `argument-hint` when arguments are expected.
- Use project-relative or plugin-relative references. For plugin commands,
  prefer `${CLAUDE_PLUGIN_ROOT}` over hardcoded paths.
- Keep one command focused on one workflow.

Reference files:

- `ref/claude-scholar/skills/command-development/SKILL.md`
- `ref/claude-scholar/skills/command-development/references/plugin-features-reference.md`
- `ref/claude-scholar/commands/sc/sc.md`

Avoid:

- Describing what a command will do without instructing the agent how to do it.
- Generic command names that collide with common user commands.
- Loading every reference file from a skill when the local pattern is
  progressive disclosure.
