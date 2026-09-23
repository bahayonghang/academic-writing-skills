# C5 实施证据

111 个状态不是 111 项已合规。学院清单没有把复合条款标成 PASS。

## 旧模板基线

采集在产品改动之前。解释器：`uv run --extra dev python -X utf8`。环境：`PYTHONIOENCODING=utf-8`。入口：`academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex`。参数：`--year 2026 --json`。四个旧模板（yanshan、thuthesis、pkuthss、generic）乘 doctor、master，共 8 条。原始 stdout、stderr 在本目录 `baseline/`。

| 命令 | exit | stdout 字节 | stderr 字节 |
| --- | --- | --- | --- |
| yanshan doctor | 1 | 20244 | 0 |
| yanshan master | 1 | 20235 | 0 |
| thuthesis doctor | 1 | 14423 | 0 |
| thuthesis master | 1 | 14423 | 0 |
| pkuthss doctor | 1 | 14153 | 0 |
| pkuthss master | 1 | 14110 | 0 |
| generic doctor | 1 | 11394 | 0 |
| generic master | 1 | 11394 | 0 |

exit 1 是旧清单里原有的 FAIL，不是本子改动。采集命令本身 exit 0。

`git diff -- templates/yanshan.md templates/thuthesis.md templates/pkuthss.md templates/generic.md` 字节数为 0。实施后 `test_old_template_json_matches_baseline` 对上述 8 份 stdout/stderr 做了原始字节比较，并包含在通过的 `just ci` 里。没有改保存的基线去迁就新输出。新模板不在这 8 条基线里。

## 111 行矩阵

公开矩阵：`tests/fixtures/college-checklist/yanshan-ee-2025.json`。条款从本任务 `research/checklist-map.md` 逐条转写，不依赖论文仓库。doctor 与 master、`--year 2026`、合成 fixture `thesis-project/main.tex` 各 111 行。ID 为 YSE-001 至 YSE-111。

| 学位 | MANUAL | NEEDS-LLM | MODULE | SKIP | PASS | FAIL |
| --- | --- | --- | --- | --- | --- | --- |
| doctor | 67 | 22 | 22 | 0 | 0 | 0 |
| master | 66 | 21 | 22 | 2 | 0 | 0 |

master 的 SKIP 只有 YSE-074 与 YSE-090。YSE-010、YSE-047、YSE-066、YSE-092 为通用，硕士不 SKIP。

方法计数：manual 67，llm 21，module:bibliography 7，module:references 6，module:format 3，module:consistency 2，module:expression 2，module:tables 2，script:third_person 1。没有 `TEMPLATE_THRESHOLDS["yanshan-ee-2025"]`。

学院清单 CLI 在该合成稿上 exit 0，原因是没有 FAIL 检查器。报告和 JSON 的 `not_acceptance` 写明 MODULE、MANUAL、NEEDS-LLM、SKIP 均未验收。exit 0 不是学院验收通过。

## 仍为人工或 NEEDS-LLM 的项

- MANUAL：67 条 manual，含 YSE-087 与 YSE-111。不用脚本 FAIL 数量推导审查结论。
- NEEDS-LLM：21 条 llm，外加 YSE-088。YSE-088 在合成稿上未发现所列候选，证据仍是 NEEDS-LLM，并写明零命中不是全文第三人称证明。
- MODULE：22 条。命令只打印，状态不是已检查。检查项正文含「脚本仅辅助，余项人工」。
- 第 1、3、10、12、86、89、92、93、109 项不是 PASS。
- YSE-079 保持「公式末不加标点」，方法仍是 `module:format`。没有改 `check_format.py`。
- YSE-098 保留 `LI G Z`，方法仍是 `module:bibliography`。没有改 `verify_bib.py`。

## 门禁

| 命令 | exit | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_check_spec.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/contracts/test_spec_checklists.py tests/contracts/test_skill_contracts.py tests/contracts/test_thesis_zh_guidance_fidelity.py` | 0 | 172 passed |
| `just ci`（eval 末条仍锁在 56 时） | 1 | 2332 passed，1 failed：`test_checked_in_fixture_and_appended_eval` 要求最后一条仍是 56 |
| 修正后 `just ci` | 0 | 版本、lint、pyright、pytest 四步通过。2333 passed，2 skipped。pyright 既有 warning 未新增 error |
| `uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only` | 0 | 285 条。`yanshan-ee-2025.md` 的 `sourceLocale` 为 `zh`。此命令不是最终资源通过 |
| `uv run python docs/scripts/check_resource_sync.py` | 0 | all resources，285 条 |
| `just doc-build` | 0 | vitepress build complete |

追加 eval 后，交叉表面测试改为按 id 56 锁定原条目，不再把 56 当作最后一条。eval 57 只追加，未重排。

## UNVERIFIED

真实论文、PDF 页底几何、学校是否接受、五个宿主运行，均为 UNVERIFIED。本子没有执行 MODULE 提示里的后续命令，没有读取 PDF，没有新增 `--pdf` 或 PyMuPDF。

## 复查修复

YSE-001 至 YSE-111 与 `research/checklist-map.md` 的规范子句逐条相等。`module:` 行只在句末增加「脚本仅辅助，余项人工。」。缺失或改写的条款数是 0。

`third_person` 曾把下列位置报成候选：`\cref`、`\Cref`、`\parencite`、`\textcite`、`\autocite`、`\vref`、`\nameref` 的键；`\mintinline`；`\Verb`；`filecontents*` 中的文献数据。这些位置现已跳过。我国、我校、致谢标题或标准环境、数学，以及原先已跳过的代码与 `thebibliography`，仍不产生候选。零命中仍是 NEEDS-LLM。

`references/modules/spec-check.md` 写明：学院清单没有 FAIL 时退出码为 0，退出码 0 不是学院验收通过。

| 命令 | exit | 结果 |
| --- | --- | --- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_thesis_zh/test_check_spec.py tests/skills/latex_thesis_zh/test_latex_thesis_zh_coverage.py tests/contracts/test_spec_checklists.py tests/contracts/test_thesis_zh_guidance_fidelity.py` | 0 | 150 passed |
| `just lint` | 0 | ruff format 与 ruff check 通过 |
| `just typecheck` | 0 | 0 errors，86 warnings（既有） |
| `uv run python docs/scripts/check_resource_sync.py` | 0 | 285 条 |

旧四模板 JSON 由上述 pytest 里的 `test_old_template_json_matches_baseline` 与 `research/baseline/` 做字节比较，结果通过。没有改基线文件。没有重跑 `just ci` 或 `just doc-build`。
