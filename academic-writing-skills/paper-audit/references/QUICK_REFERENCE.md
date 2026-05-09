# Quick Reference

Read next:
- `references/MODE_GUIDE.md` — full per-mode workflow, phase steps, committee focus routing
- `references/PRESUBMISSION_GUIDE.md` — `PRESUBMISSION` mode-integration matrix

## Modes

| Mode | Purpose |
|---|---|
| `quick-audit` | fast readiness screen with `PRESUBMISSION` mechanical checks |
| `deep-review` | reviewer-style structured critique; Phase 0 includes `PRESUBMISSION` |
| `gate` | PASS/FAIL submission gate; Major/Minor mechanical findings are advisory |
| `re-audit` | compare current paper against earlier audit, including mechanical regressions |
| `polish` | precheck before a polishing workflow |

Legacy aliases:

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

## CLI

```bash
python audit.py <file> --mode quick-audit
python audit.py <file> --mode deep-review --scholar-eval --literature-search
python audit.py <file> --mode gate --format json
python audit.py <file> --mode re-audit --previous-report old_report.md
python pre_submission_check.py <file> --json
```

## PRESUBMISSION layer

Runs inside `quick-audit`, `gate`, `re-audit`, and `deep-review` Phase 0.

- Module name: `PRESUBMISSION`
- Source rule file: `references/PRE_SUBMISSION_RULES.md`
- Script: `scripts/pre_submission_check.py`
- Gate behavior: Critical blocks; Major/Minor stay advisory
- Deep-review behavior: full/editor can promote high-signal findings to
  `pre_submission_readiness`; focused reviews keep them in Phase 0 context
- PDF behavior: text-only checks; LaTeX/Typst source hygiene is explicitly skipped

## Deep-review scripts

```bash
python prepare_review_workspace.py paper.tex --output-dir ./review_results
python consolidate_review_findings.py ./review_results/paper-slug
python verify_quotes.py ./review_results/paper-slug --write-back
python render_deep_review_report.py ./review_results/paper-slug
python diff_review_issues.py old_final_issues.json new_final_issues.json
```

## Main outputs

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `peer_review_report.md`
- `revision_roadmap.md`
