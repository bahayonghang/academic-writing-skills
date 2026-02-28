# Module: Bibliography

**Trigger**: bib, bibliography, 参考文献, citation

## Commands

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --standard gb7714
python scripts/verify_bib.py references.bib --tex main.tex --json
```

## Details
Checks: required fields, duplicate keys, missing citations, unused entries.
Key output fields: `missing_in_bib`, `unused_in_tex`.

See also: [CITATION_VERIFICATION.md](../references/CITATION_VERIFICATION.md) for API-based verification.
