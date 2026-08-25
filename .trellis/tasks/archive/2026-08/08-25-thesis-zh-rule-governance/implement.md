# 执行计划：写作规则分级与因果门禁治理

共享执行约束见
`.trellis/tasks/08-25-thesis-zh-visible-prose-ir/implement.md`。

## 执行顺序

### S1 — 复核「基于上述分析」（TPR-12，先于任何指南修改）

规划期已对最小 fixture 跑当前 `deai_check.py`：退出码 0，痕迹列表为空。
本步复跑同一命令，确认输出仍为空后再改指南。

- [ ] 复跑 design.md「复现记录」中的命令
- [ ] 若仍为零 throat-clearing finding，按已定裁决改指南示例或加
      `applies_when`；若出现新 finding，停止并更新 design.md 后再改指南
- [ ] 不改 deai 词表

**验证**：`git diff -- academic-writing-skills/latex-thesis-zh/references/deai/`
为空。不把未出现的 throat-clearing=2 写入测试。

### S2 — 失败测试

- [ ] `tests/skills/latex_thesis_zh/test_rule_governance.py`：适用/不适用、
      工学实验不报 GPU Major、不等预算消融、deai 字节不变

**验证**：新测试失败指向规则尚未分级，不是 deai 表被改。

### S3 — 指南分级与示例裁决

触及：

- `academic-writing-skills/latex-thesis-zh/references/writing/writing-philosophy-zh.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/academic-style-zh.md`

- [ ] 增加 `level` `applies_when` `exceptions` `authority` `counterexample`
- [ ] 按 S1 记录修改「基于上述分析」示例
- [ ] 在 design.md 附录映射防误报红线 12 条

**验证**：AC1-AC4 转绿；deai 三文件 diff 仍为空。

### S4 — 因果门禁与阶梯去重

触及：

- `academic-writing-skills/latex-thesis-zh/references/writing/over-claim-guard.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/results-analysis-guide-zh.md`
- 仅必要时 `scripts/analyze_experiment.py`

- [ ] 五项门禁；保留「消融实验 / 消融设置」
- [ ] canonical 阶梯只留一处；同步 `test_results_analysis.py`
- [ ] 确认不把 over-claim-guard 写入 SKILL.md Reference Map

**验证**：AC5-AC8 转绿；`test_polish_contract_alignment.py` 通过。

### S5 — 文档与校验

- [ ] 本提交内重建 manifest
- [ ] `just ci`；`just doc-build`
- [ ] Phase 3.4 确认提交清单

## 回滚

`git restore --source=HEAD --` 四份 writing md 与可能改动的
`analyze_experiment.py`。禁止 restore deai 文件。

## 人工确认

真实论文误报率保持 missing evidence。S1 复现记录必须先于指南修改进入
design.md。
