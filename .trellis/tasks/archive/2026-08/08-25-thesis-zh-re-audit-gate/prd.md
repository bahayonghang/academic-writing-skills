# re-audit 与 gate 语义

父任务：`.trellis/tasks/08-25-thesis-zh-quality-closure`
证据源：父任务 `research/evidence-audit.md`

## Goal

让复审比较根因而不是词面（手册 P0-5 后半），并让 gate 结论带证据边界
（手册 §7.4）。核心要防的两件事：换个说法被判为「已解决」；
脚本没报问题被当作「语义正确」。

## Scope

**改**：新增 `academic-writing-skills/latex-thesis-zh/scripts/re_audit.py`；
`references/workflow/controlled-rewrite.md` 的 re-audit 段；
`tests/skills/latex_thesis_zh/test_re_audit.py`；`references/modules/` 相关模块
的 gate 语义说明；`docs/` 镜像 + manifest。

**不改**：IR、artifacts、mode orchestrator 实现（前置子任务已交付）。
本脚本不写入论文源，不调用 mode 层执行 patch（TPR-08）。

## Requirements

- R1：`scripts/re_audit.py` 输入为新源 + 旧 findings / 可选 ledger。输出五态
  `addressed` / `partial` / `unresolved` / `new` / `regressed`，外加
  evidence delta（证据强度前后值、被影响接口）。比较依据是 identity 规则，
  不是 quote 词面。identity 与状态转移表以 design.md 为真源（TPR-08）。

- R2：identity = `root_cause_key` + span family。span family 优先 `node_id`；
  否则同一相对路径且行区间重叠或中心点相差 ≤5 行视为同一 family。
  源 span 移动但 identity 仍匹配时保持同一 finding，不标 `new`。
  拆分：一个旧 identity 对应两个新 span family → 仍开放的 family 按 design.md
  转移表判定，多出的 family 记 `new`。合并：两个旧 identity 合成一个新节点后
  按同一转移表判定。每个 identity 只输出一态；判定顺序以 design.md 为真源。

- R3：re-audit 只读。旧 patch 的 `source_hash_before` 与当前源不匹配时，输出
  `stale_patch=true` 与 `gate_blocker=true`，**不应用** patch。写入 owner 仍是
  子任务 3 的 `revise` mode。本脚本不得调用 `thesis_workflow.py` 的写路径。

- R4：gate 五态：`pass` / `fail` / `skipped` / `missing evidence` /
  `no_script_finding`。`no_script_finding` 不得升级为语义 pass。静态、编译、
  视觉证据彼此不可替代。缺人工或视觉证据时降为 `missing evidence`。

- R5：改变 LaTeX 接受面的 fixture 运行既有 `scripts/compile.py` wrapper
  （默认禁 shell escape）。PDF 视觉检查保留为人工或受控图像证据，本任务不实现
  自动抽样。

- R6：docs manifest、SKILL.md `version` 保持 `6.0.0`、`just ci` 与
  `just doc-build` 通过。

## Acceptance Criteria

- [ ] AC1（R1, R2）：七例 fixture 的 gold 分别为 `unresolved`（F1 只换连接词）、
      `addressed`（F2 补足接口且 missing_evidence 空）、`partial`（F3 部分
      missing_evidence 清除）、`new`（F4 新 root_cause_key）、`regressed`
      （F5 已解决 identity 再现或强度下降）、F6 span 移动保持 identity、
      F7 stale_patch 不写源
- [ ] AC2（R1, R2）：只换措辞不被判为 `addressed`；`root_cause_key` 相同但
      quote 变化时仍匹配到旧 finding
- [ ] AC3（R2）：span 移动（同行文件、中心点相差 ≤5 行或同一 `node_id`）保持
      原 identity，不标 `new`
- [ ] AC4（R5）：protected token / numeric multiset 在 re-audit 中被核对
- [ ] AC5（R3）：source hash 不匹配时输出 `stale_patch` + `gate_blocker`，
      工作树源文件字节不变；测试断言未调用 mode 写路径
- [ ] AC6（R4）：`no_script_finding` 与 `pass` 明确区分；脚本静默不产生
      `pass` verdict
- [ ] AC7（R4）：缺人工或视觉证据时 verdict 降级为 `missing evidence`，不判 pass
- [ ] AC8（R1）：每态输出含 evidence delta 说明
- [ ] AC9（R5）：编译 gate 走既有 `scripts/compile.py`，未新造编译器，shell
      escape 默认禁用
- [ ] AC10（R6）：改 references 后在本提交内重建 manifest + 双语页面；SKILL.md
      只改 `last_updated`；`just ci` 全绿；`just doc-build` 成功
- [ ] AC11（R4, R5）：PDF 视觉证据自动抽样标 **missing evidence**

## Constraints

- 不新造编译器或 include resolver
- 不引入 paper-audit 的 revision trajectory 渲染与投稿评分字段
- 不改构建配置；不修改用户论文
- 格式化/回滚/提交遵循父任务 dirt 冻结清单与 Phase 3.4

## Dependencies

依赖子任务 3（`08-25-thesis-zh-mode-contract`）：re-audit 消费
`revision-ledger.jsonl` 与 `final-findings.json`，gate 是 mode 矩阵的第五态。
子任务 3 合入后开始。

## 修订记录

- 2026-08-25 审阅返回：TPR-01 R/AC ID；TPR-08 identity/有序转移表、partial gold、
  F6/F7、只读与写入 owner 分离。
