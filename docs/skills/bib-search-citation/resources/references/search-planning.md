# Search Planning Defaults and Compact Operators

## Defaults

Use these defaults unless the user says otherwise:

- research discovery request -> `sort: relevance`
- no explicit limit -> `limit: 5`
- no explicit field list -> return `key`, `title`, `shorttitle`, `author`, `year`,
  `venue`, `doi`, `eprint`, `keywords`, `annotation`, and `abstract`
- asks for "original", "full entry", or "bib" -> `include_raw_bib: true`
- asks for citation snippets in a mixed LaTeX/Typst workflow -> `citation_mode: both`

## Supported compact operators

- `author:cheng`
- `year>=2024`, `year<=2025`, `year:2024`, `year:2023,2024`
- `type:article,misc`, `-type:misc`
- `has:code,doi`, `-has:pdf`
- `annotation:CodeAvailable`, `keywords:mamba`, `abstract:photovoltaic`
- `sort:year_desc`, `limit:10`, `fields:key,title,year,doi`
- `cite:latex`, `cite:typst`, `cite:both`, `cite:none`
- `raw:true`
- `recent:3` (recency window for the additive `meta.recency` report; or `--recent-window`)
- `claim:"..."` (adds per-result `claim_support`; prefer `--claim` for claims with spaces)

The useful `has` values are `doi`, `abstract`, `keywords`, `annotation`,
`shorttitle`, `eprint`, `pdf`, and `code`. The `code` flag is inferred from
fields such as `url`, `abstract`, `keywords`, `annotation`, `note`, and
`howpublished` when they mention GitHub, GitLab, code, repository, or source.
