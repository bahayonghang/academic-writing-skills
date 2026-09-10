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

## Output Path Contract

```bash
uv run python $SKILL_DIR/scripts/compile.py main.tex --outdir build
uv run python $SKILL_DIR/scripts/compile.py main.tex --recipe latexmk --outdir build
uv run python $SKILL_DIR/scripts/compile.py main.tex --compiler xelatex --outdir "build output"
uv run python $SKILL_DIR/scripts/compile.py main.tex --compiler lualatex --outdir build
```

The source entry's parent directory is the working directory. Without `--outdir`, the expected PDF is the source
entry with its extension replaced by `.pdf`. Relative output directories resolve against that parent directory;
absolute directories are normalized without changing their location. Spaces and Chinese characters remain in one
command argument. The same resolved output path drives both latexmk arguments and the final PDF check/report.

The default path and explicit `--compiler` use latexmk, as does `--recipe latexmk`. All support `--outdir`.
Manual `xelatex` / `lualatex` recipes and their `-bibtex` / `-biber` variants do not support output-directory
coordination: with `--outdir` they return 1 before any TeX or bibliography process, with a supported-path hint.
They are never silently converted to a different recipe. Without `--outdir`, manual recipes retain their
existing behavior, including continuing after nonzero BibTeX/Biber warnings.

For normally completed latexmk runs, a nonzero process result is returned even if a PDF exists. Exit code 0
requires a PDF at the expected path; a missing target returns 1, and a source-directory PDF cannot substitute
for an output-directory target. This also fixes the former false success for explicit compiler runs with no PDF,
including runs without `--outdir`. A target already considered up to date by latexmk is a valid success: the
wrapper does not force rebuilding, compare timestamps, or prove content/visual correctness. Watch interruption
handling is unchanged.

The wrapper derives this path from the source filename and `--outdir`; it does not infer output overrides from
`.latexmkrc`, `jobname`, or `auxdir`. Pass the intended directory explicitly. Supporting custom naming or manual
bibliography output paths requires a separate change.

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

# Set the output directory through wrapper --outdir build.

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
