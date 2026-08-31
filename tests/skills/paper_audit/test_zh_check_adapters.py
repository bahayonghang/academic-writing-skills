"""Named adapters for latex-thesis-zh checkers wired into paper-audit."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from tests.support.paths import SCRIPT_DIR_ZH

SAMPLE_SPEC = {
    "items": [
        {
            "id": "GEN-01",
            "requirement": "题名不超过 25 字",
            "status": "FAIL",
            "evidence": "题名 30 字",
        },
        {"id": "GEN-03", "requirement": "双语摘要", "status": "PASS", "evidence": ""},
    ]
}
SAMPLE_ABSTRACT = {
    "status": "WARNING",
    "mode": "thesis",
    "checks": [
        {
            "id": "T-PAIN",
            "level": "Warning",
            "flagged": True,
            "message": "未发现痛点",
            "evidence": "",
        }
    ],
    "bilingual": {"english_found": False, "checks": []},
    "count": {"count": 12, "status": "PASS"},
}
SAMPLE_CONCLUSION = {
    "status": "WARNING",
    "findings": [
        {
            "code": "CC-01",
            "severity": "Warning",
            "loc": "第12行",
            "message": "结论缺少量化",
            "suggestion": "",
            "reason": "",
        }
    ],
}
SAMPLE_TABLES = {
    "status": "FAIL",
    "issues": [
        {
            "line": 8,
            "level": "ERROR",
            "priority": "P1",
            "message": "vertical lines",
            "category": "rules",
        }
    ],
}
SAMPLE_STYLE = {
    "findings": [
        {
            "code": "E-COLLOQ",
            "loc": "第3行",
            "severity": "Info",
            "priority": "P3",
            "title": "口语化程度副词",
            "original": "很多工作",
            "suggestion": "大量",
            "basis": "",
        }
    ]
}
SAMPLE_BLIND = """\
============================================================
盲审匿名化检查报告
[R1/R2] 需隐匿项（[Script] 自动定位）:
% BLIND-REVIEW (main.tex:L4) [HIGH] [P0] [Script]: R1 作者字段 — 张三
============================================================
"""
SAMPLE_LITERATURE = "% 文献综述（第10行）[Severity: Major] [Priority: P1]: [Script] 作者年份罗列\n"


def _adapters():
    from zh_check_adapters import (
        AbstractJsonAdapter,
        BlindReviewTextAdapter,
        ConclusionJsonAdapter,
        LiteratureTextAdapter,
        SpecJsonAdapter,
        StyleZhJsonAdapter,
        TablesJsonAdapter,
    )

    return {
        "check_spec.py": (SpecJsonAdapter(), json.dumps(SAMPLE_SPEC, ensure_ascii=False), "SPEC"),
        "analyze_abstract.py": (
            AbstractJsonAdapter(),
            json.dumps(SAMPLE_ABSTRACT, ensure_ascii=False),
            "ABSTRACT",
        ),
        "analyze_conclusion.py": (
            ConclusionJsonAdapter(),
            json.dumps(SAMPLE_CONCLUSION, ensure_ascii=False),
            "CONCLUSION",
        ),
        "check_tables.py": (
            TablesJsonAdapter(),
            json.dumps(SAMPLE_TABLES),
            "TABLES",
        ),
        "check_style_zh.py": (
            StyleZhJsonAdapter(),
            json.dumps(SAMPLE_STYLE, ensure_ascii=False),
            "SENTENCES",
        ),
        "blind_review.py": (BlindReviewTextAdapter(), SAMPLE_BLIND, "BLIND"),
        "analyze_literature.py": (LiteratureTextAdapter(), SAMPLE_LITERATURE, "LITERATURE"),
    }


@pytest.mark.parametrize("script_name", list(_adapters()))
def test_adapter_real_sample_has_script_tag(script_name: str) -> None:
    adapter, sample, module = _adapters()[script_name]
    issues = adapter.parse(sample)
    assert issues
    assert all(issue.module == module for issue in issues)
    assert all("[Script]" in issue.message for issue in issues)


@pytest.mark.parametrize("script_name", list(_adapters()))
def test_adapter_unknown_flag_exits_2(script_name: str) -> None:
    script = SCRIPT_DIR_ZH / script_name
    result = subprocess.run(
        [sys.executable, str(script), "dummy.tex", "--not-a-real-flag"],
        capture_output=True,
        text=True,
        cwd=str(script.parent),
        check=False,
    )
    assert result.returncode == 2


@pytest.mark.parametrize("script_name", list(_adapters()))
def test_adapter_nonzero_exit_without_output_is_error(script_name: str) -> None:
    import audit

    script = SCRIPT_DIR_ZH / script_name
    issues, kind = audit._ingest_check_output(
        script_name.split(".")[0],
        script,
        2,
        "",
        "unrecognized arguments",
    )
    assert kind == "error"
    assert issues
    assert "clean" not in issues[0].message.lower()
    joined = " ".join(issue.message for issue in issues)
    assert "exit 2" in joined


@pytest.mark.parametrize("script_name", list(_adapters()))
def test_adapter_empty_output_is_clean_on_success(script_name: str) -> None:
    import audit

    script = SCRIPT_DIR_ZH / script_name
    issues, kind = audit._ingest_check_output("check", script, 0, "", "")
    assert kind == "clean"
    assert issues == []


@pytest.mark.parametrize(
    "script_name",
    [
        "check_spec.py",
        "analyze_abstract.py",
        "analyze_conclusion.py",
        "check_tables.py",
        "check_style_zh.py",
    ],
)
def test_json_adapter_rejects_illegal_json(script_name: str) -> None:
    from zh_check_adapters import AdapterParseError

    adapter, _, _ = _adapters()[script_name]
    with pytest.raises(AdapterParseError):
        adapter.parse("{")


def test_nonzero_exit_does_not_print_clean() -> None:
    import audit

    issues, kind = audit._ingest_check_output(
        "spec", SCRIPT_DIR_ZH / "check_spec.py", 2, "", "unrecognized arguments"
    )
    assert kind == "error"
    assert issues
    assert all("clean" not in issue.message.lower() for issue in issues)
    assert "exit 2" in issues[0].message


def test_style_zh_maps_info_and_warning() -> None:
    from zh_check_adapters import STYLE_ZH_SEVERITY, StyleZhJsonAdapter

    assert STYLE_ZH_SEVERITY == {"Info": "Info", "Warning": "Minor"}
    issues = StyleZhJsonAdapter().parse(json.dumps(SAMPLE_STYLE, ensure_ascii=False))
    assert issues[0].severity == "Info"
