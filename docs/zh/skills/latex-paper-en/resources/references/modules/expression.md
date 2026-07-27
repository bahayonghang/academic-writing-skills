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
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
% Original: We use machine learning to get better results.
% Revised: We employ machine learning to achieve superior performance.
% Rationale: Replace weak verbs with academic alternatives
% Changed:       1 lexical substitution (get -> achieve)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    lexical-substitution
```

本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

润色时不得升高措辞强度。把留有余地的报告换成更强的断言（`suggests` → `demonstrates`、`may` → `does`）是过度声称，不是语气改善：保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [over-claim-guard.md](../evidence/over-claim-guard.md)；报告动词四级阶梯见 [style-guide.md](../writing/style-guide.md)。

风格指南：[style-guide.md](../writing/style-guide.md)

