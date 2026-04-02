"""Tests for analyze_abstract.py (latex-paper-en)."""

import tempfile
from pathlib import Path

from analyze_abstract import AbstractAnalyzer
from conftest import SCRIPT_DIR_EN  # noqa: F401 (triggers sys.path setup)


def _write_tex(content: str) -> Path:
    """Write content to a temp .tex file and return the path."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)


FULL_ABSTRACT = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Despite growing interest in neural architecture search, limited research has addressed
its application to edge devices. This study aims to investigate efficient NAS methods
for resource-constrained environments. We propose a lightweight search framework
evaluated on the CIFAR-10 and ImageNet datasets using a novel proxy metric. Results
show that our approach achieves 94.2\% accuracy while reducing search time by 3.5x
compared to state-of-the-art methods. Our findings suggest that proxy-based NAS can
enable practical deployment on mobile devices, advancing the field of efficient AI.
\end{abstract}
\end{document}
"""

MISSING_RESULTS = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Despite growing interest in neural architecture search, limited research has addressed
its application to edge devices. This study aims to investigate efficient NAS methods
for resource-constrained environments. We propose a lightweight search framework
evaluated on the CIFAR-10 dataset. Our results demonstrate that the method performs well
compared to baselines. Our findings suggest practical deployment on mobile devices.
\end{abstract}
\end{document}
"""

VAGUE_OBJECTIVE = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Despite challenges in deep learning, in this paper we study neural networks.
We use a model trained on a dataset. Results show that accuracy improved to 92.1\%.
Our work contributes to the field.
\end{abstract}
\end{document}
"""

CHINESE_ABSTRACT = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
近年来，深度学习在工业领域日益增长。然而，现有方法在边缘部署方面研究不足。
本文旨在提出一种轻量级模型压缩框架。采用知识蒸馏方法，在CIFAR-10数据集上进行评估。
结果表明，本方法达到94.2\%的准确率，较基线提高3.5\%。
研究发现表明，该方法可用于实际工业部署，具有重要意义。
\end{abstract}
\end{document}
"""

NO_ABSTRACT = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
Hello world.
\end{document}
"""

LONG_ABSTRACT = (
    r"""
\documentclass{article}
\begin{document}
\begin{abstract}
"""
    + " ".join(["word"] * 300)
    + r"""
\end{abstract}
\end{document}
"""
)


def test_abstract_all_elements_present() -> None:
    path = _write_tex(FULL_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        assert result["status"] == "PASS"
        for key in ["background", "objective", "methods", "results", "conclusion"]:
            assert result["elements"][key]["status"] == "PRESENT", f"{key} should be PRESENT"
    finally:
        path.unlink(missing_ok=True)


def test_abstract_missing_results_data() -> None:
    path = _write_tex(MISSING_RESULTS)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        # Results should be VAGUE because "performs well" has no numbers
        assert result["elements"]["results"]["status"] == "VAGUE"
    finally:
        path.unlink(missing_ok=True)


def test_abstract_vague_objective() -> None:
    path = _write_tex(VAGUE_OBJECTIVE)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        assert result["elements"]["objective"]["status"] == "VAGUE"
    finally:
        path.unlink(missing_ok=True)


def test_abstract_chinese_detection() -> None:
    path = _write_tex(CHINESE_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        assert result["language"] == "zh"
        assert result["elements"]["background"]["status"] == "PRESENT"
        assert result["elements"]["methods"]["status"] == "PRESENT"
        assert result["elements"]["results"]["status"] == "PRESENT"
    finally:
        path.unlink(missing_ok=True)


def test_abstract_no_abstract_found() -> None:
    path = _write_tex(NO_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        assert result["status"] == "ERROR"
        assert "No abstract" in result["message"]
    finally:
        path.unlink(missing_ok=True)


def test_abstract_word_count_over() -> None:
    path = _write_tex(LONG_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path), max_words=250)
        result = analyzer.analyze()
        assert result["count"]["status"] == "WARNING"
        assert result["count"]["count"] > 250
    finally:
        path.unlink(missing_ok=True)


def test_abstract_file_not_found() -> None:
    analyzer = AbstractAnalyzer("nonexistent.tex")
    result = analyzer.analyze()
    assert result["status"] == "ERROR"


def test_abstract_report_format() -> None:
    path = _write_tex(FULL_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        report = analyzer.generate_report(result)
        assert "Abstract Structure Diagnosis" in report
        assert "PRESENT" in report
    finally:
        path.unlink(missing_ok=True)


def test_abstract_json_output_structure() -> None:
    path = _write_tex(FULL_ABSTRACT)
    try:
        analyzer = AbstractAnalyzer(str(path))
        result = analyzer.analyze()
        assert "elements" in result
        assert "count" in result
        assert "status" in result
        assert "language" in result
        for key in ["background", "objective", "methods", "results", "conclusion"]:
            elem = result["elements"][key]
            assert "status" in elem
            assert "evidence" in elem
            assert "suggestion" in elem
    finally:
        path.unlink(missing_ok=True)
