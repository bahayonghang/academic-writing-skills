# Execution Notes

## 2026-07-16 baseline

- Branch: `dev`
- Scoped restore baseline: `99eaf06198de3bc7d9eea46b2bd80ba705586f11`
- `tests/contracts/test_skill_versions.py`: 1 passed
- `tests/skills/paper_audit`: 310 passed
- Resource inventory: 250 manifest entries, passed
- Existing locks located with `rg -n "reproducibility_partial|sanitize_issue|CRITICAL|4 specialized" tests academic-writing-skills/paper-audit`.

## Planning correction before activation

The W1/W2 source files are present in `docs/resource-manifest.json`. Content edits change
their `sourceSha256`, and `just ci` runs the inventory-only contract test. The task therefore
refreshes manifest hashes after W2. Per parent decision D7, bilingual resource bodies and
usage/overview synchronization remain owned by `07-15-audit-release-integration`; an
inventory-only pass must not be reported as full bilingual resource synchronization.
