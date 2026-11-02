"""Tests for the Touying backend of scripts/build_deck.py (compile tests need DEFENSE_TYPST_COMPILE=1)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

MARKER_RE = re.compile(r"^// defense-frame: id=(\S+) role=(\S+) chapter=(\S+) layout=(\S+)$", re.M)
NOTE_RE = re.compile(r"#note\[|\bnote: \[")
INJECTED = 'Injection # $ ] // " \\ 与 **强调** 结束'
INJECTED_TAKEAWAY = 'takeaway # $x$ ] // "q"'


def build(defense_scripts, tmp_path: Path, *extra: str) -> int:
    args = [
        "--plan",
        str(tmp_path / "slide_plan.yaml"),
        "--inventory",
        str(tmp_path / "inventory.json"),
        "--out",
        str(tmp_path / "deck"),
    ]
    return defense_scripts.build_deck.main([*args, *extra])


def write_plan(plan: dict, path: Path) -> None:
    path.write_text(
        yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8"
    )


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frame_segments(typ: str) -> list[tuple[str, str]]:
    matches = list(MARKER_RE.finditer(typ))
    ends = [match.start() for match in matches[1:]] + [len(typ)]
    return [(match.group(1), typ[match.end() : end]) for match, end in zip(matches, ends)]


def inject(plan: dict) -> None:
    frame = next(f for f in plan["frames"] if f["id"] == "c1-background-2")
    frame["bullets"] = [INJECTED]
    frame["takeaway"] = INJECTED_TAKEAWAY


def test_markers_follow_the_plan_with_one_note_each(built_typst: Path, touying_plan: dict) -> None:
    typ = (built_typst / "defense.typ").read_text(encoding="utf-8")
    segments = frame_segments(typ)
    assert [frame_id for frame_id, _ in segments] == [f["id"] for f in touying_plan["frames"]]
    assert len(segments) == 54
    for frame_id, body in segments:
        assert len(NOTE_RE.findall(body)) == 1, frame_id
    assert '#import "@preview/simply-ysu-touying:0.2.0": *' in typ
    assert 'stage-en: "Pre-defense"' in typ
    assert not (built_typst / "defense.tex").exists()
    assert sorted(p.name for p in built_typst.iterdir()) == [
        "build_manifest.json",
        "defense.typ",
        "img",
        "notes.md",
    ]


def test_plan_text_is_written_as_string_literals(
    touying_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    inject(touying_plan)
    write_plan(touying_plan, tmp_path / "slide_plan.yaml")
    assert build(defense_scripts, tmp_path) == 0
    typ = (tmp_path / "deck" / "defense.typ").read_text(encoding="utf-8")
    assert '[#"Injection # $ ] // \\" \\\\ 与 "#hl("强调")#" 结束"]' in typ
    assert '#takeaway("takeaway # $x$ ] // \\"q\\"")' in typ


def test_images_are_copied_unchanged(
    built_typst: Path, mini_thesis: Path, touying_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    manifest = read_json(built_typst / "build_manifest.json")
    assert manifest["backend"] == "touying"
    assert manifest["notes_pdf"] == "defense-notes.pdf"
    assert manifest["typst_package"] == "@preview/simply-ysu-touying:0.2.0"
    copied = manifest["copied_images"]
    assert copied and all(item.startswith("img/") for item in copied)
    for item in copied:
        source = mini_thesis / item.removeprefix("img/")
        assert (built_typst / item).read_bytes() == source.read_bytes()
    on_disk = sorted(
        p.relative_to(built_typst).as_posix()
        for p in (built_typst / "img").rglob("*")
        if p.is_file()
    )
    assert on_disk == sorted(copied)

    assert build(defense_scripts, tmp_path) == 4
    first = built_typst / copied[0]
    stamps = {name: (built_typst / name).stat().st_mtime_ns for name in ("defense.typ", copied[0])}
    stale = built_typst / "img" / "fig" / "stale" / "old.png"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"old")
    user_file = built_typst / "img" / "keep.png"
    user_file.write_bytes(b"user")
    manifest["copied_images"].append("img/fig/stale/old.png")
    manifest["copied_images"].append("../outside.png")
    write_json(built_typst / "build_manifest.json", manifest)
    (tmp_path / "outside.png").write_bytes(b"outside")
    assert build(defense_scripts, tmp_path, "--force") == 0
    assert not stale.exists() and not stale.parent.exists()
    assert user_file.exists() and (tmp_path / "outside.png").exists()
    assert first.is_file()
    for name, stamp in stamps.items():
        assert (built_typst / name).stat().st_mtime_ns == stamp, name


def test_without_notes_pdf_manifest_records_null(
    touying_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    assert build(defense_scripts, tmp_path, "--no-notes-pdf") == 0
    assert read_json(tmp_path / "deck" / "build_manifest.json")["notes_pdf"] is None


def test_old_plan_without_deck_builds_beamer(
    filled_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    filled_plan.pop("deck", None)
    write_plan(filled_plan, tmp_path / "slide_plan.yaml")
    assert build(defense_scripts, tmp_path) == 0
    assert (tmp_path / "deck" / "defense.tex").is_file()
    assert not (tmp_path / "deck" / "defense.typ").exists()


def test_touying_rejects_other_themes(touying_plan: dict, tmp_path: Path, defense_scripts, capsys):
    touying_plan["meta"]["theme"] = "generic"
    write_plan(touying_plan, tmp_path / "slide_plan.yaml")
    assert build(defense_scripts, tmp_path) == 2
    assert "yanshan" in capsys.readouterr().err
    touying_plan["meta"]["theme"] = "yanshan"
    touying_plan["deck"]["backend"] = "slidev"
    write_plan(touying_plan, tmp_path / "slide_plan.yaml")
    assert build(defense_scripts, tmp_path) == 2
    assert not (tmp_path / "deck").exists()


def edit_inventory(tmp_path: Path, change) -> None:
    path = tmp_path / "inventory.json"
    data = read_json(path)
    change(data)
    write_json(path, data)


def test_complex_table_exits_2(touying_plan: dict, tmp_path: Path, defense_scripts, capsys):
    def change(data: dict) -> None:
        table = next(t for t in data["tables"] if t["label"] == "tab:c3-datasets")
        table["tabular_source"] = (
            "\\begin{tabular}{cc}\n\\multirow{2}{*}{a} & b \\\\\n & c \\\\\n\\end{tabular}"
        )

    edit_inventory(tmp_path, change)
    assert build(defense_scripts, tmp_path) == 2
    err = capsys.readouterr().err
    assert "tab:c3-datasets" in err and "multirow" in err
    assert not (tmp_path / "deck").exists()


def test_eps_figure_exits_2(touying_plan: dict, tmp_path: Path, defense_scripts, capsys):
    def change(data: dict) -> None:
        figure = next(f for f in data["figures"] if f["label"] == "fig:c3-network")
        for item in figure["files"]:
            item["resolved"] = item["resolved"].rsplit(".", 1)[0] + ".eps"

    edit_inventory(tmp_path, change)
    assert build(defense_scripts, tmp_path) == 2
    assert ".eps" in capsys.readouterr().err


def test_parameterised_def_exits_2(touying_plan: dict, tmp_path: Path, defense_scripts, capsys):
    def change(data: dict) -> None:
        macro = next(m for m in data["macros"] if m["name"] == "Loss")
        macro["definition"] = "\\def\\Loss#1{\\mathcal{L}(#1)}"

    edit_inventory(tmp_path, change)
    assert build(defense_scripts, tmp_path) == 2
    assert "Loss" in capsys.readouterr().err


def test_missing_package_exits_6_before_compiling(
    touying_plan: dict, tmp_path: Path, defense_scripts, monkeypatch, capsys
) -> None:
    backend = defense_scripts.build_deck.typst_backend
    calls: list[list[str]] = []
    monkeypatch.setattr(backend.shutil, "which", lambda name: "typst")
    monkeypatch.setattr(backend, "typst_version", lambda executable: (0, 15, 1))
    monkeypatch.setattr(backend.subprocess, "run", lambda command, **kw: calls.append(command))
    monkeypatch.delenv("TYPST_PACKAGE_PATH", raising=False)
    monkeypatch.setenv("TYPST_PACKAGE_CACHE_PATH", str(tmp_path / "no-cache"))
    empty = tmp_path / "no-packages"
    empty.mkdir()
    code = build(defense_scripts, tmp_path, "--compile", "--typst-package-path", str(empty))
    assert code == 6
    assert calls == []
    assert "@preview/simply-ysu-touying:0.2.0" in capsys.readouterr().err
    assert (tmp_path / "deck" / "defense.typ").is_file()
    assert not (tmp_path / "deck" / "defense.pdf").exists()


def test_compile_produces_slides_and_notes(
    typst_compile, touying_plan: dict, tmp_path: Path, defense_scripts, capsys
) -> None:
    pymupdf = pytest.importorskip("pymupdf")
    inject(touying_plan)
    write_plan(touying_plan, tmp_path / "slide_plan.yaml")
    assert build(defense_scripts, tmp_path, "--compile") == 0
    deck = tmp_path / "deck"
    capsys.readouterr()
    with pymupdf.open(deck / "defense.pdf") as slides:
        assert slides.page_count == 54
        text = " ".join(page.get_text() for page in slides)
    assert "Injection # $ ] //" in text and "强调" in text
    with pymupdf.open(deck / "defense-notes.pdf") as notes:
        assert notes.page_count == 108
        labels = defense_scripts.check_typst.page_labels(notes)
    assert all(not label.startswith("notes:") for label in labels[0::2])
    assert all(label.startswith("notes:") for label in labels[1::2])

    args = ["--deck", str(deck / "defense.typ"), "--inventory", str(tmp_path / "inventory.json")]
    code = defense_scripts.check_deck.main([*args, "--json"])
    result = json.loads(capsys.readouterr().out)
    assert result["findings"] == []
    assert result["skipped"] == ["D-OVERFLOW-H"]
    assert code == 0
