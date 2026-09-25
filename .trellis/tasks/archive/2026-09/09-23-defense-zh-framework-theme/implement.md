# C1 执行计划

## Entry

前置：用户明确授权实施，且本子任务已 `task.py start`（status = in_progress）。
读取顺序：`implement.jsonl` 列出的 spec 与父 research → 本 `prd.md` → `design.md` → 父 `design.md` §1、§5、§7。
文件边界：只新增或修改 design §1 所列文件。任何其他路径的改动先停下并上报。

## Steps

1. 新建 `academic-writing-skills/latex-defense-zh/references/`，按 design §2.1–2.6 写七份参考文档。
   事实只取父 `research/framework-analysis.md` 与 `research/reference-skills-analysis.md`；示例题目用中性合成内容。
   `time-budget.md` 的三档表与两种结构值必须与 design §2.5 逐项一致（由步骤 5 的测试核对）。
2. 新建 `templates/beamer/defense-layouts.sty`：父 design §5 的全部宏、六个颜色名的默认值、字体回退、
   `\DefenseSetup` 的 l3keys（logo、stage、logo-text）、章表 seq 与 `\DefenseTocFrame`。校徽路径为空或文件不存在时显示 `logo-text` 文字标识。
3. 新建两主题 `.sty`：只定义颜色、headline/frametitle、封面与致谢外观，并 `\RequirePackage{defense-layouts}`。
   yanshan 数值按 design §2.4 与父 research §4 换算表；generic 同版位、无校徽、generic 色值。
4. 新建 `templates/beamer/demo-deck.tex`：合成内容，十二个版式各至少一帧，每帧前写 `% layout: <name>`；
   用 `\providecommand{\DefenseThemeName}{YanshanDefense}` 给默认主题。
5. 新建 `tests/skills/latex_defense_zh/test_defense_theme_assets.py`，实现 design §4 的五个用例。
6. docs 资源登记（design §1 docs 条目）：
   1. 运行 `--write-manifest --inventory-only`，确认新增七条的 `sourceLocale` 为 `zh`。
   2. 写七份 zh 资源页（与源一致，只做必要的链接目标重写）与七份 en 资源页（完整翻译，保留标题层级、代码块、
      inline code 与表格形状，链接目标与 zh 页相同）。
   3. 改资源契约测试技能集合一行、两份安装页命令块各加一行、命令条数说明由七改八。
7. 在会话 scratchpad 中手工编译两主题各一次（命令见下），目视检查封面、目录、各版式与致谢页；
   记录编译命令、退出码、PDF 页数和 `Overfull` 计数到本任务 `research/c1-evidence.md`（不记录本机绝对路径）。
8. 执行质量门命令；全部通过后在 `research/c1-evidence.md` 追加命令与结果，然后停止，等待 C2 授权。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
DEFENSE_ZH_COMPILE=1 rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh
rtk proxy uv run --extra dev python -m pytest -q tests/contracts/test_docs_bilingual_resources.py
rtk proxy just ci
rtk proxy just doc-build
```

手工编译（在 scratchpad 的副本目录内执行；校徽用合成 PNG）：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error demo-deck.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -jobname=demo-generic "-usepretex=\def\DefenseThemeName{GenericDefense}" demo-deck.tex
```

C1 期间新技能无 SKILL.md、不在 catalog 列表中；`test_skill_contracts.py` 等列表型契约测试不覆盖本目录，这是预期状态。

## Review gate

- 人工 grep 技能目录、docs 新页面与测试文件，确认不含参考 pptx 作者姓名、用户姓名与论文题目、本机绝对路径（AC6）；
  搜索用词只在会话中输入，不写入任何文件。
- 确认 `git status --porcelain` 只列出 design §1 的文件与本任务 `research/c1-evidence.md`。
- 确认两主题不定义任何版式宏（测试 2），十二个版式名在 slide-layouts.md 与 demo-deck.tex 中一致（测试 3）。

## Rollback

删除 `academic-writing-skills/latex-defense-zh/`、`tests/skills/latex_defense_zh/`、`docs/skills/latex-defense-zh/`、
`docs/zh/skills/latex-defense-zh/`；`git checkout` 还原 `docs/resource-manifest.json`、两份安装页与
`tests/contracts/test_docs_bilingual_resources.py`。本计划不授权 commit、archive 或 push。
