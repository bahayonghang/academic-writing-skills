---
name: latex-thesis-zh
description: Chinese LaTeX academic thesis assistant (PhD/Master). Use when writing, reviewing, outlining, compiling, or de-AIing Chinese LaTeX theses.
metadata:
  category: academic-writing
  tags: [latex, thesis, chinese, phd, master, xelatex, gb7714, thuthesis, pkuthss, compilation, bibliography]
argument-hint: "[main.tex] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(xelatex *), Bash(lualatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *)
---

# LaTeX 中文学位论文助手

Process Chinese LaTeX theses using analysis scripts.

## Steps

1. Parse inputs from `$ARGUMENTS`. If missing, ask the user for the `.tex` file path and target module.
2. Review context in `$SKILL_DIR/references/ACADEMIC_STYLE_ZH.md` and `$SKILL_DIR/references/GB_STANDARD.md` if needed.
3. For exact module commands (Compile, Map Structure, GB/T 7714 Format, Expression, Logic, Trans, Bib, Templates, De-AI, Title, Caption), read the scripts folder or the corresponding `.md` file in `$SKILL_DIR/references/modules/` or `$SKILL_DIR/references/`.
4. Run the requested script (e.g., `python $SKILL_DIR/scripts/compile.py main.tex`).
5. Output all suggestions in standard LaTeX diff-comment format: `% 模块（第N行）[Severity] [Priority]: 问题 ...`
6. Never modify `\cite{}`, `\ref{}`, `\label{}`, or math environments without explicit user permission.

## Examples

- Run `python $SKILL_DIR/scripts/compile.py $ARGUMENTS`.
- Run `python $SKILL_DIR/scripts/check_format.py $ARGUMENTS`.

## Troubleshooting

- Provide `main.tex` and `--module` when arguments are missing.
- Report command output and exit code when a script returns non-zero.
