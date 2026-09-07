# 实施计划

## 前置

C1–C5 完成。正式规则/知识回写须有用户实施批准；外部发布不在本任务范围。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 收齐 C1–C5 验收与 diff，强模型独立检查权限、证据、跨技能和跨工具规则。
2. 执行最终共同门禁一次；对 C3 原复现再核验一次，对 C4 完整安装布局复用通过证据。
3. 完整填写五工具台账。只有具体工具启动/费用已有授权时才做可选新会话 smoke，记录真实版本/模型、输入及结果；否则对应运行状态记 UNVERIFIED。AC2 验收的是台账完整与诚实，不是所有 runtime 状态通过。
4. 把已批准且已证实的经验写入项目 spec 和索引，校准 public harness 指南状态。
5. 报告已完成/失败/缺证；不触发远程工作流，不擅自发布或修改分支保护。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
just ci
uv run --extra dev python docs/scripts/check_resource_sync.py
just doc-build
uv run --extra dev python .trellis/tasks/09-07-five-harness-evergreen-audit/research/probe_isolated_audit.py
git diff --check
```

## 审查与完成

AC1–AC4 通过后可完成本次推荐的“静态规则与隔离脚本交付”；可选 runtime 项仍按工具独立列状态，不作为静态交付的假绿证据。只有五工具实际运行均通过才能另称“五平台运行验证完成”。项目 spec 回写采用同一事实源，不复制日志。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
