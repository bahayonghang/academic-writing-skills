"""Unit tests for scripts/typst_backend.py (no Typst needed)."""

from __future__ import annotations

from pathlib import Path

import pytest

SIMPLE_TABLE = (
    "\\begin{tabular}{lcc}\n  \\toprule\n  方法 & RMSE & MAE\\\\\n  \\midrule\n"
    "  方法 A\\cite{demo-a} & 0.52 & 0.41\\\\\n"
    "  本章（图~\\ref{fig:x}） & \\textbf{0.39} & $x^{2}$\\\\\n  \\bottomrule\n\\end{tabular}"
)


@pytest.fixture
def backend(defense_scripts):
    return defense_scripts.typst_backend


def test_string_literals_escape_only_backslash_and_quote(backend) -> None:
    assert backend.ty_str('a "b" \\ c\n  d') == '"a \\"b\\" \\\\ c d"'
    assert backend.ty_str("# $ ] // *_@<`=") == '"# $ ] // *_@<`="'
    assert backend.ty_str(None) == '""'


def test_emphasis_splits_into_hl_calls(backend) -> None:
    assert backend.ty_text("提升 **50%** 精度") == '[#"提升 "#hl("50%")#" 精度"]'
    assert backend.ty_text("**关键**") == '[#hl("关键")]'
    assert backend.ty_text("要点 **a** 与 **b", "strong") == '[#"要点 "#strong("a")#" 与 **b"]'
    assert backend.ty_text("无强调") == '"无强调"'


def test_raw_block_fence_outgrows_backticks(backend) -> None:
    assert backend.raw_block("a") == "```\na\n```"
    assert backend.raw_block("x ```` y").startswith("`````\n")


def test_default_nav_label(backend) -> None:
    assert backend.default_nav_label(1, "绪论") == ("绪论", False)
    assert backend.default_nav_label(7, "总结与展望") == ("总结与展望", False)
    assert backend.default_nav_label(3, "基于时空图卷积的流量补全方法研究") == ("第3章", True)


def test_latex_inline_converts_caption_source(backend) -> None:
    numbers = {"fig:x": "3-3", "eq:y": "3-5"}
    pieces, missing = backend.latex_inline(
        "见图~\\ref{fig:x}与式\\eqref{eq:y}\\cite[p.~2]{k} \\textbf{粗} $a_1$ 50\\% \\foo", numbers
    )
    assert missing == ["\\foo"]
    assert pieces == [
        ("str", "见图\u00a03-3与式(3-5) "),
        ("strong", "粗"),
        ("str", " "),
        ("math", "a_1"),
        ("str", " 50% \\foo"),
    ]
    markup = backend.render_pieces(pieces, macros=True)
    assert '#strong("粗")' in markup
    assert "#mi(thesis-macros + ```\na_1\n```.text)" in markup
    assert backend.latex_inline("\\ref{none}", numbers)[0] == [("str", "??")]


def test_simple_table_grid(backend) -> None:
    numbers = {"fig:x": "3-3"}
    rows = backend.tabular_rows(SIMPLE_TABLE)
    assert rows[0] == ["方法", "RMSE", "MAE"]
    assert len(rows) == 3
    assert backend.table_plain(SIMPLE_TABLE, numbers) == [
        "方法",
        "RMSE",
        "MAE",
        "方法 A",
        "0.52",
        "0.41",
        "本章（图\u00a03-3）",
        "0.39",
        "x^{2}",
    ]


@pytest.mark.parametrize(
    "body",
    [
        "\\begin{tabular}{cc}\\multirow{2}{*}{a} & b\\\\\\end{tabular}",
        "\\begin{tabular}{cc}\\multicolumn{2}{c}{a}\\\\\\end{tabular}",
        "\\begin{tabular}{cc}\\makecell{a} & b\\\\\\end{tabular}",
        "\\begin{tabular}{c}\\begin{tabular}{c}a\\end{tabular}\\\\\\end{tabular}",
        "\\begin{longtable}{cc}a & b\\\\\\end{longtable}",
        "\\begin{tabular}{cc}\\unknowncmd{a} & b\\\\\\end{tabular}",
    ],
    ids=["multirow", "multicolumn", "makecell", "nested", "longtable", "unknown-command"],
)
def test_complex_tables_are_rejected(backend, body: str) -> None:
    with pytest.raises(backend.TypstBackendError):
        backend.table_grid(body, {})
    assert backend.table_plain(body, {}) is None


def test_macro_translation(backend) -> None:
    translate = backend.translate_macro
    assert translate(
        {"name": "Loss", "command": "def", "definition": "\\def\\Loss{\\mathcal{L}}"}
    ) == ("\\newcommand{\\Loss}{\\mathcal{L}}")
    star = {
        "name": "argmin",
        "command": "DeclareMathOperator*",
        "definition": "\\DeclareMathOperator*{\\argmin}{arg\\,min}",
    }
    assert translate(star) == "\\newcommand{\\argmin}{\\operatorname*{arg\\,min}}"
    plain = {
        "name": "tr",
        "command": "DeclareMathOperator",
        "definition": "\\DeclareMathOperator{\\tr}{tr}",
    }
    assert translate(plain) == "\\newcommand{\\tr}{\\operatorname{tr}}"
    renew = {"name": "v", "command": "renewcommand", "definition": "\\renewcommand{\\v}[1]{#1}"}
    assert translate(renew) == "\\newcommand{\\v}[1]{#1}"
    with pytest.raises(backend.TypstBackendError):
        translate({"name": "p", "command": "def", "definition": "\\def\\p#1{#1}"})


def test_equation_body_drops_labels_only(backend) -> None:
    equation = {"tex": "\n  a = b \\label{eq:a}\n"}
    assert backend.equation_body(equation) == "  a = b "


@pytest.mark.parametrize(
    ("resolved", "ok"),
    [
        ("fig/a.png", True),
        ("fig/a.PDF", True),
        ("fig/a.svg", True),
        ("fig/a.eps", False),
        ("fig/a.gif", False),
        ("../outside/a.png", False),
    ],
)
def test_image_problem(backend, resolved: str, ok: bool) -> None:
    assert (backend.image_problem(resolved) is None) is ok
    assert backend.image_target("fig/a.png") == "img/fig/a.png"


def test_stage_labels(backend) -> None:
    assert backend.stage_labels("predefense", "doctor") == ("博士学位论文预答辩", "Pre-defense")
    assert backend.stage_labels("defense", "master") == ("硕士学位论文答辩", "Defense")
    assert backend.stage_labels("defense", "unknown") == ("学位论文答辩", "Defense")


def make_package(root: Path, namespace: str, name: str, version: str) -> None:
    directory = root / namespace / name / version
    directory.mkdir(parents=True)
    (directory / "typst.toml").write_text("[package]\n", encoding="utf-8")


def test_find_package_honors_paths_and_env(backend, tmp_path: Path) -> None:
    assert backend.parse_spec("@preview/mitex:0.2.6") == ("preview", "mitex", "0.2.6")
    assert backend.parse_spec("mitex") is None
    local, cache = tmp_path / "local", tmp_path / "cache"
    make_package(local, "local", "simply-ysu-touying", "0.2.0")
    make_package(cache, "preview", "mitex", "0.2.6")
    env = {"TYPST_PACKAGE_CACHE_PATH": str(cache)}
    assert backend.find_package("@local/simply-ysu-touying:0.2.0", str(local), env) is not None
    assert backend.find_package("@preview/mitex:0.2.6", str(local), env) is not None
    assert backend.find_package("@local/mitex:0.2.6", str(local), env) is None
    env_path = {"TYPST_PACKAGE_PATH": str(local), "TYPST_PACKAGE_CACHE_PATH": str(tmp_path / "x")}
    assert backend.find_package("@local/simply-ysu-touying:0.2.0", None, env_path) is not None
    assert backend.missing_packages(
        ["@preview/mitex:0.2.6", "@preview/touying:0.8.0"], str(local), env
    ) == ["@preview/touying:0.8.0"]


def test_compile_needs_typst_and_version(backend, tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(backend.shutil, "which", lambda name: None)
    assert backend.compile_deck(tmp_path, theme_package=backend.DEFAULT_THEME_PACKAGE) == 5
    assert "未找到 typst" in capsys.readouterr().err
    monkeypatch.setattr(backend.shutil, "which", lambda name: "typst")
    monkeypatch.setattr(backend, "typst_version", lambda executable: (0, 14, 2))
    assert backend.compile_deck(tmp_path, theme_package=backend.DEFAULT_THEME_PACKAGE) == 5
    assert "0.14.2" in capsys.readouterr().err


def test_compile_with_missing_package_exits_6_without_compiling(
    backend, tmp_path: Path, monkeypatch, capsys
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr(backend.shutil, "which", lambda name: "typst")
    monkeypatch.setattr(backend, "typst_version", lambda executable: (0, 15, 1))
    monkeypatch.setattr(backend.subprocess, "run", lambda command, **kw: calls.append(command))
    monkeypatch.setenv("TYPST_PACKAGE_CACHE_PATH", str(tmp_path / "empty-cache"))
    empty = tmp_path / "empty-packages"
    empty.mkdir()
    code = backend.compile_deck(
        tmp_path, theme_package=backend.DEFAULT_THEME_PACKAGE, package_path=str(empty)
    )
    assert code == 6
    assert calls == []
    err = capsys.readouterr().err
    assert "@preview/simply-ysu-touying:0.2.0" in err and "references/touying-backend.md" in err
