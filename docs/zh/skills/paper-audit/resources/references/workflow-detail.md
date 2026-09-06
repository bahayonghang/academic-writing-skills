# 工作流程细节

补充的每一步细节`references/MODE_GUIDE.md`. `SKILL.md`
保留台阶骨架；实际运行模式时读取此文件。

## 工作区覆盖保护（深入审查第 1 阶段）

如果目标审阅工作区已存在，请在替换前停下来询问
它。使用`prepare_review_workspace.py --overwrite`只有在用户确认后
现有的工件可以被丢弃；对于一体化
`audit.py --mode deep-review`路径、使用`--overwrite-workspace`相同之后
确认。

## 不落盘审查路径（交付级别 `T3`）

`SKILL.md` 定义了三个交付级别。本节覆盖 `T3`，即任何内容都不得写入磁盘。

`quick-audit`、`gate`、`re-audit`、`polish` 的落盘行为于 2026-09-06 实测：在只放
论文文件的目录中逐个运行，对比运行前后的目录列表。每次运行都跑完并把报告打到
stdout，因此下表的"无"表示运行完成且未留下文件——不是没能启动。`deep-review`
一行未实测，来自阅读 `scripts/audit.py` 与 `scripts/prepare_review_workspace.py`：

| 模式 | 落盘 | `T3` |
|---|---|---|
| `quick-audit` | 无 | 可用 |
| `gate` | 无 | 可用 |
| `re-audit` | `audit.py` 无落盘；`diff_review_issues.py` 可能在当前 bundle 旁写出 `revision_trajectory.md` | `T1` 直接可用；`T2`/`T3` 需加 `--no-trajectory` |
| `polish` | 论文文件旁的 `.polish-state/` | 不可用 |
| `deep-review` | 审查工作区 | 不可用 |

只要论文位于仓库内，`polish` 就同样不满足交付级别 `T2`：它写在论文旁边，
而不是写在当前工作目录。

在 `T3` 下，运行 `quick-audit` 或 `gate`，从 stdout 读取报告。不要把 stdout
重定向到文件，也不要传 `--output` / `-o`——该标志在所有模式下都会写出报告
文件，不只是在上表标为落盘的模式里。

运行前在环境中设置 `PYTHONDONTWRITEBYTECODE=1`。上表只统计报告与工作区文件。
`audit.py` 以不带 `-B` 的子进程启动每个检查脚本，而父进程的 `-B` 不会传递下去，
因此不设该变量时 Python 会把 `__pycache__/` 写进本技能自己的 `scripts/` 目录
——这是写入本仓库（`T2` 禁止），也是发生了写入（`T3` 禁止）。

`deep-review` 无法降级到 `T3`——改为提供 `quick-audit` 或 `gate`，并说明损失
了什么：没有委员会多视角评审，没有章节与横切通道，没有合并去重与根因归并，
没有引文校验。

逐项点名未能运行的脚本。两组必须分开——混在一起会让读者以为审查证据缺失，
而实际上缺的只是一个输出文件。

缺席会导致审查证据缺失的脚本——逐项标记 `missing evidence`：

- `prepare_review_workspace.py` —— 章节索引与论文摘要
- `build_claim_map.py` —— 主张提取与候选主张
- `consolidate_review_findings.py` —— 去重与根因归并
- `verify_quotes.py` —— 对照原文的引文校验

缺席只导致写出的报告不存在的渲染器，而这正是 `T3` 的设计意图——报告为"未产出"，
不标 `missing evidence`：

- `render_deep_review_report.py` —— Markdown 报告渲染
- `render_html_report.py` —— HTML 报告渲染

不得把其中任何一项描述为已用其他方式完成，也不得代它们标注 `[Script]`。
`quick-audit` 与 `gate` 在 `T3` 下确实运行的检查器仍然产出真实的 `[Script]`
发现；只有上面第一组会丢失证据的脚本属于 `missing evidence`。

## 整合命令序列（深入审查第 4/5 阶段）

```bash
uv run python -B "$SKILL_DIR/scripts/consolidate_review_findings.py" <review_dir>
uv run python -B "$SKILL_DIR/scripts/verify_quotes.py" <review_dir> --write-back
uv run python -B "$SKILL_DIR/scripts/render_deep_review_report.py" <review_dir> --lang $LANG
uv run python -B "$SKILL_DIR/scripts/render_html_report.py" <review_dir> --lang $LANG
```

请注意`--lang $LANG`两个渲染器上的标志 - 传递锁定的报告
语言，以便 Markdown 和 HTML 双胞胎呈现一致。

## 同行评审报告风格

当用户明确要求提供期刊评论散文时，设置
`--report-style peer-review`. `review_report.md`仍然是主要的
工作区根目录中的工件；`peer_review_report.md`生成为
下的一个同伴`artifacts/summary/`对于那种风格。

## 修改建议（可选的合并后步骤）

整合后，深度审查工作流程可以选择调用
`agents/revision_suggestion_agent.md`生产
`artifacts/data/revision_suggestions.json`与具体的原始/建议
文本对和附加操作。当文件存在时，
`revision_suggestions.md`它的 HTML 孪生会自动拾取它；什么时候
如果不存在，两者都会退回到优先级/部分路线图框架。

## 登机口出示顺序

使用以下命令运行 **EIC 筛选**（阶段 0.5）`agents/editor_in_chief_agent.md`
第一的;报告通过/失败；当前判决 -> EIC -> 阻止者 -> 咨询。一个
直接拒稿判决是一个障碍。仅关键`PRESUBMISSION`发现
挡住大门。

## 重新审核状态标签

呈现根本原因感知状态标签：`FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

## 波兰安全停留

如果审计预检查报告阻止程序，请停止并报告它们。只能继续
如果预检查是安全的，则进行抛光。
