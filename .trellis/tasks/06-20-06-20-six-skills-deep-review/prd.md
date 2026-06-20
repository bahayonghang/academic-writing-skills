# 六技能深度复审与优化

## Goal

对 `academic-writing-skills/` 下六个 skill 做归档后的独立复审（四视角：正确性与合规、skill 工程质量、跨技能一致性、真实可用性/边界），并修复复审中发现的问题。

## 复审结论（2026-06-20）

复审手段：完整读 6 份 SKILL.md 契约；全部 ~80 个脚本 `py_compile` 通过；SKILL.md 路由所宣称的关键 CLI flag 全部在脚本 argparse 中命中；ScholarEval 权重和=1.00；`--online`/`--literature-search`/`--scholar-eval`/`--tavily-key`/`--s2-key`/`--regression` 均真实存在；版本字段全为 5.2.0 与 pyproject 一致。

**未发现正确性 bug，未发现红线违规。** 这是对一个刚经历 F1–F24 + 五技能优化、824 测试全绿的套件做复审的预期结果。发现集中在跨技能一致性与文档完备性：

| ID | 视角 | 严重度 | 位置 | 问题 | 修复方向 |
|---|---|---|---|---|---|
| C1 | 一致性/契约 | 中 | latex-thesis-zh/SKILL.md:23 | 唯一一个用 `argument_hint`（下划线）且缩进在 `metadata:` 下；其余 5 个均为顶层 `argument-hint:`（连字符）。破坏全仓 frontmatter 约定，该字段不被识别。 | 改名为顶层 `argument-hint:` 并退到顶层缩进。 |
| C2 | 一致性 | 低 | latex-thesis-zh/SKILL.md | 唯一缺 `when_to_use:` 字段的 skill（其余 5 个都有），触发词全挤进 description。 | 抽出 `when_to_use:` 块，与兄弟 skill 路由结构对齐。 |
| C3 | 一致性/可维护性 | ~~中~~ → **误报** | */scripts/parsers.py | 初判为副本 API 面漂移；**实施时发现是误报**：分歧由 `tests/test_parsers_alignment.py` 显式设计、文档化（docstring + ALIGNMENTS 映射）并测试锁定（`test_clean_text_is_canonical_only` 断言 zh 不含 clean_text）。非漂移，无需改 parsers.py。 | 已文档化，仅在 CLAUDE.md 补一行指针提升可发现性。 |
| A1 | 工程质量/文档 | 低 | paper-audit/SKILL.md | Scripts 表与正文未提及 scholar_eval.py / scoring_model.py / literature_search.py / literature_compare.py，但 argument-hint 暴露了 `--scholar-eval`/`--literature-search`。 | 在 Scripts 表补列并一行说明，或注明为进阶可选路径。 |

## Requirements

- R1：修复 C1——latex-thesis-zh frontmatter `argument_hint`(metadata 内, 下划线) → 顶层 `argument-hint:`(连字符)，值不变。
- R2：修复 C2——为 latex-thesis-zh 增补顶层 `when_to_use:` 块，从现有 description 提炼触发词，不改 description 语义。
- R3：处理 A1——paper-audit SKILL.md Scripts 表补列 4 个未列脚本并各一行用途说明。
- R4：处理 C3——按评审决定执行 (a) 文档化或 (b) 最小对齐；默认推荐 (a) 在各 parsers.py 顶部加一行"副本，故意精简，勿盲目对齐"注释 + 在 CLAUDE.md 既有约定旁补一句，避免过度工程。
- 全程遵守全仓红线：不改 \cite/\ref/\label/数学环境、不编造、不改受保护术语、不 bump version（只在被改 SKILL.md 更新 last_updated）。

## Acceptance Criteria

- [x] R1：6 个 SKILL.md 的 frontmatter 均为顶层 `argument-hint:`，无 `argument_hint`。
- [x] R2：6 个 SKILL.md 均含顶层 `when_to_use:`。
- [x] R3：paper-audit Scripts 表含 scholar_eval/scoring_model/literature_search/literature_compare 四行。
- [x] R4：C3 实施时确认为误报（已被 test_parsers_alignment.py 文档化+锁定）；仅在 CLAUDE.md 补一行指针，未改 parsers.py。
- [x] 被修改的 SKILL.md 仅更新 `last_updated`，`version` 仍为 5.2.0。
- [x] `just ci` 全绿（lint + typecheck + 826 测试），与复审前一致。

## Notes

- 这是轻量任务：改动以 SKILL.md frontmatter / 文档为主，无脚本逻辑改动（除 R4 方案 b 才动 parsers.py 注释）。
- C3 是唯一需要评审拍板的设计点，已在 R4 给出默认推荐。
