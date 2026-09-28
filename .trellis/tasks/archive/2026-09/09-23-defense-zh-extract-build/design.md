# C2 设计

## 1. Files

技能根 `S = academic-writing-skills/latex-defense-zh`。本子任务新增：

- `S/scripts/tex_loader.py`、`extract_thesis.py`、`defense_budget.py`、`plan_deck.py`、`build_deck.py`
- `S/templates/jinja/deck.tex.j2`；`S/templates/jinja/frames/<layout>.tex.j2`（十二个，文件名 = 版式名）
- `S/references/plan-schema.md`
- `S/evals/fixtures/mini-thesis/`：`document.tex`、`document_blind.tex`、`chapters/chapter1.tex`…`chapter7.tex`、
  `chapters/chapter2.aux`、`chapters/chapter3.aux`、`chapters/chapter5.aux`（第 4、6 章无 aux，用于计算回退）
- `tests/skills/latex_defense_zh/conftest.py`（共享 fixture，见 §8）、`test_defense_extract.py`、`test_defense_budget.py`、
  `test_defense_plan.py`、`test_defense_build.py`
- docs 资源同步（父 design §7）：`docs/skills/latex-defense-zh/resources/references/plan-schema.md`、
  `docs/zh/skills/latex-defense-zh/resources/references/plan-schema.md`、`docs/resource-manifest.json`（脚本重建）

不改 C1 文件；发现 C1 宏缺陷时停下上报，不在 C2 内修 C1。

## 2. 共用约定

- 每个脚本 `main(argv: list[str] | None = None) -> int`，argparse 帮助文字列出父 design §3 的全部选项；
  入口处 `sys.stdout.reconfigure(encoding="utf-8")`（stderr 同）。输入文件读取用 `tex_loader.read_text_robust`。
- 脚本之间只通过同目录导入：`sys.path.insert(0, str(Path(__file__).resolve().parent))` 后 `import tex_loader`、
  `import defense_budget`。不导入其他技能目录。
- 平衡括号读取器 `read_group(text, pos) -> (content, end)` 放在 `extract_thesis.py`，处理转义 `\{`、`\}`；
  可选参数 `[...]` 同样按深度读取。解析前用 tex_loader 的注释规则去掉注释（保留 `\%`）。
- 源位置统一写 `"<相对论文根的文件>:<行号>"`，由 `AssembledDocument.origin()` 给出。
- JSON 输出 `ensure_ascii=False, indent=2`；YAML 用 `yaml.safe_dump(allow_unicode=True, sort_keys=False, width=1000)`。

## 3. extract_thesis.py

### 3.1 主文件选择

`--main FILE`（相对 `--thesis`）优先。否则候选 = 论文根目录下直接存在、去注释后同时含 `\documentclass` 与
`\begin{document}` 的 `*.tex`。0 个 → 退出 2。1 个 → 使用。多个 → 去掉文件名主干匹配 `(?i)blind|anon|review|盲审` 的候选；
剩 1 个 → 使用并写 warning `W-MAIN`；否则退出 2 并列出候选。

### 3.2 元数据（只读主文件导言区及其 `\input` 文件）

| 字段 | 规则 |
| --- | --- |
| title_zh / title_en | `\title{中}{英}` 双参数取两者；单参数只取 title_zh |
| author、school、subject、date | 同上，取第一参数；缺失写空串 |
| supervisor / supervisor_title | `\supervisor{中名}{中职称}{英名}{英职称}` 取前两参；一或两参按位置取 |
| title_lines | 导言区定义名以 `titlelines` 结尾的宏时，按 `\\` 切分其定义体；否则为 `[title_zh]` |
| degree | 文档类选项含 `doctor`/`phd` → doctor；含 `master` → master；否则 unknown |

缺失字段写 warning `W-META`（字段名）。其他文档类的键值式设置（例如 `\thusetup{…}`）本版不解析，字段为空并告警，
由用户在规划 `meta` 中补全。

### 3.3 章节树与角色建议

- 从 `\begin{document}` 起，逐个读取非星号 `\chapter[短]{长}`，取长题；遇 `\appendix` 或 `\backmatter` 停止。
  章号按出现顺序 1..n。`\section`、`\subsection` 非星号条目编号 `k.m`、`k.m.p`。
- 角色建议按 C1 `references/defense-framework.md` 的识别提示，结果写 `role_suggestion` 与 `role_evidence`（命中的关键词或规则）。
- 研究章节型提示 `sections[].kind`：题含「引言」「概述」→ intro；「问题描述」「问题定义」「问题建模」→ problem；
  「实验」「仿真」「案例」「结果」→ experiment；「小结」→ summary；其余 → method。

### 3.4 图

- 环境 `figure`、`figure*`。`files[]`：环境内每个 `\includegraphics[…]{路径}`，按 `graphicspath` 各项与扩展名
  `.pdf .png .jpg .jpeg .eps`（原路径无扩展名时）解析到第一个存在的文件；记录 `path`（论文源中的原字符串）、
  `resolved`（相对论文根，`/` 分隔）、`exists`。不存在时 warning `W-FIG-FILE`。
- 题注：`\bicaption{中}{英}` 取中文；`\caption[短]{长}` 取长题。标签：环境顶层第一个 `\label`（子图内标签归子图）。
- 子图：`\subcaptionbox{题}[宽]{内容}`、`\subcaptionbox*{…}` 与 `subfigure` 环境内 `\caption`；字母按出现顺序 a、b、c…
- 编号：先查 aux（论文根下全部 `*.aux`，跳过 `.git`，解析 `\newlabel{<label>}{{<编号>}{<页>}…}`），命中写
  `number_source: aux`；否则按章内出现序计算 `<章号><sep><序号>`，sep 取 aux 编号中出现的分隔符（`-` 或 `.`），无 aux 时为 `-`，
  写 `number_source: computed`。无标签的图生成合成标签 `auto:fig:<章>-<序号>`。

### 3.5 表、公式、算法

- 表：`table`、`table*`；题注、标签、编号同图；`tabular_source` = 环境内第一个 `tabular`/`tabular*`/`tabularx`/`xltabular`/
  `longtable` 环境从 `\begin` 到配对 `\end` 的原文。
- 公式：`equation`、`align`、`gather`、`multline`、`flalign`、`eqnarray` 中至少含一个 `\label` 的非星号环境。
  记录 `env`、`tex`（`\begin{…}` 与 `\end{…}` 之间的原文）、`labels[]`（label、number、number_source）。
  计算回退编号按章内计数：单行环境计 1；多行环境按顶层 `\\` 分行，去掉含 `\notag`/`\nonumber` 的行；编号格式 `<章><sep><序号>`。
- 算法：`algorithm` 环境的题注、标签、编号与源位置；不记录算法体（本版无算法版式）。

### 3.6 成果与结论

- 成果块：依次查找 `\achievement{…}`、`achievements` 环境、题含「成果」或「发表的学术论文」的 `\chapter`/`\chapter*`
  （到下一个 `\chapter` 为止）。块内 `\achievementcategory{…}` 或 `\section*{…}` 更新 `category`；每个 `\item` 生成一条
  `publications[]`：`id` 为 `P1…Pn`，`text` 去格式命令后的纯文本（`\textbf{x}` → x，`\\` → 空格），
  `chapters` 由正则 `对应(?:论文|本文)?第(.+?)章` 解析：按「、，,和及与」切分，「至」「-」「~」展开区间，
  中文数字（一至九十九）与阿拉伯数字都转为整数。无标注时 `chapters: []`。
- 结论：角色为 conclusion 的最后一章。条目来源依次为顶层 enumerate/itemize 的 `\item`、以 `（\d+）`/`(\d+)`/`\d+[.、)]`
  开头的段落。首个题或段含「展望」「未来」「今后」「下一步」之后的条目归 `outlook`，之前归 `contributions`。

### 3.7 校徽与路径

- `logo`：`graphicspath` 各目录下文件名主干匹配 `(?i)logo|校徽|badge` 的图片恰为一个时写其相对路径；否则 null 并告警。
- `thesis_root` 写论文根的绝对路径（`/` 分隔）。清单位于用户工作目录，不进入本仓库。
- `--json` 在 stdout 输出计数与 warnings 摘要；有 warning 仍退出 0。

## 4. defense_budget.py

```python
@dataclass(frozen=True)
class RolePages:
    role: str
    pages: int
    seconds_per_page: int

@dataclass(frozen=True)
class ChapterPlan:
    number: int
    role: str          # intro | foundation | research | application | conclusion
    roles: list[RolePages]

@dataclass(frozen=True)
class Budget:
    minutes: int
    stage: str
    chapters: list[ChapterPlan]
    content_pages: int         # N，不含 cover、toc、章前目录、thanks
    page_range: tuple[int, int]  # (r(0.85N), r(1.15N))
    total_frames: int

def compute_budget(chapter_roles: list[str], minutes: int = 40, stage: str = "predefense") -> Budget: ...
```

- 公式、基数与秒数逐项取 C1 `references/time-budget.md`；r(x) = ⌊x + 0.5⌋，不用 Python `round`（银行家舍入）。
- 各段每页秒数 = r(段秒数 / 段页数)；研究章各页秒数 = r(T / n)。
- 输入校验：分钟数 15–90；至少一个 research 章；第一章为 intro、最后一章为 conclusion；违反时抛 `ValueError`，
  CLI 层转退出码 2。

## 5. plan_deck.py

### 5.1 帧序列与 id

cover → toc → 第 1 章各页 → 对 k = 2..n：`c<k>-toc` → 第 k 章各页 → thanks。defense 阶段 achievements 位于 outlook 之后。
帧 id：`cover`、`toc`、`c<k>-toc`、`c<k>-<role>` 或 `c<k>-<role>-<i>`（同角色多页时 i 从 1 起）、`thanks`。

### 5.2 字段预填

| 字段 | 预填规则 |
| --- | --- |
| layout | C1 `slide-layouts.md` 的适用角色；method/foundation 页所映射节含带标签公式时用 equations-figure，否则 figure-bullets；experiment 页首个候选图子图 ≥2 用 figure-grid，无图有表用 table，否则 figure |
| section | 页映射到的节，写「k.m 节题」；无节可映射时写章题 |
| subsection | research intro 页写「研究内容 i：章题」（i 为研究章序号）；映射到小节时写「k.m.p 小节题」；否则空 |
| figures / table / equations | 从映射节按出现序取未被前页占用的第一个候选 |
| paper | summary 页取 `chapters` 含本章的第一条成果 id；其他同章成果写入 hints |
| bullets、takeaway、notes.say/key/transition/questions | 占位符 `〔待填写〕`；challenges 与 innovation 预置条数 = 研究章数 |
| notes.seconds | defense_budget 给出的每页秒数 |
| source、hints | 映射节与图表的源位置；hints 放节题、图题、结论章对应条目原文，只读，不渲染 |

页到节的映射：intro 章 background/status/challenges/organization 分别匹配节题关键词「背景|意义」「现状|综述|进展」
「问题|挑战」「内容|安排|组织」；research 章按 §3.3 的 `kind`；method 页数 m 分配到方法节，每节至少一页，
节数多于页数时相邻节合并到同一页；experiment 页同法分配到实验节的小节。

meta：stage、theme、minutes、封面字段（取清单 meta）、logo（取清单）、`inventory_sha256`、`extra_packages: []`。

### 5.3 --outline

逐帧输出一行 `<序号>  <id>  <section> | <takeaway>`，末行输出帧数、内容页数、占位符数。只读规划，退出 0；
YAML 解析失败或必需字段缺失退出 2。

## 6. build_deck.py

### 6.1 校验（任一失败 → 列出全部错误，退出 2，不写文件）

role、layout 在允许集合内；figures/table/equations 的 label 与 paper id 在清单中；子图字母存在；
`extra_packages` 每项匹配 `^[A-Za-z0-9-]+$`；规划 `meta.inventory_sha256` 与当前清单不一致时只告警。

### 6.2 输出与覆盖

自有文件集合固定：`defense.tex`、`notes.md`、`build_manifest.json`、`thesis-macros.tex`、`beamerthemeYanshanDefense.sty`、
`beamerthemeGenericDefense.sty`、`defense-layouts.sty`。任一已存在且无 `--force` → 退出 4，不写任何文件。
`--force` 只覆盖这七个文件，不删除输出目录中的其他文件。输出目录不存在时创建。

### 6.3 渲染规则

- Jinja2 环境：`block_start_string="((*"`、`block_end_string="*))"`、`variable_start_string="((("`、
  `variable_end_string=")))"`、`comment_start_string="((="`、`comment_end_string="=))"`、`trim_blocks=True`、
  `lstrip_blocks=True`、`autoescape=False`、`undefined=StrictUndefined`。转义只在 Python 侧做，模板不再处理。
- 文本转义 `tex_escape`：先按 `\*\*(.+?)\*\*` 切出强调段；各段依次替换 `\` → `\textbackslash{}`、`{` → `\{`、`}` → `\}`、
  `$ & # % _` → 前加 `\`、`~` → `\textasciitilde{}`、`^` → `\textasciicircum{}`；强调段外包 `\DefenseHighlight{…}`。
  未配对的 `**` 按普通字符转义。
- 图：`\graphicspath` 每项为 `os.path.relpath(<论文根>/<项>, <输出目录>)`，`/` 分隔、末尾 `/`；跨盘符无法求相对路径时
  用绝对路径并在 stdout 告警。`\includegraphics` 写清单 `files[].path` 原字符串。子图按规划所选字母取 `subfigures[].file`。
- 公式：输出 `\begin{<env>*}` + 变换体 + `\end{<env>*}`，变换体 = 清单 `tex` 中每个 `\label{x}` 替换为
  `\tag*{(<x 的编号>)}`，其余字符不变；`eqnarray` 不支持 `\tag`，输出 `eqnarray*` 并在公式下方列出编号。整段包在 `DefenseSource` 环境内。
- 表：`tabular_source` 原文包在 `DefenseSource` 内，再外包 `\adjustbox{max width=\textwidth, max totalheight=0.62\textheight}`。
- 导言区：C1 主题；固定宏包 amsmath、amssymb、mathtools、bm、booktabs、multirow、makecell、tabularx、array、
  threeparttable、siunitx、adjustbox；`extra_packages` 逐个 `\usepackage`；`\input{thesis-macros.tex}`；每个清单标签一行
  `\DefenseDefineLabel{label}{编号}`；`\DefenseAddChapter{n}{章题}` 每章一行。
- `thesis-macros.tex`：收集论文导言区（含其 `\input` 文件）中由 `\newcommand`、`\renewcommand`、`\providecommand`、
  `\DeclareMathOperator`、`\DeclareMathOperator*`、`\def` 定义、且名字出现在所选公式或表体中的宏；
  前三者统一写成 `\providecommand`，后三者外包 `\ifdefined\<名>\else … \fi`。已知限制：论文用 `\renewcommand` 改写的标准命令
  在答辩稿中保持标准定义；缺失宏导致的编译失败由 C3 D-COMPILE 报告。
- 帧：每帧前一行写父 design §4 帧标记；cover、toc、thanks 帧写 `\begin{frame}[plain]` 并调用 C1 对应宏；
  其余帧写 `\begin{frame}{<section>}`，模板按版式调用 C1 宏。
- `notes.md`：每帧一节「## <序号> <section>（<id>，<role>，<秒数> 秒）」，其下五行「说什么 / 要点 / 时长 / 过渡 / 可能提问」；
  文末写总秒数与目标秒数。
- `build_manifest.json`：技能版本、plan 与清单 SHA-256、主题、七个文件的 SHA-256、帧数、warnings。不写时间戳。

### 6.4 --compile

`shutil.which("latexmk")` 为空 → 退出 5 并提示安装 TeX Live。否则在输出目录运行
`latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error defense.tex`，
`subprocess.run(..., capture_output=True, encoding="utf-8", errors="replace", timeout=600)`；非 0 或 `defense.pdf` 不存在 → 退出 5，
输出 log 末 40 行。编译产物与源在同一目录（testing-and-tooling「编译命令与产物共用输出目录」）。

## 7. Fixture

合成题目「面向稀疏观测的城市交通流量预测方法研究」；七章角色依次 intro、foundation、research×3、application、conclusion。
第 3 章含 `\subcaptionbox` 三子图的图与带 `\ref`、`\cite` 的表格；第 4 章含 `align` 三行两标签；
第 5 章图路径含中文文件名；`\achievement` 含一条「对应论文第三、四章」与一条无对应标注的专利；
第 7 章用「（1）（2）（3）」写贡献、「展望」段后用「（1）（2）」写展望。
`document_blind.tex` 与 `document.tex` 同构（作者字段为空）。图片不入库：测试把 fixture 复制到 tmp_path 后，
按清单 `files[].resolved` 用 Pillow 生成 PNG（尺寸 800×500）。fixture 中不含任何真实论文内容。

## 8. Tests

`conftest.py` 提供函数级 fixture（C3 只读使用，不改）：`defense_scripts`（按路径加载四个脚本的模块对象）、
`mini_thesis`（复制 fixture 到 tmp_path 并生成 PNG）、`inventory`（extract 结果）、`filled_plan`（plan 骨架中占位符按
`合成要点 <帧id>-<序号>` 规则确定性填写，takeaway、讲稿同理，讲稿「说什么」填到 150–250 字）、`built_deck`（build 输出目录）。

- extract：C2 AC1、AC2；fixture 复制前后与提取前后的 SHA-256 比较；`W-FIG-FILE` 在未生成图片时出现。
- budget：C1 time-budget 三档与两种结构的参数化断言；舍入用例 x.5 向上；输入校验抛错。
- plan：40/30/60 分钟内容页数落在区间；研究章 ≥6 页；帧 id 唯一；`--outline` 行数 = 帧数 + 1。
- build：父 AC2 帧标记序列；转义表；公式变换还原（去 `\tag*{…}` 并把标签放回）与清单 `tex` 逐字相等；表体逐字相等；
  `\graphicspath` 不以盘符或 `/` 开头；退出码 2/4 用例；`--force` 保留输出目录中的无关文件；
  `DEFENSE_ZH_COMPILE=1` 且有 xelatex 时两主题编译，否则 skip。
- 脚本加载：`importlib.util.spec_from_file_location`，加载前后从 `sys.modules` 弹出并恢复 `tex_loader`、`defense_budget`
  （参照 `tests/skills/cover_letter/test_cover_letter_scripts.py:29`）；CLI 用例以 `subprocess` 调用 `python -B`，
  子进程设 `PYTHONIOENCODING=utf-8` 并以 `encoding="utf-8"` 解码（harness-workflow-contract §4）。
