"""Regression coverage for latex-paper-en/scripts/check_claim_forward.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_EN, SKILLS_ROOT

_SCRIPT = SCRIPT_DIR_EN / "check_claim_forward.py"
_FIXTURE = SKILLS_ROOT / "latex-paper-en" / "evals" / "fixtures" / "claim_forward_cases.tex"

import check_claim_forward as cf  # noqa: E402  (SCRIPT_DIR_EN is on sys.path via conftest)


def _findings(path: Path, section: str | None = None):
    findings, errors, _meta = cf.run(path, section)
    return findings, errors


def _write(tmp_path: Path, body: str, *, section: str = "Introduction") -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    tex = tmp_path / "main.tex"
    star = "*" if section == "Limitations" else ""
    heading = r"\section" + star + "{" + section + "}"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n"
        + heading
        + "\n"
        + body
        + "\n\\end{document}\n",
        encoding="utf-8",
    )
    return tex


def test_fixture_hits_each_code_once_and_boundaries_stay_silent() -> None:
    findings, errors = _findings(_FIXTURE)
    assert not errors
    by_code = {code: [f for f in findings if f.code == code] for code in cf.CODES}
    assert {code: len(v) for code, v in by_code.items()} == dict.fromkeys(cf.CODES, 1)
    originals = " ".join(f.original for f in findings)
    # Case F (cited prior work), G (Limitations section), H (bare only/limited) are silent.
    assert "falls short of real-time" not in originals
    assert "suffer from serious drift" not in originals
    assert "does not cover outdoor" not in originals
    assert "only requires a single GPU" not in originals


def test_fixture_severity_and_priority_follow_contract() -> None:
    findings, _ = _findings(_FIXTURE)
    table = {f.code: (f.severity, f.priority) for f in findings}
    assert table["CF-DISCLAIM"] == ("Minor", "P2")  # introduction is high-impact
    assert table["CF-SELFWEAK"] == ("Minor", "P2")
    assert table["CF-CAVEAT-POS"] == ("Info", "P3")
    assert table["CF-HEDGE-STACK"] == ("Info", "P3")
    assert table["CF-CLOSE-NEG"] == ("Minor", "P2")


def test_disclaim_is_info_outside_high_impact_sections(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "We do not claim to cover outdoor scenes.\nWe show a 5\\% gain on indoor scenes.",
        section="Method",
    )
    findings, _ = _findings(tex)
    codes = {f.code: f for f in findings}
    assert codes["CF-DISCLAIM"].severity == "Info"
    assert codes["CF-DISCLAIM"].priority == "P3"


def test_disclaim_skipped_in_related_work(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "We do not attempt to survey every tracker.\nWe show the three most relevant families.",
        section="Related Work",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-DISCLAIM"]


def test_caveat_pos_candidate_keeps_the_limitation(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "Although the study covers one dataset, the trend is consistent.\n"
        "We demonstrate a 7\\% improvement over the baseline.",
    )
    findings, _ = _findings(tex)
    cav = [f for f in findings if f.code == "CF-CAVEAT-POS"]
    assert len(cav) == 1
    assert "Although the study covers one dataset" in cav[0].candidate
    assert cav[0].candidate.startswith("We demonstrate")


def test_selfweak_respects_citation_exemption(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "Prior trackers~\\cite{a} still lag far behind on long sequences.\n"
        "These methods also suffer from serious drift.\n"
        "We propose a corrector that removes the drift.",
        section="Discussion",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-SELFWEAK"]


def test_selfweak_bare_only_and_limited_are_not_flagged(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "Our method achieves a 3\\% gain.\nIt only needs one GPU and a limited memory budget.",
        section="Results",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-SELFWEAK"]


def test_hedge_stack_threshold_is_three_on_claim_sentences(tmp_path: Path) -> None:
    two = _write(tmp_path / "two", "Our approach may possibly improve recall.", section="Method")
    three = _write(
        tmp_path / "three",
        "Our approach may possibly improve recall to some extent.",
        section="Method",
    )
    non_claim = _write(
        tmp_path / "nc",
        "The weather may possibly change to some extent tomorrow.",
        section="Method",
    )
    for path, expected in ((two, 0), (three, 1), (non_claim, 0)):
        findings, _ = _findings(path)
        assert len([f for f in findings if f.code == "CF-HEDGE-STACK"]) == expected, path


def test_close_neg_suppressed_by_direction_marker(tmp_path: Path) -> None:
    body = (
        "We showed a 12\\% gain.\n\n"
        "Our framework runs in real time.\n"
        "However, it does not handle variable frame rates; future work will extend the buffer."
    )
    tex = _write(tmp_path, body, section="Conclusion")
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]


def test_close_neg_only_in_final_paragraph_of_closing_sections(tmp_path: Path) -> None:
    body = (
        "Our framework runs in real time.\n"
        "However, it does not handle variable frame rates.\n\n"
        "We showed a 12\\% gain overall."
    )
    tex = _write(tmp_path, body, section="Conclusion")
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]
    tex_disc = _write(
        tmp_path / "d",
        "Our framework runs in real time.\nHowever, it does not handle variable frame rates.",
        section="Discussion",
    )
    findings, _ = _findings(tex_disc)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]


def test_limitations_section_is_exempt_from_positional_codes(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "Our evaluation does not cover outdoor scenes.\nWe show indoor results only.",
        section="Limitations",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code in {"CF-CAVEAT-POS", "CF-CLOSE-NEG", "CF-DISCLAIM"}]


def test_missing_section_reports_error_and_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--section", "nosuch"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "ERROR [Severity: Critical] [Priority: P0]: Section not found: nosuch" in result.stdout


def test_text_output_uses_contract_block_shape() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--section", "results"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    head = [ln for ln in lines if ln.startswith("% CLAIM-FORWARD (Line")]
    assert head and "[Script] CF-SELFWEAK" in head[0]
    assert any(ln.startswith("% Original: ") for ln in lines)
    assert any(ln.startswith("% Candidate: ") for ln in lines)
    assert "% Meaning-Check: NEEDS-LLM" in lines
    assert not any("Meaning-Check: PRESERVED" in ln for ln in lines)


def test_json_output_fields() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] == 5
    assert set(payload["summary"]["by_code"]) == set(cf.CODES)
    first = payload["findings"][0]
    for field in ("code", "line", "severity", "priority", "original", "candidate", "section"):
        assert field in first


def test_terms_yaml_matches_builtin_fallback() -> None:
    import yaml

    yaml_path = SKILLS_ROOT / "latex-paper-en" / "references" / "writing" / cf.TERMS_FILENAME
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    for key in cf._LIST_KEYS:
        assert data[key] == cf._DEFAULT_TERMS[key], key
    assert data["self_weakening"] == cf._DEFAULT_TERMS["self_weakening"]


def test_terms_fallback_when_yaml_missing(tmp_path: Path) -> None:
    fake_script_dir = tmp_path / "scripts"
    fake_script_dir.mkdir()
    terms, source = cf._load_terms(fake_script_dir)
    assert source == "builtin"
    assert terms["hedges"] == cf._DEFAULT_TERMS["hedges"]


def test_terms_partial_yaml_falls_back_per_field(tmp_path: Path) -> None:
    (tmp_path / "references" / "writing").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "references" / "writing" / cf.TERMS_FILENAME).write_text(
        "hedges: [maybe]\nself_weakening: 'not-a-list'\n", encoding="utf-8"
    )
    terms, source = cf._load_terms(tmp_path / "scripts")
    assert source == "yaml"
    assert terms["hedges"] == ["maybe"]
    assert terms["self_weakening"] == cf._DEFAULT_TERMS["self_weakening"]


@pytest.mark.parametrize("code", cf.CODES)
def test_every_code_has_a_finding_note_that_never_deletes_evidence(code: str) -> None:
    findings, _ = _findings(_FIXTURE)
    f = next(f for f in findings if f.code == code)
    assert "delete the evidence" not in f.note.lower()
    if code in {"CF-CAVEAT-POS", "CF-CLOSE-NEG", "CF-DISCLAIM"}:
        # Positional codes keep the original sentence inside the candidate.
        assert f.original.split(".")[0][:30] in f.candidate
