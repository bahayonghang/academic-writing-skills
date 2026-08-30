# Subsection Context Interfaces in Chinese Theses

This guide defines the subsection cursor, cross-heading interface observations, and read-only
windows for `analyze_logic.py --subsection-context`. These observations only open manual review
entry points; they never rewrite thesis prose automatically.

<!-- S-CTX-CONTRACT:BEGIN -->
## Subsection Context Contract

Subsection depth is defined as `depth = level - root_level + 1`, where `root_level` is the minimum
heading level in the document; only `depth == 3` forms an `x.x.x` subsection unit. When depth-3 is
absent, do not fall back: return an empty unit list and one declaration instead of substituting a
depth-2 heading for a subsection.

| Code | Recomputable signal | Manual review question |
| --- | --- | --- |
| `S-CTX-IN` | The first current paragraph has no inbound marker, and its endpoint Jaccard against the evidence-side last sentence is strictly below `0.0200` | Does this subsection need to inherit the previous subsection's conclusion or output? |
| `S-CTX-OUT` | The last current paragraph has no prospective/closing marker, and the first sentence of `next.head` has no back-reference marker | Does this subsection need to hand an input or question to the next subsection? |
| `S-CTX-ROLE` | The first current paragraph has no locating marker and reuses no parent-title keyword | What role does this subsection play under parent section `x.x`? |

Only current may produce rewrite suggestions; prev.tail, next.head, and parent_lead are always
read-only evidence.
<!-- S-CTX-CONTRACT:END -->

## Eligible Paragraphs and Missing-Part Semantics

`SUBSECTION_CONTEXT_MIN_HAN = 20` is a constructive lower bound: a subsection entrance is often a
one- or two-sentence locating passage, so reusing `PARAGRAPH_ARC_MIN_HAN = 40` would systematically
drop valid interfaces; fragments below 20 Chinese characters are too small to carry a stable
inbound, handoff, or locating role. Chinese characters must also make up at least `0.30` of visible
text.

The checker intentionally does not reuse `_arc_is_eligible`. Its only structural difference is
that subsection context keeps `is_heading_lead`, because the first eligible paragraph after a
heading is exactly the `current` and `next.head` observation target. List items, paragraphs ending
at protected environments, and abstract, conclusion, acknowledgment, appendix, organization, and
summary scopes remain excluded.

When an adjacent unit exists but has no eligible paragraph, its part stays out of `read_only`, is
marked `no_eligible_paragraph`, and findings that depend on that side are suppressed. When a
document has no depth-3 heading, the declaration is fixed as:

```text
% 小节级：本文档无 depth-3 标题，未产出小节级观察。
```

## Commands and Windows

```bash
uv run python scripts/analyze_logic.py main.tex --subsection-context
uv run python scripts/analyze_logic.py main.tex --subsection-context --subsection 2.1.1
uv run python scripts/analyze_logic.py main.tex --emit-window --subsection 2.1.1
```

`--emit-window` prints only part names, source files, file-local lines, and editable/read-only
markers; it never copies prose. Multi-file theses are assembled through `tex_loader.py` first, then
assembled lines are mapped back to real source files such as `chapters/*.tex`.
