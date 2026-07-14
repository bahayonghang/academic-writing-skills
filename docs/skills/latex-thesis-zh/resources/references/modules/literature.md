# Module: Literature Review Synthesis

Purpose: Determine whether related work/literature review forms a genuine academic dialogue instead of merely listing authors and years.

```bash
uv run python -B scripts/analyze_literature.py thesis.tex --section related
```

## Core Checks

- **A1: Thematic Clustering Instead of Author Listing**
  - Several consecutive sentences such as “Zhang (2019) proposed... Li (2020) proposed...” are judged as list-style writing.
- **A2: Comparative Analysis Sentence**
  - Each thematic cluster should end with a comparison, concession, limitation, or trade-off sentence, not merely report who did what.
- **A3: Research-Gap Derivation**
  - The literature review should derive a research gap from shared limitations of prior work, then connect it to this thesis's entry point.

## Introduction Citation Diagnosis (B1-B5, `--intro-citations`)

```bash
uv run python -B scripts/analyze_literature.py thesis.tex --intro-citations --bib refs.bib
```

The scope is the introduction chapter. If no introduction is recognized, the script counts the whole
file and emits a note. `--intro-citations` ignores `--section`. Every output is marked `[Script]`.

- **B1: Citation Count Range** - Compare unique citation keys in the introduction with `--min-cites`/`--max-cites` (default 120/160 for a doctoral thesis; a master's thesis may halve them according to university rules). Below the lower bound is Major; above the upper bound is Info only.
- **B2: Citation Pile-Up** - Locate every `\cite` containing 3 or more papers and recommend moving each citation to its corresponding claim sentence.
- **B3: Same Author/Team Clustering** - Normalize author prefixes in keys and report any prefix with >=3 papers, including line numbers for the whole co-cited cluster. Chinese-surname pinyin can create same-surname false positives; the output explicitly requires manual review.
- **B4: Year Distribution** (requires `--bib`) - Strict targets: >=30% in the latest three years and >=50% in the latest five years. Without a bib, degrade to an Info note rather than error. `--current-year` overrides the base year (system year by default).
- **B5: Visual Synthesis** - If the research-status scope contains no table or figure, suggest adding a research-evolution timeline or literature-comparison matrix.

See `../writing/introduction-guide-zh.md` for threshold sources and literature-selection proportions.
When citations are insufficient, search only the user's .bib; never fabricate entries.

## Recommended Rewrite Chain

`共识 -> 分歧 -> 局限 -> 空白 -> 本文切入点`

Recommended process:

1. Summarize the shared understanding of prior work under one theme.
2. Identify key differences, strengths/weaknesses, or applicability boundaries among methods.
3. Extract a limitation shared by those works.
4. Converge that limitation into one explicit research gap.
5. Finally explain why this thesis enters at that point.

## Degree-Thesis Adaptation

The literature review's “entry point for this thesis” must serve the mainline of the entire degree
thesis, not only the contribution sentence of one conference paper. When needed, also read
`../writing/thesis-writing-guide.md` and check:

- whether the gap derived at the end of the review is stated as a scientific problem in the introduction;
- whether later method chapters answer the gap directly;
- whether experiment chapters validate the contribution corresponding to the gap;
- whether the conclusion and outlook close or bound the gap.

## Boundaries

- Do not add any citation absent from the original text.
- Do not rewrite an entire prose passage by default; provide diagnosis and a rewrite blueprint first.
- If existing evidence cannot support a “research gap,” state that evidence is insufficient instead of inventing one.
