# Copilot instructions (academic-writing-skills)

## Big picture
- This repo ships **Claude Code skills** under `academic-writing-skills/` and a **VitePress docs site** under `docs/`.

## Key directories
- `academic-writing-skills/latex-paper-en/` (English paper skill)
  - Entry/spec: `SKILL.md`
  - Tools: `scripts/` (`compile.py`, `check_format.py`, `extract_prose.py`, `verify_bib.py`, `deai_check.py`, `deai_batch.py`)
  - Reference docs: `references/` (e.g. `COMMON_ERRORS.md`, `VENUES.md`, `FORBIDDEN_TERMS.md`)
- `academic-writing-skills/latex-thesis-zh/` (Chinese thesis skill)
  - Entry/spec: `SKILL.md`
  - Tools: `scripts/` (`compile.py`, `check_format.py`, `map_structure.py`, `check_consistency.py`, `deai_check.py`, `deai_batch.py`)
  - Reference docs: `references/` (e.g. `GB_STANDARD.md`, `STRUCTURE_GUIDE.md`, `UNIVERSITIES/`)
- `academic-writing-skills/typst-paper/` (Typst paper skill)
  - Entry/spec: `SKILL.md`
  - Tools: `scripts/` (`compile.py`, `check_format.py`, `verify_bib.py`, `deai_check.py`, `deai_batch.py`)
  - Reference docs: `references/` (e.g. `STYLE_GUIDE.md`, `TYPST_SYNTAX.md`, `DEAI_GUIDE.md`)

## Repo-specific rules (do not break)
- All skills explicitly require:
  - Never touch LaTeX inside `\cite{}`, `\ref{}`, `\label{}` or math environments.
  - Never touch Typst inside `@cite`, `<label>`, or `$...$` math.
  - Never fabricate bibliography entries; only operate on existing `.bib` or `.yml`.
  - Don't change protected terminology without permission (see `references/FORBIDDEN_TERMS.md`).
  - Prefer producing changes as **commented diff/suggestion blocks**, not silently rewriting content.

## Common workflows
- Docs (VitePress):
  - Dev: `cd docs && npm install && npm run docs:dev`
  - Build: `cd docs && npm run docs:build`
  - Preview: `cd docs && npm run docs:preview`
  - GitHub Pages deploy runs on **release published** and uploads `docs/.vitepress/dist` (see `.github/workflows/deploy.yml`).

## Installation
- Users should manually copy skill folders to `~/.claude/skills/`:
  ```bash
  cp -r academic-writing-skills/latex-paper-en ~/.claude/skills/
  cp -r academic-writing-skills/latex-thesis-zh ~/.claude/skills/
  cp -r academic-writing-skills/typst-paper ~/.claude/skills/
  ```

## Conventions
- Keep changes minimal and scoped to the relevant skill (`latex-paper-en` vs `latex-thesis-zh` vs `typst-paper`).
- If you change shared behavior (e.g. compilation), consider whether all skills' scripts should stay aligned.
