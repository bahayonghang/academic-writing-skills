# 示例：参考书目和标题

用户请求：
验证我提交的 Typst 中的参考书目，并告诉我标题对于系统论文来说是否过于模糊。

推荐模块顺序：
1. `bibliography`
2. `title`

命令：
```bash
uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --typ main.typ
uv run python $SKILL_DIR/scripts/optimize_title.py main.typ --check
```

预期输出：
- BibTeX 或 Hayagriva 缺失/未使用的引文结果。
- 标题分数加上候选人的改进。
