# Quick Reference

Read next:

- `references/MODE_GUIDE.md` — full per-mode workflow, phase steps, committee focus routing
- `references/PRESUBMISSION_GUIDE.md` — `PRESUBMISSION` mode-integration matrix

## Modes

| Mode          | Purpose                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| `quick-audit` | fast readiness screen with `PRESUBMISSION` mechanical checks                  |
| `deep-review` | reviewer-style structured critique; Phase 0 includes `PRESUBMISSION`          |
| `gate`        | PASS/FAIL submission gate; Major/Minor mechanical findings are advisory       |
| `re-audit`    | compare current paper against earlier audit, including mechanical regressions |
| `polish`      | precheck before a polishing workflow                                          |

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

- `review_report.md`
- `revision_suggestions.md`
- `review_report.html`
- `revision_suggestions.html`
- `artifacts/data/final_issues.json`
- `artifacts/summary/overall_assessment.txt`
- `artifacts/summary/peer_review_report.md`

## Common Misclassifications

A short list of recurring LLM errors during `paper-audit` runs. When in doubt,
consult the cited reference and resolve in favor of the more conservative
classification.

- **Promoting a single em-dash to a gate blocker.** PRE_SUBMISSION_RULES G1
  treats em-dash overuse as Major only above the threshold. A single em-dash
  is not a gate-blocking finding. See `PRE_SUBMISSION_RULES.md` G1.
- **Re-finding a section issue inside a cross-cutting lane.** If a finding
  already lives in `section_methods` or `section_results`, it should not be
  re-reported by `claims_vs_evidence` or `notation_and_numeric_consistency`
  unless the cross-cutting view adds a new dimension. See
  `CONSOLIDATION_RULES.md`.
- **Treating ScholarEval N/A as a Major issue.** N/A means the dimension was
  not exercised (often because `--literature-search` was not requested), not
  that the paper failed it. See `SCHOLAR_EVAL_GUIDE.md`.
- **Emitting issue severity inside `quick-audit`.** `quick-audit` produces a
  readiness screen, not a reviewer-grade verdict. Severity assignment lives in
  `deep-review` synthesis. See `MODE_GUIDE.md`.
- **Silently merging singleton CRITICAL findings.** Synthesis must preserve
  singleton CRITICAL findings unless explicitly downgraded by Arbitration
  Priority 1 (Evidence Principle). See `synthesis_agent.md` Forbidden
  Operations.
- **Over-merging across `review_lane` boundaries.** Lane provenance must
  survive consolidation. Findings from different lanes can be linked via
  `root_cause_key` without losing their lane attribution. See
  `CONSOLIDATION_RULES.md` and `ISSUE_SCHEMA.md`.
- **Treating PDF mode as a degraded LaTeX mode.** PDF runs intentionally skip
  source-only checks (bibliography hygiene, label resolution, compile
  warnings). Findings that reference LaTeX macros from a PDF input are
  TROUBLESHOOTING F5. See `TROUBLESHOOTING.md`.
- **Letting EIC `Desk Reject` override committee consensus in
  `deep-review`.** EIC is a 90-second pitch screener; its verdict is binding
  only in `gate` mode. See `editor_in_chief_agent.md` and TROUBLESHOOTING F8.
- **Inflating issue lists past lane output limits.** Each cross-cutting lane
  has a max-issues budget in `REVIEW_LANE_GUIDE.md`. Recurring patterns must
  collapse into one issue with multiple example locations rather than emit
  one issue per occurrence.
