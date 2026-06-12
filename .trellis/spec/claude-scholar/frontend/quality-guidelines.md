# Quality Guidelines

User-facing docs must stay concise, triggerable, and portable across local
install paths.

Local checks:

- README and localized README variants should describe the same install and
  safety semantics.
- Skill descriptions should contain user-intent verbs so agent tools can surface
  them.
- Command docs should be specific enough to execute without hidden context.
- Public docs must not contain private local paths, tokens, or one-machine
  assumptions.

Reference files:

- `ref/claude-scholar/CLAUDE.md`
- `ref/claude-scholar/README.md`
- `ref/claude-scholar/README.zh-CN.md`
- `ref/claude-scholar/README.ja-JP.md`
- `ref/claude-scholar/skills/command-development/SKILL.md`

Avoid:

- Long always-loaded instructions when a compact entrypoint plus on-demand
  references is enough.
- Vague skill descriptions such as "helper" or "internal tool".
- Documentation that promises install behavior not implemented by `setup.sh`.
