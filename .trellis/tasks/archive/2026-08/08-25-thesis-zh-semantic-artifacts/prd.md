# 语义中间产物与 finding schema

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`

## Goal

在脚本候选与语义问题之间补上结构化中间产物（手册 P0-4），让 finding 能链接到
artifact node 与稳定 `root_cause_key`，并把项目证据摄取（P0-2）落成 schema。
解决的核心问题：现有 analyzer 只输出单点 finding，无法回答「整章角色、上下游交付、
结果问题、主张证据、边界由谁唯一拥有」，导致每次章节任务都要临时重建矩阵。

## Scope

**改**：新增 `academic-writing-skills/latex-thesis-zh/scripts/artifacts.py`、
`academic-writing-skills/latex-thesis-zh/references/schemas/artifacts.md`、
`academic-writing-skills/latex-thesis-zh/references/workflow/evidence-intake.md`；
`analyze_logic.py`、`analyze_literature.py`、`analyze_experiment.py` 输出
artifact refs；`references/modules/{logic,literature,experiment}.md`；
`tests/skills/latex_thesis_zh/`；`docs/` 镜像 + manifest。

**不改**：IR 实现（子任务 1 已交付）；mode 契约与写入面（子任务 3）；
写作规则文件（子任务 5）。

## Requirements

- R1：canonical finding schema 的唯一真源是
  `academic-writing-skills/latex-thesis-zh/references/schemas/artifacts.md`。
  采用共享核心 + 已声明扩展，不要求与
  `academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` 字段集合相等
  （TPR-07）。共享核心：`id`、`title`、`module`、`severity`、`confidence`
  （high|medium|low|unverified）、`source_kind`（script|llm|human，其中 human
  为本 skill 扩展，脚本不得写出）、`source_span`、`quote`、`root_cause_key`、
  `missing_evidence`、`gate_blocker`。本 skill 扩展：`artifact_refs`、
  `evidence_status`（validated|inferred|missing evidence）、`allowed_action`。
  明确不采用的 paper-audit 字段：`explanation`、`comment_type`、`source_section`、
  `related_sections`、`review_lane`、`allowed_wording`、`forbidden_wording`、
  `quote_verified`、`round_scores`。不引入投稿评分、desk-reject gate。
  脚本只能报告其确定性范围；LLM finding 必须带 quote / source span，不得借脚本
  provenance 提高置信度；重复 finding 以 `root_cause_key + source span` 合并，
  同时保留不同后果。

- R2：`claim_strength` 与 `evidence_anchor` 的 owner 是 `claim-evidence.json`，
  取值 `unsupported / observed / supported / strong`。finding 经 `artifact_refs`
  引用对应 claim 节点，只读快照放在嵌套对象 `claim_snapshot`：
  `{claim_id, claim_strength, evidence_anchor}`。禁止 finding 顶层再设可写的
  `claim_strength` / `evidence_anchor`。快照强度不得高于 claim-evidence。
  无对应 claim 节点时 `evidence_status=missing evidence`，
  `claim_snapshot={claim_id: null, claim_strength: unsupported, evidence_anchor: []}`。
  `allowed_wording` / `forbidden_wording` 只存在于 claim-evidence，不进入
  finding。`causal_eligibility` 与 `claim_strength` 分栏，不互相推导。

- R3：`scripts/artifacts.py` 集中拥有 schema 校验、稳定 ID 生成、根因合并、
  JSON/JSONL IO。不为每种 map 新建一个只做 JSON 读写的脚本。可参考
  `academic-writing-skills/paper-audit/scripts/consolidate_review_findings.py`
  的合并模式，不移植投稿评分。

- R4：四张核心 map 按请求最小生成，不创建空目录、不每次强制生成全部。

  | 产物 | 最小字段 |
  | --- | --- |
  | `thesis-map.json` | chapter/section role、research question、input、output、downstream consumer、boundary owner |
  | `interface-map.json` | producer、artifact、transform、consumer、unit/shape/meaning、evidence、permission |
  | `claim-evidence.json` | exact claim、anchor、strength、causal_eligibility、missing evidence、allowed/forbidden wording |
  | `result-question.json` | question、protocol、key difference、localization、mechanism anchor、boundary、next interface |

- R5：证据摄取 schema（`references/workflow/evidence-intake.md`）：
  `repository-preflight.json` 与 `source-priority-ledger.json` 按 claim 粒度
  记录来源类型、权威范围、冲突、只读性、生成方向、允许措辞。不能把一个文件整体
  标为「最高权威」。生成工件声明供子任务 1 的 IR `generated_from` 消费。

- R6：`analyze_logic.py`、`analyze_literature.py`、`analyze_experiment.py` 的
  机器输出走 JSON schema；人类可读输出（`% MODULE (L##) ...`）保持不变，属
  严格不变面。

- R7：docs manifest、SKILL.md `version` 保持 `6.0.0`、新测试位于
  `tests/skills/latex_thesis_zh/`、`just ci` 与 `just doc-build` 通过。

## Acceptance Criteria

- [ ] AC1（R4）：fixture 中每章可从 artifact 读出 role + research question +
      input + output + boundary owner
- [ ] AC2（R1）：schema 测试断言共享核心字段名存在、不采用字段缺席、未引入
      投稿评分 / review_lane / desk-reject；不断言与 paper-audit 字段集合相等
- [ ] AC3（R1, R3）：同一根因不同措辞的两条 finding 合并为一条，且保留两个
      source span
- [ ] AC4（R2）：finding 顶层无 `claim_strength` / `evidence_anchor`；只读
      强度出现在 `claim_snapshot`；无链接时
      `claim_snapshot.claim_strength=unsupported` 且 `evidence_anchor=[]`
- [ ] AC5（R5）：source-priority ledger 按 claim 粒度记录；「整文件级最高权威」
      写法被拒绝
- [ ] AC6（R5）：低优先级来源不得反写高优先级事实（旧附录值与权威正文值冲突时，
      指出唯一 owner 与派生方向，不建议改权威源）
- [ ] AC7（R2）：`causal_eligibility` 与 `claim_strength` 分栏存储，不互相推导
- [ ] AC8（R6）：三个 analyzer 的人类可读输出与改造前逐字节一致
- [ ] AC9（R4, R5）：项目专有事实零进入 core defaults；只出现在 adapter 或脱敏
      fixture
- [ ] AC10（R7）：改 references 后在本提交内重建 manifest + 双语页面；SKILL.md
      只改 `last_updated`；`just ci` 全绿；`just doc-build` 成功
- [ ] AC11（R4）：LLM 生成的 map 事实正确性标 **missing evidence**（每个 edge /
      claim 必须有 source anchor 与 status，但正确率未测量）

## Constraints

- 中间产物按请求最小生成；不创建空目录
- 不引入 paper-audit 的大工作区布局
- 项目 adapter 只有在至少两个项目重复使用后才固化为内置示例
  （本子任务只定 schema，不内置具体 adapter）
- 不改构建配置；不修改用户论文
- 格式化/回滚/提交遵循父任务 dirt 冻结清单与 Phase 3.4

## Dependencies

依赖子任务 1（`08-25-thesis-zh-visible-prose-ir`）：artifact 的 `source_span`
与节点引用建立在 IR 之上。子任务 1 合入后开始。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-07 共享核心 + 扩展；
  `claim_snapshot` 为只读快照，finding 顶层无独立强度字段。
