# output eval 升级与 E1-E9 fixture

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`（V9，以及 V3 对手册 E1 的修正）

## Goal

让 eval 证明的东西从「路由对了、关键词出现了」升级为「结构、保源、证据强度、
假阳性」（手册 P1-3 的前四面）。当前 31 个 case 可以全部通过，同时 skill 继续
产生章节错选、假阳性和无用蓝图。人类可用性与 provider 对照保持 **missing evidence**。

本子任务结论口径是 **schema + fixture + 确定性执行证据**，不是「skill 输出更好」
的普遍效果声明（TPR-09）。

## Scope

**改**：`academic-writing-skills/latex-thesis-zh/evals/evals.json`（加字段）；
新增 `evals/fixtures/quality-regressions/`；新增
`academic-writing-skills/latex-thesis-zh/scripts/run_output_evals.py`
（确定性 repo-native runner）；新增
`tests/skills/latex_thesis_zh/test_output_evals.py`；
`evals/output-evidence/` 证据落点；`docs/` 镜像 + manifest。

**不改**：`evals/trigger_eval.json` 的 39 个查询语义（可加 mode near-neighbor，
但不承载 output quality 结论）；前五个子任务的实现。

## Requirements

- R1：case schema 只加字段不换 schema，保留
  `{id, prompt, expected_output, files}` 且 case 数不减。新增 `origin`、
  `input_files`、`baseline_output{kind,text,command,evidence_status}`、
  `with_skill_output{kind,text,evidence_status}`、
  `human_notes{rubric,status}`。`expected_contract` 不得计为模型胜出。旧 31 个
  case 保留 id 与 trigger 断言，标 `legacy-trigger-only`。

- R2：证据分层。本子任务只落地 `recorded_fixture` 与 `deterministic_run`。
  `provider_backed` 与 `human_blind_review` 保持 **missing evidence**。
  形状测试（字段存在、预填 expected）不得当作质量结果（TPR-09）。

- R3：确定性 runner `run_output_evals.py` 从 case 的 `command` 调用真实
  workflow/analyzer（argv 列表，无 shell），捕获 stdout/stderr/exit_code，
  把原始输出、命令、cwd、skill `last_updated`、可选 `ir_version`、时间、
  分母与标注版本写入 `evals/output-evidence/<case-id>/`。测试必须读取该落点，
  禁止只 `assert key in case`。预填 `with_skill_output.text` 不得作为唯一 oracle。

- R4：E1-E9 脱敏 fixture。每例必须有 `command` argv、可重放输入、以及读取
  `evals/output-evidence/<id>/` 的确定性断言。人工 rubric 与 provider 输出保持
  **missing evidence**。fixture 零项目专有事实。

  | ID | 执行对象 | 确定性断言（读 raw 输出） | 本轮不验收 |
  | --- | --- | --- | --- |
  | E1 | `deai_check.py --analyze` | 按 V3：`tabular`/`\text{}` 内「首先」不触发；正文段落可触发；被排除 span 零自然语言 finding | 手册原文「控制行被报为平行句式」；人工美感 |
  | E2 | `analyze_logic.py --process-chapter` | 两步选择器唯一命中过程章；无 unique 命中则要求 `--section`；符号表与成果章零主线 finding | 把全部 `body` 当过程章 |
  | E3 | `analyze_logic.py --motivation-thread` | list/table 节点进入承诺通道；承诺数/回应数/source span 与金标一致；control 节点不计数 | 表头误当承诺的人工判断 |
  | E4 | literature + thesis-map | 每段有 role；引文键 multiset 不变；不得新增文献 | 主题递进 1-5 分 |
  | E5 | artifacts `--artifacts interface` | 跨章接口冲突带两个 source anchor；`no_script_finding` 不得升 `pass`；外部权限保持 missing evidence | 物理语义人工分 |
  | E6 | experiment + claim-evidence | 「消融实验/消融设置」术语保留；禁止单组件净效应与「证明」类因果；数字/cite/ref/label multiset 不变 | 结果是否正面回答问题的人工分 |
  | E7 | evidence-intake + revise dry-run | 派生值可追 owner；手改 generated patch 被阻断；生成方向无环 | 是否需要重跑实验的人工判断 |
  | E8 | source-priority ledger | 按 claim 粒度记录 authority；展示路径无写生产变量权限；未核实字段 `missing evidence` | 来源可解释性人工分 |
  | E9 | `re_audit.py` | F1/F2/F4 或 F5 至少覆盖 `unresolved`/`addressed`/`new` 或 `regressed`；quote 变化仍匹配；hash mismatch 不写源 | 作者能否决定下一步的人工分 |

- R5：每个 revise case 至少运行：source path 白名单；`\cite/\ref/\label` 与数学
  环境 token round-trip；数字/单位/protected term multiset；claim strength
  non-escalation；generated owner/direction；`git diff --check`；改变 LaTeX
  接受面的 fixture 跑 compile wrapper。PDF 视觉检查保留为人工证据。

- R6：E1-E3 按 node kind 与 analyzer 分层报告 TP/FP/FN。分母与标注版本必须入
  report。无真实标注时状态为 missing evidence，不得预填目标已达成。

- R7：`evals.json` 用 Bash python 写入。`trigger_eval.json` 39 个查询语义不变。
  docs manifest、SKILL.md `version` 保持 `6.0.0`、`just ci` 与 `just doc-build`
  通过。

## Acceptance Criteria

- [ ] AC1（R1）：`evals.json` 保留四键；case 数不减；`test_evals_json_shape` 通过
- [ ] AC2（R1）：旧 31 个 case 的 id 与 trigger 断言保留，标 `legacy-trigger-only`
- [ ] AC3（R4）：E1 断言按 V3 写：生成表格/公式内的词不计数，正文段落内的词正常
      计数；不写手册原文「控制行被报为平行句式」
- [ ] AC4（R3, R4, R5）：E1-E9 各有可重放 fixture；runner 实际执行命令；
      `evals/output-evidence/<id>/` 含 raw stdout/stderr、command、exit_code、
      版本与分母；revise case 跑完 R5 的保源与白名单检查
- [ ] AC5（R2, R3）：测试失败当且仅当捕获输出违反结构/保源/证据强度/假阳性合同；
      仅检查 schema 字段存在的用例不得使 AC4 通过
- [ ] AC6（R1）：`expected_contract` 类输出未被计入任何胜率统计
- [ ] AC7（R4）：fixture 零项目专有事实
- [ ] AC8（R7）：`evals.json` 修改走 Bash python 写入
- [ ] AC9（R7）：`trigger_eval.json` 的 39 个查询语义不变；新增 mode
      near-neighbor 不改变 `test_trigger_evals.py` 的健康规则
- [ ] AC10（R2, R6）：`provider_backed`、`human_blind_review`、真实
      precision/recall、E4-E8 map 事实正确率四项状态为 **missing evidence**
- [ ] AC11（R7）：改 references / fixtures 后在本提交内重建 manifest + 双语页面；
      SKILL.md 只改 `last_updated`；`just ci` 全绿；`just doc-build` 成功

## Constraints

- 不换 eval schema，只加字段（C2）
- 不执行 provider A/B 与人工盲评（父任务决策 2）
- fixture 不得包含真实论文内容
- 不改构建配置
- 格式化/回滚/提交遵循父任务 dirt 冻结清单与 Phase 3.4
- 终检文案不得写成 Library-ready 或「skill 输出更好」的普遍结论

## Dependencies

依赖子任务 1-5 全部合入：E1-E4 验 IR 与规则，E5-E8 验 artifacts 与 mode，
E9 验 re-audit。末位执行。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-09 增加确定性 runner、E1-E9 合同表
  与禁止自证测试，结论缩为 schema+fixture+执行证据。
