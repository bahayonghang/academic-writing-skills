# 同行评审主要视图示例

请求示例：

```text
Please review this manuscript as an SCI journal reviewer. I want Summary, Major Issues, Minor Issues, and Recommendation.
```

预期管道：

```bash
uv run python -B "$SKILL_DIR/scripts/prepare_review_workspace.py" paper.tex --output-dir ./review_results
uv run python -B "$SKILL_DIR/scripts/audit.py" paper.tex --mode deep-review --report-style peer-review
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" ./review_results/paper
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" ./review_results/paper --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" ./review_results/paper --style peer-review
```

预期的高层演讲：

- 审稿人的散文是**主要观点**。
- `peer_review_report.md`之前介绍过`review_report.md`.
- 内部字段如`review_lane`, `source_kind`， 或者`root_cause_key`留在工件内部，而不是出现在面向审稿人的散文摘要中。
- CLI 摘要仍然指向`final_issues.json`以及技术后续的修订路线图。
