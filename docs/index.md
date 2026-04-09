---
layout: home

hero:
  name: "Academic Writing Skills"
  text: "Skill-first docs for LaTeX, Typst, audit, and research workflows"
  tagline: "Documentation rebuilt from the actual SKILL.md contracts in this repository."
  actions:
    - theme: brand
      text: Install
      link: /installation
    - theme: alt
      text: Browse Skills
      link: /skills/
    - theme: alt
      text: GitHub
      link: https://github.com/bahayonghang/academic-writing-skills

features:
  - icon: 📝
    title: "`latex-paper-en`"
    details: "English LaTeX paper workflow for compile, format, bibliography, grammar, sentence, logic, expression, translation, title, figure, de-AI, and experiment review."
  - icon: 📚
    title: "`latex-thesis-zh`"
    details: "Chinese thesis workflow for structure mapping, GB/T 7714 checks, template detection, compilation, consistency checks, title optimization, de-AI, and experiment review."
  - icon: ⚡
    title: "`typst-paper`"
    details: "Typst paper workflow for compile, format, bibliography, grammar, sentence, logic, expression, translation, title, de-AI, and experiment review."
  - icon: 🔬
    title: "`paper-audit`"
    details: "Deep-review-first audit for `.tex`, `.typ`, and `.pdf` with quick-audit, deep-review, gate, polish, and re-audit workflows plus a journal-style peer review report output."
  - icon: 🧭
    title: "`industrial-ai-research`"
    details: "Venue-aware Industrial AI literature workflow with mandatory intake, source prioritization, structured report modes, and survey draft generation."
  - icon: 🛠️
    title: "Script-backed"
    details: "The docs now align with the repository reality: Python scripts live under each skill's `scripts/`, and repo-local examples use `uv run python ...`."
---

## What This Site Covers

This site documents the skills that exist under `academic-writing-skills/`. It is intentionally skill-first:

- install the repository or individual skills
- decide which skill fits your task
- understand the module router for that skill
- use the matching script or prompt pattern

The primary source of truth is each skill's `SKILL.md`. These docs summarize and organize those contracts for faster onboarding.

## Included Skills

| Skill | Best for | Entry |
| --- | --- | --- |
| `latex-paper-en` | Existing English LaTeX papers | [/skills/latex-paper-en/](/skills/latex-paper-en/) |
| `latex-thesis-zh` | Existing Chinese LaTeX theses | [/skills/latex-thesis-zh/](/skills/latex-thesis-zh/) |
| `typst-paper` | Existing Typst papers | [/skills/typst-paper/](/skills/typst-paper/) |
| `paper-audit` | Pre-submission checks and reviews | [/skills/paper-audit/](/skills/paper-audit/) |
| `industrial-ai-research` | Industrial AI literature research | [/skills/industrial-ai-research/](/skills/industrial-ai-research/) |

## Core Principles

- Use the smallest matching module instead of running every checker by default.
- Provide the entry file path and target scope when you want script execution.
- Keep compilation, checking, rewriting, and auditing as separate steps when possible.
- Treat the docs as guidance for the repository version you installed, not as generic LaTeX or Typst advice.

## Fast Path

1. Start with [/installation](/installation).
2. Follow [/quick-start](/quick-start) for the first working command.
3. Use [/skills/](/skills/) to choose the correct skill.
4. Use [/usage](/usage) for cross-skill conventions.

## Repository Layout

```text
academic-writing-skills/
├─ latex-paper-en/
├─ latex-thesis-zh/
├─ typst-paper/
├─ paper-audit/
├─ industrial-ai-research/
└─ docs/
```
