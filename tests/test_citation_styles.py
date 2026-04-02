"""Tests for verify_bib.py --style parameter (citation style validation)."""

import tempfile
from pathlib import Path

from conftest import SCRIPT_DIR_EN  # noqa: F401
from verify_bib import BibTeXVerifier


def _write_bib(content: str) -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".bib", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


SAMPLE_BIB = r"""
@article{smith2023,
  author = {Smith, John and Jones, Alice and Brown, Bob},
  title = {A Great Paper},
  journal = {Nature Communications},
  year = {2023},
  volume = {10},
  pages = {1-15},
}

@article{doe2022,
  author = {Doe, Jane and Lee, Chris and Kim, Dan and Park, Eve and Wang, Frank and Chen, Grace and Liu, Hank},
  title = {Another Paper},
  journal = {IEEE Trans. Pattern Anal. Mach. Intell.},
  year = {2022},
  volume = {44},
  number = {3},
  pages = {100--120},
  doi = {10.1109/TPAMI.2022.1234567},
}

@article{nodoi2021,
  author = {Test, Author},
  title = {No DOI Paper},
  journal = {Some Journal},
  year = {2021},
  volume = {5},
  pages = {10--20},
}
"""


def test_verify_bib_ieee_default() -> None:
    """Default style (IEEE) should work without regressions."""
    path = _write_bib(SAMPLE_BIB)
    try:
        verifier = BibTeXVerifier(str(path))
        result = verifier.verify()
        assert result["total_entries"] == 3
        # Should still work as before
        assert result["status"] in ("PASS", "WARNING")
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_page_format_en_dash() -> None:
    """Pages with single hyphen should produce a warning."""
    path = _write_bib(SAMPLE_BIB)
    try:
        verifier = BibTeXVerifier(str(path), style="ieee")
        result = verifier.verify()
        page_issues = [i for i in result["issues"] if i.get("type") == "page_format"]
        # smith2023 has pages = {1-15} (single hyphen)
        assert len(page_issues) >= 1
        assert (
            "en dash" in page_issues[0]["message"].lower() or "en dash" in page_issues[0]["message"]
        )
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_apa_author_threshold() -> None:
    """APA uses different et al. threshold than IEEE."""
    path = _write_bib(SAMPLE_BIB)
    try:
        # APA threshold is 20 for reference list (but 3 for in-text)
        # doe2022 has 7 authors — under APA limit, should not warn about author count
        verifier = BibTeXVerifier(str(path), style="apa")
        result = verifier.verify()
        author_issues = [
            i
            for i in result["issues"]
            if i.get("type") == "author_count" and i.get("key") == "doe2022"
        ]
        # 7 authors, APA threshold is 20 → no author count warning
        assert len(author_issues) == 0
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_nature_author_threshold() -> None:
    """Nature uses et al. after 5 authors."""
    path = _write_bib(SAMPLE_BIB)
    try:
        verifier = BibTeXVerifier(str(path), style="nature")
        result = verifier.verify()
        author_issues = [
            i
            for i in result["issues"]
            if i.get("type") == "author_count" and i.get("key") == "doe2022"
        ]
        # doe2022 has 7 authors, Nature threshold is 5 → should warn
        assert len(author_issues) == 1
        assert "5" in author_issues[0]["message"]
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_doi_missing_warning() -> None:
    """IEEE/APA/Nature should warn about missing DOI."""
    path = _write_bib(SAMPLE_BIB)
    try:
        for style in ("ieee", "apa", "nature"):
            verifier = BibTeXVerifier(str(path), style=style)
            result = verifier.verify()
            doi_issues = [
                i
                for i in result["issues"]
                if i.get("type") == "doi_missing" and i.get("key") == "nodoi2021"
            ]
            assert len(doi_issues) >= 1, f"{style} should warn about missing DOI"
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_vancouver_no_doi_warning() -> None:
    """Vancouver typically doesn't require DOI."""
    path = _write_bib(SAMPLE_BIB)
    try:
        verifier = BibTeXVerifier(str(path), style="vancouver")
        result = verifier.verify()
        doi_issues = [
            i
            for i in result["issues"]
            if i.get("type") == "doi_missing" and i.get("key") == "nodoi2021"
        ]
        assert len(doi_issues) == 0, "Vancouver should not warn about missing DOI"
    finally:
        path.unlink(missing_ok=True)


def test_verify_bib_correct_en_dash_no_warning() -> None:
    """Pages with -- (en dash) should not produce page_format warning."""
    path = _write_bib(SAMPLE_BIB)
    try:
        verifier = BibTeXVerifier(str(path), style="ieee")
        result = verifier.verify()
        page_issues = [
            i
            for i in result["issues"]
            if i.get("type") == "page_format" and i.get("key") == "doe2022"
        ]
        # doe2022 has pages = {100--120} → correct, no warning
        assert len(page_issues) == 0
    finally:
        path.unlink(missing_ok=True)
