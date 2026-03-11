# Module: Bibliography

**Trigger**: bib, bibliography, 参考文献, citation

## Commands

```bash
uv run python -B scripts/verify_bib.py references.bib
uv run python -B scripts/verify_bib.py references.bib --tex main.tex
uv run python -B scripts/verify_bib.py references.bib --standard gb7714
uv run python -B scripts/verify_bib.py references.bib --tex main.tex --json
```

## Details
Checks: required fields, duplicate keys, missing citations, unused entries.
Key output fields: `missing_in_bib`, `unused_in_tex`.
Skill-layer response: convert the raw verification results into `% BIBLIOGRAPHY ...` style findings when presenting them to the user.

See also: [CITATION_VERIFICATION.md](../CITATION_VERIFICATION.md) for API-based verification.

