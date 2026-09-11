---
name: ieee-writing-materials
description: >-
  Distilled IEEE Transactions writing knowledge from a metadata-filtered local
  corpus (industrial informatics, control, instrumentation, and related IEEE
  journals). Trigger when drafting or reviewing IEEE Transactions prose for
  Abstract, Introduction, Related Work, Method, Experiments, or Conclusion.
  Not a Nature polish skill and not a LaTeX format checker.
---

# IEEE Writing Materials

Root file is routing only. Executable patterns live in `knowledge/*.tsv`. Human summaries live in `references/`. Per-paper evidence lives in `observations/`.

## When to use

- IEEE Transactions English, especially Industrial Informatics, Instrumentation and Measurement, Neural Networks and Learning Systems, and other IEEE control / industrial venues
- Section-level wording that should follow this corpus rather than Nature house style

## Do not use

- Nature / Nature Portfolio polish
- Chinese thesis structure or wording (`latex-thesis-zh`)
- IEEE page layout, two-column format, citation style, compile, or catalog checks (`latex-paper-en`)

## Load order

Load only the files for the current section. Do not load every TSV by default.

1. `references/style-guide.md`
2. Exactly one file under `references/writing/` matching the section
3. Matching TSV rows for that section (`writing_rules.tsv`, `phrase_bank.tsv`, plus the statistical table the request needs)

Cite `core` rows, or a statistical opener with `paper_count >= 5`. Candidate rows stay in TSV until promotion.

Resume distillation with `scripts/next_pending.py`. Validate with `scripts/validate_knowledge.py`.
