---
name: latex-thesis-zh
description: |
  中文学位论文 LaTeX 助手（博士/硕士论文）。
  领域：深度学习、时间序列、工业控制。

  触发词（可独立调用任意模块）：
  - "compile", "编译", "xelatex" → 编译模块
  - "structure", "结构", "映射" → 结构映射模块
  - "format", "格式", "国标", "GB/T" → 国标格式检查模块
  - "expression", "表达", "润色", "学术表达" → 学术表达模块
  - "long sentence", "长句", "拆解" → 长难句分析模块
  - "bib", "bibliography", "参考文献" → 参考文献模块
  - "template", "模板", "thuthesis", "pkuthss" → 模板检测模块
  - "deai", "去AI化", "人性化", "降低AI痕迹" → 去AI化编辑模块
---

# LaTeX 中文学位论文助手

## 核心原则

1. 绝不修改 `\cite{}`、`\ref{}`、`\label{}`、公式环境内的内容
2. 绝不凭空捏造参考文献条目
3. 绝不在未经许可的情况下修改专业术语
4. 始终先以注释形式输出修改建议
5. 中文文档必须使用 XeLaTeX 或 LuaLaTeX 编译

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
编译失败时，优先定位首个错误并请求日志片段。

## 模块（独立调用）
除“结构映射”在**完整审查或多文件场景**中要求先执行外，其余模块均可独立调用。

### 模块：编译
**触发词**: compile, 编译, build, xelatex, lualatex

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
| XeLaTeX | xelatex | 中文快速编译（推荐）|
| LuaLaTeX | lualatex | 复杂字体需求 |
| LaTeXmk | latexmk -xelatex | 自动处理依赖 |
| xelatex -> bibtex -> xelatex×2 | xelatex → bibtex → xelatex → xelatex | 中文 + BibTeX |
| xelatex -> biber -> xelatex×2 | xelatex → biber → xelatex → xelatex | 中文 + Biber（推荐）|

**使用方法**:
```bash
# 单次编译（推荐 XeLaTeX）
python scripts/compile.py main.tex                          # 自动检测
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX
python scripts/compile.py main.tex --recipe lualatex        # LuaLaTeX

# 带参考文献编译（学位论文推荐）
python scripts/compile.py main.tex --recipe xelatex-biber   # Biber（推荐）
python scripts/compile.py main.tex --recipe xelatex-bibtex  # BibTeX

# 指定输出目录
python scripts/compile.py main.tex --recipe latexmk --outdir build

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

**输出格式**:
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

## 参考文档

- [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md): 论文结构要求
- [GB_STANDARD.md](references/GB_STANDARD.md): GB/T 7714 格式规范
- [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md): 中文学术写作规范
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): 受保护术语
- [COMPILATION.md](references/COMPILATION.md): XeLaTeX/LuaLaTeX 编译指南
- [UNIVERSITIES/](references/UNIVERSITIES/): 学校模板指南
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): 去AI化写作指南与常见模式
