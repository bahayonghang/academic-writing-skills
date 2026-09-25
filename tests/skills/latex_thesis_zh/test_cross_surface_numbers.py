"""Opt-in cross-surface number candidates for latex-thesis-zh."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH, SKILLS_ROOT, TESTS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "analyze_experiment.py"
_SKILL = SKILLS_ROOT / "latex-thesis-zh"
_RA_FIXTURE = TESTS_ROOT / "skills" / "latex_thesis_zh" / "fixtures" / "results_analysis"
_CONTRACT = (
    REPO_ROOT
    / ".trellis"
    / "spec"
    / "academic-writing-skills"
    / "results-analysis-checker-contract.md"
)
_SHARED = ("parsers", "tex_loader")
_STATS_RE = re.compile(
    r"compared_keys=(\d+) uncovered=(\d+) differences=(\d+)。本检查不是全文合规证明。"
)
_TERMS = {"metrics": ["合成指标", "对照指标"], "eval_sets": ["合成评价集", "对照评价集"]}


def _load_zh():
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in _SHARED}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location("zh_cross_surface", _SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


experiment = _load_zh()


def _doc(*chapters: str) -> str:
    body = "\n".join(chapters)
    return "\\documentclass{ctexbook}\n\\begin{document}\n" + body + "\n\\end{document}\n"


def _chapter(title: str, table: str, body: str, summary: str | None) -> str:
    parts = [f"\\chapter{{{title}}}"]
    if table:
        parts.append(table.rstrip("\n"))
    if body:
        parts.append(body)
    if summary is not None:
        parts.append("\\section{本章小结}")
        if summary:
            parts.append(summary)
    return "\n".join(parts) + "\n"


def _table(
    cell: str = r"92.3\%",
    header: str = "合成指标",
    caption: str = "合成评价集上的比较",
    label: str = "tab:syn",
    row: str = "方法甲",
    env: str = "table",
    extra_header: str = "",
    extra_cell: str = "",
) -> str:
    if extra_header:
        spec = "lll"
        header_line = f"方法 & {header} & {extra_header} \\\\"
        data_line = f"{row} & {cell} & {extra_cell} \\\\"
    else:
        spec = "ll"
        header_line = f"方法 & {header} \\\\"
        data_line = f"{row} & {cell} \\\\"
    end = "table*" if env == "table*" else env
    return (
        f"\\begin{{{env}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\label{{{label}}}\n"
        f"\\begin{{tabular}}{{{spec}}}\n"
        f"{header_line}\n"
        "\\hline\n"
        f"{data_line}\n"
        "\\end{tabular}\n"
        f"\\end{{{end}}}\n"
    )


def _claim(
    value: str = r"92.3\%",
    metric: str = "合成指标",
    eval_set: str = "合成评价集",
    row: str = "方法甲",
    label: str = "tab:syn",
) -> str:
    return f"表\\ref{{{label}}}中{row}在{eval_set}上的{metric}为 {value}。"


def _write(tmp: Path, text: str, name: str = "main.tex") -> Path:
    path = tmp / name
    path.write_text(text, encoding="utf-8")
    return path


def _terms(tmp: Path, payload: dict | None = None) -> Path:
    path = tmp / "terms.json"
    path.write_text(
        json.dumps(_TERMS if payload is None else payload, ensure_ascii=False), encoding="utf-8"
    )
    return path


def _xs(
    path: Path,
    terms: Path | None = None,
    section: str | None = None,
    results: bool = False,
) -> str:
    return "\n".join(
        experiment.analyze(
            path,
            section=section,
            results_analysis=results,
            cross_surface=True,
            cross_surface_terms=terms,
        )
    )


def _stats(report: str) -> tuple[int, int, int]:
    match = _STATS_RE.search(report)
    assert match, report
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def _assert_info(report: str) -> None:
    for line in report.splitlines():
        if "RA-XS-" not in line:
            continue
        assert "[Severity: Info]" in line
        assert "[Priority: P3]" in line
        assert "[Script]" in line
        assert "Meaning-Check: NEEDS-LLM" in line
        assert "应为" not in line


def _equal_doc() -> str:
    claim = _claim()
    return _doc(_chapter("性能结果", _table(), claim, claim))


def _cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(_SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def test_loader_targets_zh_cross_surface_copy() -> None:
    assert experiment.__file__ is not None
    assert Path(experiment.__file__).resolve() == _SCRIPT.resolve()
    assert experiment.DEFAULT_XS_METRICS == ("准确率", "精确率", "召回率", "F1", "误差")
    assert experiment.DEFAULT_XS_EVAL_SETS == ("测试集", "验证集", "训练集")
    assert len(experiment.RA_CHECKERS) == 8
    assert "合成指标" not in experiment.RA_METRIC_TERM_RE.pattern


def test_three_surfaces_equal_compares_one_key(tmp_path: Path) -> None:
    report = _xs(_write(tmp_path, _equal_doc()), _terms(tmp_path))
    _assert_info(report)
    assert _stats(report) == (1, 0, 0)
    for code in ("RA-XS-BODY", "RA-XS-SUMMARY", "RA-XS-MISSING", "RA-XS-COVERAGE"):
        assert code not in report


def test_body_mismatch_does_not_report_summary(tmp_path: Path) -> None:
    text = _doc(_chapter("性能结果", _table(), _claim(r"92.1\%"), _claim()))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    _assert_info(report)
    assert "RA-XS-BODY" in report
    assert "RA-XS-SUMMARY" not in report
    assert "RA-XS-MISSING" not in report
    assert "92.1" not in report and "92.3" not in report
    assert _stats(report)[0] == 1
    assert _stats(report)[2] == 1


def test_other_metric_same_digits_do_not_cancel_body_difference(tmp_path: Path) -> None:
    table = _table(extra_header="对照指标", extra_cell=r"92.1\%")
    text = _doc(_chapter("性能结果", table, _claim(r"92.1\%"), _claim()))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    assert "RA-XS-BODY" in report
    assert "RA-XS-SUMMARY" not in report
    assert "92.1" not in report and "92.3" not in report


def test_missing_surfaces_and_missing_row(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    no_heading = _doc(_chapter("性能结果", _table(), _claim(), None))
    missing_heading = _xs(_write(tmp_path, no_heading, "no-heading.tex"), terms)
    assert "RA-XS-MISSING" in missing_heading and "小结" in missing_heading
    assert "无小结" in missing_heading
    assert "RA-XS-BODY" not in missing_heading

    quiet = _doc(_chapter("性能结果", _table(), "实验设置如下。", _claim()))
    missing_body = _xs(_write(tmp_path, quiet, "no-body.tex"), terms)
    assert "RA-XS-MISSING" in missing_body and "正文" in missing_body
    assert "RA-XS-BODY" not in missing_body
    assert _stats(missing_body)[2] == 0

    absent_row = _doc(_chapter("性能结果", _table(), "实验设置如下。", _claim(row="方法乙")))
    missing_record = _xs(_write(tmp_path, absent_row, "no-row.tex"), terms)
    assert "RA-XS-SUMMARY" in missing_record
    assert "92.3" not in missing_record


def test_ambiguous_bindings_are_needs_llm_without_a_compared_key(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    cases = {
        "two-refs.tex": _doc(
            _chapter(
                "性能结果",
                _table() + _table(label="tab:other"),
                "表\\ref{tab:syn}与表\\ref{tab:other}中方法甲在合成评价集上的合成指标为 92.3\\%。",
                "实验设置如下。",
            )
        ),
        "unit.tex": _doc(_chapter("性能结果", _table(), _claim("92.3 ms"), _claim("92.3 ms"))),
        "eval.tex": _doc(
            _chapter(
                "性能结果",
                _table(caption="比较结果"),
                "表\\ref{tab:syn}中方法甲的合成指标为 92.3\\%。",
                "表\\ref{tab:syn}中方法甲的合成指标为 92.3\\%。",
            )
        ),
        "object.tex": _doc(
            _chapter(
                "性能结果",
                _table(),
                "表\\ref{tab:syn}在合成评价集上的合成指标为 92.3\\%。",
                "表\\ref{tab:syn}在合成评价集上的合成指标为 92.3\\%。",
            )
        ),
    }
    for name, text in cases.items():
        report = _xs(_write(tmp_path, text, name), terms)
        _assert_info(report)
        assert "RA-XS-COVERAGE" in report
        assert "RA-XS-BODY" not in report and "RA-XS-SUMMARY" not in report
        assert _stats(report)[0] == 0


def test_grouping_sign_interval_and_scientific_notation_normalize(tmp_path: Path) -> None:
    rows = (
        ("分组对象", r"1\,234.5\%", r"1234.5\%"),
        ("负号对象", r"$-$2.5\%", r"-2.5\%"),
        ("区间对象", r"3.40--1.20\%", r"1.20--3.40\%"),
        ("科学对象", r"$1.23\times 10^{2}\%$", r"123\%"),
    )
    header = "方法 & 合成指标 \\\\"
    data = "\n".join(f"{row} & {cell} \\\\" for row, cell, _value in rows)
    table = (
        "\\begin{table}\n\\caption{合成评价集上的比较}\n\\label{tab:syn}\n"
        "\\begin{tabular}{ll}\n"
        f"{header}\n\\hline\n{data}\n\\end{{tabular}}\n\\end{{table}}\n"
    )
    prose = "\n".join(_claim(value, row=row) for row, _cell, value in rows)
    report = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, prose, prose))), _terms(tmp_path)
    )
    assert _stats(report) == (4, 0, 0)
    assert "RA-XS-BODY" not in report


def test_interval_endpoint_is_not_the_same_value(tmp_path: Path) -> None:
    table = _table(cell=r"1.20--3.40\%")
    text = _doc(_chapter("性能结果", table, _claim(r"1.20\%"), _claim(r"1.20--3.40\%")))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    assert "RA-XS-BODY" in report
    assert "RA-XS-SUMMARY" not in report


def test_percent_is_not_rescaled_to_a_fraction(tmp_path: Path) -> None:
    table = _table(cell=r"92.1\%")
    text = _doc(_chapter("性能结果", table, _claim("0.921"), _claim(r"92.1\%")))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    assert "RA-XS-BODY" not in report
    assert "RA-XS-COVERAGE" in report
    assert "RA-XS-MISSING" in report and "正文" in report


def test_dimensionless_requires_an_explicit_marker(tmp_path: Path) -> None:
    table = _table(cell="0.50", header="合成指标（无量纲）")
    marked = _claim("0.50").replace("为 0.50", "为无量纲 0.50")
    bound = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, marked, marked)), "yes.tex"),
        _terms(tmp_path),
    )
    assert _stats(bound) == (1, 0, 0)

    bare = _claim("0.50")
    unbound = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, bare, bare)), "no.tex"),
        _terms(tmp_path),
    )
    assert _stats(unbound)[0] == 0
    assert "RA-XS-BODY" not in unbound


def test_uncovered_syntax_missing_table_and_missing_summary(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    multi = _doc(
        _chapter(
            "性能结果",
            "\\begin{table}\n\\caption{合成评价集上的比较}\n\\label{tab:syn}\n"
            "\\begin{tabular}{ll}\n方法 & 合成指标 \\\\\n"
            "\\multirow{2}{*}{方法甲} & 92.3\\% \\\\\n\\end{tabular}\n\\end{table}\n",
            _claim(),
            _claim(),
        )
    )
    multi_report = _xs(_write(tmp_path, multi, "multirow.tex"), terms)
    assert "RA-XS-COVERAGE" in multi_report
    assert "RA-XS-BODY" not in multi_report
    assert _stats(multi_report)[0] == 0
    assert "92.3" not in multi_report

    macro = _doc(
        _chapter(
            "性能结果",
            "\\begin{table}\n\\caption{合成评价集上的比较}\n\\label{tab:macro}\n"
            "\\resulttable\n\\end{table}\n",
            _claim(label="tab:macro"),
            _claim(label="tab:macro"),
        )
    )
    macro_report = _xs(_write(tmp_path, macro, "macro.tex"), terms)
    assert "RA-XS-COVERAGE" in macro_report and _stats(macro_report)[0] == 0
    assert "92.3" not in macro_report

    no_table = _doc(_chapter("性能结果", "", _claim(), _claim()))
    no_table_report = _xs(_write(tmp_path, no_table, "notable.tex"), terms)
    assert "无结果表" in no_table_report
    assert _stats(no_table_report)[0] == 0
    assert "RA-XS-BODY" not in no_table_report


def test_table_star_and_longtable_bind(tmp_path: Path) -> None:
    star = _chapter("性能结果", _table(env="table*"), _claim(), _claim())
    longtable = (
        "\\chapter{补充性能}\n"
        "\\begin{longtable}{ll}\n"
        "\\caption{合成评价集上的比较}\\\\\n"
        "\\label{tab:long}\\\\\n"
        "方法 & 合成指标 \\\\\n"
        "方法甲 & 92.3\\% \\\\\n"
        "\\end{longtable}\n"
        + _claim(label="tab:long")
        + "\n\\section{本章小结}\n"
        + _claim(label="tab:long")
        + "\n"
    )
    report = _xs(_write(tmp_path, _doc(star, longtable)), _terms(tmp_path))
    assert _stats(report) == (2, 0, 0)


def test_include_keeps_chapters_isolated(tmp_path: Path) -> None:
    ch1 = _chapter("合成章一", _table(), _claim(), _claim())
    ch2 = (
        "\\chapter{合成章二}\n"
        + _table(cell=r"10.0\%", label="tab:two", row="方法乙")
        + _claim(r"10.0\%", row="方法乙", label="tab:two")
        + "\n"
        + _claim(label="tab:syn")
        + "\n\\section{本章小结}\n"
        + _claim(r"10.0\%", row="方法乙", label="tab:two")
        + "\n"
    )
    (tmp_path / "ch1.tex").write_text(ch1, encoding="utf-8")
    (tmp_path / "ch2.tex").write_text(ch2, encoding="utf-8")
    main = _write(
        tmp_path,
        "\\documentclass{ctexbook}\n\\begin{document}\n\\input{ch1}\n\\input{ch2}\n\\end{document}\n",
    )
    report = _xs(main, _terms(tmp_path))
    _assert_info(report)
    assert _stats(report)[0] == 2
    assert "RA-XS-BODY" not in report and "RA-XS-SUMMARY" not in report
    assert any("ch2.tex:" in line and "不在本章" in line for line in report.splitlines())


def test_section_limits_the_scan(tmp_path: Path) -> None:
    first = _chapter("性能结果", _table(), _claim(), _claim())
    second = _chapter(
        "方法设计",
        _table(label="tab:other"),
        _claim(r"11.0\%", label="tab:other"),
        _claim(label="tab:other"),
    )
    path = _write(tmp_path, _doc(first, second))
    terms = _terms(tmp_path)
    limited = _xs(path, terms, section="result")
    assert "RA-XS-BODY" not in limited
    assert _stats(limited) == (1, 0, 0)
    full = _xs(path, terms)
    assert "RA-XS-BODY" in full
    missed = _xs(path, terms, section="abstract")
    assert _stats(missed)[0] == 0
    assert "未命中指定章节" in missed


def test_custom_terms_replace_only_present_fields(tmp_path: Path) -> None:
    synthetic = _write(tmp_path, _equal_doc(), "synthetic.tex")
    assert _stats(_xs(synthetic))[0] == 0
    assert _stats(_xs(synthetic, _terms(tmp_path, _TERMS))) == (1, 0, 0)

    default_claim = _claim(metric="准确率", eval_set="测试集", value=r"91.0\%")
    default_doc = _doc(
        _chapter(
            "性能结果",
            _table(cell=r"91.0\%", header="准确率", caption="测试集上的比较"),
            default_claim,
            default_claim,
        )
    )
    default_path = _write(tmp_path, default_doc, "default.tex")
    assert _stats(_xs(default_path)) == (1, 0, 0)
    assert _stats(_xs(default_path, _terms(tmp_path, {}))) == (1, 0, 0)

    metric_only = _claim(metric="合成指标", eval_set="测试集")
    metric_doc = _doc(
        _chapter(
            "性能结果",
            _table(caption="测试集上的比较"),
            metric_only,
            metric_only,
        )
    )
    metric_path = _write(tmp_path, metric_doc, "metric.tex")
    assert _stats(_xs(metric_path, _terms(tmp_path, {"metrics": ["合成指标"]}))) == (1, 0, 0)

    eval_only = _claim(metric="准确率", eval_set="合成评价集", value=r"91.0\%")
    eval_doc = _doc(
        _chapter(
            "性能结果",
            _table(cell=r"91.0\%", header="准确率", caption="合成评价集上的比较"),
            eval_only,
            eval_only,
        )
    )
    eval_path = _write(tmp_path, eval_doc, "eval.tex")
    assert _stats(_xs(eval_path, _terms(tmp_path, {"eval_sets": ["合成评价集"]}))) == (1, 0, 0)

    empty = _xs(default_path, _terms(tmp_path, {"metrics": [], "eval_sets": ["测试集"]}))
    assert _stats(empty)[0] == 0


@pytest.mark.parametrize(
    "payload",
    ["{", "[]", '{"metrics":"合成指标"}', '{"metrics":[1]}', '{"extra":[]}', '{"metrics":[""]}'],
)
def test_illegal_terms_exit_nonzero(tmp_path: Path, payload: str) -> None:
    tex = _write(tmp_path, _equal_doc())
    bad = tmp_path / "bad.json"
    bad.write_text(payload, encoding="utf-8")
    result = _cli(str(tex), "--cross-surface", "--cross-surface-terms", str(bad))
    assert result.returncode != 0
    assert "不是全文合规证明" not in result.stdout
    assert result.stdout.strip() == ""


def test_terms_flag_without_cross_surface_is_a_parameter_error(tmp_path: Path) -> None:
    tex = _write(tmp_path, _equal_doc())
    missing = tmp_path / "missing.json"
    result = _cli(str(tex), "--results-analysis", "--cross-surface-terms", str(missing))
    assert result.returncode != 0
    assert "requires --cross-surface" in result.stderr
    assert result.stdout.strip() == ""
    assert not missing.exists()


def test_negated_eval_set_and_metric_implication(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    negated = "表\\ref{tab:syn}中不使用合成评价集而使用对照评价集，方法甲的合成指标为 92.3\\%。"
    table = _table(caption="对照评价集上的比较")
    report = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, negated, negated)), "neg.tex"), terms
    )
    assert "RA-XS-EVALSET" not in report
    assert _stats(report) == (1, 0, 0)

    mixed = _doc(
        _chapter(
            "性能结果",
            _table(caption="比较结果"),
            _claim() + _claim(value=r"91.0\%", eval_set="对照评价集"),
            "实验设置如下。",
        )
    )
    mixed_report = _xs(_write(tmp_path, mixed, "mix.tex"), terms)
    assert "RA-XS-EVALSET" in mixed_report
    assert "RA-XS-BODY" not in mixed_report
    assert _stats(mixed_report)[0] == 0

    implied = _doc(_chapter("性能结果", "", "由合成指标可得对照指标。", "实验设置如下。"))
    implied_report = _xs(_write(tmp_path, implied, "metric.tex"), terms)
    assert "RA-XS-METRIC" in implied_report
    assert "RA-XS-BODY" not in implied_report

    denied = _doc(_chapter("性能结果", "", "不能由合成指标可得对照指标。", "实验设置如下。"))
    denied_report = _xs(_write(tmp_path, denied, "denied.tex"), terms)
    assert "RA-XS-METRIC" not in denied_report

    converted = _doc(_chapter("性能结果", "", "合成指标换算为对照指标。", None))
    assert "RA-XS-METRIC" in _xs(_write(tmp_path, converted, "convert.tex"), terms)


def test_default_and_results_analysis_omit_cross_surface_stats(tmp_path: Path) -> None:
    path = _write(tmp_path, _equal_doc())
    default = "\n".join(experiment.analyze(path))
    results = "\n".join(experiment.analyze(path, results_analysis=True))
    for report in (default, results):
        assert "RA-XS-" not in report
        assert "CROSS-SURFACE" not in report
        assert "不是全文合规证明" not in report


def test_both_flags_keep_results_analysis_prefix() -> None:
    path = _RA_FIXTURE / "intervals.tex"
    ra_only = experiment.analyze(path, results_analysis=True)
    both = experiment.analyze(path, results_analysis=True, cross_surface=True)
    assert both[: len(ra_only)] == ra_only
    report = "\n".join(both)
    assert "RA-EQUIV" in report
    assert "不是全文合规证明" in report
    assert "不是全文合规证明" not in "\n".join(ra_only)


def test_guides_and_contract_state_the_narrow_subset() -> None:
    guide = (_SKILL / "references" / "writing" / "results-analysis-guide-zh.md").read_text(
        encoding="utf-8"
    )
    experiment_doc = (_SKILL / "references" / "modules" / "experiment.md").read_text(
        encoding="utf-8"
    )
    routing = (_SKILL / "references" / "modules" / "routing-rules.md").read_text(encoding="utf-8")
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    contract = _CONTRACT.read_text(encoding="utf-8")
    for text in (guide, experiment_doc, routing, skill, contract):
        assert "--cross-surface" in text
    assert "正例：由准确率可得F1" in guide
    assert "反例：不能由准确率可得F1" in guide
    assert "显示层" in guide and "源层" in guide and "分母" in guide
    assert "不输出修正数字" in guide
    assert "RA-XS-BODY" in experiment_doc
    for term in (*experiment.DEFAULT_XS_METRICS, *experiment.DEFAULT_XS_EVAL_SETS):
        assert term in contract
    for code in (
        "RA-XS-BODY",
        "RA-XS-SUMMARY",
        "RA-XS-MISSING",
        "RA-XS-EVALSET",
        "RA-XS-METRIC",
        "RA-XS-COVERAGE",
    ):
        assert code in contract
    assert "check_consistency.py --governance --custom-terms FILE" in skill
    assert "--school yanshan-ee-2025" in skill
    assert "--author-cite" in skill and "--progression-density" in skill


def test_absent_table_row_is_summary_not_body(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    both = _doc(_chapter("性能结果", _table(), _claim(row="方法乙"), _claim(row="方法乙")))
    both_report = _xs(_write(tmp_path, both, "both.tex"), terms)
    _assert_info(both_report)
    assert "RA-XS-SUMMARY" in both_report
    assert "RA-XS-BODY" not in both_report
    assert "RA-XS-MISSING" not in both_report
    assert "92.3" not in both_report

    body_only = _doc(_chapter("性能结果", _table(), _claim(row="方法乙"), "实验设置如下。"))
    body_report = _xs(_write(tmp_path, body_only, "body.tex"), terms)
    assert "RA-XS-SUMMARY" in body_report
    assert "RA-XS-BODY" not in body_report
    assert "RA-XS-MISSING" in body_report and "小结" in body_report


def test_extended_object_name_is_not_the_shorter_row(tmp_path: Path) -> None:
    claim = _claim().replace("方法甲", "方法甲乙")
    report = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", _table(), claim, claim))),
        _terms(tmp_path),
    )
    _assert_info(report)
    assert _stats(report)[0] == 0
    assert "RA-XS-BODY" not in report
    assert "RA-XS-SUMMARY" in report
    assert "92.3" not in report


def test_integer_under_percent_header_binds_without_rescaling(tmp_path: Path) -> None:
    table = _table(cell="92", header=r"合成指标（\%）")
    claim = _claim(value=r"92\%")
    bound = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, claim, claim)), "bound.tex"),
        _terms(tmp_path),
    )
    assert _stats(bound) == (1, 0, 0)
    fraction = _claim("0.92")
    unbound = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, fraction, claim)), "fraction.tex"),
        _terms(tmp_path),
    )
    _assert_info(unbound)
    assert "RA-XS-BODY" not in unbound
    assert "RA-XS-COVERAGE" in unbound
    assert "0.92" not in unbound


def test_unparsed_cell_is_not_reported_as_a_missing_row(tmp_path: Path) -> None:
    table = _table(extra_header="对照指标", extra_cell="待定")
    text = _doc(
        _chapter("性能结果", table, _claim(metric="对照指标", value=r"1.0\%"), "实验设置如下。")
    )
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    _assert_info(report)
    assert "RA-XS-COVERAGE" in report
    assert "RA-XS-SUMMARY" not in report
    assert "RA-XS-BODY" not in report
    assert _stats(report)[0] == 0


def test_summary_number_without_ref_stays_unbound(tmp_path: Path) -> None:
    summary = "方法甲在合成评价集上的合成指标为 92.3\\%。"
    text = _doc(_chapter("性能结果", _table(), _claim(r"92.1\%"), summary))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    _assert_info(report)
    assert "RA-XS-BODY" in report
    assert "RA-XS-MISSING" in report and "小结" in report
    assert "无表引用" in report
    assert "RA-XS-SUMMARY" not in report
    assert "92.1" not in report and "92.3" not in report


def test_checked_in_fixture_and_appended_eval() -> None:
    fixture = _SKILL / "evals" / "fixtures" / "cross-surface" / "main.tex"
    terms = _SKILL / "evals" / "fixtures" / "cross-surface" / "terms.json"
    report = _xs(fixture, terms)
    assert _stats(report) == (1, 0, 0)
    payload = json.loads((_SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))
    ids = [item["id"] for item in payload["evals"]]
    assert ids == sorted(ids)
    assert len(set(ids)) == len(ids)
    assert 56 in ids
    entry = next(item for item in payload["evals"] if item["id"] == 56)
    assert entry["files"] == [
        "evals/fixtures/cross-surface/main.tex",
        "evals/fixtures/cross-surface/terms.json",
    ]
    assert "--cross-surface" in entry["prompt"]
    assert "Meaning-Check: NEEDS-LLM" in entry["expected_output"]


def test_header_comment_with_ampersand_does_not_shift_columns(tmp_path: Path) -> None:
    terms = _terms(tmp_path)
    comment = "% 列：方法 & 对照指标\n"
    plain = _table()
    commented = plain.replace("方法 & 合成指标 \\\\", comment + "方法 & 合成指标 \\\\")
    assert comment in commented
    claim = _claim()
    with_comment = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", commented, claim, claim)), "c.tex"), terms
    )
    without = _xs(_write(tmp_path, _doc(_chapter("性能结果", plain, claim, claim)), "p.tex"), terms)
    _assert_info(with_comment)
    assert _stats(with_comment) == (1, 0, 0)
    assert "RA-XS-BODY" not in with_comment and "RA-XS-SUMMARY" not in with_comment
    assert with_comment.replace("c.tex", "x") == without.replace("p.tex", "x")

    other = _claim(metric="对照指标", value=r"1.0\%")
    missing = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", commented, other, other)), "m.tex"), terms
    )
    _assert_info(missing)
    assert "RA-XS-SUMMARY" in missing and "表中无此记录" in missing
    assert "RA-XS-BODY" not in missing
    assert _stats(missing)[0] == 0


def test_trailing_comment_after_row_keeps_next_row(tmp_path: Path) -> None:
    table = _table().replace(
        r"方法甲 & 92.3\% \\",
        r"方法甲 & 92.3\% \\ % 旧值 & 91.0\%" + "\n" + r"方法乙 & 88.5\% \\",
    )
    assert "% 旧值" in table
    claim = _claim(value=r"88.5\%", row="方法乙")
    report = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", table, claim, claim))), _terms(tmp_path)
    )
    _assert_info(report)
    assert _stats(report) == (1, 0, 0)
    assert "表中无此记录" not in report
    assert "91.0" not in report


def test_escaped_percent_in_cell_survives_comment_stripping(tmp_path: Path) -> None:
    claim = _claim()
    report = _xs(
        _write(tmp_path, _doc(_chapter("性能结果", _table(cell=r"92.3\% % 备注"), claim, claim))),
        _terms(tmp_path),
    )
    assert _stats(report) == (1, 0, 0)


@pytest.mark.parametrize("marker", ["约 ", "约为 ", "大约 ", "接近 ", "约"])
def test_spaced_approximate_marker_is_not_compared(tmp_path: Path, marker: str) -> None:
    claim = _claim(value=marker + r"92\%")
    text = _doc(_chapter("性能结果", _table(), claim, claim))
    report = _xs(_write(tmp_path, text), _terms(tmp_path))
    _assert_info(report)
    assert "RA-XS-BODY" not in report and "RA-XS-SUMMARY" not in report
    assert "RA-XS-COVERAGE" in report
    assert _stats(report)[0] == 0
    assert _stats(report)[2] == 0
