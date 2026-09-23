# Cross-References Module Reference

Purpose: Check the integrity of figure, table, and equation cross-references across a
multi-file thesis project (\input/\include are resolved automatically).

## Checks

| Check                       | Severity      | Description                                           |
| --------------------------- | ------------- | ----------------------------------------------------- |
| Undefined reference         | Critical / P0 | `\ref{x}` has no matching `\label{x}` definition, a frequent blind-review deduction |
| Unreferenced label          | Minor / P2    | A `fig:`/`tab:`/`eq:` label is never referenced in the body |
| Missing caption             | Major / P1    | A figure/table environment has a label but no `\caption` / `\bicaption` |
| Reference before definition | Minor / P2    | In the same file, `\ref` appears before `\label` |
| Numbering gap               | Minor / P2    | Numeric label suffixes skip a value, such as fig:a1 and fig:a3 without fig:a2 |

## Command

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.tex
uv run python $SKILL_DIR/scripts/check_references.py main.tex --json
```

Supports `\ref` / `\eqref` / `\autoref` / `\cref` / `\Cref` / `\pageref` /
`\hyperref[]{}`. Exit code is 1 when a Critical undefined reference exists, otherwise 0.

## Notes

- Multi-file parsing follows `\input{}` / `\include{}` automatically and safely handles cycles.
- Labels/references/captions on comment lines are ignored; similar commands such as `\fakecaption` and `\captionsetup` do not count as captions.
- Caption presence recognizes optional short titles and whitespace or line breaks after `\caption` / `\bicaption`. It checks only whether a real caption command exists, not caption content or rendered template layout.
- Cross-file ordering is not checked because it is not meaningful; reference-before-definition is checked only within one file.

See [caption-guide.md](../formatting/caption-guide.md) for caption wording, continued figures, subfigures, and compiled-page acceptance.

`--school yanshan-ee-2025` adds Chinese terminal punctuation for non-table floats such as `figure` under `CAP-PUNCT`. Table floats are not reported again here. The optional short argument, argument 2 of `\bicaption`, an English period, and punctuation inside code, mathematics, or citation keys do not count. If the Chinese main argument cannot be identified, leave it manual. This mode does not add citation placement, page numbers, or bibliography-field rules. The default and `--school generic` do not enable it. Candidates are `[Script]`, Info/P3, and `Meaning-Check: NEEDS-LLM`.

## Optional citation placement and repeated pages

`--author-cite` and `--repeat-cite` are independent and may be combined with `--school`. Without either switch the script does not build the new scan, and the previous output stays unchanged.

`--author-cite` reports only a lagged citation after a clear author phrase in the same complete sentence. It supports `\cite`, `\citep`, `\citet`, `\parencite`, `\textcite`, `\autocite`, `\footcite`, and their star forms. Whitespace, comments, and 0 to 2 balanced optional arguments may occur between the command and its argument. `\textcite` and `\citet` do not add another author-position hint, because the rendered author is not in the source. 文献 and 已有研究 are not author subjects. A citation placed immediately after the author phrase is not reported. An uncertain Chinese name is only `RC-AUTHOR-UNCERTAIN` or a coverage note, and the text says the author-subject is uncertain. ASCII dotted abbreviations are not split. Incomplete sentences and paragraph boundaries are not guessed across. The report gives the file, line, short hit, and citation key. It does not rewrite the sentence or the key.

`--repeat-cite` counts each key once in each supported command. A repeated key inside one command counts once. One optional argument is the postnote. With two optional arguments, the first is the prenote and the second is the postnote. A blank postnote is empty. Visible citations in captions count. There is no school exemption and no separate figure exemption. Bibliography data, comments, macro definitions, `verbatim`, and `\nocite` do not count. The same key at least twice, with at least one missing postnote, produces `RC-REPEATPAGE`. Two occurrences that both have a literal page, or a single occurrence, do not. A postnote shared by several keys produces one `NEEDS-LLM` note even when it is non-empty, and does not prove a page for each key. A natural-language postnote is not page evidence, does not pass the college rule, and is not turned into an invented page. Literal pages are integers, roman numerals, and an explicit page range. This check still does not prove that the page supports the sentence. `\cites`, other multicite commands, custom macros that pass keys, and unexpanded arguments are not covered, and this mode says the coverage is incomplete.

Candidates are `[Script]`, Info/P3, and `Meaning-Check: NEEDS-LLM`. Together with `--school yanshan-ee-2025`, Chinese caption punctuation and these candidates both remain. The same caption is not reported twice for `CAP-PUNCT`.
