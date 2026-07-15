# 模块：编译

**触发器**：编译、编译、构建、pdflatex、xelatex

**默认行为**：使用 `latexmk` 自动处理所有依赖项（bibtex/biber、交叉引用、索引）并确定最佳编译遍数。这是大多数用例的推荐方法。

**工具**（配套VS Code LaTeX Workshop）：
|工具|命令|参数|
|------|---------|------|
|赛拉泰克斯| `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
|pdf乳胶| `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
|乳胶| `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
|比布克斯| `bibtex` | `%DOCFILE%` |
|比伯| `biber` | `%DOCFILE%` |

**食谱**：
|食谱|步骤|使用案例|
|--------|-------|----------|
|乳胶|LatexMK（自动）|**默认** - 自动处理所有依赖项|
|PDFLaTeX|pdf乳胶|快速单通道构建|
|XeLaTeX|赛拉泰克斯|快速单通道构建|
|pdflatex -> bibtex -> pdflatex*2|pdflatex → bibtex → pdflatex → pdflatex|传统 BibTeX 工作流程|
|pdflatex -> biber -> pdflatex*2|pdflatex → biber → pdflatex → pdflatex|现代 biblatex（推荐用于新项目）|
|xelatex -> bibtex -> xelatex*2|xelatex → bibtex → xelatex → xelatex|中文/Unicode + BibTeX|
|xelatex -> biber -> xelatex*2|xelatex → biber → xelatex → xelatex|中文/Unicode + biblatex|

**用法**：
```bash
# Default: latexmk auto-handles all dependencies (recommended)
uv run python -B scripts/compile.py main.tex                          # Auto-detect compiler + latexmk

# Single-pass compilation (quick builds)
uv run python -B scripts/compile.py main.tex --recipe pdflatex        # PDFLaTeX only
uv run python -B scripts/compile.py main.tex --recipe xelatex         # XeLaTeX only

# Explicit bibliography workflows (when you need control)
uv run python -B scripts/compile.py main.tex --recipe pdflatex-bibtex # Traditional BibTeX
uv run python -B scripts/compile.py main.tex --recipe pdflatex-biber  # Modern biblatex (recommended)
uv run python -B scripts/compile.py main.tex --recipe xelatex-bibtex  # XeLaTeX + BibTeX
uv run python -B scripts/compile.py main.tex --recipe xelatex-biber   # XeLaTeX + biblatex

# With output directory
uv run python -B scripts/compile.py main.tex --outdir build

# Force detected-compiler biber workflow
uv run python -B scripts/compile.py main.tex --biber

# Utilities
uv run python -B scripts/compile.py main.tex --watch                  # Watch mode
uv run python -B scripts/compile.py main.tex --clean                  # Clean aux files
uv run python -B scripts/compile.py main.tex --clean-all              # Clean all (incl. PDF)
```

**自动检测**：脚本检测中文内容（ctex、xeCJK、中文字符）并自动选择 xelatex。

