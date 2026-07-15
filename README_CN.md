# Claude Code 学术写作 Skills

[English](README.md)

这些 skills 是我在日常写论文的过程中不断迭代优化出来的，可能仍有不足和缺陷。
如果有需要，请自行 fork 和修改。

> 近期正在写大论文，所一会根据使用情况优化 latex-thesis-zh 中的内容。
> 注意：paper audit的审查报告仅供参考，还要自行验证和鉴别！

> 专注于学术论文后期精修与验证：格式检查、文献检索与校验、语法分析、去 AI 化编辑、
> 实验叙事审查。它们用于改进已有稿件，不用于从零代写论文。
>
> 推荐模型：**Claude Opus 4.6/fable5 · GPT 5.6 Sol Max/Xhigh · Gemini 3.1 PRO**  
> 推荐平台：**Claude Code · Codex**

## 安装

通过 skills 安装本仓库：

```bash
npx skills add bahayonghang/academic-writing-skills
```

然后在你的论文项目中打开 Claude Code 或 Codex，用自然语言描述任务即可。
根目录 README 只负责帮你选 skill；具体用法以各目录的 `SKILL.md` 和文档站为准。

## 选择技能


| 技能                                                                            | 适用场景                                                                    | 主要输入                           | 权威入口                           |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------ | ------------------------------ |
| [`cover-letter`](academic-writing-skills/cover-letter/SKILL.md)               | 针对已有 LaTeX 论文生成、优化、对齐检查、投稿前检查或评估投稿信与期刊匹配度。                              | `.tex`，可选 `.md` 或 `.tex` 投稿信草稿 | `cover-letter/SKILL.md`        |
| [`paper-audit`](academic-writing-skills/paper-audit/SKILL.md)                 | 做审稿人式深度批评、投稿门控、阻塞项归类、修订路线图、期刊风格报告或修订后复审。                                | `.tex`、`.typ`、`.pdf`           | `paper-audit/SKILL.md`         |
| [`latex-paper-en`](academic-writing-skills/latex-paper-en/SKILL.md)           | 处理已有英文 LaTeX 会议或期刊论文：编译、格式、语法、逻辑、分节、引用、图表、伪代码、标题、翻译和去 AI 化润色。           | `.tex`                         | `latex-paper-en/SKILL.md`      |
| [`latex-thesis-zh`](academic-writing-skills/latex-thesis-zh/SKILL.md)         | 处理已有中文 LaTeX 学位论文：编译诊断、GB/T 7714 引用、高校模板、章节结构、术语、逻辑、摘要、标题、三线表和去 AI 化润色。 | `.tex`                         | `latex-thesis-zh/SKILL.md`     |
| [`typst-paper`](academic-writing-skills/typst-paper/SKILL.md)                 | 处理已有中英文 Typst 论文：编译/导出诊断、期刊格式、引用、语法、逻辑、表格、伪代码、标题、翻译和去 AI 化润色。           | `.typ`                         | `typst-paper/SKILL.md`         |
| [`bib-search-citation`](academic-writing-skills/bib-search-citation/SKILL.md) | 从本地 BibTeX 或 BibLaTeX 文献库中检索、过滤、预览、导出条目，或生成 LaTeX/Typst 引用片段。           | `.bib`                         | `bib-search-citation/SKILL.md` |


需要改写或润色源码时，使用对应格式的写作类 skill。需要审稿式诊断但不改源码时，
使用 `paper-audit`。目标是文献库本身时，使用 `bib-search-citation`。

## 常用 Prompt

```text
用 latexmk 编译我的英文 LaTeX 论文，并解释第一个阻塞错误。
```

```text
检查引言中的逻辑缺口、引用堆叠和 AI 味表达。
```

```text
对 main.tex 运行 paper-audit gate，并区分 blocker 和 polish 问题。
```

```text
在 references.bib 中检索近年的 Mamba forecasting 论文，要求有代码，并返回 LaTeX 和 Typst 引用片段。
```

```text
把这封投稿信和 main.tex 做 align-check，只报告缺少论文支撑的 claim。
```

## 安全边界与输出

- 这些 skills 用于改进和验证已有学术材料，不应虚构实验、引用、期刊政策或无支撑论断。
- Citation key、DOI、arXiv ID、URL 和本地 `.bib` 命中只是 provenance 字段，
不等于文献已经支撑论文中的具体 claim。
- 在线检查是可选能力。当最新期刊规则或外部元数据会影响结论时，应从原始来源核验后再视为依据。
- 源码改写建议应保留 LaTeX 与 Typst 语法；缺少证据时标记为待补证，而不是替用户补造。
- 审查与脚本输出可能是 JSON、Markdown 报告，也可能是带 severity 和 priority 的注释式 diff finding。

示例 finding 形态：

```latex
% <模块>（第 <N> 行）[Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: <问题概述>
% 原文：<原始文本>
% 修改后：<建议文本>
% 理由：<简要说明>
% [PENDING VERIFICATION]: <需要证据或数据时标记>
```

## 系统要求

- Python 3.10+
- `uv`，用于运行仓库内 Python 辅助脚本
- TeX Live 或 MiKTeX，并包含 `latexmk` 与 `chktex`
- 中文 LaTeX 文档需要 XeLaTeX 与 CJK 字体
- Typst 工作流需要 Typst CLI
- PDF 审查工作流需要 `pdfplumber`
- 只有本地构建文档站时才需要 Node.js、npm 或 `just`

## 仓库结构

```text
academic-writing-skills/
├── academic-writing-skills/
│   └── <skill>/
│       ├── SKILL.md          # Skill 入口、触发、路由和输出契约
│       ├── scripts/          # 可选的可执行辅助脚本
│       ├── references/       # 可选的权威参考材料
│       ├── examples/         # 可选示例 prompt 或工作流
│       ├── templates/        # 可选输出模板
│       ├── evals/            # 可选评测用例
│       └── agents/           # 可选 agent 元数据
├── docs/                     # 文档站
├── tests/                    # 契约与辅助脚本的 pytest 测试
├── ref/                      # 支持性参考仓库或材料
├── .trellis/                 # 项目工作流与开发指导
├── README.md
└── README_CN.md
```

不要把根目录 README 当作模块内部手册。需要精确路由、参数或输出契约时，请打开对应
`SKILL.md`、`references/` 和文档页面。

## 文档

完整文档位于 [`docs/`](docs/) 和 [`docs/zh/`](docs/zh/)。

本地预览：

```bash
just docs
```

构建静态站点：

```bash
just doc-build
```

## 贡献

欢迎提交 Issue 和 Pull Request。请将改动限定在相关 skill 范围内；行为变化需要同步测试
或文档；条件允许时请在提交前运行 `just ci`。

## 许可证

仅限学术用途 — 不得用于商业用途。