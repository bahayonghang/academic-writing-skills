# LaTeX 中文学位论文助手

面向中文硕博论文的 LaTeX 写作工具包，覆盖结构映射、国标格式检查、模板检测与学术表达优化等全方位写作辅助。

## 功能特性

- **中文论文编译**：XeLaTeX / LuaLaTeX 编译流程与清理支持
- **结构映射**：多文件论文结构分析与完整性检查
- **国标合规**：GB/T 7714-2015 参考文献与版式规则校验
- **模板检测**：thuthesis、pkuthss、ustcthesis 等高校模板识别
- **学术表达**：口语化检测、学术化改写建议
- **逻辑分析**：段落衔接与方法论深度强化
- **长难句分析**：拆解复杂句，提高可读性
- **参考文献**：BibTeX 条目校验与引用一致性检查
- **去AI化编辑**：降低 AI 写作痕迹，保留学术准确性
- **标题优化**：根据学位论文规范优化和生成标题
- **一致性检查**：术语、格式全文一致性验证

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
**触发词**：`compile`, `编译`, `build`, `xelatex`, `lualatex`

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
详见 [COMPILATION.md](resources/COMPILATION.md)。

### 2. 结构映射模块
**触发词**：`structure`, `结构`, `映射`, `map`

```bash
python scripts/map_structure.py main.tex
```
详见 [STRUCTURE_GUIDE.md](resources/STRUCTURE_GUIDE.md)。

### 3. 国标格式检查模块
**触发词**：`format`, `格式`, `国标`, `GB/T`, `7714`

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```
详见 [GB_STANDARD.md](resources/GB_STANDARD.md)。

### 4. 学术表达模块
**触发词**：`expression`, `表达`, `润色`, `学术表达`, `口语化`

提供口语化检测与学术化改写建议。
详见 [ACADEMIC_STYLE_ZH.md](resources/ACADEMIC_STYLE_ZH.md)。

### 5. 逻辑衔接与方法论深度模块
**触发词**：`logic`, `coherence`, `逻辑`, `衔接`, `methodology`, `方法论`, `论证`, `argument`

加强段落间逻辑连接与论证严密性。
详见 [LOGIC_COHERENCE.md](resources/LOGIC_COHERENCE.md)。

### 6. 长难句分析模块
**触发词**：`long sentence`, `长句`, `拆解`, `simplify`

检测并拆解长句，提高可读性。

### 7. 参考文献模块
**触发词**：`bib`, `bibliography`, `参考文献`, `citation`, `引用`

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
```

### 8. 模板检测模块
**触发词**：`template`, `模板`, `thuthesis`, `pkuthss`, `ustcthesis`, `fduthesis`

```bash
python scripts/detect_template.py main.tex
```

### 9. 去AI化编辑模块
**触发词**：`deai`, `去AI化`, `人性化`, `降低AI痕迹`, `自然化`

降低 AI 写作痕迹并保持 LaTeX 语法与技术准确性。
详见 [DEAI_GUIDE.md](resources/DEAI_GUIDE.md)。

### 10. 标题优化模块
**触发词**：`title`, `标题`, `标题优化`, `生成标题`, `改进标题`

```bash
python scripts/optimize_title.py main.tex --generate
```
详见 [TITLE_OPTIMIZATION.md](resources/TITLE_OPTIMIZATION.md)。

### 11. 一致性检查模块
**触发词**：`consistency`, `一致性`, `术语`, `terminology`

```bash
python scripts/check_consistency.py main.tex
```
检查全文术语规范格式的一致性。

## 学校模板与规范

各高校模板要求见 `resources/UNIVERSITIES/`：
- 清华大学（thuthesis）
- 北京大学（pkuthss）
- 中国科学技术大学（ustcthesis）
- 复旦大学（fduthesis）
- 通用（ctexbook / GB/T 7713.1-2006）

## 参考文档

- [STRUCTURE_GUIDE.md](resources/STRUCTURE_GUIDE.md): 论文结构要求
- [GB_STANDARD.md](resources/GB_STANDARD.md): GB/T 7714 格式规范
- [ACADEMIC_STYLE_ZH.md](resources/ACADEMIC_STYLE_ZH.md): 中文学术写作规范
- [FORBIDDEN_TERMS.md](resources/FORBIDDEN_TERMS.md): 受保护术语
- [COMPILATION.md](resources/COMPILATION.md): XeLaTeX/LuaLaTeX 编译指南
- [UNIVERSITIES/](resources/UNIVERSITIES/): 学校模板指南
- [DEAI_GUIDE.md](resources/DEAI_GUIDE.md): 去AI化写作指南
- [TITLE_OPTIMIZATION.md](resources/TITLE_OPTIMIZATION.md): 标题优化指南
- [LOGIC_COHERENCE.md](resources/LOGIC_COHERENCE.md): 逻辑衔接与方法论深度指南
- [WRITING_PHILOSOPHY_ZH.md](resources/WRITING_PHILOSOPHY_ZH.md): 学位论文写作哲学

## 完整工作流

如需完整审查，建议按顺序执行：结构映射 → 国标格式检查 → 去AI化编辑 → 学术表达 → 长难句分析 → 参考文献检查。

## 常见问题

**Q: 中文论文应该用哪种编译器？**
A: 默认推荐 XeLaTeX；若有复杂字体需求可使用 LuaLaTeX。

**Q: 多文件论文必须先做结构映射吗？**
A: 建议先执行结构映射，以便确认章节顺序与文件依赖。

**Q: 参考文献用 BibTeX 还是 Biber？**
A: 以模板要求为准。若模板未明确，优先使用现代化的 Biber。

## 许可证

本工具以“按现状”方式提供，用于学术写作辅助。

## 贡献

欢迎提交 Issue 或 PR 改进本工具。
