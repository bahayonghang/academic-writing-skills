# Query Syntax

This page maps bibliography requests into the search inputs accepted by
`academic-writing-skills/bib-search-citation/scripts/search_bib.py`.

## Two Input Styles

The script supports:

1. a JSON search spec
2. a compact query expression

Use the compact form when the request already looks like a filter string.

```text
time series forecasting mamba author:Cheng year>=2024 has:code type:article,misc cite:both
```

Use the JSON form when the workflow needs explicit structured filters.

## JSON Spec Shape

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

## Compact Query Language

### Core Syntax

- plain words stay in the theme query
- `author:cheng` filters author names by substring
- `year>=2024` sets a minimum year
- `year<=2025` sets a maximum year
- `year:2024` requires an exact year
- `year:2023,2024` keeps either year
- `type:article,misc` keeps only those entry types
- `-type:misc` excludes those entry types
- `has:code,doi` requires both inferred fields
- `-has:pdf` excludes entries that appear to include a PDF
- `annotation:CodeAvailable` filters one field directly
- `keywords:mamba` filters another field directly
- `sort:year_desc` sorts newest first
- `limit:10` returns ten results
- `fields:key,title,year,doi` limits returned fields
- `cite:latex`, `cite:typst`, or `cite:both` controls citation output
- `raw:true` includes raw BibTeX
- `recent:3` sets the recency window (years) for the additive `meta.recency` report; also available as `--recent-window`
- `claim:"..."` attaches a per-result `claim_support` block (lexical overlap only); prefer the `--claim` flag for claims containing spaces

### Notes

- Multiple compact filters can be mixed freely.
- Tokens that do not match the compact syntax stay in the free-text theme query.
- Compact filters also work inside `spec.query` when you use a JSON spec.
- Generic field filters work for fields such as `title`, `shorttitle`, `annotation`,
  `keywords`, `abstract`, `file`, `copyright`, `doi`, and `eprint`.
- Negated field filters use the same form, for example `-annotation:survey`.
- Any `word:word` token becomes a generic field filter, so a misspelled field name
  matches nothing; `meta.parse_warnings` flags a filter field absent from every entry.
- `preview_bib_search.py` is a renderer, not a second search engine.

## Recency Report and Claim Binding (Additive)

Both features are additive — they never filter or reorder results.

- **Recency** is always reported under `meta.recency`: `window_years`,
  `recent_threshold` (computed from the current calendar year), `with_year`,
  `recent_count`, `recent_share`, and a `note` that warns when fewer than 80% of
  returned results fall inside the window. Tune it with `recent:N` or
  `--recent-window N` (default 3).
- **Claim binding** runs only when a claim is supplied via `--claim "..."`
  (preferred) or `claim:"..."`. Each result then gains a `claim_support` block with
  `relevance`, `matched_fields`, `shared_terms`, and a `provenance` note. This is
  lexical overlap, **not** proof of support — treat it as a verification hand-off,
  never as evidence the paper backs the claim.

## Natural-Language Mapping Examples

### Theme Search

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

### Theme Search with Explicit Filters

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

### Field-Specific Filter

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

### Negation and Exclusion

User request:

> Find recent transformer papers for time-series forecasting, but exclude arXiv-only misc entries and require DOI.

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

### Bibliographic Export Check

User request:

> Return the original BibTeX entry and both citation forms for the best TimeMachine match.

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

## Sorting Guidance

- `relevance`: best default for topic discovery
- `year_desc`: newest-first scans
- `year_asc`: historical development views
- `title`: small candidate-set review

## Edge Cases

### Filter-Only Query

When the request contains only filters and no topic words, all matching entries receive the
same score and the sort mode decides the order.

```text
author:Cheng year>=2024 type:article sort:year_desc
```

### Empty Results

If nothing matches, broaden filters in this order:

1. remove `has:` constraints
2. widen or remove the year range
3. shorten the topic query or try synonyms
4. check author spelling. The author filter is a case-insensitive, accent-folded
   substring match, so `author:Muller` matches `M{\"u}ller` and `author:chen`
   matches both `Chen` and `Cheng`. That breadth helps recovery but is also a
   false-positive risk — confirm the author before citing.

## Known Limitations

- Author matching does not normalise name order, so `author:"Jane Doe"` will not
  match a `{Doe, Jane}` field; search by surname instead.
- `matched_entries` counts structured-filter matches only, not free-text drops.
- CJK queries match best as a contiguous substring (`时间序列`).
- Multi-file libraries are not merged — run the script once per `.bib` file.
- A truncated entry (e.g. a missing closing brace) is skipped and reported in
  `meta.parse_warnings` rather than silently swallowing the rest of the file.
