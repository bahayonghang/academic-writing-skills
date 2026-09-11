---
name: elsevier-writing-materials
description: >-
  Distilled Elsevier domain-journal writing knowledge from a metadata-filtered
  local corpus (process control, chemical engineering, industrial AI: JPC,
  CACE, EAAI, ESWA, Applied Energy, and related titles). Trigger when drafting
  or reviewing Elsevier English prose for Abstract, Introduction, Related Work,
  Method, Experiments, or Conclusion. Not a Nature polish skill, not IEEE
  Transactions, and not a LaTeX format checker.
---

# Elsevier Writing Materials

Root file is routing only. Executable patterns live in `knowledge/*.tsv`. Human summaries live in `references/`. Per-paper evidence lives in `observations/`.

## When to use

- Elsevier English in process control, chemical engineering, or industrial AI
- Journals on the local allowlist: Journal of Process Control, Computers & Chemical Engineering, Control Engineering Practice, ISA Transactions, Chemical Engineering Science, Applied Energy, Energy, Engineering Applications of Artificial Intelligence, Expert Systems with Applications, Advanced Engineering Informatics

## Do not use

- Nature / Nature Portfolio polish
- IEEE Transactions wording (`materials/IEEE`)
- Chinese thesis structure (`latex-thesis-zh`)
- LaTeX format, citation style, or compile checks (`latex-paper-en`)

## Load order

Load only the files for the current section. Do not load every TSV by default.

1. `references/style-guide.md`
2. Exactly one file under `references/writing/` matching the section
3. Matching TSV rows for that section

Cite `core` rows, or a statistical opener with `paper_count >= 5`. Candidate rows stay in TSV until promotion.

Resume distillation with `scripts/next_pending.py`. Validate with `scripts/validate_knowledge.py`.
