# 中文学位论文 (latex-thesis-zh)

中文学位论文（博士/硕士）LaTeX 写作助手。

## 概述

`latex-thesis-zh` 技能专为中文学位论文设计，采用模块化架构，支持独立调用各功能模块。

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
| 去AI化编辑 | `deai`, `去AI化`, `人性化` |

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

分析多文件论文结构，**建议首先执行**。

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

**功能特性**：

- **AI 痕迹检测**：基于模式匹配的智能检测
- **分章节分析**：生成章节密度评分
- **批量处理**：支持整章或全文处理
- **语法保真编辑**：保留 LaTeX 命令、数学公式、引用

**使用方法**：

**交互式分析**（单章节）：
```bash
python scripts/deai_check.py thesis.tex --section introduction
```

**完整文档分析**：
```bash
python scripts/deai_check.py thesis.tex --analyze
```

**批量处理**（整章或全文）：
```bash
python scripts/deai_batch.py thesis.tex --all-sections
python scripts/deai_batch.py thesis.tex --chapter chapter3/introduction.tex --output polished/
```

**章节密度评分**：
```bash
python scripts/deai_check.py thesis.tex --score
```

**输出示例**：

```
================================================================================
中文博士论文去AI化写作痕迹分析报告
================================================================================
文件: thesis.tex
总行数: 1200

--------------------------------------------------------------------------------
各章节 AI 痕迹密度
--------------------------------------------------------------------------------

[高] 绪论
  AI 痕迹密度: 12.3%
  痕迹数量: 45 / 366 行

[中] 方法
  AI 痕迹密度: 5.8%
  痕迹数量: 28 / 482 行
```

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
