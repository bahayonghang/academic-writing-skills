# 示例：语法和逻辑复习

用户请求：
检查引言和相关工作部分的语法、句子长度和论证流程，但不要触及方程式或引文。

推荐模块顺序：
1. `grammar`
2. `sentences`
3. `logic`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/analyze_grammar.py main.tex --section introduction
uv run python -B $SKILL_DIR/scripts/analyze_sentences.py main.tex --section related
uv run python -B $SKILL_DIR/scripts/analyze_logic.py main.tex --section related
```

预期输出：
- LaTeX 评论结果按模块分组。
- 简短解释该问题是语法问题、可读性相关问题还是逻辑问题。
