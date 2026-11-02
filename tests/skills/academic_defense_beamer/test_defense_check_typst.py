"""Tests for check_deck.py on a Touying deck (defense.typ); no Typst needed."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml
from PIL import Image

UNCOMPILED = ["D-COMPILE", "D-OVERFLOW-V", "D-OVERFLOW-H", "D-NOTES-PDF"]
PRIORITY = {"Critical": "P0", "Major": "P1", "Minor": "P2", "Info": "P3"}
NETWORK_IMAGE = "img/fig/chapter3/network.png"
BULLET = '"合成要点 c1-background-2-1"'
C3_PAPER = "示例作者, 示例导师. 基于时空图卷积的示例流量补全方法[J]. 示例学报, 2025, 1(1): 1-10."
C5_PAPER = "示例作者. 面向模型更新的示例在线预测方法[C]. 示例会议, 2026: 21-28."
SLIDE_SIZE = (453.5, 255.1)
NOTES_SIZE = (453.5, 453.5 * 13.5 / 16)
Mutation = Callable[[Path, Path], list[str]]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run_check(defense_scripts, capsys, tmp_path: Path, *extra: str) -> tuple[int, dict]:
    deck = tmp_path / "deck" / "defense.typ"
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
    lines = (deck / "defense.typ").read_text(encoding="utf-8").split("\n")
    return next(number for number, line in enumerate(lines, 1) if needle in line)


def newer_than_deck(deck: Path, path: Path) -> None:
    mtime = (deck / "defense.typ").stat().st_mtime + 10
    os.utime(path, (mtime, mtime))


def write_log(deck: Path, text: str, pdf: bool = True) -> None:
    (deck / "defense.log").write_text(text, encoding="utf-8")
    if pdf:
        (deck / "defense.pdf").write_bytes(b"%PDF-1.5\n")
        newer_than_deck(deck, deck / "defense.pdf")


def replace(old: str, new: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        edit_file(deck / "defense.typ", old, new)
        return []

    return mutate


def drop_frame(frame_id: str) -> Mutation:
    """Delete a frame from its marker line up to the next marker."""

    def mutate(deck: Path, root: Path) -> list[str]:
        path = deck / "defense.typ"
        lines = path.read_text(encoding="utf-8").split("\n")
        start = next(
            i
            for i, line in enumerate(lines)
            if line.startswith(f"// defense-frame: id={frame_id} ")
        )
        end = next(
            i for i in range(start + 1, len(lines)) if lines[i].startswith("// defense-frame: ")
        )
        del lines[start:end]
        path.write_text("\n".join(lines), encoding="utf-8")
        return []

    return mutate


def drop_note(frame_id: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        path = deck / "defense.typ"
        lines = path.read_text(encoding="utf-8").split("\n")
        prefix = f'#note[#strong("合成要点 {frame_id}")'
        kept = [line for line in lines if not line.startswith(prefix)]
        assert len(kept) == len(lines) - 1, prefix
        path.write_text("\n".join(kept), encoding="utf-8")
        return []

    return mutate


def log(template: str, pdf: bool = True) -> Mutation:
    """Write defense.log; ``{line}`` becomes the deck line of the network image (c3-method-3)."""

    def mutate(deck: Path, root: Path) -> list[str]:
        write_log(deck, template.format(line=deck_line(deck, NETWORK_IMAGE)), pdf)
        return []

    return mutate


def cli_args(*extra: str) -> Mutation:
    def mutate(deck: Path, root: Path) -> list[str]:
        return list(extra)

    return mutate


def delete_copy(deck: Path, root: Path) -> list[str]:
    (deck / "img" / "fig" / "chapter4" / "fusion.png").unlink()
    return []


def tall_copy(deck: Path, root: Path) -> list[str]:
    Image.new("RGB", (400, 800), (200, 210, 225)).save(
        deck / "img" / "fig" / "chapter4" / "results.png"
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


# (case id, code, severity, frame id, mutation)
CASES: list[tuple[str, str, str, str, Mutation]] = [
    (
        "marker-missing",
        "D-MARKER",
        "Minor",
        "#17",
        replace("// defense-frame: id=c3-method-2 role=method chapter=3 layout=bullets\n", ""),
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
        replace('#side-card(label: "创新点 3")[#"合成要点 c7-innovation-3"]\n', ""),
    ),
    ("placeholder", "D-PLACEHOLDER", "Major", "c1-background-2", replace(BULLET, '"〔待填写〕"')),
    (
        "fig-allow",
        "D-FIG-ALLOW",
        "Critical",
        "c3-method-3",
        replace(NETWORK_IMAGE, "img/fig/chapter3/invented.png"),
    ),
    ("fig-missing", "D-FIG-MISSING", "Major", "c4-method-3", delete_copy),
    (
        "fig-number",
        "D-FIG-NUMBER",
        "Major",
        "c3-method-3",
        replace('#"图3-3"#h(1em)', '#"图3-9"#h(1em)'),
    ),
    (
        "fig-caption",
        "D-FIG-NUMBER",
        "Major",
        "c3-method-3",
        replace('#"图3-3"#h(1em)', '#"图3-2"#h(1em)'),
    ),
    ("fig-aspect", "D-FIG-ASPECT", "Minor", "c4-experiment-1", tall_copy),
    ("eq-src", "D-EQ-SRC", "Critical", "c3-method-1", replace("\\sigma^{2}", "\\sigma^{3}")),
    (
        "eq-outside",
        "D-EQ-SRC",
        "Major",
        "c3-method-2",
        replace('"合成要点 c3-method-2-1"', "[$x$]"),
    ),
    ("tab-src", "D-TAB-SRC", "Critical", "c3-experiment-4", replace('[#"0.52"]', '[#"0.53"]')),
    (
        "tab-outside",
        "D-TAB-SRC",
        "Major",
        "c3-experiment-2",
        replace('"合成要点 c3-experiment-2-1"', "table(columns: 1)[a]"),
    ),
    (
        "num-src",
        "D-NUM-SRC",
        "Major",
        "c3-experiment-2",
        replace('"合成要点 c3-experiment-2-1"', '"误差下降 37.25%"'),
    ),
    ("paper-text", "D-PAPER", "Critical", "c3-summary", replace("1(1): 1-10.", "1(1): 1-11.")),
    ("paper-chapter", "D-PAPER", "Major", "c3-summary", replace(C3_PAPER, C5_PAPER)),
    (
        "paper-missing",
        "D-PAPER",
        "Minor",
        "c3-summary",
        replace(f'#paper-box[#"{C3_PAPER}"]\n', ""),
    ),
    ("meta-empty", "D-META", "Major", "-", replace('author: "示例作者"', 'author: ""')),
    ("meta-title", "D-META", "Major", "-", replace('"流量预测方法研究"]', '"流量补全方法研究"]')),
    ("meta-info", "D-META", "Info", "-", clear_inventory_author),
    (
        "stage-defense",
        "D-STAGE",
        "Major",
        "-",
        replace('stage-en: "Pre-defense"', 'stage-en: "Defense"'),
    ),
    ("stage-plan", "D-STAGE", "Major", "-", plan_stage_defense),
    ("density-major", "D-DENSITY", "Major", "c1-background-2", replace(BULLET, f'"{"测" * 300}"')),
    ("density-minor", "D-DENSITY", "Minor", "c1-background-2", replace(BULLET, f'"{"测" * 200}"')),
    (
        "density-items",
        "D-DENSITY",
        "Minor",
        "c1-background-2",
        replace(f"  {BULLET},\n", '  "条目",\n' * 6),
    ),
    (
        "density-takeaway",
        "D-DENSITY",
        "Minor",
        "c1-background-2",
        replace('#takeaway("合成结论 c1-background-2")', f'#takeaway("{"测" * 45}")'),
    ),
    ("budget", "D-BUDGET", "Major", "-", cli_args("--minutes", "60")),
    ("notes-missing", "D-NOTES", "Major", "-", delete_notes),
    ("notes-call", "D-NOTES", "Minor", "c3-problem", drop_note("c3-problem")),
    (
        "compile-error",
        "D-COMPILE",
        "Critical",
        "c3-method-3",
        log(
            "== typst compile defense.pdf ==\nerror: unknown variable: foo\n   ┌─ defense.typ:{line}:2\n"
        ),
    ),
    (
        "compile-error-rounded",
        "D-COMPILE",
        "Critical",
        "c3-method-3",
        log("error: file not found\n   ╭─ ./defense.typ:{line}:10\n"),
    ),
    ("compile-unlocated", "D-COMPILE", "Critical", "-", log("error: failed to load package\n")),
    (
        "compile-pdf",
        "D-COMPILE",
        "Critical",
        "-",
        log("== typst compile defense.pdf ==\n", pdf=False),
    ),
]


# ---------------------------------------------------------------------------
# Baseline and injected defects
# ---------------------------------------------------------------------------


def test_baseline_deck_has_no_findings(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"], result["skipped"]) == (0, [], UNCOMPILED)
    assert result["deck"] == "defense.typ"
    code, result = run_check(
        defense_scripts, capsys, tmp_path, "--plan", str(tmp_path / "slide_plan.yaml")
    )
    assert (code, result["findings"], result["skipped"]) == (0, [], UNCOMPILED)


def test_clean_log_skips_only_horizontal_overflow(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(defense_scripts.check_deck.check_typst, "note_records", lambda path: None)
    write_log(built_typst, "== typst compile defense.pdf ==\nwarning: unused\n")
    manifest_path = built_typst / "build_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["notes_pdf"] = None
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    code, result = run_check(defense_scripts, capsys, tmp_path)
    # The placeholder PDF has no readable page count, so D-OVERFLOW-V is skipped as well.
    assert (code, result["findings"]) == (0, [])
    assert "D-OVERFLOW-H" in result["skipped"] and "D-COMPILE" not in result["skipped"]


@pytest.mark.parametrize(
    ("code", "severity", "frame", "mutate"),
    [case[1:] for case in CASES],
    ids=[case[0] for case in CASES],
)
def test_injected_defect_is_reported(
    built_typst: Path,
    tmp_path: Path,
    defense_scripts,
    capsys,
    monkeypatch,
    code: str,
    severity: str,
    frame: str,
    mutate: Mutation,
) -> None:
    monkeypatch.setattr(defense_scripts.check_deck.check_typst, "note_records", lambda path: None)
    extra = mutate(built_typst, tmp_path)
    exit_code, result = run_check(defense_scripts, capsys, tmp_path, *extra)
    assert (code, severity, PRIORITY[severity], frame) in keys(result), result["findings"]
    assert exit_code == (1 if severity in ("Critical", "Major") else 0)
    assert "D-OVERFLOW-H" in result["skipped"]
    if code == "D-NUM-SRC":
        finding = next(f for f in result["findings"] if f["code"] == code)
        assert finding["meaning_check"] == "NEEDS-LLM"
        assert "37.25" in finding["message"]


def test_source_regions_hide_thesis_text(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    """Numbers inside a caption region are thesis text, not plan text (no D-NUM-SRC)."""
    replace('#"示例补全指标对比"', '#"示例补全指标对比 99.99"')(built_typst, tmp_path)
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert not [f for f in result["findings"] if f["code"] == "D-NUM-SRC"]


# ---------------------------------------------------------------------------
# Suffix and manifest dispatch
# ---------------------------------------------------------------------------


def test_deck_suffix_must_match_manifest(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    inventory = str(tmp_path / "inventory.json")
    copy = built_typst / "defense.tex"
    copy.write_text((built_typst / "defense.typ").read_text(encoding="utf-8"), encoding="utf-8")
    assert defense_scripts.check_deck.main(["--deck", str(copy), "--inventory", inventory]) == 2
    assert "touying" in capsys.readouterr().err
    other = built_typst / "defense.md"
    other.write_text("x", encoding="utf-8")
    assert defense_scripts.check_deck.main(["--deck", str(other), "--inventory", inventory]) == 2
    assert "defense.typ" in capsys.readouterr().err


def test_beamer_deck_with_typ_suffix_is_rejected(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    typ = built_deck / "defense.typ"
    typ.write_text("// empty\n", encoding="utf-8")
    args = ["--deck", str(typ), "--inventory", str(tmp_path / "inventory.json")]
    assert defense_scripts.check_deck.main(args) == 2
    assert "beamer" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# D-OVERFLOW-V: page records of the compiled deck
# ---------------------------------------------------------------------------


def write_pdf(path: Path, sizes: list[tuple[float, float]], labels=None) -> None:
    """Synthetic PDF; ``labels`` are (prefix, start) rules written as Typst does (indirect)."""
    pymupdf = pytest.importorskip("pymupdf")
    document = pymupdf.open()
    for width, height in sizes:
        document.new_page(width=width, height=height)
    if labels is not None:
        nums = []
        for index, (prefix, start) in enumerate(labels):
            xref = document.get_new_xref()
            p = f" /P ({prefix})" if prefix else ""
            document.update_object(xref, f"<< /Type /PageLabel /S /D{p} /St {start} >>")
            nums.append(f"{index} {xref} 0 R")
        document.xref_set_key(
            document.pdf_catalog(), "PageLabels", f"<< /Nums [{' '.join(nums)}] >>"
        )
    document.save(path)
    document.close()


def compiled(deck: Path, pages: int) -> None:
    write_pdf(deck / "defense.pdf", [SLIDE_SIZE] * pages)
    newer_than_deck(deck, deck / "defense.pdf")
    (deck / "defense.log").write_text("== typst compile defense.pdf ==\n", encoding="utf-8")


def overflow(result: dict) -> list[tuple[str, str]]:
    return [(f["severity"], f["frame"]) for f in result["findings"] if f["code"] == "D-OVERFLOW-V"]


def test_overflow_located_from_note_records(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys, monkeypatch
) -> None:
    compiled(built_typst, 56)
    # Frame 16 (c3-method-1) spans pages 16-17; the last frame (54) spans pages 55-56.
    records = [{"frame": n, "page": n if n <= 16 else n + 1} for n in range(1, 55)]
    monkeypatch.setattr(defense_scripts.check_deck.check_typst, "note_records", lambda p: records)
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert overflow(result) == [("Major", "c3-method-1"), ("Major", "thanks")]
    line = deck_line(built_typst, "// defense-frame: id=c3-method-1 ")
    finding = next(f for f in result["findings"] if f["frame"] == "c3-method-1")
    assert finding["line"] == line and "续出 1 页" in finding["message"]
    assert code == 1


def test_overflow_without_records_counts_pages(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys, monkeypatch
) -> None:
    monkeypatch.setattr(defense_scripts.check_deck.check_typst, "note_records", lambda p: None)
    compiled(built_typst, 54)
    _, result = run_check(defense_scripts, capsys, tmp_path)
    assert overflow(result) == []
    compiled(built_typst, 55)
    _, result = run_check(defense_scripts, capsys, tmp_path)
    assert overflow(result) == [("Major", "-")]
    assert "D-OVERFLOW-H" in result["skipped"]


# ---------------------------------------------------------------------------
# D-NOTES-PDF: notes:N pages of the presenter build
# ---------------------------------------------------------------------------


def presenter_pages(frames: int = 54) -> tuple[list, list]:
    sizes, labels = [], []
    for number in range(1, frames + 1):
        sizes += [SLIDE_SIZE, NOTES_SIZE]
        labels += [("", number), ("notes:", number)]
    return sizes, labels


def notes_findings(defense_scripts, capsys, tmp_path: Path) -> tuple[int, list[dict]]:
    code, result = run_check(defense_scripts, capsys, tmp_path)
    return code, [f for f in result["findings"] if f["code"] == "D-NOTES-PDF"]


@pytest.fixture
def slides_built(built_typst: Path, defense_scripts, monkeypatch) -> Path:
    monkeypatch.setattr(defense_scripts.check_deck.check_typst, "note_records", lambda p: None)
    compiled(built_typst, 54)
    return built_typst


def test_typst_page_labels_are_read(slides_built: Path, defense_scripts) -> None:
    pymupdf = pytest.importorskip("pymupdf")
    sizes, labels = presenter_pages(3)
    path = slides_built / "labels.pdf"
    write_pdf(path, sizes, labels)
    with pymupdf.open(path) as document:
        found = defense_scripts.check_typst.page_labels(document)
    assert found == ["1", "notes:1", "2", "notes:2", "3", "notes:3"]


def test_notes_pdf_presenter_build_passes(
    slides_built: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    write_pdf(slides_built / "defense-notes.pdf", *presenter_pages())
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"], result["skipped"]) == (0, [], ["D-OVERFLOW-H"])


def wrong_height(sizes: list, labels: list) -> tuple[list, list]:
    sizes[1] = (SLIDE_SIZE[0], SLIDE_SIZE[1])
    return sizes, labels


def missing_last_note(sizes: list, labels: list) -> tuple[list, list]:
    return sizes[:-1], labels[:-1]


def unpaired_label(sizes: list, labels: list) -> tuple[list, list]:
    labels[5] = ("notes:", 9)
    return sizes, labels


@pytest.mark.parametrize(
    ("change", "needle"),
    [
        (wrong_height, "13.5/16"),
        (missing_last_note, "备注页 53 个"),
        (unpaired_label, "不配对"),
    ],
    ids=["height", "missing-note", "label"],
)
def test_notes_pdf_defect_is_reported(
    slides_built: Path, tmp_path: Path, defense_scripts, capsys, change, needle: str
) -> None:
    write_pdf(slides_built / "defense-notes.pdf", *change(*presenter_pages()))
    code, found = notes_findings(defense_scripts, capsys, tmp_path)
    assert found and all(f["severity"] == "Major" for f in found)
    assert any(needle in f["message"] for f in found), found
    assert code == 1


def test_notes_pdf_missing_file_is_minor(
    slides_built: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    code, found = notes_findings(defense_scripts, capsys, tmp_path)
    assert code == 0
    assert [(f["severity"], f["frame"]) for f in found] == [("Minor", "-")]
    assert "缺少备注版 defense-notes.pdf" in found[0]["message"]


def test_tilde_in_table_cell_is_a_no_break_space(
    built_typst: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    """``~`` reaches defense.typ as U+00A0, and D-TAB-SRC compares it without a false positive."""
    path = tmp_path / "inventory.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    table = next(t for t in data["tables"] if t["label"] == "tab:c3-datasets")
    assert "示例数据集 A" in table["tabular_source"]
    table["tabular_source"] = table["tabular_source"].replace("示例数据集 A", "示例数据集~A")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args = ["--plan", str(tmp_path / "slide_plan.yaml"), "--inventory", str(path)]
    assert defense_scripts.build_deck.main([*args, "--out", str(built_typst), "--force"]) == 0
    capsys.readouterr()
    typ = (built_typst / "defense.typ").read_text(encoding="utf-8")
    assert '"示例数据集\u00a0A"' in typ
    code, result = run_check(defense_scripts, capsys, tmp_path)
    assert (code, result["findings"]) == (0, [])
