# Module: Bibliography

**Trigger**: bib, bibliography, 参考文献, citation

## Commands

```bash
uv run python scripts/verify_bib.py references.bib
uv run python scripts/verify_bib.py references.bib --typ main.typ
uv run python scripts/verify_bib.py references.yml --style ieee
```

## Details
Typst supports both BibTeX (`.bib`) and Hayagriva (`.yml`) formats:
```typst
#bibliography("references.bib", style: "ieee")   // BibTeX
#bibliography("references.yml", style: "apa")    // Hayagriva
```

Checks: required fields, duplicate keys, missing citations, unused entries.
See also: [CITATION_VERIFICATION.md](../references/CITATION_VERIFICATION.md) for API-based verification.

