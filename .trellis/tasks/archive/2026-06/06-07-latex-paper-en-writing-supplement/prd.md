# 补强 latex-paper-en 学术写作能力

## Goal

把 `latex-paper-en` 的写作支持补到接近 `research-writing-skill` 的层级，重点覆盖英文论文的 section-writing、claim-evidence 闭合、章节主线、图表叙事与 reviewer-facing 自检，同时保持英文论文 / LaTeX / 安全边界不变。

## Requirements

- 新增一批面向高阶写作能力的 eval 场景，而不只是路由和基础诊断场景。
- 至少新增 5 个高阶 eval 场景，覆盖 section-writing、claim-evidence、自检、图表叙事或章节闭合中的关键能力。
- 新增的 eval 场景应覆盖 Introduction、Related Work、Method、Experiments、Conclusion、claim-evidence/self-review、figure/venue 叙事等能力族。
- trigger eval 需要补充至少 8 个 research-writing-skill 近邻场景，包含 should-trigger 与 should-not-trigger 的边界样例。
- 继续保留 `latex-paper-en` 现有的英文论文定位、section router、LaTeX 安全边界和 reviewer-facing 输出格式。
- 如果新增或调整参考文件，docs mirror 需要同步保持一致。

## Acceptance Criteria

- [ ] `evals.json` 新增一批高阶写作场景，且每个场景都对应一个可解释的写作能力点。
- [ ] 至少 5 个 eval 能稳定覆盖 Introduction / Related Work / Method / Experiments / Conclusion / self-review / figure caption 中的高阶能力点。
- [ ] 新 eval 覆盖至少以下能力族：Introduction 写作蓝图、Related Work 主题合成与 gap 推导、Method 动机-设计-优势、Experiments/Discussion 证据闭合、Conclusion 收束、claim-evidence/self-review。
- [ ] `trigger_eval.json` 至少新增 8 个近邻误触发样例，能区分 section-writing 与 audit / translation / thesis / generic polishing。
- [ ] 现有模块路由、脚本约定、LaTeX anchors、安全边界不被破坏。
- [ ] 如有新增参考文件，docs 镜像目录同步更新。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
