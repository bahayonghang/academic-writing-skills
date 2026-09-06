# LaTeX Compilation Guide

## Skill Entry Point

Within this skill, compile through the bundled wrapper with the thesis's actual entry file and detected recipe:

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

LuaLaTeX and its bibliography recipes are also supported. The raw commands below document compiler behavior;
they do not authorize bypassing the wrapper, installing system packages, cleaning the original PDF, or enabling
shell escape. Use the entry file, engine, bibliography backend, and output path established by the current project.

## Compiler Selection

### pdfLaTeX
- **Best for**: English papers, fast compilation
- **Limitations**: Poor CJK support, requires `CJKutf8` package
- **Command**: `latexmk -pdf main.tex`

### XeLaTeX (Recommended for Chinese)
- **Best for**: Chinese documents, Unicode support, system fonts
- **Packages**: `ctex`, `xeCJK`, `fontspec`
- **Command**: `latexmk -xelatex main.tex`

### LuaLaTeX
- **Best for**: Modern features, Lua scripting, complex typography
- **Note**: Actively maintained, recommended for future-proofing
- **Command**: `latexmk -lualatex main.tex`

## latexmk Configuration

Create `.latexmkrc` in project root:

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

## Common Issues

### Chinese Font Not Found
```latex
% Specify fonts explicitly
\setCJKmainfont{SimSun}[BoldFont=SimHei, ItalicFont=KaiTi]
\setCJKsansfont{SimHei}
\setCJKmonofont{FangSong}
```

### Missing Package

Report the missing package and the wrapper's exact exit code and log evidence. Do not install TeX Live or MiKTeX
packages without explicit authorization.

### Bibliography Not Updating
```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-bibtex
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe xelatex-biber
```

Choose one matching recipe after inspecting the project; do not run both blindly and do not delete the original PDF.

## Watch Mode (Continuous Compilation)

```bash
# Auto-recompile on file changes
latexmk -xelatex -pvc main.tex

# With PDF viewer sync
latexmk -xelatex -pvc -view=pdf main.tex
```

## Rendered Layout Verification

For a caption, continued figure, long table, table scaling, or image-clarity change, wrapper success is only the
compilation gate. Inspect relevant `.aux` or list-of-figures/list-of-tables entries when numbering is involved, then
render and actually view the changed page and adjacent pages. Check continuation numbering, caption order, clipping,
overflow, blank regions, and text readability. Image DPI metadata or the existence of a PNG/PDF does not prove the
effective ppi or final visual quality; effective ppi depends on pixel dimensions and final layout size.

If compilation, rendering, or visual inspection was not performed, name the missing evidence. Do not add PDF
compression, cleanup, system installation, or UI automation as a substitute.

## Cross-Platform Notes

### Windows
- Install MiKTeX or TeX Live
- Use PowerShell or CMD
- Path: Use forward slashes or escaped backslashes

### Linux
```bash
sudo apt-get install texlive-full latexmk
```

### macOS
```bash
brew install --cask mactex
# Or: brew install basictex
```
