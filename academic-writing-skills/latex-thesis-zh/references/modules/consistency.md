# Consistency Module Reference

Purpose: Review terminology, abbreviation, and notation consistency across thesis chapters. Script observations are candidates for review, not proof of semantic equivalence.

## Terminology Consistency Rules

1. **Introduce unfamiliar terms**: Explain technical terms when readers need an explanation; add the English equivalent where relevant to the discipline or template.
2. **Preserve conceptual distinctions**: Deep learning and deep neural networks, machine learning and machine intelligence, and recurrent and recursive neural networks are different concepts. Co-occurrence does not justify merging their names.
3. **Review naming in context**: Built-in groups identify possible surface-form variation. Existing `--custom-terms` JSON groups express the author's explicit grouping, but neither group order nor frequency selects a canonical name. Confirm equivalence and a reason for revision before changing terminology.

## Abbreviation Rules

1. **First-use expansion**: Introduce an abbreviation before using it alone: "长短期记忆网络（LSTM）". First use means the first effective occurrence in the assembled document, including occurrences earlier on the definition's own line.
2. **Later uses**: Full forms and abbreviations may alternate for readability. Frequent full-form use after a definition is only an optional style candidate; it does not require replacing every full form.
3. **Chapter re-introduction**: Re-introduction can help readers who start at a later chapter. Repeating the same expansion within or across chapters is legal; later chapters may also reuse an earlier definition. The checker does not require a new definition in every chapter.
4. **Definition candidates**: The script takes a bounded visible name fragment beside parentheses on the same physical line. It does not cross a sentence boundary or a structural command to guess a full name. Missing reliable boundaries and different visible expansions are marked `NEEDS-LLM`; Chinese and English expansions may be equivalent.
5. **Titles**: Follow the discipline and template when deciding whether an abbreviation is sufficiently familiar for a title; the script does not establish that familiarity.

## Notation Uniformity

- **Variables**: Review symbol meanings and typography against the discipline and template.
- **Subscripts/superscripts**: Check that conventions and referents remain clear across equations.
- **Units**: Check dimensions and any stated conversions before judging different units for the same quantity inconsistent.

These are `[LLM]` or author checks. The consistency script does not establish mathematical or unit equivalence and does not modify equations, citation keys, labels, or source text.

## Common Issues

| Issue | Example | Fix |
|-------|---------|-----|
| Surface-form candidate | Author-grouped "自编码器"/"自动编码器" | Confirm the same referent before choosing a form |
| Undefined abbreviation | "使用 GAN 生成" without prior definition | Add first-use expansion |
| Different visible expansions | Chinese and English full forms for one abbreviation | Review equivalence with `NEEDS-LLM`, without assuming conflict |
| Possible notation conflict | $x$ as both input and output in different sections | Review scope and meaning without automatic mathematical edits |

## Detection Approach

```bash
uv run python scripts/check_consistency.py main.tex --terms
uv run python scripts/check_consistency.py main.tex --abbreviations
uv run python scripts/check_consistency.py main.tex
```

- `--terms`: Counts configured surface forms and reports naming or optional full-form style candidates. It does not prove synonymy or detect all capitalization inconsistencies.
- `--abbreviations`: Checks recognized uppercase abbreviations, first-use order, and visible definition candidates. Parenthesized defining abbreviations are excluded from standalone-use counts. An abbreviation with no definition is reported only at the existing threshold of two uses, excluding common stopwords; a use before a later definition is reported even once.
- Full mode runs both checks. Findings are `[Script]` observations; semantic decisions remain `NEEDS-LLM` until reviewed.

With a main-file input, the checker uses the existing loader's include expansion and source map, preserves text before and after includes, excludes unrelated drafts, and reports source paths and lines. Without an entry (a directory, `--all-files`, or the list-of-files API), it checks each file's order separately and explicitly states that cross-file order is unverified. It does not infer reading order from filenames. Loader warnings about missing includes or decoding remain visible; a clean result covers only the readable, recognized content in that scope.

Default behavior changes correct false positives and false passes: distinct concepts are no longer merged, late definitions are detected, legal repeated expansions are retained, and uncertain meanings are review candidates. These checks do not certify the semantic consistency of a real thesis.

> For logic and coherence checks (non-terminology), see [`logic.md`](logic.md). Full reference: [`../writing/logic-coherence.md`](../writing/logic-coherence.md)
