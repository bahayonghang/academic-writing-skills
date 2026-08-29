"""Regression coverage for the opt-in latex-paper-en paragraph-arc diagnostic."""

from __future__ import annotations

from pathlib import Path

import analyze_logic as logic
import pytest
import yaml

from tests.support.paths import SCRIPT_DIR_EN, SKILLS_ROOT, TESTS_ROOT

_FIXTURE_DIR = TESTS_ROOT / "fixtures" / "paragraph_arc_en"
_SKILL_DIR = SKILLS_ROOT / "latex-paper-en"

GOOD_FIRST = (
    "The asynchronous observation window is the central constraint governing this paragraph's "
    "argument."
)
MIDDLE = (
    "The evaluation retains channel timestamps, records missing observations, compares aligned "
    "representations, and reports the operating conditions that bound each resulting estimate "
    "while preserving every documented sensor identity and validation decision for later review."
)
GOOD_CLOSE = "Taken together, these observations establish the interface required for the following analysis."
PLAIN_CLOSE = "The encoder passes the resulting representation to a fixed prediction head for online estimation."
WEAK_FIRST = "One difficult setting."


def _write_tex(tmp_path: Path, body: str, *, section: str = "Introduction") -> Path:
    tex = tmp_path / "case.tex"
    tex.write_text(f"\\section{{{section}}}\n{body}\n", encoding="utf-8")
    return tex


def _arc_headers(report: list[str], code: str | None = None) -> list[str]:
    headers = [line for line in report if "[Script] P-ARC-" in line]
    return [line for line in headers if code in line] if code else headers


def _paragraph(
    first: str,
    last: str,
    *,
    start: int = 10,
    section: str = "introduction",
    segment_id: int = 1,
) -> logic.ArcParagraph:
    return logic.ArcParagraph(
        start=start,
        end=start + 1,
        visible=f"{first} {last}",
        raw=f"{first} {last}",
        sentences=(first, last),
        section=section,
        segment_id=segment_id,
        in_item=False,
        ends_with_env=False,
    )


def _weak_paragraph() -> str:
    return f"{WEAK_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"


def test_loader_targets_en_copy_and_exports_arc_contract() -> None:
    assert logic.__file__ is not None
    assert Path(logic.__file__).resolve() == (SCRIPT_DIR_EN / "analyze_logic.py").resolve()
    assert logic.PARAGRAPH_ARC_MIN_WORDS == 40
    assert logic.PARAGRAPH_ARC_DOUBLE_MISSING_RUN == 2
    assert logic.PARAGRAPH_ARC_LINK_THRESHOLD == 0.0200


def test_default_output_is_byte_identical_to_pre_change_baseline() -> None:
    sample = _FIXTURE_DIR / "baseline-sample.tex"
    expected = (_FIXTURE_DIR / "baseline-before.txt").read_bytes()
    actual = ("\n".join(logic.analyze(sample, "introduction")) + "\n").encode("utf-8")
    assert actual == expected
    assert b"P-ARC-" not in actual


def test_controlled_fixture_exercises_all_four_synthetic_findings() -> None:
    fixture = _FIXTURE_DIR / "controlled-sample.tex"
    source = fixture.read_text(encoding="utf-8")
    for marker in (
        r"\section{Introduction}",
        r"\section{Related Work}",
        r"\section{Methods}",
        r"\begin{equation}",
        r"\begin{itemize}",
    ):
        assert marker in source

    report = logic.analyze(
        fixture,
        "introduction",
        paragraph_arc=True,
    )
    headers = "\n".join(_arc_headers(report))
    for code in ("P-ARC-LEAD", "P-ARC-CLOSE", "P-ARC-LINK", "P-ARC-FLAT"):
        assert code in headers


def test_lead_and_close_findings_are_independent_and_located(tmp_path: Path) -> None:
    weak_lead = f"{WEAK_FIRST}\n{MIDDLE}\n{GOOD_CLOSE}"
    missing_close = f"{GOOD_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"
    tex = _write_tex(tmp_path, f"{weak_lead}\n\n{missing_close}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    lead = _arc_headers(report, "P-ARC-LEAD")
    close = _arc_headers(report, "P-ARC-CLOSE")
    assert len(lead) == 1 and "Line 2" in lead[0]
    assert len(close) == 1 and "Line 8" in close[0]


def test_sentence_locations_ignore_standalone_label_lines(tmp_path: Path) -> None:
    body = f"\\label{{par:arc-location}}\n{WEAK_FIRST}\n{MIDDLE}\n{GOOD_CLOSE}\n\\ref{{sec:next}}"
    tex = _write_tex(tmp_path, body)
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    lead = _arc_headers(report, "P-ARC-LEAD")
    assert len(lead) == 1 and "Line 3" in lead[0]


def test_heading_first_paragraph_participates_and_heading_resets_link(tmp_path: Path) -> None:
    first = _weak_paragraph()
    second = f"{GOOD_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"
    tex = _write_tex(tmp_path, f"{first}\n\n\\subsection{{Boundary}}\n{second}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert _arc_headers(report, "P-ARC-LEAD")
    assert not _arc_headers(report, "P-ARC-LINK")


def test_clean_lead_and_close_emit_no_corresponding_findings(tmp_path: Path) -> None:
    tex = _write_tex(tmp_path, f"{GOOD_FIRST}\n{MIDDLE}\n{GOOD_CLOSE}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LEAD")
    assert not _arc_headers(report, "P-ARC-CLOSE")
    assert not _arc_headers(report, "P-ARC-FLAT")


@pytest.mark.parametrize(
    "environment",
    ["equation", "alignat", "figure", "table", "longtable", "algorithm", "itemize", "description"],
)
def test_link_never_crosses_protected_environment(tmp_path: Path, environment: str) -> None:
    left = f"{GOOD_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"
    right = (
        "A separate calibration stream is the main source of evidence for this comparison.\n"
        f"{MIDDLE}\n{PLAIN_CLOSE}"
    )
    protected = (
        "\\begin{itemize}\n\\item protected content\n\\end{itemize}"
        if environment == "itemize"
        else f"\\begin{{{environment}}}\nprotected content\n\\end{{{environment}}}"
    )
    tex = _write_tex(tmp_path, f"{left}\n{protected}\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


@pytest.mark.parametrize("environment", sorted(logic._ARC_PROTECTED_ENVS))
def test_protected_environment_content_never_emits_arc_findings(
    tmp_path: Path, environment: str
) -> None:
    content = _weak_paragraph()
    if environment in {"itemize", "enumerate", "description"}:
        content = f"\\item {content}"
    tex = _write_tex(
        tmp_path,
        f"\\begin{{{environment}}}\n{content}\n\\end{{{environment}}}",
    )
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_original_adjacency_is_not_rebuilt_across_short_paragraph(tmp_path: Path) -> None:
    left = f"{GOOD_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"
    short = "A short paragraph stays outside this diagnostic."
    right = (
        "A separate calibration stream is the main source of evidence for this comparison.\n"
        f"{MIDDLE}\n{PLAIN_CLOSE}"
    )
    tex = _write_tex(tmp_path, f"{left}\n\n{short}\n\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


def test_dedicated_sections_are_exempt_but_intro_heading_lead_is_not() -> None:
    paragraph = _weak_paragraph()
    content = (
        f"\\begin{{abstract}}\n{paragraph}\n\\end{{abstract}}\n"
        f"\\section{{Introduction}}\n{paragraph}\n"
        f"\\section{{Conclusion}}\n{paragraph}\n"
        f"\\section*{{Acknowledgments}}\n{paragraph}\n"
        f"\\appendix\n\\section{{Appendix A}}\n{paragraph}\n"
    )
    parser = logic.get_parser(Path("case.tex"))
    sections = parser.split_sections(content)
    paragraphs = logic._split_arc_paragraphs(content, parser, sections)
    eligible = [paragraph for paragraph in paragraphs if logic._arc_is_eligible(paragraph)]
    assert len(eligible) == 1 and eligible[0].section == "introduction"


def test_top_level_ownership_resumes_after_recognized_child_section() -> None:
    content = (
        "\\section{Introduction}\n"
        f"{GOOD_FIRST} {MIDDLE} {PLAIN_CLOSE}\n"
        "\\subsection{Paper Roadmap}\n"
        f"{GOOD_FIRST} {MIDDLE} {PLAIN_CLOSE}\n"
        "\\subsection{Research Question}\n"
        f"{WEAK_FIRST} {MIDDLE} {PLAIN_CLOSE}\n"
    )
    parser = logic.get_parser(Path("case.tex"))
    sections = parser.split_sections(content)
    paragraphs = logic._split_arc_paragraphs(content, parser, sections)
    target = paragraphs[-1]
    assert target.section == "introduction"
    assert logic._arc_is_eligible(target)


@pytest.mark.parametrize(
    "display_math",
    ["\\[\nE = mc^2\n\\]", "$$\nE = mc^2\n$$"],
)
def test_link_never_crosses_display_math(tmp_path: Path, display_math: str) -> None:
    left = f"{GOOD_FIRST}\n{MIDDLE}\n{PLAIN_CLOSE}"
    right = (
        "A separate calibration stream is the main source of evidence for this comparison.\n"
        f"{MIDDLE}\n{PLAIN_CLOSE}"
    )
    tex = _write_tex(tmp_path, f"{left}\n{display_math}\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


def test_link_explicit_marker_and_overlap_are_pass_paths() -> None:
    terms = logic.DEFAULT_PARAGRAPH_ARC_TERMS
    left = _paragraph(
        GOOD_FIRST, "The calibration interface retains shared process context for evaluation."
    )
    explicit = _paragraph(
        "However, a separate calibration interface retains enough context for evaluation.",
        PLAIN_CLOSE,
        start=20,
    )
    overlap = _paragraph(
        "The calibration interface retains shared process context for downstream evaluation.",
        PLAIN_CLOSE,
        start=30,
    )
    assert logic._arc_link_missing(left, explicit, terms) == (False, None)
    missing, score = logic._arc_link_missing(left, overlap, terms)
    assert missing is False and score is not None and score >= 0.0200


def test_link_rounding_empty_sets_and_strict_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    terms = logic.DEFAULT_PARAGRAPH_ARC_TERMS
    left_sentinel = "Left endpoint words remain long enough for exact boundary calculation here."
    right_sentinel = "Right endpoint words remain long enough for exact boundary calculation here."
    left = _paragraph(GOOD_FIRST, left_sentinel)
    right = _paragraph(right_sentinel, PLAIN_CLOSE, start=20)

    exact_left = {"common", *(f"left{i}" for i in range(24))}
    exact_right = {"common", *(f"right{i}" for i in range(25))}
    monkeypatch.setattr(
        logic,
        "_thread_tokens",
        lambda text: exact_left if text == left_sentinel else exact_right,
    )
    assert logic._arc_link_missing(left, right, terms) == (False, 0.0200)

    below_right = {"common", *(f"right{i}" for i in range(26))}
    monkeypatch.setattr(
        logic,
        "_thread_tokens",
        lambda text: exact_left if text == left_sentinel else below_right,
    )
    assert logic._arc_link_missing(left, right, terms) == (True, 0.0196)

    monkeypatch.setattr(logic, "_thread_tokens", lambda _text: set())
    assert logic._arc_link_missing(left, right, terms) == (True, 0.0)


def test_flat_single_sentence_and_author_enumeration_paths(tmp_path: Path) -> None:
    single = " ".join(["Evidence"] + ["supports the bounded operating condition"] * 10) + "."
    enumeration = (
        "Smith (2020) proposed a calibrated estimator that retained asynchronous timestamps and "
        "reported bounded errors across repeated operating trials with documented sensor identities "
        "and validation decisions. "
        "Jones (2021) developed a separate encoder that preserved channel identities and compared "
        "prediction errors under matched evaluation conditions across repeated production campaigns "
        "and independent operating periods."
    )
    tex = _write_tex(tmp_path, f"{single}\n\n{enumeration}", section="Methods")
    report = logic.analyze(tex, paragraph_arc=True)
    assert len(_arc_headers(report, "P-ARC-FLAT")) == 2

    related = _write_tex(tmp_path, enumeration, section="Related Work")
    related_report = logic.analyze(related, "related", paragraph_arc=True)
    assert not _arc_headers(related_report, "P-ARC-FLAT")


def test_two_consecutive_double_missing_paragraphs_upgrade_once(tmp_path: Path) -> None:
    paragraph = _weak_paragraph()
    tex = _write_tex(tmp_path, f"{paragraph}\n\n{paragraph}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    joined = "\n".join(report)
    assert joined.count("[Severity: Minor] [Priority: P2]: [Script] P-ARC-LEAD+CLOSE") == 1
    assert sum("[Script] P-ARC-LEAD " in line for line in report) == 2
    assert sum("[Script] P-ARC-CLOSE " in line for line in report) == 2


@pytest.mark.parametrize(
    "barrier",
    [
        "A short paragraph stays outside this diagnostic.",
        "\\subsection{New boundary}",
        "\\begin{equation}\ny=f(x)\n\\end{equation}",
        "\\begin{itemize}\n\\item protected item\n\\end{itemize}",
    ],
)
def test_double_missing_run_resets_at_ineligible_or_segment_boundary(
    tmp_path: Path, barrier: str
) -> None:
    paragraph = _weak_paragraph()
    tex = _write_tex(tmp_path, f"{paragraph}\n\n{barrier}\n\n{paragraph}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LEAD+CLOSE")


def test_list_items_never_emit_paragraph_arc_findings(tmp_path: Path) -> None:
    item = _weak_paragraph()
    tex = _write_tex(
        tmp_path,
        f"\\begin{{itemize}}\n\\item {item}\n\\item {item}\n\\end{{itemize}}",
    )
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_standalone_item_commands_are_hard_boundaries(tmp_path: Path) -> None:
    item = _weak_paragraph()
    tex = _write_tex(tmp_path, f"\\item {item}\n\\item {item}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_section_scope_excludes_other_sections(tmp_path: Path) -> None:
    intro = f"{GOOD_FIRST}\n{MIDDLE}\n{GOOD_CLOSE}"
    content = f"\\section{{Introduction}}\n{intro}\n\\section{{Methods}}\n{_weak_paragraph()}\n"
    tex = tmp_path / "case.tex"
    tex.write_text(content, encoding="utf-8")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_every_arc_finding_has_script_and_meaning_check(tmp_path: Path) -> None:
    tex = _write_tex(tmp_path, _weak_paragraph())
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert _arc_headers(report)
    for index, line in enumerate(report):
        if "[Script] P-ARC-" in line:
            assert "% Meaning-Check: NEEDS-LLM" in report[index + 1 : index + 6]


def test_yaml_defaults_and_neutral_docs_copies_match() -> None:
    source = _SKILL_DIR / "references" / "writing" / "paragraph-arc-terms.yaml"
    configured = yaml.safe_load(source.read_text(encoding="utf-8"))
    assert set(configured) == set(logic.DEFAULT_PARAGRAPH_ARC_TERMS)
    for key, values in logic.DEFAULT_PARAGRAPH_ARC_TERMS.items():
        assert configured[key] == list(values)

    repo_root = SKILLS_ROOT.parent
    for locale in ("skills", "zh/skills"):
        mirror = (
            repo_root
            / "docs"
            / locale
            / "latex-paper-en"
            / "resources"
            / "references"
            / "writing"
            / source.name
        )
        assert mirror.read_bytes() == source.read_bytes()


def test_terms_loader_falls_back_per_invalid_field(tmp_path: Path) -> None:
    script_dir = tmp_path / "scripts"
    script_dir.mkdir()
    assert logic._load_paragraph_arc_terms(script_dir) == logic.DEFAULT_PARAGRAPH_ARC_TERMS

    terms_dir = tmp_path / "references" / "writing"
    terms_dir.mkdir(parents=True)
    (terms_dir / logic.PARAGRAPH_ARC_TERMS_FILENAME).write_text(
        "judgment_predicates: invalid\n"
        "prospective_patterns:\n"
        "  - '[invalid'\n"
        "explicit_link_patterns:\n" + r"  - '^Custom link\b'" + "\n",
        encoding="utf-8",
    )
    loaded = logic._load_paragraph_arc_terms(script_dir)
    assert loaded["judgment_predicates"] == logic.DEFAULT_PARAGRAPH_ARC_TERMS["judgment_predicates"]
    assert (
        loaded["prospective_patterns"] == logic.DEFAULT_PARAGRAPH_ARC_TERMS["prospective_patterns"]
    )
    assert loaded["explicit_link_patterns"] == (r"^Custom link\b",)


def test_logic_remains_outside_rewrite_contract() -> None:
    routing = (_SKILL_DIR / "references" / "modules" / "routing-rules.md").read_text(
        encoding="utf-8"
    )
    assert "`logic`, `literature`" in routing
    arc_route = routing.split("--paragraph-arc", maxsplit=1)[1][:450]
    assert "no rewrite contract" in arc_route
