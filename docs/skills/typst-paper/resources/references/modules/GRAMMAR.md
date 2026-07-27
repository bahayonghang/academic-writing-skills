# Module: Syntax Analysis (English)

**Trigger words**: grammar, grammar, proofread, polish, article usage

**Script Usage**:

```bash
uv run python ../scripts/analyze_grammar.py main.typ
uv run python ../scripts/analyze_grammar.py main.typ --section introduction
```

**Key inspection areas**:

- subject-verb agreement
- Article usage (a/an/the)
- Tense consistency (method in past tense, result in present tense)
- Chinglish detection

**Output format**:

```typst
// GRAMMAR（第23行）[Severity: Major] [Priority: P1] [Script]: 冠词缺失
// 原文：We propose method for...
// 修改后：We propose a method for...
// 理由：单数可数名词前缺少不定冠词
// Changed:       1 article insertion (propose method -> propose a method)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    none
```

**Rewrite contract**: this module emits text that can directly replace the source, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and may set only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it stays a proposal for the author to verify. Field definitions and the `Risk-Flags` closed set: `references/skill-routing-notes.md`.

**Never raise claim strength**: "repairing" a hedge into an assertion (`the results may indicate` → `the results indicate`) is an over-claim wearing a grammar-fix disguise. Keep the original strength, or set `Risk-Flags: overstatement`. Criteria: [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md).

**Common Grammar Errors**:

| error type                 | Example                          | Correction                      |
| -------------------------- | -------------------------------- | ------------------------------- |
| Missing article            | propose method                   | propose a method                |
| subject-verb inconsistency | The data shows                   | The data show                   |
| Tense confusion            | We proposed... The results shows | We proposed... The results show |
| Chinglish                  | more and more                    | increasingly                    |

Reference: [COMMON_ERRORS.md](../COMMON_ERRORS.md),[STYLE_GUIDE.md](../STYLE_GUIDE.md)
