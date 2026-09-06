# 集成验收与证据回归

父任务：[09-06-paper-audit-intake-delivery](../09-06-paper-audit-intake-delivery/prd.md)
承担父需求 R8 及跨子任务合并验收。

## Goal

为前两个子任务的行为改动补可复跑的 eval 用例，
同步 VitePress 双语说明页，做一次完整集成检查，
并按 qiaomu-meta 证据分层输出交付说明。

## Background

`academic-writing-skills/paper-audit/evals/trigger_eval.json` 结构为
`{"skill_name", "queries": [{"query", "should_trigger", "category"}]}`，
现有条目均为触发边界用例，不覆盖门控与交付形态。

`academic-writing-skills/paper-audit/evals/evals.json` 结构为
`{"skill_name", "evals": [{"id", "prompt", "expected_output", "files", "assertions"}]}`，
assertion 类型含 `contains` 与 `regex`。
现有第 1 条已用 `\[(Script|LLM)\]` 正则验证 provenance，可复用同一手法验证 T3 下一律 `[LLM]`。

已知陷阱：用 Edit/Write 改 `evals.json` 会触发 JSON 格式化 hook 压平数组，
必须走 Bash 里的 python 写入。

`docs/skills/paper-audit/index.md` 与 `docs/zh/skills/paper-audit/index.md`
第 12、27、45、52、63、155 行多处把 review workspace 描述为 deep-review 的固有产物，
未提及禁止落盘的情形。两份页面是手写页，不由 `resource-manifest.json` 托管。

## Requirements

- R1（触发用例）：`trigger_eval.json` 新增覆盖门控与交付形态的 query，
  包含已指定模式 + 存在旧报告、以及明确禁止落盘两类。
- R2（行为用例）：`evals.json` 新增用例，断言
  已指定模式时不产生模式选择题、T3 下不出现 `review_results`、
  T3 下结论标 `[LLM]` 且列出 `missing evidence`。
- R3（双语说明页）：`docs/skills/paper-audit/index.md` 与其 zh 对应页
  补一节说明三级交付形态与不落盘路径，与源文件表述一致。
- R4（集成检查）：`just ci`、`docs/scripts/check_resource_sync.py`、`just doc-build` 全通过。
- R5（证据标注）：交付说明按 design advantage / validated advantage / hypothesis 三档标注每条改进；
  未取得的证据写 missing evidence，不以计划充当证据。
- R6（跨子任务一致性）：`MODE_GUIDE.md` 的门控措辞与 `SKILL.md` 的三级边界表述
  不冲突、不重复定义同一概念。

## Acceptance Criteria

- [x] AC1（R1）：`trigger_eval.json` 至少新增 2 条 query，`should_trigger` 与 `category` 字段齐全，
      JSON 结构与现有条目一致。
      → 新增门控（旧报告）与禁止落盘两条，`category` 均为既有取值 `edge`；
      改后实测 20 条 / 13 正 / 7 负，`tests/contracts/test_trigger_evals.py` 全通过。
- [x] AC2（R2）：`evals.json` 至少新增 2 条用例，
      每条含 `id`、`prompt`、`expected_output`、`assertions`；
      T3 用例含一条断言 `review_results` 不出现，一条断言含 `missing evidence`。
      → eval 24（已指定模式 + 旧报告）与 eval 25（T3 不落盘），四键齐全；
      eval 25 含 `not_contains: review_results` 与 `contains: missing evidence`。
      两条均绑 `evals/fixtures/quick_audit_fixture.tex`，满足
      `test_skill_contracts.py:417` 的 `files` 非空且路径存在约束。
- [x] AC3（R2）：`evals.json` 改动通过 Bash python 写入，
      改后 `git diff` 中现有条目的数组格式未被压平。
      → `git diff` 为 23 行纯新增，既有条目零 diff。
- [x] AC4（R3）：两份 index.md 新增节内容与
      `SKILL.md` 三级边界、`workflow-detail.md` 不落盘节表述一致，无第三种说法。
      → en/zh 各 18 行新增、逐条对应。核对中发现 C2（`--output` 的 `T2` 允许动作被误禁），
      已在本子任务的两份 index.md 内改正；详见 `research/consistency-check.md`。
- [x] AC5（R4）：`just ci` 通过；`uv run python docs/scripts/check_resource_sync.py` 通过；
      `just doc-build` 通过。
      → `just ci` exit 0（`1756 passed in 117.28s`）；
      `check_resource_sync.py` exit 0（`all resources (271 manifest entries)`）；
      `just doc-build` exit 0（`build complete in 14.91s`）。
      后两条在回退 en index.md 表格对齐噪声后于最终工作树状态复跑。
- [x] AC6（R5）：交付说明逐条标注证据档位；
      至少明确列出本轮未做的验证（真实论文盲评、跨平台安装、独立第三方复核）为 missing evidence。
      → `research/delivery-notes.md`，三档逐条标注；
      missing evidence 共 6 项，含指定的三项，另加 `deep-review` 落盘未实跑、
      eval 断言未真实执行、部署副本未同步。
- [x] AC7（R6）：逐句核对 `MODE_GUIDE.md` 门控段与 `SKILL.md` 三级边界段，
      记录核对结果；发现冲突时回退到对应子任务修正，不在本子任务里改那两份源文件。
      → `research/consistency-check.md`，3 项发现。
      C1（交付级别冲突未列入实质冲突定义）回退 intake-gating 改 `MODE_GUIDE.md`；
      C3（`--overwrite` / `--overwrite-workspace` 归属错配）回退 delivery-tiers 改 `SKILL.md`；
      C2 落在本子任务拥有的 index.md 内，就地修正。

## Out of Scope

不改 `SKILL.md`、`MODE_GUIDE.md`、`workflow-detail.md`、`output-layout.md`
——发现问题回退到对应子任务修正。
不改任何脚本。不新增 fixture 之外的测试基础设施。
不提交、不推送、不发布、不归档。
