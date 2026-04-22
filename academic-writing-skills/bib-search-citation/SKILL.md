---
name: bib-search-citation
description: >-
  Search, filter, and format entries from BibTeX or BibLaTeX .bib files for
  research workflows. Use when a user wants to find papers, search a
  bibliography, filter a library, or look up references by topic, author, year,
  venue, DOI, arXiv ID, keywords, annotation, abstract, or entry type. Handles
  Zotero-exported libraries. Supports compact search expressions such as
  author:, year-gte, type:, and has:, combined filters, research-oriented
  output fields, raw
  BibTeX export, and LaTeX/Typst citation snippet generation.
category: docs-writing-publishing
tags: [bibtex, biblatex, citation, latex, typst, bibliography, research, zotero, bib]
version: "1.1.0"
allowed-tools: Read, Bash
---

# Bib Search Citation

## Overview

Use this skill when the user provides a `.bib` file and wants research-oriented retrieval rather than just a single citation key lookup. This skill is designed for large bibliographies with mixed standard and custom fields, including fields such as `shorttitle`, `annotation`, `keywords`, `abstract`, and `file`.

Follow this workflow:

1. Identify the `.bib` file to use.
2. If `rtk` is available, prefer it for exploratory steps such as locating `.bib` files and inspecting representative fields.
3. Translate the user's request into either a JSON search spec or a compact query expression.
4. Run `scripts/search_bib.py` on the `.bib` file and keep its JSON output uncompressed.
5. Optionally pipe the JSON into `scripts/preview_bib_search.py` for a compact human-readable summary.
6. Review the results and present the best matches clearly.
7. Include LaTeX and/or Typst citation snippets whenever the user asks for them or would benefit from them.

## Input expectations

The typical input is:

- one `.bib` file provided by the user
- a natural-language research query
- optional structured filters such as year range, entry type, author, DOI presence, code availability, or custom field matches
- optional compact filters such as `author:cheng year>=2024 has:code type:article`
- optional output preferences such as `latex`, `typst`, `both`, or raw BibTeX

If the user gives a natural-language request only, infer a reasonable search spec and say what assumptions you made. If the user writes a compact filter expression directly, preserve it as closely as possible instead of converting it into vague prose.

## Search planning

Before running the script, map the request into a search spec.

### Common spec fields

- `query`: free-text topic query
- `filters.year_min`, `filters.year_max`, `filters.years_in`, `filters.exclude_years`
- `filters.author_contains`, `filters.author_excludes`
- `filters.type_in`, `filters.exclude_type_in`
- `filters.has`, `filters.exclude_has`
- `filters.field_contains`, `filters.field_excludes`
- `sort`: `relevance`, `year_desc`, `year_asc`, or `title`
- `limit`: default 5 unless the user asks for more
- `return_fields`: fields to expose in the answer
- `include_raw_bib`: `true` when the user asks for the original entry or when exact export matters
- `citation_mode`: `latex`, `typst`, `both`, or `none`

### Heuristics for natural-language requests

Use these defaults unless the user says otherwise:

- research discovery request -> `sort: relevance`
- no explicit limit -> `limit: 5`
- no explicit field list -> return the research-oriented default fields: `key`, `title`, `shorttitle`, `author`, `year`, `venue`, `doi`, `eprint`, `keywords`, `annotation`, `abstract`
- asks for "original", "full entry", or "bib" -> `include_raw_bib: true`
- asks for both LaTeX and Typst, or just says "citation" in a mixed writing workflow -> `citation_mode: both`

### Compact query language

The script can parse direct query expressions inside `--query`, and it can also parse them when they appear inside `spec.query`.

Supported compact operators:

- `author:cheng`
- `year>=2024`
- `year:2024` or `year:2023,2024`
- `type:article,misc`
- `-type:misc`
- `has:code,doi`
- `-has:pdf`
- `annotation:CodeAvailable`
- `keywords:mamba`
- `sort:year_desc`
- `limit:10`
- `fields:key,title,year,doi`
- `cite:latex`, `cite:typst`, or `cite:both`
- `raw:true`

Unstructured tokens that do not match the compact syntax remain part of the topic query.

### Supported `has` values

The script supports these useful `has` values:

- `doi`
- `abstract`
- `keywords`
- `annotation`
- `shorttitle`
- `eprint`
- `pdf`
- `code`

`code` is inferred from fields such as `url`, `abstract`, `keywords`, `annotation`, `note`, or `howpublished` that mention GitHub, GitLab, code, repository, or source.

For more examples, see `references/query-syntax.md`.

## Running the script

Run the script with a JSON spec, a spec file, or a compact query.

## RTK Fast Path

If `rtk` is available, prefer it only for model-facing exploration:

- locate bibliography files with `rtk find . -name "*.bib"`
- inspect a representative slice with `rtk read /path/to/library.bib -l aggressive -m 80`
- confirm whether fields such as DOI, keywords, annotation, or eprint are present with `rtk grep "doi|keywords|annotation|eprint" /path/to/library.bib`

Keep machine-readable search results on the raw script path:

- use raw `python scripts/search_bib.py ...` whenever another tool or script needs JSON
- do not wrap `search_bib.py` output with RTK compression
- use `python scripts/preview_bib_search.py` only after JSON has already been produced

### Inline JSON example

```bash
python scripts/search_bib.py \
  --bib /path/to/library.bib \
  --spec-json '{
    "query": "mamba time series forecasting author:Cheng year>=2024 has:code",
    "sort": "relevance",
    "limit": 5,
    "citation_mode": "both",
    "include_raw_bib": false
  }'
```

### Compact query example

```bash
python scripts/search_bib.py \
  --bib /path/to/library.bib \
  --query 'mamba time series forecasting author:Cheng year>=2024 has:code type:article,misc cite:both limit:5'
```

### Spec file example

```bash
python scripts/search_bib.py --bib /path/to/library.bib --spec-file /path/to/spec.json
```

### Human-readable preview example

```bash
python scripts/search_bib.py \
  --bib /path/to/library.bib \
  --query 'mamba time series forecasting author:Cheng year>=2024 has:code type:article,misc cite:both limit:5' \
| python scripts/preview_bib_search.py
```

If the user uploads a `.bib` file into the conversation, first make sure you know its local path in the execution environment, then run the script against that file.

## Output expectations

When presenting results to the user, prefer this order:

1. brief summary of how many strong matches were found
2. top matches with the requested research fields
3. citation snippets in the requested format
4. raw BibTeX only when requested or materially useful

For each selected entry, usually include:

- citation key
- title and optional shorttitle
- authors
- year and venue
- DOI and/or eprint when present
- the most relevant supporting fields for the query, such as keywords, annotation, or a short abstract excerpt

If the user asked for a compact query, it is helpful to echo the interpreted filters briefly, especially when negation or multiple field filters are involved.

When using the preview helper:

- treat it as a compact rendering of the JSON, not as a separate search engine
- keep `search_bib.py` as the source of truth for filtering, scoring, sorting, and citations
- do not rely on the preview output when exact raw BibTeX preservation matters

## Citation formatting rules

### LaTeX

When `citation_mode` includes `latex`, expose:

- `\\cite{key}`
- `\\parencite{key}`
- `\\textcite{key}`

These are intended for `biblatex` workflows. If the user only wants one form, show only that form.

### Typst

When `citation_mode` includes `typst`, expose:

- `@key` when the key is simple enough for shorthand usage
- `#cite(<key>)` when shorthand is fine
- `#cite(label("key"))` when the key contains characters that make shorthand fragile

If the script reports `typst.needs_label = true`, prefer the explicit `label("...")` form instead of shorthand.

## Result quality checks

Before answering:

- make sure the returned entries satisfy the user's explicit filters
- do not overclaim topic relevance; if results are only approximate, say so
- when several entries are similar, explain the difference briefly
- preserve raw BibTeX exactly when quoting the original entry

## Error handling

### Parse errors

If the `.bib` file contains malformed entries (unbalanced braces, encoding issues, truncated fields), the script skips those entries silently and processes the rest. When a file fails to parse entirely, check the encoding (the script assumes UTF-8) and look for obvious structural corruption such as missing closing braces.

### Empty result sets

When zero entries match, suggest broadening the search:

- remove `has:` constraints (e.g. `has:code` excludes many entries)
- widen the year range or drop it entirely
- use fewer or shorter topic keywords
- check author name spelling or try partial matches

### Large file performance

The script is pure Python with a linear scan and no external dependencies. For typical academic libraries (up to ~10,000 entries) it completes in seconds. For very large files (50,000+ entries), expect proportionally longer runtimes but no functional issues.

## Resources

- `scripts/search_bib.py`: parses `.bib` files, applies filters, ranks results, and formats citation snippets
- `scripts/preview_bib_search.py`: renders `search_bib.py` JSON into a compact human-readable summary
- `references/query-syntax.md`: examples for mapping user requests into structured search specs and compact expressions
