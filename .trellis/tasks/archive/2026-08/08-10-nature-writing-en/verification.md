# Verification — 08-10-nature-writing-en

## Behavioral Route Eval

Evaluation method: deterministic inspection of the trigger and exclusion rules in
`references/modules/routing-rules.md`. This is local contract evidence, not a provider-backed
model evaluation.

| Case | Prompt | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| Positive | `把我的 Results 改成期刊式叙事` | Load `references/writing/article-architecture.md` | Prompt matches `Results` / `期刊式`; the route points to the architecture reference. | PASS |
| Negative | `润色我的 NeurIPS 摘要语法` | Do not load `references/writing/article-architecture.md` | Prompt has no journal-architecture trigger; the route explicitly excludes ordinary grammar and conference-abstract polishing. | PASS |

Command result: `PositiveRoutesToArchitecture=True` and
`NegativeSkipsArchitecture=True`.

## Resource And Build Evidence

- `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`:
  PASS, 258 manifest entries.
- `uv run python docs/scripts/check_resource_sync.py --skill latex-paper-en`:
  PASS, 258 manifest entries.
- `uv run python docs/scripts/check_resource_sync.py`: PASS, 258 manifest entries.
- `just doc-build`: PASS, VitePress build completed.
- Focused pre-manifest gate: 1403 tests passed; the two failures were the expected missing/stale
  resource-manifest checks before regeneration.
- Post-sync focused gate
  `uv run --extra dev python -m pytest tests/contracts/ tests/skills/ -q`: PASS,
  1405 tests passed in 119.28 seconds.
- Manifest zero-drift check: PASS. SHA-256 remained
  `8EF1904F41BD02A39844BBA06F741F41765D4B6C562A346BA24B980E9A9408DA` after regeneration.

## Scope And Non-Increment Decisions

- `git diff --stat -- academic-writing-skills/latex-paper-en/scripts` produced no output.
- `analyze_abstract.py`, `optimize_title.py`, and `check_tables.py` were not modified.
- Existing table checks for `booktabs`, rule commands, caption placement, notes, and numeric
  precision remain the owners of those rules. This task adds only the non-mandatory direction-marker
  documentation.
- Delta items N6, N8, N9, N10, N12, N13, N14, and N18 remain rejected and were not duplicated.
- No content was added to `paper-audit`.

## Evidence Limits

- Provider-backed routing/output evaluation: **UNVERIFIED / missing evidence**. No provider call was
  authorized or run.
- Precision, recall, or writing-quality impact on real papers: **UNVERIFIED / missing evidence**.
  No real-paper corpus evaluation was run.
- The integrated guidance remains community-derived, Nature-leaning rhetoric. It is not verified as
  official Nature policy.

## Final Validation

- `just ci`: PASS.
  - Skill-version alignment: 1 test passed.
  - Ruff format: 183 files already formatted.
  - Ruff lint: all checks passed.
  - Pyright: completed with pre-existing warnings in untouched scripts.
  - Pytest: 1497 tests passed in 117.45 seconds.
- `git diff --check`: PASS.
- Final full resource check: PASS, 258 manifest entries.
- Final script diff and status checks: no changes under
  `academic-writing-skills/latex-paper-en/scripts`.
