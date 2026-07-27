# Module: Grammar Analysis

**Trigger**: grammar, proofread, article usage, tense, subject-verb agreement

**Purpose**: Run a lightweight, rule-based grammar pass on visible prose from an existing LaTeX/Typst document.

## Commands

```bash
uv run python -B scripts/analyze_grammar.py main.tex
uv run python -B scripts/analyze_grammar.py main.tex --section introduction
```

## Raw Script Output

The script emits reviewer-style comment blocks such as:

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

## Rewrite Contract

This module emits replacement text, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it is a proposal for the author to verify. Field definitions and the full `Risk-Flags` closed set: `references/modules/routing-rules.md`.

A grammar fix must never raise claim strength. Repairing a hedge into an assertion (`the results may indicate` -> `the results indicate`) is an over-claim disguised as a grammar fix: keep the original strength, or flag `Risk-Flags: overstatement`. Criteria: [over-claim-guard.md](../evidence/over-claim-guard.md); reporting-verb ladder in [style-guide.md](../writing/style-guide.md).

## Skill-Layer Response

- Keep the final answer source-aware and concise.
- Preserve equations, citations, labels, and macros.
- Summarize the raw findings as LaTeX-friendly review comments instead of switching to a separate table format.
