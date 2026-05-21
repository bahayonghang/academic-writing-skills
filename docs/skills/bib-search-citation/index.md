# `bib-search-citation`

Fast `.bib` library search and citation extraction for BibTeX and BibLaTeX workflows.

## Use It For

- searching large `.bib` libraries by topic
- filtering entries by author, year, type, DOI, arXiv, keywords, annotation, or abstract
- generating LaTeX and Typst citation snippets from matched entries
- returning raw BibTeX for export or manual verification
- triaging Zotero-exported libraries with mixed custom fields
- checking which entries appear to include code, PDF, DOI, keywords, or abstracts

## Do Not Use It For

- validating citations inside a `.tex` or `.typ` project
- compile or format diagnostics
- rewriting related-work prose
- online paper discovery when there is no local bibliography file

## Search Router

| Surface | Best for | Command |
| --- | --- | --- |
| `query` | one-shot compact search | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"` |
| `spec-json` | repeatable structured filters | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-json '{"query":"mamba time series forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | saved search workflow | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-file search.json` |
| `preview` | compact human-readable summary after JSON output | `uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## Minimum Inputs

- a `.bib` file path
- either a compact query or a JSON spec
- optional sort, limit, and citation-mode preferences
- optional request for raw BibTeX or custom returned fields

## Good First Requests

```text
Search references.bib for Cheng papers after 2024 on Mamba forecasting and return both LaTeX and Typst citations.
```

```text
Find entries in library.bib whose annotation contains CodeAvailable and show the raw BibTeX.
```

```text
List the newest transformer forecasting papers in references.bib, but exclude misc entries and require DOI.
```

```text
Find the best TimeMachine match in references.bib and return one raw entry plus cite snippets.
```

## Read This Next

- [Query Syntax](./resources/query-syntax.md)

## Important Notes

- `search_bib.py` is the source of truth for filtering, ranking, and citation formatting.
- `preview_bib_search.py` only renders JSON results into a shorter summary.
- Compact filters support `author:`, `year>=`, `year<=`, `type:`, `has:`, `fields:`,
  `cite:`, and `raw:true`.
- `has:code` is inferred from fields such as `url`, `annotation`, `keywords`, `note`,
  `howpublished`, and `abstract`.
- A `.bib` match, citation key, DOI, arXiv ID, or URL is bibliography
  provenance, not proof that the paper supports a manuscript claim.
- If the query contains only filters and no topic words, the sort mode controls result order.
- Malformed entries may be skipped during parsing, so unexpectedly small result sets can come
  from broken BibTeX structure or encoding issues.
