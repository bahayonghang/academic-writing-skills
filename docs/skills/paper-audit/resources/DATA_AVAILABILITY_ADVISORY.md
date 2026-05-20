# Data Availability Advisory

Use this advisory when a submission-readiness or deep-review pass needs to check whether central paper claims can be traced to source data, code, or stable external records. It is an audit aid, not a data-hosting workflow.

## What to Check

| Item | Question | Severity guidance |
|---|---|---|
| Central claim source data | Do the main conclusions have a data file, repository, accession, appendix table, or figure source data path? | Gate blocker only when venue policy requires it and the central evidence is missing. |
| Figure/table provenance | Can each central figure panel or table be mapped to raw or processed data? | Major when the mapping is absent for a central result; minor for auxiliary figures. |
| Stable identifier | Is there a DOI, accession, repository URL, or stable archive for external data/code? | Major if required by venue; otherwise advisory. |
| License and access | Are access restrictions, licenses, or request procedures stated? | Minor to moderate depending on reproducibility impact. |
| Code/analysis artifact | Are scripts, notebooks, or analysis settings named when they affect central claims? | Major for computational papers when absent. |

## Reporting Rules

- Do not claim data are unavailable unless the manuscript or supplied artifacts show that gap.
- If the user provides no artifact list, report `missing_evidence` rather than inventing repositories.
- Distinguish source data, processed data, figure source data, software outputs, and secondary data.
- For gate mode, fail only on explicit venue-required data availability gaps that affect central evidence.
