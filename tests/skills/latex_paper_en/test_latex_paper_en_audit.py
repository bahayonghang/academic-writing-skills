"""Regression tests for the latex-paper-en audit fixes (E1-E18, E20-E24).

These pin the behaviors fixed in task 06-13-en-paper-precision and bind the
multi-file ``evals/fixtures/paper-project`` fixture.
"""

from __future__ import annotations

import importlib
import struct
import subprocess
import sys
import zlib

import pytest

from tests.support.paths import SKILLS_ROOT

SKILL_DIR = SKILLS_ROOT / "latex-paper-en"
SCRIPTS = SKILL_DIR / "scripts"
FIXTURE = SKILL_DIR / "evals" / "fixtures" / "paper-project"
MAIN_TEX = FIXTURE / "main.tex"


def _run(script: str, *args: str, stdin: str | None = None):
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        input=stdin,
        check=False,
    )


@pytest.fixture(scope="module", autouse=True)
def _ensure_fixture_png():
    """The fixture ships a tiny PNG; regenerate it if a checkout dropped it."""
    png = FIXTURE / "figs" / "arch.png"
    if not png.exists():
        png.parent.mkdir(parents=True, exist_ok=True)
        w = h = 2
        raw = b"".join(b"\x00" + b"\xff\x00\x00" * w for _ in range(h))

        def chunk(tag: bytes, data: bytes) -> bytes:
            body = tag + data
            return (
                struct.pack(">I", len(data))
                + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
            )

        png.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b"")
        )


# ── E1 / E26: check_format no longer always PASSes ────────────────────────────


def test_check_format_parses_terse_chktex_output():
    parsers = importlib.import_module("check_format")
    checker = parsers.FormatChecker("dummy.tex")
    sample = (
        "C:/proj/main.tex:3:15:36:You should put a space in front of parenthesis.\n"
        "C:/proj/main.tex:5:12:18:Use either `` or '' as an alternative to `\"'.\n"
        "main.tex:9:1:13:Intersentence spacing should be done with backslash.\n"
    )
    issues = checker._parse_output(sample)
    assert len(issues) == 3
    assert issues[0]["code"] == 36
    assert issues[0]["category"] == "spacing"
    assert issues[1]["category"] == "quotation"


def test_check_format_internal_error_on_unparseable_output():
    parsers = importlib.import_module("check_format")
    checker = parsers.FormatChecker("dummy.tex")
    # Non-empty output that does not match the expected format must not be PASS.
    assert checker._parse_output("Some unexpected banner line") == []


# ── E3: deai_check works without PyYAML ───────────────────────────────────────


def test_deai_thresholds_fall_back_without_pyyaml(monkeypatch):
    deai = importlib.import_module("deai_check")
    real_import = (
        __builtins__["__import__"] if isinstance(__builtins__, dict) else __builtins__.__import__
    )

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ImportError("simulated missing PyYAML")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    thresholds = deai._load_thresholds(SCRIPTS)
    # Must return the built-in defaults rather than raising ImportError.
    assert isinstance(thresholds, dict) and thresholds


# ── E4 / E5: --section alias + unknown-section error ──────────────────────────


def test_deai_section_alias_resolves():
    result = _run("deai_check.py", str(MAIN_TEX), "--section", "methods")
    assert result.returncode == 0
    assert "Section: method" in result.stdout


def test_deai_unknown_section_errors_with_available_keys():
    result = _run("deai_check.py", str(MAIN_TEX), "--section", "nope")
    assert result.returncode == 2
    assert "Available sections" in result.stderr


# ── E2: starred / plural / commented headings via split_sections ──────────────


def test_split_sections_handles_starred_plural_and_comments():
    parsers = importlib.import_module("parsers")
    content = MAIN_TEX.read_text(encoding="utf-8")
    sections = parsers.LatexParser().split_sections(content)
    assert "method" in sections  # \section{Methods}
    assert "experiment" in sections  # \section{Experiments}


# ── E7: graphicspath nested braces resolve subdir figures ─────────────────────


def test_graphicspath_subdir_resolves():
    result = _run("check_figures.py", str(MAIN_TEX))
    assert "MISSING" not in result.stdout


# ── E13: hard-wrapped long sentence is detected ───────────────────────────────


def test_long_sentence_detected_across_wrapped_lines():
    result = _run("analyze_sentences.py", str(MAIN_TEX), "--max-words", "50")
    assert "LONG SENTENCE (Line" in result.stdout


# ── E14: model-name labels do not create a phantom numbering gap ──────────────


def test_no_false_numbering_gap_for_model_names():
    result = _run("check_references.py", str(MAIN_TEX))
    assert "Numbering gap" not in result.stdout


# ── E6: citation inside an \input'd file is not reported unused ───────────────


def test_multifile_citation_not_unused():
    result = _run("verify_bib.py", str(FIXTURE / "references.bib"), "--tex", str(MAIN_TEX))
    assert "vaswani2017" not in result.stdout.split("Unused BibTeX entries:")[-1]
    assert "unused2020" in result.stdout


# ── E15: improve_expression no longer fights the deai guide ───────────────────


def test_improve_expression_drops_conflicting_replacements():
    improve = importlib.import_module("improve_expression")
    assert not any("employ" in v for v in improve.WEAK_VERBS.values())
    assert not any("demonstrate" in v for v in improve.WEAK_VERBS.values())


# ── E10: generate_table --style plain differs from booktabs ───────────────────


def test_generate_table_plain_differs_from_booktabs():
    gen = importlib.import_module("generate_table")
    headers = ["Method", "Acc"]
    rows = [["A", "90"], ["B", "85"]]
    plain = gen.TableGenerator(style="plain")._to_latex(headers, rows)
    booktabs = gen.TableGenerator(style="booktabs")._to_latex(headers, rows)
    assert plain != booktabs
    assert "\\hline" in plain
    assert "\\toprule" in booktabs


# ── E8: verify_bib --online sends DOI-bearing entries to the verifier ─────────


def test_online_verification_covers_doi_entries(monkeypatch, tmp_path):
    verify = importlib.import_module("verify_bib")
    bib = tmp_path / "refs.bib"
    bib.write_text(
        "@article{withdoi, title={T}, author={A}, journal={J}, year={2020}, doi={10.1/x}}\n",
        encoding="utf-8",
    )
    verified_keys: list[str] = []

    class FakeResult:
        status = "verified"
        suggested_doi = ""

        def __init__(self, key):
            self.bib_key = key

    class FakeVerifier:
        def __init__(self, *a, **k):
            pass

        def verify_entry(self, entry):
            verified_keys.append(entry.get("key", ""))
            return FakeResult(entry.get("key", ""))

    monkeypatch.setitem(sys.modules, "online_bib_verify", type(sys)("online_bib_verify"))
    sys.modules["online_bib_verify"].OnlineBibVerifier = FakeVerifier

    verifier = verify.BibTeXVerifier(str(bib), online=True)
    verifier.verify()
    # The DOI-bearing entry must have been sent for online verification (E8).
    assert "withdoi" in verified_keys


# ── E16: --interactive refuses a non-tty caller instead of blocking ───────────


def test_optimize_title_interactive_requires_tty():
    result = _run("optimize_title.py", str(MAIN_TEX), "--interactive", stdin="")
    assert result.returncode == 2
    assert "requires a terminal" in result.stderr


# ── E23: smoke tests for previously-untested scripts ──────────────────────────


def test_extract_prose_runs():
    result = _run("extract_prose.py", str(MAIN_TEX))
    assert result.returncode == 0


def test_analyze_grammar_runs_and_preserves_case():
    grammar = importlib.import_module("analyze_grammar")
    findings = grammar._apply_rules("These method use BERT and the data shows gains")
    # An acronym in the line must keep its original casing.
    assert any("BERT" in revised for _, revised, _ in findings)
