# AI-Disclosure Policy (Venue Placement)

Moved verbatim from `SKILL.md` Safety Boundaries; this wording is deliberate (CL-3/CL-4
disclosure-consistency decision) — do not reword.

> This skill produces AI-assisted text. Before submitting, verify the target venue's AI-disclosure policy: ICMJE (Jan 2026) and several publishers (Science/AAAS, NEJM, APS) require generative-AI use to be disclosed **in the cover letter**, while IEEE / ACM / Elsevier / Springer place that disclosure in the manuscript. The `presubmission` declaration check flags a missing `ai_disclosure` for venues that require it, but the author remains responsible for confirming the current policy.

Related: `align-check` cross-checks AI-disclosure consistency between the letter and the
manuscript (see `MODE_GUIDE.md`, Mode 3, step 6) — if one document discloses generative-AI
use (or non-use) and the other is silent, or the two contradict on polarity, it emits a
`moderate` `disclosure_consistency` finding.
