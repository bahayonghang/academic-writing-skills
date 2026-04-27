"""Mechanical pre-submission checks for paper-audit.

The checker intentionally stays deterministic: it reports source/text hygiene
signals that can be verified from the input file and leaves plagiarism,
chartjunk, and scientific validity to reviewer-style lanes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from parsers import extract_abstract, get_parser

EM_DASH = "\u2014"
MODULE = "PRESUBMISSION"
SOURCE_FORMATS = {".tex", ".typ"}


@dataclass
class PreSubmissionIssue:
    """One protocol-compatible pre-submission finding."""

    module: str
    line: int | None
    severity: str
    priority: str
    message: str
    code: str


@dataclass
class LineView:
    """Original and reader-visible line content."""

    number: int
    raw: str
    visible: str


BANNED_TONE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("AI1", r"\binnovative\b"),
    ("AI2", r"\bpioneering\b"),
    ("AI3", r"\brevolutionary\b"),
    ("AI4", r"\btransformative\b"),
    ("AI5", r"\bbreakthrough\b"),
    ("AI6", r"\bunprecedented\b"),
    ("AI7", r"\bremarkable\b"),
    ("AI8", r"\bsuperior\b"),
    ("AI9", r"\bsurpass(?:es|ed|ing)?\b"),
    ("AI10", r"\bstate[- ]of[- ]the[- ]art\b"),
    ("AI11", r"\bhighlights? the potential of\b"),
    ("AI12", r"\bpaves? the way\b"),
    ("AI13", r"\bprofound challenges?\b"),
    ("AI14", r"\bat its essence\b"),
)

ABSTRACT_SIGNALS: dict[str, tuple[str, ...]] = {
    "background": (
        "challenge",
        "problem",
        "need",
        "motivation",
        "important",
        "difficult",
        "recent",
    ),
    "objective": (
        "we propose",
        "we present",
        "this paper",
        "we study",
        "we investigate",
        "aim",
        "objective",
    ),
    "method": (
        "method",
        "approach",
        "framework",
        "model",
        "algorithm",
        "we use",
        "we train",
        "we design",
    ),
    "results": (
        "result",
        "achieve",
        "improve",
        "outperform",
        "reduce",
        "increase",
        "accuracy",
        "f1",
        "rmse",
        "%",
    ),
    "conclusion": (
        "demonstrate",
        "show",
        "suggest",
        "indicate",
        "conclude",
        "implication",
    ),
}

WEAK_TOPIC_STARTERS = (
    "however",
    "moreover",
    "furthermore",
    "in addition",
    "besides",
    "also",
)


def _line_for_offset(content: str, offset: int) -> int:
    """Return a 1-based line number for a character offset."""
    return content.count("\n", 0, max(0, offset)) + 1


def _strip_latex_comment(line: str) -> str:
    """Remove unescaped LaTeX comments from one source line."""
    match = re.search(r"(?<!\\)%", line)
    if not match:
        return line
    return line[: match.start()]


def _strip_latex_comments(content: str) -> str:
    return "\n".join(_strip_latex_comment(line) for line in content.splitlines())


def _read_document(path: Path, pdf_mode: str) -> tuple[str, str, object]:
    fmt = path.suffix.lower()
    parser = get_parser(str(path), pdf_mode=pdf_mode)
    if fmt == ".pdf":
        return parser.extract_text_from_file(str(path)), fmt, parser
    return path.read_text(encoding="utf-8"), fmt, parser


def _line_views(content: str, fmt: str, parser: object) -> list[LineView]:
    views: list[LineView] = []
    for number, raw in enumerate(content.splitlines(), start=1):
        if fmt == ".tex":
            source_line = _strip_latex_comment(raw)
            visible = parser.extract_visible_text(source_line)  # type: ignore[attr-defined]
        elif fmt == ".typ":
            source_line = raw.split("//", 1)[0]
            visible = parser.extract_visible_text(source_line)  # type: ignore[attr-defined]
        else:
            visible = raw.strip()
        views.append(LineView(number=number, raw=raw, visible=visible.strip()))
    return views


def _issue(
    issues: list[PreSubmissionIssue],
    *,
    code: str,
    line: int | None,
    severity: str,
    priority: str,
    message: str,
) -> None:
    issues.append(
        PreSubmissionIssue(
            module=MODULE,
            line=line,
            severity=severity,
            priority=priority,
            message=f"[{code}] {message}",
            code=code,
        )
    )


def _scan_em_dashes(views: list[LineView], issues: list[PreSubmissionIssue]) -> None:
    for view in views:
        if EM_DASH not in view.visible:
            continue
        _issue(
            issues,
            code="G1",
            line=view.number,
            severity="Major",
            priority="P1",
            message=(
                "Em dash found; replace it with a comma, colon, parenthesis, or sentence "
                "boundary unless it is part of a preserved quotation."
            ),
        )


def _scan_ai_tone(views: list[LineView], issues: list[PreSubmissionIssue]) -> None:
    text = "\n".join(view.visible for view in views)
    for code, pattern in BANNED_TONE_PATTERNS:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
        if len(matches) < 3:
            continue
        first_offset = matches[0].start()
        first_line = text.count("\n", 0, first_offset) + 1
        _issue(
            issues,
            code=code,
            line=first_line,
            severity="Major",
            priority="P1",
            message=(
                f"AI-tone term pattern `{pattern}` appears {len(matches)} times; reduce "
                "promotional or template-like wording before submission."
            ),
        )


def _extract_pdf_abstract(content: str) -> str:
    match = re.search(
        r"\babstract\b[:\s]*(.*?)(?=\n\s*(?:1\.?\s*)?introduction\b|\n\s*keywords?\b|\Z)",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return " ".join(lines[:8]).strip()


def _abstract_text(content: str, fmt: str) -> str:
    if fmt == ".pdf":
        return _extract_pdf_abstract(content)
    return extract_abstract(content)


def _scan_abstract(content: str, fmt: str, issues: list[PreSubmissionIssue]) -> None:
    abstract = _abstract_text(content, fmt)
    if not abstract:
        _issue(
            issues,
            code="A0",
            line=None,
            severity="Major",
            priority="P1",
            message="Abstract was not detected; submission packages need a visible abstract.",
        )
        return

    lowered = abstract.lower()
    missing: list[str] = []
    for element, signals in ABSTRACT_SIGNALS.items():
        if not any(signal in lowered for signal in signals):
            missing.append(element)

    has_quantitative_result = bool(re.search(r"\b\d+(?:\.\d+)?\s*(?:%|percent|x)?\b", abstract))
    if "results" not in missing and not has_quantitative_result:
        missing.append("quantitative results")

    if not missing:
        return

    severity = "Major" if any("results" in item for item in missing) else "Minor"
    priority = "P1" if severity == "Major" else "P2"
    _issue(
        issues,
        code="A1",
        line=None,
        severity=severity,
        priority=priority,
        message=(f"Abstract five-element check is incomplete; missing {', '.join(missing)}."),
    )


def _scan_latex_citation_tilde(content: str, issues: list[PreSubmissionIssue]) -> None:
    source = _strip_latex_comments(content)
    cite_re = re.compile(
        r"(?P<prefix>[A-Za-z0-9)\]}])(?P<space>\s*)"
        r"(?P<cite>\\cite\w*\*?(?:\[[^\]]*\]\s*)*\{[^}]+\})"
    )
    for match in cite_re.finditer(source):
        if match.group("space") == "~":
            continue
        _issue(
            issues,
            code="L1",
            line=_line_for_offset(source, match.start("cite")),
            severity="Minor",
            priority="P2",
            message=(
                "LaTeX citation should use a non-breaking tie before citation, e.g. "
                "`Method~\\cite{key}`."
            ),
        )


def _scan_latex_labels(content: str, issues: list[PreSubmissionIssue]) -> None:
    source = _strip_latex_comments(content)
    for match in re.finditer(r"\\label\{([^}]+)\}", source):
        label = match.group(1).strip()
        line = _line_for_offset(source, match.start())
        if " " in label:
            _issue(
                issues,
                code="L2",
                line=line,
                severity="Major",
                priority="P1",
                message=f"LaTeX label `{label}` contains spaces; use compact snake_case labels.",
            )
        if "-" in label:
            _issue(
                issues,
                code="L3",
                line=line,
                severity="Minor",
                priority="P2",
                message=f"LaTeX label `{label}` uses hyphens; prefer underscores for portability.",
            )


def _scan_unreferenced_numbered_equations(
    content: str,
    issues: list[PreSubmissionIssue],
) -> None:
    source = _strip_latex_comments(content)
    env_re = re.compile(
        r"\\begin\{(?P<env>equation|align|gather|multline|eqnarray)\}"
        r"(?P<body>.*?)\\end\{(?P=env)\}",
        flags=re.DOTALL,
    )
    for match in env_re.finditer(source):
        body = match.group("body")
        line = _line_for_offset(source, match.start())
        labels = re.findall(r"\\label\{([^}]+)\}", body)
        if not labels:
            _issue(
                issues,
                code="L4",
                line=line,
                severity="Minor",
                priority="P2",
                message="Numbered equation environment has no label for later reference.",
            )
            continue
        for label in labels:
            ref_re = re.compile(rf"\\(?:eqref|ref|autoref|cref|Cref)\{{{re.escape(label)}\}}")
            ref_count = sum(
                1
                for ref_match in ref_re.finditer(source)
                if not (match.start() <= ref_match.start() <= match.end())
            )
            if ref_count:
                continue
            _issue(
                issues,
                code="L5",
                line=line,
                severity="Minor",
                priority="P2",
                message=f"Numbered equation label `{label}` is never referenced in text.",
            )


def _paragraphs(views: list[LineView]) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    current: list[str] = []
    start_line: int | None = None
    for view in views:
        text = view.visible.strip()
        if not text:
            if current and start_line is not None:
                paragraphs.append((start_line, " ".join(current)))
            current = []
            start_line = None
            continue
        if start_line is None:
            start_line = view.number
        current.append(text)
    if current and start_line is not None:
        paragraphs.append((start_line, " ".join(current)))
    return paragraphs


def _scan_paragraph_shape(views: list[LineView], issues: list[PreSubmissionIssue]) -> None:
    long_count = 0
    weak_topic_count = 0
    for line, paragraph in _paragraphs(views):
        words = re.findall(r"\b[\w'-]+\b", paragraph)
        sentences = [item for item in re.split(r"(?<=[.!?])\s+", paragraph) if item.strip()]
        if len(words) > 180 or len(sentences) > 8:
            long_count += 1
            if long_count <= 5:
                _issue(
                    issues,
                    code="G2",
                    line=line,
                    severity="Minor",
                    priority="P2",
                    message=(
                        f"Long paragraph detected ({len(words)} words, "
                        f"{len(sentences)} sentences); split or add a clearer topic sentence."
                    ),
                )

        first_sentence = sentences[0].strip().lower() if sentences else ""
        if (
            len(words) >= 90
            and len(sentences) >= 3
            and any(first_sentence.startswith(starter) for starter in WEAK_TOPIC_STARTERS)
        ):
            weak_topic_count += 1
            if weak_topic_count <= 5:
                _issue(
                    issues,
                    code="G3",
                    line=line,
                    severity="Minor",
                    priority="P2",
                    message=(
                        "Paragraph begins with a transition rather than a claim-like topic "
                        "sentence; verify the local argument chain."
                    ),
                )


def _strip_latex_markup(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    return re.sub(r"\s+", " ", text.replace("{", " ").replace("}", " ")).strip()


def _scan_latex_captions(content: str, issues: list[PreSubmissionIssue]) -> None:
    source = _strip_latex_comments(content)
    caption_re = re.compile(r"\\caption(?:\[[^\]]*\])?\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}")
    for match in caption_re.finditer(source):
        caption = _strip_latex_markup(match.group(1))
        line = _line_for_offset(source, match.start())
        _check_caption_text(caption, line, issues)


def _scan_typst_captions(content: str, issues: list[PreSubmissionIssue]) -> None:
    caption_re = re.compile(
        r"caption\s*:\s*(?:\[(?P<bracket>[^\]]+)\]|\"(?P<string>[^\"]+)\")",
        flags=re.DOTALL,
    )
    for match in caption_re.finditer(content):
        caption = re.sub(r"\s+", " ", match.group("bracket") or match.group("string") or "")
        _check_caption_text(caption, _line_for_offset(content, match.start()), issues)


def _check_caption_text(
    caption: str,
    line: int,
    issues: list[PreSubmissionIssue],
) -> None:
    words = re.findall(r"\b[\w'-]+\b", caption)
    lowered = caption.lower()
    has_specific_finding = bool(
        re.search(r"\b\d+(?:\.\d+)?\b", caption)
        or re.search(
            r"\b(improves?|reduces?|increases?|shows?|compares?|outperforms?|drops?|rises?)\b",
            lowered,
        )
    )
    generic_start = re.match(r"^(figure|this figure|results?|comparison)\s", lowered)
    if len(words) < 5 or (generic_start and not has_specific_finding):
        _issue(
            issues,
            code="F1",
            line=line,
            severity="Minor",
            priority="P2",
            message=(
                "Caption lacks a concrete finding or comparison cue; add the specific result "
                "the figure/table is meant to communicate."
            ),
        )


def run_checks(path: str | Path, pdf_mode: str = "basic") -> list[PreSubmissionIssue]:
    """Run deterministic pre-submission checks and return issue objects."""
    source_path = Path(path)
    content, fmt, parser = _read_document(source_path, pdf_mode)
    views = _line_views(content, fmt, parser)
    issues: list[PreSubmissionIssue] = []

    _scan_em_dashes(views, issues)
    _scan_ai_tone(views, issues)
    _scan_abstract(content, fmt, issues)
    _scan_paragraph_shape(views, issues)

    if fmt == ".tex":
        _scan_latex_citation_tilde(content, issues)
        _scan_latex_labels(content, issues)
        _scan_unreferenced_numbered_equations(content, issues)
        _scan_latex_captions(content, issues)
    elif fmt == ".typ":
        _scan_typst_captions(content, issues)

    return issues


def _format_protocol_issue(issue: PreSubmissionIssue) -> str:
    loc = f"(Line {issue.line}) " if issue.line is not None else ""
    return (
        f"% {MODULE} {loc}[Severity: {issue.severity}] "
        f"[Priority: {issue.priority}]: {issue.message}"
    )


def _render_protocol(
    issues: list[PreSubmissionIssue],
    *,
    fmt: str,
) -> str:
    lines = [_format_protocol_issue(issue) for issue in issues]
    if fmt == ".pdf":
        lines.append(
            "# PRESUBMISSION: PDF input; skipped source-only LaTeX/Typst checks "
            "(citation ties, labels, numbered equations, source captions)."
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run mechanical pre-submission checks.")
    parser.add_argument("paper", help="Path to .tex, .typ, or .pdf paper")
    parser.add_argument("--pdf-mode", choices=["basic", "enhanced"], default="basic")
    parser.add_argument("--json", action="store_true", help="Emit JSON issue list")
    args = parser.parse_args(argv)

    path = Path(args.paper).resolve()
    if not path.exists():
        print(f"File not found: {args.paper}", file=sys.stderr)
        return 2
    if path.suffix.lower() not in {".tex", ".typ", ".pdf"}:
        print(f"Unsupported format: {path.suffix}", file=sys.stderr)
        return 2

    issues = run_checks(path, pdf_mode=args.pdf_mode)
    if args.json:
        print(json.dumps([asdict(issue) for issue in issues], indent=2, ensure_ascii=False))
    else:
        output = _render_protocol(issues, fmt=path.suffix.lower())
        if output:
            print(output)

    return 1 if any(issue.severity == "Critical" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
