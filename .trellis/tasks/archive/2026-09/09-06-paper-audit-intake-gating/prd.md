# 意图门控：显式模式不再复问

父任务：[09-06-paper-audit-intake-delivery](../09-06-paper-audit-intake-delivery/prd.md)
承担父需求 R1、R2、R8。

## Goal

把 `MODE_GUIDE.md` 的 `### Auto-Detection at Intake` 从无条件提问改为条件提问：
用户已显式指定模式时直接执行，检测信号降为一句上下文陈述；
只有会改变审查范围或结论的实质冲突才升级为提问。

## Background

`academic-writing-skills/paper-audit/references/MODE_GUIDE.md:30-56` 现状：
小节前言写 "Surface these conditions to the user as a prompt"，
四条 bullet 分别以 "ask whether the user wants `re-audit` mode"、
"ask whether this is a revised submission"、
"ask whether `deep-review` is more appropriate"、
"dispatch `agents/revision_coach_agent.md` first" 收尾，
收尾句 `MODE_GUIDE.md:53-56` 写 "let the user confirm or decline"。
四条都不检查用户是否已经指定了模式。

`MODE_GUIDE.md:24-26` 的 re-audit 前置条件：
"If it is missing, stop immediately and ask only for that path"。
codex 要求保留该依赖，但允许"路径可从现有上下文唯一确定时先自行查找"。

不可动的字面：`tests/skills/paper_audit/test_paper_audit_synthesis.py:106-111`
断言 `MODE_GUIDE.md` 含 `Auto-Detection at Intake`，
且该小节含 `revision_coach_agent` dispatch。

## Requirements

- R1：小节开头加前置分支——用户已在请求中显式指定模式时，
  四类检测只作一句陈述，不生成模式选择题。
- R2：给出"实质冲突"的可判定定义：
  检测信号会改变审查范围（纳入或排除章节、改变对比基线）
  或会改变结论（改变 gate 的 PASS/FAIL、改变 issue 严重度）时才提问。
- R3：模式未由用户指定时，四类检测的现有提问行为不变。
- R4：`--previous-report` 缺失时，先在论文目录与当前工作目录查找候选；
  恰好一个候选时陈述该路径并继续，零个或多于一个时停下只问该路径。
- R5：保留 `Auto-Detection at Intake` 标题字面与 `revision_coach_agent` dispatch 字面。
- R6：`MODE_GUIDE.md` 的 sha256 更新进 `docs/resource-manifest.json`，
  en/zh 两份镜像同步。

## Acceptance Criteria

- [x] AC1（R1）：`MODE_GUIDE.md` 中四条检测 bullet 各自区分"模式已指定"与"模式未指定"两种响应。
- [x] AC2（R2）：实质冲突定义在文中可独立引用，附一个提问正例与一个不提问反例，
      两例差别只在冲突是否影响范围或结论。
- [x] AC3（R1）：给定输入"对 paper.tex 跑 quick-audit"且同目录存在 `audit_report_2026-08.md`，
      按新规则的实际响应中不出现模式选择题；检测信号以陈述句出现。
      验收依据是保存的实际模型响应，不是关键字存在。
- [x] AC4（R3）：给定输入"帮我看看这篇论文"（未指定模式）且存在同一旧报告，
      实际响应仍提出 re-audit 询问。
- [x] AC5（R4）：`MODE_GUIDE.md:24` 段落改为查找—唯一则陈述—否则询问的三分支，
      re-audit 对前次报告的依赖未被移除。
- [x] AC6（R5、R6）：`uv run --extra dev python -m pytest tests/skills/paper_audit tests/contracts -q` 通过；
      `uv run python docs/scripts/check_resource_sync.py` 通过。

## Out of Scope

不改 `SKILL.md`、`workflow-detail.md`、`output-layout.md`（属 delivery-tiers 子任务）。
不改 evals（属 verify 子任务）。不改任何脚本。不新增或删除检测类别。
不移除任何现有的必要确认。
