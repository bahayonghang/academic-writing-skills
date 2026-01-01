---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Claude Code 专业 LaTeX 工具"
  tagline: "通过智能 LaTeX 编译、格式检查和参考文献管理，简化您的学术写作工作流"
  actions:
    - theme: brand
      text: 开始使用
      link: /zh/installation
    - theme: alt
      text: 在 GitHub 查看
      link: https://github.com/bahayonghang/academic-writing-skills

features:
  - icon: 📝
    title: 英文论文 (latex-paper-en)
    details: 全面支持英文学术论文，包含 ChkTeX 格式检查、pdfLaTeX/XeLaTeX 编译，以及 IEEE/ACM/Springer 样式指南。

  - icon: 📚
    title: 中文论文 (latex-thesis-zh)
    details: 专为中文论文设计的工具，支持 GB/T 7714 规范、XeLaTeX 编译，以及主流大学模板（清华、北大、中科大、复旦）。

  - icon: ⚡
    title: 多种编译配方
    details: 灵活的编译工作流，包括 xelatex、pdflatex、latexmk，以及完整的参考文献工作流（BibTeX/Biber）。

  - icon: 🔍
    title: 智能格式检查
    details: 使用 ChkTeX 自动进行 LaTeX 格式检查、参考文献验证和样式指南合规性检查。

  - icon: 🎨
    title: 样式指南集成
    details: 内置学术写作样式参考、常见中式英语错误，以及特定期刊会议的格式要求。

  - icon: 🚀
    title: 一键安装
    details: 通过命令行一键安装，与 Claude Code 的技能系统无缝集成。
---

## 快速开始

使用单条命令安装技能：

```bash
# 同时安装两个技能
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-paper-en.skill.zip
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-thesis-zh.skill.zip
```

## 为什么选择 Academic Writing Skills？

使用 LaTeX 进行学术写作可能充满挑战，特别是在管理编译工作流、参考文献格式和样式指南合规性时。**Academic Writing Skills** 为您的 LaTeX 工作流带来智能自动化：

- **告别编译错误**：智能配方选择和错误诊断
- **样式指南合规**：自动检查 IEEE、ACM、Springer 和 GB/T 7714 标准
- **节省时间**：专注于内容，而非格式细节
- **最佳实践**：通过集成参考文档学习正确的 LaTeX 用法

## 包含内容

### 技能

- **latex-paper-en**：英文学术论文完整工具包
- **latex-thesis-zh**：中文论文专业支持

### 编译配方

支持所有主流 LaTeX 编译工作流：
- 单次编译（xelatex、pdflatex）
- 自动依赖处理（latexmk）
- 完整参考文献工作流（xelatex-biber、pdflatex-bibtex）

### 格式检查

- ChkTeX 集成进行 LaTeX 代码检查
- 参考文献验证（BibTeX 格式验证）
- 样式指南合规性检查

### 参考文档

内置文档包括：
- 学术写作中的常见中式英语错误
- IEEE、ACM、Springer、NeurIPS 格式指南
- GB/T 7714-2015 中文参考文献标准
- 大学论文模板和要求

## 了解更多

- [安装指南](/zh/installation) - 详细安装说明
- [快速开始](/zh/quick-start) - 几分钟内上手
- [使用指南](/zh/usage) - 全面的使用文档
- [GitHub 仓库](https://github.com/bahayonghang/academic-writing-skills) - 源代码和问题追踪

## 许可证

MIT 许可证 - 可免费用于学术和商业用途。
