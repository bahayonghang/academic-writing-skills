"""Tests for scripts/rebuttal_intake.py and scripts/rebuttal_common.py (rebuttal C1)."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.support.paths import SKILLS_ROOT

SCRIPT = SKILLS_ROOT / "latex-defense-zh" / "scripts" / "rebuttal_intake.py"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
CLI_OPTIONS = (
    "--reviews",
    "--thesis",
    "--main",
    "--root",
    "--stage",
    "--form-title",
    "--order",
    "--base-commit",
    "--force",
    "--json",
)
WATERMARK = "示例平台水印-——987654321"


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run(defense_scripts, capsys, *args: object) -> tuple[int, str, str]:
    code = defense_scripts.rebuttal_intake.main([str(arg) for arg in args])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def concerns_by_id(workspace: Path) -> dict[str, dict]:
    ledger = yaml.safe_load((workspace / "concerns.yaml").read_text(encoding="utf-8"))
    return {concern["id"]: concern for concern in ledger["concerns"]}


def test_help_lists_cli_options() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=ENV,
        check=True,
    )
    for option in CLI_OPTIONS:
        assert option in result.stdout


def test_txt_reviews_normalized(rebuttal_reviews: Path, defense_scripts, capsys) -> None:
    code, out, _ = run(defense_scripts, capsys, "--reviews", rebuttal_reviews, "--json")
    assert code == 0
    summary = json.loads(out)
    reviewers = {item["id"]: item for item in summary["reviewers"]}
    assert reviewers["R1"]["file"] == "评阅书1.txt"
    assert (reviewers["R1"]["grade"], reviewers["R1"]["total_score"]) == ("A", 88)
    assert (reviewers["R2"]["grade"], reviewers["R2"]["total_score"]) == ("B", 85)
    assert (reviewers["R1"]["items"], reviewers["R2"]["items"]) == (3, 2)
    assert summary["ledger_written"] is True

    workspace = rebuttal_reviews.parent / "workspace"
    first = (workspace / "reviews" / "R1.md").read_text(encoding="utf-8")
    second = (workspace / "reviews" / "R2.md").read_text(encoding="utf-8")
    for text in (first, second):
        assert "示例平台" not in text
        assert "第1页" not in text
        assert not any(line.strip() in {"1", "2"} for line in text.splitlines())
        assert "是否同意答辩：同意答辩" in text
    assert "1. 验证数据仅来自单一示例路网，跨路网迁移能力缺乏实证，建议补充讨论。" in first
    assert "3. 写作规范方面：" in first
    assert "1.5 倍数据规模" in second
    assert "\n3. " not in second

    concerns = concerns_by_id(workspace)
    assert list(concerns) == ["R1-1", "R1-2", "R1-3", "R2-1", "R2-2"]
    assert all(concern["status"] == "open" for concern in concerns.values())
    assert all(concern["source"] == "[Script]" for concern in concerns.values())


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    import pymupdf

    path.parent.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open()
    for lines in pages:
        page = document.new_page()
        for index, line in enumerate([WATERMARK, *lines]):
            page.insert_text((50, 60 + 20 * index), line, fontname="china-s", fontsize=11)
    document.save(path)
    document.close()


def test_pdf_review_normalized(tmp_path: Path, defense_scripts, capsys) -> None:
    pytest.importorskip("pymupdf")
    reviews = tmp_path / "pre-review" / "review_results"
    write_pdf(
        reviews / "评阅书1.pdf",
        [
            [
                "博士学术学位论文评阅书",
                "总分 90",
                "总体评价 A 优秀90-100",
                "是否同意答辩 同意答辩",
                "示例 第1页",
            ],
            [
                "对学位论文的学术评语",
                "论文选题合理，方法完整，实验数据充分。",
                "论文的不足之处和建议",
                "1、图2-1中的文字过于密集，",
                "建议重绘。",
                "示例 第2页",
            ],
            ["2、第3章的实验设置说明不完整，建议补充参数取值与数据来源。", "示例 第3页"],
        ],
    )
    code, out, _ = run(defense_scripts, capsys, "--reviews", reviews, "--json")
    assert code == 0
    reviewer = json.loads(out)["reviewers"][0]
    assert (reviewer["grade"], reviewer["total_score"], reviewer["items"]) == ("A", 90, 2)
    text = (tmp_path / "pre-review" / "workspace" / "reviews" / "R1.md").read_text("utf-8")
    assert WATERMARK not in text
    assert "第2页" not in text
    assert "1. 图2-1中的文字过于密集，建议重绘。" in text
    assert "2. 第3章的实验设置说明不完整" in text


def test_anchor_detection(defense_scripts) -> None:
    text = (
        "图2-7与表3.1，式(2-1)、公式（3-2），算法5-1；第3章至第5章，第六章，"
        "2.3节与4.1.2节，文献[24]、文献[1,2]、文献[5-7]，1.5 倍"
    )
    anchors = [
        (anchor.kind, anchor.key) for anchor in defense_scripts.rebuttal_common.find_anchors(text)
    ]
    assert anchors == [
        ("figure", "2-7"),
        ("table", "3-1"),
        ("equation", "2-1"),
        ("equation", "3-2"),
        ("algorithm", "5-1"),
        ("chapter", "3"),
        ("chapter", "4"),
        ("chapter", "5"),
        ("chapter", "6"),
        ("section", "2.3"),
        ("section", "4.1.2"),
        ("reference", "24"),
        ("reference", "1"),
        ("reference", "2"),
        ("reference", "5"),
        ("reference", "6"),
        ("reference", "7"),
    ]


def test_anchor_mapping_with_thesis(
    rebuttal_reviews: Path, rebuttal_thesis: Path, defense_scripts, capsys
) -> None:
    args = ("--reviews", rebuttal_reviews, "--thesis", rebuttal_thesis)
    code, _, _ = run(defense_scripts, capsys, *args)
    assert code == 0
    concerns = concerns_by_id(rebuttal_reviews.parent / "workspace")

    def anchors(concern_id: str) -> dict[str, dict]:
        return {
            anchor["text"] + anchor["base_number"]: anchor
            for anchor in concerns[concern_id]["anchors"]
        }

    figure = anchors("R1-3")["图2-12-1"]
    assert (figure["kind"], figure["label"], figure["base_page"]) == (
        "figure",
        "fig:c2-profile",
        12,
    )
    assert anchors("R1-3")["文献[3]3"]["label"] == "wang2019survey"
    equation = anchors("R1-2")["式(2-1)2-1"]
    assert (equation["label"], equation["base_page"]) == ("eq:c2-target", 13)
    assert anchors("R1-2")["第2章2"]["label"] == "chap:c2"
    assert anchors("R2-2")["2.3节2.3"]["label"] == "sec:c2-3"
    references = anchors("R2-2")
    assert references["文献[1,2]1"]["label"] == "zhang2020flow"
    assert references["文献[1,2]2"]["label"] == "li2021graph"


def test_directory_layout_and_readonly(
    rebuttal_reviews: Path, rebuttal_thesis: Path, defense_scripts, capsys
) -> None:
    before = (tree_digest(rebuttal_reviews), tree_digest(rebuttal_thesis))
    names = sorted(path.name for path in rebuttal_reviews.iterdir())
    args = ("--reviews", rebuttal_reviews, "--thesis", rebuttal_thesis)
    code, _, _ = run(defense_scripts, capsys, *args)
    assert code == 0
    assert (tree_digest(rebuttal_reviews), tree_digest(rebuttal_thesis)) == before
    assert sorted(path.name for path in rebuttal_reviews.iterdir()) == names

    root = rebuttal_reviews.parent
    assert (root / "responses").is_dir()
    workspace = root / "workspace"
    assert {path.name for path in workspace.iterdir()} == {
        "reviews",
        "concerns.yaml",
        "rebuttal_state.json",
    }
    state = json.loads((workspace / "rebuttal_state.json").read_text(encoding="utf-8"))
    assert state["schema"] == "rebuttal-state/1"
    assert state["reviews_dir"] == "review_results"
    assert state["form_title"] == "博士学位论文预评审评阅意见修改审查表"
    assert [review["id"] for review in state["reviews"]] == ["R1", "R2"]
    assert state["reviews"][0]["pages"] == 2


def test_exit_codes(
    rebuttal_reviews: Path, tmp_path: Path, defense_scripts, capsys, monkeypatch
) -> None:
    assert run(defense_scripts, capsys, "--reviews", tmp_path / "missing")[0] == 2
    assert (
        run(defense_scripts, capsys, "--reviews", rebuttal_reviews, "--root", rebuttal_reviews)[0]
        == 2
    )

    blocked = tmp_path / "blocked"
    shutil.copytree(rebuttal_reviews, blocked)
    (blocked / "评阅书3.docx").write_bytes(b"PK")
    code, _, err = run(defense_scripts, capsys, "--reviews", blocked)
    assert code == 2
    assert "请导出为 PDF 或 TXT" in err

    with_pdf = tmp_path / "with-pdf"
    shutil.copytree(rebuttal_reviews, with_pdf)
    (with_pdf / "评阅书3.pdf").write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(defense_scripts.rebuttal_intake, "_PYMUPDF_AVAILABLE", False)
    assert run(defense_scripts, capsys, "--reviews", with_pdf)[0] == 3
    monkeypatch.undo()

    assert run(defense_scripts, capsys, "--reviews", rebuttal_reviews)[0] == 0
    code, _, err = run(defense_scripts, capsys, "--reviews", rebuttal_reviews)
    assert code == 4
    assert "--force" in err


def test_same_name_pdf_and_md_count_once(
    rebuttal_reviews: Path, defense_scripts, capsys, monkeypatch
) -> None:
    for name in ("评阅书1", "评阅书2"):
        txt = rebuttal_reviews / f"{name}.txt"
        txt.rename(txt.with_suffix(".md"))
        (rebuttal_reviews / f"{name}.pdf").write_bytes(b"%PDF-1.4\n")
    monkeypatch.setattr(defense_scripts.rebuttal_intake, "_PYMUPDF_AVAILABLE", False)
    code, out, _ = run(defense_scripts, capsys, "--reviews", rebuttal_reviews, "--json")
    assert code == 0
    summary = json.loads(out)
    assert [item["file"] for item in summary["reviewers"]] == ["评阅书1.md", "评阅书2.md"]
    skipped = [w["message"] for w in summary["warnings"] if w["code"] == "W-SKIP-FILE"]
    assert len(skipped) == 2
    assert any("评阅书1.pdf" in message and "评阅书1.md" in message for message in skipped)


def test_markdown_headings_split_sections(rebuttal_reviews: Path, defense_scripts, capsys) -> None:
    for txt in rebuttal_reviews.glob("*.txt"):
        text = txt.read_text(encoding="utf-8")
        for heading in ("对学位论文的学术评语", "论文的不足之处和建议"):
            text = text.replace(heading, f"## {heading}")
        txt.with_suffix(".md").write_text(text, encoding="utf-8")
        txt.unlink()
    code, out, _ = run(defense_scripts, capsys, "--reviews", rebuttal_reviews, "--json")
    assert code == 0
    summary = json.loads(out)
    assert [item["items"] for item in summary["reviewers"]] == [3, 2]
    assert "W-NO-SECTION" not in {w["code"] for w in summary["warnings"]}


def test_force_keeps_ledger(rebuttal_reviews: Path, defense_scripts, capsys) -> None:
    assert run(defense_scripts, capsys, "--reviews", rebuttal_reviews)[0] == 0
    workspace = rebuttal_reviews.parent / "workspace"
    ledger = workspace / "concerns.yaml"
    edited = ledger.read_text(encoding="utf-8").replace("status: open", "status: done", 1)
    ledger.write_text(edited, encoding="utf-8", newline="\n")
    ledger_bytes = ledger.read_bytes()
    (workspace / "reviews" / "R1.md").write_text("旧内容\n", encoding="utf-8")
    (workspace / "reviews" / "R9.md").write_text("旧内容\n", encoding="utf-8")

    code, out, _ = run(defense_scripts, capsys, "--reviews", rebuttal_reviews, "--force", "--json")
    assert code == 0
    assert json.loads(out)["ledger_written"] is False
    assert ledger.read_bytes() == ledger_bytes
    assert "旧内容" not in (workspace / "reviews" / "R1.md").read_text(encoding="utf-8")
    assert not (workspace / "reviews" / "R9.md").exists()


def test_without_thesis(rebuttal_reviews: Path, defense_scripts, capsys) -> None:
    assert run(defense_scripts, capsys, "--reviews", rebuttal_reviews)[0] == 0
    workspace = rebuttal_reviews.parent / "workspace"
    anchors = [
        anchor for concern in concerns_by_id(workspace).values() for anchor in concern["anchors"]
    ]
    assert anchors
    assert all(anchor["label"] is None and anchor["base_page"] is None for anchor in anchors)
    state = json.loads((workspace / "rebuttal_state.json").read_text(encoding="utf-8"))
    assert state["thesis"] == {"given": False, "main": None, "base_commit": None, "aux_labels": 0}


def test_base_commit_recorded(
    rebuttal_reviews: Path, rebuttal_thesis: Path, defense_scripts, capsys
) -> None:
    git = shutil.which("git")
    if git is None:
        pytest.skip("git is not installed")
    identity = ("-c", "user.name=test", "-c", "user.email=test@example.invalid")
    for args in (("init", "-q"), ("add", "-A"), (*identity, "commit", "-q", "-m", "base")):
        subprocess.run([git, "-C", str(rebuttal_thesis), *args], check=True, capture_output=True)
    head = subprocess.run(
        [git, "-C", str(rebuttal_thesis), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    args = ("--reviews", rebuttal_reviews, "--thesis", rebuttal_thesis, "--main", "document.tex")
    assert run(defense_scripts, capsys, *args)[0] == 0
    state_path = rebuttal_reviews.parent / "workspace" / "rebuttal_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["thesis"]["base_commit"] == head
    assert state["thesis"]["main"] == "document.tex"

    assert run(defense_scripts, capsys, *args, "--force", "--base-commit", "abc1234")[0] == 0
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["thesis"]["base_commit"] == "abc1234"
