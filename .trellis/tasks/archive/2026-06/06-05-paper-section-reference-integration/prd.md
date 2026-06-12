# Integrate paper section writing references

## Goal

Improve `academic-writing-skills/latex-paper-en` by integrating the
section-specific writing strategy from
`ref/Research-Paper-Writing-Skills/research-paper-writing/references`, so an
agent working on an existing English LaTeX paper can move beyond diagnostics
into reviewer-facing section planning, paragraph-role rewriting, flow checks,
and claim-evidence self-review.

Also determine whether `academic-writing-skills/latex-thesis-zh` should receive
a compatible but thesis-specific adaptation, rather than a direct transplant of
English conference-paper guidance.

## User Value

- English paper users get dedicated guidance for Abstract, Introduction,
  Related Work, Method, Experiments, and Conclusion instead of only broad
  `logic` / `literature` / `experiment` diagnosis.
- The existing LaTeX-safe workflow remains intact: preserve citations, labels,
  refs, math, macros, and source structure unless the user explicitly asks for
  prose proposals.
- Chinese thesis users can benefit from the transferable reasoning patterns
  (problem-to-gap funnel, paragraph role, claim-evidence closure, experiment
  discussion layering) without forcing conference-paper shapes onto degree
  theses.

## Confirmed Facts

- `research-paper-writing/SKILL.md` is a writing-strategy skill, not a LaTeX
  script workflow. It routes by paper section and asks the agent to build a
  mini-outline, rewrite paragraph-by-paragraph, run reverse outlining, check
  major claims against evidence, and use `paper-review.md` for adversarial
  self-review.
- The source reference set includes dedicated guides for `abstract`,
  `introduction`, `related-work`, `method`, `experiments`, `conclusion`,
  `paper-review`, paragraph flow, and a section-specific example bank.
- The source repository is MIT licensed and the README attributes most writing
  methodology to Prof. Peng Sida's public notes, with curation by Master-cai.
  If content is copied or closely adapted, attribution and license handling must
  be preserved.
- `latex-paper-en/SKILL.md` is already module-routed around existing `.tex`
  projects. It has modules for `compile`, `format`, `bibliography`, `grammar`,
  `sentences`, `logic`, `literature`, `expression`, `translation`, `title`,
  `figures`, `pseudocode`, `deai`, `experiment`, `tables`, `abstract`, and
  `adapt`.
- `latex-paper-en` already has some overlapping concepts:
  - `abstract` diagnoses a five-element abstract structure.
  - `logic` checks paragraph coherence, introduction funnel, related-work
    quality, cross-section closure, and motivation red-thread closure.
  - `literature` uses a `Consensus -> Disagreement -> Limitations -> Gap ->
    This paper` rewrite chain.
  - `experiment` checks baselines, ablations, significance, discussion depth,
    literature echo, and conclusion completeness.
- `latex-paper-en/evals/evals.json` and `trigger_eval.json` already include
  route/eval coverage for introduction logic, related-work synthesis,
  cross-section story alignment, experiments, discussion, pseudocode, and
  abstract-adjacent prompts.
- `latex-thesis-zh/SKILL.md` is a Chinese thesis workflow for existing `.tex`
  degree-thesis projects. It includes thesis-specific modules for template,
  structure, consistency, GB/T 7714 bibliography, logic, literature,
  experiment, tables, title, de-AI, and abstract.
- `latex-thesis-zh` already has thesis-specific guidance absent from the source
  English paper skill, especially heading lead-ins, chapter mainline, thesis
  structure, and Chinese academic style constraints.
- Contract tests require skill assets, module names in `SKILL.md`, `uv run
  python` command hygiene, description length bounds, eval file shape, trigger
  eval health, and router commands matching script help.
- Current worktree has unrelated uncommitted changes in `.gitignore` and
  `AGENTS.md`; this task must not overwrite or clean them.

## Requirements

1. Preserve existing skill identities and core scope:
   - keep `latex-paper-en` as the English LaTeX paper assistant for existing
     paper projects;
   - keep `latex-thesis-zh` as the Chinese LaTeX thesis assistant for existing
     degree-thesis projects.
2. Add section-writing capability to `latex-paper-en` without collapsing all
   writing tasks into the existing diagnostic modules.
3. Keep progressive disclosure: route to one section-writing reference at a
   time instead of loading the full source reference tree.
4. Preserve LaTeX safety boundaries:
   - do not fabricate citations, claims, metrics, baselines, or results;
   - preserve `\cite{}`, `\ref{}`, `\label{}`, custom macros, and math by
     default;
   - separate diagnosis from generated prose proposals.
5. Treat source guidance as writing methodology, not deterministic scripts.
   New section-writing guidance may be LLM-driven and need not add new scripts
   unless implementation discovers a repeated deterministic check.
6. Update evals and trigger evals so the new capability is testable and
   triggerable.
7. If copying or closely adapting source files, include license/attribution
   handling appropriate for the MIT source and upstream credits.
8. For `latex-thesis-zh`, adapt only the transferable concepts that fit Chinese
   thesis structure. Do not impose conference-paper section names or a
   submission-paper conclusion style where thesis norms differ.
9. First implementation slice scope is confirmed:
   - perform a deep `latex-paper-en` section-writing integration;
   - perform a light `latex-thesis-zh` thesis-specific adaptation through
     existing thesis modules and references.

## Likely Out of Scope

- Creating a brand-new standalone `research-paper-writing` skill in this repo.
- Running full skill-creator benchmark loops with subagents unless the user
  explicitly asks for evaluation beyond local contract tests.
- Deep external literature research or paper-specific citation fact checking.
- Rewriting the current script analyzers unless a small routing or contract
  change requires it.
- Broad docs-site redesign or unrelated README updates unless required by
  public skill inventory documentation.

## Acceptance Criteria

- [ ] Planning artifacts clearly decide the integration strategy for
      `latex-paper-en` and the adaptation scope for `latex-thesis-zh`.
- [ ] `latex-paper-en` has a discoverable section-writing route or module that
      covers Abstract, Introduction, Related Work, Method, Experiments, and
      Conclusion with one-section-at-a-time references.
- [ ] The `latex-paper-en` output contract for section writing includes a
      compact outline, paragraph roles, self-review checklist, and
      claim-evidence map while preserving LaTeX syntax.
- [ ] Existing diagnostic modules still route as before for compile, format,
      bibliography, grammar, de-AI, pseudocode, tables, and script-backed
      checks.
- [ ] `latex-thesis-zh` receives either a documented no-change decision or a
      bounded thesis-specific adaptation with Chinese thesis semantics.
- [ ] Evals cover at least introduction, method, conclusion, and one
      cross-section claim-evidence or paragraph-flow use case for the changed
      skill(s).
- [ ] Trigger evals include positive and near-miss negative prompts for the new
      writing route.
- [ ] Validation commands are run and recorded, at minimum targeted contract
      tests plus any script tests impacted by router changes.

## Open Questions

None blocking for the first implementation slice.

## Resolved Decisions

1. Use the recommended scope: full `latex-paper-en` section-writing integration
   plus light `latex-thesis-zh` adaptation.
2. Do not build an equally deep English-paper-style section-writing reference
   bank for `latex-thesis-zh` in this slice.
