"""Tests for scripts/rebuttal_check.py (rebuttal C2): one negative case per R-* code."""

from __future__ import annotations

import json
import os
import time

import yaml

SKIPPED_WITHOUT_THESIS = {"R-COMMIT(git)", "R-LOC(aux)", "R-PAGE-STALE", "R-RENUM", "R-NUM-SRC"}


def edit_ledger(case, change) -> None:
    path = case.workspace / "concerns.yaml"
    ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
    change({concern["id"]: concern for concern in ledger["concerns"]}, ledger)
    text = yaml.safe_dump(ledger, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(text, encoding="utf-8")


def build(defense_scripts, capsys, case) -> None:
    args = ["--workspace", str(case.workspace), "--thesis", str(case.thesis), "--force"]
    assert defense_scripts.rebuttal_build.main(args) == 0
    capsys.readouterr()


def check(defense_scripts, capsys, case, thesis: bool = True) -> tuple[int, dict]:
    args = ["--workspace", str(case.workspace), "--json"]
    if thesis:
        args += ["--thesis", str(case.thesis)]
    code = defense_scripts.rebuttal_check.main(args)
    return code, json.loads(capsys.readouterr().out)


def found(payload: dict, code: str) -> list[tuple[str, str]]:
    return [(f["severity"], f["concern"]) for f in payload["findings"] if f["code"] == code]


def run_case(defense_scripts, capsys, case, change=None) -> tuple[int, dict]:
    if change is not None:
        edit_ledger(case, change)
    build(defense_scripts, capsys, case)
    return check(defense_scripts, capsys, case)


def test_clean_case_passes(rebuttal_case, defense_scripts, capsys) -> None:
    code, payload = run_case(defense_scripts, capsys, rebuttal_case)
    assert code == 0
    assert payload["summary"]["Critical"] == 0
    assert payload["summary"]["Major"] == 0
    assert payload["skipped"] == []


def test_r_cover_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def drop(concerns: dict, ledger: dict) -> None:
        ledger["concerns"] = [c for c in ledger["concerns"] if c["id"] != "R2-2"]

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, drop)
    assert code == 1
    assert ("Critical", "R2-2") in found(payload, "R-COVER")


def test_r_status_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def plan(concerns: dict, ledger: dict) -> None:
        concerns["R1-1"]["status"] = "planned"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, plan)
    assert code == 1
    assert found(payload, "R-STATUS") == [("Major", "R1-1")]


def test_r_quote_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def misquote(concerns: dict, ledger: dict) -> None:
        concerns["R1-3b"]["quote"] = "图2-1文字很密集"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, misquote)
    assert code == 1
    assert found(payload, "R-QUOTE") == [("Major", "R1-3b")]


def test_r_commit_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def unchanged_file(concerns: dict, ledger: dict) -> None:
        concerns["R1-3c"]["evidence"]["files"] = ["chapters/chapter6.tex"]

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, unchanged_file)
    assert code == 1
    assert found(payload, "R-COMMIT") == [("Critical", "R1-3c")]


def test_commit_ignores_rebuttal_root_changes(rebuttal_case, defense_scripts, capsys) -> None:
    def rebuttal_files(concerns: dict, ledger: dict) -> None:
        concerns["R1-3c"]["evidence"]["files"] = [
            "rebuttal/pre-review/workspace/concerns.yaml",
            "rebuttal/pre-review/review_results/评阅书1.txt",
        ]

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, rebuttal_files)
    assert code == 1
    assert found(payload, "R-COMMIT") == [("Critical", "R1-3c")]


def test_r_claim_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def claim(concerns: dict, ledger: dict) -> None:
        concerns["R1-3d"]["response"] = "已补充两章之间的过渡段。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, claim)
    assert code == 1
    assert found(payload, "R-CLAIM") == [("Critical", "R1-3d")]


def test_r_loc_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def missing_label(concerns: dict, ledger: dict) -> None:
        concerns["R1-2"]["locations"] = [{"label": "eq:c2-missing"}]

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, missing_label)
    assert code == 1
    assert found(payload, "R-LOC") == [("Major", "R1-2")]


def test_r_page_stale_negative(rebuttal_case, defense_scripts, capsys) -> None:
    build(defense_scripts, capsys, rebuttal_case)
    later = time.time()
    os.utime(rebuttal_case.thesis / "chapters" / "chapter2.tex", (later, later))
    code, payload = check(defense_scripts, capsys, rebuttal_case)
    assert code == 1
    assert found(payload, "R-PAGE-STALE") == [("Major", "R1-2")]


def test_r_renum_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def old_number(concerns: dict, ledger: dict) -> None:
        concerns["R1-3b"]["locations"] = [{"file": "chapters/chapter2.tex", "section": "2.2"}]
        concerns["R1-3b"]["response"] = "已重绘图2-1，删去图中重复的说明文字。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, old_number)
    assert code == 0
    assert found(payload, "R-RENUM") == [("Minor", "R1-3b")]


def test_r_md_syntax_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def bold(concerns: dict, ledger: dict) -> None:
        concerns["R1-1"]["response"] = "本文将跨路网迁移列为**后续工作**。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, bold)
    assert code == 1
    hits = [f for f in payload["findings"] if f["code"] == "R-MD-SYNTAX"]
    assert {(f["severity"], f["concern"]) for f in hits} == {("Major", "-")}
    assert "responses/response-all.md" in {f["file"] for f in hits}


def test_r_placeholder_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def todo(concerns: dict, ledger: dict) -> None:
        concerns["R1-1"]["response"] = "TODO 补充迁移实验的说明。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, todo)
    assert code == 1
    hits = found(payload, "R-PLACEHOLDER")
    assert ("Critical", "R1-1") in hits
    assert ("Critical", "-") in hits


def test_r_num_src_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def numbers(concerns: dict, ledger: dict) -> None:
        concerns["R1-1"]["response"] += "初步估计的迁移误差约为 12.7%。"
        concerns["R2-1"]["response"] += "数据规模扩大到1.5 倍时不改变网络结构。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, numbers)
    assert code == 1
    hits = found(payload, "R-NUM-SRC")
    assert ("Major", "R1-1") in hits
    assert ("Info", "R2-1") in hits


def test_r_review_changed_negative(rebuttal_case, defense_scripts, capsys) -> None:
    review = rebuttal_case.reviews / "评阅书2.txt"
    review.write_text(review.read_text(encoding="utf-8") + "补充一行\n", encoding="utf-8")
    code, payload = run_case(defense_scripts, capsys, rebuttal_case)
    assert code == 1
    assert found(payload, "R-REVIEW-CHANGED") == [("Major", "R2")]


def test_r_shared_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def clarify(concerns: dict, ledger: dict) -> None:
        concerns["R2-2"].update(
            action="clarify",
            response="该节的切分方式与对比文献一致，此处在回复中说明。",
            locations=[],
            evidence={"kind": "none", "files": [], "note": ""},
        )

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, clarify)
    assert code == 0
    assert found(payload, "R-SHARED") == [("Minor", "R1-3a")]


def test_r_result_negative(rebuttal_case, defense_scripts, capsys) -> None:
    build(defense_scripts, capsys, rebuttal_case)
    result = rebuttal_case.root / "responses" / "review-result.md"
    result.write_text("总体评价 1（A）；总体评价 2（A）\n", encoding="utf-8")
    code, payload = check(defense_scripts, capsys, rebuttal_case)
    assert code == 1
    assert found(payload, "R-RESULT") == [("Major", "R2")]


def test_r_sync_negative(rebuttal_case, defense_scripts, capsys) -> None:
    build(defense_scripts, capsys, rebuttal_case)
    target = rebuttal_case.root / "responses" / "response-R1.md"
    target.write_text(target.read_text(encoding="utf-8") + "\n手改的一行\n", encoding="utf-8")
    code, payload = check(defense_scripts, capsys, rebuttal_case)
    assert code == 0
    hits = [f for f in payload["findings"] if f["code"] == "R-SYNC"]
    assert [(f["severity"], f["concern"], f["file"]) for f in hits] == [
        ("Minor", "-", "responses/response-R1.md")
    ]


def test_r_tone_negative(rebuttal_case, defense_scripts, capsys) -> None:
    def resource_reason(concerns: dict, ledger: dict) -> None:
        concerns["R2-1"]["response"] = "受时间所限，本文不展开不同硬件平台上的开销评测。"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, resource_reason)
    assert code == 0
    assert found(payload, "R-TONE") == [("Info", "R2-1")]


def test_skipped_without_thesis(rebuttal_case, defense_scripts, capsys) -> None:
    build(defense_scripts, capsys, rebuttal_case)
    code, payload = check(defense_scripts, capsys, rebuttal_case, thesis=False)
    assert code == 0
    assert set(payload["skipped"]) == SKIPPED_WITHOUT_THESIS
    assert set(found(payload, "R-COMMIT")) == {
        ("Info", concern) for concern in ("R1-2", "R1-3a", "R1-3b", "R1-3c", "R2-2")
    }


def test_json_payload_and_check_json(rebuttal_case, defense_scripts, capsys) -> None:
    def misquote(concerns: dict, ledger: dict) -> None:
        concerns["R1-3b"]["quote"] = "图2-1文字很密集"

    code, payload = run_case(defense_scripts, capsys, rebuttal_case, misquote)
    assert code == 1
    assert set(payload) == {"findings", "summary", "skipped"}
    assert set(payload["summary"]) == {"Critical", "Major", "Minor", "Info"}
    finding = payload["findings"][0]
    assert finding["source_kind"] == "script"
    assert finding["priority"] == "P1"
    saved = json.loads((rebuttal_case.workspace / "check.json").read_text(encoding="utf-8"))
    assert saved == payload

    args = ["--workspace", str(rebuttal_case.workspace), "--thesis", str(rebuttal_case.thesis)]
    assert defense_scripts.rebuttal_check.main(args) == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("% R-QUOTE (concern=R1-3b, workspace/concerns.yaml:")
    assert "[Severity: Major] [Priority: P1]: [Script]" in lines[0]
    assert lines[-1].startswith("% 汇总：Critical 0，Major 1")
