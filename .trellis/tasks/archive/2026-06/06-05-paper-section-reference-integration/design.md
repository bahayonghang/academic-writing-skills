# Design: Section-writing integration

## Recommended Strategy

Use a bounded additive integration.

For `latex-paper-en`, add a new LLM-driven `section-writing` route/module that
bridges existing LaTeX-project safety rules with the source
`research-paper-writing` section guides. Keep script-backed diagnosis modules
unchanged. The new route should activate when the user asks to draft, rewrite,
plan, strengthen, or reviewer-polish a specific paper section rather than just
diagnose it.

For `latex-thesis-zh`, add a smaller thesis-specific adaptation only after the
English route is settled: enrich `logic`, `literature`, `experiment`,
`abstract`, and possibly `structure` with transferable writing patterns, but do
not add English conference-paper section names as first-class thesis modules.

This is the confirmed first-slice scope. Do not build an equally deep
`latex-thesis-zh` mirror of the English section-writing reference bank in this
task.

## Why Not Direct Copy

The source skill is organized as a standalone writing coach. It assumes the
agent is drafting/revising prose and can emit section outlines, paragraph roles,
and claim-evidence maps. `latex-paper-en` is organized around existing `.tex`
projects, script checks, and source-preserving review comments. Directly
copying the source `SKILL.md` would blur these responsibilities and may cause
the assistant to rewrite source too aggressively.

The compatible layer is the reference content, not the entire runtime shape.

## `latex-paper-en` Architecture

### Module Router

Add one module:

- `section-writing`: user asks for section-specific drafting, rewrite planning,
  paragraph role design, reviewer-friendly section polish, or claim-evidence
  self-review for Abstract, Introduction, Related Work, Method, Experiments, or
  Conclusion.

The module should be LLM-driven:

- Primary command: `(LLM-driven workflow)`.
- Read next: `references/modules/SECTION_WRITING.md`.
- Section guides live under `references/section-writing/`.

This avoids adding scripts that cannot deterministically verify writing quality.

### Reference Layout

Recommended structure:

```text
academic-writing-skills/latex-paper-en/references/
  modules/SECTION_WRITING.md
  section-writing/
    INDEX.md
    ABSTRACT.md
    INTRODUCTION.md
    RELATED_WORK.md
    METHOD.md
    EXPERIMENTS.md
    CONCLUSION.md
    FLOW.md
    SELF_REVIEW.md
    examples/
      index.md
      abstract.md
      introduction.md
      method.md
```

`SECTION_WRITING.md` should be the thin router and output contract. The section
files should preserve progressive disclosure: load only the file for the active
section plus `FLOW.md` or `SELF_REVIEW.md` when explicitly needed.

### Integration with Existing Modules

- `abstract` remains the structural diagnostic module with `analyze_abstract.py`.
  If the user asks for a rewritten abstract or abstract logic variants, route to
  `section-writing` after or alongside `abstract`.
- `logic` remains the diagnostic module for coherence, funnel, cross-section
  closure, and motivation-thread checks. If the user asks to design or rewrite
  the section narrative, route to `section-writing`.
- `literature` remains the Related Work diagnostic and rewrite-blueprint module.
  Its existing `Consensus -> Disagreement -> Limitations -> Gap -> This paper`
  chain should be kept and can point to `section-writing/RELATED_WORK.md`.
- `experiment` remains reviewer-style diagnosis for experiments/discussion.
  If the user asks to plan the experiment narrative or conclusion wording, route
  to `section-writing`.

### Output Contract

For section-writing tasks, return:

1. Section objective and compact outline.
2. Paragraph roles, such as opening, challenge, prior-work limitation, method,
   advantage, evidence, limitation, implication.
3. Revised prose or rewrite blueprint, depending on whether the user requested
   prose.
4. Claim-evidence map:
   `Claim: ... | Evidence: ... | Status: supported/needs evidence/unsupported`.
5. Self-review checklist for clarity, flow, terminology, unsupported claims,
   and missing evidence.

Use LaTeX-preserving rules from `latex-paper-en`: do not rewrite citation keys,
labels, refs, math, custom macros, or table/figure anchors unless explicitly
asked.

## `latex-thesis-zh` Adaptation

### Recommended Scope

Do a light adaptation in the same overall task:

- Add thesis-facing section-writing notes to existing modules rather than
  creating a full mirrored reference bank.
- Emphasize:
  - 绪论: 背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文贡献 -> 章节安排.
  - 文献综述: 共识 -> 分歧 -> 局限 -> 研究空白 -> 本文切入点.
  - 方法/章节主体: 章节主线, 模块动机, 设计说明, 技术优势, 与上一章的递进关系.
  - 实验/讨论: 有效性, 消融/敏感性, 机理解释, 与前人比较, 局限与启示.
  - 总结与展望: 工作总结, 贡献闭合, 局限边界, 未来方向.
- Keep existing thesis-specific lead-in, structure, and GB/T rules dominant.

### Why Light Instead of Deep

Chinese theses have different structure and risk profile:

- They include chapters, sections, lead-ins, template rules, GB/T references,
  and defense expectations.
- The source English skill is tuned for ML/CV/NLP-style conference/journal
  papers with Abstract/Introduction/Related Work/Method/Experiments/Conclusion.
- A full deep reference bank for `latex-thesis-zh` would require rewriting the
  source methodology into Chinese thesis norms, not just translating it.

## Attribution and License

The source repo is MIT-licensed and its README attributes most writing
methodology to Prof. Peng Sida's public notes. Implementation should choose one
of these approaches:

- Prefer paraphrased adaptation with a compact attribution note in
  `references/section-writing/INDEX.md`; or
- If copying substantial source passages, include a local license/credits note
  and preserve the required MIT copyright notice for the copied portion.

## Compatibility

- Keep existing `name`, version pattern, and allowed tools unless release policy
  requires a version bump.
- Do not add router rows with nonexistent script commands. If a module is
  LLM-driven, use the existing `adapt` pattern: command cell may be
  `(LLM-driven workflow)` so router-command tests ignore it.
- Update `tests/test_skill_contracts.py` only if adding a new module name
  requires the contract to know it.
- Update `evals/evals.json` and `evals/trigger_eval.json` for changed skill(s).

## Validation

Minimum targeted validation after implementation:

```bash
uv run pytest tests/test_skill_contracts.py tests/test_trigger_evals.py
uv run pytest tests/test_latex_paper_en_scripts.py tests/test_latex_thesis_zh_scripts.py
git diff --check
```

If only Markdown/eval routing changes are made and no scripts change, the script
tests are still a reasonable regression check because the router contract loads
script help for advertised commands.
