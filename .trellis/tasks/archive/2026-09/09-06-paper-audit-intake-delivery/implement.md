# 实施计划

## 开始条件与顺序

- [ ] 用户已批准实施（当前仅批准建任务与规划，实施须另行确认）。
- [ ] 重新核对 HEAD、工作树状态、三个子任务的 planning 工件齐全。
- [ ] 先做前置实跑确认（见下节），确认结果写入 delivery-tiers 的 research 记录。
- [ ] 按 intake-gating → delivery-tiers → verify 串行执行；公共资源串行写。
- [ ] 各子任务先完成自身正反例审阅与双语/manifest 同步，再交接。
- [ ] 父任务汇总实际 AC 证据并做一次完整集成检查；提交与归档另需授权。

## 前置实跑确认（阻塞 R4 定稿）

设计中"quick-audit / gate / polish / re-audit 不落盘"目前只有静态证据
（`scripts/audit.py:2704` 与 `audit.py:1961`）。在写 T3 路径清单前先实跑：

```bash
uv run python -B academic-writing-skills/paper-audit/scripts/audit.py <fixture>.tex --mode quick-audit
```

在一个空临时目录中对每个候选模式各跑一次，运行前后各列一次目录内容，
记录实际新增的文件。实跑结果与静态推断不一致时，以实跑为准缩减候选清单。
无法实跑时，把该模式标为 `missing evidence`，不写入 T3 可用路径。

## 本轮规划检查

```bash
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-06-paper-audit-intake-delivery
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-06-paper-audit-intake-gating
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-06-paper-audit-delivery-tiers
python -X utf8 .trellis/scripts/task.py validate .trellis/tasks/09-06-paper-audit-intake-delivery-verify
```

规划结构通过不代表实施授权或产品验收。

## 集成检查

```bash
uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q
uv run python docs/scripts/check_resource_sync.py
just ci
just doc-build
```

目标测试先行，最后统一跑完整 CI 与 docs build。
失败区分本任务引入与既有问题。缺工具时不补装、不假报通过。

## 风险与回退

- 公共文件风险点：`MODE_GUIDE.md`（两处测试读取）、`SKILL.md`
  （`test_claim_evidence_contract.py:79` 读取）、`docs/resource-manifest.json`
  （三条 sha256 + 六份镜像页）。
- 门控措辞改动可能让 `test_paper_audit_synthesis.py:106` 的
  `Auto-Detection at Intake` 或 `revision_coach_agent` 断言失配——
  改动时保留这两处原字面，只在其外侧加条件分支。
- 只回退当前子任务的确切 diff，不覆盖其他会话工作。
