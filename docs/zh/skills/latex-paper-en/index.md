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
- **去AI化分析**降低 AI 生成文本痕迹

## 环境要求

> **注意**：本技能假设 LaTeX 环境已在您的系统上配置完成。

**Windows**：MiKTeX 或 TeX Live 已安装并添加到 PATH
**macOS/Linux**：TeX Live 已安装

必需工具：`pdflatex`、`xelatex`、`latexmk`、`biber`、`chktex`

## 在 Claude Code 中使用技能

本技能设计用于 Claude Code 等 AI 助手。只需在对话中提及相关触发词，助手就会激活相应模块。

### 参数约定

请求中请尽量包含：
- **主 `.tex` 路径**（执行脚本时必需）
- **目标范围**（章节/段落或全文）
- **模块选择**（编译/格式/语法/翻译等）

如信息缺失或含糊，助手会先确认，不会猜测路径或范围。

### 执行约束

- 仅在您明确要求时执行脚本/编译命令。
- 涉及清理（`--clean` / `--clean-all`）等破坏性操作前先确认。

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

## 输出协议

所有建议采用注释式 diff 格式，并包含固定字段：
- **严重级别**：Critical / Major / Minor
- **优先级**：P0 / P1 / P2

最小模板：
```latex
% <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
% 原文：...
% 修改后：...
% 理由：...
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理

- 缺少编译工具：安装 TeX Live/MiKTeX 并加入 PATH
- 缺少文件/脚本：确认工作目录与 `scripts/` 路径
- 编译失败：优先给出首个错误摘要并请求日志片段

## 模块化设计

技能采用模块化设计，每个模块可独立调用：

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
| 引用完整性 | ref, label, 引用检查 | 图表引用完整性验证 🆕 |
| De-AI Polishing | deai, 去AI化, humanize | 降低 AI 痕迹 |
| Title Optimization | title, 标题, title optimization | 标题生成与优化 🆕 |

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

## 长难句分析模块

当句子 >50 词或从句过多时，建议拆分以提升可读性。

### 在 Claude Code 中使用

```
拆解引言中超过 50 词的长句
```

```
简化第 3 节的复杂句子
```

## 学术表达模块

优化弱动词与口语化表达，提升学术语气。

### 在 Claude Code 中使用

```
提升摘要的学术语气
```

```
替换相关工作中的弱动词
```

## 逻辑衔接与方法论深度模块

确保段落间逻辑流畅，强化方法论的严谨性。

### AXES 模型（段落级逻辑衔接）

| 组成部分 | 说明 | 示例 |
|----------|------|------|
| **A**ssertion（主张） | 清晰的主题句，陈述核心观点 | "Attention mechanisms improve sequence modeling." |
| **X**ample（例证） | 支撑主张的具体证据或数据 | "In our experiments, attention achieved 95% accuracy." |
| **E**xplanation（解释） | 分析证据为何支撑主张 | "This improvement stems from the ability to capture long-range dependencies." |
| **S**ignificance（意义） | 与更广泛论点或下一段的联系 | "This finding motivates our proposed architecture." |

### 过渡信号词

| 关系类型 | 英文信号词 |
|----------|------------|
| 递进 | furthermore, moreover, in addition |
| 转折 | however, nevertheless, in contrast |
| 因果 | therefore, consequently, as a result |
| 顺序 | first, subsequently, finally |
| 举例 | for instance, specifically, in particular |

### 方法论深度检查清单

- 每个主张都有证据支撑（数据、引用或逻辑推理）
- 方法选择有充分理由（为何选此方法而非其他？）
- 明确承认研究局限性
- 清晰陈述前提假设
- 可复现性细节充分（参数、数据集、评估指标）

### 常见问题

| 问题类型 | 表现 | 修正方法 |
|----------|------|----------|
| 逻辑断层 | 段落间缺乏衔接 | 添加过渡句说明段落关系 |
| 无据主张 | 断言缺乏证据支撑 | 补充引用、数据或推理 |
| 方法论浅薄 | "We use X" 但无理由 | 解释为何 X 适合本问题 |
| 隐含假设 | 前提条件未明示 | 显式陈述假设条件 |

### 在 Claude Code 中使用

```
检查引言部分的逻辑衔接
```

```
分析方法部分的方法论深度
```

```
在第 3 节段落之间添加过渡信号词
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

```bash
# 在线验证（CrossRef + Semantic Scholar）
python scripts/verify_bib.py references.bib --online
python scripts/verify_bib.py references.bib --online --email you@example.com
```

## 去AI化编辑模块

在保留 LaTeX 语法与技术准确性的前提下，降低 AI 写作痕迹。

### 在 Claude Code 中使用

```
去AI化引言部分并保持事实不变
```

```
分析全文 AI 痕迹密度并给出重点修订段落
```

## 参考文件

- `references/TERMINOLOGY.md`：领域术语表（深度学习、时间序列、工业控制）
- `references/TRANSLATION_GUIDE.md`：翻译原则、中式英语修正、各章节指南
- `references/STYLE_GUIDE.md`：学术写作规范
- `references/COMMON_ERRORS.md`：常见错误
- `references/VENUES.md`：期刊会议要求
- `references/DEAI_GUIDE.md`：去AI化写作指南与模式库

## 推荐工作流

### 投稿前快速检查
1. 格式检查（严格模式）
2. 语法分析（摘要 + 引言）
3. 参考文献验证

### 完整质量审查
1. 格式检查 → 修复关键问题
2. 语法分析
3. 去AI化编辑
4. 长难句拆解
5. 学术表达优化
6. 参考文献验证

### 翻译流程
1. 术语确认
2. 带注释翻译
3. 中式英语检查
4. 学术润色
