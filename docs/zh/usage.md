# 使用指南

本指南详细介绍 Academic Writing Skills 的完整功能。

## 概述

Academic Writing Skills 提供三个主要技能：

| 技能 | 用途 | 主要功能 |
|------|------|----------|
| `latex-paper-en` | 英文学术论文 | 编译、格式检查、语法分析、学术翻译 |
| `latex-thesis-zh` | 中文学位论文 | 编译、GB/T 7714 检查、模板支持 |
| `typst-paper` | Typst 学术论文 | 编译、格式检查、语法分析、学术翻译 |

## 模块化设计

每个技能都采用模块化设计，您可以独立使用任何模块，无需按顺序执行。

## 参数约定

为保证执行可靠，请在请求中包含：
- **主文件路径**（`.tex` / `.typ`）
- **目标范围**（章节/段落或全文）
- **模块选择**（编译/格式/语法/模板等）

如信息缺失或含糊，助手会先确认，不会猜测路径或范围。

### latex-paper-en 模块

| 模块 | 触发词 | 功能 |
|------|--------|------|
| Compile | compile, 编译, build | LaTeX 编译 |
| Format Check | format, chktex, 格式检查 | 格式检查 |
| Grammar Analysis | grammar, 语法, proofread | 语法分析 |
| Sentence Decomposition | long sentence, 长句 | 长句分解 |
| Expression | academic tone, 学术表达 | 表达优化 |
| Logic & Methodology | logic, coherence, 逻辑, methodology, 论证 | 逻辑衔接与方法论深度 |
| Translation | translate, 翻译, 中译英 | 中英翻译 |
| Bibliography | bib, 参考文献 | 文献检查 |
| De-AI Polishing | deai, 去AI化, humanize | 降低 AI 痕迹 |
| Title Optimization | title, 标题, title optimization | 标题生成与优化 |
| Experiment Analysis | experiment, 实验分析, 数据分析 | 实验段落改写与生成 |

### latex-thesis-zh 模块

| 模块 | 触发词 | 功能 |
|------|--------|------|
| 编译 | compile, 编译, xelatex | LaTeX 编译 |
| 结构映射 | structure, 结构, 映射 | 论文结构分析 |
| 国标格式检查 | format, 格式, 国标, GB/T | GB/T 7714 合规 |
| 学术表达 | expression, 表达, 润色 | 学术表达优化 |
| 逻辑衔接与方法论 | logic, coherence, 逻辑, 衔接, methodology, 方法论 | 逻辑衔接与方法论深度 |
| 长难句分析 | long sentence, 长句, 拆解 | 长难句分析 |
| 参考文献 | bib, bibliography, 参考文献 | 文献检查 |
| 模板检测 | template, 模板, thuthesis | 模板检测 |
| 去AI化 | deai, 去AI化, 降低AI痕迹 | 降低 AI 痕迹 |
| 标题优化 | title, 标题, 标题优化, 生成标题 | 标题生成与优化 |
| 实验分析 | experiment, 实验分析, 数据分析 | 实验段落改写与生成 |

### typst-paper 模块

| 模块 | 触发词 | 功能 |
|------|--------|------|
| 编译 | compile, 编译, typst compile | Typst 编译 |
| 格式检查 | format, lint, 格式检查 | 格式检查 |
| 语法分析 | grammar, proofread, 语法 | 语法分析 |
| 长难句 | long sentence, 长句, simplify | 句子分解 |
| 表达 | academic tone, 学术表达 | 表达优化 |
| 逻辑衔接与方法论 | logic, coherence, 逻辑, 衔接, methodology, 方法论 | 逻辑衔接与方法论深度 |
| 翻译 | translate, 翻译, 中译英 | 中英翻译 |
| 参考文献 | bib, bibliography, 参考文献 | 文献检查 |
| 去AI化 | deai, 去AI化, humanize | 降低 AI 痕迹 |
| 模板 | template, IEEE, ACM, 模板 | 模板配置 |
| 标题优化 | title, 标题, title optimization | 标题生成与优化 |
| 实验分析 | experiment, 实验分析, 数据分析 | 实验段落改写与生成 |

## 安全与工具确认

为保护项目与系统安全，涉及工具调用或命令执行时遵循以下规则：

**高风险操作需明确确认**：
- 删除/移动文件或目录
- Git 破坏性操作（如 `git reset --hard`、`git push`）
- 系统配置或权限变更
- 数据库结构/数据批量变更
- 发送敏感数据的网络请求
- 全局安装/卸载或核心依赖更新

**输入约束**：
- 不执行来源不明或含糊的命令
- 需要文件路径时要求明确路径
- 不索要或保存密钥/密码等敏感信息
- 命令不明确时先澄清
- 优先最小、可回滚的操作

**执行约束**：
- 仅在您明确要求时执行脚本/编译命令
- 清理类操作（`--clean` / `--clean-all`）需先确认

**执行透明性**：
- 执行前说明具体命令
- 执行后说明改动位置与结果
- 失败时展示错误并给出安全的下一步

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

# 指定编译配置
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

## 模板检测模块（latex-thesis-zh）

检测学校模板并汇总关键要求：
```bash
python scripts/detect_template.py main.tex
```

## 推荐工作流

### 英文论文完整审查
1. 格式检查（严格）
2. 语法分析
3. 去AI化编辑
4. 长难句拆解
5. 学术表达优化
6. 实验分析逻辑改写（针对实验章节）
7. 参考文献验证

### 中文学位论文完整审查
1. 结构映射（优先）
2. 国标格式检查
3. 模板检测 + 关键要求核对
4. 去AI化编辑
5. 学术表达与长难句分析
6. 实验分析逻辑改写（针对实验章节）
7. 参考文献验证

### Typst 快速迭代
1. 编译或监视模式
2. 基础格式检查
3. 语法分析
4. 模板配置核对（如期刊要求）

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

**解决**：使用完整编译配置：
```bash
python scripts/compile.py main.tex --recipe xelatex-biber
```

## 下一步

- [英文论文核心模块](/zh/skills/latex-paper-en/)
- [中文论文指南](/zh/skills/latex-thesis-zh/)
- [Typst 论文模块](/zh/skills/typst-paper/)
