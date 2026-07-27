# Module: Syntax Analysis (English)

**Trigger words**: grammar, grammar, proofread, polish, article usage

**Script Usage**:

```bash
uv run python ../scripts/analyze_grammar.py main.typ
uv run python ../scripts/analyze_grammar.py main.typ --section introduction
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [skill-routing-notes.md](../skill-routing-notes.md). `--goal concision` routes to `sentences` and `--goal coherence` routes to `logic` — this module has no rules for either.

**Key inspection areas**:

- subject-verb agreement
- Article usage (a/an/the)
- Tense consistency (method in past tense, result in present tense)
- Chinglish detection

**Output format** (what the script actually emits):

```typst
// CONTRACT [Script]: goal=grammar strength=minimal
// GRAMMAR (Line 23) [Severity: Major] [Priority: P1] [Script]: Rule hit: \bwe propose method\b
// Original: We propose method for time series forecasting.
// Revised:  We propose a method for time series forecasting.
// Rationale: Grammar: Article missing before singular count noun.
// Changed:       1 rule-based correction (\bwe propose method\b)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    none
```

Rules match case-insensitively so acronyms elsewhere in the line (`BERT`) keep their shape, and the matched span keeps its own leading capitalization — an earlier version returned `we propose a method` for a sentence-initial match, fixing one error while introducing another.

**Rewrite contract**: this module emits text that can directly replace the source, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and may set only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it stays a proposal for the author to verify. Field definitions and the `Risk-Flags` closed set: `references/skill-routing-notes.md`.

**Never raise claim strength**: "repairing" a hedge into an assertion (`the results may indicate` → `the results indicate`) is an over-claim wearing a grammar-fix disguise. Keep the original strength, or set `Risk-Flags: overstatement`. Criteria: [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md).

**Common Grammar Errors**:

| error type                 | Example                          | Correction                      |
| -------------------------- | -------------------------------- | ------------------------------- |
| Missing article            | propose method                   | propose a method                |
| subject-verb inconsistency | The data shows                   | The data show                   |
| Tense confusion            | We proposed... The results shows | We proposed... The results show |
| Chinglish                  | more and more                    | increasingly                    |

Reference: [COMMON_ERRORS.md](../COMMON_ERRORS.md), [STYLE_GUIDE.md](../STYLE_GUIDE.md)
