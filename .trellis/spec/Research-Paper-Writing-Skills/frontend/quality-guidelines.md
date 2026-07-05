# Quality Guidelines

Quality in this repo means reviewer-facing clarity and evidence alignment.

Local patterns:

- The first sentence of each paragraph should state the paragraph message.
- Each paragraph should carry one message only.
- Section guides should expose the logic before the example text.
- The paper-review guide's checklist should be used as a revision gate, not a
  postscript.
- Claims in Abstract and Introduction must be supportable by evidence.
- De-AI or humanization guidance must preserve the academic payload before
  changing tone: facts/evidence, author stance, paragraph/section logic, and
  boundaries. It should default to findings, risk notes, or rewrite blueprints;
  prose rewrites require an explicit user request.

Academic de-AI examples:

- Good: "Remove the `not merely A but B` scaffold only after naming the real
  baseline, criterion, and evidence."
- Bad: "Rewrite the paragraph to sound less AI-generated" with no
  claim-evidence map or source-anchor preservation.

Reference files:

- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/introduction.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/method.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/paper-review.md`

Avoid:

- Generic polishing language with no technical anchor.
- A paragraph that cannot be mapped back to the outline.
- Claims that are stronger than the experimental evidence.
