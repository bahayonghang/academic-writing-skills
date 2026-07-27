# Module: Academic Expression

**Trigger words**: academic tone, academic expression, improve writing, weak verbs

**Script Usage**:

```bash
uv run python ../scripts/improve_expression.py main.typ
uv run python ../scripts/improve_expression.py main.typ --section methods
uv run python ../scripts/improve_expression.py main.typ --goal clarity --strength moderate
```

`--goal` (default `grammar`) and `--strength` (default `minimal`) declare the edit envelope; see [skill-routing-notes.md](../skill-routing-notes.md). `--goal coherence` has no rules here and routes to `logic`.

**Replacements the script applies automatically** (case is carried over from the source token):

| weak verb / phrase | replacement |
| ------------------ | ----------- |
| get                | obtain      |
| a lot of           | many        |

**Reported as candidates, never auto-applied** (the pattern is detectable, but a rule cannot tell a misuse from a correct use):

| pattern | why it stays a candidate                                                               |
| ------- | -------------------------------------------------------------------------------------- |
| make    | "Make sure", "make use of" — auto-replacing produced "develop sure" / "develop use of" |
| very    | "very few" — auto-replacing produced "highly few"                                      |
| kind of | Deleting it changes the meaning of "a kind of transformer"                             |

**Do not add `use → employ` or `show → demonstrate` back**: they were removed on purpose. The de-AI guide lists "we use ..." as correct academic English and "demonstrate the effectiveness" as an AI tell, so applying them made this module fight [DEAI.md](DEAI.md) (finding E15). A collocation exclusion list is not the fix either — `make sense`, `make up`, `make do`, `make it` are an open set, and every gap produces wrong English.

Protected tokens (statistics, values with units, model/dataset/gene names) are masked before substitution and listed under `Protected:`. Full classification: [PROTECTED_TOKENS.md](../PROTECTED_TOKENS.md).

**Chinese academic expression**:

| colloquial        | academic                       |
| ----------------- | ------------------------------ |
| Many studies show | A large body of research shows |
| works very well   | has significant advantages     |
| we use            | this paper adopts              |
| It can be seen    | It follows that                |

**How to use**: the user supplies the paragraph source; the agent analyses it and returns the polished version plus a comparison table.

**Output format** (Markdown comparison table):

```markdown
| Original / 原文 | Revised / 改进版本 | Issue Type / 问题类型 | Rationale / 优化理由 |
|-----------------|---------------------|----------------------|---------------------|
| We get better results. | We obtain better results. | Weak verb | Replace "get" -> "obtain" for academic tone |
```

**Alternative format** (comments in source code — what the script actually emits):

```typst
// CONTRACT [Script]: goal=grammar strength=minimal
// EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
// Original: We get 92.1% accuracy on CIFAR-100.
// Revised:  We obtain 92.1% accuracy on CIFAR-100.
// Rationale: Weak verb replaced: \bget\b -> obtain
// Changed:       1 lexical substitution(s): get -> obtain
// Protected:     92.1%, CIFAR-100
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    lexical-substitution
```

**Candidate block** (no `Revised:` line — the script refuses to guess):

```typst
// EXPRESSION (Line 31) [Severity: Minor] [Priority: P3] [Script]: Weak-expression candidate
// Original: Make sure the model converges.
// Candidate: weak verb "make" is context-dependent ("make sure", "make use of"); not auto-applied
// Changed:       none (candidate only: Make)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    not-assessed
```

**Rewrite contract**: this module emits text that can directly replace the source, so the rewrite contract applies. `[Script]` output always carries `Meaning-Check: NEEDS-LLM` and may set only the rule-determinable flags (`none`, `not-assessed`, `lexical-substitution`, `whitespace-normalized`); only the `[LLM]` layer may propose `PRESERVED`, and even then it stays a proposal for the author to verify. Field definitions and the `Risk-Flags` closed set: `references/skill-routing-notes.md`.

**Never raise claim strength**: swapping a hedged statement for a stronger assertion (`suggests` → `demonstrates`, `可能` → `能够`) is an over-claim, not a tone improvement. Keep the original strength, or set `Risk-Flags: overstatement` and say so explicitly. Criteria: [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md).

Reference: [STYLE_GUIDE.md](../STYLE_GUIDE.md)
