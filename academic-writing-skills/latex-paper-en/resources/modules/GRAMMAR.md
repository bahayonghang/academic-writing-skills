# Module: Grammar Analysis

**Trigger**: grammar, 语法, proofread, 润色, article usage

Focus areas:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency (past for methods, present for results)
- Chinglish detection → See [COMMON_ERRORS.md](../references/COMMON_ERRORS.md)

```bash
python scripts/analyze_grammar.py main.tex
python scripts/analyze_grammar.py main.tex --section introduction
```

**Usage**: Script outputs rule-based grammar suggestions in diff-comment style.

**Output format** (Markdown comparison table):
```markdown
| Original | Revised | Issue Type | Rationale |
|----------|---------|------------|-----------|
| We propose method for time series forecasting. | We propose a method for time series forecasting. | Grammar: Article missing | Singular count noun requires indefinite article "a" |
| The data shows significant improvement. | The data show significant improvement. | Grammar: Subject-verb agreement | "Data" is plural, requires "show" not "shows" |
| This approach get better results. | This approach achieves superior performance. | Grammar + Expression | Verb agreement error; replace weak verb "get" with academic alternative |
```

**Alternative format** (for inline comments in source):
```latex
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1]: Article missing
% Original: We propose method for...
% Revised: We propose a method for...
% Rationale: Missing indefinite article before singular count noun
```
