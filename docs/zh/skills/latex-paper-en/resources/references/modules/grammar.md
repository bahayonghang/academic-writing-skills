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
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1] [Script]: Rule hit: \bwe propose method\b
% Original: We propose method for time series forecasting.
% Revised:  we propose a method for time series forecasting.
% Rationale: Grammar: Article missing before singular count noun.
% Changed:       1 article insertion (propose method -> propose a method)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    none
```

## 改写契约

本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

语法修复不得升高措辞强度。把留有余地的表述"修"成断言（`the results may indicate` → `the results indicate`）是披着语法修复外衣的过度声称：保持原强度，或置 `Risk-Flags: overstatement`。判据见 [over-claim-guard.md](../evidence/over-claim-guard.md)；报告动词四级阶梯见 [style-guide.md](../writing/style-guide.md)。

## 技能层响应

- 保持最终答案的源头意识和简洁。
- 保留方程、引文、标签和宏。
- 将原始发现总结为 LaTeX 友好的评审意见，而不是切换到单独的表格格式。
