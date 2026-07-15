# Bibliography Module Reference

Purpose: Validate references against GB/T 7714 and check BibTeX/BibLaTeX configuration.

> Version note: GB/T 7714-2025 was published on 2025-12-02 and **took effect on 2026-07-01**, replacing the 2015 edition.
> `verify_bib.py --standard gb7714` checks against the 2015 edition; `--standard gb7714-2025`
> checks differences in the new standard, including preprint/dataset types and removal of access-date
> requirements for non-online literature. See Section 5 of
> [`../citations/gb-standard.md`](../citations/gb-standard.md) for transition guidance.

## Document Type Identifiers

| Type | Code | Example Format |
|------|------|---------------|
| Book | M | Author. Book title[M]. Place: Publisher, Year. |
| Journal | J | Author. Article title[J]. Journal, Year, Volume(Issue): Pages. |
| Thesis | D | Author. Title[D]. City: University, Year. |
| Conference | C | Author. Title[C]//Conference. City, Year: Pages. |
| Patent | P | Inventor. Patent title[P]. Country: Patent number, Date. |
| Electronic | EB/OL | Author. Title[EB/OL]. (Publication date)[Access date]. URL. |

## BibLaTeX Configuration (Recommended)

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{refs.bib}
\printbibliography[title=参考文献]
```

## BibTeX Alternative

```latex
\bibliographystyle{gbt7714-numerical}  % or gbt7714-author-year
\bibliography{refs}
```

## Common Issues

- **Author names**: Chinese surname first; English: Surname, Initials.
- **Multiple authors**: list all for 3 or fewer; for 4+, list the first 3 followed by “等”/“et al.”
- **DOI**: Must be included when available (`doi = {10.xxxx/xxxxx}`)
- **Page numbers**: Use a double dash `1--15`, not a single dash or tilde

> Full details: see Sections 1-4 of [`../citations/gb-standard.md`](../citations/gb-standard.md)
