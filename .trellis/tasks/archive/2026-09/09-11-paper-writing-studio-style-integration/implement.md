# Implementation Plan

## Preconditions

This task is planning-only until the latest planning summary is explicitly approved. Before `task.py start`, resolve the unspecified-venue decision and re-read `prd.md`, `design.md`, this file and the source package contracts. Do not modify the three source material trees.

## Ordered work

1. **Freeze the interface.** Create the package root, `SKILL.md`, `agents/interface.yaml`, README and a profile manifest. Encode selector precedence, section aliases, default output and exclusions.
2. **Build the shared core.** Add only evidence/permission invariants supported across sources: protected-token preservation, calibrated claim strength, candidate/core filtering, degraded status, summary normalization and deterministic em-dash handling where applicable.
3. **Add isolated profiles.** Define Nature, IEEE, Elsevier and unspecified load plans. Reference source prompt/reference/TSV locations without merging rows. Encode only documented profile rules and dated provenance.
4. **Add multi-section orchestration.** Reuse Nature's shared-context/entity-registry idea behind a profile interface. Keep section order, citation rhythm and self-reference local to each profile.
5. **Add eval artifacts.** Write `evals/trigger_cases.json` and output cases for all three profiles, unspecified fallback, explicit-venue/journal conflict, section aliases, candidate rows, protected values and degraded sections. Add `reports/skill-ir.json`, generated trigger report and output evidence after implementation exists.
6. **Synchronize public surfaces.** Update only the relevant resource manifest, README mirrors and docs pages if the repository's sync checker proves they are required. Keep materials knowledge packs out of install catalogs.
7. **Verify and review.** Run `validate_skill.py`, trigger/output evals, `export_skill_ir.py`, resource sync, focused tests, then `just check-versions`, `just lint`, `just typecheck`, `just test` and docs build according to changed scope. Run `release_check.py --phase local --run-tests` only after package tests exist.
8. **Independent gate.** Perform a `trellis-check` review against source paths and acceptance criteria. Classify real-paper, provider, install and human-review claims as `missing evidence`.

## Validation matrix

| Gate | Command / evidence | Pass condition |
|---|---|---|
| package shape | `python .agents/skills/qiaomu-meta-skill/scripts/validate_skill.py academic-writing-skills/paper-writing-studio` | frontmatter, root isolation and interface pass |
| triggers | `trigger_eval.py ... --cases evals/trigger_cases.json` | venue positives and exclusions pass |
| IR | `export_skill_ir.py ...` | input/output/profile/evidence boundaries exported |
| output | profile fixtures + protected-token diff | no fabricated token; summary and degraded fields are correct |
| source isolation | `git diff -- ref/nature-writing-studio materials/IEEE materials/Elsevier` | empty |
| project checks | `just check-versions`, `just lint`, `just typecheck`, `just test` | pass or separately reported baseline failures |
| docs/resources | `uv run python docs/scripts/check_resource_sync.py`, `just doc-build` | pass when public surfaces changed |

## Ownership and rollback points

- Core child owns router and normalized contract.
- Venue-profile child owns adapters and profile references; it starts after the core contract is approved.
- Evals/docs child owns evals, interface/README, reports and sync checks.
- Roll back each child by its owned paths; never revert another child's edits or the read-only source materials.
