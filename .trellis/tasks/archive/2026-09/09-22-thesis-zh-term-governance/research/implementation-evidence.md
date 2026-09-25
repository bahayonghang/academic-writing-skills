# C1 实施证据

## 基线

解释器：`uv run --extra dev python -X utf8`。环境：`PYTHONIOENCODING=utf-8`，`PYTHONDONTWRITEBYTECODE=1`。工作目录为仓库根。
固定 fixture：`academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`。
旧术语文件：`.trellis/tasks/09-22-thesis-zh-term-governance/research/baseline/old-terms.json`，只含 `zh` / `en` 分组。
改前采集 stdout、stderr、exit。改后用同一参数重跑。五条命令全部逐字节一致。没有改写已保存的基线。

| 命令 | exit | stdout | stderr | 比对 |
| --- | --- | --- | --- | --- |
| `check_consistency.py <fixture>` | 1 | 1008 | 201 | MATCH |
| `check_consistency.py <fixture> --terms` | 0 | 226 | 201 | MATCH |
| `check_consistency.py <fixture> --abbreviations` | 0 | 57 | 201 | MATCH |
| `check_consistency.py <fixture> --custom-terms <old-terms.json>` | 1 | 1008 | 201 | MATCH |
| `check_style_zh.py <fixture>` | 0 | 1170 | 0 | MATCH |

`--help` 与新开关不在基线内。

## 门禁

| 命令 | exit | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q` 四个技能测试 + `test_skill_contracts.py` + `test_thesis_zh_guidance_fidelity.py` | 0 | 295 passed |
| `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0 | 283 entries；inventory 通过。不是最终资源通过。 |
| `just ci` | 0 | 版本 1 passed；Ruff format/check 通过；Pyright 0 errors、86 warnings；pytest 2221 passed、2 skipped |
| `uv run python docs/scripts/check_resource_sync.py` | 0 | all resources，283 entries |
| `just doc-build` | 0 | vitepress build complete |

`sourceLocale` 保持原值：`consistency.md` 为 `en`；`expression.md`、`routing-rules.md`、`academic-style-zh.md`、`structure-and-consistency.md` 为 `zh`。同语言镜像与源文件在链接掩码后一致。中文译文保留新开关、字段名、`NEEDS-LLM` 与合成词，没有写入论文专名。

## AC

| AC | 证明 |
| --- | --- |
| AC1 | `test_banned_hit_lists_every_candidate_once_and_locked_reports_canonical`；`test_fixed_protection_and_user_environments_skip_governance_hits`；`test_ordinary_longer_title_and_ascii_boundaries`；`test_empty_governance_has_no_new_candidates_and_macros_block_a_clean_pass`；`test_governance_requires_custom_terms_and_rejects_bad_input`；`test_governance_keeps_synonym_groups_and_ignores_them_when_disabled`；`test_legacy_custom_terms_do_not_consume_governance_fields`；`test_fixture_project_governance_and_abbreviation_style` |
| AC2 | `test_abbreviation_style_positive_and_negative_cases`；`test_unclear_boundary_is_one_note_and_not_a_false_xor`；`test_abbreviation_order_follows_the_entry_assembly`；`test_style_dedupes_same_position_without_replacing_the_old_recognizer`；fixture 集成用例中的 later.tex 三行 |
| AC3 | `test_degree_mode_skips_only_the_legal_absolute_span`；`test_each_legal_collocation_is_span_local`；`test_degree_phrases_are_local_candidates_without_a_replacement_sentence`；`test_degree_phrase_set_and_complete_ignore_dedupe`；`test_degree_mode_keeps_existing_protection_and_section_routing`；`test_degree_report_marks_script_info_and_needs_llm`；`test_degree_cli_default_output_has_no_degree_code`；`test_degree_cli_error_is_not_a_clean_pass` |
| AC4 | `term-governance-contract.md` 与 consistency / expression / academic-style / routing / example 的公开句一致；README、usage、技能索引各有同一事实的中英句；资源全量检查通过。合成词为 `合成甲`、`旧称`、`ZX`、`AbX`、`X-2`。 |
| AC5 | 上表基线 MATCH；`test_old_json_keys_stay_without_new_flags`；`test_polish_unit_zh.py` 只改 `check_style_zh.py` 哈希；`just ci` exit 0 |

## style 哈希

`check_style_zh.py` LF sha256：

- 旧：`3774ff1d228d85c9999e5730c2c8fac11d71633a4953aa11b7fe751aa0104cbc`
- 新：`5c73bff2e73834e0879f3f57cd66b5a7ecdbe3179362e4f0023b13b32b2f0436`

`test_polish_unit_zh.py` 的其余五条冻结哈希未改。

## 共享文件与 C1 段落

| 文件 | C1 拥有的部分 |
| --- | --- |
| `SKILL.md` | 路由规则中新增的一条可选开关说明 |
| `evals/evals.json` | 追加 id 53，不重排 1–52 |
| `.trellis/spec/academic-writing-skills/index.md` | 新增 `term-governance-contract.md` 一行 |
| `docs/resource-manifest.json` | 上述五个公开源的 `sourceSha256` |
| `README.md` / `README_CN.md` | 技能表后的同一事实句 |
| `docs/usage.md` / `docs/zh/usage.md` | `latex-thesis-zh` 段落后的同一事实句 |
| `docs/skills/latex-thesis-zh/index.md` 与中文索引 | 路由表后的同一事实句 |
| `test_polish_unit_zh.py` | 仅 `check_style_zh.py` 哈希 |

`check_style_zh.py` 在 C2 开始后不得整文件回滚。C1 新增的是 `degree_wording` 与 `E-DEGREE`。

## MANUAL / NEEDS-LLM

脚本不判断同义组是否同一概念，不判断 Title Case 是否专名，也不判断程度词是否已有证据。
名称含「采用 / 使用 / 通过 / 称为 / 叫做 / 的 / 了 / 是」，或汉字串长于 20 且没有明确左边界时，只给一条 `NEEDS-LLM` 覆盖说明，不发 XOR。
存在 `\newcommand` 等未展开自定义宏时，覆盖记为不完整，不宣称没有问题。
缩略词表以外的普通表、外置 `.bib` 题名、以及未列入固定保护的未知宏参数，不作为已完成扫描。
页面、PDF 和学校接受度不在本检查内。

## UNVERIFIED

真实论文、PDF 版面、五宿主运行、provider 评估均未运行，记为 UNVERIFIED。
合成测试与 `just ci` 不证明这些外部效果。

## 质检修订

`--governance` 读取非 UTF-8 术语文件时，`UnicodeDecodeError` 未转入 `GovernanceConfigError`，stderr 是 traceback，没有 `[ERROR]`。已改为非零退出并打印 `[ERROR]`，stdout 仍无通过结论。
`test_fixture_project_governance_and_abbreviation_style` 对 locked 的断言在空列表时恒真。已改为要求 `chapters/body.tex:30` 的一条 `旧别名` → `标准名`。
本轮重跑五条无新开关基线，stdout/stderr/exit 仍逐字节 MATCH。未重跑 `just ci` 与 `just doc-build`。
