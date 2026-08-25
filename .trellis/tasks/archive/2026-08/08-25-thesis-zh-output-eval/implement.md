# 执行计划：output eval 升级与 E1-E9 fixture

共享执行约束见
`.trellis/tasks/08-25-thesis-zh-visible-prose-ir/implement.md`。

`evals.json` 必须用 Bash python 写入，禁止 Edit/Write 直接改该文件。

## 执行顺序

### S1 — runner 与失败测试

- [ ] 写 `academic-writing-skills/latex-thesis-zh/scripts/run_output_evals.py`
- [ ] 写 `tests/skills/latex_thesis_zh/test_output_evals.py`：要求读取
      `evals/output-evidence/<id>/meta.json`；包含一条反向断言——仅检查字段
      存在不得使质量 AC 通过
- [ ] 建 `evals/output-evidence/.gitkeep`

**验证**：无 fixture/命令时 runner 非零退出；测试失败原因是证据落点缺失。

### S2 — E1-E9 fixture

- [ ] 在 `evals/fixtures/quality-regressions/` 建 E1-E9，全部脱敏
- [ ] 每例 `evals.json` 的 `command` 为 argv，指向 design.md 表中的入口
- [ ] E1 按 V3；E2 与子任务 1 B1 同构（含成果章）；E3-E9 按 design.md 表

**验证**：fixture 内无真实变量名/路径/实验称谓/真实数值（搜索清单写入
check 笔记）。每个 case 缺 `command` 时 runner 非零退出。

### S3 — evals.json 加字段

- [ ] Bash python 为旧 31 case 加 `origin=legacy-trigger-only` 等字段，保留四键
- [ ] 追加 E1-E9 case，`command` 为 argv 列表

**验证**：`test_evals_json_shape` 通过；case 数 ≥ 31。

### S4 — 执行证据

- [ ] runner 对 E1-E9 写出 meta.json + stdout/stderr
- [ ] 测试对照结构/保源/证据强度/假阳性
- [ ] E1-E3 无标注时 TP/FP/FN 状态为 missing evidence，不预填达成

**验证**：AC3-AC6、AC10 转绿。格式化只跑 runner 与测试文件。

### S5 — trigger 与文档

- [ ] `trigger_eval.json` 语义不变；如加 mode near-neighbor，不破坏健康规则
- [ ] SKILL.md 只改 `last_updated`
- [ ] 本提交内重建 manifest
- [ ] `just ci`；`just doc-build`
- [ ] Phase 3.4 确认提交清单；文案用 project-native P0/P1 closure

## 回滚

删除 runner、quality-regressions 新 fixture、output-evidence、测试；
`git restore --source=HEAD -- academic-writing-skills/latex-thesis-zh/evals/evals.json`。

## 人工确认

不跑 provider A/B 与盲评。终检不得写 Library-ready 或「skill 输出更好」。
