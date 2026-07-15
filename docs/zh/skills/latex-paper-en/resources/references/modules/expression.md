# 模块：表达重组

**触发**：学术语气、学术表达、提高写作、弱动词

弱动词替换：
- 使用 → 雇用、利用、利用
- get → 获得，实现，获得
- 制作 → 构建、开发、生成
- show → 展示，说明，表明

```bash
uv run python -B scripts/improve_expression.py main.tex
uv run python -B scripts/improve_expression.py main.tex --section related
```

输出格式：
```latex
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2]: Improve academic tone
% Original: We use machine learning to get better results.
% Revised: We employ machine learning to achieve superior performance.
% Rationale: Replace weak verbs with academic alternatives
```

风格指南：[style-guide.md](../writing/style-guide.md)

