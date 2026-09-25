"""Tests for scripts/extract_thesis.py on the synthetic mini-thesis fixture."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-defense-zh"
SCRIPT = SKILL_ROOT / "scripts" / "extract_thesis.py"
FIXTURE_DIR = SKILL_ROOT / "evals" / "fixtures" / "mini-thesis"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *args],
        capture_output=True,
        encoding="utf-8",
        env=ENV,
        check=False,
    )


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def by_label(items: list[dict]) -> dict[str, dict]:
    return {item["label"]: item for item in items}


def test_chapter_roles_and_section_kinds(inventory: dict) -> None:
    roles = [chapter["role_suggestion"] for chapter in inventory["chapters"]]
    assert roles == [
        "intro",
        "foundation",
        "research",
        "research",
        "research",
        "application",
        "conclusion",
    ]
    chapter3 = inventory["chapters"][2]
    assert [section["kind"] for section in chapter3["sections"]] == [
        "intro",
        "problem",
        "method",
        "experiment",
        "summary",
    ]
    assert [sub["number"] for sub in chapter3["sections"][3]["subsections"]] == [
        "3.4.1",
        "3.4.2",
        "3.4.3",
    ]
    assert chapter3["source"] == "chapters/chapter3.tex:1"


def test_numbers_prefer_aux_and_fall_back_to_computed(inventory: dict) -> None:
    figures = by_label(inventory["figures"])
    assert (figures["fig:c3-network"]["number"], figures["fig:c3-network"]["number_source"]) == (
        "3-3",
        "aux",
    )
    for label, number in (
        ("fig:c1-organization", "1-3"),
        ("fig:c4-results", "4-3"),
        ("fig:c6-interface", "6-2"),
    ):
        assert figures[label]["number"] == number
        assert figures[label]["number_source"] == "computed"
    tables = by_label(inventory["tables"])
    assert tables["tab:c3-metrics"]["number"] == "3-2"
    assert tables["tab:c4-ablation"]["number_source"] == "computed"
    assert tables["tab:c4-ablation"]["tabular_source"].startswith("\\begin{tabular}{lc}")
    assert tables["tab:c4-ablation"]["tabular_source"].endswith("\\end{tabular}")
    equations = by_label(inventory["equations"])
    assert equations["eq:c4-hidden"]["labels"] == [
        {"label": "eq:c4-hidden", "number": "4-1", "number_source": "computed"},
        {"label": "eq:c4-output", "number": "4-2", "number_source": "computed"},
    ]
    assert equations["eq:c3-loss"]["number_source"] == "aux"
    assert equations["eq:c3-loss"]["tex"].count("\\label{eq:c3-loss}") == 1
    algorithm = inventory["algorithms"][0]
    assert (algorithm["label"], algorithm["number"], algorithm["subsection"]) == (
        "alg:c5-update",
        "5-1",
        "5.3.2",
    )


def test_subfigures_have_letters_and_captions(inventory: dict) -> None:
    figure = by_label(inventory["figures"])["fig:c3-compare"]
    assert figure["caption"] == "示例补全结果对比"
    assert [sub["letter"] for sub in figure["subfigures"]] == ["a", "b", "c"]
    assert [sub["caption"] for sub in figure["subfigures"]] == [
        "方法 A 补全结果",
        "方法 B 补全结果",
        "本章方法补全结果",
    ]
    assert figure["subfigures"][0]["label"] == "fig:c3-compare-a"
    assert figure["subfigures"][0]["number"] == "3-4(a)"
    assert figure["subfigures"][2]["file"] == "chapter3/compare-c.png"
    assert [item["resolved"] for item in figure["files"]] == [
        "fig/chapter3/compare-a.png",
        "fig/chapter3/compare-b.png",
        "fig/chapter3/compare-c.png",
    ]


def test_figure_with_chinese_file_name_resolves(inventory: dict) -> None:
    figure = by_label(inventory["figures"])["fig:c5-online"]
    assert figure["files"] == [
        {
            "path": "chapter5/在线结果/在线预测结果.png",
            "resolved": "fig/chapter5/在线结果/在线预测结果.png",
            "exists": True,
        }
    ]


def test_publications_map_to_chapters(inventory: dict) -> None:
    publications = inventory["publications"]
    assert [item["id"] for item in publications] == ["P1", "P2", "P3", "P4"]
    assert [item["chapters"] for item in publications] == [[3], [3, 4], [5], []]
    assert publications[3]["category"] == "2. 申请的发明专利"
    assert all("对应" not in item["text"] for item in publications)
    assert publications[1]["text"].endswith("11-20.")


def test_conclusion_items(inventory: dict) -> None:
    conclusion = inventory["conclusion"]
    assert conclusion["chapter"] == 7
    assert len(conclusion["contributions"]) == 3
    assert conclusion["contributions"][0].startswith("针对观测稀疏")
    assert conclusion["outlook"] == [
        "将方法推广到更多类型的交通检测数据。",
        "研究模型更新过程中的计算开销。",
    ]


def test_meta_logo_macros_and_warnings(inventory: dict) -> None:
    assert inventory["main_tex"] == "document.tex"
    assert inventory["degree"] == "doctor"
    meta = inventory["meta"]
    assert meta["title_lines"] == ["面向稀疏观测的城市交通", "流量预测方法研究"]
    assert (meta["supervisor"], meta["supervisor_title"]) == ("示例导师", "教授")
    assert meta["title_en"].startswith("Research on")
    assert inventory["logo"] == "fig/logo.png"
    assert inventory["graphicspath"] == ["fig/"]
    macros = {macro["name"]: macro for macro in inventory["macros"]}
    assert set(macros) == {"ysuctitlelines", "vect", "argmin", "Loss", "unusedmacro"}
    assert macros["argmin"]["command"] == "DeclareMathOperator*"
    assert macros["Loss"]["definition"] == "\\def\\Loss{\\mathcal{L}}"
    codes = [warning["code"] for warning in inventory["warnings"]]
    assert codes == ["W-MAIN"]


def test_blind_main_reports_missing_fields(mini_thesis: Path, defense_scripts) -> None:
    data = defense_scripts.extract_thesis.extract_inventory(mini_thesis, "document_blind.tex")
    codes = [warning["code"] for warning in data["warnings"]]
    assert codes.count("W-META") == 2
    assert "W-PUB" in codes
    assert data["publications"] == []


def test_missing_images_are_reported(tmp_path: Path, defense_scripts) -> None:
    root = tmp_path / "mini-thesis"
    shutil.copytree(FIXTURE_DIR, root)
    data = defense_scripts.extract_thesis.extract_inventory(root)
    files = [item for figure in data["figures"] for item in figure["files"]]
    codes = [warning["code"] for warning in data["warnings"]]
    assert files and not any(item["exists"] for item in files)
    assert codes.count("W-FIG-FILE") == len(files)
    assert "W-LOGO" in codes
    assert data["logo"] is None


def test_extraction_keeps_fixture_files_unchanged(tmp_path: Path) -> None:
    before = tree_hashes(FIXTURE_DIR)
    root = tmp_path / "mini-thesis"
    shutil.copytree(FIXTURE_DIR, root)
    assert tree_hashes(root) == before
    result = run_cli("--thesis", str(root), "--out", str(tmp_path / "out" / "inventory.json"))
    assert result.returncode == 0, result.stderr
    assert tree_hashes(root) == before
    assert tree_hashes(FIXTURE_DIR) == before


def test_cli_json_summary(tmp_path: Path) -> None:
    out = tmp_path / "inventory.json"
    result = run_cli("--thesis", str(FIXTURE_DIR), "--out", str(out), "--json")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["counts"]["chapters"] == 7
    assert summary["counts"]["contributions"] == 3
    assert json.loads(out.read_text(encoding="utf-8"))["main_tex"] == "document.tex"


def test_cli_exits_2_for_ambiguous_or_missing_main(tmp_path: Path) -> None:
    root = tmp_path / "mini-thesis"
    shutil.copytree(FIXTURE_DIR, root)
    shutil.copy(root / "document.tex", root / "document-print.tex")
    out = str(tmp_path / "inventory.json")
    ambiguous = run_cli("--thesis", str(root), "--out", out)
    assert ambiguous.returncode == 2
    assert "--main" in ambiguous.stderr
    chosen = run_cli("--thesis", str(root), "--main", "document-print.tex", "--out", out)
    assert chosen.returncode == 0, chosen.stderr
    empty = tmp_path / "empty"
    empty.mkdir()
    assert run_cli("--thesis", str(empty), "--out", out).returncode == 2
    assert run_cli("--thesis", str(root), "--main", "none.tex", "--out", out).returncode == 2


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("（对应论文第三、四章）", [3, 4]),
        ("（对应论文第5章）", [5]),
        ("对应第3-5章", [3, 4, 5]),
        ("对应本文第三章和第五章", [3, 5]),
        ("（对应论文第十二章）", [12]),
        ("（对应论文第二十一章）", [21]),
        ("无对应标注", []),
    ],
)
def test_parse_chapter_marks(defense_scripts, text: str, expected: list[int]) -> None:
    assert defense_scripts.extract_thesis.parse_chapter_marks(text) == expected


def test_read_group_and_split_rows(defense_scripts) -> None:
    extract = defense_scripts.extract_thesis
    assert extract.read_group("{a\\{b\\}{c}} tail", 0) == ("a\\{b\\}{c}", 11)
    body = "a &= b \\\\ c &= \\begin{cases} x \\\\ y \\end{cases} \\\\ d_{\\{1\\\\2\\}}"
    assert len(extract.split_rows(body)) == 3
    with pytest.raises(ValueError):
        extract.read_group("{open", 0)
