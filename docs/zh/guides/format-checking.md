# 格式检查指南

Academic Writing Skills 中 LaTeX 格式检查的完整指南。

## 概述

格式检查确保您的 LaTeX 代码遵循最佳实践和特定场所要求。

## 检查级别

### 快速检查 (--quick)

**执行时间**：1-2 秒

**检查内容**：
- 引用间距
- 基本标点错误
- 章节结构
- 常见 LaTeX 错误

```bash
python check_format.py paper.tex --quick
```

### 标准检查（默认）

**执行时间**：5-10 秒

**检查内容**：
- 所有快速检查项
- ChkTeX 集成
- 引用一致性
- 标签规范
- 图表标题
- 交叉引用验证

```bash
python check_format.py paper.tex
```

### 深度检查 (--deep)

**执行时间**：30-60 秒

**检查内容**：
- 所有标准检查项
- 样式指南合规（IEEE/ACM/Springer）
- 高级语法模式
- 一致性检查
- 术语验证

```bash
python check_format.py paper.tex --deep --venue ieee
```

## 常见问题

### 1. 引用间距

```latex
% 错误
word\cite{key}

% 正确
word \cite{key}
```

### 2. 数学模式中的标点

```latex
% 错误
The equation is $x = 1$ .

% 正确
The equation is $x = 1$.
```

### 3. 标签规范

```latex
% 错误
\label{1}
\label{my_figure}

% 正确
\label{sec:introduction}
\label{fig:architecture}
\label{tab:results}
\label{eq:loss_function}
```

**规范**：
- 章节：`sec:描述`
- 图片：`fig:描述`
- 表格：`tab:描述`
- 公式：`eq:描述`

### 4. 章节标题大小写

```latex
% IEEE 样式
\section{Introduction and Background}  % 标题式大写

% ACM 样式
\section{Introduction and background}  % 句子式大写
```

## 场所特定检查

### IEEE 样式

```bash
python check_format.py paper.tex --venue ieee
```

**规则**：
- 章节标题：标题式大写
- 图片引用：文中用 "Fig."，标题用 "Figure"
- 表格标题：大写 "TABLE"

### ACM 样式

```bash
python check_format.py paper.tex --venue acm
```

**规则**：
- 章节标题：句子式大写
- 图片引用：统一用 "Figure"
- 表格标题：正常 "Table"

### Springer 样式

```bash
python check_format.py paper.tex --venue springer
```

## ChkTeX 集成

### 常见 ChkTeX 警告

| 代码 | 警告 | 修复 |
|------|------|------|
| 1 | 命令以空格结束 | 添加 `{}` 或 `\` |
| 8 | 破折号长度错误 | 使用 `--` 或 `---` |
| 11 | 使用 `\dots` 代替 `...` | 替换为 `\dots` |
| 13 | 句间间距 | 缩写后使用 `\ ` |

### 手动运行 ChkTeX

```bash
chktex paper.tex
chktex -q paper.tex  # 安静模式
```

## 自动修复

```bash
python check_format.py paper.tex --fix
```

**可自动修复**：
- 引用间距
- 数学模式标点
- 命令间距
- 省略号用法

**需手动审查**：
- 标签命名
- 章节标题内容
- 未定义引用

## 输出格式

### 文本输出（默认）

```bash
python check_format.py paper.tex
```

### JSON 输出

```bash
python check_format.py paper.tex --output json
```

## 最佳实践

### 1. 经常检查

写作过程中频繁运行快速检查：
```bash
python check_format.py paper.tex --quick
```

### 2. 使用适当的检查级别

- **草稿阶段**：快速检查
- **审阅阶段**：标准检查
- **提交前**：深度检查 + 场所标志

### 3. 逐步修复问题

不要积累问题：
```bash
python check_format.py paper.tex --fix
```

### 4. 使用场所特定检查

最终检查时指定场所：
```bash
python check_format.py paper.tex --deep --venue ieee
```

## 故障排除

### ChkTeX 未找到

**解决**：安装 ChkTeX
```bash
# macOS
brew install chktex

# Ubuntu/Debian
sudo apt-get install chktex

# Windows (MiKTeX)
mpm --install=chktex
```

### 误报

**解决**：抑制特定警告
```bash
python check_format.py paper.tex --chktex-ignore 11
```

## 下一步

- [编译配置指南](/zh/guides/compilation)
- [参考文献指南](/zh/guides/bibliography)
