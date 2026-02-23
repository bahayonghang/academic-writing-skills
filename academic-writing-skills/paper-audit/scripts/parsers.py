"""
Parser re-exports for Paper Audit skill.
Provides unified access to DocumentParser, LatexParser, TypstParser,
and the get_parser factory from sibling skills.
"""

import importlib.util
from pathlib import Path
from typing import Any

# Load sibling parsers module by explicit file path to avoid name collision
_SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
_SIBLING_PARSERS = _SKILLS_ROOT / "latex-paper-en" / "scripts" / "parsers.py"

_spec = importlib.util.spec_from_file_location("_sibling_parsers", _SIBLING_PARSERS)
_sibling = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sibling)

# Re-export core parser classes
DocumentParser = _sibling.DocumentParser
LatexParser = _sibling.LatexParser
TypstParser = _sibling.TypstParser
extract_title = _sibling.extract_title
extract_abstract = _sibling.extract_abstract
extract_latex_citation_keys = getattr(_sibling, "extract_latex_citation_keys", None)


def get_parser(file_path: Any, pdf_mode: str = "basic") -> "DocumentParser":
    """
    Extended factory method supporting PDF in addition to LaTeX/Typst.

    Args:
        file_path: Path to the document file.
        pdf_mode: PDF extraction mode - "basic" (pymupdf) or "enhanced" (pymupdf4llm).

    Returns:
        Appropriate DocumentParser instance.

    Raises:
        ValueError: If the file format is not supported.
    """
    path_str = str(file_path).lower()

    if path_str.endswith(".typ"):
        return TypstParser()
    elif path_str.endswith(".tex"):
        return LatexParser()
    elif path_str.endswith(".pdf"):
        from pdf_parser import PdfParser
        return PdfParser(mode=pdf_mode)
    else:
        raise ValueError(
            f"Unsupported format: {Path(file_path).suffix}. "
            "Supported formats: .tex, .typ, .pdf"
        )


__all__ = [
    "DocumentParser",
    "LatexParser",
    "TypstParser",
    "get_parser",
    "extract_title",
    "extract_abstract",
    "extract_latex_citation_keys",
]
