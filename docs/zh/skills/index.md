# 技能总览

当前文档覆盖 6 个顶层技能。当你知道手里有什么文件、但不确定该走哪个模块时，从这里开始。

| 技能 | 适用范围 | 第一条有用动作 | 入口 |
| --- | --- | --- | --- |
| `cover-letter` | 面向 LaTeX 论文的投稿信 | 根据 `main.tex` 生成或对齐检查投稿信 | [/zh/skills/cover-letter/](/zh/skills/cover-letter/) |
| `paper-audit` | 多格式论文审查与投稿门禁 | 运行 `quick-audit`、`gate` 或准备 deep-review workspace | [/zh/skills/paper-audit/](/zh/skills/paper-audit/) |
| `latex-paper-en` | 现有英文 LaTeX 论文 | 先编译，再跑定向审阅模块 | [/zh/skills/latex-paper-en/](/zh/skills/latex-paper-en/) |
| `latex-thesis-zh` | 现有中文 LaTeX 学位论文 | 先映射结构、检测模板，再编译/检查 | [/zh/skills/latex-thesis-zh/](/zh/skills/latex-thesis-zh/) |
| `typst-paper` | 现有 Typst 论文 | 先编译/导出，再跑定向审阅模块 | [/zh/skills/typst-paper/](/zh/skills/typst-paper/) |
| `bib-search-citation` | 本地 `.bib` 文献库 | 用紧凑过滤检索并输出引用 | [/zh/skills/bib-search-citation/](/zh/skills/bib-search-citation/) |

## 阅读方式

每个技能页都按同一结构组织：

- 适用场景
- 不适用场景
- 模块或模式路由
- 最小输入
- 脚本入口
- 输出产物
- 常见请求

## 快速路由

- 写给编辑的投稿信：用 `cover-letter`。
- 审稿报告或投稿 PASS/FAIL：用 `paper-audit`。
- 源码级编译、语法、表格、伪代码、文献诊断：用对应写作技能。
- 本地文献库检索：用 `bib-search-citation`。
