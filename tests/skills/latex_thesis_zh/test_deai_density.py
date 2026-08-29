"""C1 regressions for density limits, budgets, and section allowances."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest
import yaml

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_EN, SCRIPT_DIR_ZH, SKILLS_ROOT

_SIDECARS = ("parsers", "tex_loader", "deai_check")


def _load_copy(key: str, scripts_dir: Path) -> ModuleType:
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in _SIDECARS}
    try:
        path = scripts_dir / "deai_check.py"
        spec = importlib.util.spec_from_file_location(f"_density_{key}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(scripts_dir))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


ZH = _load_copy("zh", SCRIPT_DIR_ZH)
EN = _load_copy("en", SCRIPT_DIR_EN)

_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "deai_density"
_THESIS_EXCERPTS = json.loads((_FIXTURE_DIR / "thesis_excerpts.json").read_text(encoding="utf-8"))
_CALIBRATION_SUMMARY = json.loads(
    (_FIXTURE_DIR / "calibration_summary.json").read_text(encoding="utf-8")
)


def _zh_checker(tmp_path: Path, body: str):
    path = tmp_path / "thesis.tex"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"\\documentclass{{ctexbook}}\n\\begin{{document}}\n{body}\n\\end{{document}}\n",
        encoding="utf-8",
    )
    return ZH.ChineseAITraceChecker(path)


def _en_checker(tmp_path: Path, body: str):
    path = tmp_path / "paper.tex"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"\\documentclass{{article}}\n\\begin{{document}}\n{body}\n\\end{{document}}\n",
        encoding="utf-8",
    )
    return EN.AITraceChecker(path)


def _term_traces(checker) -> list[dict]:
    return checker._check_term_threshold()


def test_loader_reaches_the_zh_density_runtime() -> None:
    assert hasattr(ZH, "ChineseAITraceChecker")
    assert not hasattr(ZH, "AITraceChecker")
    assert ZH.DEFAULT_THRESHOLDS["threshold_unit"] == "per_10k_chars"


def test_visible_prose_adapter_excludes_protected_multiline_content(tmp_path: Path) -> None:
    checker = _zh_checker(
        tmp_path,
        r"""
\chapter{绪论}
普通正文保留标记。
引用载荷 \cite{引用秘密}、\ref{引用秘密} 与 \label{引用秘密} 不计。
行内数学 $数学秘密$ 不计。% 注释秘密
\begin{equation}
公式秘密 = 数学秘密
\end{equation}
\begin{figure}
\caption{图注秘密}
图中秘密
\end{figure}
\begin{table}
表格秘密
\end{table}
\begin{algorithm}
算法秘密
\end{algorithm}
末尾正文同样保留。
""",
    )
    visible = "\n".join(text for _line, _section, text in checker._iter_visible_lines())
    assert "普通正文保留标记" in visible
    assert "末尾正文同样保留" in visible
    for protected in (
        "引用秘密",
        "数学秘密",
        "注释秘密",
        "公式秘密",
        "图注秘密",
        "图中秘密",
        "表格秘密",
        "算法秘密",
    ):
        assert protected not in visible


def test_en_visible_prose_adapter_uses_the_same_exclusion_contract(tmp_path: Path) -> None:
    checker = _en_checker(
        tmp_path,
        r"""
\section{Introduction}
Visible prose remains.
Hidden \cite{secretpayload} and inline $secretmath$ do not count. % secretcomment
\begin{table}
secret table payload
\end{table}
Final visible prose remains.
""",
    )
    visible = "\n".join(text for _line, _section, text in checker._iter_visible_lines())
    assert "Visible prose remains" in visible
    assert "Final visible prose remains" in visible
    for protected in ("secretpayload", "secretmath", "secretcomment", "secret table payload"):
        assert protected not in visible


def test_short_document_uses_fallback_without_direction_flip(tmp_path: Path) -> None:
    short = _zh_checker(tmp_path / "short", "\\chapter{绪论}\n" + "显然" * 3 + "甲" * 900)
    short.thresholds["term_thresholds"] = {"显然": 5.0}
    short_traces = _term_traces(short)
    assert len(short_traces) == 1
    assert "fallback/短文档回退" in short_traces[0]["text"]

    expanded = _zh_checker(
        tmp_path / "expanded",
        "\\chapter{绪论}\n" + ("显然" * 3 + "甲" * 900) * 3,
    )
    expanded.thresholds["term_thresholds"] = {"显然": 5.0}
    assert len(_term_traces(expanded)) == 1


def test_density_guard_still_fires_above_twice_the_limit(tmp_path: Path) -> None:
    checker = _zh_checker(tmp_path, "\\chapter{绪论}\n" + "显然" * 5 + "甲" * 10000)
    checker.thresholds["term_thresholds"] = {"显然": 2.0}
    trace = _term_traces(checker)[0]
    assert "density" in trace["text"]
    assert "fallback/短文档回退" not in trace["text"]


def test_throat_clearing_reports_only_hits_beyond_document_budget(tmp_path: Path) -> None:
    paragraphs = ["综上所述，" + "甲" * 2500 for _ in range(4)]
    checker = _zh_checker(tmp_path, "\\chapter{绪论}\n\n" + "\n\n".join(paragraphs))
    traces = checker._check_throat_clearing("introduction")
    assert len(traces) == 1
    assert "命中 4 / 预算 3 / 第 4 处" in traces[0]["text"]


def test_sequence_terms_receive_only_the_classified_section_allowance(tmp_path: Path) -> None:
    prose = "首先，" * 6 + "甲" * 1000
    background = _zh_checker(tmp_path / "background", "\\chapter{绪论}\n" + prose)
    organization = _zh_checker(
        tmp_path / "organization",
        "\\section{论文组织结构安排}\n" + prose,
    )
    for checker in (background, organization):
        checker.thresholds["term_thresholds"] = {"首先": 8.7}

    assert background.section_ranges.keys() == {"introduction"}
    assert organization.section_ranges.keys() == {"organization"}
    assert len(_term_traces(background)) == 1
    assert _term_traces(organization) == []


def test_en_per_document_limits_stay_legacy_until_c3(tmp_path: Path) -> None:
    checker = _en_checker(tmp_path, "\\section{Introduction}\n" + "novel " * 5)
    traces = _term_traces(checker)
    novel = next(trace for trace in traces if trace["pattern"] == "term_threshold:novel")
    assert "legacy cap 4" in novel["text"]
    assert checker.thresholds["threshold_unit"] == "per_document"


def test_custom_yaml_without_unit_keeps_absolute_semantics_and_warns(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    scripts_dir = tmp_path / "skill" / "scripts"
    thresholds_dir = tmp_path / "skill" / "references" / "deai"
    scripts_dir.mkdir(parents=True)
    thresholds_dir.mkdir(parents=True)
    (thresholds_dir / EN.THRESHOLDS_FILENAME).write_text(
        "term_thresholds:\n  novel: 7\n",
        encoding="utf-8",
    )
    loaded = EN._load_thresholds(scripts_dir)
    assert loaded["_legacy_term_thresholds"] is True
    assert loaded["term_thresholds"]["novel"] == 7
    assert "has no threshold_unit" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("excerpt", "expected_trace_count"),
    zip(_THESIS_EXCERPTS, [2, 2, 6, 2, 3], strict=True),
    ids=[f"paper-{index}" for index in range(1, 6)],
)
def test_five_thesis_excerpts_keep_term_traces_in_single_digits(
    tmp_path: Path,
    excerpt: dict[str, str],
    expected_trace_count: int,
) -> None:
    body = (
        "\\chapter{绪论}\n"
        f"{excerpt['background']}\n"
        "\\section{论文组织结构安排}\n"
        f"{excerpt['organization']}"
    )
    corpus = len(re.findall(r"[\u4e00-\u9fff]", excerpt["background"] + excerpt["organization"]))
    assert 3000 <= corpus <= 5000
    assert excerpt["source"].startswith("ref/thesis/decrypted/")
    assert len(_term_traces(_zh_checker(tmp_path, body))) == expected_trace_count < 10


def test_checked_in_calibration_summary_matches_zh_thresholds_and_budget() -> None:
    result = _CALIBRATION_SUMMARY
    yaml_path = SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "tone-thresholds.yaml"
    configured = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    assert result["term_thresholds"] == configured["term_thresholds"]
    assert result["section_factors"] == configured["section_factors"]
    assert result["throat_clearing"]["budget_per_10k"] == 2.6

    term_trace_counts = [
        sum(
            float(paper["term_densities"][term]) > density
            for term, density in result["term_thresholds"].items()
        )
        for paper in result["papers"]
    ]
    assert term_trace_counts == [0, 0, 1, 2, 0]

    excess = [
        max(
            0,
            int(paper["throat_hits"]) - max(1, round(2.6 * int(paper["corpus"]) / 10000)),
        )
        for paper in result["papers"]
    ]
    assert excess == [0, 0, 0, 8, 0]
    assert sum(excess) > 0
    assert all(
        output_count != int(paper["throat_hits"])
        for output_count, paper in zip(excess, result["papers"], strict=True)
    )


def test_live_calibration_reproduces_checked_in_summary_when_corpus_is_available() -> None:
    script = (
        REPO_ROOT
        / ".trellis"
        / "tasks"
        / "08-29-writing-rhythm-arc"
        / "research"
        / "calibrate_density.py"
    )
    thesis_files = sorted((REPO_ROOT / "ref" / "thesis" / "decrypted").glob("*.txt"))
    if len(thesis_files) != 5:
        pytest.skip("private five-thesis calibration corpus is not available")
    spec = importlib.util.spec_from_file_location("_density_calibration", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        module.main()
    result = json.loads(output.getvalue())
    assert result == _CALIBRATION_SUMMARY
