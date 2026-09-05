# Module: Chinese Expression Check (expression)

**Trigger**: this passage is too colloquial, make it more academic, sentences too long and convoluted, punctuation is messy, colon or semicolon piling, wrong collocation, value/unit notation

**Rule source of truth**: [academic-style-zh.md](../writing/academic-style-zh.md); numbers and units are further covered by [number-unit-guide-zh.md](../formatting/number-unit-guide-zh.md).

## Commands

```bash
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --section 绪论
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --goal concision --strength moderate
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --max-chars 70 --json
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [routing-rules.md](routing-rules.md). `--goal coherence` has no rules here and routes to `logic`. `--tier` is unrelated to both: it is `deai` detection sensitivity.

## Boundaries: what this module does not do

Every cell already has an owner; rebuilding one guarantees a clash.

| Area | Owner | What this module does |
| --- | --- | --- |
| Person (we / this paper) | T-VOICE / T-OPEN in `abstract` | **No person checker at all**; T-VOICE only checks first person, T-OPEN checks whether the opening sentence locates the research object — different dimensions |
| Claim-strength grading | [over-claim-guard.md](../writing/over-claim-guard.md) | Lexical-level suggestions only (`E-ABSOLUTE`); strength grading is not reimplemented |
| Template-specific numeric rules | YS-36 in `spec-check` (decided as `llm`) | Generally decidable items only (spacing, upright units, numerals for approximations/ordinals); the final review goes to `spec-check` |
| Sentence-length uniformity (CV, AI fingerprint) | D1 in `deai` (requires `--tier`) | **Single-sentence readability length** only; uniformity is not here, and the two never report the same item |
| Paragraph order and argument | `logic` | Not touched |
| Conclusion / abstract skeleton | `conclusion` / `abstract` | Not touched |

## The nine checkers and their tiers

**A = auto** (decision is reliable, a replacement is offered) / **B = candidate** (report only, no replacement text).

| ID | Basis | Input region | Exclusions | Tier |
| --- | --- | --- | --- | --- |
| `E-COLLOQ` | style-zh §1.1 | Visible Chinese prose | "特别是" is the §3.4 recommended example connective, not reported | A |
| `E-ABSOLUTE` | style-zh §2 | Visible Chinese prose | Quoting someone else's position (`文献[N]`, `已有研究`, `前人研究`...) | B |
| `E-COLLOC` | style-zh §4.1 | Visible Chinese prose | "了/过" and a modifier of at most 6 characters may sit between verb and object, but never across punctuation | A |
| `E-INCOMP` | style-zh §4.2 | Sentences starting with 通过/经过/利用/借助/采用 | The sentence already carries a subject marker (本文, 本研究, 作者, 该方法...) | B |
| `E-PUNCT` | style-zh §5.3 | Lines containing Chinese characters | Inline English fragments, all-English brackets (the two §5.2/§5.3 exemptions), URLs/paths/filenames | B |
| `E-NUMSPACE` | style-zh §6.2 | "number + unit" in visible prose | Percent, per-mille, degrees, Celsius and other quantities the standard writes without a space | A |
| `E-UNITFONT` | style-zh §6.2 | **Inside math environments (read-only)** | Already wrapped upright with `\mathrm` / `\text` / `\si` | B (never fixed) |
| `E-NUMSTYLE` | style-zh §6.1 | Visible Chinese prose | Numbering after 图/表/式/章/节/条/页/卷/册/第 | B |
| `E-LONGSENT` | Readability | Visible Chinese prose, split on Chinese punctuation | Formula lines, table rows, enumerated items, environment lines | B |

**Why `E-INCOMP` cannot be tier A**: dropping a subject carried over from the previous sentence is legal and common in Chinese ("本文提出 X 方法。通过实验，验证了其有效性。" — omitting 本文 in the second sentence is entirely acceptable in a thesis). A rule can recognize the pattern but cannot decide whether the subject is genuinely missing.

**Why `E-PUNCT` cannot be tier A**: `academic-style-zh.md` §5.2/§5.3 themselves grant two exemptions for English punctuation. The exempt regions are implementable, but edge cases such as mixed Chinese-English compound brackets cannot be enumerated.

**Colons, semicolons, and inter-sentence logic in continuous prose are `[LLM]`-only**: see
[academic-style-zh.md §5.4](../writing/academic-style-zh.md#punctuation-prose)
for label-style colons and paragraph-long semicolon chains. This module handles sentence-level
expression and must infer relationships only from available evidence; paragraph order and argument
structure remain with `logic`. `E-PUNCT` still reports only the mixed-language punctuation covered
by §5.3, with no new rule, threshold, or check code.

**What makes `E-UNITFONT` special**: detection is reliable, but the problem lives inside a math environment, and "never modify math environments" is red line one. So it reports only and never offers replacement text, stating explicitly that the author must adjust it by hand. **The tier follows the red line, not the decision capability** — do not mistake it for something that can be promoted to A.

**The single-character verbs in style-zh §1.3 (用/做/看/想/试) are not implemented**: they are substrings of legitimate words such as 采用, 制作, and 看法, so a rule cannot decide them; they are llm-only. The `[LLM]` layer judges those replacements against the §1.3 table.

## Output shape

Tier A (a replacement is offered):

```latex
% EXPRESSION (chapters/chap03.tex:42) [Severity: Warning] [Priority: P2] [Script]: E-COLLOC 搭配不当
% 原文: 该策略有效增加了模型的效率。
% 建议: 该策略有效提高了模型的效率。
% 依据: academic-style-zh.md §4.1（增加效率 → 提高效率）
% Changed:       1 collocation fix (增加了模型的效率 -> 提高了模型的效率)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    lexical-substitution
```

Tier B (no "建议" line, only "候选"):

```latex
% EXPRESSION (chapters/chap03.tex:57) [Severity: Info] [Priority: P3] [Script]: E-INCOMP 疑似成分残缺
% 原文: 通过对比实验，验证了所提方法的有效性。
% 候选: 「通过/经过/利用…，<动词>了…」句式疑似缺主语；中文承前省略主语亦合法，请人工判断
% 依据: academic-style-zh.md §4.2（成分残缺）
% Changed:       none
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

## Rewrite contract

This module emits text that can directly replace the source, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and may set only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it stays a proposal for the author to verify. Field definitions and the `Risk-Flags` closed set: `references/modules/routing-rules.md`.

A rewrite must never raise claim strength. Swapping a hedged statement for a stronger assertion ("可能" → "能够", "有助于" → "显著提升") is an over-claim, not an improvement in expression: keep the original strength, or set `Risk-Flags: overstatement` and say so explicitly. Criteria: [over-claim-guard.md](../writing/over-claim-guard.md) — this module offers lexical-level suggestions only and does not reimplement strength grading.
