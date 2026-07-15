# 双语文档重构执行计划

## Preconditions

- Parent and all children remain `planning` until this artifact set is reviewed.
- Inline mode is active; no implementation/check sub-agents are dispatched.
- Existing dirty `README*` and Trellis runtime changes remain outside all child scopes.

## Ordered Checklist

### 1. Core contract

- [ ] Start `07-14-docs-bilingual-core`, not the parent.
- [ ] Implement canonical resource inventory, manifest and sync checker.
- [ ] Replace manual resource sidebars with deterministic filesystem-backed groups.
- [ ] Migrate core pages and define the shared skill-overview format.
- [ ] Add focused contract tests and prove a clean baseline with an empty/controlled migration state.
- [ ] Review, commit and archive the core child before starting translation children.

### 2. Two-direction pilots

- [ ] Implement `07-14-docs-bib-search-citation` as the small English-to-Chinese pilot.
- [ ] Verify all 6 resources per locale, overview parity, manifest hashes and build.
- [ ] Implement `07-14-docs-latex-thesis-zh` as the Chinese-to-English pilot.
- [ ] Verify all 48 resources per locale, especially abstract, conclusion and chapter-guide constraints.

### 3. Remaining skill slices

- [ ] Implement `07-14-docs-cover-letter` (24 resources per locale).
- [ ] Implement `07-14-docs-paper-audit` (57 resources per locale, including public agent contracts).
- [ ] Implement `07-14-docs-latex-paper-en` (65 resources per locale).
- [ ] Implement `07-14-docs-typst-paper` (50 resources per locale).
- [ ] For every child: run manifest/structure checks, build docs, inspect representative translations,
      commit only that child, then archive it before proceeding.

### 4. Parent integration review

- [ ] Confirm all 7 children are completed and the parent task map is satisfied.
- [ ] Re-read all six `SKILL.md` routers and Reference Maps against final overviews/navigation.
- [ ] Confirm exactly one English and one Chinese canonical page exists for every public resource.
- [ ] Confirm no legacy resource paths remain and no current page links to them.
- [ ] Inspect home, installation, quick-start, usage and all skill indexes in both locales.
- [ ] Run the full verification ladder and record exact results.
- [ ] Keep unrelated pre-existing dirty files out of commits and task archive bookkeeping.

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
