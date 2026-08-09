# Logic Module Reference

Purpose: Check logical coherence, introduction funnel, heading lead-ins, literature review quality, chapter mainline, and cross-section closure.

For chapter-level rewrite planning, also read `../writing/thesis-writing-guide.md`. Keep `logic` as the diagnostic route, but use the guide to turn findings into a thesis-specific mainline plan.

## AXES Model (Paragraph-Level Coherence)

| Component | Role | Example |
|-----------|------|---------|
| **A**ssertion | Clear topic sentence | “The attention mechanism improves sequence modeling.” |
| **X**ample | Supporting evidence/data | “In the experiment, the attention mechanism achieved 95% accuracy.” |
| **E**xplanation | Why evidence supports claim | “The improvement comes from its ability to capture long-range dependencies.” |
| **S**ignificance | Connection to broader argument | “This finding supports the architectural design used in this thesis.” |

## Heading Lead-In Check (S1)

**Rule**: Every chapter, section, subsection, and content-bearing subsubsection must have a lead-in paragraph before any list, figure, table, formula, or child heading.

**Lead-in minimum**: State what will be discussed, why here, connection to previous content, and preview of internal structure.

**Detection**: Script scans `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph` - flags if first child is non-prose content.

### Chapter Introduction Specialization (Backward and Forward Bridge)

S1 checks only whether a lead-in exists. For the **chapter introduction** of each body chapter
(Chapter 2 through the chapter before the conclusion, with child sections), the script also performs a
specialized backward/forward bridging check (`% 章引言 ... [Script]`) that complements S1:

- **Missing backward link / missing forward preview** (Major/P1): the introduction does not connect to the previous chapter (no chapter number/bridge) or does not explain the current problem and section arrangement.
- **Relative reference** (Minor/P2): wording such as “previous chapter/above” should use an explicit “Chapter X” reference.
- **Too short / too long** (Minor/P2): deviates from the convention of 1-2 paragraphs, about 300-500 Chinese characters.

The introduction (Chapter 1) is handled by `_check_introduction_funnel` and explicitly excluded from
the chapter-introduction check, so there is no overlap. For rewriting guidance, see “Body-Chapter
Introduction” in [`../writing/thesis-writing-guide.md`](../writing/thesis-writing-guide.md).

## Literature Review Quality (A1-A4)

| Check | Rule | Detection |
|-------|------|-----------|
| A1: Topic clustering | Organize by theme, not author/year listing | Script: regex for 3+ consecutive “Author(Year) proposed...” |
| A2: Critical analysis | Each topic group needs evaluative commentary | LLM judgment required |
| A3: Gap derivation | Last paragraph must identify research gap | Script: keyword scan in final 10 lines |
| A4: Funnel citation density | Citations should narrow from broad to specific | LLM judgment required |

## Cross-Section Closure (C3)

**Rule**: Contribution claims in introduction must be echoed in conclusion.

**Detection**: Script extracts contribution keywords from `introduction`, checks for response keywords
(“验证了”, “证明了”, “实验表明”) in `conclusion`. Missing echo -> Major/P1.

## Introduction Mainline Checks (`--intro-mainline`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --intro-mainline
```

Four specialized introduction-mainline checks, all `[Script]` heuristics, run only when this flag is passed (default behavior is unchanged):

| Check | Rule | Severity |
|-------|------|----------|
| L-SCI | A scientific problem (table “科学问题” column or enumerated item) must not be a short noun phrase; it must include object-problem-method | Major/P1 |
| L-MAP | Counts of scientific problems/research contents/innovations should close; downgrade to Info when the body declares a non-equal item such as “engineering-validation contribution, not equal to...” | Major/P1 |
| L-FUN | The opening introduction paragraph must complete a domain background -> technical bottleneck -> this thesis funnel | Minor/P2 |
| L-DOM | A title containing “国内外研究现状” must discuss domestic/foreign work separately or declare thematic mixing | Info/P3 |

See [`../writing/introduction-guide-zh.md`](../writing/introduction-guide-zh.md) for rewrite templates and decision tables.

## Process-Chapter Mainline Checks (`--process-chapter`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --process-chapter
```

Specialized mainline checks for a process-analysis chapter (the industrial/process-background Chapter 2
form “process analysis + full-thesis method framework”). All are `[Script]` heuristics and run only with
this flag. Chapter 2 is scanned by default; `--section` can override the target chapter.

**Chapter-form precheck (two signals)**: the target chapter/section headings must match both (1) a
process signal (工艺/流程/过程分析/变量分析) and (2) a framework signal
(总体框架/技术框架/研究方案/总体方案/方案框架) before applying P-* checks. Otherwise emit one Info
(“if this is a method+experiment chapter, use the method-chapter rules”) without forcing process-analysis
checks. Common method-chapter headings such as “problem description/overall framework” no longer trigger alone.

| Check | Rule | Severity |
|-------|------|----------|
| P-FLOW | The process/flow-analysis section has no `\ref{fig:...}` flowchart reference | Major/P1 |
| P-DERIVE | Difficulty/problem section lacks process-characteristic terms -> Major; has characteristic terms but no causal connection (导致/使得/难以/造成...) -> Minor | Major/P1 or Minor/P2 |
| P-FRAME | Framework section has no framework-figure reference or covers fewer than 2 method-module names/later-chapter destinations; missing explicit “Chapter X” mapping is Info only because 5/5 sample framework sections omit chapter numbers and place mapping in the introduction organization section | Major/P1 (missing figure/vague); Info/P3 (missing chapter-number mapping) |
| P-ORDER | Framework section appears before the difficulty/problem section, violating the order invariant | Minor/P2 |

See [`../writing/process-chapter-guide-zh.md`](../writing/process-chapter-guide-zh.md) for writing rules and positive/negative examples.

## Method Narrative Checks (`--method-narrative`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --method-narrative --section 〈章名〉
```

Run this branch when a method chapter contains multiple core modules or when reviewing module
motivation, inputs and outputs, equation explanation, and adjacent interfaces. `--section` must select
exactly one chapter per run. When it is absent, the script only lists candidate chapters and exits with
status 2; it does not classify a method chapter automatically. Before interpreting a finding or
rewriting prose, read
[`../writing/method-description-guide-zh.md`](../writing/method-description-guide-zh.md) as the complete
semantic contract for the six roles, edge-by-edge interfaces, and evidence levels.

| Check | Script lane | Severity |
| --- | --- | --- |
| M-HEADING | Locates places where heading announcements may replace module transitions | Minor/P2 |
| M-SEQWORD | Locates subsection openings that give layout order without a technical relationship | Info/P3 |
| M-EQUATION | Locates numbered equations that may lack a symbol-gloss entry point afterward | Minor/P2 |
| M-EDGETABLE | Emits a subsection list and edge-interface skeleton for LLM completion; not a finding | Unscored |

All three findings are `[Script]` candidates with `Meaning-Check: NEEDS-LLM`. The script does not judge
module motivation, design rationale, complete input/output, indirect dependencies, evidence strength,
or final closure; review those items module by module through the method-description guide.

## Body-Chapter Stitching and Introduction Bridging (Default)

- **P-PAPER (all chapters by default, no flag)**: report every occurrence of “源论文/小论文/N 篇论文” in visible prose (Minor/P2), without truncation. This is direct blind-review evidence of stitching; replace with “core problem/research content/this chapter.”
- **Graded missing backward link**: from Chapter 3 onward, when a chapter introduction lacks inheritance but the rest of the chapter contains a “Chapter X” dependency clue (reuses a prior chapter's output), retain Major; for a purely parallel chapter, reduce to Info. Parallel method chapters need not inherit, verified against five sample theses. See [`../writing/method-chapter-guide-zh.md`](../writing/method-chapter-guide-zh.md) for the recommended role-reuse sentence.
- **`--first-chapter N`**: when running on a single-chapter file, declare the actual number of its first `\chapter` so bridging checks use the true chapter order. Without it, a single-chapter file is treated as the first body chapter and backward-link checking is silent. Run cross-chapter checks (bridging, chapter mainline, full-document P-PAPER coverage) on the assembled document.tex when possible.

## Thesis Writing Mainline

When the user asks how to rewrite introduction, method chapters, experiment discussion, or conclusion and outlook, map the section to:

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
