# Module: Expression Restructuring

**Trigger**: academic tone, 学术表达, improve writing, weak verbs

Weak verb replacements:

- use → employ, utilize, leverage
- get → obtain, achieve, acquire
- make → construct, develop, generate
- show → demonstrate, illustrate, indicate

```bash
uv run python -B scripts/improve_expression.py main.tex
uv run python -B scripts/improve_expression.py main.tex --section related
```

Output format:

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

This module emits replacement text, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`. Field definitions and the full `Risk-Flags` closed set: `references/modules/routing-rules.md`.

Do not raise claim strength while polishing. A verb swap that moves a hedged report toward a stronger assertion (`suggests` -> `demonstrates`, `may` -> `does`) is an over-claim, not a tone improvement: keep the original strength, or flag `Risk-Flags: overstatement` and say so explicitly. Criteria: [over-claim-guard.md](../evidence/over-claim-guard.md); the four-level reporting-verb ladder is in [style-guide.md](../writing/style-guide.md).

Style guide: [style-guide.md](../writing/style-guide.md)
