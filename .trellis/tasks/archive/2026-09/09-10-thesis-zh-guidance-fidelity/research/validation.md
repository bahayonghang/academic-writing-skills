# C1 implementation validation

Date: 2026-09-10. Scope: the five owned public guidance files, their EN/ZH mirrors, the new
synthetic fixture and contract test, append-only eval entries, and this task's research evidence.
No scripts, school thresholds, SKILL routing, task state, dependencies, or release metadata were changed by C1.

## Changes

- `references/writing/writing-philosophy-zh.md`: replace invented numeric examples with explicit input/evidence conditions; defer abstract length and chapter advice to school requirements, actual work, and existing specialist resources; retain thematic grouped citations and valid implicit connections.
- `references/writing/over-claim-guard.md`: point evidence qualification to the existing results guide; distinguish confounded ablations, component contributions, and discriminating causal evidence; remove the unsearched-first hedge shortcut and retain supported strong conclusions.
- `references/writing/abstract-structure.md`: scope the five model and its short-abstract ranges as fallback writing references; remove unsupported venue/GB-T length rows and number-invention examples; retain the thesis model and school threshold values.
- `references/modules/logic.md`: bind AXES to the supplied single-accuracy observation and link to the existing evidence owner and reverse-outline example.
- `examples/logic-and-experiment.md`: add located keep/narrow/move-proposal rows with chapter goals and evidence, protecting review-only and current-only authority.
- The five resources have corresponding source-faithful ZH pages and translated EN changes under `docs/{zh/,}skills/latex-thesis-zh/resources/`.
- Add `evals/fixtures/guidance_fidelity.tex` and `tests/contracts/test_thesis_zh_guidance_fidelity.py`.
- Append one eight-scenario composite output eval (47 -> 48) and one previously absent reverse-outline trigger (49 -> 50). Both complete historical prefixes are hash-locked and unchanged. Eval/trigger diffs were respectively +50/-0 and +5/-0.

## Local checks

| Command / check | Result | Evidence boundary |
| --- | --- | --- |
| `rtk uv run --no-sync python -m pytest tests/contracts/test_thesis_zh_guidance_fidelity.py tests/contracts/test_polish_contract_alignment.py tests/contracts/test_deai_pattern_cluster_contract.py tests/contracts/test_defensive_ai_rhetoric_contract.py tests/contracts/test_trigger_evals.py tests/contracts/test_skill_contracts.py -q` | exit 0; 99 passed in 17.46s; no failed/skipped cases | Source contracts, fixture binding, preserved historical corpus and existing routing contracts; not a model-quality score |
| `rtk uv run --no-sync ruff check tests/contracts/test_thesis_zh_guidance_fidelity.py` | exit 0; All checks passed | New test only |
| `rtk uv run --no-sync ruff format --check tests/contracts/test_thesis_zh_guidance_fidelity.py` | Final exit 0; 1 file already formatted | First check reported that the new file needed formatting; ran `rtk uv run --no-sync ruff format tests/contracts/test_thesis_zh_guidance_fidelity.py` (exit 0, 1 file reformatted), then rechecked |
| `rtk uv run --no-sync pyright tests/contracts/test_thesis_zh_guidance_fidelity.py` | exit 0; 0 errors, 0 warnings, 0 informations | New test only; the tool also printed an available-version notice; no installation performed |
| `rtk git diff --check -- <17 tracked C1 source/mirror/eval paths>` | exit 0; no whitespace errors | Exact owned tracked paths; no cleanup of unrelated files |

The initial combined lint command returned the last command's exit code, so its intermediate format
failure was recorded from `Would reformat`. Final Ruff commands were run independently after formatting.
Formatting did not alter behavior; the passing 99-test run was not repeated without a behavioral change.

## Actual response evidence

Before source edits, saved the five source snapshots to `before-rules/`, source/corpus hashes to
`baseline-hashes.json`, the historical corpora to `baseline-evals.json` / `baseline-trigger_eval.json`,
and the empty initial owned-source diff to `before-edit.diff`.

The two fresh native samplers completed all eight scenarios and wrote their original responses directly
to `output-before.md` and `output-after.md`. The input sections are identical. `sampling-before.md`,
`sampling-after.md`, and the frozen `sampling-common-rules.md` contain only selected public rules and
the supplied inputs/requests. The two spawn calls used `fork_turns=none` and distinct agents.
Exact dispatch text, the after sampler's role clarification, and its follow-up are in
`sampling-dispatch.md`; hashes, requested model settings, canonical agent IDs and output-write UTC
timestamps are in `sampling-metadata.json`.

Independent rubric review is owned by the parent-dispatched quality reviewer, in `output-review.md`.
Raw responses are not revised in place. This is local agent response review, not a provider benchmark,
human blind review, or a measurement of real-thesis quality. Actual model/usage telemetry was not
returned and is explicitly null. System/developer policies still apply despite conversation-history isolation.

## Integration and remaining evidence

- Source and mirrors are ready for the parent to refresh the shared manifest.
- Per the parent's coordination update, the parent runs the final single-skill/full resource gates,
  docs build, and repository CI, then records the results; C1 does not repeat these in parallel.
- No new fragment links were added: new navigation uses file-level pointers.
- Five-host runtime, paid-provider evaluation, human blind review and real-thesis/field acceptance remain
  `UNVERIFIED / missing evidence`. No such activity was performed or inferred from these local checks.
- Commit, archive, merge and push were not performed by C1.


## 父任务集成完成（2026-09-10）

上述交接时待执行门禁现已完成：最终完整CI为1908 passed、2项平台条件skip，
Pyright0 errors/75既有warnings；单技能和全量资源271项、docs build与独立审阅均通过。
本任务AC已全部回填；未提交或归档。最终状态与证据以
[父级集成验收](../../09-10-thesis-zh-spec-gap-optimization/research/integration-validation.md)为准。
