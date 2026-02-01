# LaTeX 中文学位论文助手

面向中文硕博论文的 LaTeX 写作工具包，覆盖结构映射、国标格式检查、模板检测与学术表达优化。

## 功能特性

- **中文论文编译**：XeLaTeX / LuaLaTeX 编译流程与清理支持
- **结构映射**：多文件论文结构分析与完整性检查
- **国标合规**：GB/T 7714-2015 参考文献与版式规则校验
- **模板检测**：thuthesis、pkuthss 等高校模板识别
- **学术表达**：口语化检测、学术化改写建议
- **长难句分析**：拆解复杂句，提高可读性
- **参考文献**：BibTeX 条目校验与引用一致性检查
- **去AI化编辑**：降低 AI 写作痕迹，保留学术准确性
- **脚本工具**：可直接运行的 Python 辅助脚本

## 快速开始

### 环境准备

1. **LaTeX 发行版**：安装 TeX Live 或 MiKTeX（确保 `xelatex`/`lualatex`/`latexmk` 可用）
2. **Python 3**：用于执行脚本

### 基本用法

1. **编译论文**：
   ```bash
   python scripts/compile.py main.tex --recipe xelatex
   ```

2. **结构映射**：
   ```bash
   python scripts/map_structure.py main.tex
   ```

3. **国标格式检查**：
   ```bash
   python scripts/check_format.py main.tex --strict
   ```

4. **模板检测**：
   ```bash
   python scripts/detect_template.py main.tex
   ```

5. **参考文献验证**：
   ```bash
   python scripts/verify_bib.py references.bib --tex main.tex
   ```

6. **去AI化编辑（交互式）**：
   ```bash
   python scripts/deai_check.py main.tex --section introduction
   ```

## 模块说明

### 1. 编译模块
**触发词**：`compile`, `编译`, `xelatex`

```bash
# 自动检测（含中文优先 XeLaTeX）
python scripts/compile.py main.tex

# 指定编译器
python scripts/compile.py main.tex --recipe xelatex
python scripts/compile.py main.tex --recipe lualatex

# 带参考文献
python scripts/compile.py main.tex --recipe xelatex-biber
python scripts/compile.py main.tex --recipe xelatex-bibtex
```

### 2. 结构映射模块
**触发词**：`structure`, `结构`, `映射`

```bash
python scripts/map_structure.py main.tex
```

### 3. 国标格式检查模块
**触发词**：`format`, `格式`, `国标`, `GB/T`

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

### 4. 学术表达模块
**触发词**：`expression`, `表达`, `润色`, `学术表达`

提供口语化检测与学术化改写建议。
详见 [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md)。

### 5. 长难句分析模块
**触发词**：`long sentence`, `长句`, `拆解`

检测并拆解长句，提高可读性。

### 6. 参考文献模块
**触发词**：`bib`, `bibliography`, `参考文献`

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
```

### 7. 模板检测模块
**触发词**：`template`, `模板`, `thuthesis`, `pkuthss`

```bash
python scripts/detect_template.py main.tex
```

### 8. 去AI化编辑模块
**触发词**：`deai`, `去AI化`, `人性化`, `降低AI痕迹`

降低 AI 写作痕迹并保持 LaTeX 语法与技术准确性。
详见 [DEAI_GUIDE.md](references/DEAI_GUIDE.md)。

## 学校模板与规范

高校模板要求详见 `references/UNIVERSITIES/`，当前已整理：
- 清华大学（thuthesis）
- 北京大学（pkuthss）
- 燕山大学（研究生学位论文撰写规范 2024 版）
- 通用模板（ctexbook）

## 参考文档

- [STRUCTURE_GUIDE.md](references/STRUCTURE_GUIDE.md): 论文结构要求
- [GB_STANDARD.md](references/GB_STANDARD.md): GB/T 7714 格式规范
- [ACADEMIC_STYLE_ZH.md](references/ACADEMIC_STYLE_ZH.md): 中文学术写作规范
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): 受保护术语
- [COMPILATION.md](references/COMPILATION.md): XeLaTeX/LuaLaTeX 编译指南
- [UNIVERSITIES/](references/UNIVERSITIES/): 学校模板指南
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): 去AI化写作指南与常见模式

## 常见问题

**Q: 中文论文应该用哪种编译器？**
A: 默认推荐 XeLaTeX；若有复杂字体需求可使用 LuaLaTeX。

**Q: 多文件论文必须先做结构映射吗？**
A: 建议先执行结构映射，以便确认章节顺序与文件依赖。

**Q: 参考文献用 BibTeX 还是 Biber？**
A: 以模板要求为准。若模板未明确，优先使用 BibTeX。

## 许可证

本工具以“按现状”方式提供，用于学术写作辅助。

## 贡献

欢迎提交 Issue 或 PR 改进本工具。
