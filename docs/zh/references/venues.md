# 期刊会议

主要学术期刊和会议的格式要求。

## IEEE

### 通用规则

- **章节标题**：标题式大写（每个主要词首字母大写）
- **图片引用**：文中用 "Fig."，标题用 "Figure"
- **表格标题**：大写 "TABLE"
- **引用格式**：数字 [1], [2], [3]

### 示例

```latex
\section{Introduction and Background}

As shown in Fig.~1, the proposed method...

\begin{table}[t]
  \caption{TABLE I: Experimental Results}
  ...
\end{table}
```

### 常见期刊

| 期刊 | 缩写 | 领域 |
|------|------|------|
| IEEE Transactions on Pattern Analysis and Machine Intelligence | TPAMI | 计算机视觉、模式识别 |
| IEEE Transactions on Neural Networks and Learning Systems | TNNLS | 神经网络、机器学习 |
| IEEE Transactions on Knowledge and Data Engineering | TKDE | 数据挖掘、知识工程 |

### 常见会议

| 会议 | 领域 | 页数限制 |
|------|------|----------|
| CVPR | 计算机视觉 | 8 页 |
| ICCV | 计算机视觉 | 8 页 |
| ICRA | 机器人 | 6-8 页 |

## ACM

### 通用规则

- **章节标题**：句子式大写（仅首词首字母大写）
- **图片引用**：统一用 "Figure"
- **表格标题**：正常 "Table"
- **引用格式**：数字 [1] 或作者-年份

### 示例

```latex
\section{Introduction and background}

As shown in Figure~1, the proposed method...

\begin{table}[t]
  \caption{Table 1: Experimental results}
  ...
\end{table}
```

### 常见会议

| 会议 | 领域 | 页数限制 |
|------|------|----------|
| SIGCHI | 人机交互 | 10 页 |
| SIGMOD | 数据库 | 12 页 |
| KDD | 数据挖掘 | 9 页 |
| WWW | 万维网 | 10 页 |

## Springer

### 通用规则

- **章节标题**：句子式或标题式（视具体期刊）
- **图片引用**：统一用 "Fig."
- **表格标题**：正常 "Table"
- **引用格式**：数字 [1] 或作者-年份

### LNCS 格式

```latex
\documentclass[runningheads]{llncs}

% 页数限制通常为 12-15 页
```

### 常见期刊

| 期刊 | 领域 |
|------|------|
| Machine Learning | 机器学习 |
| Data Mining and Knowledge Discovery | 数据挖掘 |
| Neural Computing and Applications | 神经计算 |

## NeurIPS / ICML / ICLR

### 通用规则

- **页数限制**：8 页正文 + 参考文献
- **格式**：双栏
- **匿名审稿**：提交时隐藏作者信息

### NeurIPS

```latex
\documentclass{article}
\usepackage{neurips_2024}

% 8 页正文，参考文献不限
```

### ICML

```latex
\documentclass{article}
\usepackage{icml2024}

% 8 页正文，参考文献不限
```

### ICLR

```latex
\documentclass{article}
\usepackage{iclr2024_conference}

% 8 页正文，参考文献不限
```

## AAAI / IJCAI

### AAAI

- **页数限制**：7 页正文 + 1 页参考文献
- **格式**：双栏

```latex
\documentclass[letterpaper]{article}
\usepackage{aaai24}
```

### IJCAI

- **页数限制**：7 页正文 + 1 页参考文献
- **格式**：双栏

```latex
\documentclass{article}
\usepackage{ijcai24}
```

## 中文期刊

### 计算机学报

- **格式**：GB/T 7714-2015
- **语言**：中文为主，摘要中英双语

### 软件学报

- **格式**：GB/T 7714-2015
- **语言**：中文为主

### 自动化学报

- **格式**：GB/T 7714-2015
- **语言**：中文为主

## 格式检查

使用 Academic Writing Skills 检查特定场所格式：

```bash
# IEEE 格式检查
python check_format.py paper.tex --venue ieee

# ACM 格式检查
python check_format.py paper.tex --venue acm

# Springer 格式检查
python check_format.py paper.tex --venue springer
```

## 提交清单

### 提交前检查

- [ ] 页数符合要求
- [ ] 格式符合模板
- [ ] 图片清晰可读
- [ ] 参考文献格式正确
- [ ] 匿名要求（如适用）
- [ ] 补充材料（如适用）

### 常见问题

1. **页数超限**：精简内容或移至附录
2. **格式不符**：使用官方模板
3. **图片模糊**：使用矢量图（PDF/EPS）
4. **引用缺失**：检查所有 `\cite` 命令

## 下一步

- [常见错误](/zh/references/common-errors)
- [写作规范](/zh/references/style-guide)
