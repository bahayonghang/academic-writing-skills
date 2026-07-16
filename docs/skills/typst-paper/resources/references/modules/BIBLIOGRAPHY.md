# Module: Bibliography

**Trigger**: bib, bibliography, 参考文献, citation, reference format, citation style

## Commands

```bash
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.yml          # Hayagriva
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --typ main.typ
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --style apa
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --style gb-7714-2015-numeric
uv run python -B $SKILL_DIR/scripts/verify_bib.py references.bib --online --email you@example.com
```

## Details

Checks: required fields, duplicate keys, missing citations, unused entries
(when `--typ` is given). Accepts `.bib` (BibTeX) and `.yml`/`.yaml` (Hayagriva);
Hayagriva entries are validated against their own field contract (`title` /
`author`, `date`/`parent` semantics), not the BibTeX table.

Style-specific checks (via `--style`, one of `ieee`, `apa`, `mla`, `chicago`,
`gb-7714-2015-numeric`): author count vs et al. threshold, page format (en dash,
BibTeX only), DOI requirements.

Online verification (`--online`, optional `--email` for the CrossRef polite
pool, `--online-timeout`) cross-checks entries against CrossRef / Semantic
Scholar.

The script prints a human-readable report; the skill layer converts findings
into `// BIBLIOGRAPHY ...` comment-protocol lines when presenting them.

See also: [CITATION_VERIFICATION.md](../CITATION_VERIFICATION.md) for API-based verification.
See also: [CITATION_STYLES.md](../CITATION_STYLES.md) for IEEE/APA/Chinese format rules.
See also: [JOURNAL_ABBREVIATIONS.md](../JOURNAL_ABBREVIATIONS.md) for ISO 4 journal name abbreviations.
