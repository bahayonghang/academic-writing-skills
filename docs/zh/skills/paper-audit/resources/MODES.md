# 模式说明

## `quick-audit`

适合：

- 想快速看投稿就绪性
- 想运行投稿前最后几天的 `PRESUBMISSION` 机械层
- 想拿到 checklist、severity、score 指示器
- 暂时不做完整审稿流程

主要产物：

- 脚本化审查报告
- `PRESUBMISSION` 发现：em dash、AI-tone、摘要结果缺口、source hygiene、caption finding
- checklist
- score summary

## `deep-review`

适合：

- 想做审稿人风格深审
- 关心 claim 准确性、方法有效性、比较公平性、跨章节一致性
- 想要修订路线图，而不是只有分数
- 想用委员会视角做预审（`Editor -> Theory -> Literature -> Methodology -> Logic`）

主要产物：

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `revision_roadmap.md`
- `committee/consensus.md`

单维度聚焦命令：

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus methodology
```

注意：

`audit.py --mode deep-review` 只是 Phase 0 自动审查，不等于完整 deep review。

Phase 0 会包含 `PRESUBMISSION` 层。full/editor focus 可以把高信号机械问题提升为
`pre_submission_readiness`；methodology、theory、literature、logic 聚焦深审不会让这些机械问题进入最终 focused issue bundle。

## `gate`

适合：

- 只要 PASS / FAIL
- 只看 blocker
- 用在投稿门禁或 CI

`PRESUBMISSION` 的 Major/Minor 在 `gate` 中只是 advisory。只有 Critical
发现或 checklist 失败会导致 FAIL。

## `re-audit`

适合：

- 已经有旧报告
- 想知道哪些问题修掉了，哪些还在
- 想做修订回归检查

## `polish`

适合：

- 想在润色前先确认有没有逻辑或结构 blocker

## 兼容别名

当前仍接受：

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

新文档和新命令一律使用 canonical mode 名称。

“pre-submission review / 投稿前三天检查”仍路由到 `quick-audit` 或 `gate`，
不要新增公开的 pre-submission 模式。
