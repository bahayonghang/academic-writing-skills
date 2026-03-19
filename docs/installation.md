# Installation

## Prerequisites

Install the tools required by the skills you plan to use.

| Area | Required |
| --- | --- |
| Python | Python 3.8+ and `uv` |
| LaTeX workflows | TeX Live or MiKTeX, plus `latexmk`, `chktex`, `bibtex` or `biber` |
| Typst workflows | `typst-cli` |
| Docs development | Node.js if you want to run the VitePress site locally |

Repo-local Python commands in this project use `uv run python ...`. Tests use `uv run python -m pytest ...`.

## Install the Repository

```bash
git clone https://github.com/bahayonghang/academic-writing-skills.git
cd academic-writing-skills
uv sync
```

## Install Skills

Recommended: install directly with `npx skills`.

```bash
# Install individual skills
npx skills add github.com/bahayonghang/academic-writing-skills/latex-paper-en
npx skills add github.com/bahayonghang/academic-writing-skills/latex-thesis-zh
npx skills add github.com/bahayonghang/academic-writing-skills/typst-paper
npx skills add github.com/bahayonghang/academic-writing-skills/paper-audit
npx skills add github.com/bahayonghang/academic-writing-skills/industrial-ai-research

# Or install all skills at once
npx skills add github.com/bahayonghang/academic-writing-skills
```

If you prefer manual installation, copy the skill folders you need into your Claude skill directory.

Typical folders:

- `academic-writing-skills/latex-paper-en`
- `academic-writing-skills/latex-thesis-zh`
- `academic-writing-skills/typst-paper`
- `academic-writing-skills/paper-audit`
- `academic-writing-skills/industrial-ai-research`

### Manual Copy Example

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE/.claude/skills" -Force
Copy-Item -Recurse "academic-writing-skills/latex-paper-en" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/latex-thesis-zh" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/typst-paper" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/paper-audit" "$env:USERPROFILE/.claude/skills/"
Copy-Item -Recurse "academic-writing-skills/industrial-ai-research" "$env:USERPROFILE/.claude/skills/"
```

Adjust the target directory to your local skill runtime if you are not using `~/.claude/skills`.

## Toolchain Checks

Use these checks only to verify environment availability:

```bash
uv --version
python --version
pdflatex --version
xelatex --version
typst --version
chktex --version
```

## Optional but Recommended Tools

```bash
# macOS
brew install chktex biber typst

# Ubuntu / Debian
sudo apt-get install chktex biber
```

`latexmk` and core TeX tools are usually bundled with TeX distributions.

## Verify the Repository Setup

From the repo root:

```bash
uv run ruff check .
uv run pyright
uv run python -m pytest tests/
```

## Run the Docs Site

```bash
cd docs
npm install
npm run docs:dev
```

## Troubleshooting

### `pdflatex` or `xelatex` not found

Install a LaTeX distribution and ensure its binaries are on `PATH`.

### `typst` not found

Install `typst-cli` and confirm `typst --version` works.

### `uv run python` fails

Run `uv sync` in the repository root first.
