# `industrial-ai-research`

Industrial AI literature research workflow with intake, venue-aware search, and structured outputs.

## Use It For

- predictive maintenance surveys
- intelligent scheduling literature scans
- industrial anomaly detection updates
- smart manufacturing and CPS trend mapping
- gap-finding memos for Industrial AI topics
- drafting structured survey manuscripts on Industrial AI subtopics

## Workflow Shape

1. intake
2. search plan
3. source collection
4. verification and triage
5. synthesis
6. report assembly

When `survey-draft` mode is selected, steps 1–4 run as normal, then steps 5–6 are replaced by the survey-draft workflow (S1–S4).

### Survey-Draft Workflow (S1–S4)

| Phase | Name | What happens |
| --- | --- | --- |
| S1 | Outline | Extract taxonomy from literature, build section skeleton as YAML, present to user for approval (checkpoint) |
| S2 | Evidence | Assemble a per-H3 evidence pack with locked citation scope (structured data, no prose) |
| S3 | Writer | Draft each H3 independently from its evidence pack, run self-check gate (depth, citation scope, tone) |
| S4 | Merge | Merge all section drafts, run cross-section consistency checks and 9-point quality gate, optional LaTeX handoff via `latex-paper-en` |

## Intake Defaults

If the user does not specify them, the skill defaults toward:

- time window: last 3 years
- topic emphasis: implied by the prompt

## Deliverable Modes

| Mode | Best for |
| --- | --- |
| `research-brief` | short decision-ready overview |
| `literature-map` | thematic clustering |
| `venue-ranked survey` | source-tier-sensitive survey |
| `research-gap memo` | open problems and next experiments |
| `survey-draft` | taxonomy-driven survey manuscript with outline-first writing and optional LaTeX export |

## Source Policy

Primary sources emphasize recent arXiv and top IEEE or automation venues. Crossover robotics venues are secondary unless they materially improve coverage.

## Good First Requests

```text
Research recent predictive maintenance papers in the last 3 years.
```

```text
Compare scheduling RL papers from arXiv and IEEE automation venues.
```

```text
Write a research-gap memo for industrial anomaly detection.
```

```text
Draft a survey on predictive maintenance using the survey-draft mode.
```

## Notes

- This skill is for research, not for compiling or rewriting your paper source.
- It should separate verified evidence from inference.
- Standard report modes end as one final report with stable sections. `survey-draft` is the engineering-heavier path and produces staged artifacts such as `outline.yml`, per-section evidence files, section drafts, a merged `survey-draft.md`, and a `quality-report.md`.
- `survey-draft` mode produces Markdown by default. For LaTeX output, it delegates final formatting to `latex-paper-en`.
- The current hardening direction keeps `survey-outline`, `survey-evidence`, `survey-write`, and `survey-merge` as distinct gated phases: no prose is generated until the outline is approved and all evidence packs are assembled.
- Literature review quality standards (A1-A4) from the writing skills are cross-referenced in `SURVEY_WRITING_GUIDE.md` for survey context: thematic clustering, critical analysis, gap derivation, and citation density funnel apply to survey writing as well.
- Survey prose should preserve contradictions and default to `consensus -> disagreement -> limitations -> gap`, not paper-by-paper narration or fake agreement.
