# 实施计划

## 前置

C4 完成；用户批准。

批准后先读 prd/design 与父任务 implement.md，再检查真实文件锚点是否漂移。没有明确实施批准不得运行 task.py start。

## 步骤

1. 按 C4 已审能力表加入简短跨工具执行说明，保留现有技能边界与路由。
2. 在现有 paper-audit workflow/模板及 synthesis_agent/editorial_decision_standards 补委派输入输出、顺序 fallback 和正文执行方式说明；CONSENSUS 解释必须区分多agent独立输出与单agent跨视角一致，禁止新增provider框架、JSON字段、评分规则或固定价格表。
3. 同步受影响入口页/两语资源并用 checker 重建必要 manifest 条目。
4. 按下列测试及人工语义清单复核；不新加仅锁文案字面的测试。

## 必须通过的检查

以下从仓库根运行；外层按本机 RTK 规则使用 rtk proxy，命令内容保持原义。新文件标为“新增”的测试在实施时创建。

```text
uv run --extra dev python -m pytest tests/contracts tests/skills/paper_audit/test_paper_audit_topology_docs.py tests/skills/paper_audit/test_paper_audit_synthesis.py -q
uv run --extra dev python docs/scripts/check_resource_sync.py
just doc-build
git diff --check
```

## 审查与完成

人工复核无模型替代、无伪独立 reviewer、无英文/中文学术事实变化、无 T1/T2/T3 边界回退。结构测试不代表真实模型运行。

以同一已有小段fixture做两份审查输出的人工演练：一份假定已取得原生委派证据，一份明确顺序单agent；核对后者没有 independent panel 宣称，CONSENSUS 只作跨视角解释。演练本身标为规划/说明验证，不伪称真的调用了其他harness。真实多agent运行仅有实际委派证据时才能使用该声明。

记录每条命令退出码、失败/跳过原因和适用工具，不能仅写“测试完成”。本轮只创建计划，以上验收默认未执行；父任务的审查基线不是改造后的验收结果。
