---
name: latex-thesis-zh
description: Compile, inspect, and polish Chinese LaTeX theses (XeLaTeX/LuaLaTeX). Use when working on an existing .tex thesis project needing compilation, GB/T 7714 checks, structure mapping, or academic editing.
metadata:
  category: academic-writing
  tags: [latex, thesis, chinese, phd, master, xelatex, gb7714, thuthesis, pkuthss, compilation, bibliography, structure]
argument-hint: "[main.tex] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(xelatex *), Bash(lualatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *)
---

# LaTeX 中文学位论文助手

## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Thesis build fails or toolchain is unclear | `uv run python $SKILL_DIR/scripts/compile.py main.tex` | `references/COMPILATION.md` |
| `format` | User asks about thesis formatting or GB/T 7714 layout | `uv run python $SKILL_DIR/scripts/check_format.py main.tex` | `references/GB_STANDARD.md` |
| `structure` | Need chapter/section map or thesis skeleton overview | `uv run python $SKILL_DIR/scripts/map_structure.py main.tex` | `references/STRUCTURE_GUIDE.md` |
| `consistency` | Terms, abbreviations, or naming drift across chapters | `uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms` | `references/LOGIC_COHERENCE.md` |
| `template` | Need to identify or validate thesis class/template | `uv run python $SKILL_DIR/scripts/detect_template.py main.tex` | `references/UNIVERSITIES/generic.md` |
| `bibliography` | GB/T 7714 or BibTeX validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714` | `references/GB_STANDARD.md` |
| `title` | Optimize Chinese thesis titles and chapter titles | `uv run python $SKILL_DIR/scripts/optimize_title.py main.tex --check` | `references/TITLE_OPTIMIZATION.md` |
| `deai` | Reduce AI-writing traces in visible Chinese prose | `uv run python $SKILL_DIR/scripts/deai_check.py main.tex --section introduction` | `references/DEAI_GUIDE.md` |
| `experiment` | Review experiment chapter language and structure | `uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments` | `references/modules/EXPERIMENT.md` |

## Workflow

1. Parse `$ARGUMENTS` for entry file and module. If missing, ask for the thesis `.tex` entry file and target module.
2. Read the one reference file tied to that module (see "Read next" column).
3. Run the corresponding script with `uv run python ...`.
4. Return findings as `% Module (L##) [Severity] [Priority]: ...`. Report exact command and exit code on failure.
5. If template and structure are both unclear, run `template` first, then `structure`.

## Safety

- Never fabricate citations, funding statements, acknowledgements, or academic claims.
- Never rewrite `\cite{}`, `\ref{}`, `\label{}`, math blocks, or bibliography keys unless explicitly asked.

## Scope Exclusions

Not for English papers, Typst projects, DOCX-only editing, literature research without `.tex` files, or writing a thesis from scratch.
