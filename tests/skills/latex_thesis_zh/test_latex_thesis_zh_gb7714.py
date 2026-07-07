"""Tests for verify_bib.py GB/T 7714 validation (audit F1/F2/F12 + 2025 transition).

``--standard gb7714`` must be a real check (not a no-op), ``default`` must
keep its legacy behavior, and ``gb7714-2025`` must reflect the documented
differences of the new standard (effective 2026-07-01).
"""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH


def _load_zh(name: str):
    zh_str = str(_ZH_DIR)
    inserted = False
    if zh_str not in sys.path or sys.path.index(zh_str) != 0:
        sys.path.insert(0, zh_str)
        inserted = True

    _collision_names = ("parsers", "tex_loader", "verify_bib", "online_bib_verify")
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"zh_gb_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    if inserted and zh_str in sys.path:
        sys.path.remove(zh_str)
        sys.path.append(zh_str)

    return mod


verify_bib = _load_zh("verify_bib")

# 全部虚构条目（fixture 明示虚构，零捏造反向要求）
FIXTURE_BIB = """\
@phdthesis{fake_thesis_no_school,
  author = {测试作者甲},
  title = {一个仅用于测试的虚构学位论文标题},
  year = {2023},
}
@online{fake_online_no_urldate,
  title = {虚构在线资源},
  url = {https://example.invalid/fake},
}
@techreport{fake_report_no_institution,
  author = {Test Author},
  title = {A Fictional Technical Report for Testing},
  year = {2022},
}
@article{fake_article_ok,
  author = {测试作者乙 and 测试作者丙},
  title = {虚构期刊文章标题},
  journal = {虚构学报},
  year = {2024},
  volume = {1},
  pages = {1--10},
}
@article{fake_article_no_volume,
  author = {Test Writer},
  title = {Another Fictional Article},
  journal = {Fictional Journal},
  year = {2024},
}
"""


def _write_fixture(tmp_path: Path) -> Path:
    bib = tmp_path / "refs.bib"
    bib.write_text(FIXTURE_BIB, encoding="utf-8")
    return bib


def _issue_set(result: dict) -> set[tuple[str, str]]:
    return {(i["key"], i.get("field", i["type"])) for i in result["issues"]}


class TestGb7714Mode:
    def test_gb_mode_reports_all_missing_fields(self, tmp_path: Path):
        bib = _write_fixture(tmp_path)
        result = verify_bib.BibTeXVerifier(str(bib), standard="gb7714").verify()
        issues = _issue_set(result)
        assert ("fake_thesis_no_school", "school") in issues
        assert ("fake_online_no_urldate", "urldate") in issues
        assert ("fake_report_no_institution", "institution") in issues
        assert ("fake_article_no_volume", "volume") in issues
        assert ("fake_article_no_volume", "pages") in issues

    def test_default_mode_keeps_legacy_behavior(self, tmp_path: Path):
        """default 模式下 GB 增量类型不检查（向后兼容回归）。"""
        bib = _write_fixture(tmp_path)
        result = verify_bib.BibTeXVerifier(str(bib), standard="default").verify()
        gb_keys = {"fake_thesis_no_school", "fake_online_no_urldate", "fake_report_no_institution"}
        flagged = {i["key"] for i in result["issues"] if i["type"].startswith(("missing", "gb"))}
        assert not (gb_keys & flagged), "default 模式不应启用 GB 增量检查"
        assert not any(i["type"].startswith("gb_") for i in result["issues"])

    def test_gb_mode_valid_article_passes(self, tmp_path: Path):
        bib = tmp_path / "ok.bib"
        bib.write_text(
            "@article{fake_ok, author = {测试作者}, title = {虚构标题}, "
            "journal = {虚构学报}, year = {2024}, volume = {1}, pages = {1--10}, "
            "langid = {chinese}}",
            encoding="utf-8",
        )
        result = verify_bib.BibTeXVerifier(str(bib), standard="gb7714").verify()
        assert not [i for i in result["issues"] if i["severity"] in ("error", "warning")]
        assert result["status"] == "PASS"  # info 提示不降级状态

    def test_mixed_truncation_marker_flagged(self, tmp_path: Path):
        bib = tmp_path / "mixed.bib"
        bib.write_text(
            "@article{fake_mixed, author = {测试作者甲 and 测试作者乙 and et al.}, "
            "title = {虚构标题}, journal = {虚构学报}, year = {2024}, "
            "volume = {1}, pages = {1--2}}",
            encoding="utf-8",
        )
        result = verify_bib.BibTeXVerifier(str(bib), standard="gb7714").verify()
        truncation = [i for i in result["issues"] if i["type"] == "gb_author_truncation"]
        assert truncation and truncation[0]["severity"] == "warning"
        assert "等" in truncation[0]["message"]


class TestGb77142025Mode:
    def test_2025_mode_available_and_differs_on_urldate_hint(self, tmp_path: Path):
        """非 online 类型带 url：2015 提示补 urldate，2025 不再提示（R3 差异点）。"""
        bib = tmp_path / "diff.bib"
        bib.write_text(
            "@article{fake_with_url, author = {Test}, title = {Fictional}, "
            "journal = {Fictional Journal}, year = {2024}, volume = {1}, "
            "pages = {1--2}, url = {https://example.invalid/x}}",
            encoding="utf-8",
        )
        r2015 = verify_bib.BibTeXVerifier(str(bib), standard="gb7714").verify()
        r2025 = verify_bib.BibTeXVerifier(str(bib), standard="gb7714-2025").verify()
        hint_2015 = [i for i in r2015["issues"] if i["type"] == "gb_urldate_hint"]
        hint_2025 = [i for i in r2025["issues"] if i["type"] == "gb_urldate_hint"]
        assert hint_2015 and not hint_2025

    def test_2025_mode_still_requires_urldate_for_online(self, tmp_path: Path):
        bib = _write_fixture(tmp_path)
        result = verify_bib.BibTeXVerifier(str(bib), standard="gb7714-2025").verify()
        assert ("fake_online_no_urldate", "urldate") in _issue_set(result)

    def test_transition_notes_present(self, tmp_path: Path):
        bib = _write_fixture(tmp_path)
        r2015 = verify_bib.BibTeXVerifier(str(bib), standard="gb7714").verify()
        notes_2015 = [i for i in r2015["issues"] if i["type"] == "gb_standard_transition"]
        assert notes_2015 and "2026-07-01" in notes_2015[0]["message"]

        r2025 = verify_bib.BibTeXVerifier(str(bib), standard="gb7714-2025").verify()
        notes_2025 = [i for i in r2025["issues"] if i["type"] == "gb_standard_transition"]
        assert notes_2025 and "非网络文献" in notes_2025[0]["message"]

    def test_arxiv_preprint_hint_in_2025_mode(self, tmp_path: Path):
        bib = tmp_path / "preprint.bib"
        bib.write_text(
            "@misc{fake_preprint, author = {Test}, title = {Fictional Preprint}, "
            "year = {2025}, eprint = {0000.00000}, archiveprefix = {arXiv}}",
            encoding="utf-8",
        )
        result = verify_bib.BibTeXVerifier(str(bib), standard="gb7714-2025").verify()
        assert any(i["type"] == "gb_preprint_hint" for i in result["issues"])


def test_no_google_web_search_in_source():
    """F12: Gemini CLI 工具名残留必须清除。"""
    source = (_ZH_DIR / "verify_bib.py").read_text(encoding="utf-8")
    assert "google_web_search" not in source
    assert "WebSearch" in source
