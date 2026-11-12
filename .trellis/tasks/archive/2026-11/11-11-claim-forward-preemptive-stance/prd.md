# claim-forward 补充：预设反驳壳、让步否定与改写侧立场保真

## Goal

把微信文章《论文AI味太重？我整理了一套防御写作Skill》中仓库尚未覆盖的"去除防御性表述"规则，
补进中英文论文写作 skill：

- `latex-thesis-zh` 与 `latex-paper-en` 的 `claim-forward` 指南增加四类仅 LLM 判断的处置，
  英文指南补齐中文已有的三类处置。
- 三个写作 skill（含 `typst-paper`）的改写契约补上对称规则：改写不得擅自削弱作者已有的判断强度。
- 用户说"去除防御性表述"时能路由到 `claim-forward`，且不与 `deai` 的"防御性推测解释"混淆。

全部交付位于文档、契约、eval 与测试层。本任务不改任何脚本和词表。

## 需求来源

- 文章事实记录：`research/source-article.md`。
- 逐条判定与既有契约限制：`research/gap-matrix.md`（G1–G16）。
- 上一轮整合：`.trellis/tasks/archive/2026-09/09-13-claim-forward-integration/` 与
  `09-22-thesis-zh-method-hedging-guides/`。本任务不重开其中已判定的采纳与否决。

## Requirements

- **R1 预设反驳壳（G1）**：EN/ZH 指南新增仅 LLM 的判据与三种去向。
  判据：句子在回应稿件数据和文献都没有提出的异议，且回应没有带来证据、条件或范围。
  去向：存在真实混杂或备选解释时，改写为一条带原因的具体边界；没有真实异议时删去壳，保留主张；
  属于定义性区分时保留（沿用已有的"否定转为正面陈述"处置）。
- **R2 让步后否定（G2）**：指南写明这是过度声称而非自我削弱。让步句指向真实混杂时不得删除。
  稿件已有分析时把结论绑定到该分析；没有分析时把结论收回到数据支持的范围，或标【待补证】。
  不得补造分析。计数与比例、分母变化转交结果分析模块。
- **R3 断言与让步壳共现（G3）**：指南给出固定修复顺序：证据前置，按确定性阶梯校准断言，
  再把模糊让步换成一条具体边界。同一证据缺口只输出一条 finding。
- **R4 空泛谦辞（G4）**：限制句必须写出对象和条件或量值，内容只能来自稿件。
  稿件没有可写内容时标【待补证】；与已有限制重复时删去副本。
  结论章展望前的承接句在写出具体局限时保持合法，不与 `CC-OUTLOOK-TRANS` 冲突。
- **R5 英文三类处置（G6）**：英文指南补"保留真实证据边界、否定转为正面陈述、弱点写成取舍"三节，
  语义与中文一致，示例为英文论文语境的合成短例。
- **R6 改写侧立场保真（G5、G7）**：三个写作 skill 的改写契约写明改写不得降低措辞强度。
  被禁止的静默改动至少包括：新增原文没有的 hedge、把作者的第一人称判断改成无主语的可能性表述、
  把范围缩得比原文窄、把具体陈述换成空泛评价、插入原文没有的预设让步。
  原文断言强于证据时作为过度声称 finding 报告，不在润色、去 AI 味或翻译改写里静默软化。
  `Risk-Flags` 闭集增加 `understatement`，仅 `[LLM]` 层可置；`[Script]` 可置集合不变。
- **R7 路由与触发（G8）**：ZH/EN 的路由行、模块触发词和 trigger_eval 覆盖
  "去除防御性表述 / 防御性写作 / 预设辩解 / 观点被磨平"及英文同义说法。
  "防御性推测解释"仍归 `deai`，需有一条边界查询防止误路由。
- **R8 零发现合法（G10）**：claim-forward 模块文档写明准确清楚的原文保留，
  不为凑数量输出 finding，未知不得写成确定。
- **R9 合成样例与 eval（G9）**：ZH/EN 各新增一份合成 fixture，含四类正例与至少四个应保持不动的边界例，
  领域覆盖质性证据与计数/比例。三份 `evals.json` 各追加相应条目。ZH/EN 各新增或扩充一份示例文档。
- **R10 同步**：两份 spec（claim-forward、polish-rewrite）更新；双语 docs 镜像与 manifest 同步；
  三个 SKILL.md 更新 `last_updated`。

## Constraints

- 不改任何 `scripts/*.py` 与两份 `claim-forward-terms*.yaml`；`CF-*` 脚本码集合保持五个。
- 四类处置不新增观察码，不建词表或正则（`claim-forward-contract.md` §3.1）。
- 不改 paper-audit 任何文件（其中五个由哈希锁定，文档层 `CF-*` 集合固定）。
- 不删除任何限制、不利对比或非主线结果；未验证的弱点不得写成设计优点。
- 不注入第一人称、观点或情绪；不判断 AI 作者身份；不承诺通过任何检测平台。
- 不得用 `defensive` 命名模块、脚本、码或文件；用户同义词只出现在触发词与说明文字中。
- fixture 与示例全部自写合成，不搬用文章配图文字，不使用私有论文语料。
- `description` 不超过 400 字符（现 EN 373、ZH 319、Typst 331）；`version` 保持 6.0.0。
- 实现前需完成评审并执行 `task.py start`。

## Acceptance Criteria

- [ ] **AC1（R1–R4）**：EN/ZH 指南各有四类处置；每类含判据、可保留例、不可改例和修复去向；
  明确写出"不新增观察码，不建词表"。
- [ ] **AC2（R2、R3）**：指南写明让步句涉及真实混杂时不得删除，且同段共现时先校准断言。
  合成样例中改后文本的断言强度不高于原文。
- [ ] **AC3（R5）**：英文指南含三类处置；契约测试断言三节存在，并保留既有归属与否决断言。
- [ ] **AC4（R6）**：三个 SKILL.md 的 `Risk-Flags` 行与两份契约测试的闭集一致且含 `understatement`；
  `[Script]` 可置集合断言不变；EN/Typst 的 expression、grammar、sentences、translation 模块
  与 ZH 的 expression、polish 模块都写有"不得降低措辞强度"及其例外路径。
- [ ] **AC5（R7）**：ZH/EN trigger_eval 各新增至少两条正向查询和一条边界查询；
  `test_trigger_evals.py` 通过；`test_no_new_module_named_defensive` 通过。
- [ ] **AC6（R8、R9）**：两份 fixture 存在且每个边界例在 eval 的 `expected_output` 中被要求保持不动；
  新增 eval 条目通过结构检查。
- [ ] **AC7（约束）**：`academic-writing-skills/` 下全部 `scripts/` 目录与两份
  `claim-forward-terms*.yaml` 零差异；`academic-writing-skills/paper-audit/` 零差异。
- [ ] **AC8（R10）**：`just ci` 四步通过；`uv run python docs/scripts/check_resource_sync.py` 通过；
  `just doc-build` 通过。
- [ ] **AC9（证据口径）**：交付说明区分结构检查、合成 eval 与真实模型运行；
  未做 provider 实跑与真实论文查准率评估的部分标 UNVERIFIED。

## 已确认决策（2026-11-11 用户确认，D1–D5 全部按建议执行）

| # | 决策 | 采用 | 未采用的备选 |
|---|---|---|---|
| D1 | 立场保真是否新增 `understatement` 标记 | 新增。与 `overstatement` 对称，可被契约测试锁定 | 只写规则文字，不动闭集 |
| D2 | `typst-paper` 是否移植 claim-forward 模块 | 本任务不移植，只随 D1 同步契约 | 做仅文档层移植，另开子任务 |
| D3 | 四类处置是否给仅 LLM 的新码 | 不给，按 §3.1 以小节标题称呼 | 仿 `CF-LOSS-FRAME` 增四个仅 LLM 码 |
| D4 | 空泛谦辞是否加入词表 | 不加。加入需重跑私有基线，且与结论章承接句冲突 | 基线可重跑后另开任务 |
| D5 | paper-audit 是否同步"让步后否定"信号 | 不同步，记为后续 | 另开任务，只改未锁定的文档 |

## Out of Scope

- 文章 25 项清单的整体导入、引用核对与数据复算流程（已有对应模块）。
- `typst-paper` 的 claim-forward 模块、脚本或词表。
- `check_claim_forward.py`、`deai_check.py`、`analyze_conclusion.py` 的任何改动。
- 检测规避、作者身份判断、情绪或口吻注入。
- 真实模型实跑评估与真实论文查准率评估。

## 修订记录

- 2026-11-11 v1：初版。来源抓取、差距矩阵与既有契约核对完成；D1–D5 待评审。
- 2026-11-11 v2：用户确认 D1–D5 全部按建议执行，并指定实施子代理使用 Opus 5.5。`design.md` 无需改动。
