# 双语文档重构执行计划

## Preconditions

- Parent and all children remain `planning` until this artifact set is reviewed.
- Inline mode is active; no implementation/check sub-agents are dispatched.
- Existing dirty `README*` and Trellis runtime changes remain outside all child scopes.

## Ordered Checklist

### 1. Core contract

- [x] Start `07-14-docs-bilingual-core`, not the parent.
- [x] Implement canonical resource inventory, manifest and sync checker.
- [x] Replace manual resource sidebars with deterministic filesystem-backed groups.
- [x] Migrate core pages and define the shared skill-overview format.
- [x] Add focused contract tests and prove a clean baseline with an empty/controlled migration state.
- [x] Review, commit and archive the core child before starting translation children.

### 2. Two-direction pilots

- [x] Implement `07-14-docs-bib-search-citation` as the small English-to-Chinese pilot.
- [x] Verify all 6 resources per locale, overview parity, manifest hashes and build.
- [x] Implement `07-14-docs-latex-thesis-zh` as the Chinese-to-English pilot.
- [x] Verify all 48 resources per locale, especially abstract, conclusion and chapter-guide constraints.

### 3. Remaining skill slices

- [x] Implement `07-14-docs-cover-letter` (24 resources per locale).
- [x] Implement `07-14-docs-paper-audit` (57 resources per locale, including public agent contracts).
- [x] Implement `07-14-docs-latex-paper-en` (65 resources per locale).
- [x] Implement `07-14-docs-typst-paper` (50 resources per locale).
- [x] For every child: run manifest/structure checks, build docs, inspect representative translations,
      commit only that child, then archive it before proceeding.

### 4. Parent integration review

- [x] Confirm all 7 children are completed and the parent task map is satisfied.
- [x] Re-read all six `SKILL.md` routers and Reference Maps against final overviews/navigation.
- [x] Confirm exactly one English and one Chinese canonical page exists for every public resource.
- [x] Confirm no legacy resource paths remain and no current page links to them.
- [x] Inspect home, installation, quick-start, usage and all skill indexes in both locales.
- [x] Run the full verification ladder and record exact results.
- [x] Keep unrelated pre-existing dirty files out of commits and task archive bookkeeping.

## Validation Commands

Run with `rtk` on this Windows host:

```powershell
rtk uv run python docs/scripts/check_resource_sync.py
rtk uv run pytest tests/contracts/test_docs_bilingual_resources.py -q
rtk npm --prefix docs run docs:build
rtk uv run ruff format --check .
rtk uv run ruff check .
rtk uv run pyright
rtk uv run pytest
rtk git diff --check
```

Attempt `rtk just ci` when available. If the Windows shell cannot execute the `just` recipes, the
underlying commands above are the authoritative recorded ladder.

## Review Gates

- Core child: manifest and path contract reviewed before any bulk migration.
- Pilot children: one English-origin and one Chinese-origin package pass before large packages.
- Per child: no source changes, no cross-skill translation changes, no unresolved checker exception.
- Parent: all bilingual coverage, navigation and build checks pass from the combined tree.

## Rollback Points

- After core contract commit.
- After each skill child commit and archive.
- Before parent integration cleanup.

Do not partially roll back the canonical path contract while retaining child translations that rely on it.

## Final Validation Evidence

- `check_resource_sync.py`: all 250 manifest entries passed.
- `pytest tests/contracts/test_docs_bilingual_resources.py -q`: 10 passed.
- `npm --prefix docs run docs:build`: passed with VitePress 1.6.4 and no dead links.
- Clean detached-worktree `just ci`: passed version alignment, Ruff format/check, Pyright
  (0 errors, 73 warnings), and the full pytest suite.
- Current dirty-worktree `just ci`: version gate fails because unrelated parallel work changes
  `pyproject.toml` to 6.0.0 while the six skill versions remain 5.3.0; no version files were
  included in this task.
- Seven child task directories confirmed under `.trellis/tasks/archive/2026-07/`.
