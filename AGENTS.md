# AGENTS.md - Academic Writing Skills

> Rules and conventions for agentic coding in this repository

## Project Overview

This repo ships **Claude Code skills** for academic paper editing (LaTeX/Typst). Each skill is a self-contained folder under `academic-writing-skills/` with its own `SKILL.md`, `scripts/`, and `resources/`.

## Build/Test/Lint Commands

```bash
# Development setup
uv sync --extra dev

# Run all CI checks
just ci                    # Full pipeline: lint + typecheck + test
just lint                  # Ruff format check + lint
just fix                   # Auto-fix lint/format issues
just format                # Format only

# Type checking
just typecheck             # Pyright static analysis

# Testing
just test                  # Run all tests
uv run --extra dev python -m pytest tests/ -v
uv run --extra dev python -m pytest tests/test_parsers.py -v          # Single test file
uv run --extra dev python -m pytest tests/test_parsers.py::test_latex_split_sections -v  # Single test

# Documentation (VitePress)
cd docs && npm install && npm run docs:dev    # Dev server
cd docs && npm run docs:build                 # Production build

# Cleanup
just clean                 # Remove __pycache__, .pytest_cache, etc.
```

## Code Style Guidelines

### Python

- **Formatter**: Ruff (line-length: 100)
- **Python version**: 3.10+ (type hints required)
- **Import style**: Use `from __future__ import annotations` where needed
- **Typing**: Use modern syntax (`dict[str, int]`, `list[str] | None`)

### Naming Conventions

- **Modules**: `snake_case.py` (e.g., `check_format.py`, `verify_bib.py`)
- **Classes**: `PascalCase` (e.g., `LatexParser`, `DocumentParser`)
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore` for internal helpers

### Imports (Ruff-enforced)

```python
# Standard library
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

# Third-party (if any)

# First-party
# (scripts are added to sys.path via conftest.py)
```

### Error Handling

- Prefer explicit error messages over silent failures
- Use `Path` for file operations with proper existence checks
- Log warnings for recoverable issues, raise for critical errors

### Type Safety

- All functions must have type annotations
- Use `Any` sparingly; prefer specific types
- Pyright runs in `typeCheckingMode = "off"` (import checking only)

## Skill Development Rules

### Critical Constraints (Never Break)

1. **Never touch** LaTeX inside `\cite{}`, `\ref{}`, `\label{}` or math environments
2. **Never touch** Typst inside `@cite`, `<label>`, or `$...$` math
3. **Never fabricate** bibliography entries; only operate on existing `.bib` or `.yml`
4. Don't change protected terminology without permission (see `references/FORBIDDEN_TERMS.md`)
5. Prefer **commented diff/suggestion blocks** over silent rewrites

### Skill Structure

Each skill lives under `academic-writing-skills/<skill-name>/`:

```
<skill-name>/
├── SKILL.md              # Entry point / skill definition
├── README.md             # User-facing documentation
├── scripts/              # Python tooling
│   ├── parsers.py        # Document parsing (shared pattern)
│   └── *.py              # Feature scripts
└── resources/            # Reference docs
    ├── modules/          # Instruction modules
    └── references/       # Style guides, standards
```

### Script Patterns

- Parse documents using `parsers.py` abstractions (`LatexParser`, `TypstParser`)
- Output suggestions in diff-comment format with severity/priority markers
- Keep changes minimal and scoped to the relevant skill

### Testing

- Tests live in `tests/` (not inside skill folders)
- Add script directories to `sys.path` in `conftest.py` for imports
- Use pytest fixtures for parser instances
- Test both LaTeX and Typst variants where applicable

## Key Directories

- `academic-writing-skills/latex-paper-en/` - English LaTeX papers (IEEE/ACM/NeurIPS)
- `academic-writing-skills/latex-thesis-zh/` - Chinese theses (GB/T 7714)
- `academic-writing-skills/typst-paper/` - Typst documents (bilingual)
- `academic-writing-skills/paper-audit/` - Automated paper auditing
- `academic-writing-skills/industrial-ai-research/` - Industrial AI research skill
- `tests/` - pytest test suite
- `docs/` - VitePress documentation site

## Common Tasks

### Add a new script to an existing skill

1. Create `scripts/<feature>.py` following existing patterns
2. Add tests in `tests/test_<feature>.py` (or extend existing)
3. Update `SKILL.md` with invocation keywords
4. Run `just ci` before committing

### Update shared behavior

If changing behavior used by multiple skills (e.g., `parsers.py`):
- Check all skills' scripts for alignment
- Ensure backward compatibility
- Update tests for all affected skills

### Adding tests for script modules

```python
# In conftest.py, ensure script path is added:
SCRIPT_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "<skill>" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Then import directly:
from parsers import LatexParser
```
