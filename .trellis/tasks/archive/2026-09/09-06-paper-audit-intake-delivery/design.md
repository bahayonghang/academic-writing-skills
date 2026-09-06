# 设计

## 边界与依据

codex 建议是实践反馈，不能覆盖仓库既有契约。
`tests/skills/paper_audit/test_paper_audit_synthesis.py:106` 与
`.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` 决定改动上限：
`Auto-Detection at Intake` 小节不可删除，references 改动必须同步 manifest 与双语页面。

采用 qiaomu-meta 的泛化门与证据分层：把"用户已指定模式仍被复问"这一具体失败
重述为域中立行为——**已由用户显式解决的决策不重新提问**——再落成核心规则；
把"审查产物必须落盘"重述为**交付形态由权限约束决定，不由工作流默认值决定**。
两条都属于跨领域可复用的意图保真与权限最小化不变量，通过泛化门。

不生产新技能包，不引入 Skill IR 或 interface.yaml，沿用仓库原生 skill 结构。
现有 `evals/trigger_eval.json` 与 `evals/evals.json` 保留，只增用例不改结构。

## 最小机制与所有权

三项改动全部在文档层，不动脚本。

- **意图门控条件化**：`MODE_GUIDE.md` 的 `### Auto-Detection at Intake`
  在小节开头加一条前置条件——用户已显式指定模式时，四类检测只作陈述不作提问；
  四条 bullet 的措辞从"ask whether"改为分支表述（未指定 → 提问；已指定 → 陈述）。
  收尾句改为区分陈述与确认两种呈现。小节标题与 `revision_coach_agent` dispatch 保留原字面，
  以满足 `test_paper_audit_synthesis.py:106` 的两条断言。
- **实质冲突判据**：新增一条可判定定义——检测信号只有在会改变审查范围
  （纳入或排除章节、改变对比基线）或会改变结论（改变 PASS/FAIL、改变 issue 严重度）时
  才升级为提问。审稿信检测属于会改变范围的一类，因此保持提问，与既有测试一致。
- **交付形态三级**：`SKILL.md` 的 `## Critical Rules` 增加一段三级边界；
  T1 沿用现有 `SKILL.md:61`，T2 与 T3 为新增。
  三级只描述允许与禁止的动作，不引入新 flag、不引入配置项。
- **不落盘路径**：`workflow-detail.md` 新增一节，说明 T3 下可用与不可用的模式。
  清单由 2026-09-06 实跑定稿（见
  [write-behavior.md](../09-06-paper-audit-delivery-tiers/research/write-behavior.md)）：
  T3 可用 `quick-audit`、`gate`、`re-audit`；
  T2 与 T3 均排除 `polish`（写入论文目录的 `.polish-state/`）；
  T3 排除 `deep-review`。实跑推翻了原先把 polish 列为候选的静态推断。
- **证据缺失声明**：T3 下 `consolidate_review_findings.py`、`verify_quotes.py`、
  `render_deep_review_report.py` / `render_html_report.py` 均不可运行，
  文档要求按名列出并标 `missing evidence`，不允许用对话复述替代。
- **输出目录明确**：`SKILL.md:134` 与 `output-layout.md` 补一句——
  落盘前把 `--output-dir` 的实际目标路径念给用户；
  覆盖规则仍走 `workflow-detail.md:6` 现有确认，不新增覆盖入口。

## 泛化决策

升级为核心规则：已显式解决的决策不重复提问；权限约束决定交付形态；
无法运行的检查必须显式声明缺证据而非静默降级。

保留为条件指引：四类检测的具体标记串、30 页 / 25k 词阈值、
`review_results` 这一具体目录名——均是本 skill 的适用条件，不是通用不变量。

拒绝：不把"少提问"泛化为"不提问"——覆盖既有工作区、
`--previous-report` 零候选或多候选、检测信号与已指定模式实质冲突三种情形仍必须提问。
不把 T3 泛化为默认级别——默认仍是 T1，T2/T3 由用户声明触发。

## 顺序与单写者

按 intake-gating → delivery-tiers → verify 串行。

- `MODE_GUIDE.md` 与其 manifest 条目：intake-gating 唯一写者。
- `SKILL.md`、`workflow-detail.md`、`output-layout.md` 与后两者的 manifest 条目：
  delivery-tiers 唯一写者。
- `evals/trigger_eval.json`、`evals/evals.json`、`docs/skills/paper-audit/index.md`
  及其 zh 对应页：verify 唯一写者。

每个子任务完成自身镜像与 manifest 同步后再交接，不覆盖前序增量。
父任务的 R 编号属于父任务；子任务自定 R/AC 并标注父需求归属。

## 验收分层与回退

静态检查（grep、manifest 散列、contract 测试）证明形状与同步；
实跑 `audit.py` 证明落盘行为；
门控与交付形态属于 LLM 行为，需要保存实际响应并逐项审阅，
不能用关键字存在或 expected_output 匹配替代。

真实论文盲评、跨平台安装、独立第三方复核本轮不运行，写 missing evidence。

回退只针对当前子任务的确切 diff，禁止 `git reset --hard` 或 `git clean` 整树。
`SKILL.md` 不在 manifest 中，改它不触发资源同步检查，但会触发
`tests/contracts/test_claim_evidence_contract.py:79` 的字符串读取，须一并跑。
