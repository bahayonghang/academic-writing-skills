# Design：正文各级段落职责与结构去重

对应 `prd.md` R1-R6。§1-§3 为文档层，§4-§6 为脚本层（决策 D1 已确认）。

## 1. 边界与所有权

- 只改 `academic-writing-skills/latex-thesis-zh`、其 docs 镜像、tests、spec。`experiment` 模块与 `analyze_experiment.py` 不动。
- 规则真相源：`references/writing/paragraph-roles-zh.md`。模块文档：`references/modules/logic.md`。路由：`SKILL.md` + `references/modules/routing-rules.md`。既有五份指南只做"追加一条 + 链接"，不改既有句子。
- 所有权矩阵（位置 → owner）：

| 位置 | 规则 owner | 脚本 owner | 本任务新增 |
| --- | --- | --- | --- |
| 章引言 | thesis-writing-guide 章引言节；method-chapter-guide §三 | `_check_chapter_intro`（默认） | 负面清单；`PR-INTRO-BG`、`PR-INTRO-TOC` |
| 含子节的总节导语 | structure-guide 导语规范 | S1 `_check_heading_leads`（默认） | 负面清单；`PR-LEAD-DUP` |
| 具体方法小节首段 | method-description-guide §三 | M-HEADING/M-SEQWORD（`--method-narrative`） | 负面清单；`PR-SUB-CHAL` |
| 公式后段落 | method-description-guide §五 | M-EQUATION（`--method-narrative`） | 负面清单；`PR-EQ-NARR` |
| 实验结果段 | results-analysis-guide §二/§八/§九 | RA-*（`experiment --results-analysis`）、B3、E-ATTR | 只指路，无新码 |
| 本章小结 | thesis-writing-guide 小结节；method-chapter-guide §六 | 无 | 负面清单；`PR-SUM-NEW` |

## 2. 新指南结构 `references/writing/paragraph-roles-zh.md`

```text
# 正文各级段落职责与结构去重
## 使用入口            —— 适用范围（第 2 章至结论前正文章）、与其他指南分工、`--paragraph-roles` 命令
## 六位置职责矩阵      —— R1.1 五列表
## 逐位置说明与正反例  —— 六小节，每节：合适职责 / 不必反复做 / 反例（标出重复了哪一层级）/ 正例
## 跨层级去重判据      —— R1.3：一处完整其余指代；信息增量两问；四类重复；结构功能性重述；过渡句带具体名词
## 与既有口径的协调    —— R1.4 四条
## [LLM] 复核清单      —— R1.5
## 检查映射            —— 位置 → 既有码 / PR-* / 仅 [LLM]；六个阈值常量表；UNVERIFIED 声明
## 来源                —— R1.6
```

"跨层级"的具体落法（本仓库原创，写入矩阵"不必反复做"列的判据来源）：绪论持有背景与综述的完整版 → 章引言不重述；章引言持有本章问题与方法链的完整版 → 总节导语不重述；总节导语持有本节对象与地图 → 小节首段不重述全部挑战；正文段持有公式与论证 → 公式后段只补符号/机制/边界，小结不新增论证；结果表持有数值 → 结果段只写差异、现象、适度解释。

## 3. 既有指南与路由的追加位置

| 文件 | 追加位置 | 内容（一到三行） |
| --- | --- | --- |
| `thesis-writing-guide.md` | 章引言节"弹性口径"列表末尾 | 不重述行业背景；目录式/路线式二选一不双写；节号目录不逐节展开；链接 |
| `thesis-writing-guide.md` | 小结节"篇幅"段后 | 不新增引用、公式、图表、推导；串要点合法、步骤级流程复述不合法；`\ref` 回指合法；链接 |
| `structure-guide.md` | 标题后导语规范列表，章引言条之后 | 含子节的总节导语只界定本节对象或给简短阅读地图，不重复整章问题与全方法链；链接 |
| `method-chapter-guide-zh.md` | §三列表末尾；§六列表末尾；§十映射表 | 背景/双写；不新增论证；映射行 |
| `method-description-guide-zh.md` | §三六角色段后；§五列表末尾 | 首段不列全部挑战；公式后不逐算子翻译；链接 |
| `results-analysis-guide-zh.md` | §二末尾 | 一句指路到新指南矩阵行 |
| `modules/routing-rules.md` | `--paragraph-arc` 条之后 | R3.1 判据条 |
| `modules/logic.md` | Subsection Context 节之后 | 新节 `## Paragraph Role Checks (--paragraph-roles)`（R3.2） |
| `SKILL.md` | Reference Map；路由规则歧义速判；`when_to_use`；`logic` 路由行 | R3.3 |

保真锁核对：`test_thesis_zh_guidance_fidelity.py` 锁定的既有句均为"存在/不存在"断言，追加行不触碰。

## 4. 脚本层：`--paragraph-roles`

### 4.1 入口与分支

```python
analyze(file_path, section=None, cross_section=False, motivation_thread=False,
        intro_mainline=False, process_chapter=False, first_chapter=None,
        method_narrative=False, paragraph_arc=False, subsection_context=False,
        subsection=None, emit_window=False, paragraph_roles=False) -> list[str]
```

- 新参数放末尾，既有位置参数顺序不变；`main()` 新增 `--paragraph-roles`（help："运行正文各级段落职责观察（章引言/总节导语/小节首段/公式后段/本章小结；默认关闭）"）。
- 分支插在 `subsection_context` 分支之后、兜底行之前：`if paragraph_roles: out.extend(_check_paragraph_roles(content, lines, parser, sections, pr_ranges, first_chapter))`，`pr_ranges = ranges if section else [(1, len(lines))]`（与 P-ARC 同构）。
- `--method-narrative` 无 `--section` 的提前 return 路径保持不变；该路径下 `--paragraph-roles` 不运行（文档注明）。

### 4.2 单元定位（复用优先）

| 单元 | 定位方式 | 复用 |
| --- | --- | --- |
| 章引言块 | 从 `_check_chapter_intro` 抽出 `_chapter_intro_block(chapter, headings, lines, parser) -> tuple[int, str, str] \| None`（report_line, intro_text, form），原函数改为调用该 helper，输出字节不变 | `_is_chapter_intro_exempt`、`INTRO_SECTION_TITLES_ZH`、`_classify_lead_gap`；第 2 章判定复用原函数的 `order==0` / `first_chapter` 逻辑 |
| 含子节的总节导语 | level-2 标题且在下一个 level≤2 标题前存在 level-3 标题；导语 = 该标题后首个 `ArcParagraph`（`is_heading_lead`）且汉字 ≥ `PR_LEAD_MIN_HAN` | `_split_arc_paragraphs`、`ArcParagraph` |
| 具体方法小节首段 | level-3 标题后首个 `ArcParagraph`；只在非豁免正文章内 | 同上；`_is_chapter_intro_exempt` |
| 公式后段落 | 每个正文章内 `_mn_equation_blocks`，块后首个可见段（到空行/标题/环境止） | `_mn_equation_blocks`、`_mn_visible_text`、`MN_EQ_GLOSS_RE_ZH` |
| 本章小结 | `extract_headings` 中标题规范化后等于"本章小结"的标题，范围到下一个 level ≤ 该标题 level 的标题或章末；**不用** `sections["summary"]`（单区间） | `extract_headings` |

### 4.3 六码契约

所有码：`[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`、`Current` 只给位置与计数/分数，不复制整句。输出格式由新 helper `_pr_finding(code, start, end, message, current, suggested, rationale)` 生成（行首 `% 段落职责（行 N）`），不改 `_arc_finding`。

| 码 | 触发条件 | 豁免 |
| --- | --- | --- |
| `PR-INTRO-BG` | 章引言块中 `background_markers` 去重命中 ≥ `PR_INTRO_BG_MIN_HITS`，且块内无"第X章"承接句命中同一句 | 第 2 章（概述式）；引言块为空（已由默认检查报） |
| `PR-INTRO-TOC` | 同一引言块内 `SECTION_NUM_PREVIEW_RE` ≥ 1 **且** `roadmap_markers` 中路线词（首先/其次/最后）≥ 2 → 双写；或 `SECTION_NUM_PREVIEW_RE` 命中 ≥ `PR_INTRO_TOC_MIN_ITEMS` → 逐节详列 | 单独节号目录（< 阈值）或单独路线预告 |
| `PR-LEAD-DUP` | 总节导语与本章章引言块的 `_arc_jaccard`（bigram）四舍五入 4 位后 ≥ `PR_LEAD_DUP_JACCARD` | 导语 < `PR_LEAD_MIN_HAN` 汉字；本章无章引言块；无 level-3 子节 |
| `PR-SUB-CHAL` | 小节首段 `challenge_markers` 命中 ≥ `PR_SUB_CHAL_MIN_HITS` 且 `enumeration_markers` 命中 ≥ 2 | 首段 < 40 汉字；绪论/结论/相关工作章；小节标题含"引言/概述" |
| `PR-EQ-NARR` | 公式后首段 `operator_markers` 去重命中 ≥ `PR_EQ_NARR_MIN_HITS` | 该段以"式中/其中"开头且只含符号释义（无算子词）；段 < 40 汉字 |
| `PR-SUM-NEW` | 小结区间内出现 `\cite{`、`\begin{equation\|align\|gather\|multline}`、`\[`、`\begin{figure\|table\|algorithm}` 任一 | `\ref`/`\eqref`/`\autoref` 回指；注释行 |

常量（全部标注"未标定 / UNVERIFIED"）：

```python
PR_INTRO_BG_MIN_HITS = 3
PR_INTRO_TOC_MIN_ITEMS = 5
PR_LEAD_DUP_JACCARD = 0.3500
PR_LEAD_MIN_HAN = 40
PR_SUB_CHAL_MIN_HITS = 2
PR_EQ_NARR_MIN_HITS = 3
```

### 4.4 词表 `references/writing/paragraph-roles-terms.yaml`

字段：`background_markers`、`roadmap_markers`、`challenge_markers`、`enumeration_markers`、`operator_markers`、`summary_new_argument_envs`。加载器 `_load_paragraph_roles_terms(script_dir)` 复制 `_load_paragraph_arc_terms` 的逐字段回退模式；内置默认元组与 YAML 相等（测试断言），docs 两份镜像与源相等（neutral）。`background_markers` 不复用 `INTRO_BACKGROUND_RE_ZH`（绪论漏斗专用，含"应用/需求"等通用词，直接复用会误报）。

### 4.5 数据流

```text
assemble(file) → parser.split_sections / extract_headings
  → 正文章列表（排除 _is_chapter_intro_exempt）
  → 每章：intro_block ─┬─ PR-INTRO-BG / PR-INTRO-TOC
                       └─ 与各含子节 section 导语比较 → PR-LEAD-DUP
       level-3 首段 → PR-SUB-CHAL
       _mn_equation_blocks → 块后首段 → PR-EQ-NARR
       "本章小结"区间 → PR-SUM-NEW
  → 按 pr_ranges 过滤（--section）→ findings（按行号排序）
```

## 5. 兼容性与取舍

- 默认输出零变化：flag 关闭时不进入分支；`_chapter_intro_block` 抽取须让 `baseline-before.txt` 与既有章引言测试全绿（这是唯一触碰既有代码的点，列为回滚点）。
- 为什么挂在 `logic` 而非 `experiment`：六行中五行是结构/衔接问题，章引言、S1、M-*、P-ARC 都在 `analyze_logic.py`；实验结果段已有 RA-* owner。
- 为什么 Info/P3：用户表格是写作建议而非规范硬条款；两态合规口径下只能报"双写/超量"；无标定语料。
- 为什么不做 `PR-RES-*`、`PR-SUM-PIPE`：结果段已由 RA-SHALLOW/RA-SECONDBEST/RA-CAUSAL/B3 覆盖；"串要点 vs 步骤级流水"需要语义判断，脚本会与"可'首先……最后'串要点"口径冲突。
- 词面重叠阈值（`PR-LEAD-DUP`）是假设：阅读地图式导语与章引言共享术语但不共享句子，bigram Jaccard 应显著低于复述；实施期用合成 fixture 校正到"复述报、地图不报"，不宣称跨论文精度。

## 6. 回滚

- 文档层单独 commit：`git revert` 即回滚；manifest 重生成一次。
- 脚本层单独 commit：删除 flag、分支、helper 与 YAML 即恢复；`_chapter_intro_block` 抽取若导致基线锁红，回退为原内联实现并改用复制逻辑的私有 helper（在 spec 记录两处同步义务）。
