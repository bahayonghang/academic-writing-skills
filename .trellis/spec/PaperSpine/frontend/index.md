# PaperSpine Frontend Guidelines

In this package, "frontend" means the installable skill, command, README, and
plugin surfaces that users and host agents consume. There is no browser UI.

## Pre-Development Checklist

Before editing dist skills, commands, or user docs:

1. Read [Directory Structure](./directory-structure.md) to confirm the host
   layout and canonical dist sources.
2. Read [Component Guidelines](./component-guidelines.md) before changing skill
   or command frontmatter and body structure.
3. Read [Hook Guidelines](./hook-guidelines.md) before changing launcher or
   host-integration docs.
4. Read [State Management](./state-management.md) before changing workflow
   artifact promises or install/config wording.
5. Read [Quality Guidelines](./quality-guidelines.md) and [Type Safety](./type-safety.md)
   before changing localized docs, metadata, or generated skill files.

## Guidelines Index

| Guide | Local Meaning |
|-------|---------------|
| [Directory Structure](./directory-structure.md) | Dist host layout and canonical source flow |
| [Component Guidelines](./component-guidelines.md) | Skill, command, and plugin frontmatter/body patterns |
| [Hook Guidelines](./hook-guidelines.md) | Launcher and host-integration docs |
| [State Management](./state-management.md) | Workflow artifact trees and install-state promises |
| [Quality Guidelines](./quality-guidelines.md) | README parity, portability, and package hygiene |
| [Type Safety](./type-safety.md) | Structured metadata and config-field contracts |

## Reference Files

- `ref/PaperSpine/README.md`
- `ref/PaperSpine/README.en.md`
- `ref/PaperSpine/dist/claude/skills/paper-spine/SKILL.md`
- `ref/PaperSpine/dist/claude/commands/paperspine.md`
- `ref/PaperSpine/src/agents/openai.yaml`
- `ref/PaperSpine/tests/test_skill_structure.py`
- `ref/PaperSpine/tests/test_cross_platform_and_ui.py`
