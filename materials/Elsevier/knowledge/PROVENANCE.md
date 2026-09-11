# Provenance

date: 2026-09-11

- n_inventory: 150
- n_observed: 150
- n_complete: 98
- n_degraded: 52

## Filter

Metadata gate plus 10-title allowlist in `corpus/FILTER.md`. Keys copied from `.trellis/tasks/09-11-elsevier-writing-materials/research/elsevier-inventory.json`. Fulltext search is not the corpus. `Energy` is exact-title only.

## Promotion

- `writing_rules` / `phrase_bank` stay `candidate` until `paper_count >= 3`, then `core`.
- Statistical tables have no core flag.
- `references/` may cite `core` rows, or a section opener with `paper_count >= 5`.

## Isolation

No Nature or IEEE TSV data rows copied. Catalog skills under `academic-writing-skills/` are not modified. `materials/IEEE/` is read-only.

## Scripts

- `scripts/next_pending.py`
- `scripts/validate_knowledge.py` — mid-run use `--allow-pending`
