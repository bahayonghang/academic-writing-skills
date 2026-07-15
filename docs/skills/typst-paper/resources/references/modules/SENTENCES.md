# Module: Analysis of long and difficult sentences
**Trigger words**: long sentence, long sentence, simplify, decompose, dismantle

**Script Usage**:
```bash
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --max-words 50 --max-clauses 3
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction
```

> Available flags:`--section`、`--max-words`(default 50),`--max-clauses`(default 3).
> No `--threshold`.

**Trigger conditions**:
- Sentence word count >`--max-words`(default 50) or number of clauses >`--max-clauses`(default 3)
- Sentence segmentation and counting are based on English (segment according to `.!?` and count according to word length)

**Output format**:
```typst
// LONG SENTENCE (Line 45, 67 words, 5 clauses) [Severity: Minor] [Priority: P2]
// Original: ...
// Suggested: ...
// Rationale: Sentence exceeds complexity threshold, split for readability.
```

**Split Strategy**:
1. Identify the backbone structure
2. Extract modification ingredients
3. Split into short sentences
4. maintain logical coherence

