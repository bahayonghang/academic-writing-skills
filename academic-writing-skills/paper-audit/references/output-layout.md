# Output Layout

Full workspace layout for `deep-review`. `SKILL.md` keeps the four-file
summary; this file is the authoritative artifact map.

## Workspace root (reader-facing, exactly four files)

- `review_report.md` — the primary deep-review report
- `revision_suggestions.md` — concrete fix recommendations for each
  Major/Moderate issue, including suggested rewrites (when applicable)
- `review_report.html` — HTML twin of the primary report
- `revision_suggestions.html` — HTML twin of the suggestions

## `artifacts/` (verification and tooling)

- `artifacts/summary/` — `paper_summary.md`, `overall_assessment.txt`,
  `peer_review_report.md`
- `artifacts/data/` — `final_issues.json`, `all_comments.json`,
  `claim_map.json`, `section_index.json`, `revision_suggestions.json`,
  `revision_trajectory.md`
- `artifacts/meta/` — `metadata.json`, `checkpoint.json`,
  `phase0_context.md`, `full_text.md`
- `artifacts/sections/`, `artifacts/comments/`, `artifacts/committee/`,
  `artifacts/references/`

## Report language

The report language is controlled by `--lang en|zh` (default: auto-detect
from `metadata.json`, fallback `en`). The language switch only affects
report headings, labels, and table headers — issue quotes, source tags
(`[Script]`, `[LLM]`), and structured field values stay in their original
form.
