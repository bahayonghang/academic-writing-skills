# PaperSpine Backend Guidelines

In this package, "backend" means the shared Python scripts, installers, update
logic, artifact validators, and test coverage that support the installable skill
suite. The repo uses standard library Python for these helpers.

## Pre-Development Checklist

Before editing scripts or install/update behavior:

1. Read [Directory Structure](./directory-structure.md) to keep source, dist,
   and test ownership clear.
2. Read [Configuration And State](./database-guidelines.md) before changing
   JSON files, install state, or dist version manifests.
3. Read [Error Handling](./error-handling.md) before changing validation,
   update, or wizard failure behavior.
4. Read [Quality Guidelines](./quality-guidelines.md) before changing script
   style or verification commands.
5. Read [Logging Guidelines](./logging-guidelines.md) before changing stdout or
   stderr output.

## Guidelines Index

| Guide | Local Meaning |
|-------|---------------|
| [Directory Structure](./directory-structure.md) | `src/`, `dist/`, tests, and install flow |
| [Configuration And State](./database-guidelines.md) | JSON config/state/version manifests; no DB |
| [Error Handling](./error-handling.md) | Update, wizard, and validation failure behavior |
| [Quality Guidelines](./quality-guidelines.md) | Standard library style and repo checks |
| [Logging Guidelines](./logging-guidelines.md) | CLI status, markdown/json reports, and error output |

## Reference Files

- `ref/PaperSpine/src/scripts/sync_local_installs.py`
- `ref/PaperSpine/src/scripts/paperspine_update.py`
- `ref/PaperSpine/src/scripts/intake_wizard.py`
- `ref/PaperSpine/src/scripts/artifact_check.py`
- `ref/PaperSpine/src/scripts/structured_review.py`
- `ref/PaperSpine/src/scripts/_paper_spine_utils.py`
- `ref/PaperSpine/tests/test_skill_structure.py`
- `ref/PaperSpine/tests/test_update_script.py`
