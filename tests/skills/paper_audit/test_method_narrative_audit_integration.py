"""End-to-end coverage for method-narrative findings in paper-audit Phase 0."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT

FIXTURES = REPO_ROOT / "tests" / "fixtures" / "paper_audit"
METHOD_CODES = ("M-HEADING", "M-SEQWORD", "M-EQUATION")


def _method_issues(issues):
    return [issue for issue in issues if any(code in issue.message for code in METHOD_CODES)]


@pytest.mark.parametrize("suffix", ["tex", "typ"])
def test_method_narrative_phase0_parsing_and_scoring(
    suffix: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    import audit

    case_path = FIXTURES / f"method_narrative_case.{suffix}"
    clean_path = FIXTURES / f"method_narrative_clean.{suffix}"
    fmt = case_path.suffix
    lang = "en"
    logic_script = audit._resolve_script("logic", lang, fmt)
    assert logic_script is not None

    # Exercise the real format-specific checker before testing orchestration.
    for path, expected_count in ((case_path, 3), (clean_path, 0)):
        returncode, stdout, stderr = audit._run_check_script(
            logic_script, str(path), ["--section", "methods"]
        )
        assert returncode == 0, stderr
        parsed = audit._parse_script_output("logic", stdout)
        assert len(_method_issues(parsed)) == expected_count
        assert all("M-EDGETABLE" not in issue.message for issue in parsed)

    original_resolve = audit._resolve_script

    def resolve_logic_only(check_name: str, check_lang: str, check_fmt: str) -> Path | None:
        if check_name != "logic":
            return None
        return original_resolve(check_name, check_lang, check_fmt)

    monkeypatch.setattr(audit, "_resolve_script", resolve_logic_only)
    monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])

    case_result = audit.run_audit(str(case_path), mode="self-check", lang=lang, scholar_eval=True)
    clean_result = audit.run_audit(str(clean_path), mode="self-check", lang=lang, scholar_eval=True)

    case_method = _method_issues(case_result.issues)
    clean_method = _method_issues(clean_result.issues)
    assert len(case_method) == 3
    assert clean_method == []
    assert sum(issue.severity == "Minor" for issue in case_method) == 2
    assert sum(issue.severity == "Info" for issue in case_method) == 1
    assert {issue.priority for issue in case_method} == {"P2", "P3"}
    assert all("M-EDGETABLE" not in issue.message for issue in case_result.issues)

    case_scores = case_result.scholar_eval_result.script_scores
    clean_scores = clean_result.scholar_eval_result.script_scores
    assert clean_scores["soundness"] - case_scores["soundness"] == pytest.approx(1.0)
    assert {key: value for key, value in case_scores.items() if key != "soundness"} == {
        key: value for key, value in clean_scores.items() if key != "soundness"
    }


def test_zh_method_narrative_fixture_stays_in_explicit_chapter_workflow() -> None:
    import audit

    logic_script = audit._resolve_script("logic", "zh", ".tex")
    assert logic_script is not None
    fixtures = (
        (
            FIXTURES / "method_narrative_case_zh.tex",
            "基于多阶段约束传播的工业质量预测方法",
            3,
        ),
        (
            FIXTURES / "method_narrative_clean_zh.tex",
            "面向不确定输入的约束校准设计",
            0,
        ),
    )

    for path, section, expected_count in fixtures:
        returncode, stdout, stderr = audit._run_check_script(
            logic_script,
            str(path),
            ["--method-narrative", "--section", section],
        )
        assert returncode == 0, stderr
        parsed = audit._parse_script_output("logic", stdout)
        assert len(_method_issues(parsed)) == expected_count
        assert all("M-EDGETABLE" not in issue.message for issue in parsed)
