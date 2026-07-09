# implement — 通用规范逐项终检机制与燕山2024清单

> 前置：`Skill(trellis-before-dev)` 已读 `.trellis/spec/academic-writing-skills/testing-and-tooling.md`
> （zh 副本测试必须 importlib 按路径加载 + 加载守卫；路径常量从 `tests.support.paths` 导入；
> evals.json 用 Bash python 写入；SKILL.md 表格改动后必跑 router 契约测试）。

## 步骤

1. **重写 `templates/yanshan.md`** → verify: 人工对照
   `research/yanshan-2024-spec-extracted.txt` 抽查 10 条 § 依据无编造。
   - 结构：规范信息 / 内容要求要点 / 书写要求要点 / 排版与打印要点 / `## 逐项检查清单`
     （design §4 的 YS-01~55 映射）/ 学术不端检测（保留现有）/ `## 盲审`（占位一行，
     由 07-08-blind-review 填充）。
   - 条目字段照 design §2 契约；文首"非模板事实快照"的免责说明更新为
     "2024 版规范快照（源：学位办 2024 年 6 月发文 PDF）；排版实现仍以学校官方模板为准"。
2. **新增 `scripts/check_spec.py`**（parse_checklist + CHECKERS 16 个 + TEMPLATE_THRESHOLDS +
   报告/JSON 输出）→ verify:
   `uv run python academic-writing-skills/latex-thesis-zh/scripts/check_spec.py academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex --template yanshan --degree doctor`
   正常输出逐项报告；`--json | python -m json.tool` 可解析。
3. **fixture 埋点**：在 `evals/fixtures/thesis-project/` 预埋 ≥3 个可判 FAIL 的违规点
   （建议：结论章加一处 `\cite` + 关键词只放 2 个 + 一个 >15 字节标题），埋点处加
   `% seed:` 注释注明服务的检查器（沿用 fixture 工程埋点联动约定）→ verify: 步骤 2 命令
   出现对应 FAIL 且证据行号正确。
4. **新增 `references/modules/spec-check.md`**：五步工作流 + NEEDS-LLM 逐项判读指引
   （每条引用 yanshan.md 的 § 依据原文）+ manual 项输出为"打印前自查单" + 输出契约行格式。
5. **SKILL.md**：router 增 `spec-check` 行、路由规则一条（触发词：对照规范逐项检查/终检/
   定稿检查/规范符合性/盲审前格式自查）、Example 一条、`when_to_use` 补短语、
   `last_updated` 改今日、`version` 不动 → verify:
   `uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py tests/contracts/test_skill_versions.py -q`。
6. **trigger evals**：用 Bash python 向 `evals/trigger_eval.json` 追加 1~2 条正例
   （"帮我对照燕山大学2024规范逐项终检这篇论文"）→ verify:
   `uv run --extra dev python -m pytest tests/contracts/test_trigger_evals.py -q`。
7. **新增 `tests/skills/latex_thesis_zh/test_check_spec.py`**（importlib 加载 + 加载守卫断言
   + 每个 checker 至少一正一反用例 + --spec-file 未知检查器降级用例 + SKIP/degree 用例）
   → verify: `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_check_spec.py -q`。
8. **新增 `tests/contracts/test_spec_checklists.py`**（design §5 四项锁）→ verify: 同文件 pytest。
9. **全量回归** → verify: `just ci` 全绿（关注 pyright error 数，basic 模式 error 会卡门禁）。

## 回滚点

- 步骤 1~2 各自独立可回退（yanshan.md 与新脚本互不引用，靠清单契约耦合）；
  契约测试（步骤 8）落地前允许中间态不一致，但提交前必须成对。
- SKILL.md 若被 hook 重排且契约测试红：`git checkout -- academic-writing-skills/latex-thesis-zh/SKILL.md`
  后重做最小编辑。

## 审查门

- 提交前自查：新增行是否都能追溯到 prd 需求；yanshan.md 无编造条目；
  `\cite`/`\ref`/`\label`/math 零触碰；报告行格式带 `[Script]`/`[LLM]` 标注。
