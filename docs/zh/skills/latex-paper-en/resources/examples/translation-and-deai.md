# 示例：翻译与去AI

用户请求：
将中文技术段落翻译成学术英语，保留 `\cite{}` 和数学，然后在简介中标记任何听起来像人工智能的短语。

推荐模块顺序：
1. `translation`
2. `deai`

命令：
```bash
uv run python -B $SKILL_DIR/scripts/translate_academic.py input_zh.txt --domain deep-learning
uv run python -B $SKILL_DIR/scripts/deai_check.py main.tex --section introduction
```

预期输出：
- 保持 LaTeX 片段完整的翻译报告。
- `% DE-AI ...` 研究结果可在不更改引文、标签或方程式的情况下识别有风险的短语。
