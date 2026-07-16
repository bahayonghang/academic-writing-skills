# 示例：编译和格式化

用户请求：
编译这篇 Typst 论文以进行 IEEE 风格的审查，并告诉我布局是否看起来明显不对劲。

推荐模块顺序：
1. `compile`
2. `format`

命令：
```bash
uv run python $SKILL_DIR/scripts/compile.py main.typ
uv run python $SKILL_DIR/scripts/check_format.py main.typ --venue ieee
```

预期输出：
- 使用调用的命令输入 Typst 编译结果。
- `// FORMAT ...` 有关论文大小、栏目、标题或引文的调查结果。
