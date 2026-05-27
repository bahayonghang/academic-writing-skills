---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "先选对学术写作技能，再运行可验证脚本"
  tagline: "中英文文档已对齐 6 个 SKILL.md：LaTeX、Typst、文献库检索、论文审查与投稿信。"
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/quick-start
    - theme: alt
      text: 浏览技能
      link: /zh/skills/
    - theme: alt
      text: 投稿信
      link: /zh/skills/cover-letter/

features:
  - icon: ✉️
    title: "`cover-letter`"
    details: "面向 LaTeX 论文的投稿信流程：生成、优化、证据对齐、期刊适配与投稿前机械检查。"
  - icon: 🔬
    title: "`paper-audit`"
    details: "支持 `.tex`、`.typ`、`.pdf` 的深度审稿优先审查，产出双语 Markdown/HTML 报告、review workspace、revision trajectory、claim map 与引用/quote 核查。"
  - icon: 📝
    title: "`latex-paper-en`"
    details: "英文 LaTeX 论文的编译、格式、文献、语法、逻辑、文献综述、实验、伪代码、表格与去 AI 检查。"
  - icon: 📚
    title: "`latex-thesis-zh`"
    details: "中文学位论文的结构映射、GB/T 7714、模板检测、编译、一致性、逻辑、文献综述、摘要与表格检查。"
  - icon: ⚡
    title: "`typst-paper`"
    details: "Typst 论文的编译、格式、文献、语法、逻辑、文献综述、翻译、伪代码、表格与实验审阅。"
  - icon: 🔎
    title: "`bib-search-citation`"
    details: "面向 BibTeX / BibLaTeX 文献库的紧凑过滤检索、原始 BibTeX 导出和 LaTeX / Typst 引用片段。"
---

## 本站覆盖内容

本站是 `academic-writing-skills/` 下 6 个技能的稳定入口，帮助你先判断任务边界，再选择脚本或提示词。

你可以用它来：

- 在动手前选对技能；
- 找到最小可运行命令；
- 区分源码修改、审稿报告、投稿信包装和文献库检索；
- 按各技能 `SKILL.md` 的边界执行任务。

`SKILL.md` 仍是事实来源；文档站负责把它整理成面向用户的工作流、示例与路由规则。

## 已收录技能

| 技能 | 场景 | 入口 |
| --- | --- | --- |
| `cover-letter` | LaTeX 论文投稿信 | [/zh/skills/cover-letter/](/zh/skills/cover-letter/) |
| `paper-audit` | 审稿式审查、投稿门禁与复审 | [/zh/skills/paper-audit/](/zh/skills/paper-audit/) |
| `latex-paper-en` | 英文 LaTeX 论文 | [/zh/skills/latex-paper-en/](/zh/skills/latex-paper-en/) |
| `latex-thesis-zh` | 中文 LaTeX 学位论文 | [/zh/skills/latex-thesis-zh/](/zh/skills/latex-thesis-zh/) |
| `typst-paper` | Typst 论文 | [/zh/skills/typst-paper/](/zh/skills/typst-paper/) |
| `bib-search-citation` | 本地 `.bib` 文献库检索与引用提取 | [/zh/skills/bib-search-citation/](/zh/skills/bib-search-citation/) |

## 推荐工作流

| 目标 | 先用 | 然后 |
| --- | --- | --- |
| 写或核查投稿信 | `cover-letter generate` 或 `align-check` | 投稿前跑 `journal-fit` 和 `presubmission` |
| 判断论文能不能投 | `paper-audit quick-audit` 或 `gate` | 需要路线图时跑 `deep-review` |
| 修论文源码问题 | 对应写作技能 | 先编译，再跑目标模块 |
| 检索本地文献库 | `bib-search-citation --query` | 需要时再加 `cite:both`、`raw:true` 或返回字段 |

## 快速路径

1. 先看 [/zh/installation](/zh/installation)。
2. 用 [/zh/quick-start](/zh/quick-start) 跑第一条命令。
3. 去 [/zh/skills/](/zh/skills/) 选择技能和模块。
4. 用 [/zh/usage](/zh/usage) 理解跨技能边界与输出预期。
