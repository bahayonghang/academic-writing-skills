# High-Frequency AI Writing Terms in Chinese Theses - Reference List

This document lists high-frequency words that most readily reveal AI writing traces in Chinese degree
theses and gives a recommended maximum occurrence count per document. The companion
`tone-thresholds.yaml` is the authoritative configuration actually read by `deai_check.py`; this file
is design documentation only.

## How Thresholds Take Effect

- `deai_check.py` reads `tone-thresholds.yaml` at startup.
- For each term under `term_thresholds:`, exceeding its threshold in visible body text from one
  document (after parser extraction removes citations, formulas, and comments) triggers one `[Script] LOW` trace.
- Chinese is not tokenized; counts use substring matching.
- Change thresholds in the yaml file; code does not read this document.

## Maintenance Cadence (This List Is a Snapshot, Not a Final State)

This list records **current** high-frequency AI writing terms, not permanent truths. As terms such as
“赋能” and “彰显” are widely called out, deliberate authors filter them and their frequency declines,
while new AI-preferred words continue to emerge. Review the list **every six months** against
excess-vocabulary research and add/remove terms as needed; do not treat it as frozen.

- Last review: 2026-06
- Sources: Kobak et al., *Sci. Adv.* 2025; Geng & Trotta 2025

## High-Frequency AI Chinese Connectors

These are not forbidden words; limited use is necessary. The threshold marks the point beyond which a reviewer is likely to perceive a formulaic pattern.

| Term | Threshold | Note |
|--------|------|-----------------------------------------------|
| 首先 | 4 | Marker of a templated argumentative opening |
| 其次 | 4 | Often stacked in a pair with “首先” |
| 然而 | 5 | Overused transition, often without genuine contrast |
| 此外 | 4 | Additive connector often used for stacking |
| 因此 | 6 | Inference/conclusion marker; a higher count is acceptable |
| 另外 | 3 | Duplicates the function of “此外”; consolidate them |
| 进而 | 3 | Progression word preferred by AI |
| 而且 | 4 | Duplicates the function of “并且” |
| 显然 | 3 | The more natural the context, the less this word is needed |
| 通常 | 4 | Vague frequency; replace when quantification is possible |
| 一般 | 5 | Weaker than “通常” |
| 尤其 | 3 | Emphasis word frequently used by AI |

## Content-Template Terms

| Term | Threshold | Note |
|--------|------|---------------------------------------------|
| 显著 | 5 | Usually lacks support from a p-value or effect size |
| 全面 | 3 | A single study can rarely be “comprehensive” |
| 深入 | 3 | Marketing language |
| 大量 | 3 | Vague quantifier |
| 众多 | 3 | Vague quantifier |
| 重要 | 5 | Explain what makes it “important” |
| 关键 | 5 | Same as above |
| 核心 | 4 | A paper should not have too many “core” items |
| 基本 | 4 | Ambiguous |
| 主要 | 5 | Ambiguous |
| 最为 | 3 | Superlative rhetoric |
| 极为 | 3 | Superlative rhetoric |
| 尤为 | 3 | Superlative rhetoric |

## Repeated Paragraph Openings (Burstiness)

Trigger when three consecutive paragraphs begin with the same first four Chinese characters. Typical cases:

- “本节首先...” / “本节首先...” / “本节首先...”
- “为了进一步...” / “为了进一步...” / “为了进一步...”
- “在本章中...” / “在本章中...” / “在本章中...”

Fix: rewrite at least one paragraph with a different syntactic form, such as a fronted adverbial, contrastive transition, or question.

## Paragraph-Opening Throat Clearing

Trigger when the first nonempty visible line of a paragraph matches one of these patterns:

- 综上所述 / 总而言之 / 总的来说 / 由此可见
- 值得指出的是 / 值得注意的是 / 需要指出的是 / 需要说明的是
- 不难发现 / 不难看出 / 众所周知 / 毋庸讳言
- Begins with “首先,” “其次,” “然而,” or “此外,”
- 一方面 / 另一方面

Each match records one `[Script] LOW` trace.

## Punctuation Patterns

- When the document-wide count of “——” exceeds `max_em_dashes_per_doc`, record one aggregated trace at the first occurrence.
- Record one trace for each Chinese “！” or English “!” in body chapters between the abstract and conclusion. Formulas, code, and comments are stripped and excluded.

## Content Outside This Table

- Syntax/grammar (covered by `analyze_logic.py` / editor self-check)
- Citation density (covered by `check_references.py`)
- Chapter structure (covered by `check_format.py` / `map_structure.py`)
- University naming rules (covered by `templates/`)
- Protected terms (covered by `forbidden-terms.md`)
