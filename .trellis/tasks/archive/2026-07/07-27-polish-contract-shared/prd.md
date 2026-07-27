# C1 共享润色契约：两层输出契约与编辑轴拆分

父任务：`.trellis/tasks/07-27-polish-capability-upgrade`
覆盖 findings：**P0-1、P1-2、P1-3**
触及 skill：`latex-paper-en`、`latex-thesis-zh`、`typst-paper`（三方 SKILL.md 与路由文档）

## Goal

为三个 skill 的**改写类模块**建立一套可审计且**不制造虚假可审计性**的输出契约，并把被混为一
谈的三个维度拆开。本子任务是纯契约层：定义 + 文档接线 + 契约测试，**不改任何检查器逻辑**。

C1 的 `design.md` 是 C2/C3 的前置冻结契约，未定稿前两者不得开工。

## Problem

### P0-1 — 无语义保全契约

全仓 grep `meaning check|risk flag|author intent` 零命中。三方的 Output Contract 只有
`% MODULE (Line N) [Severity][Priority]` 挑错格式。当模块产出 `Original:` / `Revised:` 时，
没有机制要求声明「保住了什么含义」「哪里需要作者核对」。现有 Safety Boundaries 只防**编造**
（不伪造引用/指标/基线/结果），不防**语义静默漂移**——而后者是润色的头号失效模式。

**但**：规则脚本无法可靠判断语义是否保全。若要求 `[Script]` 输出肯定式的「已保全」，等于用
契约的形式生产假保证，比没有契约更糟。契约必须分两层。

### P1-2 — 三个维度被混为一谈

| 维度                          | 语义                     | 现状                                                                 |
| ----------------------------- | ------------------------ | -------------------------------------------------------------------- |
| **编辑目标**（做什么）        | 语法/清晰度/精简/连贯    | 参照 skill SKILL.md:54-63 的 Revision Modes；三方均无此概念            |
| **编辑幅度**（改多狠）        | 轻/中/重                 | 参照 skill SKILL.md:47 的 edit strength；三方均无此概念                |
| **检测灵敏度**（报多少）      | 阈值缩放                 | 已存在：`deai --tier`，`deai_check.py` `_apply_tier` docstring 明写 "light flags fewer items, heavy flags more" |

三者取值词汇高度重叠（都会用到 light/heavy），一旦互相借用命名就会形成一词三义。参照 skill
自身两轴名字就有重叠（"Light polish" 在 :47 和 :55 各出现一次），是易混的根源，**不可照抄**。

### P1-3 — over-claim 校准未进润色分支

**更正先前措辞**：`over-claim-guard` 并非不可达——EN `references/modules/deai.md:20`、EN
`references/modules/tense-guide.md:67`、ZH `references/modules/conclusion.md:41`、Typst
`references/modules/DEAI.md:33` 都有分支级指针。真实缺口是：`expression` / `grammar` /
`sentences` 这条**润色分支上没有任何指针**，而这恰是最可能升高措辞强度的路径。

因此修法**不是**把它提升到 SKILL.md 顶层 Reference Map（SKILL.md 刚做过 104→69KB 瘦身，
顶层加条目是逆操作），而是在润色分支的模块文档里加强指针。

## Requirements

### R1 — 两层输出契约（P0-1）

字段名、枚举与分层规则的**权威定义在 `design.md`**，PRD 只锁语义要求：

- `[Script]` 层：只陈述**可验证的事实**（改了什么、跳过了什么受保护 token），语义保全判定
  一律置为 `NEEDS-LLM`，不得输出肯定式保全结论。
- `[LLM]` 层：可给出语义保全摘要与需作者核对项，但必须标为**提案**而非事实。
- 复用仓库既有 `NEEDS-LLM` 惯例（`latex-thesis-zh/scripts/check_spec.py:56` 的状态枚举
  `PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP`），**不发明新词**。注意 `NEEDS-LLM`
  目前仅存在于 `latex-thesis-zh`，C1 需将其引入 EN 与 Typst——这是有意的跨 skill 对齐。
- 风险标记取值必须是**闭集**，且必须包含「未评估」态。

### R2 — 三轴拆分与命名冻结（P1-2）

- 定义 `revision_goal`（编辑目标）与 `edit_strength`（编辑幅度）两个新概念，取值枚举在
  `design.md` 冻结。
- **`--tier` 保持不动**：语义仍为 deai 检测灵敏度，`_TIER_FACTORS` 不得改动。
- 两个新概念的参数名与取值**不得**与 `--tier` 的 `light|medium|heavy` 字面重合到会引起歧义
  的程度；具体命名由 `design.md` 定，PRD 只锁「不得一词多义」。
- 默认值必须是最小幅度（对应参照 skill "Choose the smallest mode that solves the task"）。
- 更新三方 SKILL.md 的 Required Inputs：润色类请求可追问编辑目标/幅度/作者原意，但沿用既有
  节制原则——**只在确实影响本次编辑时才问**，不得变成固定问卷。此边界写入 routing-rules。

### R3 — 润色分支加 over-claim 指针（P1-3）

- 在 EN `references/modules/{expression,grammar,sentences}.md`、Typst
  `references/modules/{EXPRESSION,GRAMMAR,SENTENCES}.md`、ZH 新增的 `expression.md`
  （由 C3 建文件，C1 提供指针文案）中加入指向各自 over-claim-guard 的强指针。
- 写明规则：**改写不得升高措辞强度**；升高即在风险标记中置 `overstatement`。
- 判据引用既有 guard 文档与 EN `references/writing/style-guide.md:81-91` 的四级 reporting
  verb 阶梯，**不新建替换表、不重复实现检测**。
- **不**把 over-claim-guard 加入任何 SKILL.md 的顶层 Reference Map。

### R4 — 契约测试

- 新增契约测试，**同时**断言 EN / ZH / Typst 三方的契约字段名、枚举取值、两层分工规则一致。
- 测试须覆盖：字段名一致性、来源标记（`[Script]`/`[LLM]`）分层规则、风险枚举闭集。
- 测试放置位置与加载方式遵循 `.trellis/spec/academic-writing-skills/testing-and-tooling.md`
  （路径常量从 `tests.support.paths` 取；非 EN/AUDIT 副本走 importlib 按路径加载）。

## Out of Scope

- **不改任何检查器逻辑**。C1 只改文档 + 加契约测试。脚本字段落地由 C2（EN/Typst）与 C3（ZH）
  执行。
- **不改 `deai_check.py`**（三副本）。它只产出行为指令不产出替换文本，且受 strict/logic 双层
  哈希锁保护。C1 仅在 SKILL.md 写明「依 deai 指令产出的改写适用 `[LLM]` 层契约」。
- 不改 `--tier` 语义或 `_TIER_FACTORS`。
- 不把 over-claim-guard 提升到顶层 Reference Map。
- 不新增 reviewer-response 能力。

## Constraints

- SKILL.md 路由表是对齐表格，改动触发 `ROUTER_ROW_RE` 契约测试。
- SKILL.md 字符串锁分布在 `tests/contracts/` 与 `tests/skills/paper_audit/` 两处；验证跑
  `just ci`，不要只跑单文件。
- 只改 `last_updated`，不 bump `version`（须持续等于 `pyproject.toml` = 6.0.0）。
- 改 `evals.json` 走 Bash python 写入，不用 Edit/Write。
- 不给 pytest 命令加 `PYTHONIOENCODING=utf-8`。

## Acceptance Criteria

- [ ] `design.md` 已定稿并冻结：字段名、枚举、两层分工、两轴命名与取值
- [ ] 三方 SKILL.md 的 Output Contract 段包含两层契约定义，字段名与枚举完全一致
- [ ] 契约适用范围**显式限定**为产出具体改写的模块；纯诊断模块**显式排除**（写在文档里，
      不靠默认）
- [ ] `[Script]` 层的语义保全判定为 `NEEDS-LLM`；风险枚举为闭集且含「未评估」态
- [ ] `NEEDS-LLM` 惯例已引入 EN 与 Typst，与 ZH `check_spec.py:56` 的既有枚举语义一致
- [ ] `revision_goal` / `edit_strength` 在三方定义，默认最小幅度，与 `--tier` 无一词多义
- [ ] `git diff` 确认 `_TIER_FACTORS` 与 `deai_check.py` 三副本**零改动**
- [ ] 润色分支模块文档含 over-claim 强指针 + 「改写不得升高措辞强度」规则
- [ ] over-claim-guard **未**出现在任何 SKILL.md 顶层 Reference Map
- [ ] routing-rules 写明追问边界（只在影响本次编辑时问）
- [ ] 新增契约测试同时断言三方一致，`just ci` 全绿且 passed ≥ 1338，pyright error = 0
