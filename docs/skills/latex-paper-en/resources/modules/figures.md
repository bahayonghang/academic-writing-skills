# Module: Figures

**Trigger**: figures, figure, missing image, DPI, resolution, raster, graphicspath, image assets

## Commands

```bash
uv run python -B scripts/check_figures.py main.tex
uv run python -B scripts/check_figures.py main.tex --min-dpi 300
```

## Details

`check_figures.py` scans `\includegraphics` calls, resolves image paths inside the project, and reports:

- missing image files;
- raster formats that should usually be converted to vector when possible;
- low DPI or likely low-resolution assets.

This module is about figure asset quality, not caption wording. If the request is about caption phrasing or evidence boundaries, use `caption` instead.

Skill-layer response:

1. Convert missing-file and low-quality findings into concise diff-style comments.
2. Keep line numbers, asset paths, and severity clear.
3. Mark caption-writing requests as out of scope unless the user also asks for `caption`.
