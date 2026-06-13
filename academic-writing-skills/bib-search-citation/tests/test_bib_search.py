#!/usr/bin/env python3
"""Tests for the bib-search-citation helper scripts."""

from __future__ import annotations

import importlib
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

preview_bib_search = importlib.import_module("preview_bib_search")

SEARCH_SCRIPT = SCRIPTS_DIR / "search_bib.py"
PREVIEW_SCRIPT = SCRIPTS_DIR / "preview_bib_search.py"
FIXTURE_BIB = Path(__file__).parent / "fixtures" / "library.bib"
PREVIEW_INPUT = Path(__file__).parent / "fixtures" / "preview_input.json"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def run_python_script(
    script: Path, *args: str, input_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )


def run_search(*args: str) -> dict:
    completed = run_python_script(SEARCH_SCRIPT, "--bib", str(FIXTURE_BIB), *args)
    return json.loads(completed.stdout)


def run_search_on(bib: Path, *args: str) -> dict:
    completed = run_python_script(SEARCH_SCRIPT, "--bib", str(bib), *args)
    return json.loads(completed.stdout)


def test_search_bib_json_contract_and_citations():
    payload = run_search(
        "--query",
        "mamba forecasting author:Cheng year>=2024 has:code cite:both limit:1",
    )

    assert payload["meta"]["query"] == "mamba forecasting"
    assert payload["meta"]["returned_entries"] == 1
    assert payload["meta"]["applied_filters"]["author_contains"] == ["Cheng"]
    assert payload["meta"]["applied_filters"]["has"] == ["code"]

    result = payload["results"][0]
    assert result["key"] == "Doe2024Mamba"
    assert result["flags"]["code"] is True
    assert result["flags"]["pdf"] is True
    assert "raw_bib" not in result
    assert result["citations"]["latex"]["cite"] == r"\cite{Doe2024Mamba}"
    assert result["citations"]["typst"]["inline"] == "@Doe2024Mamba"


def test_search_bib_include_raw_bib_without_preview_fields():
    payload = run_search(
        "--query",
        "photovoltaic raw:true cite:none limit:1",
    )

    assert payload["meta"]["returned_entries"] == 1
    result = payload["results"][0]
    assert result["key"] == "Lee2025Photovoltaic"
    assert "raw_bib" in result
    assert "@article{Lee2025Photovoltaic" in result["raw_bib"]
    assert "citations" not in result


def test_filter_only_query_keeps_sort_behavior():
    payload = run_search(
        "--query",
        "type:article sort:year_desc limit:2",
    )

    years = [result["year"] for result in payload["results"]]
    assert years == [2025, 2024]
    assert all(result["score"] == 0 for result in payload["results"])


def test_empty_query_result_is_still_valid_json():
    payload = run_search(
        "--query",
        "author:Nonexistent year>=2030 limit:5",
    )

    assert payload["meta"]["matched_entries"] == 0
    assert payload["meta"]["returned_entries"] == 0
    assert payload["results"] == []


def test_preview_from_stdin_renders_summary_and_hides_raw_bib():
    payload = run_search(
        "--query",
        "photovoltaic raw:true cite:both limit:1",
    )
    preview = run_python_script(
        PREVIEW_SCRIPT,
        input_text=json.dumps(payload, ensure_ascii=False),
    ).stdout

    assert "Query: photovoltaic | sort=relevance | returned=1 of 3 matched (3 total)" in preview
    assert "Filters: none" in preview
    assert "1. Lee2025Photovoltaic [article]" in preview
    assert "DOI: 10.1000/pv-mamba" in preview
    assert "LaTeX: \\cite{Lee2025Photovoltaic}" in preview
    assert "Typst: @Lee2025Photovoltaic | #cite(<Lee2025Photovoltaic>)" in preview
    assert "@article{Lee2025Photovoltaic" not in preview


def test_preview_input_file_mode_and_truncation():
    preview = run_python_script(PREVIEW_SCRIPT, "--input", str(PREVIEW_INPUT)).stdout

    assert "Annotation: " + ("A" * 157) + "..." in preview
    assert "Abstract: " + ("B" * 237) + "..." in preview
    assert "Keywords: " in preview and "..." in preview
    assert "LaTeX:" not in preview
    assert "Typst:" not in preview
    assert "@article{Lee2025Photovoltaic" not in preview


def test_preview_reports_invalid_payload(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(""))
    with pytest.raises(ValueError, match="expected JSON input"):
        preview_bib_search.load_payload(type("Args", (), {"input": None})())


# ── A3: recency report (additive meta) + optional claim binding ───────────────


def test_recency_block_present_and_additive():
    """meta.recency is always reported; results stay free of claim_support."""
    payload = run_search("--query", "forecasting recent:50 limit:5")
    recency = payload["meta"]["recency"]
    assert recency["window_years"] == 50
    assert recency["with_year"] == len(payload["results"])
    # A 50-year window covers every fixture entry, so all are 'recent'.
    assert recency["recent_count"] == recency["with_year"]
    assert recency["recent_share"] == 1.0
    # Regression guard: no --claim means no claim_support on any result.
    assert all("claim_support" not in result for result in payload["results"])


def test_recent_window_one_flags_aging():
    """A 1-year window (only the current year counts) trips the aging note."""
    payload = run_search("--query", "forecasting recent:1 limit:5")
    recency = payload["meta"]["recency"]
    assert recency["window_years"] == 1
    # Fixtures top out at 2025, so none fall inside a current-year-only window.
    assert recency["recent_count"] == 0
    assert "consider widening" in recency["note"]


def test_claim_binding_adds_support_block_with_provenance():
    payload = run_search(
        "--query",
        "forecasting limit:3",
        "--claim",
        "hybrid mamba photovoltaic forecasting",
    )
    supported = [r for r in payload["results"] if r.get("claim_support")]
    assert supported, "expected at least one result to carry a claim_support block"
    block = supported[0]["claim_support"]
    assert block["claim"] == "hybrid mamba photovoltaic forecasting"
    assert isinstance(block["relevance"], (int, float))
    assert block["matched_fields"], "expected matched fields for a strongly overlapping entry"
    assert "NOT proof" in block["provenance"]


# ── R1: parser robustness (B1/B2/B10) ─────────────────────────────────────────


def test_quote_inside_braces_does_not_swallow_entries():
    """A literal `"` inside a brace-delimited value must not eat later entries (B1)."""
    payload = run_search_on(FIXTURES_DIR / "quote_trap.bib", "--query", "survives")
    assert payload["meta"]["total_entries"] == 3
    assert payload["meta"]["parse_warnings"] == []


def test_truncated_entry_resyncs_and_warns():
    """A missing closing brace must not silently swallow the rest of the file (B2)."""
    payload = run_search_on(FIXTURES_DIR / "broken.bib", "--query", "recovered")
    assert payload["meta"]["total_entries"] == 2
    warnings = payload["meta"]["parse_warnings"]
    assert any(w["type"] == "unbalanced_entry" for w in warnings)
    titles = {result["title"] for result in payload["results"]}
    assert "Recovered After Resync" in titles
    assert "Also Recovered" in titles


def test_comment_and_string_are_not_phantom_entries():
    """@comment/@string/@preamble must not become searchable entries (B10)."""
    payload = run_search_on(FIXTURES_DIR / "phantom.bib", "--query", "mamba")
    # Only two real @article entries exist; the @comment mentioning mamba is not one.
    assert payload["meta"]["total_entries"] == 2
    assert payload["meta"]["returned_entries"] == 0


# ── R2: retrieval correctness (B3/B6/B7/B8/B9) ────────────────────────────────


def test_recency_does_not_leak_past_relevance_filter():
    """An unrelated query must return zero results, not every dated entry (B3)."""
    payload = run_search("--query", "quantum cryptography blockchain consensus")
    assert payload["meta"]["returned_entries"] == 0


def test_latex_accents_match_with_and_without_diacritics():
    """`author:Müller` and `author:Muller` both match `M{\\"u}ller` (B6)."""
    for needle in ("Muller", "Müller", "Gunther"):
        payload = run_search_on(FIXTURES_DIR / "biblatex.bib", "--query", f"author:{needle}")
        assert payload["meta"]["returned_entries"] == 1, needle


def test_string_macro_expansion_and_concatenation():
    """@string macros and `#` concatenation resolve in venue output (B7)."""
    macro = run_search_on(FIXTURES_DIR / "phantom.bib", "--query", "real")
    assert macro["results"][0]["venue"] == "IEEE Transactions on Geoscience and Remote Sensing"
    concat = run_search_on(FIXTURES_DIR / "phantom.bib", "--query", "concatenated")
    assert concat["results"][0]["venue"] == "Journal A Part B"


def test_journaltitle_is_used_for_venue():
    """biblatex `journaltitle` feeds derive_venue (B9)."""
    payload = run_search_on(FIXTURES_DIR / "biblatex.bib", "--query", "accent")
    assert payload["results"][0]["venue"] == "NeurIPS"


def test_crossref_child_inherits_parent_fields():
    """A crossref child inherits year and booktitle from its parent (B8)."""
    payload = run_search_on(FIXTURES_DIR / "biblatex.bib", "--query", "child")
    result = payload["results"][0]
    assert result["year"] == 2024
    assert result["venue"] == "Advances in Neural Information Processing Systems"


# ── R3: CLI and error contract (B4/B5/B11/B12/B17) ────────────────────────────


def test_cli_overrides_apply_in_spec_json_mode():
    """--claim (and friends) must reach the spec-json input mode (B11)."""
    payload = run_search(
        "--spec-json",
        json.dumps({"query": "mamba"}),
        "--claim",
        "mamba forecasting",
    )
    assert any(result.get("claim_support") for result in payload["results"])


def test_unknown_filter_key_is_rejected():
    """An invented filter key fails loudly instead of returning the full set (B12)."""
    completed = subprocess.run(
        [
            sys.executable,
            str(SEARCH_SCRIPT),
            "--bib",
            str(FIXTURE_BIB),
            "--spec-json",
            json.dumps({"filters": {"venue_contains": ["Neural"]}}),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert completed.returncode == 2
    assert "unknown filter key" in completed.stderr


def test_typo_field_filter_emits_warning():
    """A misspelled field filter surfaces a warning rather than silent zero (B12)."""
    payload = run_search("--query", "mamba tilte:forecasting")
    assert any(w["type"] == "unknown_field_filter" for w in payload["meta"]["parse_warnings"])


def test_nonpositive_limit_is_rejected():
    """limit:0 and negative limits are explicit errors, not silent defaults (B17)."""
    for limit_args in (["--query", "mamba limit:0"], ["--query", "mamba", "--limit", "-1"]):
        completed = subprocess.run(
            [sys.executable, str(SEARCH_SCRIPT), "--bib", str(FIXTURE_BIB), *limit_args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        assert completed.returncode == 2, limit_args
        assert "limit must be a positive integer" in completed.stderr


def test_missing_file_uses_json_error_contract():
    """A missing .bib file returns a JSON error on stderr with exit 2 (B4)."""
    completed = subprocess.run(
        [sys.executable, str(SEARCH_SCRIPT), "--bib", "does-not-exist.bib", "--query", "x"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert completed.returncode == 2
    payload = json.loads(completed.stderr)
    assert "could not read" in payload["error"]


def test_latin1_file_falls_back_and_flags_encoding(tmp_path):
    """A latin-1 .bib decodes via fallback and flags it in meta (B4)."""
    bib = tmp_path / "legacy.bib"
    bib.write_bytes(
        "@article{f1, title={Caf\xe9 Study}, author={Fran\xe7ois}, "
        "year={2020}, journal={J}}\n".encode("latin-1")
    )
    payload = run_search_on(bib, "--query", "study")
    assert payload["meta"]["encoding_fallback"] == "latin-1"
    assert payload["results"][0]["author"]


def test_non_gbk_author_does_not_crash(tmp_path):
    """Output stays valid UTF-8 JSON even for characters outside a legacy codec (B5)."""
    bib = tmp_path / "unicode.bib"
    bib.write_text(
        "@article{l1, title={Attention Study}, author={Łukasz Kaiser}, "
        "year={2017}, journal={NIPS}}\n",
        encoding="utf-8",
    )
    completed = subprocess.run(
        [sys.executable, str(SEARCH_SCRIPT), "--bib", str(bib), "--query", "attention"],
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0
    payload = json.loads(completed.stdout.decode("utf-8"))
    assert "Łukasz" in payload["results"][0]["author"]
