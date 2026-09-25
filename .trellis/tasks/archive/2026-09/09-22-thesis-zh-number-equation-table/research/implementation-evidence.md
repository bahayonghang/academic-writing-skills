# C2 实现证据

## 命令与退出码

解释器：`uv run --extra dev python -X utf8`。子进程环境含 `PYTHONIOENCODING=utf-8`。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_number_equation_table.py tests/skills/latex_thesis_zh/test_check_style_zh.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py` | 0 | 298 passed |
| `uv run --extra dev python -m pytest -q tests/contracts/test_skill_contracts.py tests/contracts/test_thesis_zh_guidance_fidelity.py` | 0 | 32 passed |
| `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0 | 283 entries；inventory-only 不是最终通过 |
| `just ci` | 0 | 版本、ruff、pyright、pytest；2259 passed，2 skipped |
| `uv run python docs/scripts/check_resource_sync.py` | 0 | all resources，283 entries |
| `just doc-build` | 0 | vitepress build complete |

`sourceLocale` 未改：formula/number/caption/expression/format/references/routing 仍为 `zh`；table-guide 与 modules/tables 仍为 `en`。同语言镜像与源文件一致；另一语言译文的标题层级和行内代码与源文件一致。

## 默认基线

实施前写入 `.trellis/tasks/09-22-thesis-zh-number-equation-table/research/baseline/`。夹具为 `academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`。六条命令都不带 `--school`：

- `check_style_zh.py`
- `check_format.py`
- `check_format.py --strict`
- `check_tables.py`
- `check_tables.py --fix-suggestions`
- `check_references.py`

实施前 `style-default.stdout`、`.stderr`、`.exit` 与 C1 基线逐字节相同。C1 基线未改写。`templates/` 的 `git diff` 为空，记在 `templates-diff.txt`。

实施后 `test_omitted_school_matches_generic_and_default_baseline` 再次逐字节比较上述六条命令，并再次比较 style 与 C1 基线。该测试在目标 pytest 与 `just ci` 中通过。默认输出变化未发生。`--help` 与 `--school` 不在旧基线内。

## style 哈希

`check_style_zh.py` 的 LF 规范化 sha256 从 `5c73bff2e73834e0879f3f57cd66b5a7ecdbe3179362e4f0023b13b32b2f0436` 改为 `64a89445c178bf474f2ab39b29aa0193f07752eca8ac126cc45fca1e4858d858`。`test_polish_unit_zh.py` 只改了这一项。其余冻结哈希未改。

## AC1–AC5

| AC | 测试 |
| --- | --- |
| AC1 缺省/generic 旧输出、非法 school 非零且不打印通过、`--degree-wording` 与 `--school` 不互吞 | `test_omitted_school_matches_generic_and_default_baseline`、`test_invalid_school_is_nonzero_and_not_a_pass`、`test_degree_wording_and_school_do_not_swallow_each_other`、`test_college_candidates_are_absent_without_the_flag`、`test_default_style_does_not_emit_college_number_codes` |
| AC2 百分号/摄氏度/平面角、千分空、年份/型号/DOI/TikZ、未分类裸数字 | `test_college_number_candidates`、`test_math_percent_is_located_without_rewriting_and_angle_stays`、`test_celsius_degree_form_is_not_an_angle_exemption`、`test_unclassified_bare_number_is_not_an_exemption`、`test_tikz_path_and_include_location` |
| AC3 续行正反例、cases/独立定义/约束、引导冒号、末标点、上下式、式中 | `test_equation_rules_have_independent_examples`、`test_unbalanced_equation_is_incomplete_coverage`、`test_split_continuation_is_owned_by_format_not_visible_text` |
| AC4 同上、中文题注末标点、三行同单位、无标点/英文句点/bicaption 第二参数/正确表头 | `test_table_and_figure_caption_ownership`、`test_sameas_excludes_caption_and_notes_and_unclear_columns_are_not_merged` |
| AC5 指南区分学院与 AMS、旧模板不变、契约与门禁 | 上表基线中的空模板 diff；公开指南与 `.trellis/spec/academic-writing-skills/numeric-equation-table-contract.md`；本文件的门禁退出码 |

## C2 拥有的共享段落

未改 C1 已接受句子。C2 只追加：

- `SKILL.md`：C1 术语治理句之后的一条学院 `--school` 路由句。
- `evals/evals.json`：追加 id 54，未重排 1–53。
- `.trellis/spec/academic-writing-skills/index.md`：一行 `numeric-equation-table-contract.md`。
- `docs/resource-manifest.json`：上述公开源的新散列；语言字段保持原值。
- `README.md`、`README_CN.md`、`docs/usage.md`、`docs/zh/usage.md`、两份 `latex-thesis-zh/index.md`：C1 句后各加一句学院开关。
- `check_style_zh.py`：在 C1 `--degree-wording` 之外增加 `--school`。C1 程度词逻辑未改写。
- `check_references.py`：只增加非表浮动体中文题注。未加 C3 引文、页码或文献规则。

工作区里已有、本子未编辑的 C1 文件包括 `check_consistency.py`、`consistency.md`、`academic-style-zh.md`、`term-governance` 夹具与测试、`term-governance-contract.md`。

## MANUAL / NEEDS-LLM

脚本候选一律 `Meaning-Check: NEEDS-LLM`，不输出 `PRESERVED`，不改写数学，不给整句替换。

留人工或不记为通过的范围：公式与正文同行或宏封装；推导链与续行无法区分；复杂公式和未闭合环境；式中/其中的顶格与破折号视觉对齐；表身空白和破折号的测量语义；题注编号后的视觉间距和英文大小写；`multicolumn` / `multirow` / 嵌套表；无法确认的中文题注主参数；未分类裸数字。未知宏不展开，因此不能把零发现当成学院通过。

## UNVERIFIED

真实论文、PDF 页面几何和五宿主运行未执行。合成测试与门禁不证明学校接受或误报率。

## 质检修订

上一节的 `just ci`、资源全量检查和 `just doc-build` 是实施时记录，本轮质检没有重跑。本轮也没有跑 `docs/scripts/check_resource_sync.py`：没有改公开资源。

质检探针确认并已修：

- `array` / `matrix` 内部的 `\\` 被当成 `EQ-CONT`；外层 `align` 只要含 `split` 就整段跳过，漏掉外侧 `&= D`。现在嵌套数学体在外层续行扫描中被屏蔽，复杂环境只给 `EQ-COVERAGE`。
- `A + B &= C \\ &= D` 和 `A = B + C \\ + D` 被写成无法区分。现在与对齐点关系符、上一行首个或末个关系符相同才算 `EQ-CONT`。
- `\end{align}` 后的编号公式被报成缺冒号。结构行改为覆盖不足。
- 公式末 `。` 紧挨 `\\` 时不报 `EQ-TAILPUNCT`。现在去掉行末 `\\` 再看中文句号或逗号；`split` 内的末标点仍保留。
- `\label{eq:上式}` 和单行 `\newcommand` 里的「上式」被当成正文。
- 表头用子串判断单位：`mm` 吃掉 `m`，英文单词里的字母也会挡住短单位。现按字面单位边界比较；`%`、`\%`、`℃` 仍按原文字面。
- `\caption*` / `\bicaption*` 被当成无法确认；表题行号停在 `\begin{table}`。星号题注现在读中文主参数，行号落到该命令所在行。
- 只有 `EQ-COVERAGE` 时，`check_format.py` 的总状态曾是 `PASS`。现在是 `NEEDS-LLM`。默认路径没有该码，六条无 `--school` 基线仍由测试逐字节比较。

`check_style_zh.py` 未改，冻结哈希仍是 `64a89445c178bf474f2ab39b29aa0193f07752eca8ac126cc45fca1e4858d858`。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_number_equation_table.py tests/skills/latex_thesis_zh/test_check_style_zh.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/skills/latex_thesis_zh/test_term_governance.py` | 0 | 315 passed |
| `just lint` | 0 | ruff format 与 ruff check 通过 |
| `just typecheck` | 0 | 0 errors，86 warnings，警告为既有基线 |

## 表格单元格与「以上式子」

简单 `tabular` 不再整段跳过。数据单元格里的 `50\%` 报 `NUM-SPACE`，不要求三行；`1004` 与 `1004.1` 报 `NUM-GROUP`；`1\,004.1`、只写单位的表头、`降幅/\%` 和「百分点」不报间隔。`multicolumn`、`multirow`、嵌套 `tabular` 只给一条覆盖说明，不扫描单元格。`longtable` 和 `sidewaystable` 同样只给一条覆盖说明。`以上式子` 不再命中 `EQ-CITE`；`以上式` 仍可命中。

`check_style_zh.py` 的 LF sha256 现为 `5a2ac1b5f5328b802527a8ff5784c6fe4a4894aa2dc70d1d3b38ed8e66d82a2c`。`test_polish_unit_zh.py` 只改了这一项。

本轮改了 `check_style_zh.py` 和 `check_format.py`。六条无 `--school` 命令由 `test_omitted_school_matches_generic_and_default_baseline` 逐字节比较，该测试包含在下面的 pytest 里并通过。没有重跑 `just ci` 和 `just doc-build`。没有改公开指南。

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_number_equation_table.py tests/skills/latex_thesis_zh/test_check_style_zh.py tests/skills/latex_thesis_zh/test_polish_unit_zh.py` | 0 | 254 passed |
| `just lint` | 0 | ruff format 与 ruff check 通过 |
| `just typecheck` | 0 | 0 errors，86 warnings，警告为既有基线 |
