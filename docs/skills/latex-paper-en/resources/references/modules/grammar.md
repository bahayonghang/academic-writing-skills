# Module: Grammar Analysis

**Trigger**: grammar, proofread, article usage, tense, subject-verb agreement

**Purpose**: Run a lightweight, rule-based grammar pass on visible prose from an existing LaTeX/Typst document.

## Commands

```bash
uv run python -B scripts/analyze_grammar.py main.tex
uv run python -B scripts/analyze_grammar.py main.tex --section introduction
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [routing-rules.md](routing-rules.md). `--goal concision` routes to `sentences` and `--goal coherence` routes to `logic` — this module has no rules for either.

## Raw Script Output

The script emits reviewer-style comment blocks such as:

```latex
% CONTRACT [Script]: goal=grammar strength=minimal
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1] [Script]: Rule hit: \bwe propose method\b
% Original: We propose method for time series forecasting.
% Revised:  We propose a method for time series forecasting.
% Rationale: Grammar: Article missing before singular count noun.
% Changed:       1 rule-based correction (\bwe propose method\b)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    none
```

Rules match case-insensitively so acronyms elsewhere in the line (`BERT`) keep their shape, and the matched span keeps its own leading capitalization — an earlier version returned `we propose a method` for a sentence-initial match, which fixed one error by introducing another.

## Rewrite Contract

This module emits replacement text, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it is a proposal for the author to verify. Field definitions and the full `Risk-Flags` closed set: `references/modules/routing-rules.md`.

A grammar fix must never raise or lower claim strength. Repairing a hedge into an assertion (`the results may indicate` -> `the results indicate`) is an over-claim disguised as a grammar fix: keep the original strength, or flag `Risk-Flags: overstatement`. Criteria: [over-claim-guard.md](../evidence/over-claim-guard.md); reporting-verb ladder in [style-guide.md](../writing/style-guide.md). The rule runs both ways: adding a hedge, softening the author's own judgement, or narrowing the scope while fixing grammar is silent weakening — keep the original strength, or flag `Risk-Flags: understatement` (LLM layer only) and give the evidence reason. A claim stronger than its evidence is reported as an over-claim finding, not softened here. Full list and exceptions: [routing-rules.md](routing-rules.md) (Layer rules).

## Skill-Layer Response

- Keep the final answer source-aware and concise.
- Preserve equations, citations, labels, and macros.
- Summarize the raw findings as LaTeX-friendly review comments instead of switching to a separate table format.
