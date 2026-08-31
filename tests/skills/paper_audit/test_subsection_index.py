"""Regression coverage for paper-audit subsection indexes and windows."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from parsers import get_parser
from paths import WorkspaceLayout
from prepare_review_workspace import (
    SUBSECTION_CONTEXT_MIN_HAN,
    SUBSECTION_CONTEXT_MIN_HAN_RATIO,
    SUBSECTION_CONTEXT_MIN_VISIBLE,
    ContextParagraph,
    _context_is_eligible,
    _split_context_paragraphs,
    build_context_window,
    build_subsection_units,
    prepare_subsection_artifacts,
    prepare_workspace,
)
from tex_loader import assemble

from tests.support.paths import SKILLS_ROOT

_ZH_SKILL = SKILLS_ROOT / "latex-thesis-zh"
_PROJECT_FIXTURE = _ZH_SKILL / "evals" / "fixtures" / "subsection-context" / "main.tex"
_NO_DEPTH3_FIXTURE = _ZH_SKILL / "evals" / "fixtures" / "thesis-project" / "main.tex"
_READONLY_BAIT_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "paper_audit"
    / "subsection_context_readonly_bait.tex"
)
EXPECTED_PROJECT_IDS = [
    "1.1.1",
    "1.2.1",
    "1.2.2",
    "1.2.3",
    "1.3.1",
    "1.4.1",
    "1.4.2",
    "1.4.3",
    "2.1.1",
]


def _load_zh_logic() -> Any:
    script = _ZH_SKILL / "scripts" / "analyze_logic.py"
    scripts_dir = script.parent
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location("zh_subsection_context_contract", script)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(scripts_dir))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def _read_index(layout: WorkspaceLayout) -> dict:
    return json.loads(layout.subsection_index.read_text(encoding="utf-8"))


def test_multifile_index_uses_all_headings_and_source_coordinates(tmp_path: Path) -> None:
    workspace = prepare_workspace(
        str(_PROJECT_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    layout = WorkspaceLayout(workspace)
    payload = _read_index(layout)

    assert payload["subsection_index_status"] == "ok"
    units = payload["units"]
    assert [unit["subsection_id"] for unit in units] == EXPECTED_PROJECT_IDS
    assert "前置单元" in {unit["title"] for unit in units}
    assert units[0]["source_file"] == "chapters/method-a.tex"
    assert units[-1]["source_file"] == "chapters/method-b.tex"

    first = units[0]
    source = _PROJECT_FIXTURE.parent / first["source_file"]
    source_line = source.read_text(encoding="utf-8").splitlines()[first["source_start"] - 1]
    assert first["title"] in source_line

    section_payload = json.loads(layout.section_index.read_text(encoding="utf-8"))
    assert isinstance(section_payload, list)
    assert (layout.references_dir / "SUBSECTION_CONTEXT_PROTOCOL.md").is_file()


def test_multifile_ids_match_zh_canonical_cursor(tmp_path: Path) -> None:
    workspace = prepare_workspace(
        str(_PROJECT_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    audit_ids = [unit["subsection_id"] for unit in _read_index(WorkspaceLayout(workspace))["units"]]

    zh_logic = _load_zh_logic()
    zh_doc = zh_logic.assemble(_PROJECT_FIXTURE)
    zh_parser = zh_logic.get_parser(_PROJECT_FIXTURE)
    zh_units = zh_logic._build_subsection_cursor(
        zh_doc,
        zh_parser,
        zh_parser.split_sections(zh_doc.content),
    )
    zh_ids = [unit.subsection_id for unit in zh_units]

    assert audit_ids == EXPECTED_PROJECT_IDS
    assert zh_ids == EXPECTED_PROJECT_IDS


def test_multifile_windows_match_zh_canonical_projection(tmp_path: Path) -> None:
    workspace = prepare_workspace(
        str(_PROJECT_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    layout = WorkspaceLayout(workspace)
    audit_windows = [
        json.loads(layout.window_file(subsection_id).read_text(encoding="utf-8"))
        for subsection_id in EXPECTED_PROJECT_IDS
    ]

    zh_logic = _load_zh_logic()
    zh_doc = zh_logic.assemble(_PROJECT_FIXTURE)
    zh_parser = zh_logic.get_parser(_PROJECT_FIXTURE)
    zh_sections = zh_parser.split_sections(zh_doc.content)
    zh_units = zh_logic._build_subsection_cursor(zh_doc, zh_parser, zh_sections)
    zh_paragraphs = zh_logic._split_arc_paragraphs(zh_doc.content, zh_parser, zh_sections)
    zh_logic._DOC = zh_doc
    zh_windows = [
        dict(zh_logic._build_context_window(zh_units, index, zh_paragraphs))
        for index in range(len(zh_units))
    ]

    assert audit_windows == zh_windows


def test_public_clis_expose_the_same_hardcoded_multifile_cursor(tmp_path: Path) -> None:
    audit_script = SKILLS_ROOT / "paper-audit" / "scripts" / "prepare_review_workspace.py"
    output_dir = tmp_path / "cli-review-results"
    subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            str(audit_script),
            str(_PROJECT_FIXTURE),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    workspaces = list(output_dir.iterdir())
    assert len(workspaces) == 1
    audit_payload = json.loads(
        (workspaces[0] / "artifacts" / "data" / "subsection_index.json").read_text(encoding="utf-8")
    )
    assert [unit["subsection_id"] for unit in audit_payload["units"]] == EXPECTED_PROJECT_IDS

    zh_script = _ZH_SKILL / "scripts" / "analyze_logic.py"
    observed: list[str] = []
    for subsection_id in EXPECTED_PROJECT_IDS:
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                str(zh_script),
                str(_PROJECT_FIXTURE),
                "--emit-window",
                "--subsection",
                subsection_id,
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert f"小节窗口 {subsection_id}" in result.stdout
        observed.append(subsection_id)
    assert observed == EXPECTED_PROJECT_IDS


def test_windows_match_canonical_statuses_and_do_not_copy_body_text(tmp_path: Path) -> None:
    workspace = prepare_workspace(
        str(_PROJECT_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    layout = WorkspaceLayout(workspace)
    windows = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in layout.windows_dir.glob("*.json")
    }

    cross_parent = windows["1.2.1"]
    assert cross_parent["same_parent"] == {"prev": False, "next": True}
    assert [part["part"] for part in cross_parent["read_only"]] == [
        "prev.tail",
        "parent_lead",
        "next.head",
    ]
    parent_lead = cross_parent["read_only"][1]
    assert parent_lead["source_file"] == "chapters/method-a.tex"
    assert (parent_lead["source_start"], parent_lead["source_end"]) == (12, 13)

    assert windows["1.4.2"]["current_lead_status"] == "no_eligible_paragraph"
    assert windows["1.4.3"]["current_lead_status"] == "no_eligible_paragraph"
    assert windows["1.4.2"]["next_head_status"] == "no_eligible_paragraph"

    expected_part_order = ["prev.tail", "parent_lead", "next.head"]
    status_to_part = {
        "prev_tail_status": "prev.tail",
        "parent_lead_status": "parent_lead",
        "next_head_status": "next.head",
    }
    for window in windows.values():
        source_path = _PROJECT_FIXTURE.parent / window["source_file"]
        assert window["source_file"].startswith("chapters/")
        assert source_path.is_file()
        source_lines = source_path.read_text(encoding="utf-8").splitlines()
        editable = window["editable"]
        assert window["title"] in source_lines[editable["source_start"] - 1]

        parts = {part["part"]: part for part in window["read_only"]}
        assert [part["part"] for part in window["read_only"]] == [
            name for name in expected_part_order if name in parts
        ]
        assert len(parts) <= 3
        for status_key, part_name in status_to_part.items():
            status = window.get(status_key)
            assert status in {None, "ok", "no_eligible_paragraph", "absent"}
            assert (part_name in parts) is (status == "ok")
        for part in parts.values():
            part_source = _PROJECT_FIXTURE.parent / part["source_file"]
            assert part["source_file"].startswith("chapters/")
            assert part_source.is_file()
            part_line_count = len(part_source.read_text(encoding="utf-8").splitlines())
            assert 1 <= part["source_start"] <= part["source_end"] <= part_line_count

    serialized = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(layout.windows_dir.glob("*.json"))
    )
    for source in sorted((_PROJECT_FIXTURE.parent / "chapters").glob("*.tex")):
        text = source.read_text(encoding="utf-8")
        for offset in range(max(0, len(text) - 19)):
            fragment = text[offset : offset + 20]
            assert fragment not in serialized


def test_no_depth_three_and_unsupported_formats_write_explicit_envelopes(
    tmp_path: Path,
) -> None:
    workspace = prepare_workspace(
        str(_NO_DEPTH3_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    layout = WorkspaceLayout(workspace)
    assert _read_index(layout) == {
        "subsection_index_status": "no_depth3_headings",
        "units": [],
    }
    assert isinstance(json.loads(layout.section_index.read_text(encoding="utf-8")), list)

    for suffix in (".typ", ".pdf"):
        source = tmp_path / f"unsupported{suffix}"
        source.write_text("placeholder", encoding="utf-8")
        unsupported_layout = WorkspaceLayout(tmp_path / f"state-{suffix[1:]}")
        state = prepare_subsection_artifacts(source, object(), unsupported_layout)
        assert state["status"] == "unsupported_format"
        assert _read_index(unsupported_layout) == {
            "subsection_index_status": "unsupported_format",
            "units": [],
        }


def test_depth_numbering_handles_article_and_starred_parent_chains(tmp_path: Path) -> None:
    article = tmp_path / "article.tex"
    article.write_text(
        "\\section{Root}\n"
        "\\subsection{Parent}\n"
        "\\subsubsection{Unit A}\nBody.\n"
        "\\subsubsection{Unit B}\nBody.\n",
        encoding="utf-8",
    )
    article_doc = assemble(article)
    article_units = build_subsection_units(article_doc, get_parser(str(article)))
    assert [unit.subsection_id for unit in article_units] == ["1.1.1", "1.1.2"]

    starred = tmp_path / "starred.tex"
    starred.write_text(
        "\\chapter{Numbered}\n"
        "\\section{Parent}\n"
        "\\subsection{Valid}\nBody.\n"
        "\\chapter*{Unnumbered}\n"
        "\\section{Invalid Parent}\n"
        "\\subsection{Invalid Unit}\nBody.\n",
        encoding="utf-8",
    )
    starred_doc = assemble(starred)
    starred_units = build_subsection_units(starred_doc, get_parser(str(starred)))
    assert [unit.subsection_id for unit in starred_units] == ["1.1.1"]

    starred_parent = tmp_path / "starred-parent.tex"
    starred_parent.write_text(
        "\\chapter{Numbered}\n"
        "\\section{Parent A}\n"
        "\\subsection{Valid A}\nBody.\n"
        "\\section*{Unnumbered Parent}\n"
        "\\subsection{Invalid Unit}\nBody.\n"
        "\\section{Parent B}\n"
        "\\subsection{Valid B}\nBody.\n"
        "\\subsection*{Unnumbered Unit}\nBody.\n"
        "\\subsection{Valid C}\nBody.\n",
        encoding="utf-8",
    )
    starred_parent_doc = assemble(starred_parent)
    starred_parent_units = build_subsection_units(
        starred_parent_doc,
        get_parser(str(starred_parent)),
    )
    assert [unit.subsection_id for unit in starred_parent_units] == [
        "1.1.1",
        "1.2.1",
        "1.2.2",
    ]


def test_parent_lead_starts_at_real_parent_and_stops_before_starred_child(
    tmp_path: Path,
) -> None:
    source = tmp_path / "parent-lead.tex"
    source.write_text(
        "\\chapter{根标题}\n"
        "\\section{前一父节}\n"
        "\\subsection{前一单元}\n"
        "前一单元包含足够多的中文正文字符，用于形成跨父节窗口中的上一小节证据。\n\n"
        "\\section{真实父标题}\n"
        "父节导语包含足够多的中文正文字符，用于形成跨父节窗口中的父级只读证据。\n\n"
        "\\subsection*{无编号子标题}\n"
        "这段无编号子标题正文同样足够长，但绝对不能被纳入真实父标题的导语区间。\n\n"
        "\\subsection{当前单元}\n"
        "当前单元包含足够多的中文正文字符，用于形成窗口中的可编辑内容区间。\n",
        encoding="utf-8",
    )
    parser = get_parser(str(source))
    doc = assemble(source)
    units = build_subsection_units(doc, parser)
    assert [unit.subsection_id for unit in units] == ["1.1.1", "1.2.1"]

    paragraphs = _split_context_paragraphs(doc.content, parser)
    window = build_context_window(doc, parser, units, 1, paragraphs, "zh")
    parent_lead = next(part for part in window["read_only"] if part["part"] == "parent_lead")
    assert parent_lead["source_file"] == source.name
    assert (parent_lead["source_start"], parent_lead["source_end"]) == (6, 7)
    source_lines = source.read_text(encoding="utf-8").splitlines()
    assert source_lines[parent_lead["source_start"] - 1] == r"\section{真实父标题}"
    assert "父节导语" in source_lines[parent_lead["source_end"] - 1]
    assert parent_lead["source_end"] < 9


def test_context_eligibility_uses_chinese_threshold_and_english_projection() -> None:
    assert SUBSECTION_CONTEXT_MIN_HAN == 20
    assert SUBSECTION_CONTEXT_MIN_HAN_RATIO == 0.30
    assert SUBSECTION_CONTEXT_MIN_VISIBLE == 60
    base = {
        "start": 1,
        "end": 1,
        "section": "method",
        "in_item": False,
        "ends_with_env": False,
    }
    assert _context_is_eligible(
        ContextParagraph(
            visible="本小节首段包含足够多的中文正文字符，并承担标题之后的入口定位角色。",
            **base,
        ),
        "zh",
    )
    assert not _context_is_eligible(
        ContextParagraph(visible="短段不足二十字。", **base),
        "zh",
    )
    english = ContextParagraph(
        visible=(
            "This opening paragraph contains more than sixty visible characters and "
            "therefore qualifies for an English manuscript window."
        ),
        **base,
    )
    assert _context_is_eligible(english, "en")
    assert not _context_is_eligible(english, "zh")


def test_readonly_bait_fixture_populates_all_three_evidence_parts(tmp_path: Path) -> None:
    workspace = prepare_workspace(
        str(_READONLY_BAIT_FIXTURE),
        output_dir=str(tmp_path / "review-results"),
    )
    layout = WorkspaceLayout(workspace)
    window = json.loads(layout.window_file("1.2.1").read_text(encoding="utf-8"))
    assert [part["part"] for part in window["read_only"]] == [
        "prev.tail",
        "parent_lead",
        "next.head",
    ]

    source_lines = _READONLY_BAIT_FIXTURE.read_text(encoding="utf-8").splitlines()

    def source_text(part: dict[str, object]) -> str:
        start = part["source_start"]
        end = part["source_end"]
        assert isinstance(start, int)
        assert isinstance(end, int)
        return "\n".join(source_lines[start - 1 : end])

    evidence = {part["part"]: source_text(part) for part in window["read_only"]}
    assert "句子句子" in evidence["prev.tail"]
    assert "导语非常非常" in evidence["parent_lead"]
    assert "后继句子句子" in evidence["next.head"]
    assert "句子句子" not in source_text(window["editable"])
