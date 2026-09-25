# Repository Guidelines

Shared maintainer facts for this repository live in this file.

Claude Code loads this file through the `@AGENTS.md` import in `CLAUDE.md`. Codex, Grok Build, Kimi Code, and OMP (Oh My Pi) discover `AGENTS.md` natively or through an explicit read path. Do not treat the Claude `@AGENTS.md` import syntax as universal.

Project version: **6.0.0** (`pyproject.toml`). Academic Use Only — Not for commercial use.

Applicable tools: Claude Code, Codex, Grok Build, Kimi Code, and OMP (Oh My Pi). Naming a tool here is not a runtime verification. Unrun five-tool runtime stays UNVERIFIED.

## Project Structure & Module Organization

Core skill packages live under `academic-writing-skills/`. There are seven skill root directories:

- `latex-paper-en/`
- `latex-thesis-zh/`
- `typst-paper/`
- `bib-search-citation/`
- `paper-audit/`
- `cover-letter/`
- `paper-writing-studio/`

Each skill typically contains `SKILL.md`, `scripts/`, `references/`, `examples/`, and optional `agents/`, `templates/`, or `evals/`. `SKILL.md` is the capability and routing source. Public `references/`, `templates/`, `examples/`, and Markdown `agents/` are the detailed rule sources. Automated tests live in `tests/` and in skill-local `academic-writing-skills/*/tests/`. User-facing documentation is in `docs/` with localized content under `docs/zh/`. The docs site is a bilingual mirror; do not infer skill behavior from old docs pages. Maintainer coding guidelines live under `.trellis/spec/`. Use `ref/` for supporting reference material, not product code.

Project-level rules must not use private absolute paths on a maintainer machine.

Maintaining this development repository and installing skills into a paper project are different paths. Skill packages must stay usable after copy into a manuscript repo. Do not depend on this repository’s private absolute paths or a local global tool config.

## Build, Test, and Development Commands

Use `uv` for Python workflows and `just` as the main task runner.

- `just install`: install runtime and dev dependencies with `uv sync --extra dev`.
- `just skills-install`: copy or symlink catalog skills into the current project's agent skill directories. Interactive by default, or pass skill names. GNU-style flags need `just -- skills-install ...`.
- `just check-versions`: run `tests/contracts/test_skill_versions.py`.
- `just lint`: run `ruff format --check` and `ruff check`.
- `just typecheck`: run `pyright`.
- `just test`: run pytest on `tests/` and each `academic-writing-skills/*/tests` directory.
- `just ci`: four steps in this order: `just check-versions`, `just lint`, `just typecheck`, `just test`.
- `just fix`: `ruff format` and `ruff check --fix`.
- `just docs`: start the VitePress docs site locally from `docs/`.
- `just doc-build`: build the static documentation site.

`just ci` has four steps, including `just check-versions`. `just ci` is not only lint, typecheck, and test.

Docs resource gate (not part of `just ci`): `uv run python docs/scripts/check_resource_sync.py`.

## Planning vs implementation

Task-creation or plan approval is not implementation approval. Implementation starts only after reviewed artifacts and `task.py start` (or the platform equivalent). Cheaper models must not self-expand scope. Stay inside the approved file and test boundary. Escalate when a new interface appears, the change crosses unapproved directories, an academic conclusion changes, or a failure falls outside the plan.

## Academic fact protection

These constraints apply across all skills:

1. Never modify content inside `\cite{}`, `\ref{}`, `\label{}`, math environments (LaTeX), or `@cite`, `<label>`, `$...$` (Typst).
2. Never fabricate bibliography entries, author names, venue names, or experimental results.
3. Never change protected terminology without explicit permission (see each skill's `references/FORBIDDEN_TERMS.md`).
4. Output changes as diff/suggestion blocks with severity and priority fields. Tag source as `[Script]` (automated) or `[LLM]` (agent judgment).

## Coding Style & Naming Conventions

Target Python 3.10+ and keep code compatible with the repository’s `pyright` and `ruff` settings. Follow Ruff’s 100-character line length and default formatter output; run `just fix` before opening a PR when needed. Use `snake_case` for Python modules, functions, and test files, and keep skill directories kebab-cased to match existing package names such as `latex-paper-en`. Prefer small script utilities in `scripts/` over embedding logic in `SKILL.md`.

Pyright uses `typeCheckingMode = "basic"`. Errors fail `just ci`. Existing warnings are a baseline; do not batch-clean them unless a change newly requires a fix.

## Parser copies

Five skills ship `scripts/parsers.py`: `latex-paper-en`, `latex-thesis-zh`, `typst-paper`, `paper-audit`, and `cover-letter`. `bib-search-citation` and `paper-writing-studio` do not. `DocumentParser` (ABC) → `LatexParser`, `TypstParser`. Key methods: `split_sections()`, `extract_visible_text()`, `clean_text()`, `get_comment_prefix()`. Keep copies aligned when changing shared behavior. The contract is `tests/contracts/test_parsers_alignment.py` (hash-locked `ALIGNMENTS`; canonical copy = `latex-paper-en`). Per-skill divergences are intentional and documented there — e.g. `latex-thesis-zh` omits `clean_text`, `typst-paper` omits `LatexParser`. Update `ALIGNMENTS` when a divergence is deliberate.

PDF audit uses lazy `pymupdf` (PyMuPDF). The enhanced path also uses optional `pymupdf4llm`.

## Testing Guidelines

Pytest is the test framework. Name files `test_*.py`, test functions `test_*`, and place shared fixtures in `tests/conftest.py`. Add or update tests whenever changing parsing, validation, or report-generation scripts. Run `just test` locally before submitting; use `just ci` for broader verification when touching multiple skills or docs tooling.

`tests/conftest.py` inserts `SCRIPT_DIR_EN` and `SCRIPT_DIR_AUDIT` on `sys.path`. The same file appends `SCRIPT_DIR_ZH` and `SCRIPT_DIR_COVER_LETTER` so those copies do not shadow the canonical EN/AUDIT parsers. Bare imports such as `from parsers import LatexParser` load the EN/AUDIT copies. Cover-letter tests load scripts with `importlib.util.spec_from_file_location`. Path constants live in `tests.support.paths`.

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
