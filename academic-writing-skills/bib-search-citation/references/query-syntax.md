# Query Syntax Guide

This reference helps map literature requests into a search spec for `scripts/search_bib.py`.

## Two supported input styles

The script supports both of these styles:

1. a JSON search spec
2. a compact query expression

Use the compact form when the user naturally writes something like:

```text
time series forecasting mamba author:Cheng year>=2024 has:code type:article,misc cite:both
```

Use the JSON form when the workflow already has a structured spec or when many filters need to be explicit.

## JSON search spec shape

```json
{
  "query": "mamba time series forecasting",
  "filters": {
    "year_min": 2024,
    "year_max": 2026,
    "author_contains": ["Cheng"],
    "type_in": ["article", "misc"],
    "has": ["code", "abstract"],
    "exclude_has": ["pdf"],
    "field_contains": {
      "annotation": ["CodeAvailable"],
      "keywords": ["forecasting"]
    }
  },
  "sort": "relevance",
  "limit": 5,
  "return_fields": [
    "key",
    "title",
    "shorttitle",
    "author",
    "year",
    "venue",
    "doi",
    "eprint",
    "keywords",
    "annotation",
    "abstract"
  ],
  "include_raw_bib": true,
  "citation_mode": "both"
}
```

## Compact query language

### Core syntax

- plain words remain the theme query
- `author:cheng` -> author contains `cheng`
- `year>=2024` -> year minimum is 2024
- `year<=2025` -> year maximum is 2025
- `year:2024` -> exact year 2024
- `year:2023,2024` -> year is 2023 or 2024
- `type:article,misc` -> entry type in article or misc
- `-type:misc` -> exclude misc entries
- `has:code,doi` -> require both code and doi
- `-has:pdf` -> exclude entries that appear to include a PDF
- `annotation:CodeAvailable` -> annotation contains `CodeAvailable`
- `keywords:mamba` -> keywords contains `mamba`
- `sort:year_desc` -> newest first
- `limit:10` -> return 10 results
- `fields:key,title,year,doi` -> restrict returned fields
- `cite:latex` / `cite:typst` / `cite:both`
- `raw:true` -> include raw BibTeX
- `recent:3` -> set the recency window (years) for the additive `meta.recency` report; also available as the `--recent-window` flag
- `claim:"low-latency forecasting"` -> attach a per-result `claim_support` block (lexical overlap only); also available as the `--claim` flag (preferred for claims with spaces)

### Notes

- Multiple compact filters can be mixed freely.
- Tokens that do not match the compact syntax stay in the free-text theme query.
- The parser also accepts compact syntax inside `spec.query` when a JSON spec is used.
- Generic field filters work for many fields, including `title`, `shorttitle`, `annotation`, `keywords`, `abstract`, `file`, `copyright`, `doi`, and `eprint`.
- Negated generic field filters are written like `-annotation:survey`.
- Any `word:word` token is treated as a generic field filter, so a misspelled field name (`tilte:...`) matches nothing; `meta.parse_warnings` flags a filter field that is absent from every entry.
- If you want a compact human-readable summary after the search, pipe the JSON into `scripts/preview_bib_search.py` instead of changing the query syntax.

## Recency report and claim binding (additive)

Both features are additive and never filter or reorder results.

- **Recency** is always reported under `meta.recency`: `window_years`, `recent_threshold`
  (computed from the current calendar year, so it stays correct over time),
  `with_year`, `recent_count`, `recent_share`, and a `note` that warns when fewer than
  80% of returned results fall inside the window. Tune the window with `recent:N` or
  `--recent-window N` (default 3).
- **Claim binding** runs only when a claim is supplied via `--claim "..."` (preferred) or
  `claim:"..."`. Each result then gains a `claim_support` block with `relevance`,
  `matched_fields`, `shared_terms`, and a `provenance` note. This is lexical overlap, **not**
  proof of support — keep it as a verification hand-off, never as evidence the paper backs
  the claim.

JSON spec form:

```json
{
  "query": "low-latency time-series forecasting",
  "recent_window": 3,
  "claim": "our sparse attention reduces inference latency"
}
```

## Natural-language mapping examples

### Theme search

User request:

> Find papers on long-term time-series forecasting that use Mamba.

Compact form:

```text
long-term time series forecasting mamba cite:both
```

Suggested JSON spec:

```json
{
  "query": "long-term time series forecasting mamba",
  "sort": "relevance",
  "limit": 5,
  "citation_mode": "both"
}
```

### Theme search with explicit filters

User request:

> Find 2024 or later Cheng papers on Mamba for time-series forecasting, preferably with code.

Compact form:

```text
mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:8
```

Suggested JSON spec:

```json
{
  "query": "mamba time series forecasting",
  "filters": {
    "year_min": 2024,
    "author_contains": ["Cheng"],
    "has": ["code"]
  },
  "sort": "relevance",
  "limit": 8,
  "citation_mode": "both"
}
```

### Field-specific filter

User request:

> Show entries whose annotation contains CodeAvailable and whose abstract mentions photovoltaic.

Compact form:

```text
photovoltaic annotation:CodeAvailable raw:true cite:none
```

Suggested JSON spec:

```json
{
  "query": "photovoltaic",
  "filters": {
    "field_contains": {
      "annotation": ["CodeAvailable"],
      "abstract": ["photovoltaic"]
    }
  },
  "include_raw_bib": true,
  "citation_mode": "none"
}
```

### Negation and exclusion

User request:

> Find recent transformer papers for time-series forecasting, but exclude arXiv-only misc entries and exclude entries without DOI.

Compact form:

```text
transformer time series forecasting year>=2022 -type:misc has:doi
```

Suggested JSON spec:

```json
{
  "query": "transformer time series forecasting",
  "filters": {
    "year_min": 2022,
    "exclude_type_in": ["misc"],
    "has": ["doi"]
  },
  "sort": "relevance"
}
```

### Bibliographic export check

User request:

> Return the original BibTeX entry and both LaTeX and Typst citation forms for the best match to TimeMachine.

Compact form:

```text
TimeMachine raw:true cite:both limit:1
```

Suggested JSON spec:

```json
{
  "query": "TimeMachine",
  "sort": "relevance",
  "limit": 1,
  "include_raw_bib": true,
  "citation_mode": "both"
}
```

## Sorting guidance

- `relevance`: best default for topic-based discovery
- `year_desc`: useful for newest-first scans
- `year_asc`: useful for historical development views
- `title`: useful when reviewing a narrow candidate set

## Edge cases

### Filter-only query (no topic words)

When the user only wants to filter without a topic search, all matching entries receive a score of zero and the sort mode determines the order. Example:

```text
author:Cheng year>=2024 type:article sort:year_desc
```

This returns all articles by Cheng from 2024 onward, sorted newest first, without any relevance ranking.

### Empty results guidance

If no entries match the query, try broadening filters step by step:

1. Remove `has:` constraints — `has:code` and `has:pdf` are the most restrictive
2. Widen or drop the year range
3. Use fewer topic keywords or try synonyms
4. Check author name spelling. The author filter is a case-insensitive,
   accent-folded substring match, so `author:Muller` matches `M{\"u}ller` and a
   partial name like `author:chen` matches both `Chen` and `Cheng`. That breadth
   is convenient for recovery but also a false-positive risk: confirm the author
   identity before citing rather than trusting a substring hit.

## Known limitations

- Author matching does not normalise name order or `von`/particle handling, so
  `author:"Jane Doe"` will not match a `{Doe, Jane}` field; search by surname.
- `matched_entries` counts structured-filter matches only; it does not report how
  many entries the free-text relevance threshold dropped.
- CJK queries match best as a contiguous substring (`时间序列`); space-separated
  CJK terms may not all match.
- Multi-file libraries are not merged — run the script once per `.bib` file.
- Years are detected in the 1500–2099 range; entries without a parseable year are
  excluded by any year filter.
