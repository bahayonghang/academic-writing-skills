# Scripts Map

Full script roster under `scripts/`. `SKILL.md` keeps a compact summary;
this file is the authoritative map.

| Script                                   | Purpose                                                                                                                                                  |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/audit.py`                       | Phase 0 audit and mode entrypoint                                                                                                                        |
| `scripts/paths.py`                       | `WorkspaceLayout` — single source of truth for artifact paths                                                                                            |
| `scripts/i18n.py`                        | English/Chinese string dictionary for report rendering                                                                                                   |
| `scripts/pre_submission_check.py`        | deterministic `PRESUBMISSION` mechanical audit layer                                                                                                     |
| `scripts/prepare_review_workspace.py`    | create deep-review workspace                                                                                                                             |
| `scripts/build_claim_map.py`             | extract headline claims, closure targets, and additive `claim_candidates`                                                                                |
| `scripts/consolidate_review_findings.py` | deduplicate comment JSONs                                                                                                                                |
| `scripts/verify_quotes.py`               | verify exact quote presence                                                                                                                              |
| `scripts/render_deep_review_report.py`   | render final Markdown report                                                                                                                             |
| `scripts/render_html_report.py`          | render HTML twins of review_report and revision_suggestions                                                                                              |
| `scripts/diff_review_issues.py`          | compare old vs new issue bundles                                                                                                                         |
| `scripts/scholar_eval.py`                | nine-dimension ScholarEval scoring (`--scholar-eval`)                                                                                                    |
| `scripts/scoring_model.py`               | weighted-plus overall score for `--regression` (hand-tuned weights + interaction/penalty terms, not a trained regression) with weighted-average fallback |
| `scripts/literature_search.py`           | optional external literature search backend (`--literature-search`; Tavily via `--tavily-key` / Semantic Scholar via `--s2-key`, or env keys)            |
| `scripts/literature_compare.py`          | compare manuscript citations against external literature evidence                                                                                        |
