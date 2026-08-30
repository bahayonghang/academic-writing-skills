"""Regression coverage for the opt-in subsection-context checks."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "analyze_logic.py"
_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
_PROJECT_FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "subsection-context" / "main.tex"
_ARTICLE_FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "subsection-context-article.tex"
_NO_DEPTH3_FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "thesis-project" / "main.tex"
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
EXPECTED_ARTICLE_IDS = ["1.1.1", "1.1.2"]


def _load_zh_logic():
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location("zh_subsection_context", _SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


logic: Any = _load_zh_logic()


def _cursor(tmp_path: Path, content: str, *, first_chapter: int | None = None):
    tex = tmp_path / "case.tex"
    tex.write_text(content, encoding="utf-8")
    doc = logic.assemble(tex)
    parser = logic.get_parser(tex)
    return logic._build_subsection_cursor(
        doc,
        parser,
        parser.split_sections(doc.content),
        first_chapter,
    )


def _fixture_state(path: Path):
    doc = logic.assemble(path)
    logic._DOC = doc
    parser = logic.get_parser(path)
    sections = parser.split_sections(doc.content)
    units = logic._build_subsection_cursor(doc, parser, sections)
    paragraphs = logic._split_arc_paragraphs(doc.content, parser, sections)
    windows = [logic._build_context_window(units, index, paragraphs) for index in range(len(units))]
    return doc, parser, units, paragraphs, windows


def _paragraph(
    visible: str,
    *,
    start: int = 1,
    is_heading_lead: bool = True,
    in_item: bool = False,
    ends_with_env: bool = False,
):
    return logic.ArcParagraph(
        start=start,
        end=start,
        visible=visible,
        raw=visible,
        sentences=logic._arc_sentences(visible),
        section="method",
        segment_id=1,
        is_heading_lead=is_heading_lead,
        in_item=in_item,
        ends_with_env=ends_with_env,
    )


def test_loader_targets_zh_copy_and_exports_subsection_contract() -> None:
    assert logic.__file__ is not None
    assert Path(logic.__file__).resolve() == _SCRIPT.resolve()
    assert logic.SUBSECTION_CONTEXT_MIN_HAN == 20
    assert logic.SUBSECTION_CONTEXT_MIN_HAN_RATIO == 0.30


def test_cursor_numbers_book_depth_three_and_honors_first_chapter(tmp_path: Path) -> None:
    content = (
        "\\chapter{方法}\n"
        "\\section{父节}\n"
        "\\subsection{单元甲}\n正文。\n"
        "\\subsection{单元乙}\n正文。\n"
    )
    assert [unit.subsection_id for unit in _cursor(tmp_path, content)] == ["1.1.1", "1.1.2"]
    assert [unit.subsection_id for unit in _cursor(tmp_path, content, first_chapter=2)] == [
        "2.1.1",
        "2.1.2",
    ]


def test_cursor_uses_depth_not_latex_command_for_article(tmp_path: Path) -> None:
    content = (
        "\\section{方法}\n"
        "\\subsection{父节}\n"
        "\\subsubsection{单元甲}\n正文。\n"
        "\\subsubsection{单元乙}\n正文。\n"
    )
    units = _cursor(tmp_path, content)
    assert [unit.subsection_id for unit in units] == ["1.1.1", "1.1.2"]
    assert all(unit.depth == 3 for unit in units)


def test_cursor_skips_starred_parent_and_does_not_fall_back(tmp_path: Path) -> None:
    starred = (
        "\\chapter{方法}\n"
        "\\section*{不编号父节}\n"
        "\\subsection{不得编号的单元}\n正文。\n"
        "\\section{编号父节}\n"
        "\\subsection{合法单元}\n正文。\n"
    )
    assert [unit.subsection_id for unit in _cursor(tmp_path, starred)] == ["1.1.1"]

    no_depth_three = "\\chapter{方法}\n\\section{只有二级标题}\n正文。\n"
    assert _cursor(tmp_path, no_depth_three) == []


def test_cursor_does_not_reuse_numbering_below_starred_root(tmp_path: Path) -> None:
    content = (
        "\\chapter{编号章}\n"
        "\\section{编号父节}\n"
        "\\subsection{合法单元}\n正文。\n"
        "\\chapter*{无编号根标题}\n"
        "\\section{根标题下的父节}\n"
        "\\subsection{不得归入前章的单元}\n正文。\n"
    )
    assert [unit.subsection_id for unit in _cursor(tmp_path, content)] == ["1.1.1"]

    only_starred_root = (
        "\\chapter*{无编号根标题}\n"
        "\\section{根标题下的父节}\n"
        "\\subsection{不得形成编号单元}\n正文。\n"
    )
    tex = tmp_path / "starred-root.tex"
    tex.write_text(only_starred_root, encoding="utf-8")
    report = logic.analyze(tex, subsection_context=True)
    assert logic.SUBSECTION_CONTEXT_NO_DEPTH3 in report
    assert not any("[Script] S-CTX-" in line for line in report)


def test_committed_fixtures_lock_numbering_and_multifile_sources() -> None:
    _doc, _parser, project_units, _paragraphs, _windows = _fixture_state(_PROJECT_FIXTURE)
    assert [unit.subsection_id for unit in project_units] == EXPECTED_PROJECT_IDS
    assert project_units[0].source_file == "chapters/method-a.tex"
    assert project_units[-1].source_file == "chapters/method-b.tex"

    _doc, _parser, article_units, _paragraphs, _windows = _fixture_state(_ARTICLE_FIXTURE)
    assert [unit.subsection_id for unit in article_units] == EXPECTED_ARTICLE_IDS
    assert all(unit.depth == 3 for unit in article_units)


def test_no_depth_three_declares_without_fallback() -> None:
    report = logic.analyze(_NO_DEPTH3_FIXTURE, subsection_context=True)
    assert logic.SUBSECTION_CONTEXT_NO_DEPTH3 in report
    assert not any("[Script] S-CTX-" in line for line in report)


def test_context_eligibility_keeps_heading_lead_and_rejects_boundaries() -> None:
    eligible = _paragraph("本小节首段包含足够多的中文正文字符，并承担标题之后的入口定位角色。")
    assert logic._ctx_is_eligible(eligible)
    assert not logic._ctx_is_eligible(_paragraph("短段不足二十字。"))
    assert not logic._ctx_is_eligible(
        _paragraph(eligible.visible, in_item=True, is_heading_lead=False)
    )
    assert not logic._ctx_is_eligible(
        _paragraph(eligible.visible, ends_with_env=True, is_heading_lead=False)
    )


def test_window_statuses_cover_single_short_list_and_cross_parent() -> None:
    _doc, _parser, units, _paragraphs, windows = _fixture_state(_PROJECT_FIXTURE)
    by_id = dict(zip((unit.subsection_id for unit in units), windows, strict=True))
    assert by_id["1.4.1"]["current_lead_status"] == "ok"
    assert by_id["1.4.2"]["current_lead_status"] == "no_eligible_paragraph"
    assert by_id["1.4.3"]["current_lead_status"] == "no_eligible_paragraph"
    assert by_id["1.2.1"]["same_parent"] == {"prev": False, "next": True}
    parent_lead = next(
        part for part in by_id["1.2.1"]["read_only"] if part["part"] == "parent_lead"
    )
    assert parent_lead["source_file"] == "chapters/method-a.tex"
    assert (parent_lead["source_start"], parent_lead["source_end"]) == (12, 13)

    terms = logic._load_subsection_context_terms(SCRIPT_DIR_ZH)
    for subsection_id in ("1.4.2", "1.4.3"):
        unit = next(unit for unit in units if unit.subsection_id == subsection_id)
        report = "\n".join(logic._check_subsection_context([unit], [by_id[subsection_id]], terms))
        assert "[Script] S-CTX-" not in report
    single = next(unit for unit in units if unit.subsection_id == "1.4.1")
    single_report = "\n".join(logic._check_subsection_context([single], [by_id["1.4.1"]], terms))
    assert "[Script] S-CTX-OUT " not in single_report


def test_three_codes_hit_and_clean_article_unit_does_not_hit() -> None:
    project = logic.analyze(_PROJECT_FIXTURE, subsection_context=True)
    joined = "\n".join(project)
    for code in ("S-CTX-IN", "S-CTX-OUT", "S-CTX-ROLE"):
        assert f"[Script] {code} " in joined

    clean = "\n".join(logic.analyze(_ARTICLE_FIXTURE, subsection_context=True, subsection="1.1.2"))
    assert "[Script] S-CTX-IN " not in clean
    assert "[Script] S-CTX-OUT " not in clean
    assert "[Script] S-CTX-ROLE " not in clean
    assert "S-CTX-" + "DUP" not in _SCRIPT.read_text(encoding="utf-8")


def test_context_sides_and_three_unit_escalation_boundary() -> None:
    _doc, _parser, units, _paragraphs, windows = _fixture_state(_PROJECT_FIXTURE)
    by_id = {
        unit.subsection_id: (unit, window) for unit, window in zip(units, windows, strict=True)
    }
    terms = logic._load_subsection_context_terms(SCRIPT_DIR_ZH)

    cross_unit, cross_window = by_id["1.2.1"]
    cross = "\n".join(logic._check_subsection_context([cross_unit], [cross_window], terms))
    assert 'context_sides: ["current", "parent_lead"]' in cross

    same_unit, same_window = by_id["1.2.2"]
    same = "\n".join(logic._check_subsection_context([same_unit], [same_window], terms))
    assert 'context_sides: ["current", "prev.tail"]' in same

    two_pairs = [by_id[key] for key in ("1.2.1", "1.2.2")]
    two = "\n".join(
        logic._check_subsection_context(
            [pair[0] for pair in two_pairs], [pair[1] for pair in two_pairs], terms
        )
    )
    assert "[Script] S-CTX-IN+OUT" not in two

    three_pairs = [by_id[key] for key in ("1.2.1", "1.2.2", "1.2.3")]
    three = "\n".join(
        logic._check_subsection_context(
            [pair[0] for pair in three_pairs], [pair[1] for pair in three_pairs], terms
        )
    )
    assert three.count("[Script] S-CTX-IN+OUT") == 1
    assert "[Severity: Minor] [Priority: P2]" in three


def test_emit_window_has_source_coordinates_without_prose() -> None:
    report = logic.analyze(_PROJECT_FIXTURE, subsection="1.2.1", emit_window=True)
    joined = "\n".join(report)
    coordinate_lines = [line for line in report if "[可改]" in line or "[只读]" in line]
    assert coordinate_lines
    assert all("chapters/method-a.tex L" in line for line in coordinate_lines)

    doc = logic.assemble(_PROJECT_FIXTURE)
    parser = logic.get_parser(_PROJECT_FIXTURE)
    visible_lines = (parser.extract_visible_text(line).strip() for line in doc.lines)
    prose_windows = {
        visible[index : index + 20]
        for visible in visible_lines
        for index in range(max(len(visible) - 19, 0))
    }
    assert prose_windows
    assert not any(window in joined for window in prose_windows)


def test_emit_window_requires_subsection_on_cli() -> None:
    result = subprocess.run(
        [sys.executable, str(_SCRIPT), str(_PROJECT_FIXTURE), "--emit-window"],
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert b"--emit-window" in result.stderr
    assert b"--subsection" in result.stderr


def test_subsection_term_loader_falls_back_per_field(tmp_path: Path) -> None:
    script_dir = tmp_path / "scripts"
    script_dir.mkdir()
    defaults = logic.DEFAULT_SUBSECTION_CONTEXT_TERMS
    assert logic._load_subsection_context_terms(script_dir) == defaults

    terms_dir = tmp_path / "references" / "writing"
    terms_dir.mkdir(parents=True)
    terms_path = terms_dir / logic.SUBSECTION_CONTEXT_TERMS_FILENAME
    terms_path.write_text("inbound:\n  - 自定义承接\n", encoding="utf-8")
    loaded = logic._load_subsection_context_terms(script_dir)
    assert loaded["inbound"] == ("自定义承接",)
    assert loaded["outbound"] == defaults["outbound"]

    terms_path.write_text(
        "inbound: 非法字符串\noutbound:\n  - 自定义交棒\nlocating: []\n",
        encoding="utf-8",
    )
    loaded = logic._load_subsection_context_terms(script_dir)
    assert loaded["inbound"] == defaults["inbound"]
    assert loaded["outbound"] == ("自定义交棒",)
    assert loaded["locating"] == defaults["locating"]


def test_public_reference_locks_three_code_contract_and_live_terms() -> None:
    reference = (_SKILL_DIR / "references" / "writing" / "subsection-context-zh.md").read_text(
        encoding="utf-8"
    )
    block = reference.split("<!-- S-CTX-CONTRACT:BEGIN -->", 1)[1].split(
        "<!-- S-CTX-CONTRACT:END -->", 1
    )[0]
    for code in ("S-CTX-IN", "S-CTX-OUT", "S-CTX-ROLE"):
        assert code in block
    assert "S-CTX-" + "DUP" not in block
    assert "depth = level - root_level + 1" in block
    assert "无 depth-3 不回退" in block
    assert (
        "只有 current 可产出改写建议；prev.tail、next.head、parent_lead 一律只读，仅作证据。"
    ) in block
    assert logic._load_subsection_context_terms(SCRIPT_DIR_ZH) == (
        logic.DEFAULT_SUBSECTION_CONTEXT_TERMS
    )
