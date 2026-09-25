---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Route the task, run the evidence-backed workflow"
  tagline: "Bilingual documentation for seven skills covering LaTeX, Typst, bibliography search, paper audit, submission cover letters, and venue-aware polishing."
  actions:
    - theme: brand
      text: Quick Start
      link: /quick-start
    - theme: alt
      text: Browse Skills
      link: /skills/
    - theme: alt
      text: Usage Guide
      link: /usage

features:
  - icon: ✉️
    title: "`cover-letter`"
    details: "Generate and verify submission letters against manuscript evidence and venue expectations."
  - icon: 🔬
    title: "`paper-audit`"
    details: "Run reviewer-style audits, submission gates, revision roadmaps, and re-audits."
  - icon: 📝
    title: "`latex-paper-en`"
    details: "Compile and improve existing English LaTeX journal or conference papers."
  - icon: 📚
    title: "`latex-thesis-zh`"
    details: "Check Chinese LaTeX theses from structure and GB/T 7714 through blind-review delivery."
  - icon: ⚡
    title: "`typst-paper`"
    details: "Compile, review, and adapt existing Typst manuscripts."
  - icon: 🔎
    title: "`bib-search-citation`"
    details: "Search local BibTeX/BibLaTeX libraries and return citation-ready results."
  - icon: 🖋️
    title: "`paper-writing-studio`"
    details: "Polish or translate academic prose with an explicit Nature, IEEE, Elsevier, or neutral profile."
---

## Start From The Artifact

| You have | Start with |
| --- | --- |
| A submission manuscript and need an editor letter | [`cover-letter`](/skills/cover-letter/) |
| A paper that needs critique or a readiness decision | [`paper-audit`](/skills/paper-audit/) |
| An English LaTeX paper | [`latex-paper-en`](/skills/latex-paper-en/) |
| A Chinese LaTeX thesis | [`latex-thesis-zh`](/skills/latex-thesis-zh/) |
| A Typst paper | [`typst-paper`](/skills/typst-paper/) |
| A local `.bib` library | [`bib-search-citation`](/skills/bib-search-citation/) |
| Academic prose that needs venue-style polishing or translation | [`paper-writing-studio`](/skills/paper-writing-studio/) |

## Documentation Contract

Each `SKILL.md` is the behavior source of truth. The site turns those contracts into
task-facing overviews and fully bilingual public resources.

Every skill uses the same resource layout:

```text
skills/<skill>/resources/
├─ references/
├─ templates/
├─ examples/
└─ agents/
```

The Chinese site mirrors the same paths under `/zh/skills/`. Use the overview to choose
a module or mode, then open only the resource needed for that step.

## Recommended Sequence

1. [Install the repository and required toolchain](/installation).
2. [Choose a skill and run one real command](/quick-start).
3. Use the matching skill overview to select a module or mode.
4. Use [the cross-skill guide](/usage) when a request spans writing, audit, retrieval,
   and submission packaging.
