# 执行计划：语义中间产物与 finding schema

共享执行约束（dirt 冻结清单、禁止 `ruff format .`、禁止无路径 checkout、
Phase 3.4 确认后提交）见
`.trellis/tasks/08-25-thesis-zh-visible-prose-ir/implement.md`。

## 执行顺序

### S1 — schema 与失败测试

- [ ] 写 `references/schemas/artifacts.md`：共享核心、扩展、paper-audit 映射表、
      字段所有权
- [ ] 写 `tests/skills/latex_thesis_zh/test_artifacts.py`：字段集合（非相等）、
      快照所有权、整文件权威拒绝、合并 span

**验证**：新测试失败原因是模块不存在或 schema 未落地，不是 import 到 EN 副本。

### S2 — `artifacts.py`

触及：`academic-writing-skills/latex-thesis-zh/scripts/artifacts.py`

- [ ] 校验、稳定 ID、合并、JSON/JSONL IO、四张 map builder

**验证**：`uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_artifacts.py -q`
中 schema 用例转绿。格式化只跑该文件。

### S3 — evidence-intake

触及：`academic-writing-skills/latex-thesis-zh/references/workflow/evidence-intake.md`

- [ ] preflight / source-priority / generated_artifacts schema

**验证**：AC5/AC6 测试转绿。

### S4 — analyzer JSON 旁路

触及：`analyze_logic.py` `analyze_literature.py` `analyze_experiment.py`
（均在 `academic-writing-skills/latex-thesis-zh/scripts/`）

- [ ] 可选 `--json` / `--artifacts`，默认关
- [ ] 人类可读 stdout 与子任务 1 合入后快照逐字节一致

**验证**：无新 flag 时三脚本快照一致；`--json` 含 `artifact_refs` 与
`root_cause_key`。格式化只跑上述三文件。

### S5 — 文档与校验

- [ ] 更新 `references/modules/{logic,literature,experiment}.md`
- [ ] SKILL.md 只改 `last_updated`
- [ ] 本提交内重建 manifest + 双语页面
- [ ] `just ci`；`just doc-build`
- [ ] Phase 3.4 列出文件与 unrecognized dirt

## 回滚

| 阶段 | 方式 |
| --- | --- |
| S1-S3 | 删除新增 schema/脚本/测试 |
| S4 | `git restore --source=HEAD -- academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py` |
| S5 | restore 三份 module md 与 SKILL.md；重跑 manifest 写入 |

## 人工确认

LLM map 正确率保持 missing evidence，不在本任务补测。
