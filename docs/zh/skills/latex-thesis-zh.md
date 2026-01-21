# 中文学位论文 (latex-thesis-zh)

中文学位论文（博士/硕士）LaTeX 写作助手。

## 概述

`latex-thesis-zh` 技能专为中文学位论文设计，采用模块化架构，支持独立调用各功能模块。完整审查或多文件场景建议先执行结构映射。

### 触发词

| 模块 | 触发词 |
|------|--------|
| 编译 | `compile`, `编译`, `xelatex` |
| 结构映射 | `structure`, `结构`, `映射` |
| 国标格式检查 | `format`, `格式`, `国标`, `GB/T` |
| 学术表达 | `expression`, `表达`, `润色` |
| 长难句分析 | `long sentence`, `长句`, `拆解` |
| 参考文献 | `bib`, `bibliography`, `参考文献` |
| 模板检测 | `template`, `模板`, `thuthesis` |
| 去AI化编辑 | `deai`, `去AI化`, `人性化`, `降低AI痕迹` |

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

## 模块说明

### 编译模块

以 XeLaTeX 为主要编译器，适合中文文档。

**工具配置**（对齐 VS Code LaTeX Workshop）：

| 工具 | 命令 | 参数 |
|------|------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| lualatex | `lualatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -xelatex` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**编译配置**：

| 配置 | 步骤 | 适用场景 |
|------|------|----------|
| XeLaTeX | xelatex | 中文快速编译（推荐）|
| LuaLaTeX | lualatex | 复杂字体需求 |
| LaTeXmk | latexmk -xelatex | 自动处理依赖 |
| xelatex-bibtex | xelatex → bibtex → xelatex×2 | 中文 + BibTeX |
| xelatex-biber | xelatex → biber → xelatex×2 | 中文 + Biber（推荐）|
| lualatex-bibtex | lualatex → bibtex → lualatex×2 | LuaLaTeX + BibTeX |
| lualatex-biber | lualatex → biber → lualatex×2 | LuaLaTeX + Biber |

**使用示例**：

```bash
# 快速编译
python scripts/compile.py thesis.tex --recipe xelatex

# 完整编译（推荐）
python scripts/compile.py thesis.tex --recipe xelatex-biber

# 清理辅助文件
python scripts/compile.py thesis.tex --clean
```

### 结构映射模块

分析多文件论文结构。**完整审查或多文件场景建议首先执行**。

```bash
python scripts/map_structure.py thesis.tex
```

**论文结构要求**：

| 部分 | 必需内容 |
|------|----------|
| 前置部分 | 封面、声明、摘要（中英）、目录、符号表 |
| 正文部分 | 绪论、相关工作、核心章节、结论 |
| 后置部分 | 参考文献、致谢、发表论文列表 |

### 国标格式检查模块

检查 GB/T 7714-2015 规范合规性。

```bash
python scripts/check_format.py thesis.tex
python scripts/check_format.py thesis.tex --strict
```

**检查项目**：
- 参考文献格式（biblatex-gb7714-2015）
- 图表标题格式（图下表上）
- 公式编号格式
- 各级标题样式

### 学术表达模块

检测口语化表达，提供学术化建议。

**口语 → 学术转换示例**：

| ❌ 口语化 | ✅ 学术化 |
|----------|----------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |

**禁用主观词汇**：显然、毫无疑问、众所周知、不言而喻

### 长难句分析模块

触发条件：句子 >60 字 或 >3 个从句

输出包含：主干提取、修饰成分分析、改写建议

### 参考文献模块

```bash
python scripts/verify_bib.py refs.bib
python scripts/verify_bib.py refs.bib --standard gb7714
```

### 模板检测模块

```bash
python scripts/detect_template.py thesis.tex
```

**支持的模板**：

| 模板 | 学校 |
|------|------|
| thuthesis | 清华大学 |
| pkuthss | 北京大学 |
| ustcthesis | 中国科学技术大学 |
| fduthesis | 复旦大学 |
| ctexbook | 通用 |

### 去AI化编辑模块

降低 AI 生成文本痕迹，同时保持 LaTeX 语法完整性和技术准确性。

**输入要求**：
1. **源码类型**（必填）：LaTeX / Typst
2. **章节**（必填）：摘要 / 引言 / 相关工作 / 方法 / 实验 / 结果 / 讨论 / 结论 / 其他
3. **源码片段**（必填）：直接粘贴（保留原缩进与换行）

**使用示例**：

**交互式编辑**（单章节）：
```bash
python scripts/deai_check.py thesis.tex --section introduction
```

**批量处理**（整章或全文）：
```bash
python scripts/deai_batch.py thesis.tex --chapter chapter3/introduction.tex
python scripts/deai_batch.py thesis.tex --all-sections
```

**AI 痕迹密度检测**：
```bash
python scripts/deai_check.py thesis.tex --analyze
```

**工作流程**：
1. **语法结构识别**（完整保留 LaTeX/Typst 构造）：
   - 命令：`\command{...}`、`\command[...]{}`  
   - 引用：`\cite{}`、`\ref{}`、`\label{}`、`\eqref{}`、`\autoref{}`  
   - 环境：`\begin{...}...\end{...}`  
   - 数学：`$...$`、`\[...\]`、equation/align 环境  
   - 自定义宏（默认不改）
2. **AI 痕迹检测**：
   - 空话口号："重要意义"、"显著提升"、"全面系统"、"有效解决"
   - 过度确定："显而易见"、"必然"、"完全"、"毫无疑问"
   - 机械排比：无实质内容的三段式并列
   - 模板表达："近年来"、"越来越多的"、"发挥重要作用"
3. **文本改写**（仅改可见文本）：
   - 拆分长句（>50 字）
   - 调整词序以符合自然表达
   - 用具体主张替换空泛表述
   - 删除冗余短语
   - 补充必要主语（不引入新事实）
4. **输出生成**：
   - A. 改写后源码（最小侵入式修改）
   - B. 变更摘要（3-10 条要点）
   - C. 待补证标记（需要证据支撑的断言）

**硬性约束**：
- **绝不修改**：`\cite{}`、`\ref{}`、`\label{}`、公式环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号、文献 key
- **仅修改**：普通段落文字、章节标题内的中文表达、图表标题

**输出格式**：
```latex
% ============================================================
% 去AI化编辑（第23行 - 引言）
% ============================================================
% 原文：本文提出的方法取得了显著的性能提升。
% 修改后：本文提出的方法在实验中表现出性能提升。
%
% 改动说明：
% 1. 删除空话："显著" → 删除
% 2. 保留原有主张，避免新增具体指标或对比基准
%
% ⚠️ 【待补证：需要实验数据支撑，补充具体指标】
% ============================================================

\section{引言}
本文提出的方法在实验中表现出性能提升...
```

**分章节准则**：

| 章节 | 重点 | 约束 |
|------|------|------|
| 摘要 | 目的/方法/关键结果（带数字）/结论 | 禁泛泛贡献 |
| 引言 | 重要性→空白→贡献（可核查） | 克制措辞 |
| 相关工作 | 按路线分组，差异点具体化 | 具体对比 |
| 方法 | 可复现优先（流程、参数、指标定义） | 实现细节 |
| 结果 | 仅报告事实与数值 | 不解释原因 |
| 讨论 | 讲机制、边界、失败、局限 | 批判性分析 |
| 结论 | 回答研究问题，不引入新实验 | 可执行未来工作 |

**参考文档**：

详见 `references/DEAI_GUIDE.md`，包含：
- 常见 AI 痕迹模式及消除方法
- 分章节写作准则
- 输出格式规范
- 快速参考替换表

## 工作流建议

### 日常写作

```bash
python scripts/compile.py thesis.tex --recipe xelatex
```

### 章节完成时

```bash
python scripts/compile.py thesis.tex --recipe xelatex-biber
python scripts/verify_bib.py refs.bib --standard gb7714
```

### 最终提交前

```bash
# 1. 结构映射
python scripts/map_structure.py thesis.tex

# 2. 去AI化分析
python scripts/deai_check.py thesis.tex --analyze

# 3. 完整编译
python scripts/compile.py thesis.tex --recipe xelatex-biber

# 4. 国标检查
python scripts/verify_bib.py refs.bib --standard gb7714

# 5. 术语一致性
python scripts/check_consistency.py chapters/

# 6. 清理
python scripts/compile.py thesis.tex --clean
```

## 常见问题

### 中文字体缺失

```latex
\setCJKmainfont{SimSun}  % Windows
\setCJKmainfont{STSong}  % macOS
```

### 参考文献格式不正确

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
```

## 下一步

- [编译配置指南](/zh/guides/compilation)
- [参考文献管理](/zh/guides/bibliography)
- [GB/T 7714 标准](/zh/references/gb-standard)
- [去AI化写作指南](/zh/references/deai-guide)
