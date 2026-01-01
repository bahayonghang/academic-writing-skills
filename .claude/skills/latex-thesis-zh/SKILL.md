---
name: latex-thesis-zh
description: |
  Chinese doctoral/master thesis LaTeX assistant.
  Provides: structure integrity checking, GB/T 7714 format validation,
  compilation (xelatex/lualatex via latexmk), Chinese academic expression standards,
  terminology consistency analysis.

  Use when:
  - Working with Chinese thesis projects (main.tex + chapter files)
  - User mentions "doctoral thesis", "master thesis", "dissertation", "graduation thesis"
  - User mentions Chinese: "博士论文", "硕士论文", "学位论文", "毕业论文"
  - User asks about university templates: thuthesis, pkuthss, ustcthesis, fduthesis
  - User needs GB/T 7714 bibliography format checking
  - User wants to compile Chinese LaTeX documents
---

# LaTeX Thesis Assistant (Chinese / 中文博士论文)

## Critical Rules / 核心原则

**绝对禁止违反以下规则：**
1. 绝不修改 `\cite{}`、`\ref{}`、`\label{}`、公式环境内的内容
2. 绝不凭空捏造参考文献条目 - 只能读取现有 .bib 文件
3. 绝不在未经许可的情况下修改专业术语（见 [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md)）
4. 绝不直接应用修改 - 始终先以注释形式输出 diff
5. 必须先运行结构映射，再开始分析
6. 中文文档必须使用 XeLaTeX 或 LuaLaTeX 编译

## Quick Start / 快速开始

### Compile Document / 编译文档
```bash
# Auto-detect and compile (XeLaTeX for Chinese)
python scripts/compile.py main.tex

# Explicit compiler (XeLaTeX recommended for Chinese)
python scripts/compile.py main.tex --compiler xelatex
python scripts/compile.py main.tex --compiler lualatex

# Using recipes (VS Code LaTeX Workshop style) / 使用编译配方
python scripts/compile.py main.tex --recipe xelatex           # XeLaTeX only
python scripts/compile.py main.tex --recipe latexmk           # LaTeXmk auto
python scripts/compile.py main.tex --recipe xelatex-bibtex    # xelatex -> bibtex -> xelatex*2
python scripts/compile.py main.tex --recipe xelatex-biber     # xelatex -> biber -> xelatex*2 (推荐)
python scripts/compile.py main.tex --recipe pdflatex-bibtex   # pdflatex -> bibtex -> pdflatex*2
python scripts/compile.py main.tex --recipe pdflatex-biber    # pdflatex -> biber -> pdflatex*2

# Continuous compilation (watch mode)
python scripts/compile.py main.tex --watch

# Clean auxiliary files / 清理辅助文件
python scripts/compile.py main.tex --clean
```

### Structure Mapping / 结构映射
```bash
# Map thesis structure (MUST run first)
python scripts/map_structure.py main.tex
```

## Workflow (5-Layer) / 工作流程

### Layer 0: Structure Mapping (MANDATORY)
```bash
python scripts/map_structure.py main.tex
```
Output: File tree + template type + processing order

### Layer 1: Structure Integrity Check
Check against [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md):

**Front Matter (必须):**
- Cover, Declaration, Abstract (CN+EN), TOC
- Symbol list (recommended)

**Main Body:**
- Chapter 1: Introduction (background, significance, contributions)
- Chapter 2: Related Work
- Chapters 3-N: Core content
- Final Chapter: Conclusions

**Back Matter (必须):**
- References, Acknowledgments, Publication list

### Layer 2: GB/T 7714 Format Check
See [GB_STANDARD.md](references/GB_STANDARD.md):
- Bibliography format (biblatex-gb7714-2015)
- Figure/table captions (宋体五号)
- Equation numbering (e.g., (3.1))
- Section heading styles

### Layer 3: Chinese Academic Expression
See [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md):

**Oral → Academic conversion:**
- ❌ "很多研究表明" → ✅ "大量研究表明"
- ❌ "效果很好" → ✅ "具有显著优势"

**Forbidden subjective words:**
- ❌ 显然、毫无疑问、众所周知
- ✅ 研究表明、实验结果显示、可以认为

### Layer 4: Long Sentence Decomposition
**Trigger**: >60 characters or >3 clauses

```latex
% 长难句检测（第45行，共87字）
% 主干：本文方法在多个数据集上取得优异性能。
% 修饰成分：
% - [定语] 基于深度学习的
% - [方式] 通过引入注意力机制
% 建议改写：[分拆版本]
```

### Layer 5: Expression Restructuring
```latex
% ═══════════════════════════════════════════
% 修改建议（第23行）
% ═══════════════════════════════════════════
% 原文：我们使用了ResNet模型。
% 修改后：本文采用ResNet模型作为特征提取器。
% 改进点：
% 1. "我们使用" → "本文采用"（学术规范）
% 2. 补充模型用途说明
% ═══════════════════════════════════════════
```

## Template Detection / 模板检测

Auto-detect university template:
```bash
python scripts/detect_template.py main.tex
```

Supported templates (see [UNIVERSITIES/](references/UNIVERSITIES/)):
- **thuthesis**: Tsinghua University
- **pkuthss**: Peking University
- **ustcthesis**: USTC
- **fduthesis**: Fudan University
- **generic**: General GB/T compliant

## Output Report / 输出报告

```markdown
# LaTeX 博士论文审查报告

## 总览
- 整体状态：✅ 符合要求 / ⚠️ 需要修订 / ❌ 重大问题
- 编译状态：[status]
- 模板类型：[detected template]

## 结构完整性（X/10 通过）
### ✅ 已完成项
### ⚠️ 待完善项

## 国标格式审查
### ✅ 符合项
### ❌ 不符合项

## 中文学术表达（N处建议）
[按优先级分组]

## 长难句拆解（M处）
[详细分析]
```

## References / 参考文档

- [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md): Thesis structure requirements
- [GB_STANDARD.md](references/GB_STANDARD.md): GB/T 7714 format rules
- [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md): Chinese academic writing
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): Protected terminology
- [COMPILATION.md](references/COMPILATION.md): XeLaTeX/LuaLaTeX compilation
- [UNIVERSITIES/](references/UNIVERSITIES/): University-specific templates
