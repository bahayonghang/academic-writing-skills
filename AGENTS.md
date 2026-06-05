# Repository Guidelines

## Project Structure & Module Organization
Core skill packages live under `academic-writing-skills/`, with one directory per skill such as `latex-paper-en/`, `latex-thesis-zh/`, `typst-paper/`, `bib-search-citation/`, and `paper-audit/`. Each skill typically contains `SKILL.md`, `scripts/`, `references/`, `examples/`, and optional `agents/` or `evals/`. Automated tests live in `tests/` and mirror script-level behavior. User-facing documentation is in `docs/` with localized content under `docs/zh/`. Use `ref/` for supporting reference material, not product code.

## Build, Test, and Development Commands
Use `uv` for Python workflows and `just` as the main task runner.

- `just install`: install runtime and dev dependencies with `uv sync --extra dev`.
- `just lint`: run `ruff format --check` and `ruff check`.
- `just typecheck`: run `pyright`.
- `just test`: run the pytest suite in `tests/`.
- `just ci`: run lint, type checks, and tests in sequence.
- `just docs`: start the VitePress docs site locally from `docs/`.
- `just doc-build`: build the static documentation site.

## Coding Style & Naming Conventions
Target Python 3.10+ and keep code compatible with the repository’s `pyright` and `ruff` settings. Follow Ruff’s 100-character line length and default formatter output; run `just fix` before opening a PR when needed. Use `snake_case` for Python modules, functions, and test files, and keep skill directories kebab-cased to match existing package names such as `latex-paper-en`. Prefer small script utilities in `scripts/` over embedding logic in `SKILL.md`.

## Testing Guidelines
Pytest is the test framework. Name files `test_*.py`, test functions `test_*`, and place shared fixtures in `tests/conftest.py`. Add or update tests whenever changing parsing, validation, or report-generation scripts. Run `just test` locally before submitting; use `just ci` for broader verification when touching multiple skills or docs tooling.

## Commit & Pull Request Guidelines
Recent history follows scoped Conventional Commit style, often with a Chinese summary, for example `docs: ...` or `refactor(latex-thesis-zh): ...`. Keep commits focused by skill or subsystem. PRs should include a short summary, affected paths, test evidence (`just test` or `just ci`), and screenshots for `docs/` UI changes. Link the relevant issue when one exists.

## Documentation & Contributor Notes
When adding a new skill, mirror the existing layout: `SKILL.md`, executable helpers in `scripts/`, concrete examples, and concise references. Keep docs synchronized across `README.md`, `README_CN.md`, and the VitePress pages when behavior changes.
<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

This project is managed by Trellis. The working knowledge you need lives under `.trellis/`:

- `.trellis/workflow.md` — development phases, when to create tasks, skill routing
- `.trellis/spec/` — package- and layer-scoped coding guidelines (read before writing code in a given layer)
- `.trellis/workspace/` — per-developer journals and session traces
- `.trellis/tasks/` — active and archived tasks (PRDs, research, jsonl context)

If a Trellis command is available on your platform (e.g. `/trellis:finish-work`, `/trellis:continue`), prefer it over manual steps. Not every platform exposes every command.

If you're using Codex or another agent-capable tool, additional project-scoped helpers may live in:
- `.agents/skills/` — reusable Trellis skills
- `.codex/agents/` — optional custom subagents

Managed by Trellis. Edits outside this block are preserved; edits inside may be overwritten by a future `trellis update`.

<!-- TRELLIS:END -->
