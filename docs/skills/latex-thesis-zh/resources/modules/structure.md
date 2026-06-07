# Module: Structure

**Trigger**: structure, chapter map, thesis structure, 结构映射, 章节地图, 模板检测, completeness, processing order

## Commands

```bash
uv run python -B scripts/map_structure.py thesis.tex
uv run python -B scripts/map_structure.py thesis.tex --json
uv run python -B scripts/map_structure.py thesis.tex --detect-template
uv run python -B scripts/map_structure.py thesis.tex --order
uv run python -B scripts/detect_template.py thesis.tex
```

## Details

`map_structure.py` maps the thesis file tree and reports:

- included files and their nesting levels;
- detected file types such as cover, abstract, chapter, appendix, bibliography, and acknowledgment;
- template detection for thuthesis, pkuthss, ustcthesis, fduthesis, and generic ctexbook;
- completeness signals such as missing required front/back matter.

Use this module first when the user wants a chapter map, thesis skeleton, or template-aware overview.
If the task is about paragraph logic, chapter flow, or cross-section argumentation, hand off to `logic` after the structure pass.

Skill-layer response:

1. Return a tree-style structure view or JSON output when requested.
2. Highlight missing required parts and likely chapter ordering issues.
3. Keep template detection separate from prose rewriting.
