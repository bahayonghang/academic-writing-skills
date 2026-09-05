# Compile Module Reference

Purpose: Diagnose and fix compilation issues in Chinese LaTeX thesis projects.

## Skill Execution Boundary

Run compilation through the bundled wrapper and use the project's actual entry file and bibliography backend:

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

The wrapper also supports LuaLaTeX recipes. Detect the project before choosing; `main.tex`, XeLaTeX, and one
bibliography recipe are not universal defaults. The raw compiler commands below explain tool selection and are not
an instruction to bypass the wrapper. Do not clean an existing PDF, install a missing package, or enable
`--shell-escape` as an automatic recovery step.

## Compiler Selection

| Compiler | Best For | Command |
|----------|----------|---------|
| XeLaTeX | Chinese documents, Unicode, system fonts | `latexmk -xelatex main.tex` |
| LuaLaTeX | Modern features, Lua scripting, future-proofing | `latexmk -lualatex main.tex` |
| pdfLaTeX | English-only papers (poor CJK support) | `latexmk -pdf main.tex` |

## latexmk Configuration

Create `.latexmkrc` in project root:
```perl
$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -interaction=nonstopmode -no-shell-escape %O %S';
$bibtex_use = 2;
$biber = 'biber %O %S';
```

Enable `-shell-escape` only for sources you have explicitly verified as trusted.

## Common Issues

| Problem | Solution |
|---------|----------|
| Chinese font not found | Specify fonts: `\setCJKmainfont{SimSun}[BoldFont=SimHei]` |
| Missing package | Report the missing package and installation evidence; installation requires separate authorization |
| Bibliography not updating | Select the matching wrapper recipe and report its exact exit code and log evidence |

## Watch Mode

```bash
latexmk -xelatex -pvc main.tex  # auto-recompile on changes
```

## Figure and Table Layout Acceptance

After a caption, continued figure, long table, scaling, or image-resolution change:

1. require wrapper exit code 0 and use the PDF path reported for the selected entry and recipe;
2. inspect `.aux` and the list of figures/tables when numbering or continued entries are involved;
3. render and actually view the affected page and its adjacent pages;
4. check caption order, continuation marks, overflow, blank space, clipping, and text readability.

Compilation, an `.aux` entry, or a PNG file alone is not visual proof. If the renderer is unavailable or nobody
viewed the page, record `missing evidence`. Do not add PDF compression or UI automation to this workflow.

> Full details: see [`../latex/compilation.md`](../latex/compilation.md)
