"""`--results-analysis` 区间、RA-* 判据与回归边界。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH, SKILLS_ROOT, TESTS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "analyze_experiment.py"
_FIXTURES = TESTS_ROOT / "skills" / "latex_thesis_zh" / "fixtures" / "results_analysis"
_CALIBRATION_REPORT = (
    REPO_ROOT
    / ".trellis"
    / "tasks"
    / "archive"
    / "2026-08"
    / "08-10-results-checker-zh"
    / "research"
    / "calibration-report.md"
)
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh():
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location("zh_results_analysis", _SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


experiment = _load_zh()


def _report(path: Path, *, section: str | None = None, per_chapter: bool = False) -> str:
    return "\n".join(
        experiment.analyze(
            path,
            section=section,
            per_chapter=per_chapter,
            results_analysis=True,
        )
    )


def _matrix(section_number: int) -> str:
    key = "result" if section_number == 1 else f"result_{section_number}"
    return _report(_FIXTURES / "rule_matrix.tex", section=key)


def test_loader_targets_zh_copy_and_results_family() -> None:
    assert experiment.__file__ is not None
    assert Path(experiment.__file__).resolve() == _SCRIPT.resolve()
    assert hasattr(experiment, "RA_METRIC_TERM_RE")
    assert hasattr(experiment, "_collect_results_intervals")


def test_dual_channel_overlap_is_deduplicated_in_favor_of_chapter_intervals() -> None:
    path = _FIXTURES / "intervals.tex"
    parser = experiment.get_parser(path)
    doc = experiment.assemble(path)

    intervals = experiment._collect_results_intervals(doc.lines, doc.content, parser)

    assert len(intervals) == 4
    result_intervals = [item for item in intervals if item["source"] == "chapter"]
    assert len(result_intervals) == 2
    assert len({(item["start"], item["end"]) for item in result_intervals}) == 2
    assert [item["key"] for item in intervals if item["source"] == "global"] == [
        "discussion",
        "discussion_2",
    ]


def test_section_selects_the_complete_result_suffix_family_without_chapter_channel() -> None:
    path = _FIXTURES / "intervals.tex"
    parser = experiment.get_parser(path)
    doc = experiment.assemble(path)

    intervals = experiment._collect_results_intervals(
        doc.lines, doc.content, parser, section="result"
    )

    assert len(intervals) == 2
    assert [item["key"] for item in intervals] == ["result", "result_2"]
    assert all(item["source"] == "global" for item in intervals)


@pytest.mark.parametrize(
    ("section", "expected_keys"),
    (
        ("results", ["result", "result_2"]),
        ("result_2", ["result_2"]),
        ("discussion", ["discussion", "discussion_2"]),
        ("missing", []),
    ),
)
def test_section_uses_only_the_exact_normalized_suffix_family(
    section: str, expected_keys: list[str]
) -> None:
    path = _FIXTURES / "intervals.tex"
    parser = experiment.get_parser(path)
    doc = experiment.assemble(path)

    intervals = experiment._collect_results_intervals(
        doc.lines, doc.content, parser, section=section
    )

    assert [item["key"] for item in intervals] == expected_keys
    assert all(item["source"] == "global" for item in intervals)


def test_paragraphs_preserve_raw_refs_but_remove_them_from_visible_text() -> None:
    path = _FIXTURES / "rule_matrix.tex"
    parser = experiment.get_parser(path)
    doc = experiment.assemble(path)
    interval = experiment._collect_results_intervals(
        doc.lines, doc.content, parser, section="result_9"
    )[0]

    paragraphs = experiment._split_ra_paragraphs(
        doc.lines, interval["start"], interval["end"], parser
    )
    target = next(item for item in paragraphs if "fig:curve" in item["raw_text"])

    assert set(target) == {"start_line", "raw_text", "visible_text"}
    assert r"\ref{fig:curve}" in target["raw_text"]
    assert r"\ref{fig:curve}" not in target["visible_text"]
    assert "曲线更加贴合" in target["visible_text"]


@pytest.mark.parametrize(
    ("positive_section", "negative_section", "code"),
    (
        (1, 2, "RA-EQUIV"),
        (7, 8, "RA-SECONDBEST"),
        (9, 10, "RA-SHALLOW"),
        (11, 12, "RA-DISTVOCAB"),
        (13, 14, "RA-UNIVERSAL"),
        (15, 16, "RA-STAGE"),
        (17, 18, "RA-TRANSITION"),
    ),
)
def test_each_ra_rule_has_a_positive_and_negative_boundary(
    positive_section: int, negative_section: int, code: str
) -> None:
    assert code in _matrix(positive_section)
    assert code not in _matrix(negative_section)


def test_causal_three_tier_scope_and_consistency_exclusion() -> None:
    major = _matrix(3)
    local = _matrix(4)
    chapter_only = _matrix(5)
    consistency = _matrix(6)

    assert "[Severity: Major] [Priority: P1]: [Script] RA-CAUSAL" in major
    assert "RA-CAUSAL" not in local
    assert "[Severity: Minor] [Priority: P2]: [Script] RA-CAUSAL" in chapter_only
    assert "RA-CAUSAL" not in consistency


@pytest.mark.parametrize(
    "prefix",
    (
        "误差变化与门控结构一致。",
        "误差归因分析用于定位异常来源。",
    ),
)
def test_causal_exclusions_do_not_mask_a_separate_claim_in_the_same_paragraph(
    tmp_path: Path, prefix: str
) -> None:
    path = tmp_path / "main.tex"
    path.write_text(
        "\\chapter{模型验证}\n"
        "\\section{结果分析}\n"
        f"{prefix}完整方法的性能提升主要归因于门控模块。\n"
        "\\section{本章小结}\n"
        "本章完成比较。\n",
        encoding="utf-8",
    )

    assert "[Severity: Major] [Priority: P1]: [Script] RA-CAUSAL" in _report(path)


def test_math_equivalence_does_not_mask_a_separate_statistical_claim(tmp_path: Path) -> None:
    path = tmp_path / "main.tex"
    path.write_text(
        "\\chapter{模型验证}\n"
        "\\section{结果分析}\n"
        "目标函数可作等价变换。方法 A 与方法 B 统计等价。\n"
        "\\section{本章小结}\n"
        "本章完成比较。\n",
        encoding="utf-8",
    )

    assert "RA-EQUIV" in _report(path)


def test_secondbest_ignores_runner_up_terms_from_another_section_in_same_chapter(
    tmp_path: Path,
) -> None:
    path = tmp_path / "main.tex"
    path.write_text(
        r"""\chapter{模型验证}
\section{结果分析}
表\ref{tab:main}汇总各模型结果。
方法 A 的 RMSE 最低。
工况甲用于总体评价。
工况乙用于边界评价。
工况丙用于稳健性评价。
工况丁用于迁移评价。
训练预算保持一致。
评价协议保持一致。
\section{补充实验}
次优方法 B 仅用于另一项补充实验。
\section{本章小结}
本章完成比较。
""",
        encoding="utf-8",
    )

    assert _report(path).count("RA-SECONDBEST") == 1


def test_stage_distinguishes_two_sentences_on_the_same_physical_line(tmp_path: Path) -> None:
    path = tmp_path / "main.tex"
    path.write_text(
        "\\chapter{保真度验证}\n"
        "\\section{结果分析}\n"
        "选定集的 KS 较低。生成样本的 W1 较低。\n"
        "\\section{本章小结}\n"
        "本章完成比较。\n",
        encoding="utf-8",
    )

    assert "RA-STAGE" in _report(path)


def test_stage_requires_two_fidelity_terms_and_the_final_object_term_groups(
    tmp_path: Path,
) -> None:
    no_gate = tmp_path / "no_gate.tex"
    no_gate.write_text(
        "\\chapter{保真度验证}\n"
        "\\section{结果分析}\n"
        "选定集的误差较低。生成样本的误差也较低。\n"
        "\\section{本章小结}\n"
        "本章完成比较。\n",
        encoding="utf-8",
    )
    outside_terms = tmp_path / "outside_terms.tex"
    outside_terms.write_text(
        "\\chapter{保真度验证}\n"
        "\\section{结果分析}\n"
        "选定集的 KS 较低。最终样本的 W1 较低。\n"
        "\\section{本章小结}\n"
        "本章完成比较。\n",
        encoding="utf-8",
    )

    assert "RA-STAGE" not in _report(no_gate)
    assert "RA-STAGE" not in _report(outside_terms)


def test_defensive_rhetoric_five_case_fixture_stays_outside_ra_causal() -> None:
    fixture = _FIXTURES / "defensive_boundaries.tex"
    text = fixture.read_text(encoding="utf-8")
    report = _report(fixture)

    for label in ("样例 A", "样例 B", "样例 C", "样例 D", "样例 E"):
        assert label in text
    assert "RA-CAUSAL" not in report


def test_removed_interleave_candidate_is_absent_from_runtime_and_public_routes() -> None:
    assert "RA-INTERLEAVE" not in _matrix(19)
    assert "RA-INTERLEAVE" not in _matrix(20)
    for relative_path in (
        "SKILL.md",
        "scripts/analyze_experiment.py",
        "references/modules/experiment.md",
        "references/modules/routing-rules.md",
        "references/writing/results-analysis-guide-zh.md",
    ):
        text = (SKILLS_ROOT / "latex-thesis-zh" / relative_path).read_text(encoding="utf-8")
        assert "RA-INTERLEAVE" not in text
    calibration = _CALIBRATION_REPORT.read_text(encoding="utf-8")
    assert "RA-INTERLEAVE" in calibration and "删除" in calibration
    assert "UNVERIFIED / missing evidence" in calibration


def test_duplicate_interval_reports_each_finding_once() -> None:
    report = _report(_FIXTURES / "intervals.tex")

    assert report.count("RA-EQUIV") == 2


def test_results_analysis_combines_with_per_chapter_without_changing_e_family() -> None:
    report = _report(_FIXTURES / "intervals.tex", per_chapter=True)

    assert "RA-EQUIV" in report
    assert "E-" in report

    selected = _report(_FIXTURES / "intervals.tex", section="result_2", per_chapter=True)
    assert selected.count("RA-EQUIV") == 1
    assert "E-" in selected


def test_section_mode_honors_the_owning_chapter_summary_red_line() -> None:
    report = _report(_FIXTURES / "intervals.tex", section="discussion")

    assert "RA-TRANSITION" not in report


def test_non_trigger_red_lines_stay_silent(tmp_path: Path) -> None:
    path = tmp_path / "main.tex"
    path.write_text(
        r"""\chapter{模型验证}
\section{结果分析}
表\ref{tab:main}仅记录描述性统计，未设置方法间比较。
结果接近参照，置信上界处于上界内，其余区间内数值作描述性记录。
本节未使用显著性检验，也未报告均值加方差；人工经验基线用于优化对照。
\section{本章小结}
本章完成比较。
""",
        encoding="utf-8",
    )

    report = _report(path)
    for code in (
        "RA-EQUIV",
        "RA-CAUSAL",
        "RA-SECONDBEST",
        "RA-SHALLOW",
        "RA-DISTVOCAB",
        "RA-UNIVERSAL",
        "RA-STAGE",
        "RA-TRANSITION",
    ):
        assert code not in report


def test_multifile_finding_uses_source_file_and_line_number() -> None:
    report = _report(_FIXTURES / "multifile" / "main.tex")

    assert "(chapters/results.tex:3)" in report
    assert "RA-EQUIV" in report


def test_default_and_per_chapter_modes_do_not_run_ra_family(tmp_path: Path) -> None:
    path = tmp_path / "main.tex"
    path.write_text((_FIXTURES / "intervals.tex").read_text(encoding="utf-8"), encoding="utf-8")

    default_report = "\n".join(experiment.analyze(path))
    chapter_report = "\n".join(experiment.analyze(path, per_chapter=True))

    assert "RA-" not in default_report
    assert "RA-" not in chapter_report


def test_missing_results_interval_emits_structural_info(tmp_path: Path) -> None:
    path = tmp_path / "main.tex"
    path.write_text("\\chapter{绪论}\n研究背景。\n", encoding="utf-8")

    report = _report(path)

    assert "[Severity: Info] [Priority: P3]: [Script] RA-STRUCT" in report
    assert "--section" in report


def test_results_analysis_eval_is_append_only_and_binds_real_fixture() -> None:
    skill_root = SKILLS_ROOT / "latex-thesis-zh"
    payload = json.loads((skill_root / "evals" / "evals.json").read_text(encoding="utf-8"))
    matches = [item for item in payload["evals"] if item["id"] == 30]

    assert len(matches) == 1
    semantic_eval = matches[0]
    assert semantic_eval["files"] == ["evals/fixtures/results_analysis_boundary.tex"]
    eval_ids = [item["id"] for item in payload["evals"]]
    assert eval_ids == sorted(eval_ids)
    assert len(set(eval_ids)) == len(eval_ids)

    fixture = (skill_root / semantic_eval["files"][0]).read_text(encoding="utf-8")
    for label in ("样例 A", "样例 B", "样例 C", "样例 D", "样例 E"):
        assert label in fixture
