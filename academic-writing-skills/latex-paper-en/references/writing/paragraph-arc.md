# Paragraph-Arc Review for English Papers

Use this optional diagnostic when the review question concerns paragraph openings, endings,
adjacent interfaces, or underdeveloped paragraph bodies:

```bash
uv run python -B scripts/analyze_logic.py main.tex --paragraph-arc
uv run python -B scripts/analyze_logic.py main.tex --paragraph-arc --section introduction
```

`--paragraph-arc` is additive. Omitting it leaves the existing `logic` output byte-for-byte
unchanged. The output is diagnostic only: every finding is tagged `[Script] P-ARC-*` and
`Meaning-Check: NEEDS-LLM`, and the checker never writes replacement prose.

## Scope and boundaries

- A candidate paragraph needs at least 40 visible English words, counted with
  `\b[A-Za-z][A-Za-z'-]*\b` after parser-based removal of protected markup.
- Headings start a new prose segment. The first paragraph after a heading still participates.
- Formula, figure, table, algorithm, code, and list environments are hard boundaries. The checker
  never reconnects the paragraphs on either side after filtering.
- Abstract, conclusion, acknowledgment, and appendix content is exempt.
- `--section` reuses the existing section resolver; it does not invent a second section model.

## Findings

| Code | Observable form | Manual question |
| --- | --- | --- |
| `P-ARC-LEAD` | Short predicate-free opening, empty-transition shell, citation-only lead, or numeric/symbol lead | Does the first sentence name the paragraph's claim, object, or question? |
| `P-ARC-CLOSE` | Last sentence lacks a configured retrospective or prospective signal | Does the paragraph close its claim or establish the next interface? |
| `P-ARC-LINK` | No explicit link and four-decimal endpoint-token Jaccard `< 0.0200` | Is the relation progression, contrast, cause, or reference? |
| `P-ARC-FLAT` | One visible sentence, or an author/year-only enumeration outside Related Work | Does the paragraph need comparison, decomposition, or explanation? |

`P-ARC-LINK` uses a strict boundary: `score == 0.0200` passes and only `score < 0.0200`
reports. If either endpoint has fewer than 8 visible words, the checker only tests explicit links
and marks the interface for review. Related Work author/year enumeration remains owned by A1.

In Introduction and Related Work, two originally adjacent eligible paragraphs that both lack lead
and close forms add one Minor/P2 group finding. Each individual observation remains Info/P3, and
any heading, short paragraph, exempt paragraph, environment, list item, or section change resets
the run.

## Evidence boundary

The defaults in [`paragraph-arc-terms.yaml`](paragraph-arc-terms.yaml), `N=2`, and `tau=0.0200`
are locked against controlled synthetic examples only. No corpus of 5-10 target-venue papers is
available. Real-paper precision, recall, venue transfer, and the external validity of these values
remain **UNVERIFIED**. A future review should use author-approved papers and keep claims separate
from the runtime contract.

AXES describes possible roles inside a paragraph; P-ARC only surfaces locations for review. A
topic lead can correspond to Assertion, a non-flat body can contain eXample or Explanation, and a
close can support Significance, but no morphological match proves that a semantic role is present.
