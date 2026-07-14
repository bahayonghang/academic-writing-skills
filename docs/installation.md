# Installation

## Requirements

Install only the toolchains required by the skills you use.

| Area | Requirement |
| --- | --- |
| Repository Python | Python 3.10+ and `uv` |
| LaTeX skills | TeX Live or MiKTeX; `latexmk`, BibTeX/Biber, and optional `chktex` |
| Typst skill | Typst CLI |
| Documentation site | Node.js and npm |

## Clone And Install

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync --extra dev
```

## Install Skills

Use `npx skills` for a single skill or the full collection:

```bash
npx skills add bahayonghang/academic-writing-skills/cover-letter
npx skills add bahayonghang/academic-writing-skills/paper-audit
npx skills add bahayonghang/academic-writing-skills/latex-paper-en
npx skills add bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add bahayonghang/academic-writing-skills/typst-paper
npx skills add bahayonghang/academic-writing-skills/bib-search-citation

# Install all six
npx skills add bahayonghang/academic-writing-skills
```

For manual installation, copy the required directory from `academic-writing-skills/` into
the skills directory used by your agent runtime. Do not copy only `SKILL.md`; each package
depends on its local scripts, references, templates, examples, and metadata.

## Verify The Environment

```bash
uv --version
python --version
latexmk --version
xelatex --version
typst --version
```

Run the repository gates from the root:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```

## Run The Documentation Site

```bash
npm --prefix docs install
npm --prefix docs run docs:dev
```

Use `npm --prefix docs run docs:build` for a production build.

## Common Problems

### A TeX or Typst executable is missing

Install the matching toolchain and verify the executable is on `PATH`. Python dependencies
do not install TeX or Typst binaries.

### `uv run python` cannot resolve the environment

Run `uv sync --extra dev` from the repository root, then retry.

### A skill opens but a referenced file is missing

Reinstall or recopy the complete skill directory. The skill entrypoint intentionally loads detailed
guidance from package-local resources.
