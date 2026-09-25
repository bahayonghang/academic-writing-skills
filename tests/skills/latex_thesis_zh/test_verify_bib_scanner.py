"""Balanced BibTeX scanner and encoding regressions for latex-thesis-zh."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

GBK_FIXTURE = (
    SKILLS_ROOT / "latex-thesis-zh" / "evals" / "fixtures" / "thesis-project" / "references-gbk.bib"
)


def _load_zh(name: str):
    saved_path = list(sys.path)
    collisions = ("bib_scan", "parsers", "tex_loader")
    saved = {module: sys.modules.pop(module, None) for module in collisions}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(
            f"zh_bib_{name}", SCRIPT_DIR_ZH / f"{name}.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module, value in saved.items():
            if value is None:
                sys.modules.pop(module, None)
            else:
                sys.modules[module] = value


verify_bib = _load_zh("verify_bib")
check_spec = _load_zh("check_spec")


def test_balanced_scanner_preserves_caret_at_and_nested_values(tmp_path: Path) -> None:
    bib = tmp_path / "edge.bib"
    bib.write_text(
        "@string{venue = {Journal}}\n"
        '@comment{ignored}\n@preamble{"ignored"}\n'
        "@article{one, author={A}, title={The $L^2$ Norm}, journal=venue, year={2025}, "
        "note={mail: a@b.edu}}\n"
        '@article{two, author={B}, title={{Deep {Learning}} Methods}, journal="J {Series}", year=2024}\n',
        encoding="utf-8",
    )
    verifier = verify_bib.BibTeXVerifier(str(bib))
    entries = verifier.parse()
    assert [entry["key"] for entry in entries] == ["one", "two"]
    assert entries[0]["fields"]["title"] == "The $L^2$ Norm"
    assert entries[0]["fields"]["note"] == "mail: a@b.edu"
    assert entries[0]["fields"]["journal"] == "Journal"
    assert entries[1]["fields"]["title"] == "{Deep {Learning}} Methods"
    assert entries[1]["fields"]["journal"] == "J {Series}"


def test_unclosed_entry_warns_and_resyncs(tmp_path: Path) -> None:
    bib = tmp_path / "broken.bib"
    bib.write_text(
        "@article{broken, title={Never closes}, author={A}\n"
        "@article{good, author={B}, title={Good}, journal={J}, year={2025}}\n",
        encoding="utf-8",
    )
    result = verify_bib.BibTeXVerifier(str(bib)).verify()
    assert result["total_entries"] == 1
    assert any(issue["type"] == "unbalanced_entry" for issue in result["issues"])


def test_percent_prefixed_entry_is_included_with_warning(tmp_path: Path) -> None:
    bib = tmp_path / "commented.bib"
    bib.write_text(
        "% @article{visible, author={A}, title={T}, journal={J}, year={2025}}\n",
        encoding="utf-8",
    )
    result = verify_bib.BibTeXVerifier(str(bib)).verify()
    assert result["total_entries"] == 1
    assert any(issue["type"] == "commented_entry_included" for issue in result["issues"])


def test_gb18030_bib_restores_cjk_checks_and_spec_stats(tmp_path: Path) -> None:
    assert GBK_FIXTURE.read_bytes().decode("gb18030").startswith("@article{zh2025")
    result = verify_bib.BibTeXVerifier(str(GBK_FIXTURE), standard="gb7714").verify()
    assert result["total_entries"] == 2
    assert any(issue["type"] == "encoding_warning" for issue in result["issues"])
    assert any(issue["type"] == "gb_langid_hint" for issue in result["issues"])

    tex = tmp_path / "main.tex"
    tex.write_text("\\chapter{绪论}\n\\bibliography{references-gbk}\n", encoding="utf-8")
    ctx = check_spec.SpecContext(tex, "master", "yanshan", str(GBK_FIXTURE), 2026)
    assert ctx.bib_entries == 2
    assert ctx.bib_years == [2025, 2024]
    assert "编码提示" in ctx.bib_note


def _college_bib() -> str:
    return """
@article{art,
  author = {Ada Example},
  title = {Plain Title},
  journal = {Example Journal},
  year = {2020},
  articleno = {A12}
}
@book{whole,
  author = {Guozhi Li},
  title = {Synthetic Structures},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  pages = {1--9}
}
@book{particle,
  author = {van der Waals, Johannes},
  title = {Synthetic Particles},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  pages = {10--12}
}
@book{hyphen,
  author = {Smith-Jones, Alex},
  title = {Synthetic Hyphens},
  publisher = {Example Press},
  year = {2020},
  location = {Shanghai},
  pages = {13--15}
}
@book{accent,
  author = {García, José},
  title = {Synthetic Accents},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  pages = {16--18}
}
@book{org,
  author = {{Example Institute}},
  title = {Synthetic Organization},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  pages = {19--21}
}
@book{abbrev,
  author = {LI G Z},
  title = {Not a Source Record},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  pages = {22--24}
}
@book{missingPlace,
  author = {Ada Example},
  title = {Missing Place},
  publisher = {Example Press},
  year = {2020},
  pages = {25--27}
}
@phdthesis{missingPages,
  author = {Ada Example},
  title = {Missing Pages},
  school = {Example University},
  year = {2020},
  address = {Qinhuangdao}
}
@mastersthesis{missingBoth,
  author = {Ada Example},
  title = {Missing Both},
  school = {Example University},
  year = {2020}
}
@inproceedings{missingConf,
  author = {Ada Example},
  title = {Missing Conference Pages},
  booktitle = {Example Meeting},
  year = {2020}
}
@book{articleNo,
  author = {Ada Example},
  title = {Book With Article Number},
  publisher = {Example Press},
  year = {2020},
  address = {Qinhuangdao},
  eid = {E99}
}
"""


def _verify(path: Path, standard: str = "gb7714", college: bool = False) -> dict:
    return verify_bib.BibTeXVerifier(str(path), standard, college_details=college).verify()


def test_college_details_appends_info_without_changing_standard_issues(tmp_path: Path) -> None:
    bib = tmp_path / "refs.bib"
    original = _college_bib()
    bib.write_text(original, encoding="utf-8")
    base = _verify(bib, college=False)
    extra = _verify(bib, college=True)
    assert [issue["message"] for issue in extra["issues"][: len(base["issues"])]] == [
        issue["message"] for issue in base["issues"]
    ]
    assert extra["status"] == base["status"]
    added = extra["issues"][len(base["issues"]) :]
    assert added
    assert all(issue["severity"] == "info" for issue in added)
    assert all(issue.get("priority") == "P3" for issue in added)
    assert all("[Script]" in issue["message"] for issue in added)
    assert all("Meaning-Check: NEEDS-LLM" in issue["message"] for issue in added)
    report = verify_bib.BibTeXVerifier(str(bib), "gb7714", college_details=True).generate_report(
        extra
    )
    assert "[INFO] [Priority: P3] @" in report
    assert report.count("[Priority: P3]") == len(added)
    assert bib.read_text(encoding="utf-8") == original

    art_pages = [
        issue
        for issue in extra["issues"]
        if issue["key"] == "art" and issue.get("field") == "pages"
    ]
    assert len(art_pages) == 1
    assert art_pages[0]["type"] == "gb_missing_field"
    assert not any(
        issue["key"] == "art" and issue["type"].startswith("college_") for issue in added
    )

    assert any(issue["key"] == "missingPlace" and "address" in issue["message"] for issue in added)
    assert any(
        issue["key"] == "missingPlace" and "不猜测学校" in issue["message"] for issue in added
    )
    assert not any(issue["key"] == "hyphen" and "address" in issue["message"] for issue in added)
    assert any(issue["key"] == "missingPages" and "pages" in issue["message"] for issue in added)
    assert any(issue["key"] == "missingBoth" and "address" in issue["message"] for issue in added)
    conf = [issue for issue in added if issue["key"] == "missingConf"]
    assert conf and "101" in conf[0]["message"] and "PDF" in conf[0]["message"]
    article_no = [issue for issue in added if issue["key"] == "articleNo"]
    assert article_no
    assert "文章号" in article_no[0]["message"]
    assert "不根据 PDF" in article_no[0]["message"]
    assert "建议页数" not in article_no[0]["message"]

    style = [issue for issue in added if issue["type"] == "college_author_style"]
    assert len(style) == 1
    assert "BBL/PDF" in style[0]["message"]
    assert "不把 LI G Z 当作正确的源 BibTeX" in style[0]["message"]
    assert "Guozhi Li" not in style[0]["message"]
    assert "LI G" in bib.read_text(encoding="utf-8")
    for issue in extra["issues"]:
        assert "Guozhi Li" not in issue["message"]
        if "大小写违规" in issue["message"]:
            assert "不作大小写违规" in issue["message"]


def test_college_details_without_author_data_skips_the_style_note(tmp_path: Path) -> None:
    bib = tmp_path / "refs.bib"
    bib.write_text(
        "@book{bk, title={Plain Title}, publisher={Example Press}, year={2020}, "
        "address={Shanghai}, pages={1--2}}\n",
        encoding="utf-8",
    )
    result = _verify(bib, college=True)
    assert not any(issue["type"] == "college_author_style" for issue in result["issues"])
    assert not any(issue["type"] == "college_address" for issue in result["issues"])
    assert not any(issue["type"] == "college_pages" for issue in result["issues"])


def test_college_details_rejects_non_gb_standards(tmp_path: Path) -> None:
    bib = tmp_path / "refs.bib"
    bib.write_text("@book{bk, title={Plain Title}}\n", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    script = SCRIPT_DIR_ZH / "verify_bib.py"
    cases = (
        ["--college-details"],
        ["--standard", "default", "--college-details"],
        ["--college-details", "--standard", "default"],
    )
    for args in cases:
        result = subprocess.run(
            [sys.executable, "-X", "utf8", "-B", str(script), str(bib), *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False,
        )
        assert result.returncode != 0, args
        assert "PASS" not in result.stdout
        assert "Status:" not in result.stdout

    accepted = subprocess.run(
        [
            sys.executable,
            "-X",
            "utf8",
            "-B",
            str(script),
            str(bib),
            "--standard",
            "gb7714-2025",
            "--college-details",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    assert accepted.returncode != 0
    assert "address" in accepted.stdout
    assert "Status: PASS" not in accepted.stdout
