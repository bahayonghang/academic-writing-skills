# Module: Analysis of long and difficult sentences

**Trigger words**: long sentence, long sentence, simplify, decompose, dismantle

**Script Usage**:

```bash
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --max-words 50 --max-clauses 3
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction
```

> Available flags: `--section`, `--max-words` (default 50), `--max-clauses` (default 3),
> `--goal` (default `grammar`), `--strength` (default `minimal`). There is no `--threshold`.

`--goal` and `--strength` declare the edit envelope; see [skill-routing-notes.md](../skill-routing-notes.md). Splitting a sentence is a structural edit, so under `--strength minimal` the proposal is still shown but the rationale notes that applying it needs `moderate` or higher; `--goal coherence` routes to `logic`.

**Trigger conditions**:

- Sentence word count > `--max-words` (default 50) or number of clauses > `--max-clauses` (default 3)
- Sentence segmentation and counting are based on English (split on `.!?`, length counted in words)

**Output format**:

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

**Rewrite contract**: this module emits a concrete `Suggested:` sentence, so the rewrite contract applies. The field name stays `Suggested:` (it is a proposal, not an applied edit) and the four contract fields are appended after it. `[Script]` output always carries `Meaning-Check: NEEDS-LLM`, and its normal `Risk-Flags` value is `not-assessed` — splitting a sentence is exactly where meaning drifts unnoticed. Only the `[LLM]` layer may propose `PRESERVED`. Field definitions and the `Risk-Flags` closed set: `references/skill-routing-notes.md`.

**Never raise claim strength or invent a connective**: turning a plain sequence into a causal chain (`we did X; Y improved` → `Y improved because of X`) adds a claim. Keep the original relation, or set `Risk-Flags: overstatement`. Criteria: [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md).

**Split Strategy**:

1. Identify the backbone structure
2. Extract modification ingredients
3. Split into short sentences
4. maintain logical coherence
