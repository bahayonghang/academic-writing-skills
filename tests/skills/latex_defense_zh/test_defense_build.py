"""Tests for scripts/build_deck.py and the Jinja templates."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from pathlib import Path

import pytest
import yaml

MARKER_RE = re.compile(r"^% defense-frame: id=(\S+) role=(\S+) chapter=(\S+) layout=(\S+)$")
TAG_RE = re.compile(r"\\tag\*\{\(([^)]*)\)\}")
EQUATION_RE = re.compile(r"\\begin\{(\w+)\*\}(.*?)\\end\{\1\*\}", re.S)
TABLE_RE = re.compile(
    r"\\adjustbox\{max width=\\textwidth,max totalheight=0\.62\\textheight\}\{%\n(.*?)\}\\par\n"
    r"\\end\{DefenseSource\}",
    re.S,
)
GRAPHICSPATH_RE = re.compile(r"^\\graphicspath\{(.*)\}$", re.M)
FIGURE_FILE_RE = re.compile(r"\\DefenseFigure(?:\[[^\]]*\])?\{([^}]*)\}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markers(tex: str) -> list[dict]:
    lines = tex.splitlines()
    found = []
    for index, line in enumerate(lines):
        match = MARKER_RE.match(line)
        if match:
            assert lines[index + 1].startswith("\\begin{frame}")
            frame_id, role, chapter, layout = match.groups()
            found.append(
                {
                    "id": frame_id,
                    "role": role,
                    "chapter": chapter,
                    "layout": layout,
                    "body": lines[index + 2],
                }
            )
    return found


def build(defense_scripts, tmp_path: Path, plan: dict, out: str, *extra: str) -> int:
    path = tmp_path / f"{out}.yaml"
    path.write_text(yaml.safe_dump(plan, allow_unicode=True, sort_keys=False), encoding="utf-8")
    args = ["--plan", str(path), "--inventory", str(tmp_path / "inventory.json")]
    return defense_scripts.build_deck.main([*args, "--out", str(tmp_path / out), *extra])


def test_frame_markers_follow_framework(built_deck: Path) -> None:
    tex = read(built_deck / "defense.tex")
    found = markers(tex)
    assert len(found) == tex.count("\\begin{frame}") == 54
    assert [found[0]["role"], found[1]["role"], found[-1]["role"]] == ["cover", "toc", "thanks"]
    assert found[1]["body"] == "\\DefenseTocFrame{0}"
    for number in range(2, 8):
        index = next(i for i, m in enumerate(found) if m["id"] == f"c{number}-toc")
        assert found[index]["chapter"] == str(number)
        assert found[index]["body"] == f"\\DefenseTocFrame{{{number}}}"
        assert found[index + 1]["chapter"] == str(number)
        assert all(m["chapter"] != str(number) for m in found[:index])
    for number in (3, 4, 5):
        roles = [m["role"] for m in found if m["chapter"] == str(number) and m["role"] != "toc"]
        assert roles == ["intro", "problem"] + ["method"] * 3 + ["experiment"] * 4 + ["summary"]
    conclusion = [m["role"] for m in found if m["chapter"] == "7" and m["role"] != "toc"]
    assert conclusion == ["innovation", "outlook"]


def test_tex_escape_table(defense_scripts) -> None:
    escape = defense_scripts.build_deck.tex_escape
    assert escape("a%b&c_d#e$f{g}h~i^j\\k") == (
        "a\\%b\\&c\\_d\\#e\\$f\\{g\\}h\\textasciitilde{}i\\textasciicircum{}j\\textbackslash{}k"
    )
    assert escape("提升 **50%** 精度") == "提升 \\DefenseHighlight{50\\%} 精度"
    assert escape("**a** 与 **b") == "\\DefenseHighlight{a} 与 **b"
    assert escape(None) == ""


def test_equation_and_table_bodies_round_trip(built_deck: Path, inventory: dict) -> None:
    tex = read(built_deck / "defense.tex")
    rendered = EQUATION_RE.findall(tex)
    assert len(rendered) == 6
    for env, body in rendered:
        numbers = TAG_RE.findall(body)
        matches = [
            eq
            for eq in inventory["equations"]
            if eq["env"] == env and [item["number"] for item in eq["labels"]] == numbers
        ]
        assert len(matches) == 1, (env, numbers)
        restored = body
        for item in matches[0]["labels"]:
            tag = "\\tag*{(" + item["number"] + ")}"
            restored = restored.replace(tag, "\\label{" + item["label"] + "}", 1)
        assert restored == matches[0]["tex"]
    bodies = TABLE_RE.findall(tex)
    assert len(bodies) == 5
    assert set(bodies) == {table["tabular_source"] for table in inventory["tables"]}


def test_graphicspath_is_relative_and_resolves(built_deck: Path, inventory: dict) -> None:
    tex = read(built_deck / "defense.tex")
    match = GRAPHICSPATH_RE.search(tex)
    assert match is not None
    entries = re.findall(r"\{([^{}]*)\}", match.group(1))
    assert entries == ["../mini-thesis/fig/", "../mini-thesis/"]
    for entry in entries:
        assert not re.match(r"^(/|[A-Za-z]:)", entry)
        assert (built_deck / entry).is_dir()
    allowed = {item["path"] for f in inventory["figures"] for item in f["files"]}
    allowed |= {sub["file"] for f in inventory["figures"] for sub in f["subfigures"]}
    used = FIGURE_FILE_RE.findall(tex)
    assert used and set(used) <= allowed
    for path in used:
        assert any((built_deck / entry / path).is_file() for entry in entries)
    assert "\\DefenseSetup{logo={../mini-thesis/fig/logo.png},stage=predefense}" in tex


def test_macros_notes_and_manifest(built_deck: Path) -> None:
    macros = read(built_deck / "thesis-macros.tex")
    assert "\\providecommand{\\vect}[1]{\\boldsymbol{#1}}" in macros
    assert "\\ifdefined\\Loss\\else \\def\\Loss{\\mathcal{L}}\\fi" in macros
    assert "unusedmacro" not in macros
    assert "ysuctitlelines" not in macros
    notes = read(built_deck / "notes.md")
    assert notes.count("\n## ") == 55
    assert "## 16 3.3 时空图卷积补全模型（c3-method-1，method，51 秒）" in notes
    assert "- 目标秒数：2400 秒（40 分钟）" in notes
    assert "〔待填写〕" not in notes
    manifest = json.loads(read(built_deck / "build_manifest.json"))
    assert manifest["frames"] == 54
    assert manifest["theme"] == "YanshanDefense"
    assert set(manifest["files"]) == {
        "defense.tex",
        "notes.md",
        "thesis-macros.tex",
        "beamerthemeYanshanDefense.sty",
        "beamerthemeGenericDefense.sty",
        "defense-layouts.sty",
    }
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((built_deck / name).read_bytes()).hexdigest() == digest
    assert manifest["warnings"] == []


def test_select_macros_follows_macro_use(defense_scripts) -> None:
    macros = [
        {"name": "a", "command": "newcommand", "definition": "\\newcommand{\\a}{\\b x}"},
        {"name": "b", "command": "def", "definition": "\\def\\b{y}"},
        {"name": "c", "command": "newcommand", "definition": "\\newcommand{\\c}{z}"},
    ]
    selected = defense_scripts.build_deck.select_macros(macros, ["$\\a$"])
    assert [macro["name"] for macro in selected] == ["a", "b"]


def test_existing_output_needs_force(
    built_deck: Path, filled_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    before = (built_deck / "defense.tex").read_bytes()
    assert build(defense_scripts, tmp_path, filled_plan, "deck") == 4
    assert (built_deck / "defense.tex").read_bytes() == before
    partial = tmp_path / "partial"
    partial.mkdir()
    (partial / "notes.md").write_text("old", encoding="utf-8")
    assert build(defense_scripts, tmp_path, filled_plan, "partial") == 4
    assert sorted(path.name for path in partial.iterdir()) == ["notes.md"]
    (built_deck / "keep.txt").write_text("keep", encoding="utf-8")
    (built_deck / "defense.tex").write_text("old", encoding="utf-8")
    assert build(defense_scripts, tmp_path, filled_plan, "deck", "--force") == 0
    assert (built_deck / "keep.txt").read_text(encoding="utf-8") == "keep"
    assert (built_deck / "defense.tex").read_bytes() == before


def test_no_brace_group_follows_frame_title(
    filled_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    # Beamer reads a brace group right after \begin{frame}{title} as the subtitle,
    # which swallowed the figure grid when the frame had no subsection bar.
    for frame in filled_plan["frames"]:
        if frame["layout"] not in ("cover", "toc", "thanks"):
            frame["subsection"] = ""
    assert "figure-grid" in {frame["layout"] for frame in filled_plan["frames"]}
    assert build(defense_scripts, tmp_path, filled_plan, "bare") == 0
    lines = read(tmp_path / "bare" / "defense.tex").splitlines()
    for index, line in enumerate(lines):
        if line.startswith("\\begin{frame}{"):
            assert not lines[index + 1].lstrip().startswith("{"), lines[index + 1]


def test_force_keeps_unchanged_files(
    built_deck: Path, filled_plan: dict, tmp_path: Path, defense_scripts
) -> None:
    # latexmk skips a rebuild when defense.tex is unchanged, so its mtime must not move
    # past defense.pdf; a notes-only edit rewrites notes.md alone.
    old = 1_000_000_000
    for path in built_deck.iterdir():
        os.utime(path, (old, old))
    filled_plan["frames"][3]["notes"]["say"] += "补充一句讲稿。"
    assert build(defense_scripts, tmp_path, filled_plan, "deck", "--force") == 0
    changed = sorted(p.name for p in built_deck.iterdir() if p.stat().st_mtime != old)
    assert changed == ["build_manifest.json", "notes.md"]


@pytest.mark.parametrize(
    ("frame_id", "field", "value"),
    [
        ("c3-method-1", "role", "unknown-role"),
        ("c3-method-1", "layout", "unknown-layout"),
        ("c3-method-3", "figures", [{"label": "fig:not-in-thesis"}]),
        ("c3-experiment-3", "figures", [{"label": "fig:c3-compare", "subfigures": ["a", "z"]}]),
        ("c3-method-1", "equations", [{"label": "eq:not-in-thesis"}]),
        ("c3-experiment-1", "table", "tab:not-in-thesis"),
        ("c3-summary", "paper", "P9"),
        ("c3-method-3", "figures", ["fig:c3-compare"]),
        ("c3-experiment-1", "table", ["tab:c3-datasets"]),
        ("cover", "notes", "说明"),
    ],
)
def test_invalid_plan_exits_2(
    filled_plan: dict, tmp_path: Path, defense_scripts, frame_id: str, field: str, value: object
) -> None:
    frame = next(frame for frame in filled_plan["frames"] if frame["id"] == frame_id)
    frame[field] = value
    assert build(defense_scripts, tmp_path, filled_plan, "bad") == 2
    assert not (tmp_path / "bad").exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("extra_packages", ["xcolor}\\input{x"]),
        ("minutes", "40"),
        ("title_lines", "题目"),
        ("chapters", [{"number": 1}]),
    ],
)
def test_invalid_meta_exits_2(
    filled_plan: dict, tmp_path: Path, defense_scripts, field: str, value: object
) -> None:
    filled_plan["meta"][field] = value
    assert build(defense_scripts, tmp_path, filled_plan, "bad") == 2


def test_long_table_body_exits_2(
    filled_plan: dict, inventory: dict, tmp_path: Path, defense_scripts, capsys
) -> None:
    table = next(table for table in inventory["tables"] if table["label"] == "tab:c3-datasets")
    table["tabular_source"] = "\\begin{longtable}{cc}\na & b \\\\\n\\end{longtable}"
    text = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    (tmp_path / "inventory.json").write_text(text, encoding="utf-8")
    assert build(defense_scripts, tmp_path, filled_plan, "bad") == 2
    assert "longtable" in capsys.readouterr().err


def test_plan_text_is_escaped_in_deck(filled_plan: dict, tmp_path: Path, defense_scripts) -> None:
    frame = next(frame for frame in filled_plan["frames"] if frame["id"] == "c1-background-2")
    frame["bullets"] = ["误差下降 **50%**，成本 $1_000 & 更多"]
    assert build(defense_scripts, tmp_path, filled_plan, "escaped") == 0
    tex = read(tmp_path / "escaped" / "defense.tex")
    assert "\\item 误差下降 \\DefenseHighlight{50\\%}，成本 \\$1\\_000 \\& 更多" in tex


@pytest.mark.skipif(
    os.environ.get("DEFENSE_ZH_COMPILE") != "1" or shutil.which("latexmk") is None,
    reason="set DEFENSE_ZH_COMPILE=1 and install latexmk with xelatex to compile the deck",
)
@pytest.mark.parametrize("theme", ["yanshan", "generic"])
def test_fixture_deck_compiles(
    filled_plan: dict, tmp_path: Path, defense_scripts, theme: str
) -> None:
    filled_plan["meta"]["theme"] = theme
    assert build(defense_scripts, tmp_path, filled_plan, f"deck-{theme}", "--compile") == 0
    log = read(tmp_path / f"deck-{theme}" / "defense.log")
    assert "(54 pages" in log
