---
name: latex-thesis-zh
version: 1.1.0
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
  - deep-learning
  - compilation
  - bibliography
description: |
  中文学位论文 LaTeX 助手（博士/硕士论文）。
  领域：深度学习、时间序列、工业控制。

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

**默认注释模板**（diff-comment 风格）：
```latex
% <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
% 原文：...
% 修改后：...
% 理由：...
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

## 失败处理（全局）

工具/脚本无法执行时，输出包含原因与建议的注释块：
```latex
% ERROR [Severity: Critical] [Priority: P0]: <简要错误>
% 原因：<缺少脚本/工具或路径无效>
% 建议：<安装工具/核对路径/重试命令>
```
常见情况：
- **脚本不存在**：确认 `scripts/` 路径与工作目录
- **编译器缺失**：建议安装 TeX Live/MiKTeX 并加入 PATH
- **文件不存在**：请用户提供正确 `.tex` 路径
- **编译失败**：优先定位首个错误并请求日志片段

## 模块（独立调用）
除“结构映射”在**完整审查或多文件场景**中要求先执行外，其余模块均可独立调用。

### 模块：编译
**触发词**: compile, 编译, build, xelatex, lualatex

**默认行为**: 使用 `latexmk + XeLaTeX` 自动处理所有依赖（bibtex/biber、交叉引用、索引、术语表），并自动决定最优编译次数。这是中文论文的推荐方案。

**工具** (对齐 VS Code LaTeX Workshop):
| 工具 | 命令 | 参数 |
|------|------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| lualatex | `lualatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -xelatex -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**编译配置**:
| 配置 | 步骤 | 适用场景 |
|------|------|----------|
| latexmk | latexmk -xelatex (自动) | **默认** - 自动处理所有依赖（推荐）|
| XeLaTeX | xelatex | 快速单次编译 |
| LuaLaTeX | lualatex | 复杂字体需求 |
| xelatex -> bibtex -> xelatex×2 | xelatex → bibtex → xelatex → xelatex | 传统 BibTeX 工作流 |
| xelatex -> biber -> xelatex×2 | xelatex → biber → xelatex → xelatex | 现代 biblatex（推荐新论文）|

**使用方法**:
```bash
# 默认: latexmk + XeLaTeX 自动处理所有依赖（推荐）
python scripts/compile.py main.tex                          # 自动检测 + latexmk

# 单次编译（快速构建）
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX 单次
python scripts/compile.py main.tex --recipe lualatex        # LuaLaTeX 单次

# 显式参考文献工作流（需要精确控制时）
python scripts/compile.py main.tex --recipe xelatex-bibtex  # 传统 BibTeX
python scripts/compile.py main.tex --recipe xelatex-biber   # 现代 biblatex（推荐）

# 指定输出目录
python scripts/compile.py main.tex --outdir build

# 辅助功能
python scripts/compile.py main.tex --watch                  # 监视模式
python scripts/compile.py main.tex --clean                  # 清理辅助文件
python scripts/compile.py main.tex --clean-all              # 清理全部（含 PDF）
```

**自动检测**: 脚本检测到 ctex、xeCJK 或中文字符时自动选择 XeLaTeX。

---

### 模块：结构映射
**触发词**: structure, 结构, 映射, map

**完整审查/多文件场景先执行**：分析多文件论文结构

```bash
python scripts/map_structure.py main.tex
```

**输出内容**:
- 文件树结构
- 模板类型检测
- 章节处理顺序

**论文结构要求**:

| 部分 | 必需内容 |
|------|----------|
| 前置部分 | 封面、声明、摘要（中英）、目录、符号表 |
| 正文部分 | 绪论、相关工作、核心章节、结论 |
| 后置部分 | 参考文献、致谢、发表论文列表 |

详见 [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md)

---

### 模块：国标格式检查
**触发词**: format, 格式, 国标, GB/T, 7714

检查 GB/T 7714-2015 规范：

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

**检查项目**:
| 类别 | 规范 |
|------|------|
| 参考文献 | biblatex-gb7714-2015 格式 |
| 图表标题 | 宋体五号，图下表上 |
| 公式编号 | 章节编号如 (3.1) |
| 标题样式 | 各级标题字体字号 |

详见 [GB_STANDARD.md](references/GB_STANDARD.md)

---

### 模块：学术表达
**触发词**: expression, 表达, 润色, 学术表达, 口语化

**口语 → 学术转换**:
| ❌ 口语化 | ✅ 学术化 |
|----------|----------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |
| 比较好 | 较为优越 |

**禁用主观词汇**:
- ❌ 显然、毫无疑问、众所周知、不言而喻
- ✅ 研究表明、实验结果显示、可以认为、据此推断

**使用方式**：用户提供段落源码，Agent 分析并返回润色版本及对比表格。

**输出格式**（Markdown 对比表格）:
```markdown
| 原文 | 改进版本 | 问题类型 | 优化理由 |
|------|----------|----------|----------|
| 我们使用了ResNet模型。 | 本文采用ResNet模型作为特征提取器。 | 口语化表达 | "我们使用" → "本文采用"（学术规范）；补充模型用途说明 |
| 效果很好，可以看出性能提升明显。 | 实验结果表明，该方法具有显著的性能优势。 | 口语化 + 主观表达 | 避免"很好"、"可以看出"等口语化表达；使用"实验结果表明"增强客观性 |
| 显然，这种方法更优越。 | 实验结果显示，该方法在多个指标上优于基线方法。 | 过度主观 | 删除"显然"；用实验结果支撑结论；明确对比对象 |
```

**备选格式**（源码内注释）:
```latex
% ═══════════════════════════════════════════
% 修改建议（第23行）[Severity: Major] [Priority: P1]
% ═══════════════════════════════════════════
% 原文：我们使用了ResNet模型。
% 修改后：本文采用ResNet模型作为特征提取器。
% 改进点：
% 1. "我们使用" → "本文采用"（学术规范）
% 2. 补充模型用途说明
% 理由：口语化表达不符合学术规范
% ═══════════════════════════════════════════
```

详见 [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md)

---

### 模块：逻辑衔接与方法论深度
**触发词**: logic, coherence, 逻辑, 衔接, methodology, 方法论, 论证, argument

**目标**：确保段落间逻辑流畅，强化方法论的严谨性。

**重点检查领域**：

**1. 段落级逻辑衔接（AXES 模型）**：
| 组成部分 | 说明 | 示例 |
|----------|------|------|
| **A**ssertion（主张） | 清晰的主题句，陈述核心观点 | "注意力机制能够提升序列建模效果。" |
| **X**ample（例证） | 支撑主张的具体证据或数据 | "实验中，注意力机制达到95%准确率。" |
| **E**xplanation（解释） | 分析证据为何支撑主张 | "这一提升源于其捕获长程依赖的能力。" |
| **S**ignificance（意义） | 与更广泛论点或下一段的联系 | "这一发现为本文架构设计提供了依据。" |

**2. 过渡信号词**：
| 关系类型 | 中文信号词 | 英文对应 |
|----------|------------|----------|
| 递进 | 此外、进一步、更重要的是 | furthermore, moreover |
| 转折 | 然而、但是、相反 | however, nevertheless |
| 因果 | 因此、由此可见、故而 | therefore, consequently |
| 顺序 | 首先、随后、最后 | first, subsequently, finally |
| 举例 | 例如、具体而言、特别是 | for instance, specifically |

**3. 方法论深度检查清单**：
- [ ] 每个主张都有证据支撑（数据、引用或逻辑推理）
- [ ] 方法选择有充分理由（为何选此方法而非其他？）
- [ ] 明确承认研究局限性
- [ ] 清晰陈述前提假设
- [ ] 可复现性细节充分（参数、数据集、评估指标）

**4. 常见问题**：
| 问题类型 | 表现 | 修正方法 |
|----------|------|----------|
| 逻辑断层 | 段落间缺乏衔接 | 添加过渡句说明段落关系 |
| 无据主张 | 断言缺乏证据支撑 | 补充引用、数据或推理 |
| 方法论浅薄 | "本文采用X"但无理由 | 解释为何X适合本问题 |
| 隐含假设 | 前提条件未明示 | 显式陈述假设条件 |

**输出格式**：
```latex
% 逻辑衔接（第45行）[Severity: Major] [Priority: P1]: 段落间逻辑断层
% 问题：从问题描述直接跳转到解决方案，缺乏过渡
% 原文：数据存在噪声。本文提出一种滤波方法。
% 修改后：数据存在噪声，这对后续分析造成干扰。因此，本文提出一种滤波方法以解决该问题。
% 理由：添加因果过渡，连接问题与解决方案

% 方法论深度（第78行）[Severity: Major] [Priority: P1]: 方法选择缺乏论证
% 问题：方法选择未说明理由
% 原文：本文采用ResNet作为骨干网络。
% 修改后：本文采用ResNet作为骨干网络，其残差连接结构能有效缓解梯度消失问题，且在特征提取任务中表现优异。
% 理由：用技术原理论证架构选择
```

**分章节指南**：
| 章节 | 逻辑衔接重点 | 方法论深度重点 |
|------|--------------|----------------|
| 绪论 | 问题→空白→贡献的流畅衔接 | 论证研究意义 |
| 相关工作 | 按主题分组，显式对比 | 定位与前人工作的关系 |
| 方法 | 步骤间逻辑递进 | 论证每个设计选择 |
| 实验 | 设置→结果→分析的流程 | 解释评估指标选择 |
| 讨论 | 发现→启示→局限的衔接 | 承认研究边界 |

**最佳实践**（参考 [Elsevier](https://elsevier.blog/logical-academic-writing/)、[Proof-Reading-Service](https://www.proof-reading-service.com/blogs/academic-publishing/a-guide-to-creating-clear-and-well-structured-scholarly-arguments)）：
1. **一段一主题**：每段聚焦单一核心观点
2. **主题句先行**：段首即陈述本段主张
3. **证据链完整**：每个主张都需支撑（数据、引用或逻辑）
4. **显式过渡**：使用信号词标明段落关系
5. **论证而非描述**：解释"为何"，而非仅陈述"是什么"

---

### 模块：长难句分析
**触发词**: long sentence, 长句, 拆解, simplify

**触发条件**: 句子 >60 字 或 >3 个从句

**输出格式**:
```latex
% 长难句检测（第45行，共87字）[Severity: Minor] [Priority: P2]
% 主干：本文方法在多个数据集上取得优异性能。
% 修饰成分：
%   - [定语] 基于深度学习的
%   - [方式] 通过引入注意力机制
%   - [条件] 在保证实时性的前提下
% 建议改写：
%   本文提出基于深度学习的方法。该方法通过引入注意力机制，
%   在保证实时性的前提下，于多个数据集上取得优异性能。
```

---

### 模块：参考文献
**触发词**: bib, bibliography, 参考文献, citation, 引用

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex    # 检查引用
python scripts/verify_bib.py references.bib --standard gb7714 # 国标检查
```

**检查项目**:
- 必填字段完整性
- 重复条目检测
- 未使用条目
- 缺失引用
- GB/T 7714 格式合规

---

### 模块：模板检测
**触发词**: template, 模板, thuthesis, pkuthss, ustcthesis, fduthesis

```bash
python scripts/detect_template.py main.tex
```
输出包含模板识别结果与关键要求摘要（来自 `references/UNIVERSITIES/`）。

**支持的模板**:
| 模板 | 学校 | 特殊要求 |
|------|------|----------|
| thuthesis | 清华大学 | 图表编号：图 3-1 |
| pkuthss | 北京大学 | 需符号说明章节 |
| ustcthesis | 中国科学技术大学 | - |
| fduthesis | 复旦大学 | - |
| ctexbook | 通用 | 遵循 GB/T 7713.1-2006 |

详见 [UNIVERSITIES/](references/UNIVERSITIES/)

---

### 模块：去AI化编辑
**触发词**: deai, 去AI化, 人性化, 降低AI痕迹, 自然化

**目标**：在保持 LaTeX 语法和技术准确性的前提下，降低 AI 写作痕迹。

**输入要求**：
1. **源码类型**（必填）：LaTeX
2. **章节**（必填）：摘要 / 引言 / 相关工作 / 方法 / 实验 / 结果 / 讨论 / 结论 / 其他
3. **源码片段**（必填）：直接粘贴（保留原缩进与换行）

**使用示例**：

**交互式编辑**（推荐用于单章节）：
```python
python scripts/deai_check.py main.tex --section introduction
# 输出：交互式提问 + AI痕迹分析 + 改写后源码
```

**批量处理**（用于整章或全文）：
```bash
python scripts/deai_batch.py main.tex --chapter chapter3/introduction.tex
python scripts/deai_batch.py main.tex --all-sections  # 处理整个文档
```

**工作流程**：
1. **语法结构识别**：检测 LaTeX 命令，完整保留：
   - 命令：`\command{...}`、`\command[...]{}`
   - 引用：`\cite{}`、`\ref{}`、`\label{}`、`\eqref{}`、`\autoref{}`
   - 环境：`\begin{...\end{...}`
   - 数学：`$...$`、`\[...\]`、equation/align 环境
   - 自定义宏（默认不改）

2. **AI 痕迹检测**：
   - 空话口号："重要意义"、"显著提升"、"全面系统"、"有效解决"
   - 过度确定："显而易见"、"必然"、"完全"、"毫无疑问"
   - 机械排比：无实质内容的三段式并列
   - 模板表达："近年来"、"越来越多的"、"发挥重要作用"

3. **文本改写**（仅改可见文本）：
   - 拆分长句（>50字）
   - 调整词序以符合自然表达
   - 用具体主张替换空泛表述
   - 删除冗余短语
   - 补充必要主语（不引入新事实）

4. **输出生成**：
   - **A. 改写后源码**：完整源码，最小侵入式修改
   - **B. 变更摘要**：3-10条要点说明改动类型
   - **C. 待补证标记**：标注需要证据支撑的断言

**硬性约束**：
- **绝不修改**：`\cite{}`、`\ref{}`、`\label{}`、公式环境
- **绝不新增**：事实、数据、结论、指标、实验设置、引用编号、文献 key
- **仅修改**：普通段落文字、章节标题内的中文表达

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

**AI 痕迹密度检测**：
```bash
python scripts/deai_check.py main.tex --analyze
# 输出：各章节 AI 痕迹密度得分 + 待改进章节建议
```

参考文档：[DEAI_GUIDE.md](references/DEAI_GUIDE.md)

---

### 模块：标题优化
**触发词**: title, 标题, 标题优化, 生成标题, 改进标题

**目标**：根据学位论文规范和学术最佳实践，生成和优化论文标题。

**使用示例**：

**根据内容生成标题**：
```bash
python scripts/optimize_title.py main.tex --generate
# 分析摘要/引言，提出 3-5 个标题候选方案
```

**优化现有标题**：
```bash
python scripts/optimize_title.py main.tex --optimize
# 分析当前标题并提供改进建议
```

**检查标题质量**：
```bash
python scripts/optimize_title.py main.tex --check
# 根据最佳实践评估标题（评分 0-100）
```

**标题质量标准**（基于 GB/T 7713.1-2006 及国际最佳实践）：

| 标准 | 权重 | 说明 |
|------|------|------|
| **简洁性** | 25% | 删除"关于...的研究"、"...的探索"、"新型"、"改进的" |
| **可搜索性** | 30% | 核心术语（方法+问题）出现在前 20 字内 |
| **长度** | 15% | 最佳：15-25 字；可接受：10-30 字 |
| **具体性** | 20% | 具体方法/问题名称，避免泛泛而谈 |
| **规范性** | 10% | 符合学位论文标题规范，避免生僻缩写 |

**标题生成工作流**：

**步骤 1：内容分析**
从摘要/引言中提取：
- **研究问题**：解决什么挑战？
- **研究方法**：提出什么方法？
- **应用领域**：什么应用场景？
- **核心贡献**：主要成果是什么？（可选）

**步骤 2：关键词提取**
识别 3-5 个核心关键词：
- 方法关键词："Transformer"、"图神经网络"、"强化学习"
- 问题关键词："时间序列预测"、"故障检测"、"图像分割"
- 领域关键词："工业控制"、"医学影像"、"自动驾驶"

**步骤 3：标题模板选择**
学位论文常用模式：

| 模式 | 示例 | 适用场景 |
|------|------|----------|
| 基于方法的问题研究 | "基于Transformer的时间序列预测方法研究" | 方法创新型 |
| 领域中的问题与方法 | "工业系统故障检测的图神经网络方法" | 应用导向型 |
| 问题的方法及应用 | "时间序列预测的注意力机制及其在工业控制中的应用" | 理论+应用型 |
| 面向领域的方法研究 | "面向智能制造的深度学习预测性维护方法" | 领域专项型 |

**步骤 4：生成标题候选**
生成 3-5 个不同侧重的候选标题：
1. 方法侧重型
2. 问题侧重型
3. 应用侧重型
4. 平衡型（推荐）
5. 简洁变体

**步骤 5：质量评分**
每个候选标题获得：
- 总体评分（0-100）
- 各标准细分评分
- 具体改进建议

**标题优化规则**：

**❌ 删除无效词汇**：
| 避免使用 | 原因 |
|----------|------|
| 关于...的研究 | 冗余（所有论文都是研究） |
| ...的探索 | 冗余且不具体 |
| 新型 / 新颖的 | 发表即意味着新颖 |
| 改进的 / 优化的 | 不具体，需说明如何改进 |
| 基于...的 | 可简化为直接表述 |

**✅ 推荐结构**：
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究

好：图神经网络故障检测方法及其工业应用
差：新型改进的基于图神经网络的故障检测方法研究

好：注意力机制的多变量时间序列预测方法
差：基于注意力机制的改进型多变量时间序列预测模型研究
```

**关键词布局策略**：
- **前 20 字**：最重要的关键词（方法+问题）
- **避免开头**："关于"、"对于"、"针对"（可放在中间）
- **优先使用**：名词和技术术语，而非动词和形容词

**缩写使用准则**：
| ✅ 可接受 | ❌ 标题中避免 |
|----------|--------------|
| AI、机器学习、深度学习 | 实验室特定缩写 |
| LSTM、GRU、CNN | 化学分子式（除非极常见） |
| 物联网、5G、GPS | 非标准方法名缩写 |
| DNA、RNA、MRI | 生僻领域专用缩写 |

**学校模板特殊要求**：

**清华大学（thuthesis）**：
- 中文标题：不超过 36 个汉字
- 英文标题：对应中文标题翻译
- 避免使用缩写和公式
- 示例："深度学习在智能制造预测性维护中的应用研究"

**北京大学（pkuthss）**：
- 中文标题：简明扼要，一般不超过 25 字
- 可使用副标题（用破折号分隔）
- 示例："图神经网络故障检测方法——面向工业控制系统的研究"

**通用要求（ctexbook）**：
- 遵循 GB/T 7713.1-2006 规范
- 中文标题：15-25 字为宜
- 英文标题：对应翻译，注意冠词和介词
- 示例："基于Transformer的时间序列预测方法及应用"

**输出格式**：

```latex
% ============================================================
% 标题优化报告
% ============================================================
% 当前标题："关于基于深度学习的时间序列预测的研究"
% 质量评分：48/100
%
% 检测到的问题：
% 1. [严重] 包含"关于...的研究"（删除冗余词汇）
% 2. [重要] 方法描述过于宽泛（"深度学习"太笼统）
% 3. [次要] 长度可接受（18字）但可更具体
%
% 推荐标题（按评分排序）：
%
% 1. "工业控制系统时间序列预测的Transformer方法" [评分: 94/100]
%    - 简洁性：✅ (19字)
%    - 可搜索性：✅ (方法+问题在前15字)
%    - 具体性：✅ (Transformer，而非"深度学习")
%    - 领域性：✅ (工业控制系统)
%    - 规范性：✅ (符合学位论文规范)
%
% 2. "多变量时间序列预测的注意力机制研究" [评分: 89/100]
%    - 简洁性：✅ (17字)
%    - 可搜索性：✅ (核心术语靠前)
%    - 具体性：✅ (注意力机制、多变量)
%    - 建议：可考虑添加应用领域
%
% 3. "深度学习时间序列预测方法及其在智能制造中的应用" [评分: 81/100]
%    - 简洁性：⚠️ (24字，可接受)
%    - 可搜索性：✅
%    - 具体性：⚠️ ("深度学习"仍较宽泛)
%    - 领域性：✅ (智能制造)
%
% 关键词分析：
% - 主要：Transformer、时间序列、预测
% - 次要：工业控制、注意力、LSTM
% - 可搜索性："Transformer 时间序列"在知网出现 456 篇（平衡度好）
%
% 建议的 LaTeX 更新：
% \title{工业控制系统时间序列预测的Transformer方法}
% \englishtitle{Transformer-Based Time Series Forecasting for Industrial Control Systems}
% ============================================================
```

**中英文标题对照**：

标题翻译时需注意：
- 中文"基于X的Y"通常译为 "X-Based Y" 或 "Y via X"
- 避免逐字翻译，保持英文表达习惯
- 英文标题使用 Title Case（主要词首字母大写）

| 中文标题 | 英文标题 |
|----------|----------|
| 工业系统故障检测的图神经网络方法 | Graph Neural Networks for Fault Detection in Industrial Systems |
| 基于注意力机制的时间序列预测研究 | Attention-Based Time Series Forecasting |
| 深度学习在智能制造中的应用 | Deep Learning Applications in Smart Manufacturing |

**交互式模式**（推荐）：
```bash
python scripts/optimize_title.py main.tex --interactive
# 逐步引导式标题创建，包含用户输入
```

**批量模式**（多篇论文）：
```bash
python scripts/optimize_title.py chapters/*.tex --batch --output title_report.txt
```

**标题对比测试**（可选）：
```bash
python scripts/optimize_title.py main.tex --compare "标题A" "标题B" "标题C"
# 对比多个标题候选，提供详细评分
```

**最佳实践总结**：
1. **关键词前置**：方法+问题放在前 20 字
2. **具体明确**："Transformer" > "深度学习" > "机器学习"
3. **删除冗余**：去掉"关于"、"研究"、"新型"、"基于"
4. **控制长度**：目标 15-25 字（中文）
5. **测试可搜索性**：用这些关键词能找到你的论文吗？
6. **避免生僻**：除非是广泛认可的术语（AI、LSTM、CNN）
7. **符合规范**：遵循学校模板和 GB/T 7713.1-2006 标准

参考文档：[GB_STANDARD.md](references/GB_STANDARD.md)、[UNIVERSITIES/](references/UNIVERSITIES/)

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

## 输出报告模板

```markdown
# LaTeX 学位论文审查报告

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

## 学术表达（N处建议）
[按优先级分组]

## 长难句拆解（M处）
[详细分析]
```

---

## 最佳实践

本技能遵循 Claude Code Skills 最佳实践：

### 技能设计原则
1. **职责单一**：每个模块处理一项特定任务（KISS 原则）
2. **最小权限**：仅请求必要的工具访问权限
3. **明确触发**：使用特定关键词调用模块
4. **结构化输出**：所有建议使用统一的 diff-comment 格式

### 使用指南
1. **先检查编译**：在进行其他检查前，确保文档能正常编译
2. **迭代优化**：每次只应用一个模块，便于控制修改范围
3. **保护关键元素**：绝不修改 `\cite{}`、`\ref{}`、`\label{}`、公式环境
4. **提交前验证**：接受修改前仔细审查所有建议

### 与其他工具集成
- 配合版本控制（git）跟踪修改历史
- 结合 LaTeX Workshop 实现实时预览
- 导出建议与导师或合作者共同审阅

---

## 参考文档

- [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md): 论文结构要求
- [GB_STANDARD.md](references/GB_STANDARD.md): GB/T 7714 格式规范
- [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md): 中文学术写作规范
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): 受保护术语
- [COMPILATION.md](references/COMPILATION.md): XeLaTeX/LuaLaTeX 编译指南
- [UNIVERSITIES/](references/UNIVERSITIES/): 学校模板指南
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): 去AI化写作指南与常见模式
