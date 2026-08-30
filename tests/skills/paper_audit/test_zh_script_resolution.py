"""Language/format script resolution for paper-audit zh profile (C1)."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "paper_audit" / "zh_thesis"


def test_zh_tex_four_way_judgment() -> None:
    import audit

    sentences = audit._resolve_check("sentences", "zh", ".tex")
    grammar = audit._resolve_check("grammar", "zh", ".tex")
    figures = audit._resolve_check("figures", "zh", ".tex")
    pseudocode = audit._resolve_check("pseudocode", "zh", ".tex")

    assert sentences.path is not None
    assert sentences.path.name == "check_style_zh.py"
    assert sentences.reason == "override"
    assert grammar.path is None and grammar.reason == "suppressed"
    assert figures.path is not None
    assert figures.reason == "lang-neutral-reuse"
    assert figures.origin == "en"
    assert pseudocode.path is None and pseudocode.reason == "suppressed"


def test_polish_precheck_zh_sentences_is_style_zh(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import audit

    paper = tmp_path / "paper.tex"
    paper.write_text(
        (FIXTURES / "zh_thesis_clean.tex").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    seen: list[Path | None] = []
    original = audit._resolve_script

    def wrapped(check_name: str, lang: str, fmt: str) -> Path | None:
        path = original(check_name, lang, fmt)
        if check_name == "sentences":
            seen.append(path)
        return path

    monkeypatch.setattr(audit, "_resolve_script", wrapped)
    monkeypatch.setattr(audit, "_run_check_script", lambda *args, **kwargs: (0, "", ""))
    audit.run_polish_precheck(str(paper), lang="zh")
    assert seen
    assert seen[0] is not None
    assert seen[0].name == "check_style_zh.py"


def test_typst_zh_only_checks_are_format_exempt() -> None:
    import audit

    for check in audit.ZH_ONLY_TEX_CHECKS:
        resolution = audit._resolve_check(check, "zh", ".typ")
        assert resolution.reason == "format-exempt"
        assert resolution.path is None


def test_pdf_zh_only_checks_are_format_skipped() -> None:
    import audit

    for check in audit.ZH_ONLY_TEX_CHECKS:
        resolution = audit._resolve_check(check, "zh", ".pdf")
        assert resolution.reason == "format-skipped"
        assert resolution.path is None


def test_gbt7714_dead_entry_removed() -> None:
    import audit

    assert "gbt7714" not in audit.ZH_EXTRA_CHECKS
    assert "gbt7714" not in audit._SCRIPT_MAP
    assert audit._resolve_script("gbt7714", "zh", ".tex") is None


def test_optimize_title_and_map_structure_are_not_dead_keys() -> None:
    import audit

    assert "optimize_title" not in audit._SCRIPT_MAP
    assert "map_structure" not in audit._SCRIPT_MAP
    assert audit._resolve_script("optimize_title", "zh", ".tex") is None
    assert audit._resolve_script("map_structure", "zh", ".tex") is None


def test_resolution_logs_four_states(capsys: pytest.CaptureFixture[str]) -> None:
    import audit

    audit._log_resolution(
        "figures",
        audit.ScriptResolution(Path("check_figures.py"), "en", "lang-neutral-reuse"),
        "zh",
        ".tex",
    )
    audit._log_resolution(
        "sentences",
        audit.ScriptResolution(SCRIPT_DIR_ZH / "check_style_zh.py", "zh", "override"),
        "zh",
        ".tex",
    )
    audit._log_resolution(
        "grammar",
        audit.ScriptResolution(None, "none", "suppressed"),
        "zh",
        ".tex",
    )
    audit._log_resolution(
        "missing",
        audit.ScriptResolution(None, "none", "missing"),
        "zh",
        ".tex",
    )
    text = capsys.readouterr().out
    assert "lang-neutral reuse" in text
    assert "origin=zh, override" in text
    assert "suppressed for lang=zh" in text
    assert "script not found" in text


def test_e1_run_audit_records_resolve_check(monkeypatch: pytest.MonkeyPatch) -> None:
    import audit

    seen: list[tuple[str, str]] = []
    original = audit._resolve_check

    def wrapped(check_name: str, lang: str, fmt: str):
        result = original(check_name, lang, fmt)
        seen.append((check_name, result.reason))
        return result

    monkeypatch.setattr(audit, "_resolve_check", wrapped)
    monkeypatch.setattr(audit, "_run_check_script", lambda *args, **kwargs: (0, "", ""))
    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])

    audit.run_audit(str(FIXTURES / "zh_thesis_defects.tex"), mode="quick-audit", lang="zh")
    reasons = dict(seen)
    assert reasons["grammar"] == "suppressed"
    assert reasons["sentences"] == "override"
    assert reasons["figures"] == "lang-neutral-reuse"
    assert reasons["pseudocode"] == "suppressed"


def test_e2_deep_review_still_hardcodes_quick_audit() -> None:
    import audit

    source = inspect.getsource(audit.run_deep_review)
    assert 'mode="quick-audit"' in source


def test_e3_reaudit_still_hardcodes_quick_audit() -> None:
    import audit

    source = inspect.getsource(audit.run_reaudit)
    assert 'mode="quick-audit"' in source


def test_gate_eligible_set_excludes_consistency_and_optional_chapters() -> None:
    import audit

    assert set(audit.GATE_ELIGIBLE_ZH) == {"spec", "blind"}
    assert "consistency" not in audit.GATE_ELIGIBLE_ZH
    assert "abstract" not in audit.GATE_ELIGIBLE_ZH
    assert "tables" not in audit.GATE_ELIGIBLE_ZH
