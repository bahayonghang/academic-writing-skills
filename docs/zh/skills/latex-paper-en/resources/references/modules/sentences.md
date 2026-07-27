# 模块：长句分析

**触发**：长句、长句、简化、分解、>50 个单词

触发条件：句子>50字或>3个从句

```bash
uv run python -B scripts/analyze_sentences.py main.tex
uv run python -B scripts/analyze_sentences.py main.tex --section introduction --max-words 45 --max-clauses 3
```

输出格式：
```latex
% LONG SENTENCE (Line 45, 67 words) [Severity: Minor] [Priority: P2] [Script]
% Core: [subject + verb + object]
% Subordinates:
%   - [Relative] which...
%   - [Purpose] to...
% Suggested: [simplified version]
% Changed:       split proposal only; source not rewritten
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

## 改写契约

本模块产出具体的 `Suggested:` 句子，适用改写契约。字段名保持 `Suggested:`（它是提案而非已应用的编辑），四个契约字段追加其后。`[Script]` 层恒为 `Meaning-Check: NEEDS-LLM`，而 `not-assessed` 是它常态的 `Risk-Flags` 取值——拆句正是语义最容易悄悄漂移的地方。只有 `[LLM]` 层可提出 `PRESERVED`。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

拆句不得升高措辞强度，也不得凭空补上原文不支持的连接关系。把并列陈述变成因果链（`we did X; Y improved` → `Y improved because of X`）等于新增论断：保持原有关系，或置 `Risk-Flags: overstatement`。判据见 [over-claim-guard.md](../evidence/over-claim-guard.md)。

