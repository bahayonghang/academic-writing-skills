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
