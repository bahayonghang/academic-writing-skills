"""Opt-in college source checks for numbers, equations, captions, and tables."""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH

COLLEGE = "yanshan-ee-2025"
_BASELINES = REPO_ROOT / "tests/fixtures/thesis-zh-baselines"
BASELINE = _BASELINES / "number-equation-table"
C1_STYLE = _BASELINES / "term-governance"
FIXTURE = (
    REPO_ROOT / "academic-writing-skills/latex-thesis-zh/evals/fixtures/thesis-project/main.tex"
)
_SHARED = ("parsers", "tex_loader")


def _load(name: str):
    path = SCRIPT_DIR_ZH / f"{name}.py"
    saved_path = list(sys.path)
    saved = {item: sys.modules.pop(item, None) for item in _SHARED}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(f"zh_net_{name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for item, mod in saved.items():
            if mod is None:
                sys.modules.pop(item, None)
            else:
                sys.modules[item] = mod


check_style_zh = _load("check_style_zh")
check_format = _load("check_format")
check_tables = _load("check_tables")
check_references = _load("check_references")


def test_loader_guard_resolves_zh_college_entrypoints():
    assert check_style_zh.ChineseStyleChecker.__module__.startswith("zh_net_")
    assert hasattr(check_format.FormatChecker, "_college_equation_issues")
    assert hasattr(check_tables.TableChecker, "_check_college_table")
    assert hasattr(check_references.ReferenceChecker, "check_college_figure_captions")


def _write(tmp_path: Path, body: str, name: str = "main.tex") -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


def _wrap(body: str) -> str:
    return "\\documentclass{ctexbook}\n\\begin{document}\n" + body + "\n\\end{document}\n"


def _style(tmp_path: Path, body: str, **kwargs):
    tex = _write(tmp_path, _wrap(body))
    checker = check_style_zh.ChineseStyleChecker(tex, **kwargs)
    return checker.analyze().findings


def _style_codes(tmp_path: Path, body: str, **kwargs) -> list[str]:
    return [item.code for item in _style(tmp_path, body, **kwargs)]


def _format_issues(tmp_path: Path, body: str, school: str = COLLEGE) -> list[dict]:
    tex = _write(tmp_path, _wrap(body))
    result = check_format.FormatChecker(str(tex), school=school).check()
    return [item for item in result["issues"] if str(item.get("code", "")).startswith("EQ-")]


def _format_codes(tmp_path: Path, body: str, school: str = COLLEGE) -> set[str]:
    return {item["code"] for item in _format_issues(tmp_path, body, school)}


def _table_issues(tmp_path: Path, body: str, school: str = COLLEGE) -> list[dict]:
    tex = _write(tmp_path, _wrap(body))
    result = check_tables.TableChecker(str(tex), school=school).check()
    return [item for item in result["issues"] if item.get("code")]


def _table_codes(tmp_path: Path, body: str, school: str = COLLEGE) -> set[str]:
    return {item["code"] for item in _table_issues(tmp_path, body, school)}


def _ref_issues(tmp_path: Path, body: str, school: str = COLLEGE) -> list[dict]:
    tex = _write(tmp_path, _wrap(body))
    checker = check_references.ThesisReferenceChecker(str(tex), school=school)
    return [item for item in checker.run_all() if item.get("code")]


def _ref_codes(tmp_path: Path, body: str, school: str = COLLEGE) -> set[str]:
    return {item["code"] for item in _ref_issues(tmp_path, body, school)}


def _cli(script: str, tex: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(SCRIPT_DIR_ZH / script), str(tex), *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


def test_invalid_school_is_nonzero_and_not_a_pass(tmp_path: Path):
    tex = _write(tmp_path, _wrap("温升达到50\\%。\n"))
    for script in (
        "check_style_zh.py",
        "check_format.py",
        "check_tables.py",
        "check_references.py",
    ):
        for choice in ("yanshan", "no-such-school"):
            result = _cli(script, tex, "--school", choice)
            assert result.returncode != 0, script
            assert "PASS" not in result.stdout
            assert "未发现规则级表达问题" not in result.stdout


def _portable_cli_bytes(data: bytes) -> bytes:
    """Ignore checkout-only bytes in Windows-captured CLI snapshots.

    Ubuntu CI emits LF, prints a different ``File:`` path, and has no chktex.
    Every other byte still has to match.
    """
    text = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    text = re.sub(rb"(?m)^File: .+$", b"File: <TEX>", text)
    return re.sub(rb"(?m)^ChkTeX: .+$", b"ChkTeX: <CHKTEX>", text)


def test_omitted_school_matches_generic_and_default_baseline():
    commands = (
        ("style-default", "check_style_zh.py", []),
        ("format-default", "check_format.py", []),
        ("format-strict", "check_format.py", ["--strict"]),
        ("tables-default", "check_tables.py", []),
        ("tables-fix", "check_tables.py", ["--fix-suggestions"]),
        ("references-default", "check_references.py", []),
    )
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, script, extra in commands:
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(SCRIPT_DIR_ZH / script), str(FIXTURE), *extra],
            capture_output=True,
            env=env,
            check=False,
        )
        assert _portable_cli_bytes(completed.stdout) == _portable_cli_bytes(
            (BASELINE / f"{name}.stdout").read_bytes()
        ), name
        assert _portable_cli_bytes(completed.stderr) == _portable_cli_bytes(
            (BASELINE / f"{name}.stderr").read_bytes()
        ), name
        assert completed.returncode == int((BASELINE / f"{name}.exit").read_text(encoding="ascii"))
    captured = (BASELINE / "format-default.stdout").read_bytes()
    linux_like = captured.replace(b"\r\n", b"\n")
    linux_like = re.sub(rb"(?m)^File: .+$", b"File: /tmp/checkout/main.tex", linux_like)
    linux_like = linux_like.replace(b"ChkTeX: Available", b"ChkTeX: Not Available")
    assert _portable_cli_bytes(linux_like) == _portable_cli_bytes(captured)
    drifted = captured.replace(b"Status: WARNING", b"Status: PASS", 1)
    assert _portable_cli_bytes(drifted) != _portable_cli_bytes(captured)

    for suffix in ("stdout", "stderr", "exit"):
        assert (BASELINE / f"style-default.{suffix}").read_bytes() == (
            C1_STYLE / f"style-default.{suffix}"
        ).read_bytes()
    diff = subprocess.run(
        ["git", "diff", "--", "academic-writing-skills/latex-thesis-zh/templates"],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    assert diff.stdout == b""


def test_degree_wording_and_school_do_not_swallow_each_other(tmp_path: Path):
    body = "极易达到50\\%。"
    degree = _style_codes(tmp_path, body, degree_wording=True)
    school = _style_codes(tmp_path, body, school=COLLEGE)
    both = _style(tmp_path, body, degree_wording=True, school=COLLEGE)
    codes = [item.code for item in both]
    assert "E-DEGREE" in degree and "NUM-SPACE" not in degree
    assert "NUM-SPACE" in school and "E-DEGREE" not in school
    assert codes.count("E-DEGREE") == 1
    assert codes.count("NUM-SPACE") == 1
    space = next(item for item in both if item.code == "NUM-SPACE")
    degree_hit = next(item for item in both if item.code == "E-DEGREE")
    assert space.original == "50\\%"
    assert degree_hit.original == "极易"
    assert space.suggestion == ""
    assert "极易达到" not in space.candidate


@pytest.mark.parametrize(
    ("body", "present", "absent"),
    (
        ("温升达到50\\%。", "NUM-SPACE", None),
        ("温升达到25℃。", "NUM-SPACE", None),
        ("温升达到50~\\%。", None, "NUM-SPACE"),
        ("温升达到25~℃。", None, "NUM-SPACE"),
        ("温升达到50 \\%。", None, "NUM-SPACE"),
        ("温升达到50\\,\\%。", None, "NUM-SPACE"),
        ("平面角为30°。", None, "NUM-SPACE"),
        ("平面角为30′且另一处为30″。", None, "NUM-SPACE"),
        ("表头单位为降幅/\\%。", None, "NUM-SPACE"),
        ("结果提高了5个百分点。", None, "NUM-SPACE"),
        ("分组写成1004.1。", "NUM-GROUP", None),
        ("分组写成0.1746。", "NUM-GROUP", None),
        ("错分组写成0.17\\,46。", "NUM-GROUP", None),
        ("分组写成1\\,004.1。", None, "NUM-GROUP"),
        ("分组写成0.174\\,6。", None, "NUM-GROUP"),
        ("年份写成2026年。", None, "NUM-GROUP"),
        ("型号写成RTX4090。", None, "NUM-GROUP"),
        ("标识写成doi:10.1109/EXAMPLE。", None, "NUM-GROUP"),
        ("裸数字1004出现在句中。", "NUM-COVERAGE", "NUM-GROUP"),
    ),
)
def test_college_number_candidates(
    tmp_path: Path, body: str, present: str | None, absent: str | None
):
    codes = _style_codes(tmp_path, body, school=COLLEGE)
    if present:
        assert present in codes
    if absent:
        assert absent not in codes
    generic = _style_codes(tmp_path, body, school="generic")
    assert "NUM-SPACE" not in generic
    assert "NUM-GROUP" not in generic
    assert "NUM-COVERAGE" not in generic


def test_math_percent_is_located_without_rewriting_and_angle_stays(tmp_path: Path):
    findings = _style(tmp_path, "温升为$50\\%$，角度为$30^\\circ$。", school=COLLEGE)
    space = [item for item in findings if item.code == "NUM-SPACE"]
    assert len(space) == 1
    assert space[0].original == "50\\%"
    assert space[0].suggestion == ""
    assert space[0].severity == "Info"
    assert space[0].priority == "P3"
    assert "不改写数学" in space[0].candidate
    assert "30" not in space[0].original
    report = check_style_zh.generate_report(
        check_style_zh.ChineseStyleChecker(
            _write(tmp_path, _wrap("温升为$50\\%$。")),
            school=COLLEGE,
        ).analyze()
    )
    assert "[Script]" in report
    assert "Meaning-Check: NEEDS-LLM" in report
    assert "PRESERVED" not in report


def test_celsius_degree_form_is_not_an_angle_exemption(tmp_path: Path):
    flagged = _style_codes(tmp_path, "温度为$25^\\circ\\mathrm{C}$。", school=COLLEGE)
    clean = _style_codes(tmp_path, "温度为$25~^\\circ\\mathrm{C}$。", school=COLLEGE)
    assert "NUM-SPACE" in flagged
    assert "NUM-SPACE" not in clean


def test_unclassified_bare_number_is_not_an_exemption(tmp_path: Path):
    findings = list(_style(tmp_path, "编号外的1004需要人工看。", school=COLLEGE))
    coverage = [item for item in findings if item.code == "NUM-COVERAGE"]
    assert coverage
    assert coverage[0].original == "1004"
    assert "不是确定违规" in coverage[0].candidate
    assert "不构成学院豁免" in coverage[0].candidate
    assert "NUM-GROUP" not in [item.code for item in findings]
    assert "NUM-COVERAGE" not in _style_codes(tmp_path, "学号20210001不分组。", school=COLLEGE)


def test_simple_tabular_cells_carry_number_candidates(tmp_path: Path):
    body = (
        "\\begin{tabular}{cc}\n"
        "\\toprule\n"
        "方法 & 误差/\\% \\\\\n"
        "\\midrule\n"
        "甲 & 50\\% \\\\\n"
        "乙 & 1004.1 \\\\\n"
        "丙 & 1\\,004.1 \\\\\n"
        "丁 & 1004 \\\\\n"
        "戊 & 降幅/\\% \\\\\n"
        "己 & 5个百分点 \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
    )
    findings = _style(tmp_path, body, school=COLLEGE)
    space = [item for item in findings if item.code == "NUM-SPACE"]
    groups = [item.original for item in findings if item.code == "NUM-GROUP"]
    assert len(space) == 1
    assert space[0].original == "50\\%"
    assert space[0].suggestion == ""
    assert space[0].severity == "Info"
    assert space[0].priority == "P3"
    assert "1004.1" in groups
    assert "1004" in groups
    assert "1\\,004.1" not in groups
    assert "NUM-SPACE" not in _style_codes(tmp_path, body, school="generic")
    one_row = "\\begin{tabular}{c}\n50\\%\n\\end{tabular}\n"
    assert "NUM-SPACE" in _style_codes(tmp_path, one_row, school=COLLEGE)
    sized = "\\begin{tabular}{p{12.3456cm}}\n50\\%\n\\end{tabular}\n"
    sized_codes = _style_codes(tmp_path, sized, school=COLLEGE)
    assert "NUM-SPACE" in sized_codes
    assert "NUM-GROUP" not in sized_codes
    math = _style(tmp_path, "\\begin{tabular}{c}\n$50\\%$\n\\end{tabular}\n", school=COLLEGE)
    math_space = next(item for item in math if item.code == "NUM-SPACE")
    assert math_space.suggestion == ""
    assert "不改写数学" in math_space.candidate


def test_non_simple_tables_are_coverage_not_cell_hits(tmp_path: Path):
    cases = {
        "longtable": "\\begin{longtable}{c}\n50\\% \\\\\n1004.1 \\\\\n\\end{longtable}\n",
        "sidewaystable": (
            "\\begin{sidewaystable}\n\\begin{tabular}{c}\n50\\%\n\\end{tabular}\n"
            "\\end{sidewaystable}\n"
        ),
        "multicolumn": (
            "\\begin{tabular}{cc}\n\\multicolumn{2}{c}{50\\%} \\\\\n1 & 2 \\\\\n\\end{tabular}\n"
        ),
        "nested": (
            "\\begin{tabular}{c}\n\\begin{tabular}{c}\n50\\%\n\\end{tabular}\n\\end{tabular}\n"
        ),
    }
    for name, body in cases.items():
        findings = _style(tmp_path, body, school=COLLEGE)
        codes = [item.code for item in findings]
        assert codes.count("NUM-COVERAGE") == 1, name
        assert "NUM-SPACE" not in codes, name
        assert "NUM-GROUP" not in codes, name
        note = next(item for item in findings if item.code == "NUM-COVERAGE")
        assert note.severity == "Info"
        assert note.priority == "P3"
        assert note.suggestion == ""
        assert "不作为通过" in note.candidate
    assert "NUM-COVERAGE" not in _style_codes(tmp_path, cases["longtable"], school="generic")


def test_yishang_shizi_is_not_an_equation_cite(tmp_path: Path):
    assert "EQ-CITE" not in _format_codes(tmp_path, "以上式子表明结果。\n")
    assert "EQ-CITE" in _format_codes(tmp_path, "以上式表明结果。\n")
    assert "EQ-CITE" in _format_codes(tmp_path, "由上式可得结果。\n")


def test_tikz_path_and_include_location(tmp_path: Path):
    tikz = _style_codes(
        tmp_path,
        "\\begin{tikzpicture}\n\\draw (0.1746, 0) -- (1, 0);\n\\end{tikzpicture}\n",
        school=COLLEGE,
    )
    assert "NUM-GROUP" not in tikz
    assert "NUM-GROUP" not in _style_codes(tmp_path, "见路径 fig/1004.png 即可。", school=COLLEGE)
    chapter = tmp_path / "body.tex"
    chapter.write_text("温升达到50\\%。\n", encoding="utf-8")
    main = _write(
        tmp_path, "\\documentclass{ctexbook}\n\\begin{document}\n\\input{body}\n\\end{document}\n"
    )
    findings = check_style_zh.ChineseStyleChecker(main, school=COLLEGE).analyze().findings
    assert any(item.code == "NUM-SPACE" and "body.tex:" in item.loc for item in findings)


def test_equation_rules_have_independent_examples(tmp_path: Path):
    assert "EQ-CONT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\nA &= B + C \\\\\n&= D\n\\end{align}\n",
    )
    assert "EQ-CONT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\nA = B + C = \\\\\nD\n\\end{equation}\n",
    )
    assert "EQ-CONT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{cases}\n"
        "a, & x > 0 \\\\\nb, & x < 0\n\\end{cases}\n\\end{equation}\n",
    )
    assert "EQ-CONT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\nx &= 1 \\\\\ny &= 2\n\\end{align}\n",
    )
    assert "EQ-CONT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\na &= b \\\\\n&= c \\quad \\text{s.t. } x>0\n\\end{align}\n",
    )
    changed = _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\na &= b \\\\\n&\\le c\n\\end{align}\n",
    )
    assert "EQ-CONT" not in changed
    assert "EQ-COVERAGE" in changed

    assert "EQ-LEADIN" in _format_codes(
        tmp_path,
        "关系如下。\n% 注释：\n\\label{eq:a}\n\\begin{equation}\na=b\n\\end{equation}\n",
    )
    assert "EQ-LEADIN" not in _format_codes(
        tmp_path,
        "关系如下：\n% 注释\n\\label{eq:a}\n\\begin{equation}\na=b\n\\end{equation}\n",
    )
    same_line = _format_codes(tmp_path, "关系如下：\\begin{equation}\na=b\n\\end{equation}\n")
    assert "EQ-LEADIN" not in same_line
    assert "EQ-COVERAGE" in same_line
    assert "EQ-LEADIN" not in _format_codes(
        tmp_path,
        "关系如下。\n\\begin{equation*}\na=b\n\\end{equation*}\n",
    )

    assert "EQ-TAILPUNCT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation} a = b。 \\end{equation}\n",
    )
    assert "EQ-TAILPUNCT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\na = b\n\\end{equation}\n",
    )
    assert "EQ-TAILPUNCT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{cases}\n"
        "a, & x > 0 \\\\\nb, & x < 0\n\\end{cases}\n\\end{equation}\n",
    )
    assert "EQ-TAILPUNCT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{cases}\n"
        "a, & x > 0 \\\\\nb, & x < 0\n\\end{cases}。\n\\end{equation}\n",
    )

    assert "EQ-CITE" in _format_codes(tmp_path, "由上式可得结果。\n")
    assert "EQ-CITE" not in _format_codes(tmp_path, "见式~\\eqref{eq:a}可知。\n% 见上式\n")

    assert "EQ-NOTE" in _format_codes(tmp_path, "式中：$x$——输入。\n")
    assert "EQ-NOTE" not in _format_codes(tmp_path, "式中  $x$——输入。\n")
    assert "EQ-NOTE" in _format_codes(tmp_path, "其中 $x$为输入。\n")
    assert "EQ-NOTE" not in _format_codes(tmp_path, "其中$x$为输入。\n")
    assert "EQ-NOTE" not in _format_codes(tmp_path, "% 其中 $x$——输入。\n正文不解释。\n")

    issues = _format_issues(
        tmp_path,
        "关系如下：\n\\begin{align}\nA &= B + C \\\\\n&= D\n\\end{align}\n",
    )
    hit = next(item for item in issues if item["code"] == "EQ-CONT")
    assert hit["severity"] == "info"
    assert hit["priority"] == "P3"
    assert hit["meaning_check"] == "NEEDS-LLM"
    assert "[Script]" in hit["message"]
    assert "PRESERVED" not in hit["message"]
    assert hit["matched"] != "A &= B + C \\\\\n&= D"


def test_unbalanced_equation_is_incomplete_coverage(tmp_path: Path):
    codes = _format_codes(tmp_path, "关系如下：\n\\begin{equation}\na=b\n")
    assert "EQ-COVERAGE" in codes
    issues = _format_issues(tmp_path, "关系如下：\n\\begin{equation}\na=b\n")
    assert any("不作为通过" in item["message"] for item in issues if item["code"] == "EQ-COVERAGE")


def test_nested_and_complex_equations_keep_continuation_boundaries(tmp_path: Path):
    array = (
        "关系如下：\n\\begin{equation}\n\\begin{array}{cc}\n"
        "a & = b \\\\\n& = c\n\\end{array}\n\\end{equation}\n"
    )
    assert "EQ-CONT" not in _format_codes(tmp_path, array)
    assert "EQ-COVERAGE" in _format_codes(tmp_path, array)
    tex = _write(tmp_path, _wrap(array))
    assert check_format.FormatChecker(str(tex), school=COLLEGE).check()["status"] != "PASS"

    assert "EQ-CONT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\nA &= B + C \\\\\n&= D \\\\\n"
        "\\begin{split}\nx &= 1\n\\end{split}\n\\end{align}\n",
    )
    assert "EQ-CONT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\nA + B &= C \\\\\n&= D\n\\end{align}\n",
    )
    operator = _format_issues(
        tmp_path,
        "关系如下：\n\\begin{equation}\nA = B + C \\\\\n+ D\n\\end{equation}\n",
    )
    assert any(item["code"] == "EQ-CONT" and item["matched"].strip() == "+" for item in operator)
    assert "EQ-LEADIN" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\na &= b\n\\end{align}\n\\begin{equation}\nc = d\n\\end{equation}\n",
    )
    assert "EQ-TAILPUNCT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{align}\na &= b。 \\\\\n\\end{align}\n",
    )
    assert "EQ-TAILPUNCT" in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{split}\na &= b。\n\\end{split}\n\\end{equation}\n",
    )
    assert "EQ-CITE" not in _format_codes(tmp_path, "\\label{eq:上式}\n正文不指代。\n")
    assert "EQ-CITE" not in _format_codes(tmp_path, "\\newcommand{\\foo}{见上式}\n正文。\n")
    cited = [
        item
        for item in _format_issues(tmp_path, "由上式可得。\n\\label{eq:上式}\n")
        if item["code"] == "EQ-CITE"
    ]
    assert len(cited) == 1
    assert cited[0]["matched"] == "上式"


def test_split_continuation_is_owned_by_format_not_visible_text(tmp_path: Path):
    codes = _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{split}\nA &= B + C \\\\\n&= D\n"
        "\\end{split}\n\\end{equation}\n",
    )
    assert "EQ-CONT" in codes
    assert "EQ-CONT" not in _format_codes(
        tmp_path,
        "关系如下：\n\\begin{equation}\n\\begin{split}\nA &= B + C \\\\\n&= D\n"
        "\\end{split}\n\\end{equation}\n",
        school="generic",
    )


def test_table_and_figure_caption_ownership(tmp_path: Path):
    table = """
\\begin{table}
\\caption{中文表题。}
\\begin{tabular}{cc}
\\toprule
方法 & 误差 \\\\
\\midrule
甲 & 1.2\\% \\\\
乙 & 1.3\\% \\\\
丙 & 1.4\\% \\\\
\\bottomrule
\\end{tabular}
\\end{table}
\\begin{figure}
\\caption{中文图题。}
\\end{figure}
"""
    assert "CAP-PUNCT" in _table_codes(tmp_path, table)
    assert "TB-UNITHEAD" in _table_codes(tmp_path, table)
    figure_only = _ref_codes(tmp_path, table)
    assert "CAP-PUNCT" in figure_only
    table_lines = {
        item["line"] for item in _table_issues(tmp_path, table) if item["code"] == "CAP-PUNCT"
    }
    figure_lines = {
        item["line"] for item in _ref_issues(tmp_path, table) if item["code"] == "CAP-PUNCT"
    }
    assert table_lines.isdisjoint(figure_lines)

    clean_table = table.replace("中文表题。", "中文表题").replace("误差", "误差/\\%")
    assert "CAP-PUNCT" not in _table_codes(tmp_path, clean_table)
    assert "TB-UNITHEAD" not in _table_codes(tmp_path, clean_table)
    assert "CAP-PUNCT" not in _ref_codes(
        tmp_path, "\\begin{figure}\n\\caption{中文图题}\n\\end{figure}\n"
    )
    assert "CAP-PUNCT" not in _ref_codes(
        tmp_path, "\\begin{figure}\n\\caption{中文图题.}\n\\end{figure}\n"
    )
    assert "CAP-PUNCT" not in _ref_codes(
        tmp_path,
        "\\begin{figure}\n\\bicaption{中文图题}{English Title.}\n\\end{figure}\n",
    )
    assert "CAP-PUNCT" not in _table_codes(
        tmp_path,
        "\\begin{table}\n\\caption[短题。]{中文表题}\n\\begin{tabular}{c}\n\\toprule\n甲 \\\\\n"
        "\\midrule\n1 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n",
    )
    assert "CAP-PUNCT" not in _ref_codes(
        tmp_path,
        "\\begin{figure}\n\\caption{含$a.$与\\cite{k.}的题}\n\\end{figure}\n",
    )


def test_sameas_excludes_caption_and_notes_and_unclear_columns_are_not_merged(tmp_path: Path):
    body_hit = """
\\begin{table}
\\caption{表题不含重复词}
\\begin{tabular}{cc}
\\toprule
甲 & 乙 \\\\
\\midrule
A & 同上 \\\\
B & 1 \\\\
\\bottomrule
\\end{tabular}
\\end{table}
"""
    assert "TB-SAMEAS" in _table_codes(tmp_path, body_hit)
    assert "TB-SAMEAS" not in _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{同上仅在题注}
\\begin{tabular}{cc}
\\toprule
甲 & 乙 \\\\
\\midrule
A & 1 \\\\
B & 2 \\\\
\\bottomrule
\\end{tabular}
\\begin{tablenotes}
\\item 同左
\\end{tablenotes}
\\end{table}
""",
    )
    unclear = _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{cc}
\\toprule
\\multicolumn{2}{c}{合并} \\\\
\\midrule
1.0\\% & 2 \\\\
1.1\\% & 2 \\\\
1.2\\% & 2 \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )
    assert "TB-UNITHEAD" not in unclear
    assert "TB-COVERAGE" in unclear
    assert "TB-UNITHEAD" not in _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{c}
\\toprule
误差 \\\\
\\midrule
— \\\\
— \\\\
— \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )
    only_two = _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{cc}
\\toprule
方法 & 误差 \\\\
\\midrule
甲 & 1.2\\% \\\\
乙 & 1.3\\% \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )
    assert "TB-UNITHEAD" not in only_two
    assert "TB-UNITHEAD" in _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{c}
\\toprule
method \\\\
\\midrule
1.2m \\\\
1.3m \\\\
1.4m \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )
    assert "TB-UNITHEAD" in _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{c}
\\toprule
误差/mm \\\\
\\midrule
1.2m \\\\
1.3m \\\\
1.4m \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )
    assert "TB-UNITHEAD" not in _table_codes(
        tmp_path,
        """
\\begin{table}
\\caption{表题}
\\begin{tabular}{c}
\\toprule
长度/m \\\\
\\midrule
1.2m \\\\
1.3m \\\\
1.4m \\\\
\\bottomrule
\\end{tabular}
\\end{table}
""",
    )


def test_starred_caption_uses_the_chinese_argument_line(tmp_path: Path):
    body = (
        "\\begin{table}\n\\centering\n\\caption*{中文表题。}\n"
        "\\begin{tabular}{c}\n\\toprule\n甲 \\\\\n\\midrule\n1 \\\\\n"
        "\\bottomrule\n\\end{tabular}\n\\end{table}\n"
    )
    issues = _table_issues(tmp_path, body)
    punct = [item for item in issues if item["code"] == "CAP-PUNCT"]
    assert len(punct) == 1
    assert "\\caption*" in _wrap(body).splitlines()[punct[0]["line"] - 1]
    assert "CAP-COVERAGE" not in {item["code"] for item in issues}
    clean = body.replace("中文表题。", "中文表题")
    clean_codes = _table_codes(tmp_path, clean)
    assert "CAP-PUNCT" not in clean_codes
    assert "CAP-COVERAGE" not in clean_codes
    assert "CAP-PUNCT" in _ref_codes(
        tmp_path, "\\begin{figure}\n\\caption*{中文图题。}\n\\end{figure}\n"
    )
    figure_clean = _ref_codes(tmp_path, "\\begin{figure}\n\\caption*{中文图题}\n\\end{figure}\n")
    assert "CAP-PUNCT" not in figure_clean
    assert "CAP-COVERAGE" not in figure_clean


def test_college_candidates_are_absent_without_the_flag(tmp_path: Path):
    body = "由上式可得50\\%。\n\\begin{equation}\na=b。\n\\end{equation}\n"
    assert not _format_codes(tmp_path, body, school="generic")
    assert _format_codes(tmp_path, body, school=COLLEGE)
    table = (
        "\\begin{table}\n\\caption{中文表题。}\n\\begin{tabular}{c}\n"
        "\\toprule\n甲 \\\\\n\\midrule\n同上 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n"
    )
    assert not _table_codes(tmp_path, table, school="generic")
    assert _table_codes(tmp_path, table, school=COLLEGE)
    figure = "\\begin{figure}\n\\caption{中文图题。}\n\\end{figure}\n"
    assert not _ref_codes(tmp_path, figure, school="generic")
    assert "CAP-PUNCT" in _ref_codes(tmp_path, figure, school=COLLEGE)


def test_layout_lengths_and_dotted_identifiers_are_not_group_hits(tmp_path: Path):
    layout = (
        "\\resizebox{12.3456cm}{!}{甲}\\scalebox{0.1234}{乙}\n"
        "\\begin{minipage}[t]{0.4567\\textwidth}丙\\end{minipage}\n"
        "\\rule{1.2345cm}{0.4pt}\\hspace{1.2345cm}\\vspace{12.3456pt}\n"
        "版本 v1.2.1004 与 V2.0.1746 是标识。\n"
    )
    codes = _style_codes(tmp_path, layout, school=COLLEGE)
    assert "NUM-GROUP" not in codes
    assert "NUM-GROUP" in _style_codes(tmp_path, "分组写成1004.1。", school=COLLEGE)


def test_bare_mathrm_c_is_not_celsius(tmp_path: Path):
    assert "NUM-SPACE" not in _style_codes(tmp_path, "取$5\\mathrm{C}$为常数。", school=COLLEGE)
    for form in ("25℃", "25°C", "$25\\celsius$", "$25^{\\circ}\\mathrm{C}$"):
        assert "NUM-SPACE" in _style_codes(tmp_path, f"温度为{form}。", school=COLLEGE), form


def test_unscanned_table_floats_get_one_coverage_note(tmp_path: Path):
    cases = {
        "longtable": "\\begin{longtable}{c}\n\\caption{中文表题。}\\\\\n同上 \\\\\n\\end{longtable}\n",
        "sidewaystable": (
            "\\begin{sidewaystable}\n\\caption{中文表题。}\n\\begin{tabular}{c}\n同上 \\\\\n"
            "\\end{tabular}\n\\end{sidewaystable}\n"
        ),
        "tabularx": (
            "\\begin{table}\n\\caption{中文表题。}\n\\begin{tabularx}{\\textwidth}{X}\n同上 \\\\\n"
            "\\end{tabularx}\n\\end{table}\n"
        ),
        "多个 tabular": (
            "\\begin{table}\n\\caption{中文表题。}\n\\begin{tabular}{c}\n同上 \\\\\n\\end{tabular}\n"
            "\\begin{tabular}{c}\n同左 \\\\\n\\end{tabular}\n\\end{table}\n"
        ),
    }
    for name, body in cases.items():
        issues = _table_issues(tmp_path, body, school=COLLEGE)
        notes = [item for item in issues if item["code"] == "TB-COVERAGE"]
        assert len(notes) == 1, name
        assert name in notes[0]["message"]
        assert "不作为通过" in notes[0]["message"]
        assert notes[0]["level"] == "INFO"
        assert notes[0]["priority"] == "P3"
        assert not any(item["code"] in {"TB-SAMEAS", "CAP-PUNCT"} for item in issues), name
        assert "TB-COVERAGE" not in _table_codes(tmp_path, body, school="generic"), name
