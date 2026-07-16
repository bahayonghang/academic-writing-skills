"""Balanced BibTeX scanner and encoding regressions for latex-thesis-zh."""

import importlib.util
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
