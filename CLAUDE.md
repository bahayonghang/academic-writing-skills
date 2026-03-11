# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

- This repository ships **Claude Code skills** for academic writing workflows (LaTeX/Typst/PDF audit + Industrial AI literature synthesis).
- Skills live under `academic-writing-skills/` as **self-contained folders**.
- Documentation lives under `docs/` as a **VitePress** site (deployed to GitHub Pages on release).

## Common commands

### Python (skills + tests)

This repo uses **uv** + `pyproject.toml`.

```bash
# Install dev dependencies
uv sync --extra dev

# Run the full local CI pipeline
just ci

# Lint / format (Ruff)
just lint            # ruff format --check + ruff check
just format          # ruff format
just fix             # ruff format + ruff check --fix

# Type checking (Pyright)
just typecheck

# Tests
just test

# Run a single test file / test
uv run --extra dev python -m pytest tests/test_parsers.py -v
uv run --extra dev python -m pytest tests/test_parsers.py::test_latex_split_sections -v
```

Notes:
- The canonical task runner is the repo root `justfile`.
- Pyright is configured with `typeCheckingMode = "off"` (import checking / lightweight analysis).

### Docs (VitePress)

```bash
cd docs
npm install
npm run docs:dev

# Build / preview
npm run docs:build
npm run docs:preview
```

CI/Deploy detail:
- `.github/workflows/deploy.yml` builds the VitePress site and publishes `docs/.vitepress/dist` to GitHub Pages **on release published** (or manual workflow dispatch).

## Repository structure (big picture)

### 1) Skill packages (primary)

`academic-writing-skills/<skill-name>/` is the unit of distribution.

The core skills:
- `academic-writing-skills/latex-paper-en/`: English LaTeX paper workflows (IEEE/ACM/Springer/NeurIPS/ICML).
- `academic-writing-skills/latex-thesis-zh/`: Chinese thesis workflows (GB/T 7714 + template detection / structure mapping).
- `academic-writing-skills/typst-paper/`: Typst paper workflows (bilingual).
- `academic-writing-skills/paper-audit/`: Orchestrated audit across `.tex` / `.typ` / `.pdf`, with scoring and optional multi-agent review.
- `academic-writing-skills/industrial-ai-research/`: Literature research skill with an intake-first protocol.

Each skill typically contains:
- `SKILL.md`: entry spec + module router (how requests map to scripts).
- `scripts/`: Python tooling for compile/check/analyze.
- `references/` or `resources/`: reference docs the skill reads at runtime.
- optionally `agents/`, `evals/`, `examples/`, `templates/`.

### 2) Shared script patterns (how skills work)

Most skills implement a **module router** pattern:
- user intent → module (compile/format/bibliography/grammar/sentences/logic/expression/title/deai/experiment/…)
- module → run a single Python script under `scripts/` via `uv run python -B ...`

`paper-audit` is the cross-format orchestrator:
- For `.tex` / `.typ` audits, it reuses checks from sibling skills’ `scripts/` where possible.
- For `.pdf` audits, it uses `paper-audit/scripts/` (PDF parsing + visual/layout checks).

Tests live centrally under `tests/` and validate the parser + analysis utilities used by multiple skills.

### 3) Docs site

- `docs/` is a standalone VitePress project.
- `docs/.vitepress/config.ts` defines navigation, i18n (English + `zh/`), and the GitHub Pages base path.

## Non-negotiable content safety constraints (skills)

These constraints are repeated across skill specs and must not be broken when editing scripts or prompts:

- **Never modify** LaTeX inside `\cite{}`, `\ref{}`, `\label{}` or math environments.
- **Never modify** Typst inside `@cite`, `<label>`, or `$...$` math.
- **Never fabricate** bibliography entries; only operate on existing `.bib` / `.yml`.
- Do not change protected terminology unless the user explicitly approves (see each skill’s `references/FORBIDDEN_TERMS.md` where present).
- Prefer emitting **commented diff/suggestion blocks** rather than silently rewriting source content.

## When you’re unsure where to start

- For any behavior change, start at the relevant `academic-writing-skills/<skill>/SKILL.md` (it documents module routing and the “read next” reference files).
- For CI failures, run `just ci` locally and then narrow to `just lint`, `just typecheck`, or `just test`.
