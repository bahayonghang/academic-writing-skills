# 快速参考

接下来阅读：

- `references/MODE_GUIDE.md`— 完整的每种模式工作流程、阶段步骤、委员会焦点路由
- `references/PRESUBMISSION_GUIDE.md` — `PRESUBMISSION`模式积分矩阵

## 模式

|模式|目的|
| ------------- | ----------------------------------------------------------------------------- |
| `quick-audit` |快速准备屏幕`PRESUBMISSION`机械检查|
| `deep-review` |审稿人式的结构化批评；阶段 0 包括`PRESUBMISSION`          |
| `gate`        |通过/失败提交门；主要/次要机械结果仅供参考|
| `re-audit`    |将当前论文与早期审核进行比较，包括机械回归|
| `polish`      |抛光工作流程之前的预检查|

旧别名：

- `self-check` -> `quick-audit`
- `review` -> `deep-review`

## 命令行界面

```bash
python audit.py <file> --mode quick-audit
python audit.py <file> --mode deep-review --scholar-eval --literature-search
python audit.py <file> --mode gate --format json
python audit.py <file> --mode re-audit --previous-report old_report.md
python pre_submission_check.py <file> --json
```

## 预提交层

在里面运行`quick-audit`, `gate`, `re-audit`， 和`deep-review`阶段 0。

- 模块名称：`PRESUBMISSION`
- 源规则文件：`references/PRE_SUBMISSION_RULES.md`
- 脚本：`scripts/pre_submission_check.py`
- 门行为：关键块；主要/次要居留咨询
- 深度评审行为：全文/编辑可以将高信号结果推广到
  `pre_submission_readiness`;重点审查使它们处于第 0 阶段的背景下
- PDF 行为：纯文本检查；明确跳过 LaTeX/Typst 源卫生

## 深入审查脚本

```bash
python prepare_review_workspace.py paper.tex --output-dir ./review_results
python consolidate_review_findings.py ./review_results/paper-slug
python verify_quotes.py ./review_results/paper-slug --write-back
python render_deep_review_report.py ./review_results/paper-slug
python diff_review_issues.py old_final_issues.json new_final_issues.json
```

## 主要产出

- `review_report.md`
- `revision_suggestions.md`
- `review_report.html`
- `revision_suggestions.html`
- `artifacts/data/final_issues.json`
- `artifacts/summary/overall_assessment.txt`
- `artifacts/summary/peer_review_report.md`

## 常见的错误分类

期间反复出现的LLM错误的简短列表`paper-audit`运行。当有疑问时，
查阅引用的参考文献并决定采取更保守的做法
分类。

- **将单个em-dash提升为门禁者。** PRE_SUBMISSION_RULES G1
仅在阈值以上时将 em-dash 过度使用视为主要。单个破折号
并不是一个阻碍性的发现。看`PRE_SUBMISSION_RULES.md`G1。
- **重新查找横切审查通道内的路段问题。** 如果发现
已经住在`section_methods`或者`section_results`，不应该是
重新报道者`claims_vs_evidence`或者`notation_and_numeric_consistency`
除非横切视图添加了新的维度。看
  `CONSOLIDATION_RULES.md`.
- **将 ScholarEval N/A 视为主要问题。** N/A 表示维度为
没有锻炼（通常是因为`--literature-search`没有要求），没有
这篇论文失败了。看`SCHOLAR_EVAL_GUIDE.md`.
- **内部发出问题严重性`quick-audit`.** `quick-audit`产生一个
准备情况屏幕，而不是审阅者级别的结论。严重性分配位于
  `deep-review`合成。看`MODE_GUIDE.md`.
- **默默地合并单例关键发现。**综合必须保留
除非仲裁明确降级，否则单例关键发现
优先级 1（证据原则）。看`synthesis_agent.md`禁止
运营。
- **过度合并`review_lane`边界。** 审查通道来源必须
在整合中生存下来。不同审查通道的调查结果可以通过以下方式链接
  `root_cause_key`而不失去他们的审查通道属性。看
  `CONSOLIDATION_RULES.md`和`ISSUE_SCHEMA.md`.
- **将 PDF 模式视为降级的 LaTeX 模式。** PDF 运行时有意跳过
仅源检查（参考书目卫生、标签解析、编译
警告）。从 PDF 输入引用 LaTeX 宏的结果是
故障排除 F5。看`TROUBLESHOOTING.md`.
- **出租EIC`Desk Reject`推翻委员会的共识
  `deep-review`.** EIC 是一个 90 秒的音调筛选器；其判决具有约束力
仅在`gate`模式。看`editor_in_chief_agent.md`和故障排除 F8。
- **夸大的问题列出了过去的审查通道输出限制。**每个横切审查通道
最大问题预算为`REVIEW_LANE_GUIDE.md`。重复出现的模式必须
折叠成具有多个示例位置的一个问题而不是发出
每次出现一个问题。
