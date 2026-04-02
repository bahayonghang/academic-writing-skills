# Quick Start

## 1. Pick the Skill

| If you have... | Use |
| --- | --- |
| An English LaTeX paper | `latex-paper-en` |
| A Chinese LaTeX thesis | `latex-thesis-zh` |
| A Typst paper | `typst-paper` |
| A paper you want to audit before submission | `paper-audit` |
| An Industrial AI topic to research | `industrial-ai-research` |

## 2. Try One Real Command

All repository-local Python examples below follow the repo rule: `uv run python ...`.

### English LaTeX paper

```bash
uv run python academic-writing-skills/latex-paper-en/scripts/compile.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_format.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py main.tex
uv run python academic-writing-skills/latex-paper-en/scripts/check_tables.py main.tex
```

### Chinese LaTeX thesis

```bash
uv run python academic-writing-skills/latex-thesis-zh/scripts/map_structure.py thesis.tex
uv run python academic-writing-skills/latex-thesis-zh/scripts/compile.py thesis.tex
```

### Typst paper

```bash
uv run python academic-writing-skills/typst-paper/scripts/compile.py main.typ
uv run python academic-writing-skills/typst-paper/scripts/check_format.py main.typ
```

### Paper audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus methodology
```

## 3. Typical Prompt Patterns

You can also call the skills conversationally in your agent runtime:

```text
Compile main.tex with the latex-paper-en skill.
```

```text
Map the structure of thesis.tex and check GB/T issues.
```

```text
Compile main.typ and review the abstract for grammar.
```

```text
Run a gate audit on paper.pdf before submission.
```

## 4. Recommended First Workflow

### For LaTeX papers

1. Compile.
2. Run format or bibliography checks.
3. Run grammar, sentence, or logic checks on a target section.

### For Chinese theses

1. Run structure mapping first.
2. Detect the template if it is unclear.
3. Compile and verify bibliography or consistency.

### For Typst papers

1. Compile.
2. Run format or bibliography checks.
3. Run language-quality modules on the section you are editing.

### For audits

1. Choose a mode: `quick-audit`, `deep-review`, `gate`, `polish`, or `re-audit`.
2. Point to the `.tex`, `.typ`, or `.pdf` file.
3. Add venue flags only when you actually need venue-specific checks.
4. Use `quick-audit` for fast screening and `deep-review` for the full reviewer-style workflow.
5. In `deep-review`, use `--focus ...` if you only want one committee dimension.
