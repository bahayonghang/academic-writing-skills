"""Tests for scripts/check_deck.py on the built fixture deck."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml
from PIL import Image

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-defense-zh"
SCRIPT = SKILL_ROOT / "scripts" / "check_deck.py"
QUALITY_GATE = SKILL_ROOT / "references" / "quality-gate.md"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
LOG_CODES = ["D-COMPILE", "D-OVERFLOW-V", "D-OVERFLOW-H"]
LINE_RE = re.compile(
    r"^% (D-[A-Z]+(?:-[A-Z]+)*) \(frame=(\S+), ([\w.-]+):(\d+|-)\) "
    r"\[Severity: (Critical|Major|Minor|Info)\] \[Priority: (P[0-3])\]: \[Script\] (.+)$"
)
SUMMARY_RE = re.compile(r"^% 汇总：Critical \d+，Major \d+，Minor \d+，Info \d+；skipped：\S+$")
FINDING_KEYS = {
    "code",
    "severity",
    "priority",
    "source_kind",
    "frame",
    "line",
    "file",
    "message",
    "meaning_check",
}
PRIORITY = {"Critical": "P0", "Major": "P1", "Minor": "P2", "Info": "P3"}
NETWORK_FIGURE = "chapter3/network.png"
Mutation = Callable[[Path, Path], list[str]]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run_check(defense_scripts, capsys, tmp_path: Path, *extra: str) -> tuple[int, dict]:
    deck = tmp_path / "deck" / "defense.tex"
    args = ["--deck", str(deck), "--inventory", str(tmp_path / "inventory.json"), "--json"]
    code = defense_scripts.check_deck.main([*args, *extra])
    return code, json.loads(capsys.readouterr().out)


def keys(result: dict) -> set[tuple[str, str, str, str]]:
    return {(f["code"], f["severity"], f["priority"], f["frame"]) for f in result["findings"]}


def edit_file(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, old
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def deck_line(deck: Path, needle: str) -> int:
    lines = (deck / "defense.tex").read_text(encoding="utf-8").split("\n")
    return next(number for number, line in enumerate(lines, 1) if needle in line)


def write_log(deck: Path, text: str, pdf: bool = True) -> None:
    (deck / "defense.log").write_text(text, encoding="utf-8")
    if pdf:
        path = deck / "defense.pdf"
        path.write_bytes(b"%PDF-1.5\n")
        mtime = (deck / "defense.tex").stat().st_mtime + 10
        os.utime(path, (mtime, mtime))


def tree_hashes(*roots: Path) -> dict[str, str]:
    found = {}
    for root in roots:
        paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in paths:
            found[path.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


# ---------------------------------------------------------------------------
# Mutations: each one injects one defect into the built deck or its inputs
# ---------------------------------------------------------------------------


def replace(old: str, new: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        edit_file(deck / "defense.tex", old, new)
        return []

    return mutate


def replace_notes(pattern: str, new: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        path = deck / "notes.md"
        text, count = re.subn(pattern, new, path.read_text(encoding="utf-8"), count=1, flags=re.M)
        assert count == 1, pattern
        path.write_text(text, encoding="utf-8")
        return []

    return mutate


def drop_frame(frame_id: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        path = deck / "defense.tex"
        lines = path.read_text(encoding="utf-8").split("\n")
        start = next(
            i for i, line in enumerate(lines) if line.startswith(f"% defense-frame: id={frame_id} ")
        )
        end = next(i for i in range(start, len(lines)) if lines[i] == "\\end{frame}")
        del lines[start : end + 2]
        path.write_text("\n".join(lines), encoding="utf-8")
        return []

    return mutate


def log(template: str, pdf: bool = True) -> Mutation:
    """Write defense.log; ``{line}`` becomes the deck line of the network figure (c3-method-3)."""

    def mutate(deck: Path, root: Path) -> list[str]:
        write_log(deck, template.format(line=deck_line(deck, NETWORK_FIGURE)), pdf)
        return []

    return mutate


def cli_args(*extra: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        return list(extra)

    return mutate


def delete_image(deck: Path, root: Path) -> list[str]:
    (root / "mini-thesis" / "fig" / "chapter4" / "fusion.png").unlink()
    return []


def tall_image(deck: Path, root: Path) -> list[str]:
    Image.new("RGB", (400, 800), (200, 210, 225)).save(
        root / "mini-thesis" / "fig" / "chapter4" / "results.png"
    )
    return []


def delete_notes(deck: Path, root: Path) -> list[str]:
    (deck / "notes.md").unlink()
    return []


def clear_inventory_author(deck: Path, root: Path) -> list[str]:
    path = root / "inventory.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["meta"]["author"] = ""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return []


def plan_stage_defense(deck: Path, root: Path) -> list[str]:
    plan = yaml.safe_load((root / "slide_plan.yaml").read_text(encoding="utf-8"))
    plan["meta"]["stage"] = "defense"
    path = root / "plan-defense.yaml"
    path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return ["--plan", str(path)]


ACHIEVEMENTS_FRAME = (
    "% defense-frame: id=c7-achievements role=achievements chapter=7 layout=bullets\n"
    "\\begin{frame}{总结与展望}\n\\begin{itemize}\n  \\item 合成成果\n\\end{itemize}\n"
    "\\end{frame}\n\n% defense-frame: id=thanks "
)
C3_PAPER = "示例作者, 示例导师. 基于时空图卷积的示例流量补全方法[J]. 示例学报, 2025, 1(1): 1-10."
C5_PAPER = "示例作者. 面向模型更新的示例在线预测方法[C]. 示例会议, 2026: 21-28."
BULLET = "合成要点 c1-background-2-1"
NUMBER_BULLET = "误差下降 37.25\\%"
BACKUP_FRAME = (
    "% defense-frame: id=backup-1 role=backup chapter=3 layout=bullets\n"
    "\\begin{frame}{备用页}\n\\begin{itemize}\n  \\item 合成要点 backup-1\n\\end{itemize}\n"
    "\\end{frame}\n\n\\end{document}"
)
BACKUP_NOTES = (
    "## 55 备用页（backup-1，backup，900 秒）\n\n- 说什么：合成讲稿 backup-1。\n"
    "- 要点：合成要点 backup-1\n- 时长：900 秒\n- 过渡：无\n- 可能提问：无\n\n## 合计"
)

# (case id, code, severity, frame id, mutation)
CASES: list[tuple[str, str, str, str, Mutation]] = [
    (
        "marker-missing",
        "D-MARKER",
        "Minor",
        "#17",
        replace("% defense-frame: id=c3-method-2 role=method chapter=3 layout=bullets\n", ""),
    ),
    (
        "marker-invalid",
        "D-MARKER",
        "Major",
        "c3-method-2",
        replace("id=c3-method-2 role=method", "id=c3-method-2 role=unknown-role"),
    ),
    ("coverage", "D-COVERAGE", "Major", "c7-toc", drop_frame("c7-outlook")),
    ("toc", "D-TOC", "Major", "c4-intro", drop_frame("c4-toc")),
    (
        "chain",
        "D-CHAIN",
        "Major",
        "c7-innovation",
        replace("\\DefenseCard{创新点 3}{合成要点 c7-innovation-3}\n", ""),
    ),
    ("placeholder", "D-PLACEHOLDER", "Major", "c1-background-2", replace(BULLET, "〔待填写〕")),
    (
        "fig-allow",
        "D-FIG-ALLOW",
        "Critical",
        "c3-method-3",
        replace(NETWORK_FIGURE, "chapter3/invented.png"),
    ),
    ("fig-missing", "D-FIG-MISSING", "Major", "c4-method-3", delete_image),
    ("fig-number", "D-FIG-NUMBER", "Major", "c3-method-3", replace("图3-3\\quad", "图3-9\\quad")),
    ("fig-caption", "D-FIG-NUMBER", "Major", "c3-method-3", replace("图3-3\\quad", "图3-2\\quad")),
    ("fig-aspect", "D-FIG-ASPECT", "Minor", "c4-experiment-1", tall_image),
    ("eq-src", "D-EQ-SRC", "Critical", "c3-method-1", replace("\\sigma^{2}", "\\sigma^{3}")),
    (
        "eq-outside",
        "D-EQ-SRC",
        "Major",
        "c3-method-2",
        replace("合成要点 c3-method-2-1", "合成要点 $x$"),
    ),
    ("tab-src", "D-TAB-SRC", "Critical", "c3-experiment-4", replace("& 0.52 &", "& 0.53 &")),
    (
        "tab-outside",
        "D-TAB-SRC",
        "Major",
        "c3-experiment-2",
        replace("合成要点 c3-experiment-2-1", "\\begin{tabular}{c}a\\end{tabular}"),
    ),
    (
        "num-src",
        "D-NUM-SRC",
        "Major",
        "c3-experiment-2",
        replace("合成要点 c3-experiment-2-1", NUMBER_BULLET),
    ),
    ("paper-text", "D-PAPER", "Critical", "c3-summary", replace("1(1): 1-10.", "1(1): 1-11.")),
    ("paper-chapter", "D-PAPER", "Major", "c3-summary", replace(C3_PAPER, C5_PAPER)),
    (
        "paper-missing",
        "D-PAPER",
        "Minor",
        "c3-summary",
        replace(f"\\DefensePaperBox{{{C3_PAPER}}}\n", ""),
    ),
    ("meta-empty", "D-META", "Major", "-", replace("\\author{示例作者}", "\\author{}")),
    ("meta-title", "D-META", "Major", "-", replace("流量预测方法研究}", "流量补全方法研究}")),
    ("meta-info", "D-META", "Info", "-", clear_inventory_author),
    ("stage-defense", "D-STAGE", "Major", "-", replace("stage=predefense", "stage=defense")),
    ("stage-plan", "D-STAGE", "Major", "-", plan_stage_defense),
    (
        "stage-achievements",
        "D-STAGE",
        "Minor",
        "c7-achievements",
        replace("% defense-frame: id=thanks ", ACHIEVEMENTS_FRAME),
    ),
    ("density-major", "D-DENSITY", "Major", "c1-background-2", replace(BULLET, "测" * 300)),
    ("density-minor", "D-DENSITY", "Minor", "c1-background-2", replace(BULLET, "测" * 200)),
    (
        "density-items",
        "D-DENSITY",
        "Minor",
        "c1-background-2",
        replace(f"  \\item {BULLET}\n", "  \\item 条目\n" * 6),
    ),
    (
        "density-takeaway",
        "D-DENSITY",
        "Minor",
        "c1-background-2",
        replace("合成结论 c1-background-2}", "测" * 45 + "}"),
    ),
    ("budget", "D-BUDGET", "Major", "-", cli_args("--minutes", "60")),
    ("budget-notes", "D-BUDGET", "Minor", "-", replace_notes(r"^- 时长：50 秒$", "- 时长：500 秒")),
    ("notes-missing", "D-NOTES", "Major", "-", delete_notes),
    (
        "notes-field",
        "D-NOTES",
        "Minor",
        "c3-problem",
        replace_notes(r"^- 过渡：合成过渡 c3-problem\n", ""),
    ),
    (
        "notes-say",
        "D-NOTES",
        "Minor",
        "c3-problem",
        replace_notes(r"^- 说什么：合成讲稿 c3-problem。.*$", "- 说什么：太短。"),
    ),
    (
        "compile-error",
        "D-COMPILE",
        "Critical",
        "c3-method-3",
        log("./defense.tex:{line}: Undefined control sequence.\n"),
    ),
    (
        "compile-error-bang",
        "D-COMPILE",
        "Critical",
        "c3-method-3",
        log("! Undefined control sequence.\n<argument> \\foo\n\nl.{line} \\DefenseFigure\n"),
    ),
    (
        "compile-undefined",
        "D-COMPILE",
        "Major",
        "c3-method-3",
        log("LaTeX Warning: Reference `fig:x' on page 3 undefined on input line {line}.\n"),
    ),
    ("compile-pdf", "D-COMPILE", "Critical", "-", log("clean log\n", pdf=False)),
    (
        "overflow-v",
        "D-OVERFLOW-V",
        "Major",
        "c3-method-3",
        log("Overfull \\vbox (12.0pt too high) detected at line {line}\n"),
    ),
    (
        "overflow-h-major",
        "D-OVERFLOW-H",
        "Major",
        "c3-method-3",
        log("Overfull \\hbox (25.0pt too wide) in paragraph at lines {line}--{line}\n"),
    ),
    (
        "overflow-h-minor",
        "D-OVERFLOW-H",
        "Minor",
        "c3-method-3",
        log("Overfull \\hbox (12.0pt too wide) in paragraph at lines {line}--{line}\n"),
    ),
]


# ---------------------------------------------------------------------------
# Positive cases and code coverage
# ---------------------------------------------------------------------------


def test_baseline_deck_has_no_findings(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"], result["skipped"]) == (0, [], LOG_CODES)
    code, result = run_check(
        defense_scripts, capsys, tmp_path, "--plan", str(tmp_path / "slide_plan.yaml")
    )
    assert (code, result["findings"], result["skipped"]) == (0, [], LOG_CODES)


def test_clean_log_has_no_findings(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    line = deck_line(built_deck, NETWORK_FIGURE)
    write_log(
        built_deck,
        f"Overfull \\hbox (3.0pt too wide) in paragraph at lines {line}--{line}\n"
        "Output written on defense.xdv (54 pages).\n",
    )
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"], result["skipped"]) == (0, [], [])


def test_backup_frame_is_outside_the_time_budget(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    """The time budget does not count backup pages (references/defense-framework.md)."""
    replace("\\end{document}", BACKUP_FRAME)(built_deck, tmp_path)
    replace_notes(r"^## 合计$", BACKUP_NOTES)(built_deck, tmp_path)
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"]) == (0, [])


def test_cases_cover_every_code(defense_scripts) -> None:
    codes = defense_scripts.check_deck.CODES
    assert len(codes) == 21
    assert {case[1] for case in CASES} == set(codes)
    table = re.findall(r"^\|\s*(D-[A-Z]+(?:-[A-Z]+)*)\s*\|", QUALITY_GATE.read_text("utf-8"), re.M)
    assert set(table) == set(codes)


@pytest.mark.parametrize(
    ("code", "severity", "frame", "mutate"),
    [case[1:] for case in CASES],
    ids=[case[0] for case in CASES],
)
def test_injected_defect_is_reported(
    built_deck: Path,
    tmp_path: Path,
    defense_scripts,
    capsys,
    code: str,
    severity: str,
    frame: str,
    mutate: Mutation,
) -> None:
    extra = mutate(built_deck, tmp_path)
    exit_code, result = run_check(defense_scripts, capsys, tmp_path, *extra)
    assert (code, severity, PRIORITY[severity], frame) in keys(result), result["findings"]
    assert exit_code == (1 if severity in ("Critical", "Major") else 0)
    if code == "D-NUM-SRC":
        finding = next(f for f in result["findings"] if f["code"] == code)
        assert finding["meaning_check"] == "NEEDS-LLM"
        assert "37.25" in finding["message"]


# ---------------------------------------------------------------------------
# Parent AC8: numbers, images, and equations outside the thesis
# ---------------------------------------------------------------------------


def test_parent_ac8_number_outside_thesis(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    replace("合成要点 c3-experiment-2-1", NUMBER_BULLET)(built_deck, tmp_path)
    assert ("D-NUM-SRC", "Major", "P1", "c3-experiment-2") in keys(
        run_check(defense_scripts, capsys, tmp_path)[1]
    )


def test_parent_ac8_image_outside_inventory(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    replace(NETWORK_FIGURE, "chapter3/invented.png")(built_deck, tmp_path)
    assert ("D-FIG-ALLOW", "Critical", "P0", "c3-method-3") in keys(
        run_check(defense_scripts, capsys, tmp_path)[1]
    )


def test_parent_ac8_rewritten_equation(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    replace("\\sigma^{2}", "\\sigma^{3}")(built_deck, tmp_path)
    assert ("D-EQ-SRC", "Critical", "P0", "c3-method-1") in keys(
        run_check(defense_scripts, capsys, tmp_path)[1]
    )


# ---------------------------------------------------------------------------
# Output contract, input errors, and read-only behavior
# ---------------------------------------------------------------------------


def test_text_and_json_output_contract(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    replace("合成要点 c3-experiment-2-1", NUMBER_BULLET)(built_deck, tmp_path)
    delete_notes(built_deck, tmp_path)
    args = [
        "--deck",
        str(built_deck / "defense.tex"),
        "--inventory",
        str(tmp_path / "inventory.json"),
    ]
    assert defense_scripts.check_deck.main(args) == 1
    lines = capsys.readouterr().out.strip().split("\n")
    assert SUMMARY_RE.match(lines[-1]), lines[-1]
    assert lines[-1].endswith("skipped：D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H")
    matches = [LINE_RE.match(line) for line in lines[:-1]]
    assert lines[:-1] and all(matches), lines
    assert any("[Script] Meaning-Check: NEEDS-LLM：数字 37.25" in line for line in lines)
    assert "% D-NOTES (frame=-, notes.md:-) [Severity: Major] [Priority: P1]" in "\n".join(lines)

    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert code == 1
    assert set(result) == {"deck", "findings", "summary", "skipped"}
    assert result["deck"] == "defense.tex"
    assert set(result["summary"]) == set(PRIORITY)
    assert all(set(finding) == FINDING_KEYS for finding in result["findings"])
    assert {finding["source_kind"] for finding in result["findings"]} == {"script"}
    assert {finding["meaning_check"] for finding in result["findings"]} == {"", "NEEDS-LLM"}


@pytest.mark.parametrize(
    "case",
    [
        "missing-deck",
        "missing-inventory",
        "bad-inventory",
        "missing-plan",
        "missing-log",
        "minutes-range",
    ],
)
def test_input_errors_exit_2(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys, case: str
) -> None:
    deck = str(built_deck / "defense.tex")
    inventory = str(tmp_path / "inventory.json")
    args = {
        "missing-deck": ["--deck", str(tmp_path / "none.tex"), "--inventory", inventory],
        "missing-inventory": ["--deck", deck, "--inventory", str(tmp_path / "none.json")],
        "bad-inventory": ["--deck", deck, "--inventory", str(tmp_path / "bad.json")],
        "missing-plan": ["--deck", deck, "--inventory", inventory, "--plan", str(tmp_path / "x")],
        "missing-log": ["--deck", deck, "--inventory", inventory, "--log", str(tmp_path / "x")],
        "minutes-range": ["--deck", deck, "--inventory", inventory, "--minutes", "5"],
    }[case]
    (tmp_path / "bad.json").write_text("{not json", encoding="utf-8")
    assert defense_scripts.check_deck.main(args) == 2
    assert "错误：" in capsys.readouterr().err


def test_unreadable_thesis_skips_number_check(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    path = tmp_path / "inventory.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["thesis_root"] = (tmp_path / "missing-thesis").as_posix()
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"], result["skipped"]) == (0, [], ["D-NUM-SRC", *LOG_CODES])


def test_check_does_not_write(built_deck: Path, tmp_path: Path, defense_scripts, capsys) -> None:
    line = deck_line(built_deck, NETWORK_FIGURE)
    write_log(built_deck, f"Overfull \\vbox (12.0pt too high) detected at line {line}\n")
    roots = (built_deck, tmp_path / "inventory.json", tmp_path / "slide_plan.yaml")
    before = tree_hashes(*roots, tmp_path / "mini-thesis")
    run_check(defense_scripts, capsys, tmp_path, "--plan", str(tmp_path / "slide_plan.yaml"))
    args = [
        "--deck",
        str(built_deck / "defense.tex"),
        "--inventory",
        str(tmp_path / "inventory.json"),
    ]
    defense_scripts.check_deck.main(args)
    capsys.readouterr()
    assert tree_hashes(*roots, tmp_path / "mini-thesis") == before
    assert sorted(path.name for path in built_deck.iterdir()) == sorted(
        [*defense_scripts.build_deck.OWNED_FILES, "defense.log", "defense.pdf"]
    )


def test_cli_prints_utf8(built_deck: Path, tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(SCRIPT),
            "--deck",
            str(built_deck / "defense.tex"),
            "--inventory",
            str(tmp_path / "inventory.json"),
        ],
        capture_output=True,
        encoding="utf-8",
        env=ENV,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == (
        "% 汇总：Critical 0，Major 0，Minor 0，Info 0；skipped：D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H"
    )
