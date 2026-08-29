# mode 契约与受控改写账本

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`（V6）

## Goal

把「审什么」（content module）与「能否写」（behavior mode）分成正交两维，
并让改写成为可追踪的状态转换而不是一次性文本输出（手册 P0-1 + P0-5）。

当前状态：改写契约只覆盖 `expression` 一个模块
（`academic-writing-skills/latex-thesis-zh/SKILL.md` Rewrite Contract 段），
其余 16 个模块被
`academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md`
列为纯诊断。高价值问题能被指出，却无法安全落到段落。

## Scope

**改**：新增 `academic-writing-skills/latex-thesis-zh/references/workflow/mode-contract.md`、
`academic-writing-skills/latex-thesis-zh/references/workflow/controlled-rewrite.md`、
`academic-writing-skills/latex-thesis-zh/scripts/thesis_workflow.py`；
更新 `SKILL.md`、`references/modules/routing-rules.md`、`agents/openai.yaml`；
`tests/skills/latex_thesis_zh/`；`docs/` 镜像 + manifest。

**不改**：既有 analyzer 的独立 CLI 行为（严格不变面）；IR 与 artifacts 实现。

## Requirements

- R1：五种正交 mode。`module × mode` 是矩阵，不是新模块。权限、产物、失败语义
  由 design.md 的输入优先级表与输出 destination 状态表唯一决定（TPR-11）。
  stdout 默认不是合同文件产物；只有 `--output -` 时 stdout 视为契约产物。
  未授权产物路径时返回摘要与建议文件名，不借生成 report 扩大源文件写入权限。

- R2：输入优先级（高到低）：（1）显式 `--mode`；（2）源写授权 flag；
  （3）`--output` / 报告路径；（4）自然语言「优化/润色」；（5）默认 `diagnose`。
  显式 `--mode revise` 且无源写授权：退出码 2，不降级为 plan。
  自然语言「优化/润色」且无源写授权：推断为 `plan`，退出码 0，无 source patch。
  未获写入授权不能用「给可直接替换文本」绕过权限。

- R3：`scripts/thesis_workflow.py` 统一 mode 调度。旧 analyzer 命令仍可独立运行。
  `--goal` / `--strength` / `--tier` 三轴语义不变：`--strength` 是改写幅度，
  `--tier` 是 deai 检测灵敏度，两套词汇刻意不重叠。

- R4：受控改写不变量写入 `references/workflow/controlled-rewrite.md`：
  保护 `\cite{}` / `\ref{}` / `\label{}` / 公式 / 数值 / 单位 / 模板宏 / 用户术语；
  允许删除无证据主张但须入账；允许补入已有证据支持的桥接句并记录 evidence
  anchor，不得凭写作常识补事实；claim strength 升级阻断自动写入；source patch
  默认 dry-run；生成文件不得手改；LLM `Meaning-Check: PRESERVED` 是提案；
  `[Script]` 层恒为 `Meaning-Check: NEEDS-LLM`。

- R5：`revision-ledger.jsonl` 每条记录 `change_id`、`finding_ids`、
  `source_span_before`、`source_hash_before`、`action`、
  `protected_tokens_before/after`、`numeric_tokens_before/after`、
  `claim_strength_before/after`、`evidence_anchors`、`meaning_check`、
  `compile_status`、`visual_status`。

- R6：改写顺序：冻结 source hash 与保护集合 → 选择 root causes 与允许动作 →
  先改章节角色/段落顺序/桥接 → 再改句子结构 → 最后改词汇/标点/版式 →
  记录 evidence 与 strength delta → fidelity checks。与
  `academic-writing-skills/latex-thesis-zh/SKILL.md` 既有由粗到细规则一致。

- R7：路由文档更新为 `module × mode` 矩阵，保留旧 CLI 兼容说明。
  `agents/openai.yaml` 的 `default_prompt` 改为先锁 mode / 权限再路由 module。
  `interface:` / `display_name:` / `short_description:` / `default_prompt:` 四键保留。

- R8：docs manifest、SKILL.md `version` 保持 `6.0.0`、C3 路由对齐、
  `just ci` 与 `just doc-build` 通过。本任务不对任何真实论文执行写入。

## Acceptance Criteria

- [ ] AC1（R1, R2）：同一 Chapter 1 请求分别以显式 `--mode diagnose` /
      `--mode plan` / `--mode revise` 执行：前两者零 source patch；后者无源写
      授权时退出码 2 且零 patch，有授权时默认 dry-run 并带 ledger
- [ ] AC2（R2）：自然语言「优化/润色」且无源写授权 → mode=plan、退出码 0、
      零 source patch；有源写授权 → revise dry-run
- [ ] AC3（R1）：diagnose/plan/re-audit/gate 无报告路径时只向 stdout 打摘要与
      建议文件名，不写源、不把 stdout 计为合同文件；有授权报告路径时写表中产物
- [ ] AC4（R1, R3）：每种 mode 的权限、产物、失败语义可由机器断言；覆盖显式
      mode、模糊请求、无 report 路径、无 source 写授权、`--output -`、以及
      自然语言「优化」且有源写授权
- [ ] AC5（R4, R5, R6）：fidelity gate：protected token multiset、numeric token
      multiset、claim strength、source hash 均有可核记录；改写顺序与 R6 一致
- [ ] AC6（R4）：claim strength 升级的 patch 被阻断
- [ ] AC7（R4）：手改 generated 文件的 patch 被阻断，finding 指向 owner
- [ ] AC8（R4）：写入范围外的 resolved path 被拒绝
- [ ] AC9（R4）：`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`
- [ ] AC10（R3, R8）：旧 analyzer CLI 命令、flag、help 文本、输出格式不变；
      路由 `--flag` 与 `--help` 一致
- [ ] AC11（R7）：`agents/openai.yaml` 仍含四键；`--strength` 与 `--tier`
      词汇未合并
- [ ] AC12（R8）：改 references / SKILL.md 后在本提交内重建 manifest + 双语
      页面；SKILL.md 只改 `last_updated`；`just ci` 全绿；`just doc-build` 成功
- [ ] AC13（R8）：本任务不对任何真实论文执行写入；revise 只验证到 dry-run +
      白名单层

## Constraints

- `revise` 默认 dry-run，本任务不放开真实写入
- 不新增 module（mode 是正交维度，不是新模块）
- SKILL.md 保持精简：mode 详细判据放 `references/workflow/mode-contract.md`
- 不改构建配置
- 格式化/回滚/提交遵循父任务 dirt 冻结清单与 Phase 3.4

## Dependencies

依赖子任务 2（`08-25-thesis-zh-semantic-artifacts`）：`plan` mode 的产物是
thesis/interface map，`revise` 的 evidence anchor 指向 claim-evidence map。
子任务 2 合入后开始。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-11 输入优先级、destination 全表、
  stdout 仅在 `--output -` 时为契约产物。
