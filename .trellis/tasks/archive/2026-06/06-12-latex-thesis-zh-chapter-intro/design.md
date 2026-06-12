# Design: latex-thesis-zh 章引言承上启下检查与指导

## 落点与边界

- 归属现有 `logic` 模块（它已拥有"标题后导语"与"章节主线"职责），**不新建模块、不加新 CLI 子命令**。
- 默认随 `logic` 输出（承上启下是论文主线核心，不做成 `--flag` 冷门开关）。
- 仅作用于"正文章引言"：level-1 标题，排除 `LEAD_EXEMPT_TITLES_ZH` 以及"绪论/引言/结论/总结/展望"等非正文章；绪论由 `_check_introduction_funnel` 负责，互不重叠。

## 与现有检查的关系

| 现有 | 现状 | 本次处理 |
|---|---|---|
| `_check_heading_leads`（S1） | 对所有标题统一判"有无导语 + 是否 <18 字" | **不动**，保持通用兜底 |
| `_check_chapter_mainline`（承上桥接） | 仅"本章/本文"开头 + 缺桥接 + ≥2 章才报，只查承上 | **扩展**为章引言专项：覆盖承上 + 启下 + 篇幅 + 相对指代 |
| `_check_introduction_funnel`（绪论漏斗） | 负责第1章绪论 | **不动**；章引言检查显式排除绪论，零重叠 |

实现方式：保留 `_check_chapter_mainline` 对外可观察行为（原本会报的"多章缺桥接"仍报），在其内部或新增 `_check_chapter_intro(content, lines, parser)` 分维度产出，由 `analyze()` 在默认路径调用。

## 检测启发式（全部 `[Script]`，分级）

章引言块 = `\chapter` 标题行之后到该章首个 `\section`（或下一 `\chapter`）之间的可见正文。对每个正文章：

| 维度 | 启发式 | 等级 |
|---|---|---|
| 承上缺失 | 块内无 `CHAPTER_BRIDGE_KEYWORDS_ZH` 桥接词，且无 `CHAPTER_NUM_REF_RE`（"第\d+章"）/"前文/上述"承接引用 | Major/P1 |
| 启下缺失 | 块内无"本章" + `CHAPTER_PREVIEW_KEYWORDS_ZH`（组织/安排/结构/首先…其次/分为…节/如下/将…展开）等预告信号 | Major/P1 |
| 篇幅异常（过短） | 块为空或仅 1 短句 → 提示扩成两段承上启下 | Minor/P2 |
| 篇幅异常（过长） | 块远超约定（如可见正文行数/字数超阈值，疑似正文堆入引言）→ 提示下沉到小节 | Minor/P2 |
| 相对指代 | 命中 `RELATIVE_REF_PATTERNS_ZH`（上一章/上文/前一章/下一章/下文）→ 建议改用章节号"第X章" | Minor/P2 |
| 疑似与绪论重复 | 不正则判定，输出一条 LLM 复核备注 | 备注 |

第一个正文章（通常上一章是绪论/相关工作）对"承上"放宽：缺桥接降级或豁免，避免对第2章误报。

## 新增/复用符号

- 新增常量（沿用现有命名风格，与 `CHAPTER_BRIDGE_KEYWORDS_ZH` 并列）：
  - `CHAPTER_PREVIEW_KEYWORDS_ZH`：启下/路标信号词。
  - `RELATIVE_REF_PATTERNS_ZH`：相对指代词。
  - `CHAPTER_NUM_REF_RE`：`re.compile(r"第\s*\d+\s*章")` 等章节号承接。
- 复用：`CHAPTER_BRIDGE_KEYWORDS_ZH`、`LEAD_EXEMPT_TITLES_ZH`、`_is_exempt_heading`、`_classify_lead_gap`、`parser.extract_visible_text`、`parser.extract_headings`。

## 文件改动面

| 文件 | 改动 |
|---|---|
| `references/writing/thesis-writing-guide.md` | 新增《正文章引言（承上启下两段式）》节：两段角色 + 篇幅 + 模板 + 正反例 |
| `references/writing/structure-guide.md` | 导语规范处加一句：正文章引言宜两段承上启下、用章节号指代 |
| `references/modules/logic.md` | 在 Heading Lead-In / Chapter Mainline 处加一句章引言专项说明 |
| `SKILL.md` | 路由规则 / Reference Map 增加一句章引言指引（最小措辞）；version + last_updated |
| `scripts/analyze_logic.py` | 扩展章引言检查 + 新增常量 |
| 测试（`tests/` 或 skill `evals/`） | 3 个 fixture + 断言 |

## 兼容性

- 不改写 `\cite/\ref/\label`、数学环境、模板宏、章节号。
- 输出沿用 `% Module (L##) [Severity] [Priority]: ...` + `[Script]` 标签。
- 章引言检查仅追加行，不删除既有 `logic` 输出；通过 fixture 回归验证既有检查不受影响。

## Validation Shape

- 规范两段章引言 fixture → 零 P1。
- 章后直接 `\section` fixture → 报承上缺失 + 启下缺失。
- "上一章"相对指代 + 单句 fixture → 报相对指代 + 篇幅过短。
- 既有 logic 测试 + contract + version 测试全绿。
