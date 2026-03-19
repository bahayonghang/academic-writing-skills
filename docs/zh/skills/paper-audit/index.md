# `paper-audit`

面向 LaTeX、Typst 和 PDF 的深度审稿优先论文审查技能。

## 适用场景

- 投稿前快速筛查
- 模拟审稿人式深审
- 投稿门禁 PASS/FAIL 判断
- 基于旧报告的修订回归复检
- 润色前 precheck

## 不适用场景

- 一上来就做源文件改写
- 把编译修复当主任务
- 单独做文献综述写作
- 没有审查目标、只做纯 copy-editing

## 模式

| 模式 | 适用场景 | 脚本 |
| --- | --- | --- |
| `quick-audit` | 想先做一次快速就绪性检查 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit` |
| `deep-review` | 想拿到结构化问题清单和修订路线图 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review` |
| `gate` | 只看阻塞性问题与结论 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate` |
| `polish` | 想在润色前先做安全检查 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | 想对照旧报告做回归复检 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report.md` |

兼容别名：

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

## 如何选模式

- 只想快速看风险时用 `quick-audit`
- 想模拟审稿人并拿到路线图时用 `deep-review`
- 只关心 blocker 时用 `gate`
- 已有旧报告、要看修订效果时用 `re-audit`
- 想润色前先做安全检查时用 `polish`

## Deep-review 概览

1. 用 `prepare_review_workspace.py` 准备 workspace
2. 用 `audit.py --mode deep-review` 生成 Phase 0 自动审查
3. 派发 section lanes 和 cross-cutting lanes
4. 合并评论 JSON
5. 校验 quote
6. 生成 `review_report.md`

## 主要产物

- `final_issues.json`
- `overall_assessment.txt`
- `review_report.md`
- `revision_roadmap.md`

## 继续阅读

- [工作流](./resources/WORKFLOW.md)
- [模式说明](./resources/MODES.md)
- [输出产物](./resources/OUTPUTS.md)
- [命令与示例](./resources/CLI_AND_EXAMPLES.md)
- [常见问题](./resources/TROUBLESHOOTING.md)

## 推荐提示词

```text
对 paper.tex 做一次 quick-audit，告诉我什么会阻止投稿。
```

```text
像顶会审稿人一样 deep-review 这篇论文，并给我修订路线图。
```

```text
对这篇 IEEE 论文做 gate 检查，把硬阻塞和伪代码建议项分开。
```

```text
基于旧报告对这篇修订稿做 re-audit。
```

## 重要说明

- `audit.py --mode deep-review` 只是 Phase 0，不是完整深审。
- deep-review 的主产物是结构化问题清单，而不是分数本身。
- 能用源文件时优先用源文件；PDF 虽可用，但对公式和符号密集论文更弱。
