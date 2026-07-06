# Module: De-AI Editing

**Trigger**: deai, humanize, reduce AI traces, natural writing, tone cleanup

**Purpose**: Detect likely AI-writing traces in visible prose while preserving LaTeX structure and technical claims.

## Commands

```bash
uv run python -B scripts/deai_check.py main.tex --section introduction
uv run python -B scripts/deai_check.py main.tex --analyze
uv run python -B scripts/deai_batch.py main.tex --all-sections
```

## Raw Script Output

- `deai_check.py` emits section-level analysis, trace scores, and optional fix suggestions.
- `deai_batch.py` supports broader batch inspection across sections.
- The `tense` category (`[Script]` LOW) flags present-tense reporting verbs in Methods / Experiments / Results, gated to those sections; see [tense-guide.md](tense-guide.md).
- The `overclaim` category (`[Script]` LOW) flags unambiguous causal / firstness / universality phrasing; see [over-claim-guard.md](../evidence/over-claim-guard.md).

## Skill-Layer Response

- Treat the script output as analysis, not as permission to rewrite the paper by default.
- Return `% DE-AI ...` style findings or a short risk summary unless the user explicitly asks for source edits.
- Preserve `\cite{}`, `\ref{}`, `\label{}`, custom macros, and math environments.
- Never invent new claims, metrics, baselines, or references while smoothing the prose.

## Claim-Evidence-First Humanization

Before reducing AI tone, preserve the academic payload:

- **Facts/evidence**: numbers, datasets, experiments, figures, tables, citations, equations, and metrics.
- **Claims/stance**: the paper's real contribution, uncertainty, design choice, and limitation.
- **Logic**: paragraph role, section role, and claim-evidence map.
- **Boundaries**: assumptions, scope, missing evidence, and unsupported claims.

Only then remove rhetorical scaffolds such as `not merely A, but B`, `essentially`, `the key is`, `The conclusion is:`, or vague `this/things/factors`. Keep a contrast when it names a real baseline, criterion, and evidence; otherwise state the claim directly. The module should not promise lower detector scores or replace venue AI-use disclosure.

## Disclosure obligation (read before de-AI editing)

This module improves readability; it does **not** remove a disclosure obligation.
If an LLM had a non-trivial role in producing the paper, the target venue may
require you to disclose it (in a dedicated section, a checklist, the
acknowledgements, or the cover letter). See
[ai-disclosure.md](../venues/ai-disclosure.md) for the per-venue policy matrix.
Do not treat "reducing AI traces" as a substitute for required disclosure.

Reference: [guide.md](../deai/guide.md)

## Graded mode (`--tier`) and D1-D5 dimensions

`--tier {light|medium|heavy}` is **opt-in**. Without it, the default output is exactly as before. When present, it:

- **scales thresholds** — `light` flags fewer items (looser caps), `heavy` flags more (stricter caps); `medium` keeps the current thresholds;
- **enables the D1 sentence-length check** — flags sections whose sentence-length coefficient of variation is suspiciously low (machine-even cadence);
- **labels every finding with its AIGC dimension** D1-D5 and attaches a one-line teaching note (why detectors flag the pattern).

```bash
uv run python -B scripts/deai_check.py main.tex --analyze --tier heavy
```

The five dimensions are readability-oriented, **not** tuned to evade any specific detector: D1 sentence-length variety, D2 paragraph structure, D3 information density, D4 connector frequency, D5 term-context matching. Thresholds (including `sentence_length.cv_threshold`) remain overridable via `references/deai/tone-thresholds.yaml`.
