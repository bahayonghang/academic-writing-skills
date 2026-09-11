# Per-paper observation schema

每个 Elsevier 条目一份 `materials/Elsevier/observations/<KEY>.md`。`<KEY>` 为 Zotero item key。字段对齐 `materials/IEEE/observations/_schema.md`，节枚举与故事 ID 换成 Elsevier。

## Frontmatter

```yaml
key: <ZOTERO_KEY>
title: "<verbatim title>"
venue: "Journal of Process Control"
doi: "10.1016/..."
item_type: journalArticle
has_pdf: true
status: complete          # complete | degraded
pages_read: "1-4"
date_observed: 2026-09-11
story_pattern: SP-ELS-001  # 未知则 pending
```

`status=degraded`：无 PDF。仍须写摘要级观察。

## Body

与 IEEE 相同九节：Structure、Openers、Gap transitions、Hedge verbs、Cross-section linkers、Candidate rules、Candidate phrases、House style、Quotes。

`In this paper` / `this paper proposes` / `this article` 进 phrase_bank，不进 anti_ai_patterns。

## Extraction

`zot --json item get` → `item children` → 有 PDF 则 `item pdf --pages`。无 PDF 只用题录与 `abstractNote`。原句保持 PDF 文本，拼回 `U+0002` 断词。

## 晋升

先写 observation，再改 TSV。`writing_rules` / `phrase_bank`：`paper_count >= 3` 升 `core`。
