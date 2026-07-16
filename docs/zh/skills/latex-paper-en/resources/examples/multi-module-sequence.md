# 示例：多模块序列

用户请求：
检查简介中的语法、句子长度和逻辑，然后查看实验部分是否存在弱基线和缺失的消融。

推荐模块顺序：
1. `grammar`
2. `sentences`
3. `logic`
4. `experiment`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/analyze_grammar.py main.tex --section introduction
uv run python -B $SKILL_DIR/scripts/analyze_sentences.py main.tex --section introduction
uv run python -B $SKILL_DIR/scripts/analyze_logic.py main.tex --section introduction
uv run python -B $SKILL_DIR/scripts/analyze_experiment.py main.tex --section experiments
```

预期输出：
- 结果按模块分组，而不是按一个混合评论块分组。
- 散文问题和实验评论问题之间有明确的区别。
- 如果任何模块失败，则报告准确的命令和退出代码。
