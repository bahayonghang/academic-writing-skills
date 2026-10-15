# Migration review — 2026-10-15

Status: PASS for the approved migration's local verification gates. No unresolved migration defect found. Optional/runtime limitations and the inherited out-of-scope observation remain explicit below.

## Findings fixed

- `tests/skills/latex_thesis_zh/test_thesis_rebuttal_{build,check,intake}.py`: fixture-name migration exceeded Ruff formatting limits. Applied Ruff formatting only; all original test functions retained.
- `docs/skills/latex-thesis-zh/index.md` and Chinese counterpart: Minimum Inputs still universally required a thesis entry file, contradicting the new review-only route. Scoped it to source modules and stated that review intake needs only PDF/TXT/MD reports.
- `tests/contracts/test_subsection_context_contract.py`: the historical metadata assertion still required 2026-09-20. Updated to the approved migration date 2026-10-15; version and route assertions remain.
- `tests/contracts/test_thesis_zh_guidance_fidelity.py`: the C6 assertion assumed eval 58 must always be last. Select that exact protected entry by ID, retaining sorted/unique IDs and all original output-content assertions. This allows the approved appended reply evals without dropping historical coverage.
- `tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py`: its exhaustive router smoke inventory lacked the three migrated reply CLIs. Added their real `--help` subprocess smokes; the separate installed tests run their full writable pipeline, avoiding writes into the shared source fixture. Targeted check: 4 passed, 50 deselected (`check-smoke-fixes.txt`).
- Main/implementer coordinated fixes: migrated intake's PyMuPDF text return typing, exact three-file thesis reference-layout contract, reply route expectations, and thesis Write/Edit metadata for the existing ledger-fill workflow. All are included in final passing CI.

## Findings not fixed

- Inherited limitation (P2, outside migration behavior changes): `rebuttal_common.load_thesis_numbers` preserves the old `check_deck.load_thesis_numbers` implementation exactly. It calls `tex_loader.assemble(main)` without the explicit thesis root and catches `ValueError`. A nested main that references an otherwise valid sibling subtree can therefore produce skipped R-NUM-SRC coverage. It does not read outside the loader boundary. Changing this would alter preserved behavior; recommend a separate scoped follow-up with nested-main and boundary-error regression cases.
- Generic Qiaomu package validation has the three pre-existing layout incompatibilities recorded by the main session. No ceremonial README/interface/manifest files were added to hide them.
- Five-tool sessions, provider-backed triggering, real thesis/reviewer data, and real XeLaTeX acceptance were not run. No such PASS is claimed.

## Review evidence

- `git diff 53c2ab5 -- academic-writing-skills/latex-defense-zh` is empty. Restored defense test conftest and entry test also match that baseline.
- Dependency review: reply scripts no longer import `extract_thesis` or `check_deck`. The five transplanted functions (`cn_to_int`, `read_group`, `skip_ws`, `normalize_digits`, `load_thesis_numbers`) have identical ASTs to their source implementations.
- All original reply test functions preserved: build 8, check 20, intake 12. The gate still has all 16 R-* checks, a clean synthetic case and negative-code cases. The four new installed/ownership tests exercise isolated thesis copies, external cwd, cleared PYTHONPATH, local imports, readonly input hashes, real synthetic Git evidence, and explicit review-only skips.
- Public resource scan found no erroneous defense reply command/link. Historical CHANGELOG entries intentionally remain. Current Chinese source mirrors, English translations, manifest paths and route locations were reviewed.
- README model/platform edits from the parallel session were preserved. Shared parsers/loaders, dependency configuration, archived tasks and journals were not modified by this reviewer.

## Verification

- Affected historical contract suites after fixes: PASS, 24 tests (`check-contract-fixes.txt`).
- Resource sync: PASS, exit 0, all 305 manifest entries (`check-resources.txt`).
- `just doc-build`: PASS, exit 0, after the bilingual input correction, 22.98s (`check-doc-build.txt`). Initial invocation hit local npm.ps1 execution policy; retry used only process-local `PSExecutionPolicyPreference=Bypass`, with no repository or persistent machine-policy change.
- Initial complete `just ci`: FAIL, exactly the three contract failures fixed above; 2841 passed / 3 failed / 11 skipped in 500.59s. Evidence: `check-ci-initial.txt`. The earlier pre-suite lint attempt failed only on the three migrated test files, which were formatted before this full run.
- Final `just ci`: PASS, exit 0 (`check-ci-final.txt`, with `-ra` for skip reasons). All four sequential gates ran: version alignment 1 passed; Ruff format 252 files and lint clean; Pyright 0 errors / 86 existing-file warnings; pytest 2847 passed / 11 skipped in 511.81s, 2858 collected.
- Reply-specific results within final CI: original suite 39 passed / 1 skipped; four new installed/ownership cases passed. All 16 R-* negative cases and clean synthetic case passed.
- Final `git diff --check`: PASS, exit 0 (`check-diff.txt`).

The 11 explicit skips are: 5 defense/demo TeX compilation cases (DEFENSE_ZH_COMPILE opt-in plus toolchain required), 4 PyMuPDF-dependent cases (3 defense previews and 1 reply PDF intake; dependency absent), and 2 non-Windows Unicode protocol paths. None is counted as a runtime PASS. See the final CI log for exact nodes and reasons.

Environment: workspace `.cache/uv` for UV cache, workspace-owned TEMP/TMP and unique pytest basetemp. No PYTHONIOENCODING override on pytest. Skips must remain separate from passes in the final totals.
