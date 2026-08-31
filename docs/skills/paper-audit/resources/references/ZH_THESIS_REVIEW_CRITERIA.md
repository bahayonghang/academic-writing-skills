# Chinese Dissertation Review Criteria

Scope: dissertations with `--venue thesis-zh` or `lang == "zh"`. Do not use this document for English conference or journal papers.

Method-chapter narration quality is outside the automatic audit chain. Use `latex-thesis-zh --method-narrative --section`, matching `SKILL.md`.

This document and the matching agent **do not** emit a degree grade (excellent / good / fair / poor) or a “permission to defend” verdict. `paper-audit` already has `gate` PASS/FAIL and ScholarEval scores; a third conclusion surface would conflict.

Chinese pseudocode is not in the table below. C1 classified `check_pseudocode.py` as language-dependent and suppressed it for zh. Localization is out of scope.

## Three sets (do not mix)

| Set | Count | Source | Role |
|---|---|---|---|
| Runtime base scoring dimensions | 8 | `scripts/scoring_model.py`: `soundness` / `clarity` / `presentation` / `novelty` / `significance` / `reproducibility` / `ethics` / `literature_grounding` | Weighted scoring |
| Derived overall | 1 | `overall_base` (from the 8 dimensions) | Not an independent review dimension. The "9 base dimensions" comment above `FEATURE_NAMES` is inaccurate |
| Chinese review indicator rows | 15 | Table below | Document-layer indicators mapped onto base dimensions; they do not change weights |

Weights come from `quality_rubrics.md`. This file does not copy rubric bands or create a parallel scoring system.

## 15 Chinese review indicator rows

| # | Indicator | Base dimension | Band | Carrier |
|---|---|---|---|---|
| 1 | Topic significance and frontier | `significance` (13%) | `[LLM]` | reviewer |
| 2 | Literature review quality (critique, not a list) | `literature_grounding` (12%) | `[Script]` + `[LLM]` | `analyze_literature.py` (module `LITERATURE`) + reviewer |
| 3 | Theoretical foundation | `soundness` (18%) | `[LLM]` | reviewer |
| 4 | Research method and technical route | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_logic.py` / `analyze_experiment.py` + reviewer |
| 5 | Workload and difficulty | `significance` (13%) | `[LLM]` | reviewer; do not proxy by length, figure count, equation count, or bibliography size |
| 6 | Novelty (master / doctoral bands) | `novelty` (13%) | `[LLM]` | reviewer |
| 7 | Reliability of conclusions | `soundness` (18%) | `[Script]` + `[LLM]` | `analyze_conclusion.py` (module `CONCLUSION`) + reviewer |
| 8 | Chapter completeness | `presentation` (8%) | `[Script]` | `check_spec.py` (module `SPEC`) |
| 9 | Abstract and keyword conventions | `clarity` (13%) | `[Script]` | `analyze_abstract.py` (module `ABSTRACT`) |
| 10 | Three-line table conventions | `presentation` (8%) | `[Script]` | `check_tables.py` (module `TABLES`) |
| 11 | Figure quality and numbering | `presentation` (8%) | `[Script]` | `check_figures.py` (module `FIGURES`, language-neutral reuse) |
| 12 | GB/T 7714 references | `presentation` (8%) | `[Script]` | `verify_bib.py --standard gb7714` (module `BIB`, `.tex` only) |
| 13 | Language and expression | `clarity` (13%) | `[Script]` | `check_style_zh.py` (via the `sentences` key, module `SENTENCES`) |
| 14 | Academic integrity and originality | `ethics` (5%) | `[LLM]` | reviewer; no plagiarism scan |
| 15 | Blind-review identifying information | `ethics` (5%) | `[Script]` | `blind_review.py --check` (module `BLIND`) |

Reproducibility (`reproducibility` 8%) stays on the existing pipeline. No extra Chinese indicator row.

## Band discipline

Rows 1, 3, 5, 6, and 14 are `[LLM]`. Do not add regex or word-list checkers for them. Workload and novelty must not be proxied by length, figure count, equation count, or bibliography size.

Each `[Script]` carrier maps to exactly one module.

## Master / doctoral difference (reviewer judgment)

- Master: novelty may be application, integration, or engineering improvement, but the increment versus the closest prior work must be explicit.
- Doctoral: novelty must be a standalone knowledge contribution (method, theory, or system) that the conclusion can verify.
- Workload is about problem difficulty, implementation completeness, and evidence strength, not page count.
- Degree level comes from the school template / `latex-thesis-zh --degree`. `paper-audit` does not copy that CLI axis.

## Examiner reading path

Journal reviewers often start from contribution and experiments (see `REVIEWER_PSYCHOLOGY.md`). Dissertation examiners should first check whether structure and workload support a defense, then whether novelty meets the degree band, then expression and formal rules.

## Boundary versus existing references

| Existing file | Role | Relation |
|---|---|---|
| `DEEP_REVIEW_CRITERIA.md` | 16 issue classes | Do not add classes |
| `REVIEW_CRITERIA.md` | Top-level score mapping | Do not change mapping |
| `quality_rubrics.md` | Band descriptions | Cite weights only |
| `CHECKLIST.md` | Mechanical checklist | Keep tick items there |
| `VENUE_RULES.md` | Venue hard constraints | Point page/word limits there |
| `REVIEWER_PSYCHOLOGY.md` | Reading path | This file adds the dissertation path |
