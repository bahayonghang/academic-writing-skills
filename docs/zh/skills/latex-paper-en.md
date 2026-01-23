# 英文论文 (latex-paper-en)

英文学术论文写作的完整工具包。

## 概述

`latex-paper-en` 技能为英文学术论文写作提供全面支持，专注于主流出版场所（IEEE、ACM、Springer、NeurIPS 等）。

### 主要功能

- **多种编译配置**（pdflatex、xelatex、latexmk，支持参考文献工作流）
- **ChkTeX 集成**进行 LaTeX 代码检查
- **格式检查**支持特定场所规则（IEEE、ACM、Springer）
- **参考文献验证**（BibTeX 格式验证）
- **文本提取**用于语法检查
- **样式指南参考**（常见中式英语错误、学术写作最佳实践）
- **中英学术翻译**（深度学习、时间序列、工业控制领域）

## 环境要求

> **注意**：本技能假设 LaTeX 环境已在您的系统上配置完成。

**Windows**：MiKTeX 或 TeX Live 已安装并添加到 PATH
**macOS/Linux**：TeX Live 已安装

必需工具：`pdflatex`、`xelatex`、`latexmk`、`biber`、`chktex`

## 在 Claude Code 中使用技能

本技能设计用于 Claude Code 等 AI 助手。只需在对话中提及相关触发词，助手就会激活相应模块。

### 使用示例

**编译论文**：
```
请使用 xelatex 和 bibtex 编译我的 LaTeX 论文 main.tex
```

**检查格式**：
```
能帮我检查论文格式是否符合 IEEE 会议投稿要求吗？
```

**翻译成英文**：
```
将以下中文翻译为学术英文（深度学习领域）：
本文提出了一种基于Transformer的方法...
```

**去AI化润色**：
```
请降低引言部分的 AI 写作痕迹
```

## 模块化设计

技能采用模块化设计，每个模块可独立调用：

| 模块 | 触发词 | 功能 |
|------|--------|------|
| Compile | compile, 编译, build | LaTeX 编译 |
| Format Check | format, chktex, 格式检查 | 格式检查 |
| Grammar Analysis | grammar, 语法, proofread | 语法分析 |
| Sentence Decomposition | long sentence, 长句 | 长句分解 |
| Expression | academic tone, 学术表达 | 表达优化 |
| Translation | translate, 翻译, 中译英 | 中英翻译 |
| Bibliography | bib, 参考文献 | 文献检查 |

## 编译模块

### 工具配置（匹配 VS Code LaTeX Workshop）

| 工具 | 命令 | 参数 |
|------|------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

### 编译配置

| 配置 | 步骤 |
|------|------|
| XeLaTeX | xelatex |
| PDFLaTeX | pdflatex |
| LaTeXmk | latexmk |
| xelatex -> bibtex -> xelatex*2 | xelatex → bibtex → xelatex → xelatex |
| xelatex -> biber -> xelatex*2 | xelatex → biber → xelatex → xelatex |
| pdflatex -> bibtex -> pdflatex*2 | pdflatex → bibtex → pdflatex → pdflatex |
| pdflatex -> biber -> pdflatex*2 | pdflatex → biber → pdflatex → pdflatex |

### 在 Claude Code 中使用

只需向助手提出具体的编译需求：

**基本编译**：
```
使用 xelatex 编译 main.tex
```

**带参考文献**（推荐用于论文）：
```
使用 xelatex 和 bibtex 工作流编译 main.tex
```

**指定输出目录**：
```
使用 latexmk 编译 main.tex 并输出到 build 目录
```

**清理辅助文件**：
```
清理 main.tex 的辅助文件
```

助手会根据您的请求执行相应的编译命令。

## 格式检查模块

### 在 Claude Code 中使用

向助手请求检查论文格式：

```
检查 main.tex 的格式
```

```
以严格模式检查 main.tex 格式，用于 IEEE 投稿
```

助手会分析您的论文并提供格式建议。

## 语法分析模块

基于 LLM 的语法检查，重点关注：
- 主谓一致
- 冠词使用 (a/an/the)
- 时态一致性
- 中式英语检测

### 在 Claude Code 中使用

向助手请求语法检查：

```
检查引言部分的语法
```

```
润色方法部分并修正中式英语错误
```

## 翻译模块

### 支持领域

| 领域 | 关键词 |
|------|--------|
| 深度学习 | 神经网络、注意力机制、损失函数 |
| 时间序列 | 时序预测、ARIMA、滑动窗口 |
| 工业控制 | PID 控制、故障检测、SCADA |

### 翻译流程

1. **术语确认** - 识别专业术语并确认翻译
2. **结构分析** - 分析段落结构，确定时态
3. **逐句翻译** - 带注释的翻译
4. **中式英语检查** - 检测并修正常见错误
5. **学术润色** - 最终审查

### 使用示例

**基本翻译请求**：
```
请将以下中文翻译为学术英文（深度学习领域）：
本文提出了一种基于Transformer的时间序列预测方法...
```

**指定期刊格式**：
```
请翻译以下内容，目标期刊为IEEE Transactions格式：
实验结果表明，我们的方法在多个数据集上取得了最优性能...
```

## 参考文献模块

### 在 Claude Code 中使用

向助手请求验证参考文献：

```
验证 references.bib 的格式错误
```

```
检查 references.bib 与 main.tex 的未使用条目
```

助手会检查：
- 必填字段完整性
- 重复条目
- 未使用条目
- 引用格式一致性

## 参考文件

- `references/TERMINOLOGY.md`：领域术语表（深度学习、时间序列、工业控制）
- `references/TRANSLATION_GUIDE.md`：翻译原则、中式英语修正、各章节指南
- `references/STYLE_GUIDE.md`：学术写作规范
- `references/COMMON_ERRORS.md`：常见错误
- `references/VENUES.md`：期刊会议要求

## 下一步

- [编译配置指南](/zh/guides/compilation)
- [格式检查指南](/zh/guides/format-checking)
- [参考文献指南](/zh/guides/bibliography)
