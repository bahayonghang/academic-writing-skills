# Template Module Reference

Purpose: Detect and validate the university thesis template/class in use.

## Template Detection Workflow

1. **Scan document class**: Look for `\documentclass{thuthesis}`, `\documentclass{pkuthss}`, `\documentclass[...]{ctexbook}`, etc.
2. **Check package imports**: Identify `ctex`, `xeCJK`, `fontspec` and other template-specific packages.
3. **Match template**: Compare against known templates in `templates/` (single authoritative source).
4. **Report**: Output detected template name, version (if available), and any config warnings.

## Supported Templates

| Template           | University | Document Class                  |
| ------------------ | ---------- | ------------------------------- |
| thuthesis          | 清华大学   | `\documentclass{thuthesis}`     |
| pkuthss            | 北京大学   | `\documentclass{pkuthss}`       |
| ctexbook (generic) | Various    | `\documentclass[...]{ctexbook}` |

## Key Config Files

- `.latexmkrc` — compiler settings
- `*.cls` — template class file
- `*.cfg` — template configuration
- `refs.bib` / `references.bib` — bibliography database

## After Detection

Once the template is identified, load the corresponding template snapshot from:

- `templates/{template}.md`（thuthesis.md / pkuthss.md）for per-template constraints
- `templates/generic.md` as fallback for unknown templates（ustcthesis / fduthesis 暂同）
- `templates/yanshan.md` 为燕山大学规范获取指引（无可检测的 documentclass）

> See [`generic.md`](../../templates/generic.md), [`thuthesis.md`](../../templates/thuthesis.md),
> [`pkuthss.md`](../../templates/pkuthss.md), and [`yanshan.md`](../../templates/yanshan.md)
> for the authoritative per-template snapshots.
