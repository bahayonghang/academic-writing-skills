# C4 acceptance notes

Date: 2026-09-07. Implementer ran the isolation CLI and the docs contract tests. Main session still owns resource sync, `just doc-build`, and full `git diff --check`.

## Isolation CLI (shipped `audit.py`)

Fixture: `tests/fixtures/paper_audit/sample_paper.tex`. Command: `python -B <tmp>/paper-audit/scripts/audit.py <fixture> --mode quick-audit --lang en --format json`. Child env: `PYTHONIOENCODING=utf-8`, `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`.

| Layout | exit | RUN | missing |
| --- | --- | --- | --- |
| tmp full sibling copy (all six skill dirs) | 0 | 11 | 0 |
| tmp paper-audit-only copy | 0 | 3 | 8 |

Standalone missing=8 is the recorded limited-coverage boundary. `audit.py` exit/gate behavior was not changed.

## Commands run by implementer

```text
uv run --extra dev python -m pytest tests/skills/paper_audit/test_installed_layout.py tests/contracts/test_docs_bilingual_resources.py -q
```

Result: 11 passed, exit 0 (second run 2.88s after locking full RUN=11).

```text
uv run --extra dev ruff format --check tests/skills/paper_audit/test_installed_layout.py
uv run --extra dev ruff check tests/skills/paper_audit/test_installed_layout.py
```

Result: already formatted; All checks passed; exit 0.

```text
git diff --check -- <C4 files>
```

Result: exit 0 on C4 paths.

## UNVERIFIED

- `npx skills add` installer
- symlink layout
- five-tool runtime (fresh session, delegation, hooks trust)

No captured real run was authorized.
