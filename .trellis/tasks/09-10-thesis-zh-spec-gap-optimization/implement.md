# 父任务执行与验收计划

## 已完成的规划阶段
1. 已完成58份 spec 覆盖、源码核对、候选来源筛选、G4/G5/G6 探针及105项基线。
2. 完成全部 PRD/design/implement 和真实 JSONL context。
3. 运行 plan_precheck --include-descendants、task.py validate（全部四任务）；
   独立规划审阅发现问题时只修规划再复核。
4. 已向用户交付分析和任务清单；2026-09-10 收到明确实施授权后进入下列实施阶段。

## 实施（2026-09-10 已获用户授权）
1. 复核 HEAD/dirty 与任务边界；确认用户批准的是当前版本的父子计划。
2. 按 C1→C2→C3 调度 trellis-implement/trellis-check，注入对应真实 JSONL；
   worker 不再递归派生同类 implement/check。
3. 每 child 公开资源写完，主会话串行刷新 manifest，让 child 跑局部门禁。
4. 主会话依据已验证经验更新 testing-and-tooling/index，并保留 source 规则单点所有权。
5. 所有局部测试通过后跑最终 gate，不无故重复验证：
```powershell
rtk uv run --no-sync python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk uv run --no-sync python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
rtk uv run --no-sync python docs/scripts/check_resource_sync.py
rtk just ci
rtk just doc-build
rtk git diff --check
```
just ci 的四步是 check-versions、lint、typecheck、test。既有 Pyright warnings 不批量清理；
资源检查和 docs build 是独立门禁。只把当前实际结果写入 research/integration-validation.md。
若全树 diff-check 涉及原有用户行，分别记录本任务结果与原有问题，不擅自修复。
6. 独立检查全部三子任务源码与 AC，逐项保留 failed/skipped/missing evidence。
7. 向用户报告实际产物和未验项目；提交、归档、发布遵循后续明确授权。
   不因 task.py validate 或绿色单测自动启动下一阶段。

## 规划检查入口
从仓库根使用本会话已定位的 trellis-plan-review 技能 scripts/plan_precheck.py：
`python -X utf8 <resolved-skill>/scripts/plan_precheck.py .trellis/tasks/09-10-thesis-zh-spec-gap-optimization --include-descendants`。
<resolved-skill> 运行时按技能目录解析，不把维护者私有绝对路径写进项目合同。
各任务 `python -X utf8 .trellis/scripts/task.py validate <task-dir>` 必须有真实 context。
任务关系由 task.json.children/parent 双向记录，依赖由本计划明确，不假设父子关系自动排程。

## 回滚边界
C1/C2/C3 各自精确逆向 diff；父任务只回滚本次 manifest/spec 改动。
不影响 .gitignore、.trellis/.template-hashes.json、skills-lock.json 原有改动；
不删除论文源/产物，不整份回退多个子任务共享的测试文件。
