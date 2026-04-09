# Outputs

`paper-audit` now produces different artifacts depending on mode.

## Quick-Audit / Gate Outputs

For `quick-audit`, `gate`, and `polish` precheck, the main product is a rendered report.

Typical contents:

- severity-rated issues
- checklist results
- score summary
- gate verdict, if applicable

## Deep-Review Outputs

These are the main deep-review artifacts.

### `final_issues.json`

The canonical structured issue bundle.

Typical fields:

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `confidence`
- `source_kind`
- `source_section`
- `related_sections`
- `root_cause_key`
- `review_lane`
- `gate_blocker`
- `quote_verified`

This file is the source of truth for:

- final reviewer findings
- re-audit comparisons
- downstream visualizers or external tooling

### `overall_assessment.txt`

A short high-level judgment of the paper.

This should:

- say whether the contribution is promising
- name the 2-3 biggest risks
- tell the reader whether the issues feel fixable

### `review_report.md`

The human-readable final deep-review report.

Expected sections:

- overall assessment
- major / moderate / minor issues
- Phase 0 automated findings
- score summary
- revision roadmap

### `peer_review_report.md`

A reviewer-facing journal / SCI style report derived from the deep-review artifacts.

Expected sections:

- Summary
- Major Issues
- Minor Issues
- Recommendation

Use this artifact when you want something closer to what a real journal reviewer would submit, while keeping `review_report.md` as the richer evidence bundle.

### `revision_roadmap.md`

The prioritized action list for the authors.

Typical priorities:

- Priority 1: paper-level validity threats
- Priority 2: significant but localized problems
- Priority 3: optional improvements

### `committee/consensus.md`

Committee-level synthesis generated for deep-review.

Typical contents:

- overall score (`1-10`)
- editor verdict
- score formula trace
- top 3 issues to fix first

Scoring policy:

- base `9.0`
- subtract `1.5 * major + 0.7 * moderate + 0.2 * minor`
- floor at `1.0`
- if editor verdict is `Desk Reject`, score is capped at `4.0`

## Workspace Artifacts

These support deep review but are not the final product.

### `section_index.json`

Maps logical sections to line ranges and workspace section files.

### `claim_map.json`

Records headline claims and closure targets. Used by cross-cutting review lanes.

### `paper_summary.md`

A structured summary of the paper for reviewer lanes to share context.

### `all_comments.json`

The pre-consolidation union of all section-lane and cross-cutting-lane findings.

### `committee/*.md`

Reviewer-role notes from committee passes, when generated:

- `editor.md`
- `theory.md`
- `literature.md`
- `methodology.md`
- `logic.md`

## Script vs Reviewer Provenance

`source_kind` tells you where a finding came from:

- `script`
- `llm`

Keep these separate. A score summary may combine both, but the issue bundle should preserve provenance.
