# latex-defense-zh 答辩稿契约

## 1. Scope / Trigger

修改 `academic-writing-skills/latex-defense-zh/` 的脚本（extract、plan、build、check、preview）、Jinja2 帧模板、
Beamer 主题与版式宏、D-* 判据、清单或规划字段，以及对应公开资源时适用。
五个脚本通过清单 JSON、规划 YAML、帧标记与结果行串成一条流水线；任一环节改名或改格式，下游会静默失配。
详细字段以技能内 `references/plan-schema.md` 与 `references/quality-gate.md` 为准，本文件只锁跨脚本的接口。

## 2. Signatures

```text
extract_thesis.py --thesis DIR [--main FILE] --out inventory.json [--json]
plan_deck.py --inventory inventory.json --out slide_plan.yaml [--minutes 40] [--stage predefense|defense] [--theme yanshan|generic]
plan_deck.py --plan slide_plan.yaml --outline
build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile]
check_deck.py --deck DIR/defense.tex --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] [--minutes 40] [--json]
render_preview.py --pdf DIR/defense.pdf --out DIR/preview [--dpi 110] [--cols 4]
```

所有命令写作 `uv run python -B $SKILL_DIR/scripts/<name>.py …`；stdout/stderr 在 `__main__` 中重设为 UTF-8。

| 脚本 | 退出码 |
| --- | --- |
| extract | 0 成功；2 主文件缺失或多个非盲审候选且无 `--main` |
| plan | 0；2 参数或输入错误（`--minutes` 范围 15–90） |
| build | 0；2 规划校验失败（含 `longtable`/`xltabular` 表体）；4 自有文件已存在且无 `--force`；5 编译失败或无 latexmk |
| check | 0 无 Critical/Major；1 有；2 输入错误 |
| preview | 0；2 输入错误；3 缺 PyMuPDF（提示 `uv pip install pymupdf`） |

## 3. Contracts

- 帧标记：`build_deck.py` 在每个 `\begin{frame}` 前一行写
  `% defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>`；`\begin{frame}` 计数等于 PDF 页数。
  `check_deck.py` 以标记映射行号、页角色与页序；缺标记时回退帧序号并报 D-MARKER。
- 帧 id：`cover`、`toc`、`c<k>-toc`、`c<k>-<role>[-<i>]`、`thanks`；全稿唯一。
- 页序：封面 → 总目录（`\DefenseTocFrame{0}`）→ 第 1 章 → 第 k 章前目录（k ≥ 2）与各页 → 致谢；备用页在致谢之后，不计页数与预算。
  defense 阶段在展望页后加 `achievements`。
- 文字字段是普通文本，渲染时逐字转义；唯一标记是 `**关键词**`（`\DefenseHighlight`）。
- 公式：清单 `tex` 的 `\label{x}` 变为 `\tag*{(编号)}`，其余字符不变，放在 `DefenseSource` 中；
  D-EQ-SRC 去掉 `\label`/`\tag`/`\notag`/`\nonumber` 与空白后与清单逐字比较。
- 表体：`tabular_source` 原文放在 `DefenseSource` 与 `\adjustbox` 中；D-TAB-SRC 去掉空白后逐字比较。
- 模板只调用主题宏 API（`\Defense*` 与 `DefenseSource`），`templates/jinja/` 中不定义宏。
- 帧模板中，`\begin{frame}{<title>}` 之后不得直接跟花括号组：Beamer 把它当作帧副标题吞掉。分组一律用 `\begingroup … \endgroup`。
- 自有文件七个：`defense.tex`、`thesis-macros.tex`、`notes.md`、`build_manifest.json`、两个主题 `.sty` 与 `defense-layouts.sty`。
  `--force` 只覆盖自有文件；内容未变的自有文件不重写，保留 mtime（latexmk 按内容哈希决定是否重编，
  重写同内容的 `defense.tex` 会让 PDF 早于答辩稿而误报 D-COMPILE）。
- 只读：extract 与 check 不写论文仓库、答辩稿、清单与规划；preview 只写 `--out` 下的 `page-NNN.png` 与 `contact-sheet.png`。
- D-* 码集合固定为 21 个：D-MARKER、D-COVERAGE、D-TOC、D-CHAIN、D-PLACEHOLDER、D-FIG-ALLOW、D-FIG-MISSING、D-FIG-NUMBER、
  D-FIG-ASPECT、D-EQ-SRC、D-TAB-SRC、D-NUM-SRC、D-PAPER、D-META、D-STAGE、D-DENSITY、D-BUDGET、D-NOTES、D-COMPILE、
  D-OVERFLOW-V、D-OVERFLOW-H。结果行：
  `% D-CODE (frame=<id>, <file>:<行>) [Severity: …] [Priority: …]: [Script] message`；`--json` 含 `findings`、`summary`、`skipped`。

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| 正式版与盲审版主文件并存 | 选正式版并写 `W-MAIN` |
| 两个非盲审主文件且无 `--main` | extract 退出 2 |
| 规划字段类型错误（例如 `figures` 为字符串列表） | build 列出全部错误并退出 2，不抛异常 |
| 输出目录已有任一自有文件、无 `--force` | build 退出 4，不写任何文件 |
| 只改讲稿后 `--force --compile` | 只重写 `notes.md` 与 `build_manifest.json`；check 不报 D-COMPILE |
| `figure-grid` 帧无小节条 | 子图网格仍显示（不被当作副标题） |
| 无编译日志 | D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H 记入 `skipped` |
| 缺 `notes.md` | D-NOTES Major |
| 清单外图片、论文外数字、改写公式 | 分别报 D-FIG-ALLOW、D-NUM-SRC（NEEDS-LLM）、D-EQ-SRC |

## 5. Good / Base / Bad Cases

- Good：修改一个 D-* 判据时，同时改 `check_deck.py`、`references/quality-gate.md`（含双语资源页与 manifest 散列）与该码的正反例测试。
- Base：只改讲稿文字后重建，`defense.tex` 字节与 mtime 不变，latexmk 不重编，check 零结果。
- Bad：在帧模板里写 `{\centering …}` 紧跟帧标题；在文字字段里写 `$…$` 期望渲染数学；为消除 D-NUM-SRC 把数字换成另一个自算的数字。

## 6. Tests Required

- `tests/skills/latex_defense_zh/`：`test_defense_theme_assets.py`（主题常量、宏 API、演示稿编译）、`test_defense_budget.py`、
  `test_defense_extract.py`、`test_defense_plan.py`、`test_defense_build.py`（帧标记序列、转义、公式与表体还原、`--force`、
  帧标题后无花括号组、未变文件保留 mtime）、`test_defense_check.py`（21 码正反例与输出契约）、`test_defense_preview.py`。
- 编译用例只在 `DEFENSE_ZH_COMPILE=1` 且有 xelatex/latexmk 时运行；预览用例在无 PyMuPDF 时 skip。
  `conftest.py` 在收集阶段预导入 PyMuPDF：它在首次导入时绑定 `sys.stdout`，若首次导入发生在 `capsys` 测试内，后续用例会写入已关闭的流。
- 契约测试：`tests/contracts/test_skill_contracts.py`（路由命令参数出现在 `--help`、命令卫生、`allowed-tools`）、
  `test_skill_versions.py`、`test_skills_install.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py`。

## 7. Wrong vs Correct

```latex
% Wrong: without a subsection bar, Beamer reads this group as the frame subtitle.
\begin{frame}{3.4 实验与结果分析}
{\centering
\begin{minipage}[t]{0.3\linewidth} … \end{minipage}\par}

% Correct
\begin{frame}{3.4 实验与结果分析}
\begingroup\centering
\begin{minipage}[t]{0.3\linewidth} … \end{minipage}\par\endgroup
```
