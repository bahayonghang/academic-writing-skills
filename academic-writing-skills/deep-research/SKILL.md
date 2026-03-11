---
name: deep-research
description: Deep literature research for Industrial AI and automation topics. Use when the user needs up-to-date research on predictive maintenance, intelligent scheduling, industrial anomaly detection, smart manufacturing, cyber-physical systems, edge AI for automation, or crossover robotics-for-industry topics. Prioritize recent arXiv and top IEEE or automation venues, ask for report language before synthesis, and produce structured research reports with source buckets, shortlisted papers, synthesis, and next-step recommendations.
---

# Industrial AI Deep Research

Run a lean, source-aware deep research workflow for Industrial AI.

## Core Rules

1. Use `askquestions` or the host's equivalent interactive question tool before any synthesis.
2. Ask for four items in the opening intake:
   - report language
   - deliverable mode
   - time window
   - domain emphasis inside Industrial AI
3. Keep the skill workflow in English only, even when the requested report language is not English.
4. Prefer recent arXiv plus top IEEE and automation venues over generic web articles.
5. Default to the last 3 years, but keep seminal older work when it is still necessary for context.
6. Cite every substantive claim and separate verified evidence from inference.

## Intake Contract

Always start by asking these four questions.

### 1. Report language

Offer:
- `English`
- `Simplified Chinese`
- `Bilingual summary`

### 2. Deliverable mode

Offer:
- `research-brief`
- `literature-map`
- `venue-ranked survey`
- `research-gap memo`

### 3. Time window

Offer:
- `last 12 months`
- `last 3 years`
- `last 5 years`
- `custom window`

### 4. Domain emphasis

Offer Industrial AI choices such as:
- predictive maintenance
- intelligent scheduling
- industrial anomaly detection
- smart manufacturing and process optimization
- CPS, edge AI, and industrial intelligence
- robotics crossover for industrial environments

If the user does not choose, default to `last 3 years` and the subdomain implied by their prompt.

## Source Strategy

Read these files before searching:
- `references/source-priority.md`
- `references/venue-map.md`

Primary sources:
- arXiv: `eess.SY`, `cs.AI`
- IEEE and automation anchors: `T-ASE`, `CASE`

Supporting crossover sources:
- arXiv: `cs.RO`, `cs.LG`
- IEEE robotics venues: `ICRA`, `IROS`, `RA-L`, `T-RO`
- Adjacent industrial and control venues listed in `references/venue-map.md`

When the user asks for the latest work, prefer:
1. arXiv recent streams for rapid updates
2. top IEEE and automation venues for stronger publication filtering
3. secondary crossover venues only when they materially improve coverage

## Workflow

### Phase 1. Scope

- Rewrite the request as a precise Industrial AI research objective.
- Lock the report language, deliverable mode, time window, and domain emphasis.
- State explicit in-scope and out-of-scope boundaries.

### Phase 2. Search Plan

- Build venue buckets and keyword groups from `references/source-priority.md`.
- Separate primary sources from secondary crossover sources.
- State the recency policy and any seminal-paper exceptions.

### Phase 3. Source Collection

- Gather papers from the prioritized source buckets.
- Prefer official venue pages, arXiv recent listings, IEEE Xplore landing pages, and publisher or conference pages.
- Record why each paper was included.

### Phase 4. Verification and Triage

- Check venue quality, publication type, year, and relevance.
- Remove weak matches, duplicates, and generic blog-style sources.
- Mark unreviewed preprints as preprints.

### Phase 5. Synthesis

- Cluster the shortlisted papers by problem, method, dataset, deployment setting, and evaluation style.
- Surface trends, gaps, contradictions, and under-explored opportunities.
- Run a contrarian pass: what would challenge the dominant conclusion?

### Phase 6. Report Assembly

Use the stable report structure from `references/report-modes.md`.

Every final report must include:
- search scope
- source buckets by venue
- shortlisted papers
- synthesis of trends and gaps
- recommended next reading or next experiments

## Deliverable Modes

Read `references/report-modes.md` and follow the selected mode exactly.

- `research-brief`: short, decision-ready overview
- `literature-map`: thematic map across methods and subproblems
- `venue-ranked survey`: grouped by source quality and venue tier
- `research-gap memo`: open problems, design space, and next-step opportunities

## Quality Bar

Read `references/quality-checklist.md` before finalizing.

Non-negotiable standards:
- no unsupported claims
- no venue-blind source mixing
- no hiding contradictions
- no synthesized report before intake questions are answered
- no generic "latest research says" language without source-backed evidence

## Examples

- `examples/predictive-maintenance.md`
- `examples/intelligent-scheduling.md`
- `examples/industrial-anomaly-detection.md`

## Boundaries

This v1 skill does not implement:
- systematic review mode
- meta-analysis
- IRB-heavy or clinical ethics branches
- standalone automation scripts

If the user needs those, state the boundary and continue with the closest supported research mode.
