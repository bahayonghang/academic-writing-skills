# `industrial-ai-research`

Industrial AI literature research workflow with intake, venue-aware search, and structured outputs.

## Use It For

- predictive maintenance surveys
- intelligent scheduling literature scans
- industrial anomaly detection updates
- smart manufacturing and CPS trend mapping
- gap-finding memos for Industrial AI topics

## Workflow Shape

1. intake
2. search plan
3. source collection
4. verification and triage
5. synthesis
6. report assembly

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

## Notes

- This skill is for research, not for compiling or rewriting your paper source.
- It should separate verified evidence from inference.
