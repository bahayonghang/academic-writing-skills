# 工作流

`paper-audit` 现在分成两层：

- 面向 `quick-audit`、`gate`、`polish` precheck 的脚本优先审查
- 面向 `deep-review` 的审稿人风格深审

最常见的误解是把 `audit.py --mode deep-review` 当成完整深审。它实际上只是 Phase 0 自动审查。

## 完整 Deep Review 流程

### Phase 1：准备 workspace

```bash
uv run python academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py paper.tex --output-dir ./review_results
```

产物包括：

- `full_text.md`
- `metadata.json`
- `section_index.json`
- `claim_map.json`
- `paper_summary.md`
- `sections/*.md`
- `comments/`
- `references/`（reviewer 最小参考集）
- `committee/`（委员会分角色记录与共识）

### Phase 2：运行 Phase 0 自动审查

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --scholar-eval
```

这一层提供：

- 脚本化检查结果
- 评分指示器
- venue / checklist 上下文
- 后续 reviewer lanes 的输入

但它不会直接生成最终的结构化问题清单。

### Phase 3：运行委员会预审（deep-review 默认）

默认顺序：

1. Editor 预筛
2. Theory 理论贡献审查
3. Literature 文献对话审查
4. Methodology 方法透明度审查
5. Logic 逻辑链条审查

可选聚焦：

- `--focus full`（默认）
- `--focus editor|theory|literature|methodology|logic`

这一阶段应把结果写入 `committee/*.md`。

### Phase 4：运行 section lanes

典型 section lanes：

- 引言 / 相关工作
- 方法
- 结果
- 讨论 / 结论
- 有 appendix 时再加 appendix

### Phase 5：运行 cross-cutting lanes

典型 cross-cutting lanes：

- claims vs evidence
- notation and numeric consistency
- evaluation fairness and reproducibility
- self-consistency of standards
- prior-art and novelty grounding

### Phase 6：合并与校验

```bash
uv run python academic-writing-skills/paper-audit/scripts/consolidate_review_findings.py ./review_results/paper-slug
uv run python academic-writing-skills/paper-audit/scripts/verify_quotes.py ./review_results/paper-slug --write-back
uv run python academic-writing-skills/paper-audit/scripts/render_deep_review_report.py ./review_results/paper-slug
```

这一步负责：

- 合并真重复问题
- 保留不同 paper-level consequence
- 校验 exact quote
- 生成最终 Markdown 报告
- 写出 `committee/consensus.md`（总分 + 最先改的 3 个问题）

## Quick-Audit 工作流

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit --venue neurips
```

适合：

- 投稿前快速筛查
- 决定是否值得做更深层审稿
- CI 风格脚本报告

## Gate 工作流

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.pdf --mode gate --venue ieee
```

适合：

- PASS / FAIL 判定
- blocker 清单
- IEEE 伪代码硬规则检查

## Re-Audit 工作流

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md
```

如果你同时有旧版和新版 `final_issues.json`：

```bash
uv run python academic-writing-skills/paper-audit/scripts/diff_review_issues.py old_final_issues.json new_final_issues.json
```

## Polish 工作流

```bash
uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish
```

这是润色前的安全检查，不是完整润色本身。若有 blocker，应先修复。
