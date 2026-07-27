# Module: Long Sentence Analysis

**Trigger**: long sentence, 长句, simplify, decompose, >50 words

Trigger condition: Sentences >50 words OR >3 subordinate clauses

```bash
uv run python -B scripts/analyze_sentences.py main.tex
uv run python -B scripts/analyze_sentences.py main.tex --section introduction --max-words 45 --max-clauses 3
uv run python -B scripts/analyze_sentences.py main.tex --strength moderate
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [routing-rules.md](routing-rules.md). Splitting a sentence is a structural edit, so under `--strength minimal` the proposal is still shown but the rationale says it needs `moderate` or higher before anyone applies it. `--goal coherence` routes to `logic`.

Output format:

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

## Rewrite Contract

This module emits a concrete `Suggested:` sentence, so the rewrite contract applies. The field name stays `Suggested:` (it is a proposal, not an applied edit) and the four contract fields are appended after it. `[Script]` output always carries `Meaning-Check: NEEDS-LLM`, and `not-assessed` is its normal `Risk-Flags` value because splitting a sentence is exactly where meaning drifts unnoticed. Only the `[LLM]` layer may propose `PRESERVED`. Field definitions and the full `Risk-Flags` closed set: `references/modules/routing-rules.md`.

Splitting must not raise claim strength or invent a connective the source does not support. Turning a bare sequence into a causal chain (`we did X; Y improved` -> `Y improved because of X`) adds a claim: keep the original relation, or flag `Risk-Flags: overstatement`. Criteria: [over-claim-guard.md](../evidence/over-claim-guard.md).
