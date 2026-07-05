# Research Notes

## Source Skill: `ref/rnskill`

Read files:

- `ref/rnskill/README.md`
- `ref/rnskill/README.zh.md`
- `ref/rnskill/skills/renhua/SKILL.md`
- `ref/rnskill/skills/renhua/agents/openai.yaml`

`renhua` is not a general academic editor. It is a Chinese AI/tech public-writing
editor whose main strength is identifying AI-flavored rhetorical shells before
polishing words. Its highest-value transferable ideas are:

1. Preserve before changing: facts, numbers, model/product names, test conditions,
   technical terms, author judgment, and uncertainty.
2. Separate source material into buckets before rewriting.
3. Delete empty framing and structure shells before word-level polishing.
4. Run a final scan for recurring AI shells.
5. In audit mode, quote the trigger phrase and name the pattern.

Important non-transferable parts:

- Default “revised text only” is unsafe for academic workflows; this repository
  should default to findings or rewrite blueprints.
- Public-writing paragraphs, first-person experience, roughness, and no-list/no-table
  style are not generally appropriate for theses or journal papers.
- “Hard bans” should become academic review findings, not absolute deletions,
  because real academic contrast and enumeration can be legitimate.

## Current Repository Surface

Relevant files inspected:

- `academic-writing-skills/latex-paper-en/SKILL.md`
- `academic-writing-skills/latex-paper-en/references/modules/deai.md`
- `academic-writing-skills/latex-paper-en/references/deai/guide.md`
- `academic-writing-skills/latex-paper-en/scripts/deai_check.py`
- `academic-writing-skills/latex-thesis-zh/SKILL.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/deai.md`
- `academic-writing-skills/latex-thesis-zh/references/deai/guide.md`
- `academic-writing-skills/latex-thesis-zh/scripts/deai_check.py`
- `academic-writing-skills/typst-paper/SKILL.md`
- `academic-writing-skills/typst-paper/references/modules/DEAI.md`
- `academic-writing-skills/typst-paper/references/DEAI_GUIDE.md`
- `academic-writing-skills/typst-paper/scripts/deai_check.py`
- de-AI evals and contract tests under `academic-writing-skills/*/evals/` and `tests/`

Existing strengths:

- All three main writing skills route to a `deai` module.
- Existing scripts already protect syntax and visible prose boundaries.
- Current checks cover empty phrases, overconfidence, vague quantification,
  template openings, low information density, repeated paragraph openings,
  throat-clearing leads, punctuation, overclaim phrases, and tense signals.
- `--tier light|medium|heavy` adds D1-D5 labels for readability-oriented analysis,
  not detector evasion.
- Chinese thesis docs already state policy boundaries and warn against treating
  de-AI as a detection guarantee.

Gap against `renhua`:

- The repository catches many vocabulary-level and paragraph-level markers, but
  not enough structure-shell markers: binary contrast shells, fake insight markers,
  lecture-colon openings, vague placeholders, vague comparatives, wrong time stance,
  and slogan endings.
- Current instructions say “increase information density,” but they do not yet
  force an academic preflight that preserves claim-evidence-logic before shell removal.
- Chinese thesis has the clearest need and best fit. English paper should borrow
  the workflow principle, not the Chinese phrase list.

## Adaptation Principle

Use `renhua` as a pattern-extraction source, not as a style target.

Academic version:

```text
source paragraph
-> protect syntax and citations
-> extract facts / claims / logic / boundaries
-> flag AI shells and low-information moves
-> propose source-preserving rewrite blueprint
-> only draft prose when explicitly requested
```

The resulting prose should sound like a careful researcher, not like a social
media post and not like a generic model-generated paragraph.

## Recommended Implementation Shape

User-selected scope: cover all three writing skills in one pass.

1. Update `latex-thesis-zh` de-AI guide/module docs and script checks with Chinese
   structure-shell categories adapted from `renhua`.
2. Add thesis tests and evals for “在保持学术逻辑和规范的前提下降低 AI 味”.
3. Update `typst-paper` docs, script checks, tests, and evals for Chinese/bilingual
   structure-shell awareness while preserving Typst syntax.
4. Update `latex-paper-en` docs, script checks, tests, and evals with English
   rhetorical-scaffold equivalents and claim-evidence-first workflow.
5. Sync docs mirrors and run a tri-skill verification set before `just ci`.

Follow-up only if duplication becomes painful:

- Factor shared bilingual shell patterns only after duplication appears in at least
  two scripts and the tests prove stable behavior.
- Consider a shared reference note under each skill's own `references/deai/`
  rather than introducing a new top-level package.

## Risks

- Over-flagging legitimate academic contrast, e.g. “不是 A，而是 B” when it is the
  actual research distinction. Mitigation: phrase findings as review targets and
  prefer “name the contrast axis and evidence” over “delete always.”
- Making users think de-AI equals detector evasion. Mitigation: preserve current
  policy boundary and disclosure language.
- Scope creep across three skills. Mitigation: keep one shared contract, but
  implement locally in the order thesis-zh -> typst-paper -> latex-paper-en and
  require tests after each surface.
- Adding style rules that fight academic norms. Mitigation: keep the rewrite order
  as logic/evidence -> structure shell -> sentence rhythm -> words.
