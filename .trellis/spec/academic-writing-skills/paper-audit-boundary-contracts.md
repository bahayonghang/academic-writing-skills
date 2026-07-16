# Paper-Audit Boundary Contracts

## 1. Scope / Trigger

Read this spec before changing `consolidate_review_findings.py`, ScholarEval
module routing, or the `audit.py -> literature_compare.py` bibliography data
flow. These boundaries turn heterogeneous checker/LLM payloads into gate and
score inputs; silent fallback can otherwise create a false green result.

## 2. Signatures

```python
sanitize_issue(issue: dict) -> dict

MODULE_DIMENSION_MAP: dict[str, str]
evaluate_from_audit(
    audit_issues: list[dict],
    literature_grounding_score: float | None = None,
) -> dict[str, float | None]

compare_with_literature(
    paper_content: str,
    paper_citations: list[str],
    literature_results: list,
    bib_content: str = "",
) -> LiteratureComparisonResult

_load_bibliography_content(path: Path, content: str, fmt: str) -> str
```

## 3. Contracts

- Severity input is trimmed and case-insensitive. `critical` becomes
  `major + gate_blocker=true` even when the payload explicitly sets the blocker
  false; `observation` becomes `minor`; unknown values fall back to `moderate`.
- `description` and `location` are compatibility aliases for empty
  `explanation` and `source_section`. Never copy `location` into `quote`.
- Every checker module in `MODULE_DIMENSION_MAP` routes to exactly one score
  dimension. `EXPERIMENT` and `PSEUDOCODE` own script-side reproducibility;
  the former `LOGIC` message-text heuristic must not return.
- External bibliography content is optional. LaTeX resolves
  `\bibliography{}` and `\addbibresource{}`; Typst resolves `.bib` arguments to
  `bibliography()`. Missing or unreadable files degrade to an empty string.
- `compare_with_literature(..., bib_content="")` preserves the legacy
  `\bibitem` behavior. BibTeX parsing accepts quoted and balanced-braced title
  values and must not treat `booktitle` as `title`.
- Bibliography loading and comparison run only when literature search returned
  usable results. Empty search results leave `literature_grounding` unscored so
  weighted scoring renormalizes over available dimensions.

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| CRITICAL plus `gate_blocker=false` | Normalize to `major`, force blocker true |
| Unknown severity | Fall back to `moderate` |
| `location` without `quote` | Preserve location as `source_section`; quote stays empty |
| Unknown audit module | Ignore for script score; mapping guard test signals new modules |
| Missing `.bib` path | Skip silently and continue with legacy paper content |
| Nested BibTeX title braces | Return normalized title text |
| Empty literature result set | Do not call comparison or assign a grounding score |

## 5. Good / Base / Bad Cases

- Good: `EXPERIMENT/Critical` lowers `reproducibility_partial`, and a referenced
  `.bib` title matches a search result with positive coverage.
- Base: a paper with only `\bibitem` entries behaves identically when
  `bib_content` is omitted or empty.
- Bad: infer reproducibility from `LOGIC` messages containing the word
  "method", parse `booktitle` as a citation title, or score an API outage as
  poor literature grounding.

## 6. Tests Required

- `test_paper_audit_deep_review.py`: CRITICAL variants, explicit false blocker,
  aliases, observation mapping, and comments-directory end-to-end sorting.
- `test_paper_audit_topology_docs.py`: canonical three-level schema and agent
  template severity literals.
- `test_literature_search.py`: exact module-map guard, experiment signal,
  BibTeX title parser, legacy empty-bib behavior, `.tex/.typ` bibliography
  loading, real `run_audit` wiring, empty-results renormalization, and Typst
  metadata import-path guard.
- Run `uv run --extra dev python -m pytest tests/skills/paper_audit -q` and
  `tests/contracts` before `just ci`.

## 7. Wrong vs Correct

### Wrong

```python
severity = issue.get("severity", "moderate").lower()
reproducibility = [i for i in issues if i["module"] == "LOGIC" and "method" in i["message"]]
compare_with_literature(content, keys, results)  # external .bib titles are lost
```

### Correct

```python
severity_raw = str(issue.get("severity", "moderate")).strip().lower()
severity = SEVERITY_ALIASES.get(severity_raw, severity_raw)
dimension = MODULE_DIMENSION_MAP.get(str(issue.get("module", "")).upper())
compare_with_literature(content, keys, results, bib_content=bib_content)
```
