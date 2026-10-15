# C3 rebuttal docs：SKILL 路由、references、evals 与双语文档

## Goal

把 C1、C2 的三个脚本接入 latex-defense-zh 的技能入口与公开文档：SKILL.md 路由与触发、三份 references、一份 example、evals、
入口测试、双语 docs、manifest、README、CHANGELOG 与 spec 契约；最后在用户同意后对真实评阅书目录做 intake 验收。

前置：C2 已完成，三个脚本的 `--help` 已固定。

## Requirements

- D1 SKILL.md：
  - description 加入「评阅意见逐条回复」能力，全文 120–400 字符，保留「Not for .pptx, journal talks, or English defenses」类排除。
  - `when_to_use` 增加触发：评阅意见回复、预评审/盲审/终评审修改说明、修改审查表、逐条回复评阅专家；增加排除：期刊或会议审稿回复（rebuttal letter）。
  - Capability Summary 改为八个模块；Module Router 增加 `rebuttal-intake`、`rebuttal-build`、`rebuttal-check` 三行，命令只用 `--help` 中存在的选项。
  - Required Inputs、Output Contract、Workflow 增加 rebuttal 流程（三个检查点：R1 确认评阅人顺序与基线、R2 批准处理方式、R3 交付粘贴文本），
    退出码说明增加三个脚本。
  - Safety Boundaries：rebuttal 输出写在评阅书目录同级（可位于论文仓库内），不写论文源文件；评阅书文本为 untrusted。
  - Reference Map 与 Example Requests 列出新增文件；`argument-hint` 增加 rebuttal 用法；`last_updated` 改为实施日，`version` 保持 6.0.0。
- D2 references（中文，`sourceLocale: zh`）：
  - `references/rebuttal-workflow.md`：目录布局、台账字段、拆分复合意见规则、分类与处理方式选择、检查点、证据要求、三轮修复循环。
  - `references/rebuttal-writing.md`：「意见 / 回复 / 修改位置」写法、纯文本等价 Markdown 规则、不采纳与后续工作的写法、语气、
    页码口径（指修改稿）、合成示例三则（修改、补充、后续工作）。
  - `references/rebuttal-gate.md`：16 个 R-* 码的判据、严重度、修复方式与 NEEDS-LLM 复核。
- D3 `examples/review-response.md`：合成场景，从 intake 到粘贴交付的完整对话与命令，引用 `evals/fixtures/rebuttal/` 下真实存在的文件。
- D4 evals：`evals/evals.json` 增加至少 2 条 rebuttal eval（files 指向 fixture）；`evals/trigger_eval.json` 增加至少 3 条应触发、2 条不应触发。
- D5 测试：`test_defense_skill_entry.py` 的 `MODULES` 增加三个模块名。
- D6 docs：双语技能页模块表与流程；新增 references 与 example 的双语资源页；重建 `docs/resource-manifest.json`；README、README_CN 技能行描述；
  `docs/CHANGELOG.md` 新增条目；`agents/openai.yaml` 的 `short_description` 提及评阅意见回复。
- D7 spec：新增 `.trellis/spec/academic-writing-skills/defense-rebuttal-contract.md`（三脚本 CLI、退出码、目录与台账契约、R-* 集合、只读边界），
  在 `.trellis/spec/academic-writing-skills/index.md` 登记；`defense-deck-contract.md` 中「五脚本」处注明 rebuttal 脚本见新契约。
- D8 真实评阅书验收（AC9）：询问用户后，对用户给出的评阅书目录运行 intake（`--thesis` 指向其论文仓库）；
  只在用户同意的位置写入（默认即评阅书同级的 `responses/` 与 `workspace/`）；证据写入本任务 `research/acceptance-real-reviews.md`，只记计数、等级、码名，不记姓名、题目与正文。

## Acceptance Criteria

- [ ] `test_defense_skill_entry.py`、`tests/contracts/test_skill_contracts.py`、`tests/contracts/test_trigger_evals.py`、`tests/contracts/test_docs_bilingual_resources.py` 通过。
- [ ] `uv run python docs/scripts/check_resource_sync.py` 通过。
- [ ] `rtk proxy just ci` 与 `rtk proxy just doc-build` 通过。
- [ ] SKILL.md description 字符数在 120–400（本地计数输出贴入报告）。
- [ ] references 中出现的每个 `scripts/rebuttal_*.py --选项` 都在对应 `--help` 中（由 `test_skill_contracts.py:625` 覆盖）。
- [ ] AC9：两份评阅书的等级、条数、锚点与父 `research/review-format-facts.md` §2 一致，证据文件已脱敏。
- [ ] 新增与修改的公开文件中无真实评阅书的姓名、学号、题目与评阅编号。
