# 命令与示例

仓库内命令统一使用：

```bash
uv run python ...
```

## Quick-Audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit
```

适合回答：

- 什么会阻止投稿？
- 在做完整深审前，先该修什么？

## Deep-Review

最小 Phase 0 命令：

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
```

完整 deep-review 序列：

```bash
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex --output-dir ./review_results
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
uv run python academic-writing-skills/paper-audit/scripts/consolidate_review_findings.py ./review_results/paper-slug
uv run python academic-writing-skills/paper-audit/scripts/verify_quotes.py ./review_results/paper-slug --write-back
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py ./review_results/paper-slug
```

## IEEE Gate

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee
```

适合：

- PASS / FAIL
- blocker 清单
- 伪代码硬规则与建议项分离

## Re-Audit

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md
```

若你有旧版和新版 issue bundle：

```bash
uv run python academic-writing-skills/paper-audit/scripts/diff_review_issues.py old_final_issues.json new_final_issues.json
```

## 只有 PDF 的情况

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode quick-audit
```

如果论文公式和符号很多，优先使用 `.tex` 或 `.typ`。

## 自然语言请求示例

```text
对 paper.tex 做一次 quick-audit，把 blocker 放在最前面。
```

```text
像严苛顶会审稿人一样 deep-review 这篇论文，重点看 claim 和 evidence 是否匹配。
```

```text
对这篇 IEEE 论文做 gate 检查，告诉我伪代码还有没有硬违规。
```

```text
基于旧报告对这篇修订稿做 re-audit。
```
