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

## Opt-in governance and abbreviation style

These checks stay off unless a flag is present. Without `--governance` or `--abbreviation-style`, the existing `--terms`, `--abbreviations`, and full-report output stay unchanged. `--governance` requires `--custom-terms` and extends the same JSON object. It does not add a second file, a schema version, or a migration layer. `zh` and `en` groups keep the existing loader. `banned`, `locked`, and `exempt` are read only when `--governance` is on.

```bash
uv run python scripts/check_consistency.py main.tex --governance --custom-terms terms.json
uv run python scripts/check_consistency.py main.tex --abbreviation-style
```

```json
{
  "zh": [["合成甲", "合成乙"]],
  "en": [],
  "banned": {
    "旧称": {
      "candidates": [
        {"text": "候选甲", "slot": "过程"},
        {"text": "候选乙", "slot": "对象"}
      ]
    }
  },
  "locked": {"标准名": ["旧别名"]},
  "exempt": {"environments": ["localterms"]}
}
```

| Field | Required behavior |
| --- | --- |
| `banned` | Each term needs one non-empty `text`. `slot` may be omitted. One hit lists every candidate and slot. |
| `locked` | The canonical name maps to forbidden variants. The report names that canonical form and does not infer it from frequency. |
| `exempt` | Add environment names only. Fixed protection cannot be cancelled. |

The scan uses assembled visible text and source positions. It skips comments, the preamble, math, cite/ref/label payloads, paths, `verbatim` / `lstlisting` / `minted`, `thebibliography`, and user-named environments. Inline `\verb`, `\lstinline`, and `\texttt` contents are still scanned; only the `verbatim`, `lstlisting`, and `minted` environments are masked. An abbreviation list is exempt only for an `abbreviation`, `abbreviations`, or `acronym` environment, or for a region titled `缩略词表` or `缩略词对照表`. An ordinary table is not exempt. External `.bib` files are not scanned, and titles are not imported as candidates. Chinese terms match literally. ASCII terms use identifier boundaries. Unknown custom macros make coverage incomplete, so no hit is not a claim of no problem. Invalid JSON, a missing file, or `--governance` without `--custom-terms` is a non-zero CLI error and does not print a pass conclusion.

`--abbreviation-style` is independent. After the same protected-span mask, a qualified first mention is `中文名称（英文全称，缩写）`. Chinese and English commas are both recognized. The reported project form is `（英文全称，缩写）`. Only a name with a clear in-sentence boundary is registered. An unclear boundary produces one `NEEDS-LLM` coverage note, not a false second-mention hit. Abbreviations may mix case, digits, and internal hyphens, such as `ZX`, `AbX`, and `X-2`. After a registered pair, `中文名（缩写）` or `中文名 缩写` is a candidate. A first mention that is only `中文名（缩写）` does not prove a qualified expansion and does not create a second-mention finding. Title Case inside a full parenthetical is a candidate only; proper-name case is not rewritten. Math parentheticals and `X 为中文名` glosses are not XOR issues. Combined with `--terms` or `--abbreviations`, same-position same-class candidates are deduped. The old definition recognizer stays. New JSON fields appear only in the new mode.

Findings use `[Script]`, Info/P3, and `Meaning-Check: NEEDS-LLM`. They name the local word, field, and position. They do not supply a replacement sentence.
