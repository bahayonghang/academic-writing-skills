# C2 实施证据

记录日期：2026-09-24。本文件不记录本机绝对路径。`$SKILL_DIR` 为本技能目录，`$WORK` 为会话 scratchpad 下的新建工作目录。

## 端到端运行

工作目录中的 `mini-thesis` 为 fixture 副本。第一次提取后，按清单 `files[].resolved` 用 Pillow 生成 800 × 500 像素的纯色 PNG，另生成 `fig/logo.png`，再提取一次。规划中的占位符由 `tests/skills/latex_defense_zh/conftest.py` 的 `fill_plan` 替换为合成文本。脚本由项目 uv 环境的 Python 以 `-B` 执行。

| 步骤                           | 命令                                                                                                                                                         | 退出码 | 结果                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ---------------------------------------------------------------------------- |
| 提取（无图片）                 | `uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis $WORK/mini-thesis --out $WORK/inventory-noimg.json --json`                                   | 0      | 告警 `W-FIG-FILE` 19 条、`W-LOGO` 1 条、`W-MAIN` 1 条                        |
| 提取（生成图片后）             | `uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis $WORK/mini-thesis --out $WORK/inventory.json --json`                                         | 0      | 章 7、图 17、表 5、公式 7、算法 1、成果 4、贡献 3、展望 2；告警只有 `W-MAIN` |
| 规划                           | `uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory $WORK/inventory.json --out $WORK/slide_plan.yaml`                                              | 0      | 帧数 54，内容页数 45，占位符 279                                             |
| 串读                           | `uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan $WORK/slide_plan.yaml --outline`                                                                    | 0      | 55 行；末行「帧数 54，内容页数 45，占位符 0」                                |
| 构建 yanshan                   | `uv run python -B $SKILL_DIR/scripts/build_deck.py --plan $WORK/slide_plan-yanshan.yaml --inventory $WORK/inventory.json --out $WORK/deck-yanshan --compile` | 0      | warnings 0 条；帧标记 54 个，`\begin{frame}` 54 个                           |
| 再次构建 yanshan，无 `--force` | 同上，去掉 `--compile`                                                                                                                                       | 4      | 列出七个自有文件，未写文件                                                   |
| 构建 generic                   | `uv run python -B $SKILL_DIR/scripts/build_deck.py --plan $WORK/slide_plan-generic.yaml --inventory $WORK/inventory.json --out $WORK/deck-generic --compile` | 0      | warnings 0 条；帧标记 54 个，`\begin{frame}` 54 个                           |
| 再次构建 generic，无 `--force` | 同上，去掉 `--compile`                                                                                                                                       | 4      | 列出七个自有文件，未写文件                                                   |

两份规划只有 `meta.theme` 不同。`pdfinfo` 结果：两份 `defense.pdf` 均为 54 页，页面尺寸 453.54 × 255.12 pt（16:9）。两份 `defense.log` 中 `Overfull` 与 `Underfull` 均为 0 处，`undefined` 为 0 处。

`W-FIG-FILE` 为 19 条：17 幅图中有一幅图含 3 个子图文件。

## 目视检查

用 pdftoppm 以 40 dpi 渲染 yanshan 稿的 54 页，拼为两张联系表逐页检查：

- 封面、总目录与 6 个章前目录齐全；章前目录中当前章为粗体。
- 帧标题为「节号 节题」；研究章 `intro` 页的小节条为「研究内容 i：章题」。
- 图题注沿用论文编号，例如「图3-3」；三子图网格显示 (a)、(b)、(c) 子图题注。
- 公式编号显示为 (3-1)、(3-2)，`align` 两行显示 (4-1)、(4-2)，`\nonumber` 行无编号。
- 表格居中，含加粗数字；卡片（问题一至问题三、创新点 1 至 3）、「论文」框、展望（其一、其二）与致谢页显示正确。

本任务早先一次使用同一模板的运行（校验逻辑修改前）已逐页检查两主题：表内 `\eqref` 与 `\ref` 输出论文编号，`\cite` 不输出。后续修改只涉及校验与候选选择，不改模板与渲染函数。

## 实施中修正的问题

1. `longtable` 与 `xltabular` 放在 `\adjustbox` 中编译失败（`Missing \endgroup inserted`）。实测普通 `tabular` 在框内、`longtable` 在框外均可编译。处理：`plan_deck.py` 不预选这类表，`build_deck.py` 校验时报错并退出 2。
2. 校验遇到 YAML 类型错误时抛出异常，未按设计退出 2。例如 `figures` 写成字符串列表、`notes` 写成字符串、`table` 写成列表。处理：校验改为列出错误；另加 `meta.minutes`、`meta.title_lines`、`meta.chapters` 的类型检查。
3. 表体缺失的检查从渲染阶段移到校验阶段，与其他错误一起列出。
4. 测试预期修正：`test_equation_and_table_bodies_round_trip` 的公式块数为 6。清单有 7 条公式；第 2 章 2.3 节有两条，骨架每页只预选一条，`eq:c2-objective` 未被选用。

## 设计细化

以下细化已写入 `references/plan-schema.md`：

- `source` 与 `hints` 为列表；`position` 只写在 `figure-bullets` 帧；图引用可带 `width`（对 `figure-grid` 无效）。
- 题注源文本放在 `DefenseSource` 中；`thesis-macros.tex` 的收集范围包含题注与子图题注。
- `eqnarray*` 的编号在公式下方列出；四种删除标签的情形；以 `[`、`<`、`*` 开头的文本加 `{}` 前缀。
- 讲稿中空字段写「无」。
- design §6.3 写 `build_manifest.json` 记录「七个文件的 SHA-256」。清单文件不能记录自身散列，实现记录其余六个文件。
- 已知限制：`longtable`/`xltabular`、文档类中定义的宏、`\renewcommand` 改写的标准命令、无 `\includegraphics` 的图、改章角色后结论条目不重新提取、键值式封面设置、文件展开范围。

## docs 资源登记

- `--write-manifest --inventory-only` 重建清单为 296 条；新增 `plan-schema.md` 一条，`sourceLocale` 为 `zh`。
- zh 资源页与源文件逐字节相同（`cmp` 核对）。
- en 资源页为完整翻译；标题层级、代码块、行内代码序列与表格形状与源文件一致。

## 质量门

| 命令                                                                                                  | 结果                                |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh`                      | 73 passed，5 skipped                |
| `DEFENSE_ZH_COMPILE=1 rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 78 passed（31.42 s）                |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only`       | wrote 296 entries；inventory passed |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh`                | passed                              |
| `rtk proxy just ci`                                                                                   | 2435 passed，7 skipped              |
| `rtk proxy just doc-build`                                                                            | build complete                      |

`ruff format --check`、`ruff check` 与 `pyright`（技能目录与测试目录）无错误，包含在 `just ci` 中。

## 验收对照

| AC  | 证据                                                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC1 | `test_defense_extract.py`：章角色、aux 与计算编号、子图、成果—章映射 `[[3], [3, 4], [5], []]`、贡献 3 条与展望 2 条、提取前后 SHA-256 不变              |
| AC2 | `test_defense_extract.py`：盲审版并存时选正式版并写 `W-MAIN`；两个非盲审候选且无 `--main` 时退出 2                                                      |
| AC3 | `test_defense_budget.py` 参数化用例；`test_defense_plan.py`：30、40、60 分钟内容页数在区间内，每研究章不少于 6 页                                       |
| AC4 | `test_defense_build.py::test_frame_markers_follow_framework`                                                                                            |
| AC5 | `test_tex_escape_table`、`test_plan_text_is_escaped_in_deck`、`test_equation_and_table_bodies_round_trip`、`test_graphicspath_is_relative_and_resolves` |
| AC6 | `test_existing_output_needs_force`；`test_invalid_plan_exits_2`（10 例）、`test_invalid_meta_exits_2`（4 例）、`test_long_table_body_exits_2`           |
| AC7 | `test_fixture_deck_compiles[yanshan]` 与 `[generic]` 在 `DEFENSE_ZH_COMPILE=1` 下通过                                                                   |
| AC8 | `check_resource_sync.py --skill latex-defense-zh` 通过；`just ci` 通过                                                                                  |

## Review gate

- `tex_loader.py` 与 latex-thesis-zh 副本只差第 5 行 docstring 中的技能名（`diff` 核对）。
- `templates/jinja/` 中没有 `\newcommand`、`\renewcommand`、`\providecommand`、`\def` 等定义（grep 核对）。
- 测试只用合成 fixture；图片在测试运行时生成；编译用例在未设 `DEFENSE_ZH_COMPILE=1` 或无 latexmk 时 skip。
- `git status --porcelain`：C2 新增文件均在 design §1 列表内，另有 `docs/resource-manifest.json` 与本文件；其余未提交文件属于 C1 与 pws 登记任务。新目录下没有被忽略的文件（例如 `__pycache__`）。
- AC6（父任务私有内容扫描）：对技能目录、docs 新页面、测试文件与本任务树目录执行 grep，搜索词只在会话中输入。命中只有 `task.json` 的 `creator` 与 `assignee` 字段，以及 `tex_loader.py` 第 31 行一个英文单词的子串误报（该注释与 latex-thesis-zh 副本相同）。

## 后续

C2 通过质量门。按父任务 `implement.md`，下一步启动 C3。本任务不 commit、不归档、不 push。
