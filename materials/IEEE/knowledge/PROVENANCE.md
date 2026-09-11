# Provenance

date: 2026-09-11

- n_inventory: 353
- n_observed: 353
- n_complete: 261
- n_degraded: 92

## Filter

Metadata gate in `corpus/FILTER.md`. Corpus keys copied from `.trellis/tasks/09-11-ieee-writing-materials/research/ieee-inventory.json`. Fulltext search is not the corpus.

## Coverage

- 261 篇有可用 PDF，observation `status=complete`
- 91 篇无 PDF + 1 篇附件不足一页（`H8QUU5A7`），observation `status=degraded`
- `writing_rules` / `phrase_bank` / `paper_story_patterns` / `domain_register` 已按 261 篇 complete 正文回计
- `opener_distribution` / `gap_transitions` / `hedge_verbs` / `cross_section_linkers` / `section_openers` 仍含早先逐篇累计行，不是 261 篇全量重聚

## Promotion

- `writing_rules` / `phrase_bank` stay `candidate` until `paper_count >= 3` and the category is stable, then `core`.
- Statistical tables have no core flag.
- `references/` may cite `core` rows, or a section opener with `paper_count >= 5`.

## Isolation

No Nature prior rows copied from `ref/nature-writing-studio/skill/knowledge/*.tsv`. Catalog skills under `academic-writing-skills/` are not modified.

## Scripts

- `scripts/next_pending.py` — next inventory item with `status=pending`
- `scripts/validate_knowledge.py` — TSV headers, inventory↔observation alignment, core threshold
- `scripts/mark_observed.py` — sync inventory status from observation files
- `scripts/aggregate_counts.py` — recount core rules/phrases/story from complete observations
