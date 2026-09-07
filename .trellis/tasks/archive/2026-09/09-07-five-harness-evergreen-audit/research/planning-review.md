# 独立规划审查与修订记录

日期：2026-09-07。审查者：独立 trellis_plan_auditor（角色固定 gpt-5.6-sol / max）；主线程负责修订自身创建的计划。审查范围为父任务和6个子任务，不修改产品代码，不启动任务。

## 初审发现与修订

| 编号 | 初审问题 | 主线程规划修订 |
|---|---|---|
| PR1 / P1 | 安装契约只写 docs，没有落到安装后权威入口 | C4 新增 paper-audit/SKILL.md 依赖段与两语index所有权；明确C5后续顺序编辑 |
| PR2 / P1 | 顺序单agent执行时，原共识标签容易被误解为独立专家共识 | C5 新增 synthesis_agent.md / editorial_decision_standards.md 与镜像范围；报告正文说明执行方式，单agent CONSENSUS只作跨视角一致，不新增JSON字段/评分规则 |
| PR3 / P1 | C6台账允许UNVERIFIED，但步骤又将其作为完成阻断 | C6 AC2只验台账完整诚实；推荐范围为静态规则与隔离脚本交付，真实五工具运行作为可选扩展独立记状态 |
| PR4 / P1 | CI依赖runner预装uv/just，干净启动机制未写实 | C2明确setup-python/uv/just Actions与版本，UV_PYTHON跟随matrix，UV_FROZEN=1，先打印版本后运行门禁；来源已打开核对 |
| PR5 / P2 | C1的五工具来源不在上下文清单 | C1 implement/check各加入harness-rules.md |
| PR6 / P1 | 模型分层有说明，但C1–C6没有逐问题映射到五套harness | 父AC3补工具映射要求；父implement批准表增加“适用harness / 证据状态”，明确本轮已做与候选UNVERIFIED路径，design指向同一表 |

## 范围裁决

研究候选中的批量adapter生成/跟踪、gitignore allowlist、上游Trellis改造、固定模型路由、matrix验证器并未采纳。最终实施范围只以父design/implement及六个子任务为准。许可按用户选择保留学术非商业。

## 验证

- 父子任务树7项：机械预检0阻断，关系和编号可解析。
- task.py validate全部通过；每份JSONL均是真实条目。
- 产品基线：just ci 1756通过；full resource sync 271通过；docs build通过。它们是改造前证据。
- 全工作树git diff --check仅报告用户原有README_CN.md:14双空格；新增规划文件没有行末空白。
- 所有task.json仍planning，未运行start/提交/发布。

## 复核状态

同一独立审查者复核结论：**GO，可提交用户批准，剩余 planning blocker 为0。** 六项均闭环；三个setup action标签实时可解析，父R4与任务级harness/证据表闭合，7任务均planning。

实施期仍须获得代码修复后真实测试、workflow YAML及同SHA hosted证据；可选的五工具fresh session/安装器/委派继续单列UNVERIFIED。此GO是计划可审查、可批准，不是用户实施授权，也不是六个改造任务已经完成。
