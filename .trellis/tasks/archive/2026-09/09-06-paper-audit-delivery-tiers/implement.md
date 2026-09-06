# 实施计划

## 阻塞前置：落盘行为实跑（已完成 2026-09-06）

四个模式已在独立空目录中各跑一次，结果记入 [write-behavior.md](research/write-behavior.md)。
结论：T3 可用 `quick-audit` / `gate` / `re-audit`；
`polish` 因写 `.polish-state/` 到论文目录而在 T2 与 T3 均排除；
`deep-review` 按静态证据排除，未实跑。

## 顺序

1. ~~完成实跑，定稿 T3 可用模式清单~~ — 已完成，见上。
2. 改 `SKILL.md`：`## Critical Rules` 增三级边界段；
   `SKILL.md:134` Phase 1 补目标目录陈述要求；补 T3 下结论一律 `[LLM]` 一句。
3. 改 `references/workflow-detail.md`：新增不落盘路径一节，
   含 T3 可用模式、deep-review 不可用与降级能力差距、四个脚本的 `missing evidence` 清单。
   不改第 6-12 行覆盖确认段落。
4. 改 `references/output-layout.md`：工作区根小节前补目标目录陈述要求。
5. 同步 `workflow-detail.md` 与 `output-layout.md` 的 en/zh 四份镜像
   与 `docs/resource-manifest.json` 两条 sha256。
6. 跑 AC6 行为验收，保存实际响应到 `research/`。

## 验证命令

```bash
uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q
uv run python docs/scripts/check_resource_sync.py
git diff -- academic-writing-skills/paper-audit/SKILL.md
```

`git diff` 用于 AC9：确认 frontmatter 的 `allowed-tools` 与 `argument-hint` 未变。
manifest sha256 用 `docs/scripts/check_resource_sync.py` 同算法重算，不手写。

## 审查门

- 步骤 1 未完成不得进入步骤 3 的 T3 清单撰写。
- 步骤 2 完成后跑 `pytest tests/contracts/test_claim_evidence_contract.py -q` 再继续。
- 步骤 6 失败时回步骤 2-4 改措辞，不改测试、不改脚本。

## 回退点

步骤 2、3、4 各自独立可回退。
步骤 5 的镜像与 manifest 必须与对应源同进同退。
