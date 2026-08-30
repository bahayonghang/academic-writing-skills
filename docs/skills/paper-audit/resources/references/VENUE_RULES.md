# Venue-Specific Rules

When `--venue` (or `--journal`) is specified, the audit adds venue-specific checks:

| Venue | Key Rules |
|-------|-----------|
| `neurips` | 9-page limit, broader impact statement, paper checklist, double-blind |
| `iclr` | 10-page limit, reproducibility statement, double-blind |
| `icml` | 8-page limit, impact statement, 50MB supplementary limit |
| `ieee` | Abstract <=250 words, 3-5 keywords, >=300 DPI figures, no floating `algorithm` / `algorithm2e` pseudocode, figure-style pseudocode caption/label/reference checks |
| `acm` | CCS concepts required, acmart class, rights management |
| `thesis-zh` | See the Chinese Thesis subsection below. No `page_limit`: dissertation length is counted in characters and varies widely by school. |

### Chinese Thesis (`thesis-zh`)

Mechanical `extra_checks` use stable IDs `TZ-EC-*`. Each ID must appear as
`TZ-CL-*` in `CHECKLIST.md`. Reverse coverage is not required.

- `TZ-EC-bilingual-abstract` / `TZ-CL-bilingual-abstract`: Chinese and English abstracts are required (GB/T 7713.1 and school templates).
- `TZ-EC-bilingual-keywords` / `TZ-CL-bilingual-keywords`: Chinese and English keywords are required.
- `TZ-EC-originality` / `TZ-CL-originality`: declaration of originality is required.
- `TZ-EC-acknowledgments` / `TZ-CL-acknowledgments`: acknowledgments are required.
- Do **not** set `page_limit`. Master's and doctoral word counts differ by school (order of 30k–50k vs 80k–150k characters) and would mis-fire.
- Keep `blind_review: False`. That flag only adds a conference-style “double-blind / hide \\author” checklist item (`audit.py` `_run_checklist`). Thesis blind-review capability is the `blind` checker (`blind_review.py --check`), not this flag.
- Appendix and symbol-list existence are checklist-only (`TZ-CL-appendix-optional`, `TZ-CL-symbols-optional`). Yanshan marks both as optional; pkuthss marks the symbol list as a conditional chapter. They must not enter `extra_checks` or gate.


Without `--venue`, only universal checklist items apply.
