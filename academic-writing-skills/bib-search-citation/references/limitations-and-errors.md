# Known Limitations and Error Handling

## Known limitations

These are documented so results are reported honestly, not silently:

- **Author matching** is a case-insensitive, accent-folded substring test on the
  raw author string. It does not normalise name order, so `author:"Jane Doe"`
  will not match a `{Doe, Jane}` field; search by surname (`author:Doe`) instead.
  Substring matching also means `author:chen` matches both `Chen` and `Cheng` —
  convenient, but verify the author before citing.
- **`matched_entries`** counts entries that pass the structured filters; it does
  not reflect how many were dropped by the free-text relevance threshold.
- **CJK multi-keyword** queries match best as a contiguous substring
  (`时间序列`); space-separated CJK terms may not all match.
- **Multi-file libraries** are not merged automatically — run the script once per
  `.bib` file. The `meta.parse_warnings` list reports parsing problems: entries
  skipped over a structural defect such as a missing closing brace, duplicate
  citation keys (each affected result also carries a `warnings` field), and
  entries sitting behind a `%` marker, which real BibTeX still parses.
- **`has:code` is a word-boundary heuristic**, not a semantic classifier. It
  avoids substring matches such as `reported`, `encoder`, and `barcode`, but it
  does not understand negation (`without a linked repository` still matches) or
  reject generic phrases such as `dress code`.
- **Unbalanced compact-query quotes** trigger a tokenizer fallback instead of an
  error. Double-quoted phrases still group, while single quotes are treated as
  literal characters; the fallback is reported as `query_tokenizer_fallback` in
  `meta.parse_warnings`.
- **Year disambiguation suffixes** accept one lowercase ASCII letter, so `2024a`
  is filtered as year 2024. Longer or uppercase suffixes are not interpreted as
  BibTeX year disambiguation markers.

## Error handling

### Parse errors

If a `.bib` file contains malformed entries, the script processes the valid
entries it can parse. When unexpectedly few entries are returned, inspect the
file encoding and look for obvious structural corruption such as missing closing
braces.

### Empty result sets

When zero entries match, suggest broadening the search in this order:

1. remove `has:` constraints such as `has:code`
2. widen or remove the year range
3. use fewer or shorter topic keywords
4. check author spelling or try partial-name matches

### Large files

The helper scripts use linear scans and no external parser dependency. For very
large libraries, expect proportionally longer runtime but the same JSON contract.
