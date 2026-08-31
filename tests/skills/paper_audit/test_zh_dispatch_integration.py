"""Integration coverage for zh dispatch wiring (bib, gate, fixtures)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "paper_audit" / "zh_thesis"


def _capture_runs(monkeypatch: pytest.MonkeyPatch):
    import audit

    captured: list[tuple[str, str, list[str]]] = []
    original = audit._run_check_script

    def wrapped(script_path: Path, file_path: str, extra_args: list[str] | None = None):
        captured.append((Path(script_path).name, file_path, list(extra_args or [])))
        return original(script_path, file_path, extra_args)

    monkeypatch.setattr(audit, "_run_check_script", wrapped)
    return captured


def test_bib_task_receives_bib_path_and_gb_standard(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    captured = _capture_runs(monkeypatch)
    import audit

    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])
    result = audit.run_audit(
        str(FIXTURES / "zh_thesis_defects.tex"),
        mode="quick-audit",
        lang="zh",
        venue="thesis-zh",
    )
    bib_runs = [row for row in captured if row[0] == "verify_bib.py"]
    assert bib_runs, captured
    _script, file_path, extra = bib_runs[0]
    assert file_path.endswith(".bib")
    assert extra[:2] == ["--standard", "gb7714"] or extra[-2:] == ["--standard", "gb7714"]
    assert "--standard" in extra
    out = capsys.readouterr().out
    assert "SKIP gbt7714" not in out
    bib_issues = [issue for issue in result.issues if issue.module == "BIB"]
    assert bib_issues


def test_bib_skip_when_unresolved(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import audit

    tex = tmp_path / "lonely.tex"
    tex.write_text(
        "\\documentclass{article}\\begin{document}中文摘要。\\end{document}\n",
        encoding="utf-8",
    )
    audit.run_audit(str(tex), mode="quick-audit", lang="zh")
    out = capsys.readouterr().out
    assert "SKIP bib: no .bib resolved" in out


def test_typst_bib_does_not_pass_standard(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_runs(monkeypatch)
    import audit

    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])
    audit.run_audit(str(FIXTURES / "zh_thesis_defects.typ"), mode="quick-audit", lang="zh")
    bib_runs = [row for row in captured if row[0] == "verify_bib.py"]
    for _script, file_path, extra in bib_runs:
        assert file_path.endswith(".bib")
        assert "--standard" not in extra


def test_blind_never_passes_generate_and_is_readonly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_runs(monkeypatch)
    import audit

    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])
    target = FIXTURES / "zh_thesis_defects.tex"
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    mtime = target.stat().st_mtime_ns
    audit.run_audit(str(target), mode="quick-audit", lang="zh", venue="thesis-zh")
    after = hashlib.sha256(target.read_bytes()).hexdigest()
    assert after == before
    assert target.stat().st_mtime_ns == mtime
    blind_runs = [row for row in captured if row[0] == "blind_review.py"]
    assert blind_runs
    for _script, _path, extra in blind_runs:
        assert "--check" in extra
        assert "--generate" not in extra


def test_f1_gate_promotes_spec_and_blind(monkeypatch: pytest.MonkeyPatch) -> None:
    import audit
    from report_generator import render_gate_report

    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])
    result = audit.run_audit(
        str(FIXTURES / "zh_thesis_defects.tex"),
        mode="gate",
        lang="zh",
        venue="thesis-zh",
    )
    triples = {
        (issue.module, issue.severity, issue.severity == "Critical")
        for issue in result.issues
        if issue.module in {"SPEC", "BLIND"}
    }
    assert any(module == "SPEC" and blocker for module, _sev, blocker in triples)
    assert any(module == "BLIND" and blocker for module, _sev, blocker in triples)
    report = render_gate_report(result, lang="zh")
    assert "FAIL" in report or "不通过" in report or "fail" in report.lower()


def test_f3_optional_chapters_do_not_fail_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    import audit
    from report_generator import ChecklistItem

    monkeypatch.setattr(
        audit,
        "_run_checklist",
        lambda *args, **kwargs: [ChecklistItem("placeholder", True)],
    )
    result = audit.run_audit(
        str(FIXTURES / "zh_thesis_optional_absent.tex"),
        mode="gate",
        lang="zh",
        venue="thesis-zh",
    )
    blocking = [issue for issue in result.issues if issue.severity == "Critical"]
    assert not any("附录" in issue.message or "符号" in issue.message for issue in blocking)
    assert not any(
        issue.module in {"SPEC", "BLIND"}
        and issue.severity == "Critical"
        and ("附录" in issue.message or "符号" in issue.message)
        for issue in result.issues
    )


def test_style_zh_json_extra_args(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_runs(monkeypatch)
    import audit

    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])
    audit.run_audit(str(FIXTURES / "zh_thesis_defects.tex"), mode="quick-audit", lang="zh")
    style_runs = [row for row in captured if row[0] == "check_style_zh.py"]
    assert style_runs
    assert "--json" in style_runs[0][2]
    assert "--max-words" not in style_runs[0][2]


def test_zh_checkers_resolve_to_thesis_scripts() -> None:
    import audit

    for check, name in {
        "spec": "check_spec.py",
        "blind": "blind_review.py",
        "abstract": "analyze_abstract.py",
        "conclusion": "analyze_conclusion.py",
        "literature": "analyze_literature.py",
        "tables": "check_tables.py",
        "consistency": "check_consistency.py",
    }.items():
        script = audit._resolve_script(check, "zh", ".tex")
        assert script is not None, check
        assert script.name == name
        assert script.parent == SCRIPT_DIR_ZH
