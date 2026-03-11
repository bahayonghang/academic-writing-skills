# Deep Research (deep-research)

Industrial AI deep research with mandatory intake questions, venue-aware source prioritization, and structured report outputs.

## Overview

The `deep-research` skill is a lean research workflow for automation and Industrial AI topics. It is designed for requests such as predictive maintenance surveys, intelligent scheduling literature scans, industrial anomaly detection updates, and smart manufacturing trend mapping.

Unlike the writing-first skills in this repository, `deep-research` starts with an intake step, then prioritizes recent arXiv streams and top IEEE or automation venues before producing a structured report.

## Core Capabilities

- Mandatory opening intake for report language, deliverable mode, time window, and Industrial AI emphasis
- Industrial AI first source strategy, with robotics venues treated as crossover sources
- Venue-aware filtering for recent arXiv, IEEE automation, and adjacent industrial/control literature
- Stable report formats for short brief, literature map, venue-ranked survey, and research-gap memo
- Contrarian synthesis pass to surface weak evidence and overclaimed trends

## Intake Questions

The skill asks these before synthesis:

1. Report language
2. Deliverable mode
3. Time window
4. Domain emphasis inside Industrial AI

Default language choices:
- `English`
- `Simplified Chinese`
- `Bilingual summary`

## Deliverable Modes

| Mode | Best for |
|---|---|
| `research-brief` | fast decision-ready overview |
| `literature-map` | thematic overview across methods and papers |
| `venue-ranked survey` | source-quality-sensitive literature scan |
| `research-gap memo` | identifying open problems and next experiments |

## Default Source Policy

Primary anchors:
- arXiv `eess.SY`
- arXiv `cs.AI`
- IEEE Transactions on Automation Science and Engineering
- IEEE CASE

Secondary crossover sources:
- arXiv `cs.RO`
- arXiv `cs.LG`
- ICRA
- IROS
- RA-L
- T-RO

## Example Requests

```text
Deep research recent predictive maintenance papers
```

```text
Compare latest scheduling RL papers from arXiv and IEEE
```

```text
Research industrial anomaly detection gaps and summarize them in Chinese
```

## References

- Skill definition: `academic-writing-skills/deep-research/SKILL.md`
- Source policy: `references/source-priority.md`
- Venue map: `references/venue-map.md`
