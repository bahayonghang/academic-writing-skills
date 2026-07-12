# Logic Module Reference

Purpose: Check logical coherence, introduction funnel, heading lead-ins, literature review quality, chapter mainline, and cross-section closure.

For chapter-level rewrite planning, also read `../writing/thesis-writing-guide.md`. Keep `logic` as the diagnostic route, but use the guide to turn findings into a thesis-specific mainline plan.

## AXES Model (Paragraph-Level Coherence)

| Component | Role | Example |
|-----------|------|---------|
| **A**ssertion | Clear topic sentence | "注意力机制能够提升序列建模效果。" |
| **X**ample | Supporting evidence/data | "实验中，注意力机制达到95%准确率。" |
| **E**xplanation | Why evidence supports claim | "这一提升源于其捕获长程依赖的能力。" |
| **S**ignificance | Connection to broader argument | "这一发现为本文架构设计提供了依据。" |

## Heading Lead-In Check (S1)

**Rule**: Every chapter, section, subsection, and content-bearing subsubsection must have a lead-in paragraph before any list, figure, table, formula, or child heading.

**Lead-in minimum**: State what will be discussed, why here, connection to previous content, and preview of internal structure.

**Detection**: Script scans `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph` — flags if first child is non-prose content.

### Chapter Intro Specialization (承上启下)

S1 只判断"有没有导语"。对正文各章（第 2 章至结论前、且含下级小节）的**章引言**，脚本另做承上启下专项检查（`% 章引言 ... [Script]`），与 S1 互补：

- **承上缺失 / 启下缺失**（Major/P1）：章引言未承接前章（无章节号/桥接），或未交代本章问题与各节安排。
- **相对指代**（Minor/P2）：出现"上一章/上文"，建议改用章节号"第 X 章"。
- **篇幅过简 / 过长**（Minor/P2）：偏离"1~2 段、约 300~500 字"的约定。

绪论（第 1 章）由 `_check_introduction_funnel` 负责，章引言检查按标题显式排除，零重叠。改写指导见 [`../writing/thesis-writing-guide.md`](../writing/thesis-writing-guide.md) 的"正文章引言"一节。

## Literature Review Quality (A1-A4)

| Check | Rule | Detection |
|-------|------|-----------|
| A1: Topic clustering | Organize by theme, not author/year listing | Script: regex for 3+ consecutive "Author(Year) proposed..." |
| A2: Critical analysis | Each topic group needs evaluative commentary | LLM judgment required |
| A3: Gap derivation | Last paragraph must identify research gap | Script: keyword scan in final 10 lines |
| A4: Funnel citation density | Citations should narrow from broad to specific | LLM judgment required |

## Cross-Section Closure (C3)

**Rule**: Contribution claims in introduction must be echoed in conclusion.

**Detection**: Script extracts contribution keywords from `introduction`, checks for response keywords ("验证了", "证明了", "实验表明") in `conclusion`. Missing echo → Major/P1.

## Intro Mainline Checks (`--intro-mainline`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --intro-mainline
```

绪论主线四项专项检查，全部 `[Script]` 启发式，仅在传入该 flag 时运行（默认行为不变）：

| Check | Rule | Severity |
|-------|------|----------|
| L-SCI | 科学问题（表格“科学问题”列或枚举条目）不得是短名词短语，须含对象-问题-方法三要素 | Major/P1 |
| L-MAP | 科学问题/研究内容/创新点条数应闭合；正文声明不等量（如“工程验证贡献，不与……等量”）则降级 Info | Major/P1 |
| L-FUN | 绪论首段须完成 领域背景 -> 技术瓶颈 -> 本文 三层漏斗 | Minor/P2 |
| L-DOM | 标题写“国内外研究现状”就必须分述国内/国外，或声明按主题混排 | Info/P3 |

改写模板与判别表见 [`../writing/introduction-guide-zh.md`](../writing/introduction-guide-zh.md)。

## Process Chapter Mainline Checks (`--process-chapter`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --process-chapter
```

过程分析章（工业/过程背景第二章"工艺分析 + 全文方法框架"章式）主线专项检查，全部
`[Script]` 启发式，仅在传入该 flag 时运行（默认行为不变）。默认扫描第 2 章，`--section` 可覆盖目标章。

**章式预判（双信号）**：目标章的章/节标题须同时命中①过程信号（工艺/流程/过程分析/变量分析）
与②框架信号（总体框架/技术框架/研究方案/总体方案/方案框架）才套用 P-\* 检查；否则只输出一条
Info（"若为方法+实验章式请走方法章规则"），不强套过程分析章检查（方法章常见的"问题描述/
总体框架"节名不再单独触发）。

| Check | Rule | Severity |
|-------|------|----------|
| P-FLOW | 工艺/过程分析节内无 `\ref{fig:...}` 流程图引用（工艺章无流程图） | Major/P1 |
| P-DERIVE | 难点/问题节缺工艺特性词 → Major；有特性词但无因果连接（导致/使得/难以/造成…）→ Minor | Major/P1 或 Minor/P2 |
| P-FRAME | 框架节无框架图引用，或未覆盖 ≥2 个方法模块名/后续章指向（框架空泛）；"第 X 章"显式章号映射缺失仅 Info（推荐加强项，5/5 范文框架节均不写章号、章号映射惯例放绪论组织结构节，不写亦合规） | Major/P1（缺图/空泛）；Info/P3（缺章号映射） |
| P-ORDER | 框架节先于难点/问题节出现（违顺序不变式） | Minor/P2 |

写作规范与正反例见 [`../writing/process-chapter-guide-zh.md`](../writing/process-chapter-guide-zh.md)。

## Body-Chapter Stitching & Intro Bridging (default)

- **P-PAPER（默认全章，无需 flag）**：可见正文出现"源论文/小论文/N 篇论文"表述即报（Minor/P2），
  **逐处报告**不截断——这是盲审最直接的拼接铁证，建议改"核心问题/研究内容/本章"。
- **缺承上分级**：第 3 章起章引言缺承接时，若章内其余部分出现"第 X 章"依赖线索（复用前章
  产出）→ 维持 Major；纯并列章 → 降 Info（并列方法章可不承上，5 篇范文核实）。推荐承接
  写法（角色复用句）见 [`../writing/method-chapter-guide-zh.md`](../writing/method-chapter-guide-zh.md)。
- **`--first-chapter N`**：单章文件运行时声明文件内首个 `\chapter` 的真实章号，使承上启下
  检查按真实章序生效（缺省时单章文件被视为第一正文章，承上检查静默）。跨章检查（承上启下、
  章间主线、P-PAPER 全文覆盖）**建议在装配 document.tex 上运行**。

## Thesis Writing Mainline

When the user asks how to rewrite 绪论、方法章节、实验讨论、总结与展望, map the section to:

```text
研究背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文方法/章节工作 -> 实验证据 -> 贡献闭合 -> 局限与展望
```

Return paragraph roles and evidence status. Do not invent citations, experiments, or contribution claims.

## Transition Signals

| Relation | Chinese | English |
|----------|---------|---------|
| Addition | 此外、进一步 | furthermore, moreover |
| Contrast | 然而、但是 | however, nevertheless |
| Causation | 因此、由此可见 | therefore, consequently |
| Sequence | 首先、随后 | first, subsequently |

> Full details: see [`../writing/logic-coherence.md`](../writing/logic-coherence.md)
