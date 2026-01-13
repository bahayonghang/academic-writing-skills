# 使用指南

本指南详细介绍 Academic Writing Skills 的完整功能。

## 概述

Academic Writing Skills 提供两个主要技能：

| 技能 | 用途 | 主要功能 |
|------|------|----------|
| `latex-paper-en` | 英文学术论文 | 编译、格式检查、语法分析、学术翻译 |
| `latex-thesis-zh` | 中文学位论文 | 编译、GB/T 7714 检查、模板支持 |

## 模块化设计

每个技能都采用模块化设计，您可以独立使用任何模块，无需按顺序执行。

### latex-paper-en 模块

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

### 可用工具

| 工具 | 命令 | 参数 |
|------|------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

### 编译配置

| 配置 | 步骤 | 适用场景 |
|------|------|----------|
| XeLaTeX | xelatex | Unicode/中文支持 |
| PDFLaTeX | pdflatex | 纯英文，最快 |
| LaTeXmk | latexmk | 自动依赖处理 |
| xelatex-bibtex | xelatex → bibtex → xelatex × 2 | 中文 + BibTeX |
| xelatex-biber | xelatex → biber → xelatex × 2 | 中文 + Biber |
| pdflatex-bibtex | pdflatex → bibtex → pdflatex × 2 | 英文 + BibTeX |
| pdflatex-biber | pdflatex → biber → pdflatex × 2 | 英文 + Biber |

### 使用示例

```bash
# 自动检测编译器
python scripts/compile.py main.tex

# 指定配方
python scripts/compile.py main.tex --recipe xelatex-biber

# 指定输出目录
python scripts/compile.py main.tex --recipe latexmk --outdir build

# 清理辅助文件
python scripts/compile.py main.tex --clean
python scripts/compile.py main.tex --clean-all  # 包括 PDF
```

## 格式检查模块

使用 ChkTeX 进行 LaTeX 代码检查。

```bash
# 基本检查
python scripts/check_format.py main.tex

# 严格模式
python scripts/check_format.py main.tex --strict
```

输出示例：
```
============================================================
LaTeX Format Check Report
============================================================
File: main.tex
Status: WARNING
Message: Found 3 issues

[SPACING] (2 issues)
  Line 42: Interword spacing (`\ ') should perhaps be used.
  Line 87: Intersentence spacing (`\@') should perhaps be used.

[PUNCTUATION] (1 issue)
  Line 120: Delete this space to maintain correct pagereferences.
============================================================
```

## 语法分析模块

基于 LLM 的语法检查，无需外部工具。

重点检查：
- 主谓一致
- 冠词使用 (a/an/the)
- 时态一致性
- 中式英语检测

输出格式：
```latex
% GRAMMAR (Line 23): Article missing
% Before: We propose method for time series forecasting.
% After: We propose a method for time series forecasting.
```

## 翻译模块

支持中文学术文本到英文的翻译。

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

```
用户：翻译以下内容到学术英文（深度学习领域）：
本文提出了一种基于 Transformer 的时间序列预测方法。

助手：
## 术语确认
| 中文 | English |
|------|---------|
| 时间序列预测 | time series forecasting |
| 基于...的 | ...-based |

## 翻译结果
We propose a Transformer-based approach for time series forecasting.

## 注释
- "本文提出" → "We propose" (标准学术表达)
- "基于...的方法" → "...-based approach" (复合形容词)
```

## 参考文献模块

验证 BibTeX 文件的完整性和格式。

```bash
# 基本验证
python scripts/verify_bib.py references.bib

# 与 tex 文件交叉检查
python scripts/verify_bib.py references.bib --tex main.tex

# GB/T 7714 标准检查
python scripts/verify_bib.py references.bib --standard gb7714
```

检查内容：
- 必需字段完整性
- 重复键检测
- 未使用条目
- 缺失引用

## 最佳实践

### 1. 选择正确的编译配置

```
英文论文（无中文）→ pdflatex 或 pdflatex-biber
包含中文/Unicode → xelatex 或 xelatex-biber
复杂依赖 → latexmk
```

### 2. 经常检查格式

```bash
# 开发时使用快速检查
python scripts/check_format.py paper.tex

# 提交前使用严格检查
python scripts/check_format.py paper.tex --strict
```

### 3. 翻译时确认术语

在翻译专业内容前，先确认关键术语的标准译法。

### 4. 保持参考文献整洁

定期运行参考文献验证，确保格式正确且无未使用条目。

## 故障排除

### 编译失败

**问题**：`! LaTeX Error: File 'xxx.sty' not found`

**解决**：
```bash
# TeX Live
tlmgr install <package>

# MiKTeX
mpm --install=<package>
```

### 中文显示异常

**问题**：中文显示为方框

**解决**：使用 XeLaTeX：
```bash
python scripts/compile.py main.tex --recipe xelatex
```

### 参考文献为空

**问题**：参考文献部分为空

**解决**：使用完整配方：
```bash
python scripts/compile.py main.tex --recipe xelatex-biber
```

## 下一步

- [编译配置详解](/zh/guides/compilation)
- [格式检查指南](/zh/guides/format-checking)
- [参考文献管理](/zh/guides/bibliography)
