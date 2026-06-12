# Claude Scholar User-Facing Package Guidelines

Claude Scholar has no browser frontend. In this layer, "frontend" means the
Markdown assets users and agents discover: `skills/`, `commands/`, `agents/`,
`rules/`, `CLAUDE*.md`, and localized README/setup documents.

## Pre-Development Checklist

Before editing user-facing assets:

1. Read [Directory Structure](./directory-structure.md) for package layout.
2. Read [Component Guidelines](./component-guidelines.md) before adding or
   changing skills, commands, agents, or rule files.
3. Read [Hook Guidelines](./hook-guidelines.md) before documenting behavior that
   depends on installed hooks.
4. Read [State Management](./state-management.md) before changing installation
   wording, sidecar CLAUDE behavior, or settings assumptions.
5. Read [Quality Guidelines](./quality-guidelines.md) and [Type Safety](./type-safety.md)
   before changing frontmatter, JSON/YAML references, or localized docs.

## Guidelines Index

| Guide | Local Meaning |
|-------|---------------|
| [Directory Structure](./directory-structure.md) | User-facing package layout |
| [Component Guidelines](./component-guidelines.md) | Markdown skill, command, agent, and rule authoring |
| [Hook Guidelines](./hook-guidelines.md) | Hook-facing docs and settings-template coordination |
| [State Management](./state-management.md) | Install-state, sidecars, and README promises |
| [Quality Guidelines](./quality-guidelines.md) | Documentation parity and portability |
| [Type Safety](./type-safety.md) | Frontmatter, JSON, YAML, and path contracts |

## Reference Files

- `ref/claude-scholar/CLAUDE.md`
- `ref/claude-scholar/README.md`
- `ref/claude-scholar/README.zh-CN.md`
- `ref/claude-scholar/skills/command-development/SKILL.md`
- `ref/claude-scholar/commands/sc/sc.md`
- `ref/claude-scholar/settings.json.template`
