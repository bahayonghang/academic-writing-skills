# EN 系 parsers 多文件装配与章节切分修复（四拷贝同步地基）

> 父任务：`06-12-five-skills-optimization`
> 优先级：P0 · 依赖：无 · **被依赖**：`06-13-en-paper-precision`（E2/E4/E5/E6/E9）、
> `06-13-typst-reality`（T6/T7/T21）、`06-13-cover-letter-compliance`（C2/C3/C10）、
> paper-audit 子任务——**本任务必须最先做**（与 ZH 审计的 parsers-multifile 地位相同）。
> 审计依据：父任务 `research/latex-paper-en-audit.md`（E2/E6/E9）、
> `research/typst-paper-audit.md`（T6/T7/T21）、`research/cover-letter-audit.md`（C2/C3/C10）。

## Goal

latex-thesis-zh 在 06-12 审计中修复的解析底座（章节切分四缺陷、多文件装配、
鲁棒编码）从未回灌到 EN 规范拷贝——EN/typst/paper-audit/cover-letter 四份
parsers.py 至今共享同一套已知坏行为，导致三个 skill 的全部章节级分析在
`\section*{}`、复数标题、注释行、多文件工程上系统性失效。本任务一次性修复
EN 规范拷贝并经哈希锁同步全家。

## Requirements

### R1 LatexParser.split_sections 重写（修 E2 → 联动 C10/审计拷贝）

移植 ZH 的 `extract_headings` + `SECTION_TITLE_RULES` + `_split_sections_from_headings`
+ `resolve_section_keys` 架构（`latex-thesis-zh/scripts/parsers.py:56-91`），规则表英文化：

- `\section*{...}` 星号形式（现 `*?` 量词作用于 `n`，未转义——`\sectio{X}` 反而能匹配）；
- 复数/复合标题：`Methods`、`Experiments`、`Experimental Results`、`RELATED WORKS`、
  `Results and Discussion`、ALL-CAPS 变体（现关键词后紧跟 `}` 即不匹配）；
- 跳过 `%` 注释行（现 `% \section{Related Work}` 被当真章节）；
- 同名章节 `_2` 后缀保留（现直接覆盖丢区间）；
- `--section` 未命中时列出可用 keys（消除 E4/T19 类静默假阴性的土壤）；
- `methods→method` 等别名解析（resolve_section_keys，修 E5/T3 的脚本侧）。

### R2 TypstParser 适配真实工程形态（修 T7/T21）

- 模板形参提取：`#show: ieee.with(title: [...], abstract: [...])` 形态的
  title/abstract（charged-ieee 等 Universe 模板的标准用法）；
- `= Abstract` 英文标题识别（现只认 `= 摘要` 与 `#abstract[`）；
- 同名章节聚合/后缀（与 R1 同语义）；块注释 `/* */` 内标题剥离（现只跳 `//` 行）；
- 标题规则表与 LatexParser 共享别名机制。

### R3 多文件装配层（修 E6/T6 → 联动 C3）

- 把 `latex-thesis-zh/scripts/tex_loader.py`（include 解析 + ``源文件:行号`` 映射 +
  编码三级回退 utf-8→GB18030→replace）移植为 EN 系共享 loader；
- 新增 typ_loader 等价物：递归内联 `#include "x.typ"`（带循环防护与深度上限）；
- 本任务只交付 loader + parsers API 与其自身测试；各 skill 脚本入口的接线
  由对应子任务消费（en-paper-precision A2、typst-reality R2、cover-letter A 组）。

### R4 clean_text 显示数学修复（修 E9）

- `\\[^]]*\\]` 改为 `\\\[.*?\\\]`（现从任意反斜杠吃到 `\]`，吞正文）。

### R5 四拷贝同步与哈希锁更新

- EN 规范拷贝（`latex-paper-en/scripts/parsers.py`）先行，
  typst-paper / paper-audit / cover-letter 三份拷贝同步；
- 更新 `tests/test_parsers_alignment.py` 的 ALIGNMENTS 哈希；
- **不回同步 ZH 拷贝**：ZH 的 analyze_abstract/check_tables 特化与既有
  split_sections 行为保持现状（[[latex-thesis-zh-audit-2026-06]] 明令勿动）；
  若共享段落确需变更，先核对三个对齐测试
  （test_parsers_alignment / test_writing_modules_alignment / test_venue_templates_layout）。

## Constraints

- 章节键命名保持向后兼容（`introduction`/`method`/`experiment`/... 既有键不改名，
  只增不改），消费脚本的既有测试不得因键名变化而失败。
- loader 不引入第三方依赖（纯 stdlib，与 ZH tex_loader 一致）。
- 不 bump version（本任务甚至不动 SKILL.md）。

## Acceptance Criteria

- [ ] `\section*{Introduction}`、`\section{Methods}`、`\section{Experiments}`、
      `\section{RELATED WORKS}`、`Results and Discussion` 全部正确切分。
- [ ] `% \section{Conclusion}`（行注释）与 Typst `/* = Heading */`（块注释）不再误判。
- [ ] 两个 `\section{Experiments}` 同现时前一个区间以 `experiment_2` 类后缀保留。
- [ ] charged-ieee 模板 fixture：TypstParser 提取到 title 与 abstract；
      `= Abstract` 章节进入 split_sections。
- [ ] main.tex 仅含 `\input{...}` 的多文件工程经 loader 装配后全文可见，
      诊断行号映射回 `源文件:行号`；typ 工程 `#include` 同理。
- [ ] `resolve_section_keys("methods")` 解析到 `method`；未知名返回可用键列表。
- [ ] `clean_text` 不再吞 `\emph{...}` 与 `\[...\]` 之间的正文。
- [ ] test_parsers_alignment 四拷贝哈希更新后全绿；ZH 拷贝零改动。
- [ ] `just ci` 全绿。
