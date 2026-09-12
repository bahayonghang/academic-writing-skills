# Prior-Art Research

- Researched: 2026-09-11
- Local reference: ref/nature-writing-studio/skill
- Venue routing: profiles/ieee.json and profiles/elsevier.json
- External catalogs: skills.sh and SkillsMP; installs/stars are adoption signals, not quality ratings.

The bundled unified runner could not invoke Windows npx (it requires npx.cmd), so the catalogs were queried through npx.cmd and the bundled SkillsMP client. This limitation is recorded as missing evidence for unified-runner reproducibility.

## Adopted mechanisms

- Nature reference: section-specific loading, multi-section shared context, entity registry, calibrated evidence strength and deterministic em-dash handling. Adapted into the Nature profile and shared output contract.
- IEEE: per-section load order, core/candidate promotion boundary, Transactions self-reference and Related Work alternatives. Kept in profiles/ieee.json.
- Elsevier: domain-journal self-reference, core/statistical evidence gate and section routing. Kept in profiles/elsevier.json.
- Venue-template and scholarly-evaluation catalog candidates: explicit venue selection and repeatable evidence checks were useful adjacent mechanisms; their code was not executed or copied.

## Rejected mechanisms

- Directly concatenating Nature, IEEE and Elsevier TSV rows.
- Making Nature Here we, methods-last, IEEE self-reference or Elsevier self-reference global.
- Treating catalog installs or repository stars as ratings.
- Adding formatting, compilation, Zotero writes or catalog installation to this prose skill.

## Missing evidence

No provider-backed output comparison, real-paper precision/recall, clean isolated installation or human editorial review was run. Source candidate licenses, maintenance and runtime permissions were not fully audited; public quality claims remain unverified.
