# 父任务执行与集成计划

当前阶段 planning；本轮只修改本任务树中的规划产物，不运行 start/finish/archive。

1. 审阅本版父子 prd/design/implement；使用 plan_precheck --include-descendants 和逐任务 task.py validate。
   所有上下文条目必须已存在，不能指向未来才新增的 spec。此门禁只证明结构。
2. 后续收到明确实施授权后，按 C1→C2→C3→C4→C5→C6 激活各子任务；
   每次先记录该子 baseline，再派发拥有独占文件范围的 implement/check agent。
   读取本子 manifests → prd → design → implement，原生注入失败时由子读取。
3. 每子按其 implement.md 完成目标测试、just ci、资源同步与 docs build，并记录命令、
   exit code、差异范围、MANUAL/NEEDS-LLM 与未运行证据；前子完整交付后再移交公共文件。
4. 父集成逐项核对 design 的 AC 矩阵：学院 MODULE 提示能触发 C2/C3 实际 CLI；
   新学院模板不使用旧学校阈值伪造 PASS；C1 的 degree 与 C2 school 开关组合不会重复输出；
   README/usage/SKILL/docs 的公开入口一致。遇到新改动才重跑相应门禁。
5. 汇总每子证据与仍需人工审查的条款；交付状态和批准状态分开。
   不因111行都有状态而宣称111项合规，不因静态检查绿色而宣称论文/宿主已验收。

## Validation commands

rtk proxy python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-22-thesis-zh-spec-sync-0922

plan_precheck 使用已安装 trellis-plan-review/scripts/plan_precheck.py，
参数为 .trellis/tasks/09-22-thesis-zh-spec-sync-0922 --include-descendants。
工具路径从当前技能解析，不把维护者个人绝对路径写入产品。

## Rollback

规划调整可按本轮明确文件清单复原；不清理其他未跟踪文件。
实施回滚按 design §6；公共文件逆序恢复对应子差异，禁止整目录删除。
