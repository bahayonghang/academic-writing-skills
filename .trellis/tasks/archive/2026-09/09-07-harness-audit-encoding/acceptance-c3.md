# C3 acceptance notes

## Pre-fix pytest (must fail)

Command:

```text
uv run --extra dev python -m pytest tests/skills/paper_audit/test_paper_audit_integration.py::test_run_check_script_windows_stream_utf8_keeps_unicode tests/skills/paper_audit/test_paper_audit_integration.py::test_run_check_script_unicode_protocol_non_windows tests/skills/paper_audit/test_paper_audit_integration.py::test_run_check_script_timeout_returns_minus_one -v
```

Result: exit 1. 2 failed, 1 passed, 2 skipped in 1.95s.

- `test_run_check_script_windows_stream_utf8_keeps_unicode[0]` FAILED: `assert payload["out_is_str"] is True` (stdout was None under PYTHONUTF8=0 + PYTHONIOENCODING=utf-8)
- `test_run_check_script_windows_stream_utf8_keeps_unicode[3]` FAILED: same `out_is_str` assertion
- `test_run_check_script_timeout_returns_minus_one` PASSED (timeout path unchanged)
- `test_run_check_script_unicode_protocol_non_windows[0]` SKIPPED (win32)
- `test_run_check_script_unicode_protocol_non_windows[3]` SKIPPED (win32)

Parent probe BEFORE this fix (collector exit 0 is not the bar) is in implementer scratch `probe-before-c3.txt`: checkout-stream-utf8 exit=1 with UnicodeDecodeError gbk + AttributeError None.strip.

## Post-fix pytest

Command:

```text
uv run --extra dev python -m pytest tests/skills/paper_audit/test_paper_audit_integration.py tests/skills/paper_audit/test_paper_audit.py -q
```

Result: exit 0. 149 passed, 2 skipped in 17.04s.

The two skipped cases are `test_run_check_script_unicode_protocol_non_windows[0]` and `[3]` (`sys.platform == "win32"`). Windows stream-utf8 cases `[0]` and `[3]` passed.

## Lint / typecheck

- `just lint`: exit 0 (200 files already formatted; All checks passed)
- `just typecheck`: exit 0 (existing warning baseline; 0 errors)

## Probe

Not re-run here. The parent probe writes under `.trellis/tasks/09-07-five-harness-evergreen-audit/research/`. Main session re-runs it. Stream-only checkout must become exit=0. standalone missing=8 is not a C3 defect.

