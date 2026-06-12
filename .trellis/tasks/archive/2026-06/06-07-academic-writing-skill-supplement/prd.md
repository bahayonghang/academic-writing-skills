# 补全学术写作技能

## Goal

作为父任务，协调 `latex-paper-en` 与 `latex-thesis-zh` 两条线独立演进，把 `research-writing-skill` 中更高阶的论文写作能力补进各自 skill，同时更新对应 eval / trigger eval，并保留各自的语言与场景边界。

## Requirements

- 这次更新拆成两个独立子 deliverable：`latex-paper-en` 和 `latex-thesis-zh`。
- 两个子 deliverable 都要更新 skill 内容、evals、trigger eval。
- `latex-paper-en` 继续保持英文论文、LaTeX 源码安全边界、section router、reviewer-facing 输出格式。
- `latex-thesis-zh` 继续保持中文学位论文、学校模板适配、GB/T 7714、章节主线与标题后导语约束。
- 两个 skill 都要补强更高阶写作能力：论文/章节主线、证据闭合、章节级写作动作、claim-evidence 映射、图表叙事接口。
- 不引入互相冲突的公共抽象；两条线可以借鉴同一类写作思想，但最终要落到各自 skill 体系中。

## Acceptance Criteria

- [ ] 两个 child task 已创建，且各自的范围互相独立、可单独验收。
- [ ] `latex-paper-en` 的 eval / trigger eval 覆盖 section-writing、logic、literature、experiment、abstract 以及 reviewer-facing 边界。
- [ ] `latex-thesis-zh` 的 eval / trigger eval 覆盖结构、逻辑、文献综述、实验、摘要、标题、去 AI 化与模板适配。
- [ ] 两个 skill 的新增或强化参考文件能明确表达各自的主线、证据闭合和章节级写作动作。
- [ ] 任何共享借鉴都不会破坏两个 skill 既有的语言边界、脚本约定、路径约定或安全边界。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
