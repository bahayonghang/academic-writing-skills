# PRESUBMISSION Mode Integration

How the script-backed `PRESUBMISSION` layer plugs into each `paper-audit` mode.
For the deterministic rule list, severity calibration, and AI-tone term ban
list, see `references/PRE_SUBMISSION_RULES.md`.

Read next:
- `references/PRE_SUBMISSION_RULES.md` for the rule taxonomy and term list.
- `references/MODE_GUIDE.md` for full mode workflows.

## Purpose

`PRESUBMISSION` is a deterministic final-week mechanical layer (em dashes,
AI-tone term frequency, abstract completeness, LaTeX citation/label/equation
hygiene, paragraph-shape weak signals, concrete captions). It is **not a
public mode**; it runs inside existing modes.

## Mode Behavior Matrix

| Mode | PRESUBMISSION role | Promotion | Gate effect |
|---|---|---|---|
| `quick-audit` | inline mechanical readiness signals | n/a | n/a |
| `gate` | advisory + Critical blockers | n/a | only Critical fails the gate |
| `re-audit` | regression comparison for mechanical findings | n/a | n/a |
| `deep-review` Phase 0 | script context for reviewer lanes | full/editor focus may promote high-signal items into `pre_submission_readiness` lane | n/a |

For focused theory, literature, methodology, and logic reviews,
`PRESUBMISSION` findings stay in Phase 0 context only. They never become
focused-bundle lane issues.

## Severity Mapping

| PRESUBMISSION source taxonomy | quick/gate severity | deep-review bundle severity |
|---|---|---|
| CRITICAL | Critical / P0 | major + `gate_blocker=true` |
| MAJOR | Major / P1 | moderate |
| MINOR | Minor / P2 | minor or Phase 0 only |

`gate` fails only on Critical script findings or failed checklist items. Major
and Minor `PRESUBMISSION` findings stay advisory.

## PDF vs Source Behavior

| Check group | LaTeX/Typst source | PDF mode |
|---|---|---|
| em dash scan | run | run |
| banned AI-tone frequency | run | run |
| abstract five-element check | run | run |
| long paragraph / topic-sentence weak signals | run | run |
| LaTeX citation tie hygiene | run | skipped |
| label space/hyphen rules | run | skipped |
| numbered equation reference rules | run | skipped |
| source-caption rules | run | skipped |

Skips must be visible in script output as ignored comments or metadata, never
as issues.

## Provenance Rules

- All `PRESUBMISSION` findings keep `[Script]` provenance.
- Findings must anchor to source text, line number, or section.
- Reviewer-facing prose must not silently absorb mechanical findings as if
  they were reviewer judgment.
- The skill audits only; it does not rewrite paper source. Route rewriting
  requests to the format-specific writing skill.

## Integration with `gate`

1. `gate` reads `PRESUBMISSION` findings together with its own checklist.
2. Critical findings convert to gate blockers.
3. Major and Minor findings appear in advisory recommendations after the
   verdict and EIC screening.
4. IEEE pseudocode rules: distinguish mandatory from IEEE-safe recommendation.

## Integration with `deep-review`

1. `audit.py --mode deep-review` runs `PRESUBMISSION` as part of Phase 0.
2. Focus routing decides what happens to those findings:
   - `--focus full` or `--focus editor`: high-signal items can be promoted
     into the `pre_submission_readiness` lane and consolidated alongside
     reviewer findings.
   - `--focus theory|literature|methodology|logic`: keep `PRESUBMISSION` in
     Phase 0 context only; do not surface them as focused lane issues.
3. Promotion does not bypass consolidation. Promoted items still flow through
   `consolidate_review_findings.py` and `verify_quotes.py`.

## Integration with `re-audit`

`re-audit` compares the new `PRESUBMISSION` findings to the previous run.
Status labels follow the standard `re-audit` schema: `FULLY_ADDRESSED`,
`PARTIALLY_ADDRESSED`, `NOT_ADDRESSED`, `NEW`.

Mechanical regressions are reported alongside reviewer-finding regressions but
keep their `[Script]` provenance so the user can distinguish style drift from
substantive reviewer concerns.
