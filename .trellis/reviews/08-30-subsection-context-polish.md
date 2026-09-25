---
skill: trellis-plan-review
version: 0.4.0
task_dir: "D:/Documents/Code/Agents/academic-writing-skills/.trellis/tasks/08-30-subsection-context-polish"
task_name: 08-30-subsection-context-polish
task_status: planning
review_scope: task-tree
task_count: 3
task_members:
  - 08-30-subsection-context-polish
  - 08-30-subsection-cursor-zh
  - 08-30-subsection-lane-audit
task_statuses:
  08-30-subsection-context-polish: planning
  08-30-subsection-cursor-zh: planning
  08-30-subsection-lane-audit: planning
verdict: 需返回规划
blocking: 6
should_fix: 3
notes: 1
generated_at: "2026-08-30T19:22:31.8151499+08:00"
---

# Trellis 规划审阅报告

## 审阅范围

- 根任务：`08-30-subsection-context-polish`
- 模式：`task-tree`
- 任务数量：3
- 有序成员（根优先；顺序不代表依赖）：
  - `08-30-subsection-context-polish` — `planning`
  - `08-30-subsection-cursor-zh` — `planning`
  - `08-30-subsection-lane-audit` — `planning`
- Pass 7：三个成员均为 `planning`，不适用实现漂移检查。

## 结论

需返回规划 — 阻断 6 / 应修 3 / 提示 1

## 问题清单

### TPR-01 · 阻断 · paper-audit 的索引基础无法覆盖所选多文件 fixture 与全标题范围

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/prd.md:83-88`；`08-30-subsection-lane-audit/prd.md:23-35,74-78`；`08-30-subsection-lane-audit/design.md:9-39,41-70`；`08-30-subsection-lane-audit/implement.md:14-37,77-86`
- Claim: 在既有 `build_section_index` 记录上追加 `subsections`，就能让 `prepare_review_workspace.py` 与 zh 侧在 `evals/fixtures/thesis-project/main.tex` 上产生相同的小节编号集合，并为窗口写出 `source_file` 与可直接 `Read(offset, limit)` 的源文件行号。
- Evidence: 所选 `main.tex` 的正文只通过 `\include` / `\input` 引入（`academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex:19-31`）。当前 workspace 准备器只导入 `read_text_robust`（`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:19-27`），并把单个源文件的原始文本交给 `build_section_index`（同文件 `:223-253`），未使用同目录已存在且携带 assembled-line→source 映射的 `assemble()`（`academic-writing-skills/paper-audit/scripts/tex_loader.py:167-171`）。只读探针得到 `raw_headings=0, raw_sections=[]`；即使改为 assembled content，也得到 `assembled_headings=14, assembled_sections=[]`，因为 `split_sections()` 只保留可分类的语义 section，而 `chapter_ranges()` 才保证不丢无关键词标题（`academic-writing-skills/paper-audit/scripts/parsers.py:60-65`）。计划既没有装配/源映射机制，也没有脱离语义 section 的全标题索引。
- Impact: 按计划实现时，父任务编号集合验收会失败；更糟的是可能生成空 `subsections` / 空窗口，或把 assembled 全局行号误当作 `chapters/*.tex` 的文件内行号。用户要求的“上一小节 + 当前小节 + 下一小节”在常见多文件论文上不可达。
- Route: 二选一。A：在 B 的设计中显式使用 LaTeX/Typst 装配器及 origin map，按全文 `extract_headings` / `chapter_ranges` 枚举所有单元，再映射到现有 section 记录或独立的全局 subsection index，并增加多文件、无语义关键词标题与源文件行号测试；B：经用户确认把 paper-audit 范围缩到单文件、可分类 section，并同步收窄父子需求与验收，不能继续用当前 fixture 声称全量覆盖。

### TPR-02 · 阻断 · 新 lane 只写进文档，没有接入实际 focus 与 polish 执行路径

- Task: `08-30-subsection-lane-audit`
- Affected tasks: `08-30-subsection-lane-audit`、`08-30-subsection-context-polish`
- Location: `08-30-subsection-lane-audit/prd.md:37-51,72-83`；`08-30-subsection-lane-audit/design.md:72-105`；`08-30-subsection-lane-audit/implement.md:39-52`
- Claim: 把 `subsection_context_polish` 写入 `REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md` 和 agent 协议后，它会在 `--mode polish` 以及 `deep-review --focus logic|full` 下启用。
- Evidence: 实际 `FOCUS_TO_ALLOWED_LANES` 的 `full` 与 `logic` 集合没有该 lane（`academic-writing-skills/paper-audit/scripts/audit.py:224-264`），实际 fallback/恢复路径会用这个集合过滤 section 与 cross-cutting lane（同文件 `:917-919,951-1002`）；`polish` 路径只生成规则型 precheck state 并直接返回 `AuditResult`（同文件 `:2330-2365`）。B 的执行步骤 S5-S7 只改 references/agent，没有任何 `audit.py`、checkpoint、lane dispatch 或 mode orchestration 落点，也没有运行态验收。
- Impact: 文档与契约测试可以全绿，但新 lane 在声明的 mode/focus 下不会执行；核心交付退化为“存在一段说明”，没有真正携带窗口的审阅调用。
- Route: 二选一。A：把 lane 加入真实 focus/role/dispatch/checkpoint 路径，分别定义 deep-review 与 polish 的调度入口，并以运行态测试证明 `full`、`logic`、`polish` 的启用/禁用矩阵；B：把交付明确降级为手工协议，不再声称自动启用，并同步改目标、需求和验收。

### TPR-03 · 阻断 · 共用窗口与 finding 出参没有一个可实现的类型/来源适配契约

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-cursor-zh`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/design.md:48-57,73-100`；`08-30-subsection-cursor-zh/prd.md:13-23`；`08-30-subsection-cursor-zh/design.md:28-44,72-84`；`08-30-subsection-lane-audit/prd.md:23-26,43-56`；`08-30-subsection-lane-audit/design.md:41-66,107-115`
- Claim: 一个 `same_parent`、一个 `context_side: prev|current|next` 和统一的 `[Script] + Info/P3` 码形态足以让两个 skill 表达同一个窗口与 finding 契约。
- Evidence: 父契约把 `same_parent` 写成单值（`08-30-subsection-context-polish/design.md:48-53`），B 的 JSON 示例却把它写成 `{prev, next}`（`08-30-subsection-lane-audit/design.md:61-62`）；A 的 R-A1 要求每个 cursor item 含相邻字段（`08-30-subsection-cursor-zh/prd.md:13-17`），A 的 dataclass 又明确不存这些字段（其 `design.md:28-44`）。`parent_lead` 是合法证据部件，但 `context_side` 枚举没有它；`S-CTX-IN/OUT` 本身同时使用 current 与 prev/next，单值无法表达全部证据侧。来源也冲突：父契约把四码一律声明为 `[Script] + Info/P3`（`08-30-subsection-context-polish/design.md:98-104`），而 paper-audit 现有同类审稿契约明确是“人工观察，不是脚本 finding”（`.trellis/spec/academic-writing-skills/paragraph-arc-audit-contract.md:5-8`），且 canonical issue 的 `source_kind` 与 `severity` 必须是 `script|llm`、`major|moderate|minor`（`academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md:5-14,30-38`）。计划没有 adapter。
- Impact: 三处实现会产生互不兼容的 JSON/内部对象；跨父节 finding 无法诚实标注证据来源，audit 输出还可能把 LLM 判断伪装成 Script 或写入非法 severity。契约测试即使只锁字符串也不能修复这一运行时错误。
- Route: 在父任务先定义一份字段级 schema：相邻关系的逐方向类型、`parent_lead` 的归属、单/多证据侧表示、cursor 字段是存储还是派生，以及 zh-script 与 audit-LLM 的 source/severity 投影；随后同步改 A/B 的 PRD、design、ISSUE_SCHEMA 与契约测试。另一条路线是取消跨 skill 共用 finding schema，只共享语义标签，并明确两个 surface 的独立出参。

### TPR-04 · 阻断 · depth 回退、`x.x.x` 源需求与既有 fixture 验收互相冲突

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-cursor-zh`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/prd.md:10-14`；`08-30-subsection-context-polish/design.md:24-35`；`08-30-subsection-cursor-zh/prd.md:68-78`；`08-30-subsection-cursor-zh/design.md:46-58`；`08-30-subsection-lane-audit/prd.md:72-76`
- Claim: 既有 `evals/fixtures/thesis-project/main.tex` 能用于验收形如 `2.1.1` 的小节编号，同时设计在没有 depth 3 时回退到实际最大 depth（下限 2）。
- Evidence: 对整个 fixture 搜索标题只得到 `\chapter` 与 `\section`，例如 `chapters/intro.tex:1,6`、`chapters/method-a.tex:1,4`、`chapters/experiment.tex:1,4`，没有 `\subsection`；只读装配探针也显示最大深度为 2。按父契约 `target_depth` 回退规则（`08-30-subsection-context-polish/design.md:24-27`）与 A 设计（`08-30-subsection-cursor-zh/design.md:46-53`），该 fixture 不可能同时证明 depth 3 / `2.1.1`。回退时 identifier 到底是 `2.1` 还是仍强制三段也未定义。
- Impact: A 的首条 AC 按文本无法同时满足；实现者要么违背回退设计，要么让“分析下沉到 x.x.x”在该验收上退化为 x.x。B 的集合相等 AC 还可能只比较两个错误/空集合而误通过。
- Route: 先作一个产品决定：无 depth 3 时是“明确无可分析单元”还是允许 depth 2 回退。用新增的真实 depth-3 fixture 和固定期望序列验收 `x.x.x` 主路径；若保留回退，再为现有 fixture 单列回退 AC，写清 identifier 格式、非空预期与声明文本，并让 B 的集合比较同时断言预期集合而非只断言相等。

### TPR-05 · 阻断 · “合格段”在两侧不等价，且无合格邻段时没有窗口语义

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-cursor-zh`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/design.md:59-71`；`08-30-subsection-cursor-zh/design.md:10-22,70-84`；`08-30-subsection-lane-audit/design.md:68-70`；`08-30-subsection-lane-audit/prd.md:31-35,72-78`
- Claim: B 的“同义最小实现”与 A 的 `_arc_is_eligible` 形成同一个 `prev.tail/current.full/next.head` 契约；窗口总能输出三个、跨父节时四个区间。
- Evidence: 真实 `_arc_is_eligible` 不只要求 `>=40` 个汉字，还排除 heading lead、列表、受保护环境结尾及排除区（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1372-1379`）；B 的设计明确允许字符下限“因语种不同”而不同（`08-30-subsection-lane-audit/design.md:68-70`），与父任务“沿用 `_arc_is_eligible`”冲突。现有实现把标题后的第一个正文段标为 `is_heading_lead`（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1247-1258,1313-1317`），因此只有一个正文段的小节会没有任何合格 head/tail；父子设计没有规定 `null`、空列表、次优回退或跳过 finding，AC 却要求固定数量区间。现有契约测试计划只比文本/码集/编号，没有比较实际窗口区间。
- Impact: 两侧可对同一 `subsection_id` 选出不同的上下文；常见短小节或单段小节会丢失上一/下一内容，直接违背用户的三元上下文要求，同时所有现有 AC 仍可能通过。
- Route: 二选一。A：制定按语言/格式显式分支但可复算的 canonical eligibility，定义无合格段时的空值/回退/skip 行为，并用共享 fixture 比较两侧每个窗口的实际区间；B：限制能力只面向满足同一 40-Han 条件的中文 LaTeX，并同步删除 paper-audit 的跨语种/格式暗示。无论哪条，都要给单段、短段、列表/环境边界独立 AC。

### TPR-06 · 阻断 · “只改 current”核心安全边界没有行为验收，契约文本真相源也未定位

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/prd.md:12-14,42-58,81-91`；`08-30-subsection-context-polish/design.md:73-77,125-133`；`08-30-subsection-lane-audit/prd.md:31-46,58-61,72-85`；`08-30-subsection-lane-audit/design.md:82-90,117-125`；`08-30-subsection-lane-audit/implement.md:39-64`
- Claim: 三处字符串锁与 agent/template 的 DO/DON'T 足以验收“prev/next/parent_lead 只读，只有 current 可产出改写”，并能锁定 paper-audit reference、zh reference 与 agent 三处完全一致。
- Evidence: 父 AC 只检查码集/窗口协议句、编号集合、路由与 CI；B AC 只检查文件内存在 lane/focus block/协议句，没有一次调度输出或手工步骤证明 read-only 侧不会收到改写建议。B 的设计声称存在“paper-audit references”目标，却没有命名哪一个文件必须同时持有 depth 句、窗口句和四码表；实现步骤 S5-S8 分散修改 `REVIEW_LANE_GUIDE.md`、`SUBAGENT_TEMPLATES.md`、agent、POLISH_GUIDE 与 ISSUE_SCHEMA，无法从计划确定契约测试应以哪个 reference 为真相源。父任务要求“一字不差”，B 的测试机制却写成 `_normalize_whitespace` 后比较（`08-30-subsection-lane-audit/design.md:117-125`）。
- Impact: 核心授权边界可以在真实 reviewer/Mentor 输出中失守而全套自动化仍绿；实现者还必须自行发明 paper-audit 真相源与“完全一致”的强度，导致跨技能锁不可审计。
- Route: 指定唯一的 paper-audit reference 文件及精确/规范化比较规则；新增一个行为 eval 或明确的人工验收：在 prev、next、parent_lead 放入很诱人的可改问题，断言/核对所有建议仍只锚定 current。若当前平台不能稳定自动判定 LLM 输出，则把该项保留为 manual + UNVERIFIED，不能用字符串 contract 代替行为证明。

### TPR-07 · 应修 · `T_dup` 标定判据与失败后的任务树处置不确定

- Task: `08-30-subsection-cursor-zh`
- Affected tasks: `08-30-subsection-cursor-zh`、`08-30-subsection-context-polish`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-context-polish/design.md:83-104`；`08-30-subsection-cursor-zh/design.md:120-131`；`08-30-subsection-cursor-zh/implement.md:62-69,104-109`；`08-30-subsection-lane-audit/prd.md:3-5`
- Claim: “看分布上尾、人工核对后固定”能唯一确定 `T_dup`；若分布不稳定，可在 A 内删除 `S-CTX-DUP` 后继续交付其余三码。
- Evidence: 计划没有标定样本规模、正/负标签、候选阈值规则、误报/漏报取舍、复核人或通过条件；而所列既有 thesis fixture 本身没有 depth-3 单元。A 的 rollback 会删除 `S-CTX-DUP`（`implement.md:106-109`），但父 R1/R4、父契约测试、A R-A2/AC 和 B 的四码前置仍要求完整四码，且没有“停止 B、返回父规划同步修订”的 gate。
- Impact: 同一数据可由不同实现者选出不同阈值；失败分支还会让 A 的局部 PRD 与父/B 合同分叉，树顺序虽正确但依赖合同已经失效。
- Route: 在开始实现前写出可复算的标定数据、标签与阈值选择/接受规则，并指定人工 gate 的 owner；失败时必须停止并同步返回父/A/B 规划。另一条路线是本轮明确移除 `S-CTX-DUP`，先同步缩减四码合同，再开始三码实现。

### TPR-08 · 应修 · 两个精确仓库接口名与集成命令写错

- Task: `08-30-subsection-lane-audit`
- Affected tasks: `08-30-subsection-lane-audit`
- Location: `08-30-subsection-lane-audit/design.md:36-39`；`08-30-subsection-lane-audit/implement.md:31-34,77-86`
- Claim: `scripts/paths.py` 中要扩展的类叫 `ReviewLayout`，且 S11 可用 `prepare_review_workspace.py <fixture> --review-dir <tmp>` 生成比较输入。
- Evidence: 实际类名是 `WorkspaceLayout`（`academic-writing-skills/paper-audit/scripts/paths.py:34-39`）；workspace 准备器只接受 `--output-dir` 与 `--overwrite`（`academic-writing-skills/paper-audit/scripts/prepare_review_workspace.py:302-318`），`--review-dir` 属于其他 audit/checkpoint 路径。计划也没有说明命令输出的 slug 子目录以及从何处读取 `artifacts/data/section_index.json`。
- Impact: S4 的落点标识不存在，S11 的父任务集成命令会在 argparse 阶段失败；即使手工改 flag，比较程序仍缺确定的产物路径。
- Route: 把类名、flag、workspace slug/产物定位和编号提取命令改成真实接口，并为 S11 写出可直接执行、能断言预期集合的完整命令。

### TPR-09 · 应修 · 变更清单与 rollback 没有和需求/步骤闭合

- Task: `cross-task`
- Affected tasks: `08-30-subsection-cursor-zh`、`08-30-subsection-lane-audit`
- Location: `08-30-subsection-cursor-zh/design.md:5-8`；`08-30-subsection-cursor-zh/implement.md:33-100`；`08-30-subsection-lane-audit/design.md:5-133`；`08-30-subsection-lane-audit/implement.md:95-102`
- Claim: A 的“全部改动”都在 `analyze_logic.py`；B 若 `section_index.json` 下游不兼容，可把 `subsections` 移到独立文件作为 rollback。
- Evidence: A 的执行计划还会新增 fixtures、YAML、references、docs 双语页，修改 SKILL、manifest、`evals.json` 与 tests（`08-30-subsection-cursor-zh/implement.md:33-100`），与 design 的绝对变更声明冲突；两个复杂子任务都没有一份完整的 file change list。B 的 rollback 会直接撤销 R-B1 与其 AC“section_index 追加 subsections”，但不像 S7 rollback 那样要求同步修订 PRD，父任务也没有对应处置。
- Impact: 实现漂移检查、spec/resource 同步和按单元回滚没有可靠基线；B 可在“完成定义”之前悄然换成交付另一种数据合同。
- Route: 给两个子任务补完整、穷尽的 change list，并让每项对应 implement step、验证和 rollback；任何会撤销需求的 rollback 都必须停止、同步修订父子 PRD/AC 后再继续，不能作为同一执行计划内的透明替代。

### TPR-10 · 提示 · R/AC 映射与简写引用降低了机械可审计性

- Task: `cross-task`
- Affected tasks: `08-30-subsection-context-polish`、`08-30-subsection-cursor-zh`、`08-30-subsection-lane-audit`
- Location: 三个成员的 `prd.md` 验收标准段；`08-30-subsection-context-polish/prd.md:24-26`；`08-30-subsection-cursor-zh/design.md:60-62`；`08-30-subsection-cursor-zh/implement.md:8-12`
- Claim: 当前格式足以让机械预检建立 R→AC 与唯一 path:line 映射。
- Evidence: Pass 0 找到 4 个有多副本歧义的简写引用（两个 `scripts/analyze_logic.py:*`、两个 `parsers.py:*`）；结合任务上下文后均可人工归到 latex-thesis-zh，因此没有把它们升级为事实错误。三个 PRD 的验收项均未编号为 AC，也未标注证明哪条 R，预检无法生成 clause-level 交叉引用；父任务还报告了 `R1`–`R4` 的未定义引用噪声。
- Impact: 不会单独导致错误实现，但会让后续返修、自动预检和父子覆盖检查继续依赖人工推断。
- Route: 把引用写成 repo-root 相对完整路径；为每条 AC 编号并标注所证明的 R，复合 AC 按子句映射。保持现有事实内容，不必重写未被其他 TPR 点名的段落。

## 未能核实

- `subsection_context_polish` 的 LLM/Mentor 在真实调度中是否严格遵守只读边界 — 尚无实现、行为 eval 或可运行 lane，静态文档不能证明模型输出。
- `T_dup` 的数值、分布上尾与真实误报/漏报 — 标定代码、depth-3 数据和人工标签尚不存在。
- article、Typst 与 PDF 输入的最终 subsection/window 行为 — article fixture 尚待新增，B 对 Typst/PDF 只写了降级描述，未给可运行机制。
- 实现漂移 — 三个任务均为 `planning`，Pass 7 按规则未运行。

## 可靠部分

- Pass 0 成功解析 3 个成员、2 条父子边，所有 `parent` backlink 正确；无缺失 PRD、循环、重复成员、逃逸路径或阻断 placeholder。
- 三个任务的 `implement.jsonl` / `check.jsonl` 都含真实 spec 条目且引用文件存在，没有遗留 `_example`。
- 结合任务语境后，现状引用可定位到正确构造：`analyze_logic.py:561` 是章引言检查，`:1470` 位于 paragraph-arc 主检查入口，`prepare_review_workspace.py:112` 是 `build_section_index`，`parsers.py:147` 的确匹配 `*` 但不捕获它。
- `P-ARC-LINK` 不跨标题的现状属实：reference 明写该边界，代码也以 `segment_id` 阻断跨标题相邻段（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1528-1535`）。
- 父设计复用的现有常量值已核对：`PARAGRAPH_ARC_MIN_HAN=40`、`PARAGRAPH_ARC_LINK_THRESHOLD=0.0200`、`PARAGRAPH_ARC_DOUBLE_MISSING_RUN=3`（`academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py:1040-1043`）；排除集合也确含 abstract/conclusion/acknowledgment/appendix/organization/summary（同文件 `:1117-1124`）。
- A→B 的执行依赖没有只靠树顺序暗示：父 PRD 与两个子 implement 都明确写出 A 先完成/归档、B 再对齐。
- 默认关闭、保持既有位置参数、禁止改 `parsers.py`、docs/manifest 双语同步及 `just ci` 等兼容性门已进入规划；这些内容应保留，不需要在返修中重做。

## 盲区

An agent reviewing an agent's plan is not an independent second opinion. The reviewer and the
author share most of the same blind spots. A clean report means "this pass found nothing", not
"the plan is complete". Treat the findings as a triage list, not as an approval.
