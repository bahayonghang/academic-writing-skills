# Implementation Plan: Formula Layout Guidance

## Assumptions

- The user wants a reviewed plan first, not immediate edits.
- The target skill is `academic-writing-skills/latex-thesis-zh`.
- Formula-layout advice belongs to the existing `format` pathway unless
  implementation evidence justifies a separate module.

## Checklist

1. Add formula layout reference
   - Create `academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md`.
   - Include the decision tree:
     - keep one-line formulas that fit;
     - split when width, margin, or equation-number displacement occurs;
     - align derivations at relation operators;
     - use grouped/cases structures for systems or constraints;
     - avoid changing independent formulas for symmetry.
   - Verify: reference contains the screenshot-specific rule and no absolute
     claim that only three cases can ever be split.

2. Wire the reference into existing guidance
   - Update `references/modules/format.md` to mention formula layout and point
     to `../formatting/formula-guide.md`.
   - Update `templates/generic.md` formula-numbering notes with the practical
     right-aligned-number check.
   - Optionally update `templates/thuthesis.md` only if wording can stay
     template-factual and not speculative.
   - Verify: links are relative and resolve from Markdown context.

3. Update `SKILL.md` routing
   - Add formula line breaking / equation number collision to Triggering.
   - Add a routing rule: formula layout questions use `format`; reference
     integrity questions about `\label`, `\eqref`, undefined references still
     use `references`; heading followed by formula still uses `logic`.
   - Add an example request matching "第一个公式编号挤到第二行，第二个公式不用动".
   - Verify: no new module row unless implementation intentionally creates one.

4. Add eval coverage
   - Add one eval to `academic-writing-skills/latex-thesis-zh/evals/evals.json`
     for the screenshot scenario.
   - Assertions should check for:
     - `format` route or formula-layout language;
     - equation number pushed to another line / width overflow;
     - leave the second formula unchanged;
     - no fabricated citation.
   - Consider updating `trigger_eval.json` only if formula-layout prompts should
     improve skill triggering.

5. Validate
   - Run a targeted JSON parse check for `evals/evals.json`.
   - Run any existing quick validator if present in this repo.
   - Run targeted pytest for skill contracts if available.
   - Run `just doc-build` if docs or generated catalog references change.
   - Run `just ci` if implementation touches shared tests or scripts.

## Review Gate Before Implementation

Do not run `task.py start` until the user approves this plan or asks to begin
implementation.

## Rollback Points

- If adding a new reference creates broken links, revert only the reference-link
  changes and keep the PRD/research artifacts.
- If eval updates conflict with existing schema, revert the eval entry and add a
  minimal prompt-only eval after inspecting the schema pattern.
