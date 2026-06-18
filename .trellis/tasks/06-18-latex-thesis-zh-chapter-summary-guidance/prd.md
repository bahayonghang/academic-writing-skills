# Optimize latex-thesis-zh chapter summary guidance

## Goal

Improve `academic-writing-skills/latex-thesis-zh` so chapter-summary requests
for Chinese degree theses route to the existing thesis writing workflow and
produce the compact "本章小结" style shown in the user-provided Yanshan University
sample: one coherent prose paragraph that summarizes the chapter's problem,
method path, key work, evidence/results, and transition value, instead of
expanding into several generic paragraphs.

## Confirmed Facts

- The current `latex-thesis-zh` skill already supports chapter structure,
  chapter introductions, method/experiment chapter logic, and thesis-level
  conclusion closure.
- `references/writing/thesis-writing-guide.md` has detailed guidance for
  "正文章引言（承上启下两段式）" but no matching subsection for "本章小结".
- `references/writing/structure-guide.md` recommends a chapter structure ending
  in "本章小结", but does not constrain summary length, paragraph count, or
  rhetorical shape.
- `SKILL.md` routing rules mention chapter introductions and chapter-level
  rewrites, but do not explicitly route "本章小结/章节小结/章末小结" requests.
- The docs mirrors under `docs/skills/latex-thesis-zh/` and
  `docs/zh/skills/latex-thesis-zh/` duplicate the same writing references and
  must be kept in sync if the source reference changes.
- The current eval set has coverage for heading architecture, chapter
  introductions, method mainline, experiment discussion, and conclusion closure,
  but no eval that asserts a one-paragraph "本章小结" answer.

## Requirements

- Add an explicit "本章小结" writing contract to `latex-thesis-zh` without
  creating a new English-paper-style `section-writing` module.
- Route user requests containing "本章小结", "章节小结", "章末小结", or "小结写法"
  through the existing `logic` / thesis-writing guidance path.
- Define the default output shape as one natural paragraph, not a bullet list
  and not several short paragraphs, unless the user or school template asks for
  another form.
- The paragraph should summarize, in order, the chapter problem or evaluation
  target, the method/work performed, the key mechanisms or evidence, and how
  the chapter supports the next chapter or final conclusion.
- Preserve LaTeX macros, citations, labels, references, math environments, and
  source claims. Do not invent data, comparisons, or conclusions.
- Document how chapter summaries differ from the final "结论/总结与展望": chapter
  summaries are local evidence summaries; the final conclusion is the overall
  thesis-level synthesis and should not repeat "第 X 章..." mechanically.
- Update source references and docs mirrors consistently.
- Add eval/trigger coverage so future changes cannot regress this behavior.

## Out of Scope

- Implementing a full deterministic summary-generation script.
- Rewriting user thesis chapters in this planning phase.
- Adding a new public module to `latex-thesis-zh`.
- Changing school-specific templates beyond referencing existing generic and
  Yanshan guidance boundaries.

## Acceptance Criteria

- [ ] `latex-thesis-zh/SKILL.md` explicitly routes chapter-summary requests to
      the existing thesis writing guidance path.
- [ ] `references/writing/thesis-writing-guide.md` contains a "本章小结" section
      with paragraph-count, content-order, and safety constraints.
- [ ] `references/writing/structure-guide.md` and both docs mirrors mention the
      same summary contract, not only the existence of a "本章小结" section.
- [ ] `evals/evals.json` includes at least one realistic prompt for writing or
      checking a chapter summary, with assertions for "one paragraph/compact
      prose", core components, and no fabricated citations.
- [ ] `evals/trigger_eval.json` includes should-trigger examples for
      chapter-summary wording and preserves near-miss negatives for non-thesis
      or English-paper contexts.
- [ ] Targeted validation passes for skill contracts, trigger evals, and the
      latex-thesis-zh script/eval tests affected by documentation or routing.
