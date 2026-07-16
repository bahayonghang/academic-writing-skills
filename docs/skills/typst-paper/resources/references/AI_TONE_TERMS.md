# AI Tone Terms (Bilingual, Typst) — Reference

The Typst template is shared by Chinese and English bilingual papers. This file records two sets of high-frequency word lists and trigger instructions at the same time.
Supporting threshold file`AI_TONE_THRESHOLDS.yaml`yes`deai_check.py`The authoritative configuration actually read.

## Threshold Validation Method

- `deai_check.py`Read on startup`AI_TONE_THRESHOLDS.yaml`。
- In `term_thresholds:`:
  - key All ASCII letters → Count by word boundary (case insensitive).
  - key contains non-ASCII characters → count directly by substring.
- Each over-threshold word triggers a `[Script] LOW` trace.
- Thresholds are only changed in yaml; this MD is for illustration only.

## Maintenance cadence (snapshot, not a final state)

These term lists capture *current* AI-tone tells, not a permanent truth. As words
such as`delve` / `pivotal`(and "enabling" and "manifesting" in Chinese) get widely named, careful authors
filter them and their frequency drops, while new AI-preferred words keep emerging.
Re-check roughly every 6 months against excess-vocabulary research; prune or add
accordingly rather than treating the list as frozen.

- Last reviewed / Last review: 2026-06
- Sources / Source: Kobak et al., *Sci. Adv.* 2025; Geng & Trotta 2025

## English

|Word|Threshold|Why it matters|
|---------------|-----------|------------------------------------------------------------------|
|significant| 5         |Often hides missing effect size or p-value|
|comprehensive| 3         |Marketing language; rarely earned by a single study|
|effective| 5         |Cheap claim without baseline comparison|
|novel| 4         |Reviewers discount the word unless the novelty is named|
|robust| 4         |Needs the perturbation / noise level that justifies the claim|
|important| 5         |Replace with what is at stake|
|various| 5         |Vague quantifier; usually fixable with a number|
|several| 5         |Vague quantifier|
|numerous| 3         |Vague quantifier|
|furthermore| 3         |Padding connector|
|moreover| 3         |Padding connector|
|notably| 3         |Editorial framing|
|obviously| 3         |Over-confident hedge|
|clearly| 4         |Over-confident hedge|

## Chinese

|word|threshold|Remark|
|--------|------|--------------------------------|
|first| 4    |Discussion opening template|
|Secondly| 4    |paired with "first"|
|However| 5    |turning abuse|
|therefore| 6    |Can keep more|
|obviously| 3    |The more natural, the less necessary|
|Significantly| 5    |Often lacks quantitative support|
|comprehensive| 3    |It is difficult to "comprehensive" a single study|
|go deep| 3    |marketing language|
|important| 5    |Explain clearly what "important" means|
|key| 5    |Same as above|
|core| 4    |A paper should not have too many "cores"|

## Burstiness (repetition at the beginning of paragraph)

Fires when 3 consecutive paragraphs start with the same first 8 characters. The 8-character setting covers both Chinese and English:

- "Furtherm..." / "Furtherm..." / "Furtherm..." (English)
- "First of all, I..." / "First of all, I..." / "First of all, I..." (Chinese)

Fix: Rewrite at least one paragraph to use a different syntax.

## Throat clearing

There are about 10 first phrases in the English and Chinese segments each, and one hit will be credited with `[Script] LOW`.
See `AI_TONE_THRESHOLDS.yaml` for a complete list.

## Punctuation

- full text`—` / `---`The total exceeds`max_em_dashes_per_doc`→ Record an aggregation trace at the first occurrence.
- Appears in the main text section`!`or`！`→ Record one trace at a time.

## Out of scope

- Syntax syntax (covered by editor self-test).
- Reference density (overridden by `verify_bib.py`).
- Chapter structure (covered by `check_format.py`).
- Protected terms and mathematical environments (see the SKILL.md / FORBIDDEN_TERMS.md style chapter).
