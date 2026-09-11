# Design

## Boundary and ownership

`academic-writing-skills/paper-writing-studio/` owns the unified router, profile contract, output normalization, eval fixtures and public documentation. `ref/nature-writing-studio/`, `materials/IEEE/` and `materials/Elsevier/` remain read-only source packages. The router may reference stable relative paths or copy only small adapter metadata when packaging requires it; it must not duplicate corpus rows or mutate source provenance.

## Layered model

`input_text + target + venue? + journal? + domain?
             |
             v
venue selector: explicit venue > journal allowlist > domain map > unspecified
             |
             v
section alias map -> profile-local load plan
             |
             +--> shared invariants: traceability, protected tokens, calibrated evidence, degraded
             |
             +--> nature profile: Nature prompts/TSV/cross-section rules
             +--> ieee profile: IEEE references + core/statistical gates
             +--> elsevier profile: Elsevier references + core/statistical gates
             +--> unspecified profile: neutral scholarly baseline, no venue-specific priors
             |
             v
text + text_compact + summary(venue/profile/evidence/degraded)`

The selector is a deterministic adapter, not a confidence-scoring rule engine. A journal allowlist is valid only when the source material explicitly owns it. A domain heuristic may select a profile only for an unambiguous mapping; otherwise it returns `unspecified` and records the missing evidence.

## Contracts

### Input

`yaml
input_text: string
target: abstract | introduction | related_work | methods | method | results | experiments | discussion | conclusion | figure_legend | sentence | multi_section
venue: nature | ieee | elsevier | unspecified   # optional
journal: string                               # optional
domain: string                                # optional
output: markdown | json                       # markdown default`

### Profile load plan

Each profile declares `profile_version`, section aliases, `style_guide`, one section reference, permitted TSVs, provenance path, and degradation behavior. The loader rejects a missing section mapping instead of silently loading all resources. `candidate` rows remain available for observation/reporting but cannot populate `rules_applied` or `patterns_used`; statistical openers require `paper_count >= 5`.

### Output

Markdown remains the human default. A normalized internal result carries:

`yaml
text: string | null
text_compact: string | null
summary:
  venue: nature | ieee | elsevier | unspecified
  profile_version: string
  section: string
  domain: string | null
  rules_applied: [string]
  patterns_used: [string]
  evidence_rows: [string]
  ai_tells_avoided: [string]
  untraceable_tokens: [string]
  degraded: string | null
  conflicts: [string]`

The `multi_section` adapter retains a shared entity registry and cross-section audit, but does not assume Nature's citation, section order or `Here we` rule for other profiles. If a section cannot pass traceability, it is `text: null` with a non-empty `degraded` explanation.

## Keep / adapt / reject / invent ledger

| Decision | Mechanism | Placement |
|---|---|---|
| keep | Nature verification layer, calibrated hedge tiers, em-dash scrub, dual output, shared context | shared invariant implementation and Nature adapter |
| keep | IEEE/Elsevier core threshold and per-section load order | profile adapters |
| adapt | Nature section prompts and multi-section orchestration | profile-neutral interface plus profile-specific prompt plans |
| adapt | source package `SKILL.md` routing style | unified root SKILL and interface metadata |
| reject | direct concatenation of Nature/IEEE/Elsevier TSV rows | forbidden by loader and tests |
| reject | universal `Here we`, methods-last, self-reference or roadmap rules | profile-only fixtures |
| invent | selector precedence, conflict report, unspecified baseline, common aliases, evidence-aware summary | core router and output contract |

## Compatibility and rollback

The first implementation is a new empty skill package, so no existing public interface needs migration. Existing materials are read-only dependencies. Rollback is path-scoped deletion/revert of the new `paper-writing-studio` package and task artifacts; no source corpus rollback is required.

## Risks and deferred evidence

- Nature counts differ between SKILL and metadata; use actual files/provenance during implementation.
- A journal allowlist can drift; keep it in profile metadata with a dated provenance note and never infer a venue from a broad keyword.
- Local fixtures can show routing and token preservation but cannot prove stylistic similarity on real papers, provider execution, clean installation or human editorial acceptance. Those remain `missing evidence`.
