# `bib-search-citation`

Search and cite from one local BibTeX/BibLaTeX `.bib` library, including Zotero exports
with custom metadata fields.

## Use It For

- Search by topic, author, year, venue, DOI, arXiv/eprint, keywords, annotation, or abstract.
- Combine compact filters such as `year>=2024`, `has:code`, and `cite:both`.
- Return stable JSON, exact raw BibTeX, or LaTeX/Typst citation snippets.
- Preview saved JSON results as a compact human-readable summary.
- Add lexical claim-overlap and recency metadata as verification handoffs.

## Do Not Use It For

- Validate citations already used in a manuscript; use the writing skill's bibliography module.
- Compile, format, or rewrite `.tex` or `.typ` projects.
- Run online discovery without a local `.bib` file.
- Treat a bibliography match or lexical overlap as proof that a paper supports a claim.
- Invent metadata missing from the source library.

## Module Router

| Module | Use when | Primary command |
| --- | --- | --- |
| `query` | One-shot compact search with inline filters | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query 'mamba forecasting author:Cheng year>=2024 has:code cite:both limit:5'` |
| `spec-json` | A complex request needs explicit structured filters | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --spec-json '{"query":"mamba forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | A saved search must be repeatable | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --spec-file search.json` |
| `preview` | Search JSON already exists and needs a short summary | `uv run python -B academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## Minimum Inputs

- One local `.bib` path.
- One compact `--query`, inline `--spec-json`, or saved `--spec-file`.
- Optional sort, limit, return fields, citation mode, raw-export, recency, or claim preferences.

## First Commands

```bash
uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query 'transformer forecasting year>=2024 has:doi cite:both limit:5'
uv run python -B academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json
```

`search_bib.py` owns parsing, filtering, scoring, sorting, raw-entry preservation, and citation
generation. `preview_bib_search.py` only renders existing JSON.

## Output Artifacts

- Structured JSON with interpreted filters and matching entries.
- Requested bibliographic fields and provenance identifiers.
- Optional exact `raw_bib`.
- Optional LaTeX and Typst citation snippets.
- Additive `meta.recency` and per-result `claim_support` with explicit caveats.

## Public Resources

### References

- [Query syntax](./resources/references/query-syntax.md)
- [Search planning defaults](./resources/references/search-planning.md)
- [Known limitations and errors](./resources/references/limitations-and-errors.md)

### Examples

- [Compact query](./resources/examples/compact-query.md)
- [Raw BibTeX export](./resources/examples/raw-bib-export.md)
- [Preview summary](./resources/examples/preview-summary.md)

## Common Requests And Handoffs

Use this skill for local retrieval and citation-ready output. Hand off to a writing skill when
citations must be checked inside manuscript source, and to a research verification workflow when
the paper's content must be read to determine whether it supports a claim.
