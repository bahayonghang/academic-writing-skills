# `bib-search-citation`

Fast `.bib` library search and citation extraction for BibTeX and BibLaTeX workflows, including Zotero exports with custom metadata fields.

## Use It For

- Search large `.bib` libraries by topic words and field-specific filters.
- Filter by author, year, entry type, DOI, arXiv/eprint, PDF, code, keywords, annotation, or abstract.
- Generate LaTeX and Typst citation snippets.
- Return raw BibTeX for export or manual verification.
- Preview JSON search results as compact human-readable summaries.

## Do Not Use It For

- Validate citations already used inside a `.tex` or `.typ` project; use the writing skill bibliography module.
- Compile, format, or edit manuscripts.
- Rewrite Related Work prose.
- Online literature discovery when no local bibliography exists.
- Treat a citation key as proof that a manuscript claim is supported.

## Module Router

| Surface | Use when | Primary command |
| --- | --- | --- |
| `query` | One-shot compact search | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"` |
| `spec-json` | Structured filters are clearer than a compact query | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-json '{"query":"mamba forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | You need a repeatable saved search | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-file search.json` |
| `preview` | You already have JSON results and need a short summary | `uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## Minimum Inputs

- Path to one local `.bib` file.
- Compact `--query`, inline `--spec-json`, or saved `--spec-file`.
- Optional sort, limit, citation mode, raw BibTeX, or returned-field preferences.

## Output Artifacts

- Structured JSON search results.
- Optional raw BibTeX entries.
- LaTeX and/or Typst citation snippets.
- Compact preview output via `preview_bib_search.py`.

## Common Requests

```text
Search references.bib for Cheng papers after 2024 on Mamba forecasting and return both LaTeX and Typst citations.
```

```text
Find entries whose annotation contains CodeAvailable and show raw BibTeX.
```

```text
List the newest transformer forecasting papers but require DOI and exclude misc entries.
```

```text
Find the best TimeMachine match and return one raw entry plus citation snippets.
```

## Notes

- Run the smallest module that can answer the request before escalating to broader review.
- Preserve citations, labels, math, and source structure unless the user explicitly asks for edits.
- Use `paper-audit` after source-level compile and bibliography checks are stable when the goal is submission readiness.
