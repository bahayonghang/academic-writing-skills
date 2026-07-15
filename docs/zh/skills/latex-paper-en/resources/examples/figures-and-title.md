# 示例：数字和标题

用户请求：
在提交给 ACM 之前，请检查我的数据是否已准备好发表以及标题是否过于通用。

推荐模块顺序：
1. `figures`
2. `title`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/check_figures.py main.tex
uv run python -B $SKILL_DIR/scripts/optimize_title.py main.tex --check
```

预期输出：
- 图关于丢失文件、DPI 或标题/扩展名问题的警告。
- 标题分数以及具体的标题改进建议。
