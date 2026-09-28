# C3 实施证据

记录日期：2026-09-25。宿主：Claude Code（云端会话容器）。本文件不记录本机绝对路径。
`$SKILL_DIR` 为本技能目录，`$WORK` 为会话 scratchpad 下的新建工作目录。

## 环境

容器内安装 TeX Live（Ubuntu 包：texlive-xetex、texlive-latex-extra、texlive-lang-chinese、texlive-science、
texlive-fonts-recommended、tex-gyre、latexmk、poppler-utils）；项目虚拟环境另装 PyMuPDF 1.28.2（`uv pip install pymupdf`，
不进入 `pyproject.toml` 依赖）。容器无 Microsoft YaHei 与 Arial，主题按回退链使用 FandolHei 与 TeX Gyre Heros。

## 端到端运行

工作目录中的 `mini-thesis` 为 C2 fixture 副本；首次提取后按清单 `files[].resolved` 用 Pillow 生成纯色 PNG 与 `fig/logo.png`，
再提取一次。规划占位符由 `tests/skills/latex_defense_zh/conftest.py` 的 `fill_plan` 替换为合成文本。

| 步骤 | 命令 | 退出码 | 结果 |
| ---- | ---- | ------ | ---- |
| 提取 | `uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis $WORK/mini-thesis --out $WORK/inventory.json --json` | 0 | 章 7、图 17、表 5、公式 7、算法 1、成果 4、贡献 3、展望 2；告警只有 `W-MAIN` |
| 规划 | `uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory $WORK/inventory.json --out $WORK/slide_plan.yaml` | 0 | 帧数 54，内容页数 45，占位符 279 |
| 串读 | `uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan $WORK/slide_plan.yaml --outline` | 0 | 占位符 0 |
| 构建 | `uv run python -B $SKILL_DIR/scripts/build_deck.py --plan $WORK/slide_plan.yaml --inventory $WORK/inventory.json --out $WORK/deck --compile` | 0 | 帧数 54；warnings 0 条；`pdfinfo` 54 页 |
| 检查（文本） | `uv run python -B $SKILL_DIR/scripts/check_deck.py --deck $WORK/deck/defense.tex --inventory $WORK/inventory.json --plan $WORK/slide_plan.yaml --log $WORK/deck/defense.log` | 0 | Critical 0，Major 0，Minor 0，Info 0；skipped 无 |
| 检查（`--json`） | `uv run python -B $SKILL_DIR/scripts/check_deck.py --deck $WORK/deck/defense.tex --inventory $WORK/inventory.json --json` | 0 | `summary` 全 0；`skipped` 为空（同目录 `defense.log` 被自动读取） |
| 预览 | `uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf $WORK/deck/defense.pdf --out $WORK/deck/preview` | 0 | 54 张逐页 PNG 与 `contact-sheet.png` |

## 目视检查（总览图）

封面、总目录、6 个章前目录（当前章加粗）、研究章五种角色页、卡片页、「论文」框、创新点与展望、致谢页齐全；
子图网格、公式编号 (3-1)、(4-1)/(4-2) 与表格显示正确；未见溢出或文字截断。

## 实施中修正的问题

- 测试隔离：PyMuPDF 在首次导入时绑定当时的 `sys.stdout`。若首次导入发生在带 `capsys` 的预览测试内，
  该流在测试结束后关闭，后续 `test_demo_deck_compiles` 打开 PDF 时报 `ValueError: I/O operation on closed file`。
  处理：`tests/skills/latex_defense_zh/conftest.py` 在收集阶段预导入 PyMuPDF（缺失时忽略）。

## 质量门

| 命令 | 结果 |
| ---- | ---- |
| `uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 全部通过（PyMuPDF 可用，编译用例 skip） |
| `DEFENSE_ZH_COMPILE=1 uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 146 passed |
| `uv run python docs/scripts/check_resource_sync.py` | resource contract passed（297 条） |
| `just ci` | 通过（见 C4 证据中的最终运行） |

## 验收对照

| AC | 证据 |
| --- | --- |
| AC1 | `test_defense_check.py` 以码名参数化正例与反例；21 个码与 `quality-gate.md`、`check_deck.py` 集合一致（grep 核对） |
| AC2 | `test_parent_ac8_*` 三例 |
| AC3 | 输出行格式与 `--json` 字段集合用例；退出码 0/1/2 用例 |
| AC4 | 无 log 时 skipped 用例；无 notes.md 报 D-NOTES 用例 |
| AC5 | `test_defense_preview.py` 在 PyMuPDF 可用时 10 passed |
| AC6 | `test_check_does_not_write` 与预览只读用例 |
| AC7 | 资源检查与 `just ci` 通过 |
