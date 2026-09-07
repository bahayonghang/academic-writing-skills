# 实施计划

## 前置

用户批准最终计划。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 记录 README 两处进入任务前 diff，确认该片段不在本次改动范围。
2. 以代码/SKILL/justfile 为事实来源，精简并统一 AGENTS、CLAUDE 和用户入口说明。
3. 只纠正 pyproject 描述/许可冲突，不修改 dependencies 或 version。
4. 运行所列门禁，强模型检查语义一致及用户许可决策；补对应任务验收记录。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py tests/contracts/test_skill_contracts.py -q
rg -n 'v3\.0\.0|MIT|pdfplumber|Academic Use|商业' AGENTS.md CLAUDE.md README.md README_CN.md pyproject.toml
git diff --check
```

## 审查与完成

rg 只用于人工核对，不添加机械许可/语义扫描器。新的命令示例按路径核实。主审确认仅限批准段落变更。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
