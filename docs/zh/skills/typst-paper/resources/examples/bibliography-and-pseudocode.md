# 示例：参考书目和伪代码

用户请求：
验证该 Typst 项目是否使用 Hayagriva 或 BibTeX，然后查看 `algorithm-figure` 块并告诉我哪些问题是强制性的，哪些问题仅是 IEEE 类似的建议。

推荐模块顺序：
1. `bibliography`
2. `pseudocode`

命令：
```bash
uv run python $SKILL_DIR/scripts/verify_bib.py references.yml --typ main.typ
uv run python $SKILL_DIR/scripts/check_pseudocode.py main.typ --venue ieee
```

预期输出：
- 在运行检查之前检测参考书目格式。
- 保留 `@cite`、标签和 Typst 宏。
- 将硬包装/标题问题与行号或注释长度等咨询项目分开。
