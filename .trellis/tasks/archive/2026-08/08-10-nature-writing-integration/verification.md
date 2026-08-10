# Verification - 08-10-nature-writing-integration

## 结论

父任务跨子任务终检通过，未发现需要修改的产品问题，也未做产品修复。终检直接审查了 EN
产品提交 `a136e6d` 与 ZH 产品提交 `db1424b`；未以两个子任务的 verification 自述替代代码、
文档、测试和构建证据。

## 提交与范围证据

- 基线为 `f0748cf`。EN 产品提交 `a136e6d` 先落地，ZH 产品提交 `db1424b` 后落地，符合
  manifest 串行依赖；`23511fb`、`69b40c4` 仅归档子任务。
- `git diff f0748cf..HEAD -- academic-writing-skills tests docs` 显示产品范围只包含 EN
  references/SKILL、ZH 两份写作参考与 `analyze_abstract.py`、B-NAT 测试，以及对应双语资源和
  manifest。
- EN 的 `analyze_abstract.py`、`optimize_title.py`、`check_tables.py`，整个 `typst-paper`、
  `paper-audit`、`tests/contracts/test_writing_modules_alignment.py` 均相对基线零改动。
- deai 对齐文件、所有 `parsers.py` 副本及其对齐契约相对基线零改动。ZH 脚本目录仅
  `scripts/analyze_abstract.py` 变化，且该提交只在 `_run_bilingual()` 追加 B-NAT。

## N1-N19 差量核对

| 项 | 终检结果 | 实现或不实现证据 |
| --- | --- | --- |
| N1 | PASS | `latex-paper-en/references/writing/article-architecture.md` 的 Full-Paper Argument Chain 明确包含 need、bottleneck、move、evidence、implication、boundary。 |
| N2 | PASS | 同文件 Journal-Style Abstract Moves 提供六步期刊式模式，并明确与既有三种摘要模式并列、非替代。 |
| N3 | PASS | EN 同文件 Abstract Diagnostics 为三条 `[LLM] / Info / P3` 候选；ZH `analyze_abstract.py:1099` 仅在找到英文摘要时追加一条 `B-NAT`，为 `[LLM]`、`level=Info`、`flagged=false`。 |
| N4 | PASS | EN Results Evidence Ladder 含六层顺序和 `To test [question], we [action].` 的 claim-first 模式。 |
| N5 | PASS | EN Discussion Widening 含六步扩展、不逐图复述，并交叉引用既有 Discussion Layering。 |
| N6 | PASS (reject) | 既有 `section-writing/conclusion.md` 未改，未复制结论四段式。 |
| N7 | PASS | `references/modules/title.md:113` 增加 doc-only `[LLM]` 公式和 prestige 词具体化要求；`optimize_title.py` 未改。 |
| N8-N10 | PASS (reject) | 既有 abstract/introduction/method 章节指南未改，未重复移植同源模板。 |
| N11 | PASS | `references/modules/tables.md:24` 仅补三种方向标注形式和非强制定位；既有实验三问、精度、booktabs 等规则未重复实现，`check_tables.py` 未改。 |
| N12-N14 | PASS (reject) | related-work/flow owner 文件未改，`paper-audit` 零改动。 |
| N15 | PASS | `translation-guide.md:273` 包含 claim/evidence/condition/comparison/implication/limitation 六分解，并按目标章节顺序重排。 |
| N16 | PASS | `translation-guide.md:293` 只增加“对象前置”和“gap 前置”两类修复；其余四类只交叉引用 over-claim guard。 |
| N17 | PASS | `conclusion-guide-zh.md:65` 区分范围局限/技术缺陷，限定为组织顺序，并禁止隐去基线落后及安全/有效性权衡。 |
| N18 | PASS (reject) | over-claim guard 及其 owner 未改，未复制动词阶梯。 |
| N19 | PASS (adapt-verify) | `results-analysis-guide-zh.md:37` 已用两条八步链管理结果叙事顺序，`:143` 要求图表导语先点主要结论；`:192` 单独定义证据强度阶梯。两概念已有独立 owner，因此按 PRD 选择“已覆盖不改”。 |

## 跨子任务一致性

### 来源降级与归属

- EN `article-architecture.md:3-9` 明确来源是社区归纳的 Nature-leaning 修辞启发式，缺文章
  corpus、DOI 和样本选择方法，未引用 Nature 官方作者指南，并说明同源内容已被既有章节库吸收。
- ZH `abstract-structure.md:156-159` 与 `conclusion-guide-zh.md:78-82` 保留相同的来源限制和
  非官方规则边界。全文没有把本次增量称为 Nature 官方规范或投稿合规 profile。

### N3 共享措辞与 schema

- EN 与 ZH 均保留三条“可能”级候选：开头无上下文可能缺领域背景、末句宽泛承诺可能需
  收束范围、无数字/比较/具体测试可能缺落地感；均明确需结合摘要类型或 LLM 复核，不作判定。
- EN 是文档诊断表，完整使用 `[LLM] + Severity Info + Priority P3`。
- ZH 沿用 B-SEM 的既有 `_finding` schema，仅使用 `level=Info`、`source=[LLM]`、
  `flagged=false`，没有为单项新增 priority JSON 字段。父 AC 中的 P3 是概念优先级，不要求扩大
  全部 B-* schema；该限定与实际实现一致。
- EN 第三条明确指向既有 `Results-VAGUE` 并禁止重复脚本规则；EN 脚本保持零改动。

### SKILL 与版本

- `latex-paper-en/SKILL.md` 相对基线只把 `last_updated` 从 `2026-08-09` 改为
  `2026-08-10`；`latex-thesis-zh/SKILL.md` 当时已是该日期，未制造无语义改动。
- 两个 SKILL 的 `version` 与 `pyproject.toml` 均为 `6.0.0`；版本契约测试通过。

## 行为证据

- EN 正例“把我的 Results 改成期刊式叙事”命中
  `references/modules/routing-rules.md:21` 的 `Results narrative` / `期刊式` 路由；反例“润色我的
  NeurIPS 摘要语法”由同一规则的 ordinary grammar / conference-abstract 排除条件跳过。该证据是
  本地确定性路由契约检查，不是 provider-backed 模型评估。
- ZH 聚焦测试 `test_bilingual_nature_prompt_is_llm_lane` 证明有英文摘要时存在唯一追加路径且字段、
  三条候选措辞符合契约；`test_bilingual_nature_prompt_requires_english_abstract` 证明无英文摘要时
  不输出 B-NAT。聚焦测试文件共 `47 passed`。

## 资源与最终验证

- 终检重建：`uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`
  通过，共 258 条；重建前后 `docs/resource-manifest.json` SHA-256 均为
  `CE7D7A54C820B006CB150BB94A798D66C22937A679E5E2B8E8D42295B4AE21F8`，且 `git diff
  --exit-code` 通过，确认零漂移。
- `--skill latex-paper-en`：PASS，258 条。
- `--skill latex-thesis-zh`：PASS，258 条。
- 全量 `check_resource_sync.py`：PASS，258 条。
- B-NAT 聚焦测试：PASS，`47 passed`。
- writing alignment、parsers alignment、skill version 聚焦测试：PASS，`58 passed`。
- `just ci`：PASS；Ruff format/check 通过，Pyright `0 errors, 72 warnings`，pytest
  `1499 passed in 114.08s`。
- `just doc-build`：PASS，VitePress `build complete in 15.10s`。

## 证据边界

- Provider-backed 路由和输出评估：**UNVERIFIED / missing evidence**。本次未获授权也未调用 provider。
- 真实论文上的查准率、召回率或写作质量收益：**UNVERIFIED / missing evidence**。合成 fixture、
  静态路由检查、CI 与文档构建均不能证明真实论文效果。
- Nature 官方性或投稿合规性：**UNVERIFIED / not claimed**。集成内容仅按社区归纳的
  Nature-leaning 修辞启发式使用。
