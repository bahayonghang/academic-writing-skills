# Implementation Plan: latex-thesis-zh

## Phase 0: Review Gate

- [ ] Confirm scope = corpus expansion（Phase 1-3）+ 章引言能力补强（Phase 4），二者均不新增模块。
- [ ] Confirm 章引言工作流通过扩展现有 `logic` 模块实现，no new thesis module will be added.
- [ ] Keep the task in planning until the PRD and design are reviewed.

## Phase 1: Corpus Expansion

- [ ] Update `academic-writing-skills/latex-thesis-zh/evals/evals.json`.
  - Add or sharpen prompts for:
    - 绪论漏斗 / 科学问题收束。
    - 文献综述主题化与研究空白推导。
    - 方法章节动机 -> 设计 -> 优势。
    - 实验 / 讨论的分层、消融、机理、局限。
    - 摘要 / 创新点 / 结论闭合。
    - 标题后导语 / 章节桥接 / 去 AI 味边界。
- [ ] Update `academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json`.
  - Add positive near-neighbors for thesis-specific writing work.
  - Add negative near-neighbors for English paper, Typst, paper-audit, bibliography-only, generic polishing, from-scratch drafting, translation-only, compile-only, and format-only requests.
  - Keep prompts realistic and high-signal.

## Phase 2: Boundary Check

- [ ] Review whether any prompt wording suggests a trigger boundary gap in `SKILL.md`.
- [ ] If needed, make the smallest possible wording fix only.
- [ ] Keep thesis-specific routes and terminology dominant.

## Phase 3: Validation

Run:

```bash
uv run pytest tests/test_skill_contracts.py tests/test_trigger_evals.py tests/test_skill_versions.py
git diff --check
```

If one prompt category is too close to another skill, tighten that boundary before considering the task ready.

## Rollback Points

- If a prompt becomes generic polish, rewrite it to require thesis chapter reasoning.
- If the trigger set confuses thesis work with English-paper work, move the borderline case to the negative side.
- If the eval set is too repetitive, collapse overlapping prompts and keep the strongest writing move per family.
