# Implementation Plan: latex-paper-en

## Phase 0: Review Gate

- [ ] Confirm the scope is still limited to corpus expansion and minimal trigger wording changes.
- [ ] Confirm no new module names are required.
- [ ] Keep the task in planning until the PRD and design are reviewed.

## Phase 1: Corpus Expansion

- [ ] Update `academic-writing-skills/latex-paper-en/evals/evals.json`.
  - Add higher-signal prompts for:
    - Introduction funnel / blueprint.
    - Related-work synthesis and gap derivation.
    - Method motivation -> design -> advantage.
    - Experiments / discussion takeaways, ablation, robustness.
    - Conclusion closure and claim-evidence self-review.
    - Figure / caption / venue narration.
  - Keep each prompt distinct and tied to a single writing capability.
- [ ] Update `academic-writing-skills/latex-paper-en/evals/trigger_eval.json`.
  - Add positive near-neighbors for writing-plan work.
  - Add negative near-neighbors for audit / thesis / Typst / translation / citation-search / from-scratch drafting.
  - Keep the prompts realistic and hard enough that a naive keyword match would be unreliable.

## Phase 2: Boundary Check

- [ ] Review whether any prompt wording suggests a missing trigger boundary in `SKILL.md`.
- [ ] If needed, make the smallest possible wording fix only.
- [ ] Do not add new abstractions or shared helpers.

## Phase 3: Validation

Run:

```bash
uv run pytest tests/test_skill_contracts.py tests/test_trigger_evals.py tests/test_skill_versions.py
git diff --check
```

If a failure points to a boundary problem, fix the smallest prompt or wording issue and rerun the same checks.

## Rollback Points

- If a prompt drifts into generic proofreading, rewrite it so it needs section-level reasoning.
- If the trigger set over-fires on adjacent tasks, tighten the negative near-neighbors first.
- If the eval set becomes redundant, merge overlapping prompts rather than adding more volume.
