# Troubleshooting

## Operational Errors

| Problem                                                | Solution                                                                                                                                             |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| No file path provided                                  | Ask user for a valid `.tex`, `.typ`, or `.pdf` file                                                                                                  |
| Script execution fails                                 | Report the command, exit code, and stderr output                                                                                                     |
| Missing sibling skill scripts                          | Check that `latex-paper-en/scripts/`, `latex-thesis-zh/scripts/`, or `typst-paper/scripts/` exist                                                    |
| PDF checks limited                                     | PDF mode skips format/bib/figures checks; only visual and content analysis available                                                                 |
| `--venue` not recognized                               | Use one of: `neurips`, `iclr`, `icml`, `ieee`, `acm`, `thesis-zh`                                                                                    |
| ScholarEval LLM dimensions show N/A                    | Run with `--scholar-eval`, then provide LLM scores via `--llm-json`                                                                                  |
| Re-audit missing previous report                       | Provide `--previous-report PATH` pointing to the prior audit output                                                                                  |
| Literature search returns no results                   | Check API keys; Semantic Scholar works without key but slower; arXiv always available                                                                |
| `TAVILY_API_KEY` not set                               | Set env var or pass `--tavily-key`; Tavily is optional — S2 + arXiv work without it                                                                  |
| Semantic Scholar rate limited                          | Set `S2_API_KEY` for higher limits; the client has built-in exponential backoff                                                                      |
| Literature Grounding shows N/A                         | Run with `--literature-search` to enable automated literature verification                                                                           |
| Scoring model (`--regression`) gives unexpected scores | Check `scripts/models/scoring_model.json`; default coefficients approximate weighted average                                                         |
| "Cannot find `final_issues.json` at workspace root"    | The artifact moved to `artifacts/data/final_issues.json` under the new layout; re-run `--overwrite-workspace` on legacy v5.1 workspaces              |
| "Cannot find `revision_roadmap.md`"                    | Renamed to `revision_suggestions.md` and kept at the workspace root                                                                                  |
| HTML report not generated                              | `Jinja2` must be installed (`uv sync --extra dev`); the audit print suppresses HTML failures so check stderr                                         |
| Chinese report shows English headings                  | Pass `--lang zh` explicitly to `audit.py` / `render_html_report.py`; auto-detect only kicks in when `metadata.json` already records `language: "zh"` |

## Review Quality Failure Paths

These failures surface during or after `deep-review` and `re-audit` runs. Each
ID is stable; tests and downstream automation may reference them.

### F1 — Severe reviewer divergence

**Signal**: score divergence > 2.0 across lanes for the same issue category, OR
one lane reports CRITICAL while another reports MINOR for the same finding.

**Diagnosis steps**:

1. Open `committee/consensus.md` and locate the `[SPLIT]` items
2. Cross-check evidence quotes per lane against the paper text
3. Verify lane focus alignment in `references/REVIEW_LANE_GUIDE.md`

**Handling**: Apply Arbitration Priority 1-3 from
`references/editorial_decision_standards.md`. Evidence > Expertise > Conservative
bias. Record arbitration rationale in `overall_assessment.txt`.

**Files involved**: `committee/consensus.md`, `editorial_decision_standards.md`,
`synthesis_agent.md`.

### F2 — Lightweight reviewer outputs empty JSON or missing fields

**Signal**: one of `claims_evidence_reviewer`, `notation_consistency_reviewer`,
`self_consistency_reviewer`, `evaluation_fairness_reviewer`, or
`section_reviewer` returns `[]` or omits required fields from `ISSUE_SCHEMA.md`.

**Diagnosis steps**:

1. Check `references/SUBAGENT_TEMPLATES.md` for the lane-specific block
2. Inspect the paper section the lane was assigned — empty is valid only when
   the section is trivially clean
3. Re-dispatch the lane with the canonical template

**Handling**: If empty after re-dispatch, record `[Script]` annotation
"lane reviewed, no issues found" in the synthesis output. Do not synthesize
issues.

**Files involved**: `SUBAGENT_TEMPLATES.md`, `ISSUE_SCHEMA.md`, the empty lane
output file.

### F3 — Quote verification failures cluster

**Signal**: `verify_quotes.py` flags more than 20% of issue quotes as
`quote_verified=false`.

**Diagnosis steps**:

1. Inspect failed quotes against the source `.tex` / `.typ` / extracted PDF
2. Check for LaTeX macro expansion mismatches (verbatim vs rendered)
3. Confirm the paper was not modified between lane dispatch and verification

**Handling**: Drop unverified findings or downgrade them to MINOR with a
`[Script]` warning. Surface the failure count in `overall_assessment.txt`.

**Files involved**: `scripts/verify_quotes.py`, `final_issues.json`.

### F4 — Phase 3A/3B checkpoint mid-run failure

**Signal**: `prepare_review_workspace.py` succeeded but a lane dispatch crashes
midway, leaving `review_results/` partially populated.

**Diagnosis steps**:

1. Inspect `review_results/manifest.json` (if present) for the last completed
   lane
2. Check `committee/` and lane subdirectories for partial outputs

**Handling**: Re-run the failed lane only; do not restart the full pipeline.
The synthesis step is idempotent over completed lane outputs.

**Files involved**: `scripts/prepare_review_workspace.py`,
`scripts/consolidate_review_findings.py`.

### F5 — PDF mode misreports LaTeX-specific issues

**Signal**: `--mode deep-review` with a `.pdf` input produces findings that
reference LaTeX macros, `.bib` entries, or compilation warnings.

**Diagnosis steps**:

1. Confirm `audit.py` correctly detected PDF mode (check log header)
2. Verify the format-specific lane gate disabled bibliography and compile
   lanes

**Handling**: Discard LaTeX-specific findings from the PDF run. Ask the user
for the source `.tex` if those checks are needed.

**Files involved**: `scripts/audit.py`, lane gate logic.

### F6 — Re-audit root_cause_key drift

**Signal**: `--previous-report PATH` is provided but the comparator reports
zero overlapping issues, even though the paper appears partially revised.

**Diagnosis steps**:

1. Open the previous report and confirm `root_cause_key` fields exist on each
   issue
2. Check for schema version mismatch in `ISSUE_SCHEMA.md`
3. If the old report predates `root_cause_key`, re-derive keys via the
   migration helper

**Handling**: Re-run `consolidate_review_findings.py` against the old report
to regenerate stable keys, then re-dispatch the comparator.

**Files involved**: `ISSUE_SCHEMA.md`, `scripts/consolidate_review_findings.py`.

### F7 — Score divergence > 2.0 but issue list converges

**Signal**: lanes agree on the issue list but their per-dimension scores
diverge sharply.

**Diagnosis steps**:

1. Inspect each lane's calibration against `references/quality_rubrics.md`
   tier definitions
2. Check whether one lane uses ScholarEval and another uses default scoring

**Handling**: Normalize per `quality_rubrics.md` weighted formula. Surface the
calibration delta in `overall_assessment.txt`.

**Files involved**: `quality_rubrics.md`, `scripts/scoring_model.py`.

### F8 — Desk-reject score conflicts with deep-review verdict

**Signal**: `editor_in_chief_agent` returns `Desk Reject` but `synthesis_agent`
produces only MINOR findings, or vice versa.

**Diagnosis steps**:

1. Re-read both agents' role boundaries — EIC is a 90-second pitch screener,
   not a deep-review reviewer
2. Confirm the EIC ran on metadata + opening sections only
3. Cross-check fatal-flaw signals (Section 3 of `editor_in_chief_agent.md`)
   against committee findings

**Handling**: EIC verdict applies only in `gate` mode. In `deep-review`,
surface the EIC concern as a `pitch_quality` annotation but defer the verdict
to synthesis.

**Files involved**: `editor_in_chief_agent.md`, `synthesis_agent.md`,
`MODE_GUIDE.md`.
