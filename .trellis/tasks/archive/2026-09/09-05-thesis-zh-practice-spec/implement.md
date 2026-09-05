# 实施计划

## 开始条件与顺序

- [x] 用户已于 2026-09-05 在最新规划交付后明确批准实施，可激活实际交付子任务。
- [x] 重新核对 HEAD d5e5444、dirty（仅本任务四目录）、任务状态及所有 context 路径。
- [x] 按 evidence-writing → engineering-chapter → punctuation-prose → caption-layout 执行；公共资源串行写，punctuation-prose 为用户实施中明确追加。
- [x] 各子任务先做自身正反例/回归和双语同步，再交接。
- [x] 父任务汇总实际 AC 证据并做一次完整集成检查；提交、归档和发布另依授权。

## 本轮规划检查

```powershell
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-05-thesis-zh-practice-spec
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-05-thesis-zh-evidence-writing
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-05-thesis-zh-engineering-chapter
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-05-thesis-zh-caption-layout
python -X utf8 C:/Users/lyh/.agents/skills/trellis-plan-review/scripts/plan_precheck.py .trellis/tasks/09-05-thesis-zh-practice-spec --include-descendants
rtk git diff --check
```

独立审阅检查源/目标证据、需求映射、泛化边界、实际 CLI、eval 方法和单写者；
结果记录 research/planning-review.md。结构通过不代表实施授权或产品验收。

## 未来集成检查

```powershell
uv run --extra dev python -m pytest tests/skills/latex_thesis_zh tests/contracts -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
rtk git diff --check
```

目标测试先行，最后统一完整 CI/docs build，通过后不重复扩大。
失败区分本任务引入与既有问题；缺模型/TeX/渲染工具时不补装或假报通过。
公共文件风险为入口、路由、eval、双语 usage、README/README_CN 和 manifest。
只回退确切增量，不覆盖其他会话工作。
