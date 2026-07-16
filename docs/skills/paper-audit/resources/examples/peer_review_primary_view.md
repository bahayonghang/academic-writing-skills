# Peer-Review Primary View Example

Example request:

```text
Please review this manuscript as an SCI journal reviewer. I want Summary, Major Issues, Minor Issues, and Recommendation.
```

Expected pipeline:

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" paper.tex --output-dir ./review_results
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode deep-review --report-style peer-review
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" ./review_results/paper
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" ./review_results/paper --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" ./review_results/paper --style peer-review
```

Expected top-level presentation:

- Reviewer prose is the **Primary View**.
- `peer_review_report.md` is introduced before `review_report.md`.
- Internal fields such as `review_lane`, `source_kind`, or `root_cause_key` stay inside artifacts instead of appearing in the reviewer-facing prose summary.
- The CLI summary still points to `final_issues.json` and the revision roadmap for technical follow-up.
