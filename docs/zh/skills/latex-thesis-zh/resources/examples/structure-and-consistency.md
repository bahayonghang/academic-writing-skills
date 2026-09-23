# 示例：结构与一致性检查

用户请求：
请把这篇中文学位论文的结构梳理出来，再检查术语和缩略语有没有前后不一致。

推荐模块顺序：
1. `structure`
2. `consistency`

命令：
```bash
uv run python $SKILL_DIR/scripts/map_structure.py main.tex
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --abbreviations
```

预期输出：
- 章节结构概览。
- 术语、缩略语漂移问题及其所在位置。

## 可选治理、缩写体例与程度词

用户请求：
请用合成配置检查禁用词、锁定名、缩写体例和程度词，不要改旧的默认检查。

命令：
```bash
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --governance --custom-terms terms.json
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --abbreviation-style
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --degree-wording
```

预期输出：
- `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。
- 只报告局部词、字段和位置，不给整句替换。
- 不传上述开关时，原输出保持不变。
