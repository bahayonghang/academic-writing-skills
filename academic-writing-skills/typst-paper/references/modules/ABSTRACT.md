# Module: Abstract

**Trigger**: abstract, 摘要, abstract structure, 摘要结构, check abstract, polish abstract, abstract diagnosis, 润色摘要, abstract review

## Commands

```bash
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --lang en --max-words 250
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --lang zh --max-chars 300
uv run python -B $SKILL_DIR/scripts/analyze_abstract.py main.typ --json
```

## Details

Diagnoses five structural elements in the abstract: Background, Objective, Methods, Results, Conclusion.

Per-element output: `PRESENT` / `VAGUE` / `MISSING` with evidence quote and suggestion.

Also validates word count (EN, `--max-words`) or character count (ZH, `--max-chars`) against the configured limits. Language is auto-detected unless `--lang {en,zh,auto}` is given. Abstract extraction supports `#abstract[..]`, `#show: ieee.with(abstract: [..])`, and an `= Abstract` / `= 摘要` heading.

Skill-layer response:

1. Format the diagnosis as a structured report with ✅ / ⚠️ / ❌ markers
2. Provide specific revision suggestions for VAGUE or MISSING elements
3. If the user requests polishing, generate a revised abstract with [REVISED: ...] annotations
4. Never fabricate data or add claims not in the original

See also: [ABSTRACT_STRUCTURE.md](../ABSTRACT_STRUCTURE.md) for the full five-element model and detection heuristics.
