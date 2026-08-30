# Subsection Context Protocol

This is the paper-audit mirror of the canonical subsection-context contract in
`academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`.
The marked block is synchronized by contract tests.

<!-- S-CTX-CONTRACT:BEGIN -->
## Subsection Context Contract

Subsection depth is defined as `depth = level - root_level + 1`, where `root_level` is the
minimum heading level in the document. Only `depth == 3` forms an `x.x.x` subsection unit.
There is no fallback without depth-3 headings: the unit list stays empty, a declaration is
emitted, and depth-2 headings do not substitute for subsections.

| Code | Reproducible signal | Manual review question |
| --- | --- | --- |
| `S-CTX-IN` | The opening paragraph of current has no inbound marker, and its endpoint Jaccard with the evidence-side closing sentence is strictly below `0.0200` | Does this subsection need to receive the preceding subsection's conclusion or output? |
| `S-CTX-OUT` | The closing paragraph of current has no prospective/closure marker, and the opening sentence of `next.head` has no back-reference marker | Does this subsection need to hand an input or question to the next subsection? |
| `S-CTX-ROLE` | The opening paragraph of current has no positioning marker and does not reuse a parent-title keyword | What role does this subsection play within its parent section `x.x`? |

Only current may receive rewrite suggestions; prev.tail, next.head, and parent_lead are read-only
and serve only as evidence.
<!-- S-CTX-CONTRACT:END -->
