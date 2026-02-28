---
name: paper-audit
description: Unified paper audit for Chinese and English papers. Use when reviewing paper quality, pre-submission checks, or doing adversarial reviews.
metadata:
  category: academic-writing
  tags: [audit, review, paper, pdf, latex, typst, chinese, english, scoring, checklist]
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode MODE] [--pdf-mode MODE] [--style STYLE] [--journal VENUE]"
allowed-tools: Read, Glob, Grep, Bash(python *), Task
---

# Paper Audit Skill

Unified academic paper auditing across formats and languages.

## Steps

1. Parse the paper path and mode from `$ARGUMENTS`. If missing, confirm the target `.tex`, `.typ`, or `.pdf` file.
2. Review evaluation criteria in `$SKILL_DIR/references/REVIEW_CRITERIA.md` and `$SKILL_DIR/references/CHECKLIST.md`.
3. Run the orchestrator: `python $SKILL_DIR/scripts/audit.py $ARGUMENTS`.
4. Present the MD report directly to the user. Distinguish between automated findings and LLM-judgment scores.
5. If in `review` mode, read `$SKILL_DIR/references/SCHOLAR_EVAL_GUIDE.md` and formulate LLM assessments for Novelty, Significance, Ethics, and Reproducibility.
6. If in `polish` mode, read `.polish-state/precheck.json` and spawn nested tasks for the Critic Agent and Mentor Agents as defined in the original workflow specifications.

## Examples

- Run `python $SKILL_DIR/scripts/audit.py $ARGUMENTS`.
- Run `python $SKILL_DIR/scripts/audit.py paper.pdf --mode review`.

## Troubleshooting

- Provide a valid `.tex`, `.typ`, or `.pdf` path when arguments are missing.
- Report command output and exit code when audit execution fails.
