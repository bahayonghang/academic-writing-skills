"""Tests for scripts/rebuttal_build.py (rebuttal C2)."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

from tests.support.paths import SKILLS_ROOT

SCRIPTS = SKILLS_ROOT / "latex-thesis-zh" / "scripts"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
PLAN_FIELDS = (
    "id",
    "reviewer",
    "item",
    "quote",
    "status",
    "action",
    "plan",
    "owner",
    "shared_with",
)
MARKDOWN_LINE_RE = re.compile(r"^\s*(?:#+\s|>\s?|[-*+]\s|\d+[.)]\s)")
MARKDOWN_INLINE_RE = re.compile(r"\*\*|__|`")


def run_build(thesis_rebuttal_scripts, capsys, case, *extra: str) -> tuple[int, str, str]:
    args = ["--workspace", str(case.workspace), "--thesis", str(case.thesis), *extra]
    code = thesis_rebuttal_scripts.rebuttal_build.main(args)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def edit_ledger(case, change) -> None:
    path = case.workspace / "concerns.yaml"
    ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
    change(ledger)
    text = yaml.safe_dump(ledger, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(text, encoding="utf-8")


def tree_digest(root: Path, skip: str | None = None) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_file() and not (skip and rel.startswith(skip)):
            digest.update(rel.encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def test_help_lists_cli_options() -> None:
    expected = {
        "rebuttal_build.py": ("--workspace", "--thesis", "--plan-only", "--force", "--json"),
        "rebuttal_check.py": ("--workspace", "--thesis", "--json"),
    }
    for script, options in expected.items():
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / script), "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=ENV,
            check=True,
        )
        for option in options:
            assert option in result.stdout, (script, option)


def test_plan_only(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    def keep_plan_fields(ledger: dict) -> None:
        ledger["concerns"] = [
            {key: dict(concern, status="planned")[key] for key in PLAN_FIELDS}
            for concern in ledger["concerns"]
        ]

    edit_ledger(rebuttal_case, keep_plan_fields)
    code, out, err = run_build(
        thesis_rebuttal_scripts, capsys, rebuttal_case, "--plan-only", "--json"
    )
    assert code == 0, err
    assert json.loads(out)["plan_only"] is True
    assert list((rebuttal_case.root / "responses").iterdir()) == []
    assert not (rebuttal_case.workspace / "anchors.json").exists()
    plan = (rebuttal_case.workspace / "revision_plan.md").read_text(encoding="utf-8")
    assert "## 负责方：drawio" in plan
    rows = [line for line in plan.splitlines() if line.startswith("| R")]
    assert len(rows) == 7
    assert any(line.startswith("| R1-3a、R2-2 |") for line in rows)


def test_full_render_structure(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    code, out, _ = run_build(thesis_rebuttal_scripts, capsys, rebuttal_case, "--json")
    assert code == 0
    written = json.loads(out)["written"]
    responses = rebuttal_case.root / "responses"
    for name in ("review-result.md", "response-all.md", "response-R1.md", "response-R2.md"):
        assert f"responses/{name}" in written
        assert (responses / name).is_file()
    for name in ("anchors.json", "revision_plan.md"):
        assert (rebuttal_case.workspace / name).is_file()

    text = (responses / "response-all.md").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if line]
    assert lines[0] == "博士生修改说明"
    assert "2位评阅专家共提出5条意见，拆分为8项逐项处理" in lines[1]
    assert "修改已有内容3项、补充新内容2项、在回复中说明1项、列为后续工作1项、未采纳1项" in lines[1]
    assert lines[1].endswith("下文页码均指修改后论文。")
    assert lines[2] == "一、评阅人1意见的修改说明"
    assert "二、评阅人2意见的修改说明" in lines
    assert sum(re.match(r"意见\d+：", line) is not None for line in lines) == 5
    assert sum("回复：" in line for line in lines) == 8
    assert sum("修改位置：" in line for line in lines) == 8
    assert "（与评阅人2意见2一并修改）" in text
    result = (responses / "review-result.md").read_text(encoding="utf-8")
    assert result == "总体评价 1（A）；总体评价 2（B）\n"
    single = (responses / "response-R2.md").read_text(encoding="utf-8")
    assert single.startswith("评阅人2意见的修改说明\n\n意见1：")
    assert "总体说明" not in single


def test_location_renumber_and_page(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    assert run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)[0] == 0
    text = (rebuttal_case.root / "responses" / "response-all.md").read_text(encoding="utf-8")
    assert "（2）修改位置：原图2-1，现图2-2（第13页）" in text
    assert "修改位置：式(2-1)（第14页）" in text
    assert "修改位置：第2.3节（第14页）" in text
    assert "（3）修改位置：参考文献[3]" in text
    anchors = json.loads((rebuttal_case.workspace / "anchors.json").read_text(encoding="utf-8"))
    figure = next(a for a in anchors if a["label"] == "fig:c2-profile")
    assert (figure["number"], figure["page"], figure["status"]) == ("2-2", "13", "resolved")
    assert all(anchor["status"] == "resolved" for anchor in anchors)


def test_plain_text_equivalent(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    assert run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)[0] == 0
    for path in sorted((rebuttal_case.root / "responses").glob("*.md")):
        raw = path.read_text(encoding="utf-8").splitlines()
        rendered = [MARKDOWN_INLINE_RE.sub("", MARKDOWN_LINE_RE.sub("", line)) for line in raw]
        assert rendered == raw, path.name
        assert all(not line.endswith("  ") for line in raw)


def test_hand_edit_guard(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    assert run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)[0] == 0
    target = rebuttal_case.root / "responses" / "response-R1.md"
    target.write_text(target.read_text(encoding="utf-8") + "手改的一行\n", encoding="utf-8")
    code, _, err = run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)
    assert code == 4
    assert "responses/response-R1.md" in err
    assert "手改的一行" in target.read_text(encoding="utf-8")

    assert run_build(thesis_rebuttal_scripts, capsys, rebuttal_case, "--force")[0] == 0
    assert "手改的一行" not in target.read_text(encoding="utf-8")
    state = json.loads((rebuttal_case.workspace / "rebuttal_state.json").read_text("utf-8"))
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    assert state["rendered"]["responses/response-R1.md"] == digest


def test_invalid_ledger_exit_2(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    def break_ledger(ledger: dict) -> None:
        del ledger["schema"]
        ledger["concerns"][0]["action"] = "fix"

    edit_ledger(rebuttal_case, break_ledger)
    code, _, err = run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)
    assert code == 2
    assert "schema" in err
    assert "R1-1: action='fix'" in err
    assert not (rebuttal_case.root / "responses" / "response-all.md").exists()


def test_readonly(rebuttal_case, thesis_rebuttal_scripts, capsys) -> None:
    before = (tree_digest(rebuttal_case.thesis, "rebuttal/"), tree_digest(rebuttal_case.reviews))
    assert run_build(thesis_rebuttal_scripts, capsys, rebuttal_case)[0] == 0
    args = ["--workspace", str(rebuttal_case.workspace), "--thesis", str(rebuttal_case.thesis)]
    assert thesis_rebuttal_scripts.rebuttal_check.main(args) == 0
    capsys.readouterr()
    after = (tree_digest(rebuttal_case.thesis, "rebuttal/"), tree_digest(rebuttal_case.reviews))
    assert after == before
