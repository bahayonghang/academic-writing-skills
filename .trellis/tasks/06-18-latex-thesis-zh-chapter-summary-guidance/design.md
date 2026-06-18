# Design

## Boundary

This task changes the `latex-thesis-zh` skill's guidance and eval coverage. It
does not add a new module, shared library, or script. The existing `logic`
route remains the right entry point because "本章小结" is a chapter-level
coherence and thesis-writing issue, not a separate paper-section subsystem.

## Files To Change

- `academic-writing-skills/latex-thesis-zh/SKILL.md`
  - Add trigger/routing language for "本章小结/章节小结/章末小结/小结写法".
  - Update capability/example wording if needed, staying within frontmatter
    description length constraints.
- `academic-writing-skills/latex-thesis-zh/references/writing/thesis-writing-guide.md`
  - Add the source-of-truth chapter-summary section.
- `academic-writing-skills/latex-thesis-zh/references/writing/structure-guide.md`
  - Cross-link the new summary guidance from the existing recommended chapter
    structure and checklist.
- Docs mirrors:
  - `docs/skills/latex-thesis-zh/resources/writing/thesis-writing-guide.md`
  - `docs/zh/skills/latex-thesis-zh/resources/writing/thesis-writing-guide.md`
  - `docs/skills/latex-thesis-zh/resources/writing/structure-guide.md`
  - `docs/zh/skills/latex-thesis-zh/resources/writing/structure-guide.md`
- Eval metadata:
  - `academic-writing-skills/latex-thesis-zh/evals/evals.json`
  - `academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json`

## Contract

When asked to write or check a "本章小结", the skill should:

1. stay in `latex-thesis-zh` and prefer the `logic` route plus
   `references/writing/thesis-writing-guide.md`;
2. default to one coherent prose paragraph;
3. summarize chapter-local problem, work/method, evidence/result, and thesis
   mainline value;
4. keep claims source-bound and mark missing evidence;
5. avoid final-conclusion repetition, outline-style "第 X 章..." lists, and
   multi-paragraph expansion unless explicitly requested.

## Compatibility

- Existing chapter-introduction, heading-architecture, method, experiment, and
  conclusion-closure guidance must keep their current route.
- No command-table row should advertise a new script option unless that option
  exists in `--help`; tests check router command hygiene.
- Docs mirrors should be textually aligned with source references where those
  references are mirrored today.

## Tradeoffs

- A hard "exactly one paragraph" instruction could conflict with schools or
  advisors that require numbered findings. The safer default is "one paragraph
  unless the source/user/template asks otherwise".
- A deterministic checker for paragraph count is possible but out of scope for
  the requested planning pass. Eval assertions are enough for this guidance
  optimization.
