---
name: latex-thesis-zh
category: academic-writing
tags:
  - latex
  - thesis
  - chinese
  - phd
  - master
  - xelatex
  - gb7714
  - thuthesis
  - pkuthss
  - compilation
  - bibliography
description: |
  中文学位论文 LaTeX 助手（博士/硕士论文）。
  Use when writing, reviewing, or improving Chinese LaTeX theses (PhD/Master).
  Use when user mentions 编译, 格式, 去AI化, 标题, 参考文献, 模板, 一致性,
  or any Chinese thesis quality task.
  支持多种学校模板和 GB/T 7714 国标格式。

  触发词（可独立调用任意模块）：
  - "compile", "编译", "xelatex" → 编译模块
  - "structure", "结构", "映射" → 结构映射模块
  - "format", "格式", "国标", "GB/T" → 国标格式检查模块
  - "expression", "表达", "润色", "学术表达" → 学术表达模块
  - "logic", "coherence", "逻辑", "衔接", "methodology", "方法论" → 逻辑衔接与方法论深度模块
  - "long sentence", "长句", "拆解" → 长难句分析模块
  - "bib", "bibliography", "参考文献" → 参考文献模块
  - "template", "模板", "thuthesis", "pkuthss" → 模板检测模块
  - "deai", "去AI化", "人性化", "降低AI痕迹" → 去AI化编辑模块
  - "title", "标题", "标题优化", "生成标题" → 标题优化模块
  - "consistency", "一致性", "术语" → 一致性检查模块
argument-hint: "[main.tex] [--section <章节>] [--module <模块>]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(xelatex *), Bash(lualatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *)
---

# LaTeX 中文学位论文助手

## 核心原则

1. 绝不修改 `\cite{}`、`\ref{}`、`\label{}`、公式环境内的内容
2. 绝不凭空捏造参考文献条目
3. 绝不在未经许可的情况下修改专业术语
4. 始终先以注释形式输出修改建议
5. 中文文档必须使用 XeLaTeX 或 LuaLaTeX 编译

## 参数约定（$ARGUMENTS）

- `$ARGUMENTS` 用于接收主文件路径、目标章节、模块选择等关键信息。
- 若 `$ARGUMENTS` 缺失或含糊，先询问：主 `.tex` 路径、目标范围、所需模块。
- 路径按字面处理，不推断或补全未提供的路径。

## 执行约束

- 仅在用户明确要求时执行脚本/编译命令。
- 涉及清理（`--clean` / `--clean-all`）等破坏性操作前先确认。

## 统一输出协议（全部模块）

每条建议必须包含固定字段：
- **严重级别**：Critical / Major / Minor
- **优先级**：P0（阻断）/ P1（重要）/ P2（可改进）

```latex
% <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
% 原文：...
% 修改后：...
% 理由：...
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理（全局）

```latex
% ERROR [Severity: Critical] [Priority: P0]: <简要错误>
% 原因：<缺少脚本/工具或路径无效>
% 建议：<安装工具/核对路径/重试命令>
```

## 模块（独立调用）

除"结构映射"在**完整审查或多文件场景**中要求先执行外，其余模块均可独立调用。

---

### 模块：编译
**触发词**: compile, 编译, build, xelatex, lualatex

```bash
python scripts/compile.py main.tex                          # 默认: latexmk + XeLaTeX（推荐）
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX 单次
python scripts/compile.py main.tex --recipe lualatex        # LuaLaTeX 单次
python scripts/compile.py main.tex --recipe xelatex-bibtex  # 传统 BibTeX
python scripts/compile.py main.tex --recipe xelatex-biber   # 现代 biblatex（推荐）
python scripts/compile.py main.tex --outdir build           # 指定输出目录
python scripts/compile.py main.tex --watch                  # 监视模式
python scripts/compile.py main.tex --clean                  # 清理辅助文件
```

自动检测 ctex、xeCJK 或中文字符时选择 XeLaTeX。详见 [COMPILATION.md](resources/COMPILATION.md)

---

### 模块：结构映射
**触发词**: structure, 结构, 映射, map

**完整审查/多文件场景先执行**：分析多文件论文结构。

```bash
python scripts/map_structure.py main.tex
```

输出文件树结构、模板类型检测、章节处理顺序。详见 [STRUCTURE_GUIDE.md](resources/STRUCTURE_GUIDE.md)

---

### 模块：国标格式检查
**触发词**: format, 格式, 国标, GB/T, 7714

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

检查 GB/T 7714-2015 参考文献格式、图表标题、公式编号、标题样式。详见 [GB_STANDARD.md](resources/GB_STANDARD.md)

---

### 模块：学术表达
**触发词**: expression, 表达, 润色, 学术表达, 口语化

用户提供段落源码，Agent 分析并返回润色版本及对比表格。

**核心规则**：
- 口语 → 学术转换（"很多研究表明" → "大量研究表明"）
- 禁用主观词汇（"显然"、"毫无疑问" → "研究表明"、"实验结果显示"）

详见 [ACADEMIC_STYLE_ZH.md](resources/ACADEMIC_STYLE_ZH.md)

---

### 模块：逻辑衔接与方法论深度
**触发词**: logic, coherence, 逻辑, 衔接, methodology, 方法论, 论证, argument

确保段落间逻辑流畅，强化方法论的严谨性。

**重点检查**：
- 段落级逻辑衔接（AXES 模型：主张→例证→解释→意义）
- 过渡信号词使用
- 方法论深度（方法选择论证、局限性承认、假设陈述）

详见 [LOGIC_COHERENCE.md](resources/LOGIC_COHERENCE.md)

---

### 模块：长难句分析
**触发词**: long sentence, 长句, 拆解, simplify

**触发条件**: 句子 >60 字 或 >3 个从句

```latex
% 长难句检测（第45行，共87字）[Severity: Minor] [Priority: P2]
% 主干：本文方法在多个数据集上取得优异性能。
% 修饰成分：
%   - [定语] 基于深度学习的
%   - [方式] 通过引入注意力机制
% 建议改写：拆分为多个短句，每句聚焦一个信息点。
```

---

### 模块：参考文献
**触发词**: bib, bibliography, 参考文献, citation, 引用

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex    # 检查引用
python scripts/verify_bib.py references.bib --standard gb7714 # 国标检查
```

检查必填字段完整性、重复条目、未使用条目、缺失引用、GB/T 7714 格式合规。

---

### 模块：模板检测
**触发词**: template, 模板, thuthesis, pkuthss, ustcthesis, fduthesis

```bash
python scripts/detect_template.py main.tex
```

| 模板 | 学校 |
|------|------|
| thuthesis | 清华大学 |
| pkuthss | 北京大学 |
| ustcthesis | 中国科学技术大学 |
| fduthesis | 复旦大学 |
| ctexbook | 通用（GB/T 7713.1-2006） |

详见 [UNIVERSITIES/](resources/UNIVERSITIES/)

---

### 模块：去AI化编辑
**触发词**: deai, 去AI化, 人性化, 降低AI痕迹, 自然化

在保持 LaTeX 语法和技术准确性的前提下，降低 AI 写作痕迹。

```bash
python scripts/deai_check.py main.tex --section introduction  # 单章节分析
python scripts/deai_check.py main.tex --analyze               # 全文密度检测
python scripts/deai_check.py main.tex --fix-suggestions        # JSON 修复建议
```

**AI 痕迹检测类型**：空话口号、过度确定、机械排比、模板表达

**硬性约束**：
- **绝不修改**：`\cite{}`、`\ref{}`、`\label{}`、公式环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号
- **仅修改**：普通段落文字、章节标题内的中文表达

详见 [DEAI_GUIDE.md](resources/DEAI_GUIDE.md)

---

### 模块：标题优化
**触发词**: title, 标题, 标题优化, 生成标题, 改进标题

根据学位论文规范和学术最佳实践，生成和优化论文标题。

```bash
python scripts/optimize_title.py main.tex --generate   # 生成候选标题
python scripts/optimize_title.py main.tex --optimize    # 优化现有标题
python scripts/optimize_title.py main.tex --check       # 质量评分（0-100）
```

评分维度：简洁性(25%)、可搜索性(30%)、长度(15%)、具体性(20%)、规范性(10%)

详见 [TITLE_OPTIMIZATION.md](resources/TITLE_OPTIMIZATION.md)

---

### 模块：一致性检查
**触发词**: consistency, 一致性, 术语, terminology

检查全文术语使用一致性。

```bash
python scripts/check_consistency.py main.tex                    # 默认术语组检查
python scripts/check_consistency.py main.tex --custom-terms terms.json  # 自定义术语组
```

**检查项目**：
- 同一概念的中英文术语是否全文统一
- 缩写首次出现是否有全称定义
- 数字/单位格式一致性

---

## 完整工作流（可选）

如需完整审查，按顺序执行：

1. **结构映射** → 分析论文结构
2. **国标格式检查** → 修复格式问题
3. **去AI化编辑** → 降低 AI 写作痕迹
4. **学术表达** → 改进表达
5. **长难句分析** → 简化复杂句
6. **参考文献** → 验证引用

---

## 参考文档

- [STRUCTURE_GUIDE.md](resources/STRUCTURE_GUIDE.md): 论文结构要求
- [GB_STANDARD.md](resources/GB_STANDARD.md): GB/T 7714 格式规范
- [ACADEMIC_STYLE_ZH.md](resources/ACADEMIC_STYLE_ZH.md): 中文学术写作规范
- [FORBIDDEN_TERMS.md](resources/FORBIDDEN_TERMS.md): 受保护术语
- [COMPILATION.md](resources/COMPILATION.md): XeLaTeX/LuaLaTeX 编译指南
- [UNIVERSITIES/](resources/UNIVERSITIES/): 学校模板指南
- [DEAI_GUIDE.md](resources/DEAI_GUIDE.md): 去AI化写作指南
- [TITLE_OPTIMIZATION.md](resources/TITLE_OPTIMIZATION.md): 标题优化详细指南
- [LOGIC_COHERENCE.md](resources/LOGIC_COHERENCE.md): 逻辑衔接与方法论深度指南
- [WRITING_PHILOSOPHY_ZH.md](resources/WRITING_PHILOSOPHY_ZH.md): 学位论文写作哲学
