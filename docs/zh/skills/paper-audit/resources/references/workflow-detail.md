# 工作流程细节

补充的每一步细节`references/MODE_GUIDE.md`. `SKILL.md`
保留台阶骨架；实际运行模式时读取此文件。

## 工作区覆盖保护（深入审查第 1 阶段）

如果目标审阅工作区已存在，请在替换前停下来询问
它。使用`prepare_review_workspace.py --overwrite`只有在用户确认后
现有的工件可以被丢弃；对于一体化
`audit.py --mode deep-review`路径、使用`--overwrite-workspace`相同之后
确认。

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
