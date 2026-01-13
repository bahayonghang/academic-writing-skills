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
---

# LaTeX 中文学位论文助手

## 核心原则

1. 绝不修改 `\cite{}`、`\ref{}`、`\label{}`、公式环境内的内容
2. 绝不凭空捏造参考文献条目
3. 绝不在未经许可的情况下修改专业术语
4. 始终先以注释形式输出修改建议
5. 中文文档必须使用 XeLaTeX 或 LuaLaTeX 编译

## 模块（独立调用）

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

**必须首先执行**：分析多文件论文结构

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
% 修改建议（第23行）
% ═══════════════════════════════════════════
% 原文：我们使用了ResNet模型。
% 修改后：本文采用ResNet模型作为特征提取器。
% 改进点：
% 1. "我们使用" → "本文采用"（学术规范）
% 2. 补充模型用途说明
% ═══════════════════════════════════════════
```

详见 [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md)

---

### 模块：长难句分析
**触发词**: long sentence, 长句, 拆解, simplify

**触发条件**: 句子 >60 字 或 >3 个从句

**输出格式**:
```latex
% 长难句检测（第45行，共87字）
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

## 完整工作流（可选）

如需完整审查，按顺序执行：

1. **结构映射** → 分析论文结构
2. **国标格式检查** → 修复格式问题
3. **学术表达** → 改进表达
4. **长难句分析** → 简化复杂句
5. **参考文献** → 验证引用

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
