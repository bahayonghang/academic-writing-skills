# 执行计划：re-audit 与 gate 语义

共享执行约束见
`.trellis/tasks/08-25-thesis-zh-visible-prose-ir/implement.md`。

## 执行顺序

### S1 — 七例 fixture 与失败测试

- [ ] 在 `evals/fixtures/quality-regressions/re-audit/` 建 F1-F7
      （unresolved / addressed / partial / new / regressed / span-move /
      stale_patch）
- [ ] 写 `tests/skills/latex_thesis_zh/test_re_audit.py`：同一输入只断言一态；
      重叠条件按 design.md 序号 1→8 取第一条

**验证**：测试因 `re_audit.py` 不存在失败。

### S2 — `re_audit.py`

触及：`academic-writing-skills/latex-thesis-zh/scripts/re_audit.py`

- [ ] identity、转移表、evidence delta
- [ ] hash mismatch → `stale_patch` + `gate_blocker`，不写源
- [ ] 不得 import `thesis_workflow` 写路径（测试用 AST 或 mock 断言）
- [ ] gate 五态；`no_script_finding` 不升 `pass`

**验证**：AC1-AC8 转绿；F7 工作树源 fixture 字节不变。格式化只跑该文件。

### S3 — 文档

触及：`references/workflow/controlled-rewrite.md` 与相关 modules md

- [ ] 写入 identity 规则与「只报告过期 patch」边界
- [ ] SKILL.md 只改 `last_updated`

**验证**：文档含转移表；compile 仍指向既有 `scripts/compile.py`。

### S4 — 校验

- [ ] 本提交内重建 manifest
- [ ] `just ci`；`just doc-build`
- [ ] Phase 3.4 确认提交清单

## 回滚

删除 `re_audit.py`、测试与 F1-F7；`git restore` controlled-rewrite.md。

## 人工确认

PDF 视觉自动抽样保持 missing evidence。
