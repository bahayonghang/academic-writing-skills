# 模块：长句分析

**触发**：长句、long sentence、简化、拆解、>50 个单词

触发条件：句子超过 50 词，或从句超过 3 个

```bash
uv run python -B scripts/analyze_sentences.py main.tex
uv run python -B scripts/analyze_sentences.py main.tex --section introduction --max-words 45 --max-clauses 3
uv run python -B scripts/analyze_sentences.py main.tex --strength moderate
```

`--goal`（默认 `grammar`）与 `--strength`（默认 `minimal`）声明编辑范围，见 [routing-rules.md](routing-rules.md)。拆句属结构性编辑，因此在 `--strength minimal` 下建议仍然给出，但理由行会注明需要 `moderate` 及以上才可应用。`--goal coherence` 路由到 `logic`。

输出格式：

```latex
% CONTRACT [Script]: goal=grammar strength=minimal
% LONG SENTENCE (Line 45, 67 words, 5 clauses) [Severity: Minor] [Priority: P2] [Script]
% Original: [full sentence]
% Suggested: [simplified version]
% Rationale: Sentence exceeds complexity threshold, split for readability. Applying the split needs --strength moderate or higher.
% Changed:       none (split proposal only; source not rewritten)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

## 改写契约

本模块产出具体的 `Suggested:` 句子，适用改写契约。字段名保持 `Suggested:`（它是提案而非已应用的编辑），四个契约字段追加其后。`[Script]` 层恒为 `Meaning-Check: NEEDS-LLM`，而 `not-assessed` 是它常态的 `Risk-Flags` 取值——拆句正是语义最容易悄悄漂移的地方。只有 `[LLM]` 层可提出 `PRESERVED`。字段定义与 `Risk-Flags` 闭集见 `references/modules/routing-rules.md`。

拆句不得升高措辞强度，也不得凭空补上原文不支持的连接关系。把并列陈述变成因果链（`we did X; Y improved` -> `Y improved because of X`）等于新增论断：保持原有关系，或置 `Risk-Flags: overstatement`。判据见 [over-claim-guard.md](../evidence/over-claim-guard.md)。
