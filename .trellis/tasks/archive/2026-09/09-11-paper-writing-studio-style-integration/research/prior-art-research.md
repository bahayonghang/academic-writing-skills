# Prior-Art Research

- Researched at: 2026-09-11
- Queries: scientific academic writing style polishing agent skill; Nature IEEE Elsevier scholarly writing rewrite; venue aware academic writing editor; anti fabrication academic prose evaluation
- Catalogs: skills.sh via npx.cmd; SkillsMP via bundled client
- Rating evidence: unavailable. Installs and GitHub stars are adoption/attention signals, not quality ratings.

## Catalog and source notes

The unified runner could not start on Windows because it invokes npx rather than npx.cmd (FileNotFoundError: WinError 2). The underlying catalogs were queried separately with the Windows command name. This is a tooling limitation, not evidence about any candidate's quality. Candidate source files were not executed.

| Candidate / source | Observed signal | Relevant lesson | Decision |
|---|---:|---|---|
| yuan1z0825/nature-skills@nature-polishing (skills.sh) | 12.4K installs | Nature-specific routing is a popularity anchor, but it does not establish IEEE/Elsevier isolation or this output contract | adapt conceptually; do not copy |
| shining319/claude-code-single-person-workflow@academic-writing-style (skills.sh) | 311 installs | Adjacent academic-writing trigger vocabulary can inform boundary cases | reject as quality authority; source not inspected |
| affaan-m/ECC:scientific-thinking-scholar-evaluation (SkillsMP) | 253,169 repo stars | Repeatable evidence evaluation is complementary to prose rewriting | adapt evidence-led eval idea; source not executed |
| davila7/claude-code-templates:venue-templates (SkillsMP) | 30,563 repo stars | Venue selection should be explicit and separated from formatting/template concerns | keep boundary; formatting remains out of scope |
| K-Dense-AI/scientific-agent-skills:scientific-critical-thinking (SkillsMP) | 43,904 repo stars | Claim/evidence assessment is useful as an output check | adapt only as an eval, not a dependency |

## Keep / adapt / reject / invent

- Keep: Nature's section prompts, shared context and entity registry, calibrated hedge tiers, anti-fabrication traceability, deterministic em-dash scrub and dual output.
- Adapt: one root router with venue/journal/domain, profile-local load order, common section aliases and a summary recording profile version and evidence rows. IEEE and Elsevier self-reference and section-order rules remain local.
- Reject: direct TSV collation, default loading of all observations, treating installs/stars as ratings, adding a venue formatter or catalog installer and making Nature's Here we or methods-last universal.
- Invent: explicit selector precedence, conflict reporting, neutral unspecified profile, shared-invariant/profile-rule split and candidate/core plus degraded trigger/output cases.

## Missing evidence

No external candidate was fully reviewed for license, maintenance, permissions or runtime behavior; no cross-venue output comparison, provider run, clean installation, real-paper precision/recall or human editorial review exists yet.
