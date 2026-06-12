# Implementation Plan

## Phase 0: Review Gate

- [x] User confirms scope decision:
  - recommended: deep `latex-paper-en` section-writing integration plus light
    `latex-thesis-zh` adaptation.
- [x] User approves starting implementation after reviewing `prd.md`,
  `design.md`, and this `implement.md`.
- [x] Run `python ./.trellis/scripts/task.py start 06-05-paper-section-reference-integration`
  only after approval.

## Phase 1: English Paper Integration

- [x] Update `academic-writing-skills/latex-paper-en/SKILL.md`.
  - Add `section-writing` to capability summary, triggering, module router,
    routing rules, output contract, reference map, and examples.
  - Keep diagnostic routes intact.
  - Make route distinction explicit:
    - diagnosis/checking -> existing script-backed modules;
    - drafting/rewrite planning/paragraph roles/claim-evidence self-review ->
      `section-writing`.
- [x] Add `references/modules/SECTION_WRITING.md`.
  - State section-specific workflow.
  - Define output contract.
  - Point to section reference files.
  - Restate LaTeX preservation boundaries.
- [x] Add `references/section-writing/` reference bank.
  - `INDEX.md`: route map, attribution/license note, progressive-disclosure
    instruction.
  - `ABSTRACT.md`: abstract logic variants and claim-evidence constraints.
  - `INTRODUCTION.md`: task/application, technical challenge, pipeline
    contribution, experiment/contribution closure.
  - `RELATED_WORK.md`: topic design and comparison/gap positioning.
  - `METHOD.md`: module triad: motivation, design, technical advantage.
  - `EXPERIMENTS.md`: claim-to-experiment planning, ablations, table/figure
    communication, limitations.
  - `CONCLUSION.md`: solved problem, evidence, implication, limitation,
    future work.
  - `FLOW.md`: one paragraph/one message, topic sentence, reverse outline,
    sentence-to-sentence relation checks.
  - `SELF_REVIEW.md`: reviewer-facing self-review and claim-evidence map.
- [x] Update `academic-writing-skills/latex-paper-en/evals/evals.json`.
  - Add or revise evals for section-writing prompts:
    - Introduction rewrite plan with technical bottleneck and pipeline
      contribution.
    - Method section module triad.
    - Conclusion with evidence and limitation boundary.
    - Claim-evidence map across Abstract/Introduction/Experiments.
- [x] Update `academic-writing-skills/latex-paper-en/evals/trigger_eval.json`.
  - Add positive triggers for section-writing prompts.
  - Add near-miss negatives for standalone research from scratch,
    paper-audit/gate review, Chinese thesis, and non-LaTeX writing.

## Phase 2: Chinese Thesis Adaptation

- [x] Update `academic-writing-skills/latex-thesis-zh/SKILL.md` with a light
  thesis-specific adaptation.
  - Prefer enriching existing `logic`, `literature`, `experiment`, `abstract`,
    and `structure` language over adding a mirrored `section-writing` module.
- [x] Add or update Chinese reference notes.
  - Keep `STRUCTURE_GUIDE.md` and `LOGIC_COHERENCE.md` as the primary
    thesis-specific guides.
  - Add thesis-facing references only where a gap exists, e.g. a
    `references/THESIS_WRITING_GUIDE.md` or module-specific additions.
- [x] Update `latex-thesis-zh/evals/evals.json` if behavior changes.
  - Cover 绪论漏斗, 方法章节动机/设计/优势, 实验讨论分层, 总结与展望闭合.
- [x] Update `latex-thesis-zh/evals/trigger_eval.json` only if description or
  routing semantics change.

## Phase 3: Contracts and Versioning

- [x] If `latex-paper-en` gains a new module name, update
  `tests/test_skill_contracts.py` module list for `latex-paper-en`.
- [x] If `latex-thesis-zh` gains a new module name, update its contract list.
  If only existing modules are enriched, no contract module-list update is
  needed. Decision: no new thesis module was added, so no contract-list change
  was needed for `latex-thesis-zh`.
- [x] Decide whether this repo's version policy requires bumping frontmatter
  `metadata.version` and `last_updated`; if yes, update all relevant skill
  version files consistently. Decision: no version bump in this slice; current
  `5.2.0` contract remains valid.

## Phase 4: Verification

- [x] Run:

```bash
uv run pytest tests/test_skill_contracts.py tests/test_trigger_evals.py
```

Result: `48 passed`.

- [x] Run:

```bash
uv run pytest tests/test_latex_paper_en_scripts.py tests/test_latex_thesis_zh_scripts.py
```

Result: `109 passed`.

- [x] Run:

```bash
git diff --check
```

Result: passed; only Windows CRLF warnings.

- [x] If docs/readme/public inventory changed, run relevant docs checks:

```bash
just doc-build
```

Result: passed; generated `docs/.vitepress/dist` build artifacts were restored
after verification.

- [x] Run full project CI after formatting the touched contract test:

```bash
just ci
```

Result: passed; `628 passed`, Ruff passed, Pyright completed with existing
warnings and zero errors.

- [x] Run `skill-creator` quick validation where applicable:

```bash
$env:PYTHONUTF8='1'; python C:\Users\lyh\.codex\skills\.system\skill-creator\scripts\quick_validate.py academic-writing-skills\latex-paper-en
$env:PYTHONUTF8='1'; python C:\Users\lyh\.codex\skills\.system\skill-creator\scripts\quick_validate.py academic-writing-skills\latex-thesis-zh
```

Result: blocked by existing `argument-hint` frontmatter incompatibility in both
skills. This is a pre-existing repo convention, not introduced by this task.

## Risk Points

- Adding a router row with a fake script command will fail
  `test_latex_paper_en_module_router_commands_match_script_help`.
- Copying source reference text without attribution risks license/credit drift.
- Over-triggering `latex-paper-en` for generic from-scratch writing could
  conflict with the skill's "existing `.tex` project" scope.
- Overfitting `latex-thesis-zh` to conference-paper patterns would weaken
  thesis-specific guidance around chapters, lead-ins, templates, and GB/T
  constraints.
- Broad version bumps can trigger repo-wide version contract failures if not
  done consistently.

## Phase 5: Reference Layout Refactor

- [x] Add a reference-layout contract test.
  - Require lowercase kebab-case reference filenames.
  - For `latex-paper-en` and `latex-thesis-zh`, reject loose top-level files
    under `references/` except approved category directories.
  - Keep module names in `SKILL.md` unchanged; this is a resource-path refactor,
    not a routing behavior change.
- [x] Migrate `latex-paper-en/references/` with `git mv`.
  - `modules/*.md` -> lowercase kebab-case names.
  - Writing guidance -> `references/writing/`.
  - Section-writing bank -> `references/writing/section-writing/`.
  - Citation guidance -> `references/citations/`.
  - Venue guidance -> `references/venues/`.
  - Formatting guidance -> `references/formatting/`.
  - De-AI files -> `references/deai/`.
  - Claim-evidence contract -> `references/evidence/`.
  - Reviewer perspective -> `references/review/`.
  - Compilation guide -> `references/latex/`.
- [x] Migrate `latex-thesis-zh/references/` with `git mv`.
  - `modules/*.md` -> lowercase kebab-case names.
  - Thesis writing, structure, logic, title, abstract, style -> `references/writing/`.
  - GB/T guidance -> `references/citations/`.
  - Caption/table guides -> `references/formatting/`.
  - De-AI files -> `references/deai/`.
  - Compilation guide -> `references/latex/`.
  - `UNIVERSITIES/` -> `references/university-templates/`.
- [x] Mirror the same layout under docs resources.
  - `docs/skills/latex-paper-en/resources/references/`.
  - `docs/zh/skills/latex-paper-en/resources/references/`.
  - `docs/skills/latex-thesis-zh/resources/references/`.
  - `docs/zh/skills/latex-thesis-zh/resources/references/`.
- [x] Update hard-coded paths and links.
  - `SKILL.md` router rows and reference maps.
  - Module cross-links and prose path mentions.
  - `docs/.vitepress/config.ts` sidebars.
  - `deai_check.py` threshold paths.
  - `detect_template.py` university-template path.
  - Tests that reference old locations.
- [x] Validate:

```bash
uv run pytest tests/test_skill_contracts.py tests/test_claim_evidence_contract.py tests/test_venue_templates_layout.py tests/test_latex_paper_en_scripts.py tests/test_latex_thesis_zh_scripts.py
just doc-build
git diff --check
just ci
```

Restore `docs/.vitepress/dist` after docs build if it is regenerated.

Results:

- `uv run pytest tests/test_skill_contracts.py tests/test_claim_evidence_contract.py tests/test_venue_templates_layout.py`:
  `43 passed`.
- `uv run pytest tests/test_latex_paper_en_scripts.py tests/test_latex_thesis_zh_scripts.py`:
  `109 passed`.
- `just doc-build`: passed; regenerated `docs/.vitepress/dist` was restored.
- Layout scans: no real uppercase or underscore filenames under the two target
  `references/` trees; no loose top-level files under those `references/`
  directories; no old target reference path matches remained.
- `git diff --check`: passed, with only Windows CRLF warnings.
- `just ci`: passed after formatting touched Python/test files; Ruff passed,
  Pyright reported existing warnings and zero errors, and tests passed with
  `629 passed`.

Spec update decision: no `.trellis/spec/` update was needed. This phase
codifies a skill resource-layout convention through repository contract tests
and docs links, but it does not introduce or change command/API signatures,
cross-layer payload contracts, database schema, or infrastructure wiring.
