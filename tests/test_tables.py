"""Tests for check_tables.py and generate_table.py (latex-paper-en)."""

import json
import tempfile
from pathlib import Path

from check_tables import TableChecker
from conftest import SCRIPT_DIR_EN  # noqa: F401 (triggers sys.path setup)
from generate_table import TableGenerator, load_csv, load_json

# --- TableChecker tests ---


def _write_tex(content: str) -> Path:
    """Write content to a temp .tex file and return the path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


VALID_THREE_LINE = r"""
\documentclass{article}
\usepackage{booktabs}
\begin{document}
\begin{table}[t]
  \caption{Model comparison.}
  \label{tab:cmp}
  \centering
  \begin{tabular}{lcc}
    \toprule
    Model & Accuracy & F1 \\
    \midrule
    Baseline & 85.3 & 83.7 \\
    Ours     & 91.2 & 90.3 \\
    \bottomrule
  \end{tabular}
\end{table}
\end{document}
"""

VERTICAL_LINES = r"""
\documentclass{article}
\usepackage{booktabs}
\begin{document}
\begin{table}[t]
  \caption{Bad table.}
  \begin{tabular}{|c|c|c|}
    \toprule
    A & B & C \\
    \midrule
    1 & 2 & 3 \\
    \bottomrule
  \end{tabular}
\end{table}
\end{document}
"""

HLINE_TABLE = r"""
\documentclass{article}
\begin{document}
\begin{table}[t]
  \caption{Old style.}
  \begin{tabular}{ccc}
    \hline
    A & B & C \\
    \hline
    1 & 2 & 3 \\
    \hline
  \end{tabular}
\end{table}
\end{document}
"""

CAPTION_AFTER = r"""
\documentclass{article}
\usepackage{booktabs}
\begin{document}
\begin{table}[t]
  \begin{tabular}{lc}
    \toprule
    X & Y \\
    \midrule
    1 & 2 \\
    \bottomrule
  \end{tabular}
  \caption{Caption after tabular.}
\end{table}
\end{document}
"""


def test_check_tables_valid_booktabs() -> None:
    path = _write_tex(VALID_THREE_LINE)
    try:
        checker = TableChecker(str(path))
        result = checker.check()
        assert result["status"] == "PASS"
        assert result["table_count"] == 1
        assert result["issue_count"] == 0
    finally:
        path.unlink(missing_ok=True)


def test_check_tables_vertical_lines() -> None:
    path = _write_tex(VERTICAL_LINES)
    try:
        checker = TableChecker(str(path))
        result = checker.check()
        assert result["status"] == "FAIL"
        categories = [i["category"] for i in result["issues"]]
        assert "vertical_lines" in categories
    finally:
        path.unlink(missing_ok=True)


def test_check_tables_hline_warns() -> None:
    path = _write_tex(HLINE_TABLE)
    try:
        checker = TableChecker(str(path))
        result = checker.check()
        assert result["status"] == "WARNING"
        categories = [i["category"] for i in result["issues"]]
        assert "hline" in categories or "booktabs_missing" in categories
    finally:
        path.unlink(missing_ok=True)


def test_check_tables_caption_position() -> None:
    path = _write_tex(CAPTION_AFTER)
    try:
        checker = TableChecker(str(path))
        result = checker.check()
        categories = [i["category"] for i in result["issues"]]
        assert "caption_position" in categories
    finally:
        path.unlink(missing_ok=True)


def test_check_tables_fix_suggestions() -> None:
    path = _write_tex(VERTICAL_LINES)
    try:
        checker = TableChecker(str(path))
        result = checker.check(fix_suggestions=True)
        for issue in result["issues"]:
            assert "fix" in issue
    finally:
        path.unlink(missing_ok=True)


def test_check_tables_file_not_found() -> None:
    checker = TableChecker("nonexistent.tex")
    result = checker.check()
    assert result["status"] == "FAIL"
    assert result["issues"][0]["category"] == "file"


# --- TableGenerator tests ---


def test_generate_table_markdown() -> None:
    gen = TableGenerator()
    result = gen.generate(
        headers=["Model", "Acc", "F1"],
        rows=[["Baseline", "85.3", "83.7"], ["Ours", "91.2", "90.3"]],
    )
    md = result["markdown"]
    assert "Model" in md
    assert "85.3" in md
    assert md.count("|") > 0


def test_generate_table_latex() -> None:
    gen = TableGenerator()
    result = gen.generate(
        headers=["Model", "Acc", "F1"],
        rows=[["Baseline", "85.3", "83.7"], ["Ours", "91.2", "90.3"]],
        caption_en="Test caption.",
    )
    latex = result["latex"]
    assert r"\toprule" in latex
    assert r"\midrule" in latex
    assert r"\bottomrule" in latex
    assert r"\begin{table}" in latex
    assert r"\caption{Test caption.}" in latex


def test_generate_table_bilingual() -> None:
    gen = TableGenerator()
    result = gen.generate(
        headers=["Model", "Precision", "Recall"],
        rows=[["A", "90.0", "88.0"]],
        bilingual=True,
    )
    assert "captions" in result
    assert "en" in result["captions"]
    assert "zh" in result["captions"]


def test_generate_table_stats_note() -> None:
    gen = TableGenerator()
    result = gen.generate(
        headers=["Model", "Acc"],
        rows=[["A", "90.0"]],
        stats=True,
    )
    assert "stats_note" in result
    assert "p < 0.05" in result["stats_note"]


def test_generate_table_word_tip() -> None:
    gen = TableGenerator()
    result = gen.generate(headers=["A"], rows=[["1"]])
    assert "word_tip" in result
    assert "Word" in result["word_tip"]


def test_load_csv_from_file() -> None:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write("Model,Acc,F1\nA,90.0,88.0\nB,91.0,89.0\n")
        name = f.name
    try:
        headers, rows = load_csv(name)
        assert headers == ["Model", "Acc", "F1"]
        assert len(rows) == 2
    finally:
        Path(name).unlink(missing_ok=True)


def test_load_json_from_file() -> None:
    data = {"headers": ["X", "Y"], "rows": [["1", "2"]]}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        name = f.name
    try:
        headers, rows = load_json(name)
        assert headers == ["X", "Y"]
        assert rows == [["1", "2"]]
    finally:
        Path(name).unlink(missing_ok=True)
