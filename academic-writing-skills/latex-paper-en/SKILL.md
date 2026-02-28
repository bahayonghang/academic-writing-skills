---
name: latex-paper-en
description: Audit and improve English LaTeX academic papers. Use when writing, reviewing, or compiling IEEE, ACM, Springer, NeurIPS, and ICML papers.
metadata:
  category: academic-writing
  tags: [latex, paper, english, ieee, acm, springer, neurips, icml, deep-learning, compilation, grammar, bibliography]
argument-hint: "[main.tex] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(pdflatex *), Bash(xelatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *), Bash(chktex *)
---

# LaTeX Academic Paper Assistant (English)

Process English LaTeX academic papers using analysis scripts.

## Steps

1. Parse inputs from `$ARGUMENTS`. If missing, ask the user for the `.tex` file path and target module.
2. Review context in `$SKILL_DIR/references/STYLE_GUIDE.md` and `$SKILL_DIR/references/VENUES.md` if needed.
3. Reference `$SKILL_DIR/references/modules/` for module guidance (Compile, Format, Grammar, Expression, Logic, Translation, etc.).
4. Run the required script (e.g., `python $SKILL_DIR/scripts/check_format.py main.tex`).
5. Output all suggestions in standard LaTeX diff-comment format: `% MODULE (Line N) [Severity] [Priority]: Issue ...`
6. Never modify `\cite{}`, `\ref{}`, `\label{}`, or math environments without explicit user permission.

## Examples

- Run `python $SKILL_DIR/scripts/check_format.py $ARGUMENTS`.
- Run `python $SKILL_DIR/scripts/compile.py $ARGUMENTS`.

## Troubleshooting

- Provide `main.tex` and `--module` when arguments are missing.
- Report command output and exit code when a script returns non-zero.
