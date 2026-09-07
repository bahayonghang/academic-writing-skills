# 实施计划

## 前置

C1/C2/C3 完成；用户批准。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 读取父任务 harness-rules 与 runtime-findings；核查各工具官方来源仍适用。
2. 新增双语指南，给明确读取共同规则的 fallback；仅保留必要平台差异，不批量复制本机生成资产。
3. 更新安装页与 paper-audit/SKILL.md 的最小依赖段：完整集合/sibling 要求、单 skill 受限覆盖、正确测试入口与证据状态；同步 paper-audit 两语入口，给新页面加入两语导航。C5 必须在该变更之后编辑同一入口。
4. 新增真实隔离 CLI 测试：tmp 下复制完整集合与只有 paper-audit，对相同 fixture 比较 missing/RUN；UTF8 环境避免混入 C3 故障。
5. 完整布局无需联网 smoke；npx/软件全局安装需另有授权且真实执行后才能标已验证。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
uv run --extra dev python -m pytest tests/skills/paper_audit/test_installed_layout.py tests/contracts/test_docs_bilingual_resources.py -q
uv run --extra dev python docs/scripts/check_resource_sync.py
just doc-build
git diff --check
```

## 审查与完成

检查 rendered HTML 的新增导航 id/href，不进行用户未要求的 UI 自动化。复制安装验证不等于 npx 安装或 symlink 验证。禁止把 tool metadata 当强制安全沙箱。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
