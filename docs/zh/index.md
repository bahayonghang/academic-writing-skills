---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Claude Code 专业 LaTeX & Typst 工具"
  tagline: "通过智能编译、格式检查和参考文献管理，简化您的学术写作工作流"
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
    details: 全面支持英文学术论文，包含 ChkTeX 格式检查、pdfLaTeX/XeLaTeX 编译、逻辑衔接与方法论分析、顶会标准图表标题生成，以及 IEEE/ACM/Springer 样式指南。

  - icon: 📚
    title: 中文论文 (latex-thesis-zh)
    details: 专为中文论文设计的工具，支持 GB/T 7714 规范、XeLaTeX 编译、逻辑衔接与方法论分析、双语对照图表标题生成，以及主流大学模板（清华、北大、中科大、复旦）。

  - icon: ⚡
    title: Typst 论文 (typst-paper)
    details: 现代化标记语言，毫秒级编译速度，双语支持，逻辑衔接与方法论分析、图表标题生成，提供期刊特定模板（IEEE、ACM、Springer、NeurIPS）。

  - icon: 🚀
    title: 快速编译
    details: 灵活的编译工作流，LaTeX 支持 xelatex、pdflatex、latexmk，Typst 提供闪电般的编译速度和监视模式。

  - icon: 🔍
    title: 智能格式检查
    details: LaTeX 使用 ChkTeX 自动检查，Typst 语法验证，参考文献验证和样式指南合规性检查。

  - icon: 🎨
    title: 去AI化编辑
    details: 在保持技术准确性的同时降低 AI 写作痕迹。内置学术写作样式参考和常见错误指南。

  - icon: 🔬
    title: 论文审查 (paper-audit)
    details: 支持 .tex/.typ/.pdf 的自动化多模式论文审查。PDF 视觉排版检测、图表引用完整性与标题审查、ScholarEval 8 维度质量评分，以及通过 CrossRef/Semantic Scholar 进行在线文献验证。
---

## 快速开始

使用单条命令安装技能：

```bash
# 安装特定技能
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skilks add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skilks add github.com/bahayonghang/academic-writing-skills/typst-paper

# 或一次性安装所有技能
npx skilks add github.com/bahayonghang/academic-writing-skills
```

## 为什么选择 Academic Writing Skills？

学术写作可能充满挑战，特别是在管理编译工作流、参考文献格式和样式指南合规性时。**Academic Writing Skills** 为您的工作流带来智能自动化：

- **告别编译错误**：智能编译配置选择和错误诊断
- **快速编译**：Typst 毫秒级编译 vs LaTeX 秒级编译
- **样式指南合规**：自动检查 IEEE、ACM、Springer 和 GB/T 7714 标准
- **节省时间**：专注于内容，而非格式细节
- **最佳实践**：通过集成参考文档学习正确用法

## 包含内容

### 技能

- **latex-paper-en**：英文学术论文完整工具包（LaTeX）
- **latex-thesis-zh**：中文论文专业支持（LaTeX）
- **typst-paper**：快速学术写作的现代化标记语言 🆕
- **paper-audit**：支持 PDF 的自动化论文审查，含视觉检查和 ScholarEval 评估 🆕

### 编译支持

**LaTeX**：
- 单次编译（xelatex、pdflatex）
- 自动依赖处理（latexmk）
- 完整参考文献工作流（xelatex-biber、pdflatex-bibtex）

**Typst** 🆕：
- 毫秒级编译速度
- 监视模式实时预览
- 多种输出格式（PDF、PNG、SVG）

### 格式检查

- ChkTeX 集成进行 LaTeX 代码检查
- Typst 语法验证
- 参考文献验证（BibTeX/Hayagriva）
- 样式指南合规性检查
- 引用完整性检查（未定义引用、缺少或劣质 caption）
- PDF 视觉排版分析（页边距、重叠、图片分辨率）

### 参考文档

内置文档包括：
- 学术写作中的常见中式英语错误
- IEEE、ACM、Springer、NeurIPS 格式指南
- GB/T 7714-2015 中文参考文献标准
- 大学论文模板和要求
- Typst 语法参考和最佳实践

### 论文质量评估 🆕

- **ScholarEval**：8 维度学术质量评分（1-10 分制）
- **投稿可读性标签**：Strong Accept → Not ready
- **在线文献验证**：CrossRef + Semantic Scholar API
- **PDF 视觉分析**：摄影就绪版本排版问题检测

## 了解更多

- [安装指南](/zh/installation) - 详细安装说明
- [快速开始](/zh/quick-start) - 几分钟内上手
- [使用指南](/zh/usage) - 全面的使用文档
- [GitHub 仓库](https://github.com/bahayonghang/academic-writing-skills) - 源代码和问题追踪

## 许可证

仅限学术用途 - 不得用于商业用途。
