# C4 实施证据

## 命令与退出码

解释器：`uv run --extra dev python -X utf8`，子进程 `PYTHONIOENCODING=utf-8`。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `pytest -q tests/skills/latex_thesis_zh/test_cross_surface_numbers.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` | 0 | 78 passed（类型收窄前） |
| `pytest -q tests/skills/latex_thesis_zh/test_cross_surface_numbers.py` | 0 | 27 passed（最终脚本） |
| `pytest -q tests/contracts/test_skill_contracts.py tests/contracts/test_thesis_zh_guidance_fidelity.py` | 0 | 32 passed |
| `python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0 | 284 entries；inventory-only 不是最终通过 |
| `python docs/scripts/check_resource_sync.py --skill latex-thesis-zh` | 0 | latex-thesis-zh |
| `just ci` | 0 | 版本 1 passed；Ruff passed；Pyright 0 errors / 86 warnings；pytest 2317 passed, 2 skipped |
| `python docs/scripts/check_resource_sync.py` | 0 | all resources，284 entries |
| `just doc-build` | 0 | vitepress build complete |

`just ci` 在最后一次仅类型收窄的脚本修改之后重跑，退出码对应当前脚本。全量资源检查与 `just doc-build` 在该收窄之前通过；该修改不改变 Markdown 或 manifest，因此这两项没有重跑。

## 基线字节比较

夹具：`academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`。
未传 `--cross-surface` 或 `--generate`。比较对象是实施前写入的
`.trellis/tasks/09-22-thesis-zh-cross-surface-numbers/research/baseline/`，没有改基线去迎合新输出。

| 命令 | stdout | stderr | exit |
| --- | --- | --- | --- |
| `analyze_experiment.py <fixture>` | 相等（640 字节） | 相等 | 0 |
| `analyze_experiment.py <fixture> --results-analysis` | 相等（351 字节） | 相等 | 0 |

默认与单独 `--results-analysis` 不出现 `RA-XS-`、`CROSS-SURFACE` 或“不是全文合规证明”。

## AC 映射

| AC | 测试 |
| --- | --- |
| AC1 三表面一致为 compared_keys=1、differences=0 | `test_three_surfaces_equal_compares_one_key`；`test_checked_in_fixture_and_appended_eval` |
| AC1 同键 92.1/92.3 只报正文差异，且报告不含这两个数字 | `test_body_mismatch_does_not_report_summary` |
| AC1 另一指标碰巧同数不能抵消 | `test_other_metric_same_digits_do_not_cancel_body_difference` |
| AC1 缺正文、缺小结、绑定表无行 | `test_missing_surfaces_and_missing_row` |
| AC2 两表引用、单位不同、无评价集、无对象：NEEDS-LLM 且 compared_keys=0 | `test_ambiguous_bindings_are_needs_llm_without_a_compared_key` |
| AC2 区间端点不是区间本身；百分数不换成小数；无量纲必须写明 | `test_interval_endpoint_is_not_the_same_value`；`test_percent_is_not_rescaled_to_a_fraction`；`test_dimensionless_requires_an_explicit_marker` |
| AC2 `\,`、负号、有序区间、科学计数不换算单位 | `test_grouping_sign_interval_and_scientific_notation_normalize` |
| AC2 multirow、宏表、无表、无小结 | `test_uncovered_syntax_missing_table_and_missing_summary` |
| AC2 include 跨章隔离与 `ch2.tex:` 位置 | `test_include_keeps_chapters_isolated` |
| AC2 `--section` 不扫描其他章；无匹配不伪装一致 | `test_section_limits_the_scan` |
| AC2 默认与旧 RA 不打印新统计 | `test_default_and_results_analysis_omit_cross_surface_stats`；上表字节比较 |
| AC3 评价集混用、指标互推、否定句不误报 | `test_negated_eval_set_and_metric_implication` |
| AC3 词表只替换出现的字段；空数组不是全匹配；非法 JSON 与单独 `--cross-surface-terms` 非零且 stdout 为空 | `test_custom_terms_replace_only_present_fields`；`test_illegal_terms_exit_nonzero`；`test_terms_flag_without_cross_surface_is_a_parameter_error` |
| AC4 指南有显示层/源层、分母，以及“由准确率可得F1 / 不能由准确率可得F1” | `test_guides_and_contract_state_the_narrow_subset` |
| AC4 两开关串接且 RA 前缀不变；旧九码词表不含合成指标 | `test_both_flags_keep_results_analysis_prefix`；`test_loader_targets_zh_cross_surface_copy` |
| AC4 父门禁 | 上表 `just ci`、资源检查、`just doc-build` |

`table*` 与独立 `longtable` 由 `test_table_star_and_longtable_bind` 覆盖。冒烟命令增加 `analyze_experiment.py main.tex --cross-surface`。

## C4 拥有的共享段落

后续子任务不得覆盖这些新增句或条目。

- `academic-writing-skills/latex-thesis-zh/SKILL.md`：C3 引文句之后的一条 `--cross-surface` 句。C1–C3 句保留。
- `evals/evals.json`：只追加 id 56。工作树里已有的 id 53–55 属于前序子任务，本子未重排。
- `.trellis/spec/academic-writing-skills/index.md`：原 `results-analysis-checker-contract.md` 行补了 `--cross-surface`，没有新增第二行。
- `docs/resource-manifest.json`：`experiment.md`、`routing-rules.md`、`results-analysis-guide-zh.md` 的 `sourceLocale` 仍为 `zh`，只更新了这三份源的 `sourceSha256`。
- `README.md`、`README_CN.md`、`docs/usage.md`、`docs/zh/usage.md`、`docs/skills/latex-thesis-zh/index.md`、`docs/zh/skills/latex-thesis-zh/index.md`：C3 句后各加一条 C4 事实。

## MANUAL / NEEDS-LLM

全部 `RA-XS-*` 为 Info/P3、`[Script]`、`Meaning-Check: NEEDS-LLM`。脚本不输出修正数字，也不按差值大小分严重度。
不能唯一绑定、多个候选、未覆盖表语法、跨章引用只给 `RA-XS-COVERAGE`，不判断哪一处终值正确。
人工仍须核读三表面、分母、单位、对象，以及显示层终值与源层重算的差别。脚本不读 CSV，不复算比例，不换算单位。
零差异只说明已比较的支持子集，不是全文合规证明。

## UNVERIFIED

真实论文、PDF、五宿主运行、provider eval 均未执行。合成测试与门禁不证明这些外部效果。

## 检查修订

对照 design §3 改了绑定和报告。已绑定但表中无该记录只报 `RA-XS-SUMMARY`，缺的正文或小结仍报 `RA-XS-MISSING`，不再把缺记录报成 `RA-XS-BODY`。行标签若只是更长对象名的前缀，不按短标签绑定；`中…在` 给出的更长对象优先。表头明确为 `%` 或“无量纲”时，单元格里的整数可以绑定；`92%` 不换成 `0.921`。能定位到指标和行、但单元格终值或单位不能解析时，只报 `RA-XS-COVERAGE`，不判缺记录。差异行号改到对应表面。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `pytest -q tests/skills/latex_thesis_zh/test_cross_surface_numbers.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` | 0 | 83 passed |
| `just lint` | 0 | Ruff passed |
| `just typecheck` | 0 | 0 errors，86 warnings |
| `python docs/scripts/check_resource_sync.py` | 0 | all resources，284 entries |
| 默认与 `--results-analysis` 对原基线逐字节比较 | 0 | stdout/stderr/exit 相等；基线文件未改 |

这次没有重跑 `just ci` 和 `just doc-build`。上面原表里的这两项仍是修改前的记录，不是本次复查结果。
`experiment.md` 的 `sourceLocale` 仍为 `zh`，只更新了 `sourceSha256`。

## 2026-09-23 复审修复

只改 `academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py` 与
`tests/skills/latex_thesis_zh/test_cross_surface_numbers.py`。

- 缺陷 1（Major）：`_records_from_grid` 在按 `\` / `&` 切分表体之前，新增 `_strip_grid_comments`
  逐行去掉未转义的 `%` 注释（正则与 `_prepare_measure_text` 相同，保留 `\%`）。表头前含 `&` 的注释行
  不再使列右移；行尾注释不再吞掉下一数据行。
- 缺陷 2（Minor）：新增 `_XS_APPROX_BEFORE_RE`（`约|约为|大约|近` 后可跟空白）替换原来仅看紧邻一个字符的
  `约` 判断。`约 92\%` 等按近似值处理，返回 `unclear`，不进入相等比较，只报 `RA-XS-COVERAGE`。

新增测试：

- `test_header_comment_with_ampersand_does_not_shift_columns`：表头前注释行 → 与无注释输出相同
  （compared_keys=1、differences=0）；正文引用不存在的列 → `RA-XS-SUMMARY` 表中无此记录，无 `RA-XS-BODY`。
- `test_trailing_comment_after_row_keeps_next_row`：行尾注释 → 方法乙 compared_keys=1、differences=0，
  注释内数字不出现在报告。
- `test_escaped_percent_in_cell_survives_comment_stripping`：单元格 `92.3\% % 备注` 仍绑定为一键。
- `test_spaced_approximate_marker_is_not_compared`（5 个参数）：`约 `、`约为 `、`大约 `、`接近 `、`约`
  均不比较、differences=0、报 `RA-XS-COVERAGE`。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `pytest -q tests/skills/latex_thesis_zh/test_cross_surface_numbers.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` | 0 | 91 passed |
| 夹具目录内 `python -X utf8 analyze_experiment.py main.tex` 与 `--results-analysis` 对 `research/baseline/` 逐字节比较 | 0 | stdout/stderr/exit 六项均相等；基线未改 |
| `just lint` | 0 | Ruff passed |
| `just typecheck` | 0 | 0 errors |

未跑 `just ci`、资源同步、`just doc-build`（本次不改 Markdown/manifest）。真实论文效果仍 UNVERIFIED。
