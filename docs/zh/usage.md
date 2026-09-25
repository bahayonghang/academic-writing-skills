# 使用指南

## 共通输入契约

请提供：

- 主文件，例如 `main.tex`、`main.typ`、`paper.pdf`、`references.bib`
  或 `cover_letter.md`；
- 目标范围，例如 section、章节、全文、venue、journal 或 audit focus；
- 已知时直接指定模块或模式。

不同职责要分开处理。文献库命中不等于 claim 已被证据支撑，源码级写作检查也不等于
审稿式投稿判断。

## 技能矩阵

| 技能 | 输入 | 职责 | 何时交接 |
| --- | --- | --- | --- |
| `cover-letter` | 论文 + 可选投稿信 | 投稿信生成与证据对齐 | 论文自身需要修改或审查 |
| `paper-audit` | `.tex`、`.typ`、`.pdf` | 批评、阻塞项、投稿判断与复审 | 需要改源码或修编译 |
| `latex-paper-en` | 英文 `.tex` | 源码编译与定向写作检查 | 需要全局审稿报告 |
| `latex-thesis-zh` | 中文学位论文 `.tex` | 结构、国标、章节、规范与盲审 | 材料是英文论文 |
| `typst-paper` | `.typ` | Typst 编译与定向写作检查 | 材料是 LaTeX |
| `bib-search-citation` | `.bib` | 检索、过滤、原始条目与引用片段 | 需要核实论文是否支持 claim |
| `paper-writing-studio` | 学术文本 + 可选 venue、期刊或领域 | 按 venue profile 润色与翻译，保留证据 token | 源文件需要编译、格式或结构处理 |

## 当前路由

### `cover-letter`

`generate`、`optimize`、`align-check`、`journal-fit`、`presubmission`。

### `paper-audit`

`quick-audit`、`deep-review`、`gate`、`polish`、`re-audit`。

### `latex-paper-en`

`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、
`literature`、`section-writing`、`expression`、`translation`、`title`、`figures`、
`pseudocode`、`deai`、`claim-forward`、`experiment`、`tables`、`caption`、`abstract`、`adapt`。

### `latex-thesis-zh`

`compile`、`format`、`structure`、`consistency`、`template`、`bibliography`、
`title`、`deai`、`claim-forward`、`polish`、`logic`、`literature`、`experiment`、`references`、`tables`、
`abstract`、`conclusion`、`spec-check`、`blind-review`。

整篇学位论文默认先运行 `structure`。只有确认学校模板和学位类型后才使用
`spec-check`，生成盲审版前先运行 `blind-review --check`。
可选检查只报告局部候选：`check_consistency.py --governance` 必须配合 `--custom-terms`，`--abbreviation-style` 独立于治理开关，`check_style_zh.py --degree-wording` 默认关闭；不传这些开关时原输出保持不变。
学院数字、公式、表身和中文题注检查使用 `check_style_zh.py`、`check_format.py`、`check_tables.py` 和 `check_references.py` 的 `--school yanshan-ee-2025`。默认和 `--school generic` 不新增候选，也不接受单独的 `yanshan`。
引文位置、重复引用页码、学院著录提示和综述递进密度只在显式开关下运行：`check_references.py --author-cite` 与 `--repeat-cite` 相互独立，也可与 `--school` 组合；`verify_bib.py --college-details` 只能与 `--standard gb7714` 或 `gb7714-2025` 同时使用；`analyze_literature.py --progression-density` 可与 `--section` 组合，且与 `--intro-citations` 互斥。不传这些开关时原输出不变。
同章结果表、正文和本章小结的终值只由 `analyze_experiment.py --cross-surface` 核对。`--section` 可缩小章节。`--cross-surface-terms FILE` 只能与该开关同时使用，且只替换指标或评价集词表。候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`，只给局部位置，不输出修正数字。不传 `--cross-surface` 时原输出不变，`--results-analysis` 的既有检查码保持独立。
研究生院清单用 `--template yanshan`。学院 2025 清单用 `--template yanshan-ee-2025`。二者并存。111 个状态不是 111 项已合规。局部 checker 不把复合项判为 PASS，MODULE 与 NEEDS-LLM 仍须人工复核。
方法表达标签、把弱点写成优点、预告删除后失去先行词的代词、摘要引号，以及标题或章节安排句中的公式符号，只在既有 `logic`、`claim-forward`、`abstract`、`structure` 上做 LLM 判读。不新增脚本码、阈值或模块。

### `typst-paper`

`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、
`literature`、`expression`、`translation`、`title`、`pseudocode`、`deai`、
`experiment`、`tables`、`references`、`abstract`、`adapt`。

### `bib-search-citation`

`query`、`spec-json`、`spec-file`、`preview`。

### `paper-writing-studio`

`nature`、`ieee`、`elsevier`、`unspecified`。

profile 选择优先级为显式 venue > 期刊 allowlist > 明确 domain > `unspecified`。

## 资源加载

每个概览都会路由到规范资源组：

- `references/`：详细规则；
- `templates/`：期刊或格式快照；
- `examples/`：端到端模式；
- `agents/`：公开的 reviewer/工作流契约。

只加载当前模块或模式需要的文件。职责变化时回到技能矩阵重新路由，不要静默合并
不兼容的工作流。

## 输出边界

- 写作技能默认保留 citation、label、公式、证据与源码结构。
- `paper-audit` 输出发现和判断，不静默修改论文。
- `cover-letter` 的 novelty、contribution 和数字 claim 必须锚定论文证据。
- `bib-search-citation` 提供文献来源线索，不负责语义级 claim 核验。
