# Installation

There are two paths. Keep the paths separate.

1. Maintain this development repository (clone, `uv`, tests, docs site).
2. Install skill packages into a manuscript project (copy or `npx skills add`).

A new clone loads shared maintainer rules from tracked `AGENTS.md` and
`CLAUDE.md`. Claude Code imports `AGENTS.md` with `@AGENTS.md`. Other tools load
`AGENTS.md` through native discovery, or by opening `AGENTS.md` in the session.
Do not depend on ignored `.claude/`, `.codex/`, `.agents/`, `.cursor/`, `.grok/`,
`.kimi-code/`, or `.omp/` directories, private absolute paths, or implied global
hooks. Tool-by-tool entry, load, delegation, and permission differences:
[Harnesses](/harnesses).

## Requirements

Install only the toolchains required by the skills you use.

| Area | Requirement |
| --- | --- |
| Repository Python | Python 3.10+ and `uv` |
| LaTeX skills | TeX Live or MiKTeX; `latexmk`, BibTeX/Biber, and optional `chktex` |
| Typst skill | Typst CLI |
| Documentation site | Node.js and npm |

## Path 1: Maintain This Development Repository

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync --extra dev
```

Contributor tests use the unified pytest entry:

```bash
just test
```

`just test` runs `uv run --extra dev python -m pytest`. That command uses the
same pytest config as a direct `uv run --extra dev python -m pytest`
(`testpaths` covers `tests/` and `academic-writing-skills/`). A root-only
`uv run pytest` historically missed the 42 `bib-search-citation` package tests.

Full Python gates:

```bash
just ci
```

`just ci` is four steps: `just check-versions`, `just lint`, `just typecheck`,
`just test`.

Docs resource gate (not part of `just ci`):

```bash
uv run --extra dev python docs/scripts/check_resource_sync.py
```

Install the eight catalog skills into this clone's (or another project's) agent
skill directories with the local installer. This is a maintainer helper for a
clone of this repository. It does not replace `npx skills add`, and it does
not verify the `npx` installer, symlink layout, or five-tool runtime discovery.

```bash
just skills-install
just skills-install latex-paper-en paper-audit
just -- skills-install --list
just -- skills-install --agent cursor --copy -y
just -- skills-install --dest path/to/manuscript --all
```

`just` treats leading hyphens as its own flags, so GNU-style options need
`just -- skills-install ...`. Targets are `.claude/skills`, `.cursor/skills`,
`.agents/skills`, `.grok/skills`, `.kimi-code/skills`, and `.omp/skills`.
Windows defaults to copy; other platforms default to symlink. Those directories
are gitignored in this development repository.

## Path 2: Install Skills Into A Manuscript Project

Use `npx skills` for a single skill or the full collection:

```bash
npx skills add bahayonghang/academic-writing-skills/cover-letter
npx skills add bahayonghang/academic-writing-skills/paper-audit
npx skills add bahayonghang/academic-writing-skills/latex-paper-en
npx skills add bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add bahayonghang/academic-writing-skills/typst-paper
npx skills add bahayonghang/academic-writing-skills/bib-search-citation
npx skills add bahayonghang/academic-writing-skills/paper-writing-studio
npx skills add bahayonghang/academic-writing-skills/latex-defense-zh

# Install all eight
npx skills add bahayonghang/academic-writing-skills
```

The eight `npx skills add bahayonghang/academic-writing-skills/<skill>` command
strings are the documented installer surface. The `npx` installer, any symlink
layout the installer creates, and five-tool runtime discovery stay
**UNVERIFIED**. No captured real run is authorized in this round.

For manual installation, copy each required directory from
`academic-writing-skills/` into the skills directory used by the agent runtime.
Copy the complete skill directory. Each package depends on its local scripts,
references, templates, examples, and metadata. If the tool does not auto-load
the skill, open that skill's `SKILL.md`, then the routed `references/` file.

### paper-audit sibling layout {#paper-audit-layout}

Full `paper-audit` script-backed checks for `.tex` and `.typ` resolve sibling
writing skills from the parent of the `paper-audit/` directory:

```text
<parent>/
├── cover-letter/
├── paper-audit/
├── latex-paper-en/
├── latex-thesis-zh/
├── typst-paper/
├── bib-search-citation/
├── paper-writing-studio/
└── latex-defense-zh/
```

`audit.py` looks for `latex-paper-en/scripts`, `latex-thesis-zh/scripts`, and
`typst-paper/scripts` next to `paper-audit/`. The recommended full collection is
all eight skill directories as siblings.

A single `paper-audit` copy is **limited coverage**. Missing sibling scripts are
skipped. The existing exit and gate behavior is unchanged. Recorded isolation
probe on `tests/fixtures/paper_audit/sample_paper.tex` (`quick-audit --lang en
--format json`): standalone RUN=3, missing=8, exit 0. Recommended full sibling
layout: missing=0.

Do not copy sibling scripts into `paper-audit/`.

## Verify The Environment

```bash
uv --version
python --version
latexmk --version
xelatex --version
typst --version
```

## Run The Documentation Site

Maintainer command:

```bash
just docs
```

Node-direct equivalent:

```bash
npm --prefix docs install
npm --prefix docs run docs:dev
```

Production build: `just doc-build`, or `npm --prefix docs run docs:build`.

## Common Problems

### A TeX or Typst executable is missing

Install the matching toolchain and verify the executable is on `PATH`. Python
dependencies do not install TeX or Typst binaries.

### `uv run python` cannot resolve the environment

Run `uv sync --extra dev` from the repository root, then retry.

### A skill opens but a referenced file is missing

Reinstall or recopy the complete skill directory. The skill entrypoint
intentionally loads detailed guidance from package-local resources.

### `paper-audit` prints `script not found`

The `paper-audit` directory has no sibling writing-skill directories. Install
the [recommended full sibling layout](#paper-audit-layout). A single-skill copy
is limited coverage.
