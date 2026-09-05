# LaTeX 编译指南

## Skill 入口

在本 skill 中，通过自带 wrapper，使用论文实际入口文件和已识别的 recipe 编译：

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

也支持 LuaLaTeX 及其文献 recipe。下文原始命令用于说明编译器行为，不授权绕过 wrapper、
安装系统宏包、清理原 PDF 或启用 shell escape。入口文件、引擎、文献后端和输出路径均以
当前项目实际信息为准。

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

报告缺失宏包、wrapper 确切退出码和日志证据。未经明确授权，不安装 TeX Live 或 MiKTeX
宏包。

### 参考文献未更新
```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

检查项目后只选择一个匹配的 recipe；不要盲目运行两种 recipe，也不要删除原 PDF。

## 监视模式（持续编译）

```bash
# Auto-recompile on file changes
latexmk -xelatex -pvc main.tex

# With PDF viewer sync
latexmk -xelatex -pvc -view=pdf main.tex
```

## 编译页版式验证

题注、续图、长表、表格缩放或图像清晰度发生变化时，wrapper 成功只是编译门槛。涉及编号时，
检查相关 `.aux`、图目录或表目录条目，再渲染并实际查看修改页及相邻页。检查续图编号、题注
顺序、裁切、溢出、留白和文字可读性。图像 DPI 元数据或 PNG/PDF 文件存在，不能证明有效 ppi
或最终视觉质量；有效 ppi 取决于像素尺寸与最终排版尺寸。

未执行编译、渲染或目视检查时，列明缺失证据。不要用 PDF 压缩、清理、系统安装
或 UI 自动化替代这些证据。

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
