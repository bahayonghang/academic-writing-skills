# Design: latex-thesis-zh research-writing-level corpus expansion

## Scope Boundary

This task is thesis-specific:

- Expand the evaluation and trigger corpora for `latex-thesis-zh`.
- Keep the existing thesis route family intact.
- Do not add an English-paper-style `section-writing` module.
- Do not create a shared core with `latex-paper-en`.
- Use `research-writing-skill` only as a benchmark for writing moves.

## Benchmark Mapping

Translate the source writing moves into Chinese thesis conventions:

- 绪论 -> 背景 -> 技术瓶颈 / 研究空白 -> 科学问题 -> 本文贡献 -> 章节安排。
- 文献综述 -> 共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点。
- 方法章节 -> 章节主线、模块动机、设计说明、技术优势、与上一章的递进关系。
- 实验 / 讨论 -> 有效性、消融 / 敏感性、机理解释、与前人比较、局限与启示。
- 摘要 / 创新点 / 结论 -> 问题、方法、结果、贡献和边界闭合。
- 标题 / 导语 / 去 AI 味 -> 作为边界场景，用来区分 thesis 专属写作与泛化润色。

## Eval Families

The corpus should emphasize chapter-level writing rather than template mechanics:

1. 绪论漏斗与科学问题收束。
2. 文献综述的主题化对话与研究空白推导。
3. 方法章节的动机-设计-优势主线。
4. 实验与讨论的分层叙事、消融、机理、局限。
5. 摘要 / 创新点 / 结论的闭合与互相对齐。
6. 标题后导语、章节桥接、去 AI 味边界。

## Trigger Strategy

The trigger set should contain realistic near-neighbors:

- positive: thesis writing plans, chapter rewrites, literature-review restructuring, method mainline work, experiment-discussion layering, summary/contribution closure;
- negative: English paper requests, Typst requests, audit / gate review, bibliography-only work, generic prose polishing, from-scratch drafting, translation-only work, compile-only or format-only requests.

The negative set should be close enough to thesis work that a weak description might confuse them, but clear enough that a better description can separate them.

## Compatibility Notes

- Keep GB/T 7714, template, structure, consistency, logic, literature, experiment, title, deai, and abstract boundaries intact.
- Do not import paper-en section-writing phrasing directly.
- Prefer Chinese thesis-specific language over borrowed conference-paper terminology.

## Validation Shape

The final check should confirm:

- eval item uniqueness;
- trigger corpus balance;
- no accidental module additions;
- no regression in version or contract tests;
- no drift toward English paper or Typst phrasing.

---

## 章引言 Chapter-Intro Enhancement（Design）

### 落点与边界

- 归属现有 `logic` 模块（它已拥有"标题后导语"与"章节主线"职责），**不新建模块、不加新 CLI 子命令**。
- 默认随 `logic` 输出（承上启下是论文主线核心，不做成 `--flag` 冷门开关）。
- 仅作用于"正文章引言"：level-1 标题、排除 `LEAD_EXEMPT_TITLES_ZH` 以及"绪论/引言/结论/总结/展望"等非正文章；绪论由 `_check_introduction_funnel` 负责，互不重叠。

### 与现有检查的关系

| 现有 | 现状 | 本次处理 |
|---|---|---|
| `_check_heading_leads`（S1） | 对所有标题统一判"有无导语 + 是否 <18 字" | **不动**，保持通用兜底 |
| `_check_chapter_mainline`（承上桥接） | 仅"本章/本文"开头+缺桥接+≥2 章才报，只查承上 | **重构/扩展**为章引言专项：覆盖承上+启下+篇幅+相对指代 |

重构 `_check_chapter_mainline`（或新增 `_check_chapter_intro` 并由前者调用）时，保留其对外可观察行为的非回归：原本会报的"多章缺桥接"仍要报。

### 检测启发式（全部 `[Script]`，分级）

章引言块 = `\chapter` 到该章首个 `\section` 之间的可见正文。对每个正文章：

| 维度 | 启发式 | 等级 |
|---|---|---|
| 承上缺失 | 块内无 `CHAPTER_BRIDGE_KEYWORDS_ZH` 桥接词，且无"第\d+章/前文/上述"等承接引用 | Major/P1 |
| 启下缺失 | 块内无"本章"+（组织/安排/结构/首先…其次/分为…节/如下）等预告信号 | Major/P1 |
| 篇幅异常 | 块为空或仅 1 短句（极短）→ 提示扩成两段；或块过长（远超约定，疑似正文堆入引言）→ 提示下沉到小节 | Minor/P2 |
| 相对指代 | 命中"上一章/上文/前一章/下一章/下文" → 建议改用章节号"第X章" | Minor/P2 |
| 疑似与绪论重复 | 不正则判定，输出一条 LLM 复核备注 | 备注 |

新增常量（命名沿用现有风格）：`CHAPTER_PREVIEW_KEYWORDS_ZH`（启下信号）、`RELATIVE_REF_PATTERNS_ZH`（相对指代）、`CHAPTER_NUM_REF_RE`（"第\d+章"承接）。复用现有 `CHAPTER_BRIDGE_KEYWORDS_ZH`、`_is_exempt_heading`、`_classify_lead_gap`、`extract_visible_text`。

### 文件改动面

- `references/writing/thesis-writing-guide.md`：新增《正文章引言（承上启下两段式）》节。
- `references/writing/structure-guide.md` 与 `references/modules/logic.md`：各加一句指向章引言约定（用章节号指代、两段承上启下）。
- `SKILL.md`：路由规则 / Reference Map 增加一句章引言指引（最小措辞）。
- `scripts/analyze_logic.py`：扩展章引言检查 + 常量。
- 测试：`evals/` 或 `tests/` 下新增 3 个 fixture + 断言（脚本可判定）。

### 兼容性

- 不改写 `\cite/\ref/\label`、数学环境、模板宏、章节号。
- 输出沿用 `% Module (L##) [Severity] [Priority]: ...` + `[Script]` 标签。
- 版本号按 skill 约定递增（参见 `tests/test_skill_versions.py`）。
