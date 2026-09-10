# C6 acceptance notes

Date: 2026-09-07. Implementer wrote the spec and the honest ledger.
No commit, archive, remote workflow, global install, or Basic Memory write.
Final `just ci`, resource sync, docs build, and parent probe stay with the
main session.

## Outcome

This implement pass closes the C6 spec/ledger write for **静态规则与隔离脚本交付**.
It does **not** close **五平台运行验证完成**.

## Files

| Path | Change |
| --- | --- |
| `.trellis/spec/academic-writing-skills/harness-workflow-contract.md` | New executable contract + five-tool ledger |
| `.trellis/spec/academic-writing-skills/index.md` | Index row |
| `.trellis/tasks/09-07-five-harness-evergreen-audit/research/closeout-ledger.md` | Parent evidence pointer |
| `docs/harnesses.md` / `docs/zh/harnesses.md` | Evidence status rows only |

Did not edit skill `SKILL.md`, `audit.py`, `ci.yml`, `justfile`, README*, or tests.

## AC

- AC1: Reused C1–C5 acceptance. C3 Unicode tests and C4 installed-layout test
  are present and drive shipped functions. Baseline tests were not deleted.
  Final `just ci` / resource sync / docs build: not run here (main session).
- AC2: Five-tool ledger is complete in the spec §10. Unrun items stay UNVERIFIED.
  Completeness of the ledger is the pass.
- AC3: Approved experience written to project spec and index. Per item: applicable
  tools, version/evidence, exceptions. No Basic Memory write.
- AC4: README user model-recommendation lines were not touched.
  `README_CN.md:14` trailing spaces remain baseline. Follow-ups listed in spec §13.

## UNVERIFIED (quoted)

- Claude Code / Codex / Grok Build / Kimi Code / OMP fresh session load
- Native delegation on those five tools
- Hooks trust on those five tools
- `npx skills add` copy vs symlink
- Hosted GitHub Actions Windows/Ubuntu × 3.10/3.13 on the current SHA
- Paid new sessions

## Commands run by implementer

Lighter checks only. Outer shell may wrap with RTK; command text is the original.

| Command | Exit | Notes |
| --- | --- | --- |
| `uv run --extra dev python -m pytest --collect-only -q tests/skills/paper_audit/test_paper_audit_integration.py tests/skills/paper_audit/test_installed_layout.py` | 0 | 9 tests collected, including C3 `test_run_check_script_windows_stream_utf8_keeps_unicode[0]/[3]`, non-Windows Unicode cases, timeout, and C4 `test_installed_layout_full_vs_standalone` |
| `git diff --check -- docs/harnesses.md docs/zh/harnesses.md .trellis/spec/academic-writing-skills/index.md` | 0 | Tracked C6 diffs only. New spec file is untracked; Python trailing-whitespace scan of C6 markdown: none |
| `git diff -- README.md README_CN.md` | 0 | Empty. Model-recommendation lines not touched |

Not run: `just ci`, resource sync, `just doc-build`, parent probe.
