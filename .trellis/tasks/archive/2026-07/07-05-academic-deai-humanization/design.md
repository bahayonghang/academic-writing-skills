# Design

## Scope

This is an optimization of existing writing skills, not a new skill package.
The implementation should treat `renhua` as a reference for AI-flavored shells
and adapt the useful parts to academic writing.

Targets:

- `academic-writing-skills/latex-thesis-zh`
- `academic-writing-skills/typst-paper`
- `academic-writing-skills/latex-paper-en`

The task remains one Trellis task rather than a parent/child tree because the
deliverable is a single cross-skill de-AI contract. The implementation order can
still be staged internally, but final acceptance requires all three skills.

## Architecture

Keep the existing module-router architecture:

- `SKILL.md` stays compact and routes users to `deai`.
- Detailed de-AI guidance lives under each skill's `references/deai/` or
  `references/modules/` files.
- Scripted detections stay in each skill's `scripts/deai_check.py`.
- Evals stay under each skill's `evals/`; tests stay under `tests/`.

Do not create a shared helper unless the tri-skill implementation produces
obvious duplication that cannot be safely kept local. Language-specific
heuristics may remain in each `deai_check.py` even when they share category
names.

## Academic Humanization Contract

Add a reusable contract to de-AI docs:

1. Protect syntax first: citations, labels, refs, math, macros, Typst labels, and
   source layout are not rewrite targets by default.
2. Extract the academic payload:
   - facts/evidence: data, metrics, citations, tables, figures, experiments;
   - claims/stance: the paper's actual conclusion, uncertainty, method choice;
   - logic: paragraph role, section role, claim-evidence map;
   - boundaries: scope, assumptions, limitations, missing evidence.
3. Remove structure shells only after the payload is clear.
4. Prefer a rewrite blueprint over direct prose unless the user asks for prose.
5. Mark missing evidence as pending instead of inventing it.

## Pattern Design

For `latex-thesis-zh`, add conservative categories inspired by `renhua`:

- `binary_contrast_shell`: `不是 A，而是 B`, `不在于 A，而在于 B`,
  `不只是/不仅 A，更/还 B`.
  Suggestion: name the real comparison axis, evidence, and section role; keep it
  only if it carries a verifiable academic distinction.
- `fake_insight_marker`: `真正`, `其实`, `本质上`, `核心在于`, `关键在于`,
  `更重要的是`, `这说明`, `这背后`.
  Suggestion: remove the marker and state the evidence-backed claim directly.
- `lecture_colon`: `我的结论是：`, `原因很简单：`, `重点是：`, `分成三类：`.
  Suggestion: use a normal academic sentence or introduce a concrete inventory
  with a precise noun.
- `vague_referent`: `东西`, `这件事`, `这些`, `一类`, `几个方向` when the referent
  needs a research object, method, factor, result, or limitation.
  Suggestion: replace with the exact academic noun.
- `vague_comparative`: `更适合`, `更像`, `更自然`, `更高级` without an explicit
  comparison object or criterion.
  Suggestion: state the comparison baseline and evaluation criterion.
- `command_template_opening`: `别急着`, `先别`, `顺序别反了`, `记住这句话`.
  Suggestion: rewrite as an academic risk, procedure, or observation.

Wrong time stance is riskier in Chinese academic prose because future-tense markers
can be valid in chapter previews. Keep it as an LLM checklist item unless a precise
script predicate is found during implementation.

For `typst-paper`, implement the same Chinese/bilingual structure-shell categories
where they can be checked against visible prose without touching Typst syntax.
The script must keep current bilingual behavior and protect `@cite`, `<label>`,
math, code, and macros.

For `latex-paper-en`, implement English equivalents rather than translating the
Chinese phrase list directly:

- `binary_contrast_shell`: empty contrast scaffolds such as
  `not merely A, but B`, `not only A but also B`, or `rather than A, B` when
  they do not name a technical contrast, evidence, or baseline.
- `fake_insight_marker`: `essentially`, `in fact`, `the key is`, `it is important
  to note`, `more importantly` when they add framing without evidence.
- `lecture_colon`: `The conclusion is:`, `The reason is simple:`, `The key point is:`
  when a normal academic sentence would carry the claim.
- `vague_referent`: vague `this`, `things`, `aspects`, `factors` without a named
  research object or mechanism.

English fixes should preserve academic tone and claim-evidence mapping. They
should not force first-person public-writing voice.

## Output Contract

Findings should remain source-preserving:

```text
% DE-AI (file:line) [Severity] [Priority]: phrase-level or structure-shell issue
% Pattern: fake_insight_marker
% Suggestion: remove the marker, state the evidence-backed claim directly, and
% keep \cite{}, \ref{}, \label{}, math, and macros unchanged.
```

For prose proposals:

- Preserve all anchors and protected syntax.
- Do not add numbers, citations, baselines, experiments, or conclusions.
- When a better sentence requires evidence not present in the source, write
  `待补证` / `needs evidence` rather than fabricating it.

## Compatibility

- Existing command-line flags should remain valid.
- `--tier` behavior should remain opt-in; new categories can receive D2/D3/D5
  labels only when tier mode is active.
- Existing de-AI defaults should not become detector-evasion guidance.
- Documentation mirrors under `docs/` and `docs/zh/` must stay synchronized if
  source references are mirrored.

## Tradeoffs

Tri-skill tradeoff:

- Covering all three skills in one pass improves consistency for users who move
  between LaTeX thesis, LaTeX paper, and Typst paper workflows.
- The cost is a broader test matrix and higher false-positive risk, especially
  in English where contrast scaffolds can be legitimate rhetorical moves.

Implementation should therefore keep findings advisory and source-preserving,
with tests for legitimate contrast boundaries in every changed script.
