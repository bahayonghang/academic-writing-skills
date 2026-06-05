# Module: Abstract

**Trigger**: abstract, 摘要, abstract structure, 摘要结构, check abstract, polish abstract, abstract diagnosis, 润色摘要, abstract review

## Commands

```bash
uv run python -B scripts/analyze_abstract.py main.tex
uv run python -B scripts/analyze_abstract.py main.tex --lang en --max-words 250
uv run python -B scripts/analyze_abstract.py main.tex --lang zh --max-chars 300
uv run python -B scripts/analyze_abstract.py main.tex --json
```

## Details

Diagnoses five structural elements in the abstract: Background, Objective, Methods, Results, Conclusion.

For Chinese thesis writing, also check whether abstract, innovation/contribution claims, and conclusion form a three-way closure. See `../writing/thesis-writing-guide.md`.

Per-element output: `PRESENT` / `VAGUE` / `MISSING` with evidence quote and suggestion.

Also validates word count (EN) or character count (ZH) against configurable limits.

Skill-layer response:
1. Format the diagnosis as a structured report with ✅ / ⚠️ / ❌ markers
2. Provide specific revision suggestions for VAGUE or MISSING elements
3. If the user requests polishing, generate a revised abstract with [REVISED: ...] annotations
4. Never fabricate data or add claims not in the original

Thesis-specific closure:

- 摘要：研究问题、方法、结果、意义是否完整。
- 创新点/主要贡献：是否与摘要中的方法和结果一致。
- 总结与展望：是否回应摘要和绪论中的贡献，并给出局限边界。

See also: [abstract-structure.md](../writing/abstract-structure.md) for the full five-element model and detection heuristics.
