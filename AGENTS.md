# Repository Guidelines

## Project Structure & Module Organization
- `academic-writing-skills/` contains three skills: `latex-paper-en/`, `latex-thesis-zh/`, `typst-paper/`. Each skill has `SKILL.md`, `scripts/`, and `references/` plus a `README.md`.
- `docs/` hosts the VitePress documentation site, with localized content under `docs/zh/`.
- `tests/` contains unit tests (for example `tests/test_parsers.py`).
- Root metadata and config live in `pyproject.toml`, `requirements.txt`, and `README.md`.

## Build, Test, and Development Commands
- Docs dev server: `cd docs && npm install` then `npm run docs:dev` (local VitePress at http://localhost:5173).
- Docs build/preview: `npm run docs:build` and `npm run docs:preview`.
- Optional `just` shortcuts from `docs/justfile`, for example `cd docs && just build` or `just check-links`.
- Python tools run per skill, for example `python academic-writing-skills/latex-paper-en/scripts/check_format.py paper.tex --strict`.

## Coding Style & Naming Conventions
- Python uses 4-space indentation; keep functions small and CLI arguments explicit (argparse).
- Script names are action-oriented, such as `check_format.py` and `verify_bib.py`.
- Docs content stays in Markdown under `docs/` and `docs/zh/`.

## Testing Guidelines
- Tests use `unittest`.
- Run all tests with `python -m unittest`, or a single file with `python -m unittest tests/test_parsers.py`.
- Name new tests `test_*.py` under `tests/`.

## Commit & Pull Request Guidelines
- Follow the existing commit style: `:sparkles: feat(scope): message`, `:memo: docs: message`, `fix: message`. Common types include `feat`, `fix`, `docs`, `chore`, `refactor` with optional scopes.
- PRs should include a concise summary, the affected skill/module, and test evidence (command + result). Add screenshots when changing docs UI.

## Content Safety for Skills
- Do not edit LaTeX inside `\cite{}`, `\ref{}`, `\label{}` or math environments; do not edit Typst inside `@cite`, `<label>`, or `$...$`.
- Never fabricate bibliography entries; only use existing `.bib` or `.yml` files.
- Check forbidden terminology lists in `references/FORBIDDEN_TERMS.md` before changing terms.
