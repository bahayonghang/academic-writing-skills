# EN/ZH/Typst 润色能力升级

## Goal

对照参照 skill `ref/academic-writing-polisher`，补齐 `latex-paper-en`、`latex-thesis-zh`
（以及被对齐锁强制纳入的 `typst-paper`）在**润色**链路上的三类缺口：可审计的两层输出契约、
EN/Typst 表达链路的文档-脚本矛盾与脚本质量、ZH 完全缺失的句子/表达级润色模块。

本任务是父任务，只持有**需求集合、任务地图、跨子任务验收与集成复审**。执行细节、工具坑与
逐检查器契约由子任务各自持有，父任务不重复。

## Source of Truth

`ref/academic-writing-polisher/`（SKILL.md 122 行 + prompt-patterns.md + examples.md）。
可借鉴内核四条：

1. **Context First**（SKILL.md:40-51）：8 个上下文槽，只在确实影响本次编辑时才问。
2. **两条独立的轴**——这是本次规划最初判错的地方，必须分清：
   - SKILL.md:47 `Desired edit strength: light polish, moderate rewrite, heavy restructure`
     ＝**编辑幅度**（三档）。
   - SKILL.md:54-63 `Revision Modes` ＝**编辑目标**（Light polish / Clarity rewrite /
     Concision / Coherence，外加三个本任务不采纳的 response 类模式）。
     两轴名字有重叠（"Light polish" 两处都出现），但不同构：Concision 与 Coherence 之间没有
     幅度大小关系。
3. **可审计输出契约**（SKILL.md:65-84）：Polished Version / What Changed / Meaning Check /
   Risk Flags。价值是把改写从黑盒变成可复核。
4. **Core Rule**（SKILL.md:30-34, 86-94）：绝不悄悄添加智力内容；含义不清则**标注歧义并给
   保守版本**；措辞强度不可互换；统计值/基因蛋白名/化学名/模型名保持原样。
   注意 SKILL.md:92 只给出**原则**，**未提供任何自动识别方法**——这一点决定了 C2/C3 的自动化
   边界（见各子任务 design）。

## Findings（已逐条实读代码核验）

| #    | 范围        | 结论                                                                                                                                                                                                          | 归属 |
| ---- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| P0-1 | 三方        | 无任何语义保全契约。全仓 grep `meaning check\|risk flag\|author intent` 零命中。现有输出只有挑错格式，改写不要求声明保住了什么、请谁核对什么。Safety Boundaries 只防**编造**不防**语义漂移**                     | C1   |
| P0-2 | EN + Typst  | 模块文档与脚本直接矛盾。`improve_expression.py:27-29` 因 E15 删除了 `use→employ`、`show→demonstrate`，但 EN `expression.md:5-9` 与 Typst `EXPRESSION.md` 仍在教这两条。Typst 更重：示例写 `get→achieve` 而脚本是 `get→obtain`，且末行 `../references/STYLE_GUIDE.md` 是坏链 | C2   |
| P0-3 | ZH          | 无任何句子级/表达级润色模块。ZH 路由表 17 个模块无 `grammar`/`sentences`/`expression`；句长仅存在于 `deai_check.py` D1（需 `--tier`，量的是 CV 均匀度＝AI 痕迹，不是可读性）                                    | C3   |
| P1-1 | ZH          | `academic-style-zh.md`（136 行成熟中文规范）不在 SKILL.md Reference Map，无模块路由，全仓仅 `deai/guide.md:557`、`tense-guide-zh.md:54` 两处"另见"                                                              | C3   |
| P1-2 | 三方        | 润色链路无编辑幅度概念。`--tier` 只在 deai 且语义是**检测灵敏度**（`deai_check.py:206` docstring：light flags fewer, heavy flags more），复用其命名会造成一词三义                                                | C1   |
| P1-3 | 三方        | over-claim 校准未进润色分支。**更正**：`over-claim-guard` 并非不可达（EN `deai.md:20`、`tense-guide.md:67`、ZH `conclusion.md:41`、Typst `DEAI.md:33` 均有分支指针）；真实缺口是 `expression`/`grammar`/`sentences` 分支上**没有指针** | C1   |
| P1-4 | EN + Typst  | `improve_expression.py` 替换缺陷（实测确认）：`Make sure`→`develop sure`、`make use of`→`develop use of`、`very few`→`highly few`、`results  are`→`results are`（空白压缩）。**更正**：`\bmake\b` 不匹配 `makes`，原 PRD 的 `makes it possible` 例为伪 finding，已删 | C2   |
| P2-1 | EN + Typst  | 保护清单只覆盖 LaTeX/Typst 语法。统计值、模型名、数据集名、基因/蛋白名、化学名在正文里是纯文本 token，无护栏                                                                                                     | C2   |
| P2-2 | ZH          | 中文机械性检查空缺：标点混用、数值单位、成分残缺、搭配不当。ZH `references/formatting/` 无数字单位参考（EN/Typst 都有）                                                                                          | C3   |

## Scope Decisions（均已与用户确认）

- **D1 契约形态**：只对**产出改写建议**的模块强制两层契约；纯诊断模块（compile/format/
  bibliography/references/tables/spec-check/blind-review 等）不变，避免噪音。
- **D2 ZH 深度**：新模块 + 新脚本（不走 EN 脚本移植路线）。
- **D3 typst-paper 完整纳入**：`tests/contracts/test_writing_modules_alignment.py:71-85` 的
  `TIER1_HASH_GROUPS` 要求 `analyze_grammar.py` / `analyze_sentences.py` /
  `improve_expression.py` / `analyze_abstract.py` 在 en 与 typst 之间**逐字节一致**（实测三个
  当前均 IDENTICAL）。C2 必改前三个，故 typst 强制入范围：脚本逐字节镜像 **且** 修 typst 的
  EXPRESSION.md 与 SKILL.md 契约段。**不采纳**"解锁分叉"方案——那会为省事永久牺牲对齐不变量。
- **D4 编辑轴拆三**：`revision_goal`（做什么）/ `edit_strength`（改多狠）/ `--tier`（检测灵敏
  度，deai 专用**保持不动**）。三者命名不得互相借用。
- **D5 契约两层**：`[Script]` 层不得肯定式声明语义保全，只能报告变更事实并置
  `NEEDS-LLM`；`[LLM]` 层才给保全摘要，且标为提案。复用仓库既有 `NEEDS-LLM` 惯例
  （`check_spec.py:56` 状态枚举 `PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP`），
  **不发明新词**。

## Out of Scope

- 不移植 `Reviewer response` / `Peer review` / `Editorial feedback` 三个模式（非润色，且与
  `cover-letter`、`paper-audit` 边界冲突）。
- 不改 `bib-search-citation`、`paper-audit`、`cover-letter`。
- 不重新实现 over-claim 检测，只在润色分支加指针。
- 不改 `deai_check.py` 的阈值与 D1-D5 维度设计（已判定的有意取舍）。
- 不把三个 skill 变成通用「润色任意文本」工具；输入边界仍是 `.tex` / `.typ` 工程。

## Cross-Child Acceptance Criteria

父任务只验收**跨子任务**的闭合性；单子任务内部 AC 由各自 PRD 持有。

- [ ] 三个子任务各自完成并通过 check
- [ ] **契约字段一致性**：EN / ZH / Typst 三方的契约字段名、取值枚举、`[Script]` vs `[LLM]`
      分层规则完全一致，由一个契约测试同时断言三方
- [ ] **轴命名不冲突**：全仓不存在 `revision_goal` / `edit_strength` / `--tier` 三者语义混用；
      `deai --tier` 语义未被改动
- [ ] **所有权闭合**：`implement.md` 的模块所有权矩阵中，每个产出改写建议的模块都有且只有
      一个子任务负责，无悬空项（尤其 `deai_check.py`）
- [ ] **对齐锁全绿**：`test_writing_modules_alignment`（TIER1 字节锁）、`test_parsers_alignment`
      、`test_deai_alignment` 三把锁均绿；若有 `ALIGNMENTS` / `TIER1_HASH_GROUPS` 变更，
      须在 commit message 与 spec 中双声明
- [ ] **无伪回归项**：验收测试中不含已证伪的用例（如 `makes it possible`）
- [ ] `just ci` 全绿；基线为 **1338 passed / exit 0 / pyright 0 errors**（2026-07-27 实测），
      新增测试后 passed 数只增不减，pyright error 数不增加
- [ ] 无 Out of Scope 项被误做（尤其未新增 rebuttal 能力、未改 deai 阈值）

## Task Map

| 子任务                                | 覆盖             | 触及 skill        | 依赖              |
| ------------------------------------- | ---------------- | ----------------- | ----------------- |
| `07-27-polish-contract-shared` (C1)   | P0-1, P1-2, P1-3 | EN / ZH / Typst   | 无（须最先完成）  |
| `07-27-polish-en-expression-fix` (C2) | P0-2, P1-4, P2-1 | EN + Typst（镜像）| C1 design 定稿    |
| `07-27-polish-zh-expression-module`   | P0-3, P1-1, P2-2 | ZH                | C1 design 定稿    |

C1 的 `design.md` 是 C2/C3 的**前置契约**：它定稿字段名、枚举、两层分工与轴命名。C2 与 C3
之间无依赖，可并行；但两者都改 SKILL.md，合并时注意 `ROUTER_ROW_RE` 契约测试。

执行顺序、模块所有权矩阵与集成 gate 见 `implement.md`。

## 规划期已纠正的错误（留档，防复发）

1. 曾把 Revision Modes 当成 light→moderate→heavy 单一阶梯，并建议复用 `deai --tier` 命名——
   实为三个不同维度，已由 D4 拆开。
2. 曾要求 `[Script]` 输出肯定式 `Meaning-Preserved`——规则脚本无法判定语义，会制造虚假可审计
   性，已由 D5 改为两层。
3. 曾断言 `\bmake\b` 会把 `makes it possible` 改坏——实测不匹配，伪 finding，已删。
4. 曾把「pyproject 6.0.0 未提交」列为遗留 P0——实测 `dd01dcb` 已提交、工作区干净、`just ci`
   exit 0，已删。
5. 曾把 typst-paper 列为 Out of Scope——与 TIER1 字节锁直接冲突，已由 D3 纳入。
