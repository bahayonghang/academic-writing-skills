# `paper-audit`

面向 LaTeX、Typst 和 PDF 的深度审稿优先论文审查技能。它是 reviewer 和投稿门禁流程，不是源码编辑器。

## 适用场景

- 投稿前快速就绪性筛查。
- 最后一周机械检查：em dash、AI-tone、摘要结果缺口、citation/label/equation hygiene、段落形态弱信号。
- 模拟审稿人的 major / moderate / minor 深度批评。
- 按投稿 blocker 校准的 PASS/FAIL 门禁判断。
- 对照旧报告验证修订是否解决问题。
- 生成可追踪的 review workspace、claim map、quote check 和 revision trajectory。

## 不适用场景

- 一上来就直接修改 `.tex` 或 `.typ` 源码。
- 把编译修复当主任务。
- 没有审查目标的逐句润色。
- 单独代写文献综述。
- 投稿信生成或 claim 对齐；请用 `cover-letter`。

## 模式路由

| 模式 | 适用场景 | 主命令 |
| --- | --- | --- |
| `quick-audit` | 快速脚本化就绪性筛查 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode quick-audit` |
| `deep-review` | 需要审稿式问题清单、workspace 和修订路线图 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode deep-review --focus full` |
| `gate` | 只关心硬性投稿 blocker | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode gate --venue ieee` |
| `polish` | 润色前需要 precheck-only handoff；存在 depth-3 小节时同时提供源坐标窗口 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode polish` |
| `re-audit` | 有旧报告，需要做回归比较 | `uv run python academic-writing-skills/paper-audit/scripts/audit.py paper.tex --mode re-audit --previous-report report_v1.md` |

兼容别名：`self-check` -> `quick-audit`；`review` -> `deep-review`。

deep-review 会派发 5 个 committee agent 和 6 个以上 lane agent，随后交给
`synthesis_agent.md` 综合。`gate`、`re-audit` 和 consolidation 后的修订建议分别使用
对应的模式专属 agent。`agents/` 下的 specialized reviewer playbook 仅作参考，不会自动派发；
完整边界见[代理名册](./resources/references/agent-roster.md)。

## 最小输入

- `paper.tex`、`paper.typ` 或 `paper.pdf`。
- 可选 `--venue`、`--lang en|zh`、`--report-style deep-review|peer-review`。
- deep-review 可选 `--focus full|editor|theory|literature|methodology|logic`。
- `re-audit` 需要 `--previous-report`。
- 继续或渲染已有 workspace 时提供 `--review-dir`。

## 脚本入口

| 脚本 | 用途 |
| --- | --- |
| `audit.py` | quick-audit、deep-review、gate、polish、re-audit 的公开入口 |
| `prepare_review_workspace.py` | 准备 deep-review workspace |
| `build_claim_map.py` | 抽取 headline claims、closure targets 和 claim candidates |
| `check_citations.py` / `check_references.py` | 引用与参考文献 hygiene 检查 |
| `verify_quotes.py` | 校验报告 quote 是否来自源文本 |
| `render_deep_review_report.py` | 渲染 Markdown 深审报告 |
| `render_html_report.py` | 渲染双语 HTML 报告 |
| `render_revision_trajectory.py` | 生成 revision trajectory |
| `diff_review_issues.py` | 支持 re-audit 对比 |

## 输出产物

`deep-review` 的 workspace 根目录面向读者：

- `review_report.md` 与 `review_report.html`
- `revision_suggestions.md` 与 `revision_suggestions.html`

支撑产物位于 `artifacts/`：

- `artifacts/summary/paper_summary.md`、`overall_assessment.txt`、`peer_review_report.md`
- `artifacts/data/final_issues.json`、`all_comments.json`、`claim_map.json`、`section_index.json`、`revision_suggestions.json`、`revision_trajectory.md`
- `artifacts/meta/metadata.json`、`checkpoint.json`、`phase0_context.md`、`full_text.md`
- `artifacts/sections/`、`artifacts/comments/`、`artifacts/committee/`、`artifacts/references/`

报告语言由 `--lang en|zh` 控制。标题、标签和表头会切换语言；issue quote、source tag 和结构化字段值保持原文。

## 公开资源

### 参考资料

- [代理名册](./resources/references/agent-roster.md)
- [审核指南](./resources/references/AUDIT_GUIDE.md)
- [变更日志](./resources/references/CHANGELOG.md)
- [预提交清单](./resources/references/CHECKLIST.md)
- [声明-证据合同](./resources/references/CLAIM_EVIDENCE_CONTRACT.md)
- [合并规则](./resources/references/CONSOLIDATION_RULES.md)
- [数据可用性咨询](./resources/references/DATA_AVAILABILITY_ADVISORY.md)
- [深入审查标准](./resources/references/DEEP_REVIEW_CRITERIA.md)
- [编辑决策标准](./resources/references/editorial_decision_standards.md)
- [FORBIDDEN_TERMS.md](./resources/references/FORBIDDEN_TERMS.md)
- [问题架构](./resources/references/ISSUE_SCHEMA.md)
- [文学基础评分指南](./resources/references/LITERATURE_GROUNDING_GUIDE.md)
- [模式指南](./resources/references/MODE_GUIDE.md)
- [输出布局](./resources/references/output-layout.md)
- [超额声明防护（审核通道参考）](./resources/references/OVER_CLAIM_GUARD.md)
- [波兰语指南](./resources/references/POLISH_GUIDE.md)
- [提交前机械规则](./resources/references/PRE_SUBMISSION_RULES.md)
- [预提交模式集成](./resources/references/PRESUBMISSION_GUIDE.md)
- [定性研究标准参考](./resources/references/QUALITATIVE_STANDARDS.md)
- [论文审核质量准则](./resources/references/quality_rubrics.md)
- [快速参考](./resources/references/QUICK_REFERENCE.md)
- [审核标准](./resources/references/REVIEW_CRITERIA.md)
- [查看审查通道指南](./resources/references/REVIEW_LANE_GUIDE.md)
- [审稿心理学](./resources/references/REVIEWER_PSYCHOLOGY.md)
- [ScholarEval 9 维评分指南](./resources/references/SCHOLAR_EVAL_GUIDE.md)
- [评分系统](./resources/references/SCORING_SYSTEMS.md)
- [脚本地图](./resources/references/scripts-map.md)
- [审阅者通道模板](./resources/references/SUBAGENT_TEMPLATES.md)
- [故障排除](./resources/references/TROUBLESHOOTING.md)
- [期刊或会议特定规则](./resources/references/VENUE_RULES.md)
- [工作流程细节](./resources/references/workflow-detail.md)

### 模板

- [审计报告模板](./resources/templates/audit_report_template.md)
- [深度审查报告模板](./resources/templates/review_report_template.md)
- [修订路线图模板](./resources/templates/revision_suggestions_template.md)

### 示例

- [门模式输出示例](./resources/examples/gate_example.md)
- [同行评审主要视图示例](./resources/examples/peer_review_primary_view.md)
- [深入审查示例输出](./resources/examples/review_example.md)
- [自检示例输出](./resources/examples/self_check_example.md)

### Agent 契约

- [声明与证据审查代理](./resources/agents/claims_evidence_reviewer_agent.md)
- [委员会编辑代理（预审屏幕）](./resources/agents/committee_editor_agent.md)
- [委员会评审员3（文献对话审核员）](./resources/agents/committee_literature_agent.md)
- [委员会审核员4（逻辑链审核员）](./resources/agents/committee_logic_agent.md)
- [委员会审查员2（方法透明度检查员）](./resources/agents/committee_methodology_agent.md)
- [委员会评审员1（理论贡献询问员）](./resources/agents/committee_theory_agent.md)
- [批判性评论代理（魔鬼代言人）](./resources/agents/critical_reviewer_agent.md)
- [域名审核代理](./resources/agents/domain_reviewer_agent.md)
- [主编代理（直接拒稿筛选员）](./resources/agents/editor_in_chief_agent.md)
- [评估公平性审核代理](./resources/agents/evaluation_fairness_reviewer_agent.md)
- [文献审稿代理](./resources/agents/literature_reviewer_agent.md)
- [方法论审稿代理](./resources/agents/methodology_reviewer_agent.md)
- [符号和数字一致性审核代理](./resources/agents/notation_consistency_reviewer_agent.md)
- [现有技术审阅代理](./resources/agents/prior_art_reviewer_agent.md)
- [修订辅导代理](./resources/agents/revision_coach_agent.md)
- [修改建议代理](./resources/agents/revision_suggestion_agent.md)
- [部分审稿代理](./resources/agents/section_reviewer_agent.md)
- [自洽审阅代理](./resources/agents/self_consistency_reviewer_agent.md)
- [合成剂](./resources/agents/synthesis_agent.md)

## 常见请求

```text
对 paper.tex 做一次 quick-audit，告诉我什么会阻止投稿。
```

```text
像期刊审稿人一样 deep-review 这篇论文，并产出 review workspace 和 HTML 报告。
```

```text
对这篇 IEEE 论文做 gate 检查，把硬阻塞和伪代码建议项分开。
```

```text
只审查文献定位，判断 research gap 是真实问题还是选择性引用制造出来的。
```

```text
基于 report_v1.md 对这篇修订稿做 re-audit，总结已解决和未解决问题。
```

## 重要说明

- `PRESUBMISSION` 是接入现有模式的机械层，不是新的公开模式。
- full/editor deep-review 可把高信号投稿前发现提升到 `pre_submission_readiness`；其他 focus 默认保留在 Phase 0 上下文。
- `claim_map.json` 区分可见锚点和支撑强度；citation key 本身不等于真实支撑。
- Data availability 默认 advisory；只有 venue 明确要求且 central source data 缺失时才阻塞投稿。
- PDF 输入只做文本类检查，跳过 LaTeX/Typst 源码 hygiene。
