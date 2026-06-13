"""Regression coverage for typst-paper scripts that were previously untested.

These tests lock the behavioral fixes from the typst-reality audit (T1-T40) and
run the scripts as subprocesses so they exercise the real CLI without polluting
``sys.path`` (the canonical EN/AUDIT ``parsers`` must not be shadowed).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from conftest import SCRIPT_DIR_TYPST

FIXTURES = SCRIPT_DIR_TYPST.parent / "evals" / "fixtures"
CHARGED_IEEE = FIXTURES / "charged_ieee_fixture.typ"
BARE = FIXTURES / "bare_fixture.typ"


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT_DIR_TYPST / script), *args],
        capture_output=True,
        text=True,
        check=False,
    )


# ── check_references (T1, T25) ────────────────────────────────────


def test_check_references_no_false_undefined_for_citations(tmp_path: Path) -> None:
    """A normal paper (2 cites + 1 @fig:arch) raises no Critical undefined refs (T1)."""
    main = tmp_path / "main.typ"
    main.write_text(
        '#bibliography("refs.bib")\n'
        "= Introduction\n"
        "Prior work @smith2020 and @jones2019 motivate this. See @fig:arch.\n"
        "#figure(\n  image('a.png'),\n  caption: [Arch],\n) <fig:arch>\n",
        encoding="utf-8",
    )
    (tmp_path / "refs.bib").write_text(
        "@article{smith2020, title={A}, author={S}, journal={J}, year={2020}}\n"
        "@article{jones2019, title={B}, author={J}, journal={J}, year={2019}}\n",
        encoding="utf-8",
    )
    result = _run("check_references.py", str(main))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Undefined reference" not in result.stdout
    assert "Undefined citation" not in result.stdout


def test_check_references_flags_unknown_citation_when_bib_known(tmp_path: Path) -> None:
    main = tmp_path / "main.typ"
    main.write_text(
        '#bibliography("refs.bib")\n= Intro\nTypo cite @smith2099 here.\n',
        encoding="utf-8",
    )
    (tmp_path / "refs.bib").write_text(
        "@article{smith2020, title={A}, author={S}, journal={J}, year={2020}}\n",
        encoding="utf-8",
    )
    result = _run("check_references.py", str(main))
    assert result.returncode == 1
    assert "smith2099" in result.stdout


def test_check_references_colon_caption_string_form(tmp_path: Path) -> None:
    """`caption: "..."` string form is not a false 'missing caption' (T25)."""
    main = tmp_path / "main.typ"
    main.write_text(
        '#figure(\n  image("a.png"),\n  caption: "A string caption",\n) <fig:x>\nSee @fig:x.\n',
        encoding="utf-8",
    )
    result = _run("check_references.py", str(main))
    assert "Missing caption" not in result.stdout


# ── verify_bib (T4, T5) ──────────────────────────────────────────


def test_verify_bib_hayagriva_no_false_missing_fields(tmp_path: Path) -> None:
    yml = tmp_path / "refs.yml"
    yml.write_text(
        "harry-potter:\n  type: book\n  title: A Book\n  author: Rowling, J. K.\n  date: 2003\n",
        encoding="utf-8",
    )
    result = _run("verify_bib.py", str(yml))
    assert "missing required fields" not in (result.stdout + result.stderr)


def test_verify_bib_hyphen_key_not_misreported(tmp_path: Path) -> None:
    """A hyphenated key cited in the .typ is neither 'not found' nor 'unused' (T5)."""
    bib = tmp_path / "refs.bib"
    bib.write_text(
        "@article{harry-potter, title={A}, author={R}, journal={J}, year={2003}}\n",
        encoding="utf-8",
    )
    typ = tmp_path / "main.typ"
    typ.write_text("= Intro\nAs shown in @harry-potter, ...\n", encoding="utf-8")
    result = _run("verify_bib.py", str(bib), "--typ", str(typ))
    out = result.stdout + result.stderr
    assert "harry" not in out.replace("harry-potter", "")  # no truncated 'harry'
    assert "unused entries" not in out


# ── generate_table (T17) ─────────────────────────────────────────


def test_generate_table_plain_style_differs_from_booktabs(tmp_path: Path) -> None:
    csv = tmp_path / "data.csv"
    csv.write_text("Method,Acc\nA,90\nB,91\n", encoding="utf-8")
    booktabs = _run("generate_table.py", str(csv), "--style", "booktabs", "--json")
    plain = _run("generate_table.py", str(csv), "--style", "plain", "--json")
    assert booktabs.returncode == 0 and plain.returncode == 0
    assert "table.hline" in booktabs.stdout
    assert "stroke: 0.5pt" in plain.stdout
    assert booktabs.stdout != plain.stdout


# ── deai_check (T19, T20, T23) ───────────────────────────────────


def test_deai_unknown_section_errors(tmp_path: Path) -> None:
    typ = tmp_path / "m.typ"
    typ.write_text("= Introduction\nSome text here.\n", encoding="utf-8")
    result = _run("deai_check.py", str(typ), "--section", "does-not-exist")
    assert result.returncode == 1
    assert "Section not found" in (result.stdout + result.stderr)


def test_deai_two_chinese_emdashes_not_flagged(tmp_path: Path) -> None:
    typ = tmp_path / "m.typ"
    typ.write_text("= 引言\n这是一段话——包含破折号。另一段——也在这里。\n", encoding="utf-8")
    result = _run("deai_check.py", str(typ), "--analyze")
    assert "em_dash_overuse" not in (result.stdout + result.stderr)


def test_deai_runs_without_pyyaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """deai_check must run on defaults when PyYAML is unavailable (T23)."""
    typ = tmp_path / "m.typ"
    typ.write_text("= Introduction\nThis is a sentence with some content here.\n", encoding="utf-8")
    # Block `import yaml` in the child process.
    code = (
        "import sys; sys.modules['yaml'] = None;"
        f"sys.argv = ['deai_check.py', r'{typ}', '--analyze'];"
        f"sys.path.insert(0, r'{SCRIPT_DIR_TYPST}');"
        "exec(open(r'%s').read())" % (SCRIPT_DIR_TYPST / "deai_check.py")
    )
    result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True)
    # Should not crash with ImportError on yaml.
    assert "ModuleNotFoundError" not in result.stderr
    assert "No module named 'yaml'" not in result.stderr


# ── optimize_title (T22) ─────────────────────────────────────────


def test_optimize_title_word_boundary_no_false_ineffective(tmp_path: Path) -> None:
    typ = tmp_path / "m.typ"
    typ.write_text(
        '#set document(title: "Renewable Energy Forecasting for Housing Markets")\n= Intro\nx\n',
        encoding="utf-8",
    )
    result = _run("optimize_title.py", str(typ), "--check")
    out = result.stdout + result.stderr
    # "new" inside Renewable and "using" inside Housing must not be flagged.
    assert "ineffective" not in out.lower()


# ── analyze_experiment (T2, T38) ─────────────────────────────────


def test_analyze_experiment_flags_ungrounded_numbers(tmp_path: Path) -> None:
    typ = tmp_path / "m.typ"
    typ.write_text(
        "= Experiment\nWe report 95.2% accuracy.\nThe model reaches 3.1 BLEU.\n"
        "Training took 12 hours.\n",
        encoding="utf-8",
    )
    result = _run("analyze_experiment.py", str(typ), "--section", "experiment")
    assert "without attribution" in result.stdout


def test_analyze_experiment_missing_file_errors() -> None:
    result = _run("analyze_experiment.py", "does_not_exist.typ")
    assert result.returncode == 1
    assert "File not found" in (result.stdout + result.stderr)


# ── check_format (T8) ────────────────────────────────────────────


def test_check_format_template_no_false_twocolumn_critical() -> None:
    result = _run("check_format.py", str(CHARGED_IEEE), "--venue", "ieee")
    out = result.stdout + result.stderr
    assert "managed by the template" in out
    # The template-managed paper must not raise the two-column Critical issue.
    assert "IEEE requires two-column format" not in out


# ── fixtures are runnable end-to-end (routing smoke) ─────────────


@pytest.mark.parametrize("fixture", [CHARGED_IEEE, BARE])
def test_fixtures_parse_clean_in_check_references(fixture: Path) -> None:
    result = _run("check_references.py", str(fixture))
    # Both fixtures have valid labels + bib, so no Critical undefined refs.
    assert "Undefined reference" not in result.stdout
    assert "Undefined citation" not in result.stdout
