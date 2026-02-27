# 论文审查 (paper-audit)

面向 LaTeX、Typst 和 PDF 文档的自动化多模式论文审查工具。

## 概述

`paper-audit` 技能为多种格式（`.tex`、`.typ`、`.pdf`）的学术论文提供全面的自动化审查。它协调多个专用检查器，生成包含严重程度分级问题和质量评分的结构化报告。

### 主要功能

- **多格式支持**：LaTeX（`.tex`）、Typst（`.typ`）和 PDF（`.pdf`）输入
- **三种审查模式**：self-check（全面）、review（同行评审模拟）、gate（投稿就绪门控）
- **PDF 视觉排版检查**：页边距溢出、块重叠、字体不一致、低分辨率图片、空白页检测
- **引用完整性检查**：未定义引用、未引用标签、缺少 caption、前向引用、编号间隙
- **ScholarEval 评估**：8 维度质量评分（1-10 分制），给出投稿可读性标签
- **在线文献验证**：CrossRef + Semantic Scholar API 验证（无需 API 密钥）
- **NeurIPS 对齐评分**：Quality/Clarity/Significance/Originality 维度（1-6 分制）

## 审查模式

| 模式 | 描述 | 包含检查 |
|------|------|----------|
| `self-check` | 全面修改前审查 | 所有模块 |
| `review` | 同行评审模拟 | grammar, logic, figures, references, visual |
| `gate` | 投稿就绪门控 | format, bib, references, visual |

## 在 Claude Code 中使用

在对话中提及相关触发词：

```
投稿前帮我全面审查这篇论文
```

```
用 ScholarEval 评估我的论文质量
```

```
检查我的 PDF 排版是否有问题
```

### 参数约定

- **文件路径**（必填）：`.tex`、`.typ` 或 `.pdf`
- **模式**（可选）：`self-check`（默认）、`review`、`gate`
- **标志**（可选）：`--online` 开启在线文献验证，`--scholar-eval` 开启 ScholarEval

### 脚本命令行

```bash
# 基础审查（自动检测模式）
python scripts/audit.py paper.tex --mode self-check

# 带在线文献验证
python scripts/audit.py paper.tex --mode review --online

# 带 ScholarEval 8 维度评估
python scripts/audit.py paper.tex --mode self-check --scholar-eval

# PDF 审查（视觉 + 提取文本检查）
python scripts/audit.py paper.pdf --mode gate

# 全功能审查
python scripts/audit.py paper.tex --mode self-check --online --scholar-eval --email you@example.com
```

## 检查模块

| 模块 | 触发词 | 支持格式 | 描述 |
|------|--------|----------|------|
| `grammar` | grammar, proofread | tex, typ, pdf | 语法分析 |
| `sentences` | long sentence, 长句 | tex, typ, pdf | 长句检测 |
| `logic` | logic, coherence, 逻辑 | tex, typ, pdf | 段落衔接（AXES 模型）|
| `format` | format, lint | tex, typ | 格式检查 |
| `figures` | figures, images | tex, typ | 图片质量检查 |
| `references` | ref, label, 引用 | tex, typ | 引用完整性 🆕 |
| `visual` | visual, layout | **仅 pdf** | PDF 视觉排版 🆕 |
| `bib` | bib, bibliography | tex, typ | 文献验证 |
| `deai` | deai, 去AI化 | tex, typ, pdf | 去AI化痕迹检测 |

## 引用完整性模块

检查图表引用的完整性。

### 检查项目

| 检查 | 描述 | 严重级别 |
|------|------|----------|
| 未定义引用 | `\ref{fig:x}` 但无 `\label{fig:x}` | Critical |
| 未引用的标签 | `\label{fig:x}` 从未被引用 | Minor |
| 缺少 caption | 图表环境无 `\caption` | Major |
| 前向引用 | `\ref` 出现在 `\label` 之前 | Minor |
| 编号间隙 | `fig:1`, `fig:3` 缺少 `fig:2` | Minor |

## PDF 视觉排版模块

分析投稿就绪 PDF 的排版问题。

### 检查项目

| 检查 | 方法 | 严重级别 |
|------|------|----------|
| 页边距溢出 | 文本块 bbox vs 页面边距（默认 72pt）| Major |
| 块重叠 | 边界框交集面积 > 100 sq pt | Critical |
| 字体不一致 | 正文字体 >2 种（9-13pt）| Minor |
| 低分辨率图片 | 有效 DPI < 150 | Major |
| 空白页 | 无文本或图片的页面 | Minor |

## ScholarEval 评估模块

基于 ScholarEval（arXiv:2510.16234）的 8 维度学术质量评分。

### 评分维度

| 维度 | 权重 | 来源 | 描述 |
|------|------|------|------|
| Soundness | 20% | 脚本 | 逻辑严谨性、主张-证据一致性 |
| Clarity | 15% | 脚本 | 语法、句子质量、格式 |
| Presentation | 10% | 脚本 | 图表、视觉排版、引用 |
| Novelty | 15% | llm | 原创性与贡献 |
| Significance | 15% | llm | 对领域的影响 |
| Reproducibility | 10% | 混合 | 实验描述完整性 |
| Ethics | 5% | llm | 伦理考量 |
| Overall | 10% | 计算 | 加权综合 |

### 投稿可读性标签

| 分数 | 标签 |
|------|------|
| 9.0+ | Strong Accept — 适合顶级会议 |
| 8.0+ | Accept — 可直接投稿 |
| 7.0+ | Ready with minor revisions — 小修后投稿 |
| 6.0+ | Major revisions needed — 需大幅修改 |
| 5.0+ | Significant rework required — 需重写 |
| <5.0 | Not ready — 尚未达到投稿标准 |

## 在线文献验证

通过 CrossRef 和 Semantic Scholar 验证引文元数据。

### 特性

- **DOI 验证**：验证 DOI 有效性，交叉检查年份/期刊字段
- **标题搜索**：无 DOI 时通过标题查找论文
- **DOI 建议**：为缺少 DOI 的条目推荐 DOI
- **速率限制**：内置礼貌速率限制（请求间隔 0.5 秒）
- **无需 API 密钥**：使用 CrossRef 和 Semantic Scholar 公共 API

### 使用方式

在 audit 命令中添加 `--online` 标志：

```bash
# 开启在线验证
python scripts/audit.py paper.tex --mode self-check --online

# 使用礼貌 email 加快 CrossRef 速率限制
python scripts/audit.py paper.tex --online --email you@example.com
```

## 推荐工作流

### 投稿前快速检查

```bash
python scripts/audit.py paper.tex --mode gate --online --email you@example.com
```

### 全面自查

```bash
python scripts/audit.py paper.tex --mode self-check --scholar-eval
```

### PDF 摄像就绪检查

```bash
python scripts/audit.py paper.pdf --mode gate
```

## 参考文件

- `resources/references/SCHOLAR_EVAL_GUIDE.md`：ScholarEval 详细评分标准
