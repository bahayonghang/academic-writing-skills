# 执行计划：mode 契约与受控改写账本

共享执行约束见
`.trellis/tasks/08-25-thesis-zh-visible-prose-ir/implement.md`。

## 执行顺序

### S1 — 契约文档与失败测试

- [ ] 写 `references/workflow/mode-contract.md`（优先级表 + destination 表）
- [ ] 写 `references/workflow/controlled-rewrite.md`（不变量 + ledger 字段）
- [ ] 写 `tests/skills/latex_thesis_zh/test_mode_contract.py`：显式 mode、
      自然语言「优化」无授权、自然语言「优化」有授权、无 report 路径、
      `--output -`、无源写授权的显式 revise

**验证**：新测试因入口不存在而失败。

### S2 — orchestrator

触及：`academic-writing-skills/latex-thesis-zh/scripts/thesis_workflow.py`

- [ ] 实现优先级、destination 表、退出码 0/2/3/1
- [ ] revise 默认 dry-run；无 `--apply-source` 的显式 revise 退出 2
- [ ] ledger 与 fidelity gate（strength 升级、generated、白名单）
- [ ] `[Script]` 层 `Meaning-Check: NEEDS-LLM`

**验证**：AC1-AC4 的六类 fixture 转绿。格式化只跑该文件。

### S3 — 路由文档

触及：

- `academic-writing-skills/latex-thesis-zh/SKILL.md`
- `academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md`
- `academic-writing-skills/latex-thesis-zh/agents/openai.yaml`

- [ ] module × mode 矩阵；旧 CLI 兼容说明
- [ ] openai.yaml 四键保留；default_prompt 先锁 mode
- [ ] `--strength` 与 `--tier` 不合并

**验证**：`test_openai_yaml_shape` 与
`test_latex_thesis_zh_module_router_commands_match_script_help` 通过；
旧 analyzer help 快照不变。

### S4 — 文档与校验

- [ ] 本提交内重建 manifest + 双语页面
- [ ] `just ci`；`just doc-build`
- [ ] Phase 3.4 确认提交清单

## 回滚

删除 `thesis_workflow.py` 与两份 workflow md、测试；
`git restore --source=HEAD --` SKILL.md、routing-rules.md、openai.yaml。

## 人工确认

不对真实论文执行 `--apply-source` 写入。
