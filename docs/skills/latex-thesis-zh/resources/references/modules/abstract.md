# Module: Abstract

**Trigger**: abstract, 摘要, abstract structure, 摘要结构, check abstract, polish abstract, abstract diagnosis, 润色摘要, abstract review

## Commands

```bash
uv run python -B scripts/analyze_abstract.py main.tex                       # thesis 骨架诊断（默认）
uv run python -B scripts/analyze_abstract.py main.tex --degree master       # 硕士字数阈值
uv run python -B scripts/analyze_abstract.py main.tex --bilingual           # + 中英摘要一致性
uv run python -B scripts/analyze_abstract.py main.tex --max-chars 1500      # 覆盖字数上界
uv run python -B scripts/analyze_abstract.py main.tex --model five --lang en --max-words 250
uv run python -B scripts/analyze_abstract.py main.tex --json
```

## Details

**Default `--model thesis`** diagnoses the **structural skeleton** of a Chinese degree-thesis
abstract: opening object-positioning sentence -> problem paragraph -> colon-ended overview
sentence -> numbered work paragraphs -> optional closing paragraph. See the “Degree-Thesis
Abstract Skeleton (thesis model)” section in `../writing/abstract-structure.md` for the 13 T-* checks.
Because this skill serves degree theses only, thesis is the default. `--model five` retains the
conference-paper **five-element model** (Background/Objective/Methods/Results/Conclusion) as a
fallback. The five-element model systematically produces false positives for doctoral abstracts,
such as judging Results MISSING when no number is present even though a compliant doctoral abstract
may close qualitatively.

**Length thresholds** align with the Yanshan rules constants in check_spec: `--degree doctor`
(default) requires 900-1200 Chinese characters, and `--degree master` requires 500-650. An explicit
`--max-chars` overrides the upper bound. Unit tests lock the constants in both locations together.

**Bilingual abstract consistency (`--bilingual`)**: in thesis mode, additionally compare the English
Abstract with the Chinese abstract. B-ORD (ordinal alignment), B-NUM (numeric-set consistency,
Error), B-ENUM (numbered-item count), and B-LEN (English abstract absent or too short) are [Script];
B-SEM (sentence-level semantic correspondence) is an [LLM] lane. **Tense/voice is not implemented
here**. The report footer routes to the `deai` module's English-abstract-gated tense check; deai traces
do not flow into this module.

For Chinese thesis writing, also check whether the abstract, innovation/contribution claims, and conclusion form a three-way closure. See `../writing/thesis-writing-guide.md`.

Thesis mode outputs each check code with level, evidence excerpt, and recommendation. `--model five`
outputs `PRESENT` / `VAGUE` / `MISSING` for each element.

Skill-layer response:
1. Format the diagnosis as a structured report with ✅ / ⚠️ / ❌ markers
2. Provide specific revision suggestions for VAGUE or MISSING elements
3. If the user requests polishing, generate a revised abstract with [REVISED: ...] annotations
4. Never fabricate data or add claims not in the original

Thesis-specific closure:

- Abstract: whether the research problem, method, results, and significance are complete.
- Innovations/main contributions: whether they agree with the methods and results in the abstract.
- Conclusion and outlook: whether they answer the contributions in the abstract and introduction and state limitation boundaries.

See also: [abstract-structure.md](../writing/abstract-structure.md) for the degree-thesis abstract
skeleton (thesis model) section (T-*/B-* checks) and the legacy five-element model with detection
heuristics. See [conclusion.md](conclusion.md) for conclusion-chapter content checks.
