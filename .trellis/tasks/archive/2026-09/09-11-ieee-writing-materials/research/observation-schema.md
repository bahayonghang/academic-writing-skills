# Per-paper observation schema

每个 IEEE 条目一份 `materials/IEEE/observations/<KEY>.md`。`<KEY>` 为 Zotero item key。

## Frontmatter

```yaml
key: ZVIVPYR4
title: "<verbatim title>"
venue: "IEEE Transactions on Industrial Informatics"  # or early-access
doi: "10.1109/TII.2025.3567401"
item_type: journalArticle
has_pdf: true
status: complete          # complete | degraded
pages_read: "1-4"         # zot item pdf --pages; degraded 可空
date_observed: 2026-09-11
story_pattern: SP-IEEE-001  # 未知则 pending
```

`status=degraded`：无 PDF。仍须写摘要级观察，可少于 3 条正文信号。

## Body

1. `## Structure`：罗马数字标题原文；节序；有无独立 Related Work。
2. `## Openers`：每节首句 3-gram + 原句。
3. `## Gap transitions`：Although / However / Despite / To address 等转折 + 原句。
4. `## Hedge verbs`：propose / demonstrate / show / indicate / may 等 + 所在节。
5. `## Cross-section linkers`：节与节之间的衔接句。
6. `## Candidate rules`：本篇才看到的写法规则，带原句；此时尚未晋升。
7. `## Candidate phrases`：可复用句槽，带原句。
8. `## House style`：IEEE 常见自称（`In this paper` / `This paper proposes` / `This study introduces`）。此类进 `phrase_bank`，默认不进 `anti_ai_patterns`。
9. `## Quotes`：所有 exemplar 的原文，一行一条，可回溯页码。

## Extraction

有 PDF：`zot --json item get <KEY>`，`zot --json item children <KEY>`，`zot --json item pdf <KEY> --pages <range>`。先 1–3 页拿 Abstract / Index Terms / Introduction；再按目录补 Method / Experiments / Conclusion。

无 PDF：只用 `item get` 的 title、abstract_note、venue。禁止用全文检索里的非 IEEE 命中补证据。

原句保持 PDF 文本。断词符 `U+0002` 与行末连字符在摘录时拼回单词，不改用词。

## 晋升（与 design 一致）

Observation 写完后才改 TSV：

- 统计表（opener / gap / hedge / linker / section_openers）：命中则 `occurrences+1`，`paper_count` 按去重 key 计，`top_papers` 最多 5 个 key。
- `writing_rules` / `phrase_bank`：1–2 篇为 `candidate`；`paper_count >= 3` 且类别稳定后升 `core`。
- `references/` 只引用 `core` 行，或统计表中该节 `paper_count >= 5` 的前 10 个 opener。
