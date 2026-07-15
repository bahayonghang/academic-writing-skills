"""Regression tests: bulk tex_loader.assemble() adoption (A-EN-3 main body).

Ten scripts previously read only the entry ``.tex`` file via bare
``path.read_text()``, so a skeleton ``main.tex`` whose body lives entirely in
``\\input``-ed sub-files produced zero findings / "not found" / "no ...
detected" for content that is actually there. Each test below plants the
relevant trigger content in a sub-file (never in ``main.tex`` itself) and
asserts the fixed script still finds it.

Batch 4a covers: deai_check, analyze_logic, analyze_experiment,
analyze_literature, analyze_abstract, check_figures, check_tables,
check_pseudocode, optimize_title, deai_batch.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_EN


def _run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT_DIR_EN / script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def _write_full_project(tmp_path: Path) -> Path:
    """Skeleton main.tex whose entire body lives in \\input-ed sub-files.

    - abstract lives in sections/abstract.tex (environment form)
    - Introduction / Related Work / Methods / Experiments each get their own
      sub-file with content that triggers a specific script's checks
    - Experiments carries a figure, a non-booktabs table, and a bare
      (non-figure-wrapped) algorithm block
    """
    sections = tmp_path / "sections"
    sections.mkdir()
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{article}\n"
        "\\title{A Deep Learning Approach}\n"
        "\\begin{document}\n"
        "\\input{sections/abstract}\n"
        "\\input{sections/intro}\n"
        "\\input{sections/related}\n"
        "\\input{sections/method}\n"
        "\\input{sections/experiment}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    (sections / "abstract.tex").write_text(
        "\\begin{abstract}\n"
        "This paper presents a significant improvement over existing forecasting baselines.\n"
        "\\end{abstract}\n",
        encoding="utf-8",
    )
    (sections / "intro.tex").write_text(
        "\\section{Introduction}\nThis work addresses time series forecasting.\n",
        encoding="utf-8",
    )
    (sections / "related.tex").write_text(
        "\\section{Related Work}\n"
        "In 2019, Smith et al. proposed a novel attention mechanism for sequence modeling.\n"
        "In 2020, Jones et al. introduced a graph-based approach for document classification.\n"
        "In 2021, Wang et al. presented a hybrid method combining transformers and CNNs.\n"
        "In 2022, Li et al. developed an efficient pruning strategy for large models.\n",
        encoding="utf-8",
    )
    (sections / "method.tex").write_text(
        "\\section{Methods}\nWe use a three-layer model.\n",
        encoding="utf-8",
    )
    (sections / "experiment.tex").write_text(
        "\\section{Experiments}\n"
        "Our method significantly outperforms prior methods on the benchmark.\n"
        "\n"
        "\\begin{figure}\n"
        "\\includegraphics{arch}\n"
        "\\caption{Architecture}\n"
        "\\label{fig:arch}\n"
        "\\end{figure}\n"
        "\n"
        "\\begin{table}\n"
        "\\begin{tabular}{cc}\n"
        "\\hline\n"
        "A & B \\\\\n"
        "\\hline\n"
        "1 & 2 \\\\\n"
        "\\hline\n"
        "\\end{tabular}\n"
        "\\caption{Results}\n"
        "\\end{table}\n"
        "\n"
        "\\begin{algorithm}\n"
        "\\caption{Training procedure}\n"
        "\\label{alg:train}\n"
        "\\begin{algorithmic}\n"
        "\\State Initialize weights\n"
        "\\end{algorithmic}\n"
        "\\end{algorithm}\n",
        encoding="utf-8",
    )
    return main


# ── deai_check.py ──────────────────────────────────────────────────────────


def test_deai_check_finds_traces_in_included_section(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("deai_check.py", str(main), "--section", "abstract")
    assert result.returncode == 0
    assert "Density:" in result.stdout
    assert "0.0%" not in result.stdout.split("Density:")[1][:10]


def test_deai_check_fix_suggestions_include_source_metadata(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("deai_check.py", str(main), "--fix-suggestions")
    assert result.returncode == 0
    suggestions = json.loads(result.stdout)
    assert suggestions
    hit = next(s for s in suggestions if s["category"] == "empty_phrase")
    assert hit.get("source_file", "").endswith("abstract.tex")


# ── analyze_logic.py ───────────────────────────────────────────────────────


def test_analyze_logic_scans_methods_in_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("analyze_logic.py", str(main), "--section", "methods")
    assert "three-layer model" in result.stdout


# ── analyze_experiment.py ───────────────────────────────────────────────────


def test_analyze_experiment_flags_claim_in_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("analyze_experiment.py", str(main), "--section", "experiments")
    joined = result.stdout.lower()
    assert "no rule-based experiment review issues detected" not in joined
    assert "baseline" in joined or "comparator" in joined


# ── analyze_literature.py ───────────────────────────────────────────────────


def test_analyze_literature_flags_enumeration_in_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("analyze_literature.py", str(main), "--section", "related")
    assert "enumeration" in result.stdout.lower()


# ── analyze_abstract.py ─────────────────────────────────────────────────────


def test_analyze_abstract_reads_abstract_from_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("analyze_abstract.py", str(main), "--json")
    payload = json.loads(result.stdout)
    assert payload["status"] != "ERROR"
    assert "No abstract found" not in payload.get("message", "")


# ── check_figures.py ─────────────────────────────────────────────────────────


def test_check_figures_finds_figure_in_included_file(tmp_path: Path) -> None:
    import importlib

    main = _write_full_project(tmp_path)
    check_figures = importlib.import_module("check_figures")
    checker = check_figures.FigureChecker(main)
    figures = checker.find_figures()
    assert len(figures) == 1
    assert figures[0]["rel_path"] == "arch"


# ── check_tables.py ──────────────────────────────────────────────────────────


def test_check_tables_finds_hline_issue_in_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("check_tables.py", str(main), "--json")
    payload = json.loads(result.stdout)
    assert payload["table_count"] == 1
    messages = " ".join(i["message"] for i in payload["issues"])
    assert "hline" in messages.lower()


# ── check_pseudocode.py ──────────────────────────────────────────────────────


def test_check_pseudocode_flags_bare_algorithm_in_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("check_pseudocode.py", str(main), "--venue", "ieee", "--json")
    issues = json.loads(result.stdout)
    assert any(i["severity"] == "Critical" for i in issues)
    assert any("floating algorithm environments" in i["message"] for i in issues)


# ── optimize_title.py ────────────────────────────────────────────────────────


def test_optimize_title_generate_uses_abstract_from_included_file(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("optimize_title.py", str(main), "--generate")
    assert "No abstract found" not in result.stderr
    assert "Warning: No abstract found" not in result.stderr


# ── deai_batch.py ────────────────────────────────────────────────────────────


def test_deai_batch_all_sections_finds_traces_in_included_files(tmp_path: Path) -> None:
    main = _write_full_project(tmp_path)
    result = _run("deai_batch.py", str(main), "--all-sections")
    assert "SECTION: ABSTRACT" in result.stdout
    section_block = result.stdout.split("SECTION: ABSTRACT", 1)[1]
    section_block = section_block.split("SECTION:", 1)[0]
    assert "AI traces detected: 0" not in section_block


# ── Single-file invariance spot checks (existing suites cover the rest) ────


def test_check_figures_single_file_behavior_unchanged(tmp_path: Path) -> None:
    """Sanity check: a lone .tex file with no \\input keeps identical figure
    discovery (single-file byte-compatibility is otherwise covered by
    tests/skills/latex_paper_en/test_latex_paper_en_scripts.py)."""
    import importlib

    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n\\includegraphics{fig_a}\n\\end{document}\n",
        encoding="utf-8",
    )
    check_figures = importlib.import_module("check_figures")
    checker = check_figures.FigureChecker(tex)
    figures = checker.find_figures()
    assert len(figures) == 1
    assert figures[0]["rel_path"] == "fig_a"


# ── Batch 4b: analyze_grammar / analyze_sentences / improve_expression ─────
# (Tier-1 en+typst byte-identical hash lock; design.md §2.6.)


def _write_writing_modules_project(tmp_path: Path) -> Path:
    """Skeleton main.tex whose Methods section (grammar/sentence/expression
    trigger content) lives entirely in an \\input-ed sub-file. A trailing
    blank line in the sub-file keeps its last paragraph from merging with
    main.tex's own \\end{document} line once assembled (design §2.6 note)."""
    sections = tmp_path / "sections"
    sections.mkdir()
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\input{sections/method}\n\\end{document}\n",
        encoding="utf-8",
    )
    (sections / "method.tex").write_text(
        "\\section{Methods}\n"
        "\n"
        "The data shows strong performance on this benchmark using our approach effectively.\n"
        "\n"
        "We evaluated our proposed transformer-based architecture across multiple challenging "
        "datasets, including weather forecasting, energy consumption, and traffic flow, because "
        "these tasks required careful hyperparameter tuning, although the extensive computational "
        "resources needed to achieve consistently strong and reproducible results across all "
        "evaluated settings and conditions when compared against baselines were substantial.\n"
        "\n"
        "We use a lot of computational resources to test these methods thoroughly.\n"
        "\n",
        encoding="utf-8",
    )
    return main


def test_analyze_grammar_finds_rule_hit_in_included_file(tmp_path: Path) -> None:
    main = _write_writing_modules_project(tmp_path)
    result = _run("analyze_grammar.py", str(main))
    assert "No rule-based issues detected" not in result.stdout
    assert "sections/method.tex:" in result.stdout
    assert "the data shows" in result.stdout.lower()


def test_analyze_sentences_finds_long_sentence_in_included_file(tmp_path: Path) -> None:
    main = _write_writing_modules_project(tmp_path)
    result = _run("analyze_sentences.py", str(main))
    assert "LONG SENTENCE" in result.stdout
    assert "sections/method.tex:" in result.stdout


def test_improve_expression_revised_suggestion_points_to_source_file(tmp_path: Path) -> None:
    main = _write_writing_modules_project(tmp_path)
    result = _run("improve_expression.py", str(main))
    assert "No weak-expression patterns detected" not in result.stdout
    assert "sections/method.tex:" in result.stdout
    assert "Revised:" in result.stdout


def test_analyze_sentences_single_file_line_format_unchanged(tmp_path: Path) -> None:
    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\n"
        "We evaluated our proposed transformer-based architecture across multiple challenging "
        "datasets, including weather forecasting, energy consumption, and traffic flow, because "
        "these tasks required careful hyperparameter tuning, although the extensive computational "
        "resources needed to achieve consistently strong and reproducible results across all "
        "evaluated settings and conditions when compared against baselines were substantial.\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    result = _run("analyze_sentences.py", str(tex))
    assert "LONG SENTENCE (Line 4," in result.stdout
    assert "sections/" not in result.stdout


def test_analyze_grammar_single_file_line_format_unchanged(tmp_path: Path) -> None:
    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\nthe data shows promise.\n\\end{document}\n",
        encoding="utf-8",
    )
    result = _run("analyze_grammar.py", str(tex))
    assert "(Line 3)" in result.stdout
    assert "sections/" not in result.stdout


def test_improve_expression_single_file_line_format_unchanged(tmp_path: Path) -> None:
    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\nWe use a lot of resources.\n\\end{document}\n",
        encoding="utf-8",
    )
    result = _run("improve_expression.py", str(tex))
    assert "(Line 3)" in result.stdout
    assert "sections/" not in result.stdout
