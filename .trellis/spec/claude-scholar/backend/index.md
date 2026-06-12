# Claude Scholar Backend Guidelines

In this package, "backend" means install/update scripts, Node hook runtime,
configuration/state files, and safety checks that run outside the Markdown skill
surface. Claude Scholar has no web server and no relational database.

## Pre-Development Checklist

Before editing scripts, hooks, or install behavior:

1. Read [Directory Structure](./directory-structure.md) to confirm the ownership
   boundary between `hooks/`, `scripts/`, `rules/`, and install assets.
2. Read [Configuration And State](./database-guidelines.md) before touching
   `settings.json.template`, install manifests, package-manager state, or
   `.claude` state files.
3. Read [Error Handling](./error-handling.md) and [Logging Guidelines](./logging-guidelines.md)
   before changing hook decisions, installer output, or CLI status messages.
4. Read [Quality Guidelines](./quality-guidelines.md) before changing Node or
   shell utilities.

## Guidelines Index

| Guide | Local Meaning |
|-------|---------------|
| [Directory Structure](./directory-structure.md) | Runtime directories and script ownership |
| [Configuration And State](./database-guidelines.md) | JSON/settings state; there is no database layer |
| [Error Handling](./error-handling.md) | Hook exit codes, installer failures, safe fallbacks |
| [Quality Guidelines](./quality-guidelines.md) | Cross-platform JS/shell conventions and verification |
| [Logging Guidelines](./logging-guidelines.md) | Machine-readable hook output and human installer output |

## Reference Files

- `ref/claude-scholar/hooks/security-guard.js`
- `ref/claude-scholar/hooks/hook-common.js`
- `ref/claude-scholar/scripts/setup.sh`
- `ref/claude-scholar/scripts/uninstall.sh`
- `ref/claude-scholar/scripts/lib/utils.js`
- `ref/claude-scholar/scripts/lib/package-manager.js`
- `ref/claude-scholar/settings.json.template`
