# cover-letter AI 披露一致性增强（可选）

## Goal

【enhancement，可选，优先级最低】为 cover-letter 补上与 en/zh/typst 同代的 AI 痕迹判断力：结构级 AI 痕迹检查与"信↔稿件 AI 披露一致性"交叉检查。本任务是功能增强而非缺陷修复，做不做由用户决定。

证据详情：`../07-05-skills-deep-analysis-optimization/research/bib-cover-findings.md`（CL-3 / CL-4）

## 问题清单

- **CL-3 [enhancement]** cover-letter 的 AI-tone 检查需同词出现 3+ 次才报，且没有 en/zh/typst 那种结构级 AI 痕迹检查（commit 7311420 引入的结构壳检查未惠及 cover-letter）。
- **CL-4 [enhancement]** 只检查信内 AI 披露有无，缺"信中披露与稿件中披露是否一致"的交叉检查——align-check 已读入稿件全文，有现成输入基础。

## Requirements

- R1 CL-4（价值更高，先做）：align-check 增加 AI 披露一致性 lane——稿件有披露而信没有、信有而稿件没有、两侧措辞矛盾，三种情形各产生 finding（severity: medium）。
- R2 CL-3：结构级 AI 痕迹检查按 en 副本的结构壳检查裁剪移植（信件体裁短，阈值需重调）；同词阈值 3+ 降为 2+ 或按信件长度自适应，在 design 里写明取舍。
- R3 新检查只报告不改写（与 align-check 现有契约一致），输出走 diff/suggestion 块并标注 `[Script]`。

## Acceptance Criteria

- [ ] 稿件含 AI 披露、信件无 → align-check 产生 finding（测试断言）；反向与措辞矛盾两情形同理。
- [ ] 结构壳检查在典型 AI 生成信件样例上至少命中一类 trace，在人工写作样例上零误报（用 evals 样例验证）。
- [ ] `just ci` 全绿；不改动 en/zh/typst 侧任何代码。

## Notes

- **可选任务**：仅当用户确认要做再 start；父任务验收不含本项。
- 若做 CL-3，考虑其副本是否纳入 `07-05-deai-alignment-lock` 的对齐锁范围（体裁差异大，预期是"有意分歧"条目）。
