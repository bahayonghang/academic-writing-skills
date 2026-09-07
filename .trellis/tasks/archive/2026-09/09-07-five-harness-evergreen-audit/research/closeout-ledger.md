# C6 closeout ledger (parent planning evidence)

Date: 2026-09-07. Child: `09-07-harness-validation-closeout`.
Canonical contract: `.trellis/spec/academic-writing-skills/harness-workflow-contract.md`.
Do not copy this file into global Basic Memory.

This round closes **静态规则与隔离脚本交付** after the main session runs the
parent shared gates. This round does **not** close **五平台运行验证完成**.

## Child checks reused

| Child | Evidence reused | Notes |
| --- | --- | --- |
| C1 `09-07-harness-project-contract` | `archive/2026-09/09-07-harness-project-contract/acceptance.md` | AGENTS.md shared source; CLAUDE.md `@AGENTS.md`; academic-use kept; MIT classifier removed; version 6.0.0; six skills. README model-recommendation lines kept. `README_CN.md:14` trailing spaces are baseline. |
| C2 `09-07-harness-ci-gates` | `archive/2026-09/09-07-harness-ci-gates/acceptance.md` | pytest `testpaths` = `tests` + `academic-writing-skills`; collect-only 1756 including 42 bib tests at C2 time. `ci.yml` PR/push Windows/Ubuntu 3.10/3.13 written. Hosted same-SHA matrix **UNVERIFIED**. |
| C3 `09-07-harness-audit-encoding` | `archive/2026-09/09-07-harness-audit-encoding/acceptance-c3.md`; parent probe files | `_run_check_script` UTF-8 pair. Tests drive the shipped function. Pre-fix collector: checkout-stream-utf8 exit 1. Post-fix parent probe files (main session): stream-utf8 complete JSON, empty STDERR, matching default and utf8-mode. C6 did not re-run the probe. |
| C4 `09-07-harness-onboarding` | `archive/2026-09/09-07-harness-onboarding/acceptance.md` | Isolation CLI: sibling missing=0 RUN=11; standalone missing=8 RUN=3. `npx`/symlink **UNVERIFIED**. |
| C5 `09-07-harness-skill-portability` | `archive/2026-09/09-07-harness-skill-portability/acceptance/c5-notes.md` | Portable read/search/exec/delegate. Sequential must not say independent panel. Live five-tool delegation **UNVERIFIED**. |

New tests that must remain: C3 Unicode cases in
`tests/skills/paper_audit/test_paper_audit_integration.py`; C4
`tests/skills/paper_audit/test_installed_layout.py`.

## Five-tool ledger

Full five-column table lives in the spec §10. Summary: static rules verified
locally for all five named tools; isolation CLI verified as a shared product
check; new session / delegation / hooks trust **UNVERIFIED**. Grok
working-copy `grok inspect` is a separate discovery record, not a new-session
pass.

## UNVERIFIED (must stay UNVERIFIED)

- Claude Code / Codex / Grok Build / Kimi Code / OMP fresh session load
- Native delegation on those five tools
- Hooks trust on those five tools
- `npx skills add` copy vs symlink
- Hosted GitHub Actions Windows/Ubuntu × 3.10/3.13 on the current SHA
- Paid new sessions

## Follow-ups (not this closeout)

- `paper-audit/references/MODE_GUIDE.md` still says “dispatch” without restating native vs sequential
- `README_CN.md:14` trailing spaces (baseline; do not rewrite)
- 75 Pyright warnings (baseline; do not batch-clean)
- ZIP reproducibility, release-tag check binding, deploy-job permission split

## Shared gates

Final `just ci`, resource sync, `just doc-build`, and parent probe re-run are
owned by the main session. C6 implementer wrote the spec and ledger only.
