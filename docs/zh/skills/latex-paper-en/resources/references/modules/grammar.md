# 模块：语法分析

**触发**：语法、校对、文章用法、时态、主谓一致

**目的**：对现有 LaTeX/Typst 文档中的可见散文运行轻量级、基于规则的语法传递。

## 命令

```bash
uv run python -B scripts/analyze_grammar.py main.tex
uv run python -B scripts/analyze_grammar.py main.tex --section introduction
```

## 原始脚本输出

该脚本会发出审阅者风格的注释块，例如：

```latex
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1]: Rule hit: \bwe propose method\b
% Original: We propose method for time series forecasting.
% Revised:  we propose a method for time series forecasting.
% Rationale: Grammar: Article missing before singular count noun.
```

## 技能层响应

- 保持最终答案的源头意识和简洁。
- 保留方程、引文、标签和宏。
- 将原始发现总结为 LaTeX 友好的评审意见，而不是切换到单独的表格格式。
