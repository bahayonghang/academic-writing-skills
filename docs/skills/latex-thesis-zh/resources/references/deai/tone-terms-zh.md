# Chinese Thesis AI-Tone Terms — Density and Budget Reference

This document explains the term-density limits, short-document fallback,
section factors, and paragraph-opening budget used by `deai_check.py`. The
authoritative configuration is `tone-thresholds.yaml`; this document is not
read by the runtime. Every automated finding remains `[Script] LOW`, and its
`Meaning-Check` requires LLM/author review.

## How density limits work

- Limits are occurrences per 10,000 visible Chinese characters. Numerators
  and denominators share the runtime visible-prose adapter: equations,
  figures, tables, algorithms, comments, citation/label payloads, inline math,
  and command payloads are excluded.
- Below 3,000 visible Chinese characters, the absolute allowance is
  `ceil(密度上限 × 3000 / 10000)` and the finding is marked
  `fallback/短文档回退`.
- `首先/其次/然后/最后` receive an allowance only in recognized paper-organization,
  structural-outline, content-outline, technical-roadmap, thesis-structure,
  or chapter-summary sections. The organization factor is 6.6 and the summary
  factor is 2.5; background/review sections and non-sequence terms remain 1.0.
- A custom legacy YAML without `threshold_unit` keeps per-document absolute
  semantics and emits an upgrade notice on stderr. Old values are never
  silently interpreted as densities.

## Calibration and review

- Source: body text from five doctoral dissertations under
  `ref/thesis/decrypted`.
- Formula: `max(2.0, P90(密度) × 1.3)`, using linearly interpolated P90.
- Last review: 2026-08-29; next recalculation: 2027-02, then every six months.
- Term references: Kobak et al., *Sci. Adv.* 2025; Geng & Trotta 2025.

## Current density limits

| Term | Limit/10k chars | Term | Limit/10k chars |
| --- | ---: | --- | ---: |
| 首先 | 8.7 | 其次 | 2.7 |
| 然后 | 11.5 | 最后 | 6.4 |
| 其一 | 2.0 | 然而 | 5.9 |
| 此外 | 10.5 | 因此 | 11.9 |
| 另外 | 2.0 | 进而 | 10.9 |
| 而且 | 5.9 | 显然 | 2.0 |
| 通常 | 2.3 | 一般 | 4.8 |
| 尤其 | 2.0 | 显著 | 9.5 |
| 全面 | 2.3 | 深入 | 2.2 |
| 大量 | 4.5 | 众多 | 2.0 |
| 重要 | 9.8 | 关键 | 19.0 |
| 核心 | 2.0 | 基本 | 4.0 |
| 主要 | 15.4 | 最为 | 2.0 |
| 极为 | 2.0 | 尤为 | 2.0 |

These terms are not banned. A finding only says that document-level density
exceeds the reference distribution; check whether the word carries a genuine
logical, evidential, or structural function before revising it.

## Paragraph-opening throat-clearing budget

Paragraph-opening patterns are collected first, then one document-wide budget
is allocated from the visible Chinese-character count:

```text
budget = max(1, round(2.6 × corpus_chars / 10000))
```

Only occurrences starting at `budget + 1` emit `[Script] LOW`. Each finding reports
"hits M / budget N / occurrence K". The value `2.6/万字` is the rounded
inclusive P75=2.64 from the five-dissertation paragraph-opening proxy; a paper
below P75 may therefore have no excess finding.

## Other guards

- Burstiness still triggers when three consecutive paragraphs share the same
  first four Chinese characters.
- Document-level em-dash and body exclamation guards are unchanged.
- Grammar, citation density, section structure, and institutional naming are
  handled by their dedicated checkers.
