---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Choose the right academic-writing skill, run the right script, ship with evidence"
  tagline: "Bilingual docs aligned with the six SKILL.md contracts: LaTeX, Typst, bibliography search, paper audit, and submission cover letters."
  actions:
    - theme: brand
      text: Quick Start
      link: /quick-start
    - theme: alt
      text: Browse Skills
      link: /skills/
    - theme: alt
      text: Cover Letters
      link: /skills/cover-letter/

features:
  - icon: ✉️
    title: "`cover-letter`"
    details: "Submission-letter workflow for LaTeX manuscripts: generate, optimize, align-check, journal-fit, and pre-submission checks against manuscript evidence."
  - icon: 🔬
    title: "`paper-audit`"
    details: "Deep-review-first audit for `.tex`, `.typ`, and `.pdf`, with bilingual Markdown/HTML reports, review workspaces, revision trajectories, claim maps, and quote/citation checks."
  - icon: 📝
    title: "`latex-paper-en`"
    details: "English LaTeX paper workflow for compile, format, bibliography, grammar, logic, literature synthesis, experiments, pseudocode, tables, and de-AI review."
  - icon: 📚
    title: "`latex-thesis-zh`"
    details: "Chinese thesis workflow for structure mapping, GB/T 7714 checks, template detection, compilation, consistency, logic, literature, abstract, and tables."
  - icon: ⚡
    title: "`typst-paper`"
    details: "Typst paper workflow for compile, format, bibliography, grammar, logic, literature synthesis, translation, pseudocode, tables, and experiments."
  - icon: 🔎
    title: "`bib-search-citation`"
    details: "BibTeX/BibLaTeX library search with compact filters, raw BibTeX export, and LaTeX or Typst citation snippets."
---

## What This Site Covers

This site is the stable entry point for choosing, running, and combining the six skills under `academic-writing-skills/`.

Use it to:

- choose the right skill before asking an agent to work on a paper;
- find the smallest script command that proves or diagnoses the issue;
- understand which tasks are source editing, which are audit/reporting, and which are submission packaging;
- follow the same boundaries documented in each skill's `SKILL.md`.

`SKILL.md` remains the source of truth. These pages turn those contracts into user-facing workflows, examples, and cross-skill routing rules.

## Included Skills

| Skill | Best for | Entry |
| --- | --- | --- |
| `cover-letter` | Submission cover letters for LaTeX manuscripts | [/skills/cover-letter/](/skills/cover-letter/) |
| `paper-audit` | Reviewer-style audit, gate checks, and re-audits | [/skills/paper-audit/](/skills/paper-audit/) |
| `latex-paper-en` | Existing English LaTeX papers | [/skills/latex-paper-en/](/skills/latex-paper-en/) |
| `latex-thesis-zh` | Existing Chinese LaTeX theses | [/skills/latex-thesis-zh/](/skills/latex-thesis-zh/) |
| `typst-paper` | Existing Typst papers | [/skills/typst-paper/](/skills/typst-paper/) |
| `bib-search-citation` | Search and cite local `.bib` libraries | [/skills/bib-search-citation/](/skills/bib-search-citation/) |

## Recommended Workflow Families

| Goal | Start here | Then |
| --- | --- | --- |
| Draft or verify a submission letter | `cover-letter generate` or `align-check` | Run `journal-fit` and `presubmission` before sending |
| Decide whether a paper is ready | `paper-audit quick-audit` or `gate` | Use `deep-review` for roadmap-level critique |
| Fix source-level manuscript issues | Matching writing skill (`latex-paper-en`, `latex-thesis-zh`, `typst-paper`) | Compile first, then run targeted modules |
| Find papers in a local bibliography | `bib-search-citation --query` | Add `cite:both`, `raw:true`, or `--return-fields` only when needed |

## Fast Path

1. Start with [/installation](/installation).
2. Run a real command from [/quick-start](/quick-start).
3. Use [/skills/](/skills/) to choose a skill and module.
4. Use [/usage](/usage) for cross-skill routing and output expectations.

## Repository Layout

```text
academic-writing-skills/
├─ cover-letter/
├─ paper-audit/
├─ latex-paper-en/
├─ latex-thesis-zh/
├─ typst-paper/
├─ bib-search-citation/
└─ docs/
```
