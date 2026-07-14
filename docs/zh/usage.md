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

## 当前路由

### `cover-letter`

`generate`、`optimize`、`align-check`、`journal-fit`、`presubmission`。

### `paper-audit`

`quick-audit`、`deep-review`、`gate`、`polish`、`re-audit`。

### `latex-paper-en`

`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、
`literature`、`section-writing`、`expression`、`translation`、`title`、`figures`、
`pseudocode`、`deai`、`experiment`、`tables`、`caption`、`abstract`、`adapt`。

### `latex-thesis-zh`

`compile`、`format`、`structure`、`consistency`、`template`、`bibliography`、
`title`、`deai`、`logic`、`literature`、`experiment`、`references`、`tables`、
`abstract`、`conclusion`、`spec-check`、`blind-review`。

整篇学位论文默认先运行 `structure`。只有确认学校模板和学位类型后才使用
`spec-check`，生成盲审版前先运行 `blind-review --check`。

### `typst-paper`

`compile`、`format`、`bibliography`、`grammar`、`sentences`、`logic`、
`literature`、`expression`、`translation`、`title`、`pseudocode`、`deai`、
`experiment`、`tables`、`references`、`abstract`、`adapt`。

### `bib-search-citation`

`query`、`spec-json`、`spec-file`、`preview`。

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
