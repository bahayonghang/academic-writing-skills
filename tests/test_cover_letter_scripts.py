"""Unit tests for cover-letter scripts.

Cover-letter scripts vendor parsers.py (and tex_loader.py) from latex-paper-en.
The other skills' tests may have already cached a ``parsers`` / ``tex_loader``
module from a different copy, so ``_load`` evicts those shared names before
executing a cover-letter script — forcing its ``from parsers import ...`` to
re-resolve against the cover-letter directory it puts at ``sys.path[0]`` — and
restores both ``sys.path`` and the evicted modules afterward.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from types import ModuleType

import pytest
from conftest import SCRIPT_DIR_COVER_LETTER

SKILL_ROOT = SCRIPT_DIR_COVER_LETTER.parent
FIXTURES = SKILL_ROOT / "evals" / "fixtures"

# Shared module names other skills also vendor; evicted around each load so the
# cover-letter copy wins, then restored so later EN/AUDIT tests are unaffected.
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load(module_name: str) -> ModuleType:
    """Load a cover-letter script by basename (no .py), isolated from other
    skills' cached ``parsers`` / ``tex_loader`` modules."""
    path = SCRIPT_DIR_COVER_LETTER / f"{module_name}.py"
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_COVER_LETTER))
        spec = importlib.util.spec_from_file_location(f"_cl_{module_name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved_modules.items():
            if mod is not None:
                sys.modules[name] = mod
            else:
                sys.modules.pop(name, None)


def test_parsers_latex_extract_visible_text_preserves_citations() -> None:
    parsers = _load("parsers")
    parser = parsers.LatexParser()
    visible = parser.extract_visible_text(r"Our work \cite{wei2024} shows X.")
    assert "Our work" in visible
    assert "shows X" in visible
    assert "\\cite{wei2024}" not in visible  # citation stripped as preserved placeholder


def test_extract_manuscript_facts_returns_expected_shape() -> None:
    extract = _load("extract_manuscript_facts")
    text = (FIXTURES / "generate_fixture.tex").read_text(encoding="utf-8")
    facts = extract.extract_facts(text)
    assert facts["title"].startswith("Adaptive Latency-Aware Inference")
    assert facts["abstract"].startswith("We address the problem of anomaly")
    assert "Jia Wei" in facts["authors"]
    assert facts["corresponding_author"] == "Jia Wei"
    assert len(facts["contributions"]) >= 1
    assert any("47" in n for n in facts["headline_numbers"])


def test_extract_manuscript_facts_drops_latex_command_authors() -> None:
    extract = _load("extract_manuscript_facts")
    text = (FIXTURES / "generate_fixture.tex").read_text(encoding="utf-8")
    facts = extract.extract_facts(text)
    for author in facts["authors"]:
        assert "\\" not in author
        assert "{" not in author


def test_extract_manuscript_facts_handles_thanks_author_block() -> None:
    """NeurIPS-style \\author{Name\\thanks{...} \\\\ Affil \\And Name2} extracts
    real authors only (no affiliation leak) and no fabricated corresponding."""
    extract = _load("extract_manuscript_facts")
    text = (FIXTURES / "thanks_author_fixture.tex").read_text(encoding="utf-8")
    facts = extract.extract_facts(text)
    assert facts["authors"] == ["David S. Hippocampus", "Elias D. Striatum"]
    # No \corresponding command in the source → falls back to the first author,
    # never an email local part scraped out of \thanks.
    assert facts["corresponding_author"] == "David S. Hippocampus"
    assert "@" not in facts["corresponding_author"]


def test_extract_title_strips_thanks_and_keeps_nested_braces() -> None:
    """A \\title with a nested-brace command and a \\thanks funding statement
    yields the full clean title with no funding text."""
    extract = _load("extract_manuscript_facts")
    text = (FIXTURES / "thanks_author_fixture.tex").read_text(encoding="utf-8")
    facts = extract.extract_facts(text)
    assert facts["title"] == "Adaptive Latency-Aware Inference for Streaming Detection"
    assert "NSF" not in facts["title"]
    assert "supported" not in facts["title"]


def test_extract_corresponding_author_never_scrapes_thanks_email() -> None:
    """\\author{A\\thanks{Corresponding author: a@u.edu} \\and B} must not report
    the email local part as the corresponding author (regression for C1)."""
    extract = _load("extract_manuscript_facts")
    text = (
        r"\title{Streaming Detection}"
        r"\author{Alice Smith\thanks{Corresponding author: alice.smith@uni.edu} \and Bob Jones}"
        r"\begin{abstract}We study streaming detection.\end{abstract}"
    )
    facts = extract.extract_facts(text)
    assert facts["authors"] == ["Alice Smith", "Bob Jones"]
    assert facts["corresponding_author"] == "Alice Smith"


def test_presubmission_detects_opener_cliche_and_banned_phrases() -> None:
    presub = _load("presubmission_check")
    letter = FIXTURES / "optimize_fixture_letter.md"
    issues = presub.run_checks(letter, journal="ieee-trans", skill_dir=SKILL_ROOT)
    codes = {issue.code for issue in issues}
    assert any(code.startswith("L2") for code in codes), "opener cliché not detected"
    assert any(code.startswith("J1") for code in codes), "banned phrases not detected"


def test_presubmission_detects_missing_required_declarations() -> None:
    presub = _load("presubmission_check")
    letter = FIXTURES / "journal_fit_fixture_letter.md"  # missing COI + data availability
    issues = presub.run_checks(letter, journal="nature", skill_dir=SKILL_ROOT)
    decl_codes = [issue.code for issue in issues if issue.code.startswith("D-")]
    assert any("competing_interests" in code for code in decl_codes)


def test_presubmission_journal_conditional_no_irb_for_neurips() -> None:
    presub = _load("presubmission_check")
    letter = FIXTURES / "journal_fit_fixture_letter.md"
    issues = presub.run_checks(letter, journal="neurips", skill_dir=SKILL_ROOT)
    # NeurIPS template does not require ethics_irb, so no major D-ethics_irb finding.
    irb_required = [
        issue for issue in issues if issue.code == "D-ethics_irb" and issue.severity == "major"
    ]
    assert not irb_required, "NeurIPS template should not require IRB declaration"


def test_journal_fit_classifies_low_for_underframed_nature() -> None:
    jf = _load("journal_fit_check")
    letter = FIXTURES / "journal_fit_fixture_letter.md"
    result = jf.run_journal_fit(letter, "nature", SKILL_ROOT)
    assert result.overall in {"LOW", "MEDIUM"}
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert "novelty_framing" in axes
    assert axes["novelty_framing"] in {"LOW", "MEDIUM"}


def test_build_letter_claim_map_extracts_claim_sentences() -> None:
    builder = _load("build_letter_claim_map")
    letter_text = (FIXTURES / "align_check_fixture_letter.md").read_text(encoding="utf-8")
    claim_map = builder.build_claim_map(letter_text, manuscript_facts=None)
    assert claim_map["letter_claims"], "expected at least one claim sentence detected"
    assert any(
        "deployed" in c["claim"].lower() or "$1.2m" in c["claim"].lower()
        for c in claim_map["claim_candidates"]
    )


def test_build_letter_claim_map_reports_truncation_above_cap() -> None:
    """More than 12 claim sentences must surface a truncation marker + total
    instead of silently dropping the overflow (C12)."""
    builder = _load("build_letter_claim_map")
    text = " ".join(f"We report finding number {i} on the benchmark." for i in range(20))
    claim_map = builder.build_claim_map(text, manuscript_facts=None)
    assert claim_map["total_claim_sentences"] >= 20
    assert claim_map["truncated"] is True
    assert len(claim_map["claim_candidates"]) == 12


def test_build_letter_claim_map_no_truncation_marker_when_under_cap() -> None:
    builder = _load("build_letter_claim_map")
    text = "We report a strong result. Our method improves the baseline by 5%."
    claim_map = builder.build_claim_map(text, manuscript_facts=None)
    assert claim_map["truncated"] is False
    assert claim_map["total_claim_sentences"] == len(claim_map["claim_candidates"])


def test_build_letter_claim_map_extracts_numeric_unit_claims() -> None:
    builder = _load("build_letter_claim_map")
    text = (
        "The system achieves a 73% reduction in memory footprint. "
        "It is 2.1x faster on WADI-Stream. "
        "The framework supports 12 sensor modalities. "
        "The method saves $1.2M per facility."
    )
    claim_map = builder.build_claim_map(text, manuscript_facts=None)
    claims = [candidate["claim"] for candidate in claim_map["claim_candidates"]]
    assert any("73% reduction" in claim for claim in claims)
    assert any("2.1x faster" in claim for claim in claims)
    assert any("12 sensor modalities" in claim for claim in claims)
    assert any("$1.2M" in claim for claim in claims)


def test_extract_manuscript_facts_captures_extended_headline_numbers() -> None:
    extract = _load("extract_manuscript_facts")
    text = (
        r"\title{Demo}\begin{abstract}We report a 47\% reduction, "
        r"2.1x faster inference, 12 sensor modalities, and $1.2M savings."
        r"\end{abstract}"
    )
    facts = extract.extract_facts(text)
    numbers = facts["headline_numbers"]
    assert any("47%" in number for number in numbers)
    assert any("2.1x" in number for number in numbers)
    assert any("12 sensor modalities" in number for number in numbers)
    assert any("$1.2M" in number for number in numbers)


def test_verify_letter_against_manuscript_flags_overclaim() -> None:
    verifier = _load("verify_letter_against_manuscript")
    builder = _load("build_letter_claim_map")
    extract = _load("extract_manuscript_facts")
    letter_text = (FIXTURES / "align_check_fixture_letter.md").read_text(encoding="utf-8")
    manuscript_text = (FIXTURES / "generate_fixture.tex").read_text(encoding="utf-8")
    facts = extract.extract_facts(manuscript_text)
    claim_map = builder.build_claim_map(letter_text, manuscript_facts=facts)
    verified = verifier.verify_claim_candidates(claim_map["claim_candidates"], manuscript_text)
    # The deployment / cost-savings claim is not in the manuscript.
    deployment_claim = next(
        (c for c in verified if "deployed" in c["claim"].lower()),
        None,
    )
    assert deployment_claim is not None
    assert deployment_claim["claim_strength"] in {"unsupported", "observed"}
    assert deployment_claim["quote_verified"] is False


def test_align_check_cli_exit_code_signals_issues(
    capsys: pytest.CaptureFixture[str],
) -> None:
    align = _load("align_check")
    code = align.main(
        [
            "--letter",
            str(FIXTURES / "align_check_fixture_letter.md"),
            "--manuscript",
            str(FIXTURES / "generate_fixture.tex"),
            "--json",
        ]
    )
    # Some unsupported / observed claims expected → non-zero exit.
    assert code in {1, 2}
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert isinstance(payload, list)
    assert any(issue["comment_type"] == "claim_accuracy" for issue in payload)


def test_journal_fit_cli_json_emits_axes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    jf = _load("journal_fit_check")
    jf.main(
        [
            str(FIXTURES / "journal_fit_fixture_letter.md"),
            "--venue",
            "nature",
            "--json",
        ]
    )
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["venue"] == "Nature"
    assert payload["tier"] == "top-journal"
    assert payload["overall"] in {"HIGH", "MEDIUM", "LOW"}
    axes_names = {axis["axis"] for axis in payload["axes"]}
    assert axes_names == {
        "scope_fit",
        "novelty_framing",
        "evidence_density",
        "format_compliance",
    }
    assert "findings" in payload
    for finding in payload["findings"]:
        assert finding["comment_type"] == "journal_fit"
        assert finding["severity"] in {"major", "moderate", "minor"}
        assert finding["priority"] in {"P1", "P2", "P3"}
        assert finding["source_kind"] == "script"


def test_unified_cover_letter_cli_json_smoke_all_modes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    cli = _load("cover_letter")
    mode_args = {
        "generate": [
            "--mode",
            "generate",
            "--manuscript",
            str(FIXTURES / "generate_fixture.tex"),
            "--journal",
            "generic",
            "--json",
        ],
        "presubmission": [
            "--mode",
            "presubmission",
            "--letter",
            str(FIXTURES / "journal_fit_fixture_letter.md"),
            "--journal",
            "nature",
            "--json",
        ],
        "align-check": [
            "--mode",
            "align-check",
            "--letter",
            str(FIXTURES / "align_check_fixture_letter.md"),
            "--manuscript",
            str(FIXTURES / "generate_fixture.tex"),
            "--json",
        ],
        "journal-fit": [
            "--mode",
            "journal-fit",
            "--letter",
            str(FIXTURES / "journal_fit_fixture_letter.md"),
            "--journal",
            "nature",
            "--json",
        ],
        "optimize": [
            "--mode",
            "optimize",
            "--letter",
            str(FIXTURES / "align_check_fixture_letter.md"),
            "--manuscript",
            str(FIXTURES / "generate_fixture.tex"),
            "--journal",
            "ieee-trans",
            "--json",
        ],
    }
    for mode, args in mode_args.items():
        code = cli.main(args)
        assert code in {0, 1, 2}
        payload = json.loads(capsys.readouterr().out)
        assert payload["mode"] == mode
        assert isinstance(payload.get("findings"), list)


def test_unified_cover_letter_cli_help_lists_mode() -> None:
    cli = _load("cover_letter")
    with pytest.raises(SystemExit) as exc:
        cli.main(["--help"])
    assert exc.value.code == 0


def test_mode_guide_flags_all_exist_in_cli(capsys: pytest.CaptureFixture[str]) -> None:
    """Every --flag named in MODE_GUIDE must be a real cover_letter.py option, and
    the previously-documented ghost flags must be gone (C9)."""
    guide = (SKILL_ROOT / "references" / "MODE_GUIDE.md").read_text(encoding="utf-8")
    for ghost in ("--out-format", "--strict", "--section", "--output"):
        assert ghost not in guide, f"MODE_GUIDE still references ghost flag {ghost}"

    cli = _load("cover_letter")
    parser = cli.build_parser()
    real_flags: set[str] = set()
    for action in parser._actions:
        real_flags.update(action.option_strings)

    guide_flags = set(re.findall(r"(--[a-z][a-z-]*)", guide))
    unknown = guide_flags - real_flags
    assert not unknown, f"MODE_GUIDE flags absent from cover_letter.py: {sorted(unknown)}"


def test_ml_conference_templates_disclaim_cover_letter() -> None:
    """icml / cvpr / neurips templates must state the main track has no cover letter (C6)."""
    templates = SKILL_ROOT / "templates"
    for venue in ("icml", "cvpr", "neurips"):
        text = (templates / f"{venue}.md").read_text(encoding="utf-8").lower()
        assert "cover letter" in text and (
            "does not" in text or "not use" in text or "not strictly" in text
        ), f"{venue}.md should disclaim the main-track cover letter"
