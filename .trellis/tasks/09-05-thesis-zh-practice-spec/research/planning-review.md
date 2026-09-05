# 独立规划审阅与验证记录

- 日期：2026-09-05。
- 范围：09-05-thesis-zh-practice-spec 及三个递归子任务，统一审阅。
- 审阅者：独立 trellis_plan_auditor 角色（只读）；主线程负责工件修订与本记录。
- 结论：GO，仅表示规划可交接；不代表实施授权或产品 AC 已通过。
- 最终确定阻断：0；待修问题：0。

## 审阅与修订

独立审阅检查 PRD/design/implement/JSONL、源/目标证据、需求—验收映射、
现有 CLI 和测试面、共享文件串行写、隐私/泛化边界，以及模型/视觉证据分层。

发现并完成一项追溯修订：caption-layout 原 R5 要求 eval 同步，但 design/AC/命令
没有说明如何实现。现已在该子任务 design 的“文档行为评测”补两个 output 场景
（合法双语题注结果一致、只有DPI不能宣称视觉通过）和一个 trigger 正例；
AC6 与 implement 的语料契约命令同步补齐。独立审阅复核确认闭合。

审阅中关于正式报告应位于 .trellis/reviews 的疑问已撤回：本轮是创建规划过程的
personal auditor 只读检查，并未启动 trellis-plan-review 独立技能工作流；
plan_precheck.py 作为机械工具使用不改变本任务报告归属。本文件是唯一最终审阅记录。

## 机械与结构验证

- plan_precheck.py 原参数（父任务 + --include-descendants）：4 tasks，
  20 requirements、25 acceptance criteria；0 blocking、0 placeholders、
  0 referenced-but-undefined；5 个规划正文源码引用全部 resolved。
- task.py validate：四任务全部通过。implement/check 各有真实条目
  9/9/9/4，均无 seed-only manifest。
- 四任务 PRD/design/implement 与两类 context 文件齐全；parent/children 双向一致。
- 四任务 status 均为 planning；task.py current 无输出，没有激活任务。
- git diff --check 通过；工作树仅新增四个任务目录。
- 规划文件的额外换行扫描曾发现 task.py 生成的父元数据缺末尾换行；
  父任务 notes 更新时已规范化，不涉及产品行为。

机械/JSON 检查只证明工件可读和可追溯，不证明语义质量；GO 来自独立语义审阅。

## 规划时点实际完成与未来证据

已完成：28 份源 spec 覆盖、当前实现对照、公开先例来源阅读、题注识别的内存正反对照、
CLI --help 核验、四任务规划、结构验证与独立审阅。

未执行：技能修复、产品 pytest/just ci、docs build、真实论文编译、
新增 output/trigger 模型运行、PDF视觉检查、独立人工盲评、安装和跨平台评测。
这些是未来实施证据，保持 missing evidence，所有产品层 AC 保持未勾选。

后续必须先获得用户对最新规划的明确实施批准，再激活实际交付子任务；
不得由本记录的 GO 自动执行 task.py start。

## 后续授权与范围追加

2026-09-05 用户随后明确要求“请开始实施”，并追加中文正文冒号/分号与句间逻辑规则。
原规划审阅结论保留为历史证据；新增 punctuation-prose 子任务纳入父树并完成 context 验证，
五任务递归预检无 blocking。产品实施证据分别记录在各子任务 research 下，最终由父任务集成审阅；
不将本文件的规划 GO 作为产品通过证明。
