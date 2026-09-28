# latex-defense-zh 父设计

## 1. 包布局与文件所有权

技能根 `S = academic-writing-skills/latex-defense-zh`。

```
S/
  SKILL.md                                  C4
  agents/openai.yaml                        C4
  agents/qa-committee-agent.md              C4
  references/defense-framework.md           C1  页序、章角色、各角色页型序列
  references/slide-layouts.md               C1  版式目录：字段、适用角色、内容上限
  references/content-rules.md               C1  要点与规范、学术事实保护、溢出处置顺序
  references/visual-spec.md                 C1  两主题视觉规格、pptx→Beamer 换算
  references/time-budget.md                 C1  分钟→页数规则与区间
  references/speaker-notes.md               C1  讲稿五栏格式
  references/qa-prep.md                     C1  答辩提问类别与准备方法
  references/quality-gate.md                C3  D-* 码表、阈值与处置
  references/plan-schema.md                 C2  清单 JSON 与规划 YAML 字段
  templates/beamer/beamerthemeYanshanDefense.sty   C1
  templates/beamer/beamerthemeGenericDefense.sty   C1
  templates/beamer/defense-layouts.sty      C1  页型宏（两主题共用）
  templates/beamer/demo-deck.tex            C1  合成演示稿，覆盖全部版式
  templates/jinja/deck.tex.j2               C2
  templates/jinja/frames/<layout>.tex.j2    C2
  examples/predefense-40min.md              C4
  examples/formal-defense.md                C4
  examples/fix-after-check.md               C4
  scripts/tex_loader.py                     C2  latex-thesis-zh 副本，仅改 docstring 技能名
  scripts/extract_thesis.py                 C2
  scripts/plan_deck.py                      C2
  scripts/build_deck.py                     C2
  scripts/defense_budget.py                 C2  时长→页数公式（C1 time-budget §公式），plan 与 check 共用
  scripts/check_deck.py                     C3
  scripts/render_preview.py                 C3
  evals/evals.json、evals/trigger_eval.json C4
  evals/fixtures/mini-thesis/               C2  合成论文（文本；图片由测试运行时生成）
tests/skills/latex_defense_zh/              C1 建目录；C1/C2/C3/C4 各自新增测试文件
```

references 文件名用小写 kebab-case；中文正文（`sourceLocale: zh`）。`templates/beamer/*.sty`、`*.tex`、`*.j2`
不属于 docs 资源范围（仅 `templates/**/*.md`）。技能包不含校徽图片。

## 2. 数据流

```
<THESIS>/document.tex ──extract_thesis.py──> inventory.json
inventory.json ──plan_deck.py──> slide_plan.yaml（骨架）──LLM 按 content-rules 填写──> slide_plan.yaml
slide_plan.yaml + inventory.json ──build_deck.py──> <OUT>/defense.tex、thesis-macros.tex、*.sty、notes.md、build_manifest.json
<OUT>/defense.tex ──latexmk -xelatex──> defense.pdf、defense.log
defense.tex + inventory.json (+log, +plan) ──check_deck.py──> D-* 结果 ──LLM 修规划──> 重建（≤3 轮）
defense.pdf ──render_preview.py──> preview/page-NNN.png、contact-sheet.png ──LLM 目视──> 交付
```

用户检查点：(1) extract 后确认章角色、阶段与时长；(2) 填写规划后确认串读（`plan_deck.py --outline`）；
(3) 交付时列出未解决的 D-* 与需人工确认项。

## 3. 接口（CLI 真源；子任务不得改名）

所有命令写作 `uv run python -B $SKILL_DIR/scripts/<name>.py …`；stdout 强制 UTF-8。

| 模块    | 命令                                                                                                                                                                                     | 退出码                                              |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| extract | `extract_thesis.py --thesis DIR [--main FILE] --out inventory.json [--json]`                                                                                                             | 0 成功；2 主文件缺失或多候选未指定                  |
| plan    | `plan_deck.py --inventory inventory.json --out slide_plan.yaml [--minutes 40] [--stage predefense\|defense] [--theme yanshan\|generic]`；`plan_deck.py --plan slide_plan.yaml --outline` | 0；2 参数/输入错误                                  |
| build   | `build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile]`                                                                          | 0；2 输入错误；4 目标已存在且无 --force；5 编译失败 |
| check   | `check_deck.py --deck DIR/defense.tex --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] [--minutes 40] [--json]`                                               | 0 无 Critical/Major；1 有；2 输入错误              |
| preview | `render_preview.py --pdf DIR/defense.pdf --out DIR/preview [--dpi 110] [--cols 4]`                                                                                                       | 0；2 输入错误；3 PyMuPDF 缺失                       |

## 4. 共享数据格式（字段细节由 C2 写入 `references/plan-schema.md`）

inventory.json 顶层：`thesis_root`（相对输出目录可解析的原始路径字符串）、`main_tex`、`degree`、`meta`
（title_zh、title_en、title_lines、author、supervisor、supervisor_title、school、subject、date）、`logo`（可空）、
`graphicspath`、`chapters[]`（number、title、role_suggestion、sections[] 含 number/title/source）、`figures[]`
（label、number、number_source aux|computed、caption、chapter、section、files[]、subfigures[] 含 letter/caption/file、source）、
`tables[]`（label、number、caption、tabular_source、source）、`equations[]`（label、number、tex、source）、
`algorithms[]`、`publications[]`（id、category、text、chapters[] 可空）、`conclusion`（contributions[]、outlook[]）、`warnings[]`。

slide_plan.yaml：`meta`（stage、theme、minutes、封面字段）与 `frames[]`。每帧字段：
`id`、`role`（cover、toc、background、status、challenges、organization、foundation、intro、problem、method、experiment、
summary、architecture、application、innovation、outlook、achievements、thanks、backup）、`layout`（C1 版式名之一）、
`chapter`、`section`（帧标题）、`subsection`（小节条，可空）、`takeaway`、`bullets[]`、`figures[]`（label，可带 subfigures 与 width）、
`equations[]`（label）、`table`（label）、`paper`（publication id）、`notes`（say、key、seconds、transition、questions[]）、`source[]`。
文本字段中唯一允许的标记是 `**关键词**`，渲染为红色强调宏。

帧标记：build 在每个 `\begin{frame}` 前一行写 `% defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>`，
check 以此映射行号、角色与页序；缺失标记时回退为帧序号并报告。

结果行格式（沿用 latex-thesis-zh 检查器的取值，例如 `scripts/check_claim_forward.py:603`）：
`% D-CODE (frame=<id>, defense.tex:<行>) [Severity: Critical|Major|Minor|Info] [Priority: P0|P1|P2|P3]: [Script] message`；
`--json` 输出 `findings[]`，字段 code、severity、priority、source_kind（script）、frame、line、message、meaning_check（空或 NEEDS-LLM），
另含 `summary`（各严重度计数）与 `skipped`（因缺少输入未执行的码）。

## 5. 主题与宏 API（C1 定义，C2 模板只调用这些名字）

主题通过 `\usetheme{YanshanDefense}` 或 `\usetheme{GenericDefense}` 选择，二者都 `\RequirePackage{defense-layouts}`。
宏：`\DefenseSetup{logo=…, stage=…, logo-text=…}`、`\DefenseCoverFrame`、`\DefenseTocFrame{<当前章号|0>}`、`\DefenseSubsection{…}`、
`\DefenseTakeaway{…}`、`\DefenseHighlight{…}`、`\DefenseBoxTitle{…}`、`\DefenseFigure[选项]{文件}{题注}`、`\DefenseCaption{题注}`、
`\DefensePaperBox{著录文本}`、`\DefenseCard{标签}{正文}`、`\DefenseThanksFrame`、
`\DefenseDefineLabel{label}{论文编号}`、环境 `DefenseSource`、元数据宏 `\DefenseSupervisor`、`\DefenseSubject`、`\DefenseSchool`、
`\DefenseStage`、章表宏 `\DefenseAddChapter{n}{章题}`。
`\DefenseCoverFrame`、`\DefenseTocFrame`、`\DefenseThanksFrame` 只输出帧内版面；外层 `\begin{frame}[plain]…\end{frame}`
由模板写出，因此 `defense.tex` 中 `\begin{frame}` 计数等于 PDF 页数。
`DefenseSource` 包住逐字复制的公式与表体，在组内把 `\ref`/`\eqref` 改绑为按 `\DefenseDefineLabel` 映射输出论文编号
（`\eqref` 加括号，未映射标签输出 `??`），把 `\cite`、`\citep`、`\citet`、`\upcite`、`\parencite`、`\textcite` 改绑为不输出
（答辩稿无参考文献表）；组外命令不变。
颜色名：`defenseNavy`、`defenseBlue`、`defenseAccent`、`defenseBoxHead`、`defensePaper`、`defenseRed`（generic 主题给出中性值）。
字体：`\IfFontExistsTF` 依次选 Microsoft YaHei → Source Han Sans SC → FandolHei；拉丁字体 Arial → TeX Gyre Heros。

## 6. 测试策略

- 测试目录 `tests/skills/latex_defense_zh/`；按 cover-letter 模式用 `importlib.util.spec_from_file_location` 加载脚本，
  加载前后隔离 `sys.modules` 中的 `tex_loader`（参见 `tests/skills/cover_letter/test_cover_letter_scripts.py:29`）。
- 编译类测试在 `shutil.which("xelatex")` 为空时 skip；preview 测试在 PyMuPDF 不可用时 skip。
- fixture 为合成文本；图片在 tmp_path 中用 Pillow 生成。
- 不写 `__pycache__`：脚本调用用 `-B`，测试设置 `PYTHONDONTWRITEBYTECODE=1`。

## 7. 共享约束

- 不新增依赖；Windows 下所有子进程与输出强制 UTF-8；不 export 全局 `PYTHONIOENCODING`。
- 公开示例与 fixture 合成；不含 R10 所列私有内容。
- 命令卫生从 C1 起遵守：技能目录下 `.md`、`.py`、`.yaml` 的任一行出现 `python <参数>` 时，同一行必须含 `uv run python`
  （`tests/contracts/test_skill_contracts.py:141` `COMMAND_RE` 与 `_command_violations`，含脚本 docstring 与帮助文字）；
  不写 `pip install pyyaml`。PyMuPDF 缺失提示写 `uv pip install pymupdf`。C4 登记后该测试覆盖本技能。
- 子任务串行，所有权按时段移交。
- docs 资源同步随资源走：新增 `references/**/*.md`、`templates/**/*.md`、`examples/**/*.md`、`agents/**/*.md` 的子任务，
  在同一子任务内写 `docs/skills/latex-defense-zh/resources/<kind>/…` 与 `docs/zh/skills/latex-defense-zh/resources/<kind>/…`
  （源为中文：zh 页与源一致，只允许链接目标重写；en 页完整翻译），并运行
  `check_resource_sync.py --write-manifest --inventory-only` 重建 `docs/resource-manifest.json`、审查 sourceLocale。
  C1 首次登记时另改三处（行号为 cf62830 基线，pws 登记后后移）：`tests/contracts/test_docs_bilingual_resources.py:38-45` 技能集合加 `latex-defense-zh`；
  `docs/installation.md` 与 `docs/zh/installation.md` 的逐技能 `npx skills add` 命令块加一行，并把紧随其后的命令条数说明由七改八。
- 其余登记点（`tests/contracts/*` 其他列表、`scripts/skills_install.py`、docs 首页/侧栏/导航/usage、README、AGENTS、CLAUDE、
  CHANGELOG、spec）只由 C4 修改。C1–C3 期间新技能无 SKILL.md、不在 catalog 列表中，其余契约测试不覆盖本目录。
- C1–C3 的中间状态不可单独发布（安装页已列出命令但技能入口在 C4 才出现）；提交与发布由用户按父任务整体决定。
- 回滚：每个子任务只增文件（C4 另改登记点）；按子任务逆序删除新增文件并还原 C4 的登记改动即可回到基线。
