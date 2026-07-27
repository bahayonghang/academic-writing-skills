# 模块：长难句分析

**触发词**: long sentence, 长句, simplify, decompose, 拆解

**脚本用法**:

```bash
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --max-words 50 --max-clauses 3
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction
```

> 可用 flag：`--section`、`--max-words`（默认 50）、`--max-clauses`（默认 3）、
> `--goal`（默认 `grammar`）、`--strength`（默认 `minimal`）。没有 `--threshold`。

`--goal` 与 `--strength` 声明编辑范围，见 [skill-routing-notes.md](../skill-routing-notes.md)。拆句属结构性编辑，因此在 `--strength minimal` 下建议仍然给出，但理由行会注明需要 `moderate` 及以上才可应用；`--goal coherence` 路由到 `logic`。

**触发条件**:

- 句子词数 > `--max-words`（默认 50） 或 从句数 > `--max-clauses`（默认 3）
- 句切分与计数以英文为准（按 `.!?` 切句、按词计长）

**输出格式**:

```typst
// CONTRACT [Script]: goal=grammar strength=minimal
// LONG SENTENCE (Line 45, 67 words, 5 clauses) [Severity: Minor] [Priority: P2] [Script]
// Original: ...
// Suggested: ...
// Rationale: Sentence exceeds complexity threshold, split for readability. Applying the split needs --strength moderate or higher.
// Changed:       none (split proposal only; source not rewritten)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    not-assessed
```

**改写契约**：本模块产出具体的 `Suggested:` 句子，适用改写契约。字段名保持 `Suggested:`（它是提案而非已应用的编辑），四个契约字段追加其后。`[Script]` 层恒为 `Meaning-Check: NEEDS-LLM`，`Risk-Flags` 常态为 `not-assessed`——拆句正是语义最容易悄悄漂移的地方。只有 `[LLM]` 层可提出 `PRESERVED`。字段定义与 `Risk-Flags` 闭集见 `references/skill-routing-notes.md`。

**不得升高措辞强度或凭空补连接关系**：把并列陈述拆成因果链（`we did X; Y improved` → `Y improved because of X`）等于新增论断。保持原有关系，或置 `Risk-Flags: overstatement`。判据见 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

**拆分策略**:

1. 识别主干结构
2. 提取修饰成分
3. 拆分为多个短句
4. 保持逻辑连贯性
