---
name: typst-paper
description: Typst academic paper assistant (Chinese and English). Use when writing, compiling, or improving Typst papers for conference submissions.
metadata:
  category: academic-writing
  tags: [typst, paper, chinese, english, ieee, acm, springer, neurips, deep-learning, compilation, grammar, bibliography]
argument-hint: "[main.typ] [--section SECTION] [--module MODULE]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(typst *)
---

# Typst Academic Paper Assistant

Process Typst academic papers using analysis scripts.

## Steps

1. Parse inputs from `$ARGUMENTS`. If missing, ask the user for the `.typ` file path and target module.
2. Review context in `$SKILL_DIR/references/TYPST_SYNTAX.md` and `$SKILL_DIR/references/STYLE_GUIDE.md`.
3. Locate the appropriate script command in `$SKILL_DIR/references/modules/` based on the user's request, or run standard checks in `$SKILL_DIR/scripts/`.
4. Run the required tool or script (e.g., `typst compile main.typ` or `python $SKILL_DIR/scripts/check_format.py main.typ`).
5. Output all suggestions in standard Typst diff-comment format `// MODULE (Line N) [Severity] [Priority]: Issue ...`
6. Never modify `@cite`, `@ref`, `<label>`, or `$...$` math environments without explicit user permission.

## Examples

- Run `typst compile $ARGUMENTS`.
- Run `python $SKILL_DIR/scripts/check_format.py $ARGUMENTS`.

## Troubleshooting

- Provide `main.typ` and `--module` when arguments are missing.
- Report command output and exit code when a tool returns non-zero.
