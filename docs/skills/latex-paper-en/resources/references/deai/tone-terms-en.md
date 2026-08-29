# AI Tone Terms (English) — Reference

This document lists the English vocabulary patterns most associated with
AI-generated academic prose, with a provisional per-10,000-word occurrence
budget. The companion file `tone-thresholds.yaml` is the authoritative
source consumed by `deai_check.py`.

## How thresholds are enforced

- `deai_check.py` reads `tone-thresholds.yaml` at startup.
- Each word in `term_thresholds:` triggers a `[Script] LOW` trace once its
  visible-word density exceeds the listed value.
- Ordinary terms are case-insensitive and word-boundary matched against visible prose
  (citations, refs, math, comments, figures, tables, and algorithms are stripped first).
  Entries in `sequence_terms` are the exception: only lowercase standalone words count;
  uppercase/title-case forms and hyphenated compounds are excluded.
- C3 sets `threshold_unit: per_10k_words`. Each legacy absolute cap `A` was converted to `2A`
  per 10,000 visible words, preserving the allowance only at the 5,000-word baseline. Other
  lengths intentionally scale. This is a baseline conversion, not corpus calibration.
- A corpus of 5-10 target-venue papers is still required. English density precision, transfer,
  and the borrowed organization factor remain **UNVERIFIED**. A legacy custom YAML without
  `threshold_unit` keeps absolute semantics and emits an upgrade notice.
- Override by editing the YAML; this MD file is documentation only.

## Maintenance cadence (this list is a snapshot, not a final state)

This word list captures _current_ AI-tone tells, not a permanent truth. As words
such as `delve` and `pivotal` get widely named, careful authors filter them and
their frequency drops, while new AI-preferred words keep emerging. Re-check this
list roughly every 6 months against excess-vocabulary research and prune or add
accordingly — do not treat it as frozen.

- Last reviewed: 2026-08-29; next review: 2027-02
- Sources: Kobak et al., _Sci. Adv._ 2025; Geng & Trotta 2025

## High-frequency AI vocabulary

These words are not banned. They are useful when used sparingly. The
threshold is the point at which a reviewer is likely to flag the writing
as templated.

| Word          | Threshold | Why it matters                                                   |
| ------------- | --------- | ---------------------------------------------------------------- |
| significant   | 10        | Often hides missing effect size or p-value                       |
| comprehensive | 6         | Marketing language; rarely earned by a single study              |
| effective     | 10        | Cheap claim without baseline comparison                          |
| novel         | 8         | Reviewers discount the word unless the novelty is named          |
| robust        | 8         | Needs the perturbation / noise level that justifies the claim    |
| important     | 10        | Replace with what is at stake                                    |
| various       | 10        | Vague quantifier; usually fixable with a number                  |
| several       | 10        | Vague quantifier                                                 |
| numerous      | 6         | Vague quantifier; almost always replaceable with a count         |
| furthermore   | 6         | Padding connector; often signals a content-free addition         |
| moreover      | 6         | Padding connector                                                |
| notably       | 6         | "Notably" is rarely needed when the content is genuinely notable |
| remarkable    | 6         | Editorial language; let the data carry the claim                 |
| remarkably    | 6         | Same as above                                                    |
| obvious       | 6         | Over-confident hedge                                             |
| obviously     | 6         | Over-confident hedge                                             |
| clearly       | 8         | Over-confident hedge                                             |

## Burstiness (paragraph opening repetition)

When three or more consecutive paragraphs begin with the same two opening
tokens, the script emits a `burstiness` trace. Typical offenders:

- "We propose ..." / "We propose ..." / "We propose ..."
- "In this ..." / "In this ..." / "In this ..."
- "Furthermore, ..." / "Furthermore, ..." / "Furthermore, ..."

The remedy is to rewrite at least one opener with a different syntactic
shape (subordinate clause, prepositional phrase, contrastive connector).

## Throat-clearing phrases

Phrases that occupy the first sentence of a paragraph without delivering
information. The default pattern set covers:

- `In order to better ...`
- `In this section, we ...`
- `It is worth noting that ...`
- `It should be noted that ...`
- `As mentioned earlier ...`
- Leading discourse markers: `Notably,`, `Furthermore,`, `Moreover,`, `In summary,`, `To summarize,`

The English configuration uses 2.0 hits per 10,000 visible words with
`min_budget: 1` and reports only later hits, including the total hit count,
budget, and global occurrence number. The value preserves the legacy allowance
only at 5,000 words and is not English-corpus calibration.

## Punctuation patterns

- More than `max_em_dashes_per_doc` em-dashes (`---` or `—`) across the
  document → one aggregate trace at the first occurrence.
- Any `!` in body sections (abstract through conclusion) → one trace per
  occurrence. Inline code, math, and comments are excluded.

## Out of scope

The following are intentionally NOT enforced here:

- Sentence-level grammar (handled by `analyze_grammar.py`).
- Citation density (handled by `verify_bib.py`).
- Section structure (handled by `check_format.py`).
- Domain-specific terminology, which lives in `forbidden-terms.md`.
