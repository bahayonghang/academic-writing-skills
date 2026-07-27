# Module: Expression Restructuring

**Trigger**: academic tone, 学术表达, improve writing, weak verbs

## Rules the script applies

Applied automatically (case is carried over from the source token):

| Pattern    | Replacement |
| ---------- | ----------- |
| `get`      | `obtain`    |
| `a lot of` | `many`      |

Reported as candidates, never auto-applied — the pattern is detectable but a rule cannot tell a weak use from a correct one:

| Pattern   | Why it stays a candidate                                                               |
| --------- | -------------------------------------------------------------------------------------- |
| `make`    | "Make sure", "make use of" — auto-replacing produced "develop sure" / "develop use of" |
| `very`    | "very few" — auto-replacing produced "highly few"                                      |
| `kind of` | Deleting it changes the meaning of "a kind of transformer"                             |

**Do not add `use → employ` or `show → demonstrate` back.** They were removed on purpose: the de-AI guide lists "we use ..." as correct academic English and "demonstrate the effectiveness" as an AI tell, so applying them made this module fight [deai.md](deai.md) (finding E15). A collocation exclusion list is not the fix either — `make sense`, `make up`, `make do`, `make it` are an open set, and every gap produces wrong English.

Protected tokens (statistics, values with units, model/dataset/gene names) are masked before substitution and listed under `Protected:`. Full classification: [protected-tokens.md](../writing/protected-tokens.md).

```bash
uv run python -B scripts/improve_expression.py main.tex
uv run python -B scripts/improve_expression.py main.tex --section related
uv run python -B scripts/improve_expression.py main.tex --goal clarity --strength moderate
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [routing-rules.md](routing-rules.md). `--goal coherence` has no rules here and routes to `logic`.

Output format:

```latex
% CONTRACT [Script]: goal=grammar strength=minimal
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
% Original: We get 92.1\% accuracy on CIFAR-100.
% Revised:  We obtain 92.1\% accuracy on CIFAR-100.
% Rationale: Weak verb replaced: \bget\b -> obtain
% Changed:       1 lexical substitution(s): get -> obtain
% Protected:     92.1\%, CIFAR-100
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    lexical-substitution
```

Candidate block (no `Revised:` line — the script refuses to guess):

```latex
% EXPRESSION (Line 31) [Severity: Minor] [Priority: P3] [Script]: Weak-expression candidate
% Original: Make sure the model converges.
% Candidate: weak verb "make" is context-dependent ("make sure", "make use of"); not auto-applied
% Changed:       none (candidate only: Make)
% Protected:     none
% Meaning-Check: NEEDS-LLM
% Risk-Flags:    not-assessed
```

This module emits replacement text, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`. Field definitions and the full `Risk-Flags` closed set: `references/modules/routing-rules.md`.

Do not raise claim strength while polishing. A verb swap that moves a hedged report toward a stronger assertion (`suggests` -> `demonstrates`, `may` -> `does`) is an over-claim, not a tone improvement: keep the original strength, or flag `Risk-Flags: overstatement` and say so explicitly. Criteria: [over-claim-guard.md](../evidence/over-claim-guard.md); the four-level reporting-verb ladder is in [style-guide.md](../writing/style-guide.md).

Style guide: [style-guide.md](../writing/style-guide.md)
