# Creation Handoff

## Result

- Skill: paper-writing-studio 0.1.0
- Job: route academic prose polishing to an explicit Nature, IEEE, Elsevier or neutral profile while preserving evidence-bearing tokens.
- Path: academic-writing-skills/paper-writing-studio
- Publication: not requested; local package only.

## Reference skills studied

- ref/nature-writing-studio/skill: local source studied for section prompts, anti-fabrication, multi-section context and output shape.
- profiles/ieee.json: Transactions section routes and core/candidate evidence gates.
- profiles/elsevier.json: domain-journal routes and evidence-gate provenance.

External catalog results were used only as adjacent discovery. They were not treated as inspected reference skills or copied.

## Absorbed and rejected

- Keep: traceable output, protected tokens, calibrated claims, per-section loading and explicit provenance.
- Adapt: one selector with explicit venue/journal/domain precedence and a neutral fallback.
- Reject: merged TSV corpora, global venue slogans, formatting/compiler behavior and unverified quality claims.
- Invent: conflict reporting, profile isolation metadata and a common degraded/missing-evidence output shape.

## Advantages and limits

- [design advantage] The package makes venue selection and cross-profile isolation explicit in profiles/*.json and the normalized summary.
- [validated advantage] Trigger eval passes 15/15 cases; the output-contract eval passes 6/6 recorded fixtures covering precedence, aliases, candidate gates, protected tokens, anti-AI/degraded traces and compact output.
- [hypothesis] Profile-local routing should reduce accidental style leakage; provider-backed cross-venue comparison is missing evidence.

## Verification

Package validation, trigger evaluation, output-contract evaluation and Skill IR are local structural or recorded-fixture evidence only. Provider output, human editorial acceptance, real-paper quality, blind review and isolated installation remain missing evidence. The docs resource manifest has no entry for this package because it ships no public `references/`, `templates/`, `examples/` or Markdown `agents/` resources.
