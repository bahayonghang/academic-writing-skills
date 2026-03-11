---
name: latex-thesis-zh
description: Chinese LaTeX academic thesis assistant for existing PhD or Master's thesis `.tex` projects. Use this skill whenever the user wants to compile, inspect, or improve a Chinese LaTeX thesis, including structure mapping, template detection, GB/T 7714 bibliography checks, terminology consistency, title optimization, de-AI editing, or experiment-section review. Trigger even when the user mentions only one chapter, one template problem, or one bibliography issue.
metadata:
  category: academic-writing
  tags: [latex, thesis, chinese, phd, master, xelatex, gb7714, thuthesis, pkuthss, compilation, bibliography, structure]
argument-hint: "[main.tex] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(uv *), Bash(xelatex *), Bash(lualatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *)
---

# LaTeX 中文学位论文助手

Use this skill for targeted work on an existing Chinese LaTeX thesis project. Keep the skill focused on thesis engineering and academic polish, not end-to-end drafting.

## Capability Summary

- Compile Chinese LaTeX theses with XeLaTeX/LuaLaTeX-aware guidance.
- Map thesis structure, detect common university templates, and review chapter organization.
- Check GB/T 7714 bibliography quality, title quality, terminology consistency, and AI-writing traces.
- Review experiment sections while preserving thesis syntax and references.

## Triggering

Use this skill when the user has an existing Chinese thesis `.tex` project and wants help with:

- compilation or template/toolchain issues
- thesis structure mapping and chapter layout review
- template detection for thuthesis, pkuthss, or similar setups
- terminology or abbreviation consistency
- GB/T 7714 bibliography validation
- title optimization or de-AI editing
- experiment-section review

## Do Not Use

Do not use this skill for:

- English conference/journal paper workflows
- Typst thesis or Typst paper projects
- deep literature research without thesis source files
- writing a thesis from scratch without an existing project structure
- DOCX-only thesis editing

## Module Router

| Module | Use when | Primary command | Read next |
| --- | --- | --- | --- |
| `compile` | Thesis build fails or toolchain is unclear | `uv run python $SKILL_DIR/scripts/compile.py main.tex` | `references/COMPILATION.md` |
| `format` | User asks about thesis formatting or GB/T 7714 layout expectations | `uv run python $SKILL_DIR/scripts/check_format.py main.tex` | `references/GB_STANDARD.md` |
| `structure` | Need chapter/section map or thesis skeleton overview | `uv run python $SKILL_DIR/scripts/map_structure.py main.tex` | `references/STRUCTURE_GUIDE.md` |
| `consistency` | Terms, abbreviations, or naming drift across chapters | `uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms` | `references/LOGIC_COHERENCE.md` |
| `template` | Need to identify or validate thesis class/template | `uv run python $SKILL_DIR/scripts/detect_template.py main.tex` | `references/UNIVERSITIES/generic.md` |
| `bibliography` | GB/T 7714 or BibTeX validation | `uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714` | `references/GB_STANDARD.md` |
| `title` | Optimize Chinese thesis titles and chapter titles | `uv run python $SKILL_DIR/scripts/optimize_title.py main.tex --check` | `references/TITLE_OPTIMIZATION.md` |
| `deai` | Reduce AI-writing traces in visible Chinese prose | `uv run python $SKILL_DIR/scripts/deai_check.py main.tex --section introduction` | `references/DEAI_GUIDE.md` |
| `experiment` | Review experiment chapter language and structure | `uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments` | `references/modules/EXPERIMENT.md` |

## Required Inputs

- `main.tex` or thesis entrypoint.
- Optional `--section SECTION` or specific chapter name.
- Optional bibliography path when references are under review.
- Optional university/template context if the project is school-specific.

If arguments are missing, ask only for the thesis entry file and the target module.

## Output Contract

- Return findings in LaTeX diff-comment style whenever possible: `% 模块（第N行）[Severity] [Priority]: 问题 ...`
- Distinguish between build blockers, thesis-format issues, and writing-quality suggestions.
- Report the exact command used and the exit code when a script fails.
- Preserve `\cite{}`, `\ref{}`, `\label{}`, theorem environments, and math blocks unless the user explicitly asks for source edits.

## Workflow

1. Parse `$ARGUMENTS` and select the thesis-specific module.
2. Read the one reference file tied to that module.
3. Run the corresponding script with `uv run python ...`.
4. Return thesis-focused findings and next actions.
5. If template and structure are both unclear, run `template` first, then `structure`.

## Safety Boundaries

- Never fabricate citations, funding statements, acknowledgements, or academic claims.
- Never rewrite labels, bibliography keys, or math content by default.
- Keep template detection and prose editing separate so the user can verify each layer.

## Reference Map

- `references/ACADEMIC_STYLE_ZH.md`: Chinese academic style baseline.
- `references/COMPILATION.md`: XeLaTeX/LuaLaTeX compilation patterns.
- `references/GB_STANDARD.md`: GB/T 7714 and thesis-format essentials.
- `references/STRUCTURE_GUIDE.md`: thesis structure mapping guidance.
- `references/UNIVERSITIES/*.md`: school-specific template notes.

Read only the file that matches the active module.

## Example Requests

- “帮我定位这个 `thuthesis` 项目为什么 XeLaTeX 一直编译失败。”
- “请把这篇中文学位论文的结构梳理出来，并检查术语是否前后统一。”
- “按 GB/T 7714 看一下参考文献和标题有没有明显问题。”

See `examples/` for full request-to-command walkthroughs.
