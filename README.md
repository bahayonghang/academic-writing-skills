# Academic Writing Skills for Claude Code

[中文版](README_CN.md)

This collection of skills grew out of my day-to-day paper-writing workflow and
has been iteratively refined over time. It may still have shortcomings or rough
edges; if needed, please fork it and adapt it yourself.

> I have recently been writing my dissertation, so I will keep improving
> `latex-thesis-zh` based on actual usage.
> Note: `paper-audit` review reports are for reference only; please verify and
> evaluate them yourself.
>
> Post-writing polish and validation for academic papers: format checks,
> bibliography search and verification, grammar analysis, de-AI editing, and
> experiment narrative review. Focused on improving existing drafts, not writing
> papers from scratch.
>
> Recommended models: **Claude Opus 4.6 · Fable 5.1 · GPT 6 Astra · Gemini 3.8 Flash · Kimi K3 · DeepSeek V4 Pro**
>
>
> Recommended platforms: **Claude Code · Codex**
>
> Applicable tools: Claude Code, Codex, Grok Build, Kimi Code, and OMP (Oh My Pi).
>
> Naming a tool here is not a runtime verification. Unrun five-tool runtime stays UNVERIFIED.

## Install

Install the repository with skills:

```bash
npx skills add bahayonghang/academic-writing-skills
```

Then open an applicable tool in your manuscript project and ask for the task in
natural language. The root README is only a routing guide; the authoritative
usage details live in each `SKILL.md` file and in the docs site.

## Choose A Skill


| Skill                                                                         | Use When                                                                                                                                                                                    | Main Inputs                                   | Source Of Truth                |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------ |
| [`cover-letter`](academic-writing-skills/cover-letter/SKILL.md)               | Generate, optimize, align-check, preflight, or journal-fit-check a submission cover letter against an existing LaTeX manuscript.                                                            | `.tex`, optional `.md` or `.tex` letter draft | `cover-letter/SKILL.md`        |
| [`paper-audit`](academic-writing-skills/paper-audit/SKILL.md)                 | Run reviewer-style critique, submission gates, blocker triage, revision roadmaps, journal-style reports, or re-audits.                                                                      | `.tex`, `.typ`, `.pdf`                        | `paper-audit/SKILL.md`         |
| [`latex-paper-en`](academic-writing-skills/latex-paper-en/SKILL.md)           | Work on existing English LaTeX conference or journal papers: compile, formatting, grammar, logic, sections, references, figures, tables, pseudocode, title, translation, or de-AI polish.   | `.tex`                                        | `latex-paper-en/SKILL.md`      |
| [`latex-thesis-zh`](academic-writing-skills/latex-thesis-zh/SKILL.md)         | Work on existing Chinese LaTeX theses: compile diagnostics, GB/T 7714 references, chapter structure, bilingual captions and rendered figure/table layout, evidence-faithful abstracts, summaries, literature synthesis, engineering-application chapters, results analysis, Chinese inter-sentence expression, de-AI polish, and paragraph/subsection polish with revision checks. | `.tex`                                        | `latex-thesis-zh/SKILL.md`     |
| [`typst-paper`](academic-writing-skills/typst-paper/SKILL.md)                 | Work on existing English or Chinese Typst manuscripts: compile/export diagnostics, venue formatting, references, grammar, logic, tables, pseudocode, title, translation, or de-AI polish.   | `.typ`                                        | `typst-paper/SKILL.md`         |
| [`bib-search-citation`](academic-writing-skills/bib-search-citation/SKILL.md) | Search, filter, preview, export, or create LaTeX/Typst citation snippets from a local BibTeX or BibLaTeX library.                                                                           | `.bib`                                        | `bib-search-citation/SKILL.md` |


Opt-in checks only report local candidates: `check_consistency.py --governance` requires `--custom-terms`, `--abbreviation-style` is independent, and `check_style_zh.py --degree-wording` is off by default; without these flags the previous output stays unchanged.
College number, equation, table-body, and Chinese-caption checks use `--school yanshan-ee-2025` on `check_style_zh.py`, `check_format.py`, `check_tables.py`, and `check_references.py`. The default and `--school generic` add no candidates, and there is no bare `yanshan` alias.
Citation placement, repeated-citation pages, college bibliography prompts, and review progression density run only behind explicit flags: `check_references.py --author-cite` and `--repeat-cite` are independent and may combine with `--school`; `verify_bib.py --college-details` is legal only with `--standard gb7714` or `gb7714-2025`; `analyze_literature.py --progression-density` may combine with `--section` and is mutually exclusive with `--intro-citations`. Without these flags the previous output stays unchanged.
Same-chapter table, body, and chapter-summary final values are compared only by `analyze_experiment.py --cross-surface`. `--section` may narrow the chapter. `--cross-surface-terms FILE` is valid only with that switch and replaces only the metric or evaluation-set list. Candidates are `[Script]`, Info/P3, and `Meaning-Check: NEEDS-LLM`, with a local position and no corrected number. Without `--cross-surface` the previous output stays unchanged, and the existing `--results-analysis` codes stay independent.
The graduate-school checklist is `--template yanshan`. The 2025 college checklist is `--template yanshan-ee-2025`. The two coexist. 111 statuses are not 111 compliant items. A partial checker does not PASS a compound item, and MODULE or NEEDS-LLM still needs human review.
Method-expression labels, a weakness written as an advantage, a pronoun left without an antecedent after a deleted preview, abstract quotation marks, and formula symbols in a title or chapter-arrangement line are LLM-only readings on the existing `logic`, `claim-forward`, `abstract`, and `structure` modules. They add no script code, no threshold, and no new module.

Use the format-specific writing skills when you want source edits or polish. Use
`paper-audit` when you want reviewer-style diagnosis without rewriting the
source. Use `bib-search-citation` when the target is the bibliography library
itself.

## Typical Prompts

```text
Compile my English LaTeX paper with latexmk and explain the first blocking error.
```

```text
Check the introduction for logic gaps, citation stacking, and AI-like phrasing.
```

```text
Run a paper-audit gate on main.tex and separate blockers from polish issues.
```

```text
Search references.bib for recent Mamba forecasting papers with code and return LaTeX and Typst citation snippets.
```

```text
Align-check this cover letter against main.tex and report unsupported claims only.
```

## Safety And Outputs

- The skills are for improving and validating existing academic material. They
should not invent experiments, citations, policies, or unsupported claims.
- Citation keys, DOI, arXiv IDs, URLs, and local `.bib` matches are provenance
fields, not proof that a paper supports a manuscript claim.
- Online checks are optional. When current venue rules or external metadata
matter, verify them from the original source before treating them as binding.
- Source-editing suggestions should preserve LaTeX and Typst syntax and mark
required evidence as pending instead of filling it in.
- Audit and helper-script outputs may be JSON, Markdown reports, or diff-comment
style findings with severity and priority.

Example finding shape:

```latex
% <MODULE> (Line <N>) [Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: <Issue summary>
% Before: <original text>
% After:  <suggested text>
% Rationale: <brief explanation>
% [PENDING VERIFICATION]: <if evidence or metrics are required>
```

## Requirements

- Python 3.10+
- `uv` for running the bundled Python helpers
- TeX Live or MiKTeX with `latexmk` and `chktex` for LaTeX workflows
- XeLaTeX plus CJK fonts for Chinese LaTeX documents
- Typst CLI for Typst workflows
- `pymupdf` (PyMuPDF) for PDF audit workflows; optional `pymupdf4llm` for enhanced extraction (both lazily imported)
- Node.js and npm or `just` only when building the docs site locally

## Repository Layout

```text
academic-writing-skills/
├── academic-writing-skills/
│   └── <skill>/
│       ├── SKILL.md          # Skill entrypoint, triggers, routing, contracts
│       ├── scripts/          # Optional executable helpers
│       ├── references/       # Optional source-of-truth guidance
│       ├── examples/         # Optional example prompts or workflows
│       ├── templates/        # Optional output templates
│       ├── evals/            # Optional evaluation cases
│       └── agents/           # Optional agent metadata
├── docs/                     # Documentation site
├── tests/                    # Pytest coverage for contracts and helpers
├── ref/                      # Supporting reference repositories or material
├── .trellis/                 # Project workflow and guidance
├── README.md
└── README_CN.md
```

Do not rely on the root README for module internals. Open the relevant
`SKILL.md`, `references/`, and docs page when a workflow needs exact routing,
flags, or output contracts.

## Documentation

Full documentation is in [`docs/`](docs/) and [`docs/zh/`](docs/zh/).

Run locally:

```bash
just docs
```

Build the static site:

```bash
just doc-build
```

## Contributing

Issues and pull requests are welcome. Keep changes scoped to the relevant skill,
update tests or docs when behavior changes, and run `just ci` before submitting
when feasible.

## License

Academic Use Only — Not for commercial use.
