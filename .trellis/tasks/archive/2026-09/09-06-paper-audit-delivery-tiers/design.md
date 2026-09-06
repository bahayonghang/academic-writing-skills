# 设计

## 改动面

三份源文件：
`academic-writing-skills/paper-audit/SKILL.md`、
`academic-writing-skills/paper-audit/references/workflow-detail.md`、
`academic-writing-skills/paper-audit/references/output-layout.md`。

附带 `docs/resource-manifest.json` 中 `workflow-detail.md` 与 `output-layout.md`
两条 sha256，及各自 en/zh 共四份镜像。`SKILL.md` 不在 manifest 中。

## 三级定义

| 级别 | 名称 | 增量禁止 | 允许 |
| --- | --- | --- | --- |
| T1 | 不得修改论文 | 改写 `.tex` / `.typ` / `.pdf` 源文件 | 建工作区、写报告与 artifacts |
| T2 | 不得写入仓库 | 在论文仓库或本仓库工作树内写任何文件 | 在用户指定的仓库外目录落盘 |
| T3 | 完全不得落盘 | 写入任何位置 | 只在对话中返回结论 |

T1 是默认级别，沿用 `SKILL.md:61` 现有条款，不改其语义。
T2 与 T3 为新增。级别单调收紧，高级别继承低级别的全部禁止项，因此无重叠。

## T3 路径

清单由 2026-09-06 实跑定稿，见 [write-behavior.md](research/write-behavior.md)。

T3 可用：`quick-audit`、`gate`、`re-audit`——三项均有实跑证据（validated）。
T2 与 T3 均排除：`polish`——写 `.polish-state/` 到论文目录（`audit.py:2509`，validated）。
T3 排除：`deep-review`——必然建 `./review_results`（静态证据，design 级，未实跑）。

deep-review 在 T3 下不可用是硬事实，不做变通。
文档给出的降级选项是 quick-audit 或 gate，并明说能力差距：
没有委员会 agent 多视角、没有 section/cross-cutting lane、
没有 consolidation 去重与 root-cause 归并、没有 quote 校验。

## 证据缺失声明

T3 下不可运行的脚本按名列出，来源是 `references/workflow-detail.md:14-21` 的
consolidation 命令序列：
`consolidate_review_findings.py`、`verify_quotes.py`、
`render_deep_review_report.py`、`render_html_report.py`。
每项标 `missing evidence`，措辞统一，不允许写成"已用对话方式完成等效检查"。

## 不冒充

沿用 `SKILL.md:63` 已有的 `[Script]` / `[LLM]` provenance 规则，
补一句：T3 下所有结论均为 `[LLM]`，不得标 `[Script]`。
不新造标记体系，不新增字段。

## 目录明确

`SKILL.md:134` 的 Phase 1 行保留命令形态，
补一句要求：执行前把 `--output-dir` 解析后的实际目标路径念给用户。
`output-layout.md` 在工作区根小节前补同一要求。
覆盖行为不动，仍走 `workflow-detail.md:6-12`。
不改 `prepare_review_workspace.py:952` 的默认值。

## 泛化边界

升级为规则：权限约束决定交付形态；无法运行的检查显式声明缺证据而非静默降级。
保留为条件指引：`review_results` 这一具体目录名、四个脚本的具体文件名。
拒绝：不把 T3 设为默认；不为 T2/T3 新增 CLI flag——级别是对话约定，不是参数。

## 验收分层

`pytest` 与 `check_resource_sync.py` 证明形状与同步。
AC3 需要实跑记录。AC6 是 LLM 行为验收，须保存实际响应逐项审阅。
真实论文场景与跨平台验证本轮不做，写 missing evidence。

## 回退

三份源文件、四份镜像、两条 manifest sha256 同进同退。
`SKILL.md` 单独回退时须复跑 `tests/contracts/test_claim_evidence_contract.py`。
