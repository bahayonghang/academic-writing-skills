# 实施计划

## 前置

用户批准；可与 C1/C2 独立。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 先把探针的真实失败路径落到现有 integration test 文件：子进程发出非 ASCII，Windows 用 PYTHONUTF8=0 及 stream UTF8 保证区域编码差异。
2. 先观察新增用例失败，并保留 stderr 证据。
3. 只在 _run_check_script 设置复制后的子进程环境与显式 UTF-8 pipe encoding。
4. 运行限定测试与原探针；确认正常 fixture 的检查集合未减少。
5. 强模型复核后记录修复协议供 C6 回写。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
uv run --extra dev python -m pytest tests/skills/paper_audit/test_paper_audit_integration.py tests/skills/paper_audit/test_paper_audit.py -q
uv run --extra dev python .trellis/tasks/09-07-five-harness-evergreen-audit/research/probe_isolated_audit.py
just lint
just typecheck
```

## 审查与完成

测试必须走实际 Popen/子脚本，不能只断言 subprocess kwargs。非 Windows 也测 Unicode 协议；Windows 专属复现缺失时注明证据。主审检查没有改变 gate/scoring/timeout。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
