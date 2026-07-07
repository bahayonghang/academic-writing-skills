# De-AI Module Reference

Purpose: Detect and reduce AI-generated writing traces while preserving LaTeX syntax and technical accuracy.

## Core Principles

1. **Syntax preservation**: Never modify `\cite{}`, `\ref{}`, `\label{}`, math, or LaTeX commands
2. **Zero fabrication**: Never add data, metrics, comparisons, or claims
3. **Information density**: Every sentence must convey verifiable information
4. **Restrained wording**: Avoid unsupported certainty; use appropriate hedging
5. **Academic payload first**: Preserve the problem-method-evidence-conclusion-boundary chain before changing tone

## Academic Humanization Contract

Before removing "AI flavor", extract four protected buckets:

- **Facts/evidence**: data, formulas, experiments, figures, tables, citations, and metrics.
- **Claims/stance**: the author's actual conclusion, method choice, uncertainty, and limitation.
- **Logic**: chapter role, paragraph role, claim-evidence mapping, and cross-chapter closure.
- **Boundaries**: scope, assumptions, unverified points, and `待补证` items.

Only after these are clear should the module remove structure shells. The default output remains diagnostic findings, a risk summary, or a rewrite blueprint. Provide prose rewrites only when the user explicitly asks for them.

## High-Priority AI Patterns (Must Fix)

| Pattern | Example | Fix |
|---------|---------|-----|
| Empty adjectives | "显著提升" | Replace with specific metric: "MAE 降低 12%" |
| Absolute assertions | "显而易见", "必然" | Add qualification: "实验结果表明" |
| Vague quantifiers | "大量研究" | Use numbers: "三项研究 [1-3]" |
| Template openings | "近年来", "随着科技的飞速发展" | Start from specific problem context |
| Stacked citations | "[1]-[5]" without discussion | Discuss each cited work individually |
| Filler connectors | "总之", "不可否认的是", "值得注意的是" | Delete; state conclusion directly |
| Structure shells | "不是 A，而是 B", "真正的问题", "我的结论是：" | Keep only evidence-bearing contrasts; otherwise state the academic claim directly |
| Vague referents/comparatives | "这些东西", "更自然", "更适合" | Name the research object, baseline, and evaluation criterion |

## AI Density Scoring

| Score | Action |
|-------|--------|
| >70% | Urgent: immediate rewrite |
| 50-70% | High: rewrite soon |
| 30-50% | Medium: review and revise |
| <30% | Low: light polish only |

## Edit Types

1. Delete empty phrases  2. Add specifics  3. Split long sentences  4. Restructure  5. Downgrade certainty  6. Remove redundancy  7. Add missing subjects  8. Replace templates

## English-Abstract Tense Check (`[Script]` LOW)

`deai_check.py` also flags present-tense reporting verbs (`shows`, `presents`, `demonstrates`, `outperforms`, …) — but **only inside the English abstract**. Chinese prose has no tense, so the check is gated to the English-abstract region and stays silent everywhere else. It locates that region across the flagship templates: generic `\begin{abstract}`, thuthesis `\begin{abstract*}`, and pkuthss `\begin{eabstract}`; the Chinese `abstract` / `cabstract` environments are skipped, and when several abstracts coexist the English one is chosen by content language. A verb whose subject is a figure/table/equation (`Figure 2 shows ...`) is exempt. Each hit is a `[Script]` LOW trace suggesting past tense for methods/results.

See [`../writing/tense-guide-zh.md`](../writing/tense-guide-zh.md) for the judgment-level checklist (which verbs are borderline, why `is`/`are` are excluded).

> Full details: see [`../deai/guide.md`](../deai/guide.md)
