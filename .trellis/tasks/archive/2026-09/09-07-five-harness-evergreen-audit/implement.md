# 待批准的实施顺序与验证

## 当前状态

本轮已授权：读项目、跑现有测试、只读远端失败取证、创建父子任务及研究/设计。未授权：正式代码/说明改造、全局设置、安装依赖、付费新会话、提交/发布。所有任务保持 planning，尚未执行 task.py start。

本轮新增的探针属于审查材料；它没有修复产品。现有本地门禁全绿与新增边界探针复现失败可同时成立。

## 顺序与交接

1. 用户批准最终计划，明确批准的子任务范围；C1 和 C3 可独立执行。
2. C1 完成后执行 C2，避免 pyproject.toml 冲突。
3. C1/C2/C3 通过后执行 C4：实际安装布局说明、五工具接入和 isolation smoke。
4. C4 通过后执行 C5：skill 包内跨工具委派说明与公开资源同步。
5. C1–C5 完成后 C6 独立强模型复核、最终门禁、注明适用工具的经验回写。

每次子任务派发必须携带 Active task、需求/设计、只允许编辑的文件、已有未提交变化、必须通过的检查和失败升级条件。子任务阅读对应 spec/research 清单；不能假设继承主线程全部上下文。

## 批准表

| ID | 用户可见结果 | 必须检查 | 模型分工 | 适用 harness / 证据状态 |
|---|---|---|---|---|
| C1 / P1 | 项目说明和学术非商业声明一致，PDF 依赖准确 | 版本/技能契约，人工规则对齐，README 原有改动保留，diff check | 强模型决定/复核；低成本执行明确文档改动 | Claude 适合导入链强审；Codex适合共同规则审查（本轮已做）；Grok可独立复审、Kimi/OMP可按清单改文档，后3者任务执行为候选 |
| C2 / P1 | PR/push 自动门禁，默认 pytest 不漏42项 | node-id 集合一致；just ci；full resource sync；Node20 docs build；workflow事件/权限审查 | 强模型审CI；低成本修改 YAML/配置 | Codex负责Windows/gh取证（已做）；Claude复审YAML；Grok/Kimi执行限定YAML改动、OMP可编排互不重叠检查，均为候选；hosted matrix未验 |
| C3 / P1 | Windows stream UTF8 不再崩溃 | 真实 subprocess Unicode 回归；三种环境原探针；paper-audit限定回归；lint/typecheck | 强模型根因/复核；低成本单函数执行 | Codex已有真实失败复现，优先协调修复；Claude可独立强审；Kimi或OMP窄worker执行为候选；必须回到真实Windows命令验收 |
| C4 / P1 | 五工具入口与安装能力透明 | 隔离完整布局无意外 missing；docs contract；资源同步；构建/导航检查 | 强模型核官方边界；低成本文档/测试执行 | Grok inspect已验证working-copy发现；Claude/Codex负责规则链复核；Kimi/OMP用于各自发现验证为候选，fresh session未验；不能由Codex代证其原生加载 |
| C5 / P2 | skill 不把 Claude 工具名当通用 API，无委派时诚实降级 | contracts、audit topology/synthesis、资源同步与build，人工语义复核 | 强模型学术/权限审查；低成本镜像同步 | Claude/Codex优先审lane与共识语义；Grok/Kimi原生委派、OMP task并行是候选执行路径，均需本机能力确认；无委派走顺序且不称独立panel |
| C6 / P2 | 证据分层、经验按工具回写项目 spec | 最终 just ci/sync/build，证据状态/所有权复核 | 强模型验收；低成本整理材料 | Codex汇总本地脚本证据；Claude/Grok可做独立强审候选；如扩展runtime，Claude/Codex/Grok/Kimi/OMP须各自运行取证，所有未跑项UNVERIFIED |

具体文件和逐项检查见各子任务 prd/design/implement；[父设计](design.md) 给出完整所有权表。

“候选”表示按已核官方能力推断适用，尚未在该工具的新会话执行本改造任务；不表示模型质量/价格已测。除明确写“已做”的本轮取证外，改造执行均待批准。能力来源与版本见 research/harness-rules.md；低成本取决于当次选用的模型和账户路由。

## 最终共同检查

从仓库根执行（本机命令经 rtk proxy）：

```text
just ci
uv run --extra dev python docs/scripts/check_resource_sync.py
just doc-build
uv run --extra dev python .trellis/tasks/09-07-five-harness-evergreen-audit/research/probe_isolated_audit.py
git diff --check
```

C3 后探针的 stream-only 场景必须从 exit1 变为 exit0，不能只看探针自身 exit0；探针是证据收集器，各子进程退出状态才是验收断言。C4 保留单skill受限布局时，standalone missing8 是已记录边界，推荐的完整布局 missing0 才是验收。

工作树的 git diff --check 基线失败位于 README_CN.md:14 原有推荐模型行末双空格。保留用户该行；必须检查本任务新增 diff 不引入空白错误，原有失败单独报告，不能为通过检查擅改原有片段。

对每个任务执行 `python .trellis/scripts/task.py validate <目录>`，确认上下文均为实际存在的 spec/research 文件；该验证器只验证结构，不代表用户批准或语义验收。

## 收敛与不扩张

- 75 条已有 Pyright warning 不批量清理；业务风险有新证据才另立项。
- 历史两处 dead links 已修复，不重做。
- ZIP 可复现性、release tag 的检查绑定、deploy job 权限下沉为后续建议；没有证据显示本次需重写打包脚本。
- 默认保持本机工具目录忽略，不批量生成或提交 hook/agent 资产，不更改全局环境。
- 推荐批准范围为静态规则与隔离脚本交付：六项子任务约定的代码/文档/本地检查/诚实台账通过即可完成此范围。五工具新会话、实际 npx 安装/软链接、Windows/Linux hosted matrix 与 current SHA 的远程状态未执行时保持 UNVERIFIED，属于另列的可选运行验证，不自动验收通过，也不作为该静态范围的隐藏阻断。
- 在缺少必要运行授权时，仅暂停相应 runtime 验收，不阻止其他已批准项；不得把规划或静态交付等同于全部运行兼容。

## 本轮交付前检查

- [x] R1–R7 均有证据或明确未验证边界。
- [x] 六个子任务均有 PRD/design/implement/两份实际上下文清单，无模板占位行。
- [x] 用户关于许可的选择已纳入 C1。
- [x] 独立强模型完成计划审查，6项发现已修订，复核GO/0阻断；见 research/planning-review.md。
- [x] git 状态仅增加本任务树，README 两处原改动未变。
- [x] 所有 task.json 为 planning，未执行 start/提交/正式回写。
