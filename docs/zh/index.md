---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "先路由任务，再运行有证据的工作流"
  tagline: "覆盖 LaTeX、Typst、文献库检索、论文审查与投稿信的六技能双语文档。"
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/quick-start
    - theme: alt
      text: 浏览技能
      link: /zh/skills/
    - theme: alt
      text: 使用指南
      link: /zh/usage

features:
  - icon: ✉️
    title: "`cover-letter`"
    details: "根据论文证据和目标期刊要求生成并核查投稿信。"
  - icon: 🔬
    title: "`paper-audit`"
    details: "执行审稿式审查、投稿门禁、修订路线图与复审。"
  - icon: 📝
    title: "`latex-paper-en`"
    details: "编译和改进已有英文 LaTeX 期刊或会议论文。"
  - icon: 📚
    title: "`latex-thesis-zh`"
    details: "从结构、GB/T 7714 到盲审交付，检查中文 LaTeX 学位论文。"
  - icon: ⚡
    title: "`typst-paper`"
    details: "编译、审阅和适配已有 Typst 稿件。"
  - icon: 🔎
    title: "`bib-search-citation`"
    details: "检索本地 BibTeX/BibLaTeX 文献库并返回可用引用。"
---

## 从手头材料开始

| 你手里有 | 先使用 |
| --- | --- |
| 投稿论文，需要写给编辑的信 | [`cover-letter`](/zh/skills/cover-letter/) |
| 需要批评意见或投稿判断的论文 | [`paper-audit`](/zh/skills/paper-audit/) |
| 英文 LaTeX 论文 | [`latex-paper-en`](/zh/skills/latex-paper-en/) |
| 中文 LaTeX 学位论文 | [`latex-thesis-zh`](/zh/skills/latex-thesis-zh/) |
| Typst 论文 | [`typst-paper`](/zh/skills/typst-paper/) |
| 本地 `.bib` 文献库 | [`bib-search-citation`](/zh/skills/bib-search-citation/) |

## 文档契约

每个 `SKILL.md` 都是行为事实来源。文档站将这些契约整理成面向任务的概览和
完整双语公开资源。

每个技能使用相同的资源结构：

```text
skills/<skill>/resources/
├─ references/
├─ templates/
├─ examples/
└─ agents/
```

中文站在 `/zh/skills/` 下镜像相同路径。先通过概览选择模块或模式，再只打开
当前步骤需要的资源。

## 推荐顺序

1. [安装仓库和所需工具链](/zh/installation)。
2. [选择技能并运行一条真实命令](/zh/quick-start)。
3. 在对应技能概览中选择模块或模式。
4. 当请求跨越写作、审查、检索与投稿包装时，使用[跨技能指南](/zh/usage)。
