"""Regression tests for --section alias unification (A-EN-2 / A-EN-5).

``analyze_logic.py``, ``analyze_literature.py``, and ``deai_batch.py`` each
had their own ad-hoc ``section.lower()`` lookup instead of routing through
``parsers.resolve_section_keys`` (the alias table ``deai_check.py`` already
used). A canonical key like ``method`` never matched loose synonyms like
``methods``, so SKILL.md's own example commands failed with a bare
"Section not found" instead of resolving the alias.
"""

from __future__ import annotations

import importlib
import re
import sys

import pytest

logic_module = importlib.import_module("analyze_logic")
literature_module = importlib.import_module("analyze_literature")
deai_batch_module = importlib.import_module("deai_batch")


_METHODS_TEX = r"""\documentclass{article}
\begin{document}
\section{Methods}
We use a three-layer model because it improves throughput.
\end{document}
"""

_RELATED_WORK_TEX = r"""\documentclass{article}
\begin{document}
\section{Related Work}
Smith et al. \cite{smith2020} proposed a convolutional baseline.
Jones et al. \cite{jones2021} introduced a transformer variant.
Lee et al. \cite{lee2022} designed a hybrid architecture for the same task.
Wang et al. \cite{wang2023} extended the benchmark with larger datasets.
\end{document}
"""


# ── analyze_logic.py ───────────────────────────────────────────────────────


def test_analyze_logic_accepts_methods_alias(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_METHODS_TEX, encoding="utf-8")
    findings = logic_module.analyze(tex, "methods")
    joined = "\n".join(findings).lower()
    assert "section not found" not in joined


_ENUMERATION_TEX = r"""\documentclass{article}
\begin{document}
\section{Related Work}
In 2019, Smith et al. proposed a novel attention mechanism for sequence modeling.
In 2020, Jones et al. introduced a graph-based approach for document classification.
In 2021, Wang et al. presented a hybrid method combining transformers and CNNs.
In 2022, Li et al. developed an efficient pruning strategy for large models.
\end{document}
"""


def test_analyze_logic_related_work_alias_runs_a1_a3_checks(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_ENUMERATION_TEX, encoding="utf-8")
    findings = logic_module.analyze(tex, "related work")
    joined = "\n".join(findings).lower()
    assert "section not found" not in joined
    assert "enumeration" in joined


def test_analyze_logic_unknown_section_lists_available(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_METHODS_TEX, encoding="utf-8")
    findings = logic_module.analyze(tex, "nonexistent")
    joined = "\n".join(findings)
    assert "Section not found" in joined
    assert "available" in joined.lower()
    assert "method" in joined


def test_analyze_logic_scans_duplicate_method_sections(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Methods}
We use a three-layer model.
\section{Methods}
We use a second stage model.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, "methods")
    joined = "\n".join(findings)
    # Both duplicate "method"/"method_2" ranges must be scanned: each
    # unjustified "we use ..." statement produces its own METHODOLOGY finding.
    assert joined.count("three-layer model") == 1
    assert joined.count("second stage model") == 1


# ── analyze_literature.py ──────────────────────────────────────────────────


def test_analyze_literature_accepts_related_work_alias(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_RELATED_WORK_TEX, encoding="utf-8")
    findings = literature_module.analyze(tex, "related work")
    joined = "\n".join(findings).lower()
    assert "section not found" not in joined
    assert "needs review" in joined


def test_analyze_literature_accepts_literature_alias(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_RELATED_WORK_TEX, encoding="utf-8")
    findings = literature_module.analyze(tex, "literature")
    joined = "\n".join(findings).lower()
    assert "section not found" not in joined


def test_analyze_literature_default_related_behavior_unchanged(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_RELATED_WORK_TEX, encoding="utf-8")
    findings = literature_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "section not found" not in joined
    assert "needs review" in joined


def test_analyze_literature_unknown_section_lists_available(tmp_path):
    tex = tmp_path / "main.tex"
    tex.write_text(_RELATED_WORK_TEX, encoding="utf-8")
    findings = literature_module.analyze(tex, "nonexistent")
    joined = "\n".join(findings)
    assert "Section not found" in joined
    assert "available" in joined.lower()
    assert "related" in joined


# ── deai_batch.py ───────────────────────────────────────────────────────────


def test_deai_batch_cli_unknown_section_lists_available(tmp_path, capsys, monkeypatch):
    tex = tmp_path / "main.tex"
    tex.write_text(_METHODS_TEX, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["deai_batch.py", str(tex), "--section", "nope"])
    with pytest.raises(SystemExit) as exc_info:
        deai_batch_module.main()
    assert exc_info.value.code == 1
    output = capsys.readouterr().out
    assert re.search(r"available", output, re.IGNORECASE)


def test_deai_batch_cli_section_methods_alias_found(tmp_path, capsys, monkeypatch):
    tex = tmp_path / "main.tex"
    tex.write_text(_METHODS_TEX, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["deai_batch.py", str(tex), "--section", "methods"])
    deai_batch_module.main()
    output = capsys.readouterr().out
    assert "Section not found" not in output
    assert "Section: method" in output
