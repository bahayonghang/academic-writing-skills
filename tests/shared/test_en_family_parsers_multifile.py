"""Regression tests for the EN-family parser foundation (06-13-en-family-parsers).

Covers the P0 audit fixes back-ported from latex-thesis-zh into the four
EN-family parser copies (E2/E4/E6/E9, T6/T7/T21, C2/C3/C10):

- LatexParser/TypstParser.split_sections handle starred / plural / ALL-CAPS /
  compound titles, skip commented-out headings, suffix duplicate keys, and no
  longer let an unmatched body section swallow the previous one;
- resolve_section_keys accepts loose synonyms and lists alternatives;
- clean_text no longer eats prose between \\emph{..} and \\[..\\];
- TypstParser recognises ``= Abstract`` and strips block-commented headings;
- extract_title/extract_abstract read the ``#show: tmpl.with(title:.., abstract:..)``
  Universe template form (charged-ieee etc.);
- tex_loader / typ_loader assemble multi-file projects with source-line mapping.

Imports resolve to the copies on sys.path (paper-audit / latex-paper-en, which
are byte-identical for the shared core); the alignment test guards the rest.
"""

from pathlib import Path

import tex_loader
import typ_loader
from parsers import (
    LatexParser,
    TypstParser,
    extract_abstract,
    extract_title,
    resolve_section_keys,
)

# ── LatexParser.split_sections (E2) ───────────────────────────────


class TestLatexSplitSections:
    def test_starred_plural_caps_and_compound_titles(self):
        content = "\n".join(
            [
                r"\section*{Introduction}",
                "Intro.",
                r"\section{Methods}",
                "M.",
                r"\section{Experiments}",
                "E.",
                r"\section{RELATED WORKS}",
                "R.",
                r"\section{Results and Discussion}",
                "RD.",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert {"introduction", "method", "experiment", "related", "result"} <= set(sections)

    def test_commented_heading_ignored(self):
        content = "\n".join(
            [r"\section{Introduction}", "Body.", r"% \section{Conclusion}", "More."]
        )
        sections = LatexParser().split_sections(content)
        assert "conclusion" not in sections
        # introduction range runs to the end, not cut by the commented heading
        assert sections["introduction"] == (1, 4)

    def test_duplicate_sections_both_kept(self):
        content = "\n".join([r"\section{Experiments}", "first", r"\section{Experiments}", "second"])
        sections = LatexParser().split_sections(content)
        assert "experiment" in sections and "experiment_2" in sections
        assert sections["experiment"][0] == 1
        assert sections["experiment_2"][0] == 3

    def test_unmatched_section_not_swallowed_by_previous(self):
        content = "\n".join(
            [
                r"\section{Introduction}",
                "intro body",
                r"\section{Preliminaries}",  # unmatched body section
                "prelim body",
                r"\section{Conclusion}",
                "wrap",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert sections["introduction"] == (1, 2)

    def test_chapter_ranges_enumerates_unmatched_sections(self):
        content = "\n".join([r"\section{Introduction}", "a", r"\section{Preliminaries}", "b"])
        ranges = LatexParser().chapter_ranges(content)
        titles = [r["title"] for r in ranges]
        assert "Preliminaries" in titles
        prelim = next(r for r in ranges if r["title"] == "Preliminaries")
        assert prelim["key"] is None


# ── clean_text display-math fix (E9) ──────────────────────────────


class TestCleanText:
    def test_display_math_does_not_swallow_surrounding_prose(self):
        cleaned = LatexParser().clean_text(r"Before text \emph{kept} and \[ x = 1 \] after text.")
        assert "Before text" in cleaned
        assert "after text" in cleaned
        assert "kept" in cleaned
        assert "x = 1" not in cleaned


# ── resolve_section_keys (E5) ─────────────────────────────────────


class TestResolveSectionKeys:
    SECTIONS = {"introduction": (1, 5), "method": (6, 10), "method_2": (11, 15)}

    def test_synonym_resolves(self):
        keys, _ = resolve_section_keys("methods", self.SECTIONS)
        assert keys == ["method", "method_2"]

    def test_canonical_key_resolves(self):
        keys, _ = resolve_section_keys("introduction", self.SECTIONS)
        assert keys == ["introduction"]

    def test_unknown_returns_available_list(self):
        keys, available = resolve_section_keys("nonexistent", self.SECTIONS)
        assert keys == []
        assert "introduction" in available


# ── TypstParser (T7/T21) ──────────────────────────────────────────


class TestTypstParser:
    def test_abstract_heading_and_block_comment(self):
        content = "\n".join(
            [
                "= Abstract",
                "We present a method.",
                "= Introduction",
                "Intro.",
                "/* = Stale Heading */",
                "= Experiments",
                "E.",
            ]
        )
        sections = TypstParser().split_sections(content)
        assert {"abstract", "introduction", "experiment"} <= set(sections)
        assert "stale" not in {k.split("_")[0] for k in sections}

    def test_duplicate_typst_sections_both_kept(self):
        content = "= Methods\na\n= Methods\nb\n"
        sections = TypstParser().split_sections(content)
        assert "method" in sections and "method_2" in sections


# ── Universe template extraction (T7) ─────────────────────────────


class TestTemplateExtraction:
    TEMPLATE = (
        '#import "@preview/charged-ieee:0.1.4": ieee\n'
        "#show: ieee.with(\n"
        "  title: [A Robust Forecasting Method],\n"
        "  abstract: [We present a #emph[robust] pipeline.],\n"
        ")\n"
    )

    def test_title_from_with_call(self):
        assert extract_title(self.TEMPLATE) == "A Robust Forecasting Method"

    def test_abstract_from_with_call(self):
        assert extract_abstract(self.TEMPLATE) == "We present a robust pipeline."

    def test_abstract_from_heading(self):
        content = "= Abstract\nHeading-based abstract body.\n= Introduction\n"
        assert extract_abstract(content) == "Heading-based abstract body."


# ── tex_loader multi-file assembly (E6) ───────────────────────────


def _write_tex_project(tmp_path: Path) -> Path:
    (tmp_path / "sections").mkdir()
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\input{sections/intro}\n"
        "\\input{sections/method}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    (tmp_path / "sections" / "intro.tex").write_text(
        "\\section{Introduction}\nIntro body line.\n", encoding="utf-8"
    )
    (tmp_path / "sections" / "method.tex").write_text(
        "\\section{Methods}\nMethod body.\n", encoding="utf-8"
    )
    return main


class TestTexLoader:
    def test_assemble_expands_inputs_in_order(self, tmp_path: Path):
        doc = tex_loader.assemble(_write_tex_project(tmp_path))
        assert doc.multi_file
        assert "\\section{Introduction}" in doc.content
        assert doc.content.index("Introduction") < doc.content.index("Methods")

    def test_origin_maps_back_to_source_file(self, tmp_path: Path):
        doc = tex_loader.assemble(_write_tex_project(tmp_path))
        line_no = next(i for i, line in enumerate(doc.lines, 1) if "Intro body" in line)
        assert doc.origin(line_no) == ("sections/intro.tex", 2)
        assert doc.lineref(line_no) == "sections/intro.tex:2"

    def test_split_sections_on_assembled_multifile(self, tmp_path: Path):
        doc = tex_loader.assemble(_write_tex_project(tmp_path))
        sections = LatexParser().split_sections(doc.content)
        assert "introduction" in sections and "method" in sections

    def test_commented_input_not_expanded(self, tmp_path: Path):
        (tmp_path / "old.tex").write_text("\\section{Stale Draft}\n", encoding="utf-8")
        main = tmp_path / "main.tex"
        main.write_text("% \\input{old}\nbody\n", encoding="utf-8")
        doc = tex_loader.assemble(main)
        assert "Stale Draft" not in doc.content

    def test_missing_input_reported_not_silent(self, tmp_path: Path):
        main = tmp_path / "main.tex"
        main.write_text("\\input{ghost}\n", encoding="utf-8")
        doc = tex_loader.assemble(main)
        assert doc.missing
        assert "ghost" in "\n".join(doc.warning_lines("%"))

    def test_circular_input_terminates(self, tmp_path: Path):
        (tmp_path / "a.tex").write_text("A\n\\input{b}\n", encoding="utf-8")
        (tmp_path / "b.tex").write_text("B\n\\input{a}\n", encoding="utf-8")
        doc = tex_loader.assemble(tmp_path / "a.tex")
        assert "A" in doc.content and "B" in doc.content


# ── typ_loader multi-file assembly (T6) ───────────────────────────


def _write_typ_project(tmp_path: Path) -> Path:
    (tmp_path / "chapters").mkdir()
    main = tmp_path / "main.typ"
    main.write_text(
        "#show: ieee.with(title: [X])\n"
        '#include "chapters/intro.typ"\n'
        '/* #include "chapters/ghost.typ" */\n',
        encoding="utf-8",
    )
    (tmp_path / "chapters" / "intro.typ").write_text(
        "= Introduction\nTypst intro body.\n", encoding="utf-8"
    )
    return main


class TestTypLoader:
    def test_assemble_expands_includes(self, tmp_path: Path):
        doc = typ_loader.assemble(_write_typ_project(tmp_path))
        assert doc.multi_file
        assert "= Introduction" in doc.content

    def test_origin_maps_back_to_source_file(self, tmp_path: Path):
        doc = typ_loader.assemble(_write_typ_project(tmp_path))
        line_no = next(i for i, line in enumerate(doc.lines, 1) if "Typst intro body" in line)
        assert doc.origin(line_no) == ("chapters/intro.typ", 2)
        assert doc.lineref(line_no) == "chapters/intro.typ:2"

    def test_block_commented_include_skipped(self, tmp_path: Path):
        doc = typ_loader.assemble(_write_typ_project(tmp_path))
        assert not doc.missing  # ghost include is inside a block comment

    def test_circular_include_terminates(self, tmp_path: Path):
        (tmp_path / "a.typ").write_text('A\n#include "b.typ"\n', encoding="utf-8")
        (tmp_path / "b.typ").write_text('B\n#include "a.typ"\n', encoding="utf-8")
        doc = typ_loader.assemble(tmp_path / "a.typ")
        assert "A" in doc.content and "B" in doc.content
