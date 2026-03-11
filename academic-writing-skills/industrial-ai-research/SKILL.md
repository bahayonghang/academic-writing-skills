---
name: industrial-ai-research
description: Industrial AI literature research with mandatory intake questions, venue-aware source prioritization, and structured report outputs. Use when the user needs up-to-date research on predictive maintenance, intelligent scheduling, industrial anomaly detection, smart manufacturing, cyber-physical systems, edge AI for automation, or crossover robotics-for-industry topics.
metadata:
  category: academic-writing
  tags: [industrial-ai, research, literature-review, predictive-maintenance, scheduling, anomaly-detection, smart-manufacturing, cps, arxiv, ieee]
  version: "1.0"
  last_updated: "2026-03-11"
argument-hint: "[topic] [--mode MODE] [--lang LANG] [--window WINDOW]"
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# Industrial AI Research

Run a lean, source-aware research workflow for Industrial AI.

## Capability Summary

- Structured literature research for Industrial AI and automation topics
- Mandatory four-question intake before any search or synthesis
- Venue-aware source prioritization (arXiv, IEEE, automation venues)
- Four deliverable modes: research-brief, literature-map, venue-ranked survey, research-gap memo
- Contrarian synthesis pass to surface contradictions and under-explored gaps

## Triggering

Use this skill when the user wants to:
- Survey Industrial AI literature on a specific subtopic
- Compare papers across venues or methods within Industrial AI
- Identify research gaps in predictive maintenance, scheduling, anomaly detection, or smart manufacturing
- Produce a structured research report with source-backed evidence

## Do Not Use

- Writing or compiling LaTeX/Typst papers (use `latex-paper-en`, `latex-thesis-zh`, or `typst-paper`)
- Auditing paper quality or formatting (use `paper-audit`)
- Systematic reviews or meta-analyses requiring IRB or clinical ethics
- Topics outside the Industrial AI and automation domain

## Safety Boundaries

- Never fabricate paper metadata (title, authors, venue, year, DOI)
- Never present preprints as peer-reviewed publications
- Never start synthesis before intake questions are answered
- Never suppress contradictions or conflicting evidence
- Never use Tier 4 sources (blogs, press releases) as primary evidence

## Core Rules

1. Ask the user the four intake questions (see `references/question-flow.md`) before starting any search or synthesis.
2. Keep the skill workflow in English only, even when the requested report language is not English.
3. Prefer recent arXiv plus top IEEE and automation venues over generic web articles.
4. Default to the last 3 years, but keep seminal older work when it is still necessary for context.
5. Cite every substantive claim and separate verified evidence from inference.

## Intake Contract

Always start by asking the four intake questions defined in `references/question-flow.md`:
1. Report language (English / Simplified Chinese / Bilingual summary)
2. Deliverable mode (research-brief / literature-map / venue-ranked survey / research-gap memo)
3. Time window (last 12 months / last 3 years / last 5 years / custom)

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

## Error Handling

- **Zero results**: Broaden keywords, relax the time window by one tier, and try adjacent venues. If still empty, report the negative result with the exact queries attempted.
- **Off-subdomain topic**: State that the topic falls outside Industrial AI scope, suggest the closest supported subdomain, and ask the user whether to proceed or abort.
- **Inaccessible databases**: Note which sources were unreachable, proceed with available sources, and flag the gap in the final report.
- **Too few papers (<5 shortlisted)**: Lower the time window threshold, include Tier 2/3 venues, and explicitly note the thin evidence base in the synthesis.

## Reference Map

| File | Phase | When to read |
|------|-------|-------------|
| `references/question-flow.md` | Intake | Before asking the user any questions |
| `references/source-priority.md` | Search Plan | Before building venue buckets |
| `references/venue-map.md` | Search Plan | Before selecting specific venues |
| `references/report-modes.md` | Report Assembly | Before structuring the final output |
| `references/quality-checklist.md` | Report Assembly | Before finalizing the report |

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
