# Copilot instructions (academic-writing-skills)

## Big picture
- This repo ships **Claude Code skills** under `.claude/skills/` and a **VitePress docs site** under `docs/`.
- `dist/` contains the packaged skill artifacts (`*.skill`) that users install.

## Key directories
- `.claude/skills/latex-paper-en/` (English paper skill)
  - Entry/spec: `SKILL.md`
  - Tools: `scripts/` (`compile.py`, `check_format.py`, `extract_prose.py`, `verify_bib.py`)
  - Reference docs: `references/` (e.g. `COMMON_ERRORS.md`, `VENUES.md`, `FORBIDDEN_TERMS.md`)
- `.claude/skills/latex-thesis-zh/` (Chinese thesis skill)
  - Entry/spec: `SKILL.md`
  - Tools: `scripts/` (`compile.py`, `check_format.py`, `map_structure.py`, `check_consistency.py`)
  - Reference docs: `references/` (e.g. `GB_STANDARD.md`, `STRUCTURE_GUIDE.md`, `UNIVERSITIES/`)

## Repo-specific rules (do not break)
- Both skills explicitly require:
  - Never touch LaTeX inside `\cite{}`, `\ref{}`, `\label{}` or math environments.
  - Never fabricate bibliography entries; only operate on existing `.bib`.
  - Don’t change protected terminology without permission (see `references/FORBIDDEN_TERMS.md`).
  - Prefer producing changes as **commented diff/suggestion blocks**, not silently rewriting content.

## Common workflows
- Docs (VitePress):
  - Dev: `cd docs && npm install && npm run docs:dev`
  - Build: `cd docs && npm run docs:build`
  - Preview: `cd docs && npm run docs:preview`
  - GitHub Pages deploy runs on **release published** and uploads `docs/.vitepress/dist` (see `.github/workflows/deploy.yml`).

## Packaging skills
- When changing a skill, update its `.claude/skills/<skill>/` contents and regenerate `dist/*.skill`.
- The simple packager validates `SKILL.md` YAML frontmatter and zips the skill folder:
  - Example: `python simple_package.py .claude/skills/latex-paper-en dist`

## Conventions
- Keep changes minimal and scoped to the relevant skill (`latex-paper-en` vs `latex-thesis-zh`).
- If you change shared behavior (e.g. compilation), consider whether both skills’ scripts should stay aligned.
