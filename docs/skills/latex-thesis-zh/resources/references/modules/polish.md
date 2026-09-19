# Module: Unit Polishing (polish)

Use this module when the user explicitly asks to polish a paragraph, subsection, or the language of Chapter X. List the units first, then rewrite and verify one unit at a time. Check/review-only requests receive diagnosis only. See the [unit-polishing protocol](../writing/unit-polish-zh.md) for the full workflow.

## Commands and Units

```bash
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --section introduction
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --plan --unit 1.1.1
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --unit 1.1.1 --revised revised.tex
uv run python $SKILL_DIR/scripts/polish_unit_zh.py main.tex --verify --original original.tex --revised revised.tex --terms terms.json --max-growth 0.20 --json
```

Replace `$SKILL_DIR` with the installed skill directory. `--plan` and `--verify` are mutually exclusive. Verification requires `--revised` and exactly one of `--unit` or `--original`. For a single-chapter entry, use `--first-chapter N` to declare its actual chapter number, following the subsection-context cursor.

- A `subsection` is a depth-3 subsection relative to the heading tree, including its existing heading line; it is not tied to a particular LaTeX command. Numbering follows [logic](logic.md).
- Without depth-3 headings, list only `paragraph` units; do not fall back to depth-2. Paragraph IDs have the form `introduction#3`.
- The list contains only IDs, types, titles, source line ranges, approximate length, and read-only context coordinates, never body text. `prev.tail`, `parent_lead`, `next.head`, or the neighboring natural paragraphs remain read-only.
- Mark subsections exceeding 1200 visible Han characters for splitting and list their internal paragraph units. Rewrite and verify paragraph by paragraph; do not combine them into a chapter replacement. Run `--plan` again before each rewrite to avoid stale line numbers.

## Verification Codes and Tiers

| Code | Scope | Tier / Severity / Priority |
| --- | --- | --- |
| `UP-SCOPE` | Added, removed, or changed heading commands/text; new input/document structure commands; newly copied exact first-sentence substring from read-only context (at least 12 Han characters). Unchanged headings and repetitions already in the source are exempt | A / Error / P1 |
| `UP-CITE` | Citation-key multiset changes | A / Error / P1 |
| `UP-REF` | Target-multiset changes for `\ref` / `\eqref` / `\autoref` / `\cref` / `\pageref`, including initial-capital and starred forms | A / Error / P1 |
| `UP-LABEL` | Label-set changes | A / Error / P1 |
| `UP-MATH` | Math-content multiset changes after whitespace normalization | A / Error / P1 |
| `UP-NUM` | Multiset changes in visible-body numbers, percentages, scientific notation, and value/unit tokens | A / Error / P1 |
| `UP-TOKEN` | Set changes in digit-bearing identifiers, uppercase hyphenated names, and all-caps abbreviations | B / Warning / P2 |
| `UP-TERM` | User-term count changes; not checked without a term file | B / Warning / P2 |
| `UP-STRENGTH` | Claim-strength and hedge count changes with context; any suspected direction is for review, not a semantic judgment | B / Warning / P2 |
| `UP-NEG` | Negation-marker count changes (uncalibrated heuristic) | B / Info / P3 |
| `UP-LENGTH` | Visible Han-character growth or reduction exceeds the ratio threshold | B / Info / P3 |

`UP-CITE` recognizes `\cite`, `\citep`, `\citet`, `\upcite`, and biblatex's `\parencite`, `\autocite`, `\textcite`, `\footcite`, `\footcitetext`, `\smartcite`, and `\supercite`; it also recognizes `\cites` and the plural `s` forms of those biblatex commands. Initial capitals, stars, per-group `[前注][后注]{键}`, and multicite `(全局前注)(全局后注)` are supported. Keys from all groups are compared as one multiset. Custom macros are not expanded, and arbitrary command names containing `cite` are not treated as citations.

`--max-growth` defaults to `0.20` and checks both growth and shortening. The threshold is uncalibrated; it is neither a false-positive rate nor a quality score. `--terms` reuses the custom-term JSON from [consistency](consistency.md): `{"zh": [["软测量", "软传感器"]], "en": [["MAE", "mean absolute error"]]}`. Groups are flattened to protect each term separately, not to authorize synonym replacement.

Before counting, `UP-STRENGTH` skips term spans explicitly listed in `--terms`, so that “支持” inside “支持向量机” is not treated as a claim word. `UP-TERM` still reports term-count changes, and strength words outside those spans remain checked. Unconfigured terminology and ordinary phrases such as “相关研究” can still produce candidates. Review their reported context; a count change alone does not establish semantic drift.

Tier A reports determinate differences; tier B reports review candidates without replacement text. Each `[Script]` finding carries only `Meaning-Check: NEEDS-LLM` and no `Risk-Flags` line. Visible-text parsing cannot cover every number inside template macros; causality, scope, and terminology semantics still require human or LLM review.

## Exit Codes and Rewrite Contract

`--plan` exits 0, including no-depth-3 and unmatched-section statements; its text report lists units without a verification verdict. `--verify` exits 1 when an Error exists and 0 otherwise; argument errors exit 2. The verdict is `BLOCK` or `PASS-SCRIPT`. Even zero findings carry `NEEDS-LLM`; they do not establish semantic preservation.

The four-field contract applies only to this module's `[LLM]` rewrites. `[Script]` must never claim `PRESERVED`; an `[LLM]` claim of `PRESERVED` remains a proposal for author review. Follow the [routing contract](routing-rules.md):

```latex
% POLISH (source.tex:L10-L14) [Severity: Info] [Priority: P3] [LLM]: 单元润色提案
% Changed:       <实际改动>
% Protected:     <受保护内容>
% Meaning-Check: <PRESERVED | NEEDS-LLM>
% Risk-Flags:    <none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim>
```

Use the strength ladder in [over-claim-guard.md](../writing/over-claim-guard.md) to preserve the original claim strength without unauthorized strengthening or weakening. A script candidate does not authorize stronger wording.

## Boundaries with Existing Modules

- [expression](expression.md) owns colloquialisms, grammar, punctuation, value/unit notation, and individual sentence length; [deai](deai.md) owns padding, structural shells, and sentence-length uniformity. Reuse only their pre-rewrite diagnoses.
- [claim-forward](claim-forward.md) owns claim placement, self-weakening, and disclaimers. This workflow preserves original strength and only permits relocating limitations within the unit, never deleting limitations or adverse results.
- [logic](logic.md) owns subsection cursors, read-only windows, paragraph arcs, and argument structure. This module only changes sentences and wording, never paragraph order or the claim inventory. Edit axes retain their existing meanings; the script accepts no edit-axis arguments.
- [consistency](consistency.md) owns thesis-wide terminology consistency; this module only compares user-term counts between original and rewritten text.
