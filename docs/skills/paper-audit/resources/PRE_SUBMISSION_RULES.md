# Pre-Submission Rules

`paper-audit` ships a deterministic `PRESUBMISSION` layer (introduced in v4.5)
for the final 3-5 days before submission. It is integrated into existing
modes; there is no separate public `pre-submission` mode.

Source attribution: adapted from
`ref/Supervisor-Skills/plugins/phd-research/skills/pre-submission-reviewer`
(license: CC-BY-4.0).

## Where It Runs

- `quick-audit`: shows mechanical readiness findings with `[Script]`
  provenance.
- `gate`: keeps Critical findings as blockers; Major/Minor findings are
  advisory.
- `re-audit`: compares mechanical regressions across revisions.
- `deep-review` Phase 0: supplies context. Full/editor focus can promote
  high-signal findings into `pre_submission_readiness`; focused methodology,
  theory, literature, and logic reviews keep them out of the final bundle.

## Severity Mapping

| Source taxonomy | quick/gate severity | deep-review severity |
| --- | --- | --- |
| CRITICAL | Critical / P0 | major + gate blocker |
| MAJOR | Major / P1 | moderate |
| MINOR | Minor / P2 | minor or Phase 0 only |

## Script-Checkable Rules

- G1: em dash in reader-visible prose.
- G2: paragraph longer than 180 words or more than 8 sentences.
- G3: weak transition-only topic sentence.
- G4: banned AI-tone term group appears three or more times.
- G5: abstract misses background, objective, method, results, conclusion, or a
  quantitative result cue.
- L1: LaTeX citation lacks a non-breaking tie before `\cite...`.
- L2: LaTeX label contains spaces.
- L3: LaTeX label uses hyphens where underscores are safer.
- L4: numbered equation has no label.
- L5: numbered equation label is never referenced.
- F1: source caption lacks a concrete finding or comparison cue.

## PDF vs Source

PDF mode runs only text-verifiable items:

- em dash scan
- AI-tone frequency
- abstract completeness
- paragraph-shape weak signals

PDF mode skips source-only checks:

- LaTeX citation ties
- label naming
- numbered equation references
- source captions

The script prints the skip as ignored metadata/comment text, not as an issue.
