# LaTeX 编译指南

## 编译器选择

### pdfLaTeX
- **最适合**：英文论文、快速编译
- **限制**：CJK 支持较弱，需要 `CJKutf8` 宏包
- **命令**：`latexmk -pdf main.tex`

### XeLaTeX（中文推荐）
- **最适合**：中文文档、Unicode 支持、系统字体
- **宏包**：`ctex`、`xeCJK`、`fontspec`
- **命令**：`latexmk -xelatex main.tex`

### LuaLaTeX
- **最适合**：现代功能、Lua 脚本、复杂排版
- **说明**：仍在积极维护，推荐用于面向未来的工程
- **命令**：`latexmk -lualatex main.tex`

## latexmk 配置

在项目根目录创建 `.latexmkrc`：

```perl
# For XeLaTeX (Chinese documents)
$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -interaction=nonstopmode -no-shell-escape %O %S';

# For pdfLaTeX (English papers)
# $pdf_mode = 1;
# $pdflatex = 'pdflatex -interaction=nonstopmode -no-shell-escape %O %S';

# Enable -shell-escape only for sources you have explicitly verified as trusted.

# Bibliography
$bibtex_use = 2;
$biber = 'biber %O %S';

# Output directory (optional)
# $out_dir = 'build';

# Clean extensions
@generated_exts = (@generated_exts, 'synctex.gz', 'nav', 'snm', 'vrb');
```

## 常见问题

### 找不到中文字体
```latex
% Specify fonts explicitly
\setCJKmainfont{SimSun}[BoldFont=SimHei, ItalicFont=KaiTi]
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}
```

### 缺少宏包
```bash
# TeX Live
tlmgr install <package-name>

# MiKTeX (auto-install on first use)
# Or use MiKTeX Console
```

### 参考文献未更新
```bash
# Force rebuild
latexmk -C main.tex  # Clean all
latexmk -xelatex main.tex  # Rebuild
```

## 监视模式（持续编译）

```bash
# Auto-recompile on file changes
latexmk -xelatex -pvc main.tex

# With PDF viewer sync
latexmk -xelatex -pvc -view=pdf main.tex
```

## 跨平台说明

### Windows
- 安装 MiKTeX 或 TeX Live
- 使用 PowerShell 或 CMD
- 路径使用正斜杠或转义后的反斜杠

### Linux
```bash
sudo apt-get install texlive-full latexmk
```

### macOS
```bash
brew install --cask mactex
# Or: brew install basictex
```
