"""Mechanical pre-submission checks for cover-letter.

The checker stays deterministic: it reports text hygiene signals that can be
verified from the cover letter file (and the active journal template), leaving
claim-evidence alignment to ``align_check.py`` and journal-fit scoring to
``journal_fit_check.py``.

Adapted from ``paper-audit/scripts/pre_submission_check.py``:
* keeps ``_scan_em_dashes`` / ``_scan_ai_tone`` / ``_scan_paragraph_shape``
* drops LaTeX label / equation / citation-tilde / caption scans
* adds ``_scan_required_declarations`` (driven by template frontmatter)
* adds ``_scan_length`` (configurable per template)
* adds ``_scan_letter_opener_cliches``
* adds ``_scan_journal_specific_phrases``
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml
from parsers import LatexParser

EM_DASH = "—"
MODULE = "PRESUBMISSION"
SOURCE_FORMATS = {".tex", ".md"}


@dataclass
class PreSubmissionIssue:
    """One protocol-compatible pre-submission finding."""

    module: str
    line: int | None
    severity: str
    priority: str
    message: str
    code: str
    source_kind: str = "script"
    comment_type: str = "presentation"
    title: str = ""
    quote: str = ""
    explanation: str = ""


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

LETTER_OPENER_CLICHES: tuple[tuple[str, str], ...] = (
    ("L2a", r"^\s*we are (?:pleased|excited|delighted|honored) to submit\b"),
    ("L2b", r"^\s*we hereby submit\b"),
    ("L2c", r"^\s*please find (?:enclosed|attached)\b"),
    ("L2d", r"^\s*enclosed please find\b"),
    ("L2e", r"^\s*it is our (?:great )?pleasure to submit\b"),
)

LETTER_BANNED_PHRASES: tuple[tuple[str, str], ...] = (
    ("J1a", r"\bnovel and innovative\b"),
    ("J1b", r"\bgroundbreaking\b"),
    ("J1c", r"\bfirst[- ]of[- ]its[- ]kind\b"),
    ("J1d", r"\bgame[- ]changing\b"),
    ("J1e", r"\bparadigm shift\b"),
    ("J1f", r"\bcutting[- ]edge\b"),
    ("J1g", r"\bof great interest\b"),
    ("J1h", r"\bwill be of broad interest\b"),
)

DECLARATION_PATTERNS: dict[str, tuple[str, ...]] = {
    "originality": (
        r"not (?:been )?published elsewhere",
        r"not under (?:concurrent )?(?:consideration|review|submission)",
        r"original (?:research|work|manuscript)",
    ),
    "dual_submission": (
        r"not (?:currently )?(?:under (?:concurrent )?(?:consideration|submission|review)|submitted)(?:\s+elsewhere)?",
        r"single submission policy",
        r"(?:dual|multiple) submission",
        r"not (?:been )?submitted (?:to|elsewhere)",
        r"concurrent consideration",
    ),
    "competing_interests": (
        r"(?:no |declare(?:s)? (?:no |the following )?)?competing interests?",
        r"conflicts? of interest",
        r"declare(?:s)? no (?:competing|conflict)",
    ),
    "data_availability": (
        r"data (?:will be |are |is )?(?:made )?available",
        r"code (?:will be |is )?(?:made )?available",
        r"materials (?:are|will be) available",
        r"data and code",
        r"data availability statement",
    ),
    "ethics_irb": (
        r"institutional review board",
        r"\bIRB\b",
        r"\bIACUC\b",
        r"ethics? (?:committee|approval|board)",
        r"clinical trial (?:registration|number|identifier)",
        r"informed consent",
    ),
    "authorship": (
        r"all authors (?:have )?approved",
        r"all authors (?:have )?read and approved",
        r"authorship agreement",
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


def _strip_latex_comment(line: str) -> str:
    """Remove unescaped LaTeX comments from one source line."""
    match = re.search(r"(?<!\\)%", line)
    if not match:
        return line
    return line[: match.start()]


def _read_letter(path: Path) -> tuple[str, str]:
    """Return ``(content, fmt)``. fmt is ``.tex`` or ``.md``."""
    fmt = path.suffix.lower()
    return path.read_text(encoding="utf-8"), fmt


def _line_views(content: str, fmt: str) -> list[LineView]:
    parser = LatexParser() if fmt == ".tex" else None
    views: list[LineView] = []
    for number, raw in enumerate(content.splitlines(), start=1):
        if fmt == ".tex" and parser is not None:
            source_line = _strip_latex_comment(raw)
            visible = parser.extract_visible_text(source_line)
        else:
            # Markdown / plain text: strip leading heading markers and bold/italic
            cleaned = re.sub(r"^#+\s+", "", raw)
            cleaned = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", cleaned)
            visible = cleaned.strip()
        views.append(LineView(number=number, raw=raw, visible=visible.strip()))
    return views


def _visible_text(views: list[LineView]) -> str:
    return "\n".join(view.visible for view in views)


def _issue(
    issues: list[PreSubmissionIssue],
    *,
    code: str,
    line: int | None,
    severity: str,
    priority: str,
    message: str,
    quote: str = "",
) -> None:
    normalized_severity = severity.lower()
    comment_type = _comment_type_for_code(code)
    title = _title_for_code(code)
    issues.append(
        PreSubmissionIssue(
            module=MODULE,
            line=line,
            severity=normalized_severity,
            priority=priority,
            message=f"[{code}] {message}",
            code=code,
            comment_type=comment_type,
            title=title,
            quote=quote[:280],
            explanation=message,
        )
    )


def _comment_type_for_code(code: str) -> str:
    if code.startswith("D-"):
        return "declaration_missing"
    if code.startswith(("AI", "J1", "L2")):
        return "tone"
    return "presentation"


def _title_for_code(code: str) -> str:
    if code.startswith("D-"):
        return "Required declaration is missing"
    if code.startswith("AI"):
        return "Repeated promotional or AI-tone wording"
    if code.startswith("J1"):
        return "Cover-letter cliché phrase"
    if code.startswith("L2"):
        return "Low-specificity opener"
    if code == "L1":
        return "Cover letter exceeds template word limit"
    if code == "G1":
        return "Em dash in visible prose"
    if code == "G2":
        return "Paragraph is too long for a cover letter"
    if code == "G3":
        return "Paragraph starts with a weak transition"
    return "Pre-submission presentation issue"


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
                "Em dash found; replace it with a comma, colon, parenthesis, or sentence boundary."
            ),
            quote=view.visible,
        )


def _scan_ai_tone(views: list[LineView], issues: list[PreSubmissionIssue]) -> None:
    text = _visible_text(views)
    for code, pattern in BANNED_TONE_PATTERNS:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
        if len(matches) < 3:
            continue
        first_line = text.count("\n", 0, matches[0].start()) + 1
        _issue(
            issues,
            code=code,
            line=first_line,
            severity="Major",
            priority="P1",
            message=(
                f"AI-tone term pattern `{pattern}` appears {len(matches)} times; reduce "
                "promotional or template-like wording."
            ),
            quote=text[matches[0].start() : matches[0].end()],
        )


def _scan_letter_banned_phrases(
    views: list[LineView],
    issues: list[PreSubmissionIssue],
) -> None:
    text = _visible_text(views)
    for code, pattern in LETTER_BANNED_PHRASES:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
        if not matches:
            continue
        first_line = text.count("\n", 0, matches[0].start()) + 1
        severity = "Major" if len(matches) >= 3 else "Minor"
        priority = "P1" if severity == "Major" else "P2"
        _issue(
            issues,
            code=code,
            line=first_line,
            severity=severity,
            priority=priority,
            message=(
                f"Cover-letter cliché `{pattern}` appears {len(matches)} time(s); "
                "editors discount template-style wording."
            ),
            quote=text[matches[0].start() : matches[0].end()],
        )


def _scan_letter_opener_cliches(
    views: list[LineView],
    issues: list[PreSubmissionIssue],
) -> None:
    # The opener is the first non-empty visible line (post-salutation).
    salutation_re = re.compile(r"^\s*dear\b", flags=re.IGNORECASE)
    opener_view: LineView | None = None
    seen_salutation = False
    for view in views:
        text = view.visible.strip()
        if not text:
            continue
        if not seen_salutation and salutation_re.match(text):
            seen_salutation = True
            continue
        opener_view = view
        break
    if opener_view is None:
        return
    for code, pattern in LETTER_OPENER_CLICHES:
        if re.match(pattern, opener_view.visible, flags=re.IGNORECASE):
            _issue(
                issues,
                code=code,
                line=opener_view.number,
                severity="Minor",
                priority="P2",
                message=(
                    "Cover letter opens with a low-effort cliché; replace with a specific "
                    "manuscript-title + central-finding opener."
                ),
                quote=opener_view.visible,
            )
            return


def _scan_required_declarations(
    text: str,
    template_meta: dict[str, Any] | None,
    issues: list[PreSubmissionIssue],
) -> None:
    if not template_meta:
        return
    required = template_meta.get("required_declarations") or []
    optional = template_meta.get("optional_declarations") or []
    for kind in required:
        patterns = DECLARATION_PATTERNS.get(kind, ())
        if any(re.search(p, text, flags=re.IGNORECASE) for p in patterns):
            continue
        _issue(
            issues,
            code=f"D-{kind}",
            line=None,
            severity="Major",
            priority="P1",
            message=(
                f"Required declaration `{kind}` is missing; the active template lists it "
                "as required and editors at this venue check for it."
            ),
        )
    for kind in optional:
        patterns = DECLARATION_PATTERNS.get(kind, ())
        if any(re.search(p, text, flags=re.IGNORECASE) for p in patterns):
            continue
        _issue(
            issues,
            code=f"D-{kind}-opt",
            line=None,
            severity="Minor",
            priority="P3",
            message=(
                f"Optional declaration `{kind}` is absent; consider adding it if the "
                "manuscript context requires."
            ),
        )


def _count_visible_words(text: str) -> int:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return 0
    return len(re.findall(r"\b[\w'-]+\b", cleaned))


def _scan_length(
    views: list[LineView],
    template_meta: dict[str, Any] | None,
    issues: list[PreSubmissionIssue],
) -> None:
    if not template_meta or not template_meta.get("word_limit"):
        return
    limit = int(template_meta["word_limit"])
    visible_text = _visible_text(views)
    word_count = _count_visible_words(visible_text)
    if word_count <= limit:
        return
    ratio = word_count / limit
    severity = "Major" if ratio >= 1.20 else "Minor"
    priority = "P1" if severity == "Major" else "P2"
    _issue(
        issues,
        code="L1",
        line=None,
        severity=severity,
        priority=priority,
        message=(
            f"Cover letter has {word_count} words; template ceiling is {limit}. "
            f"Tighten by {word_count - limit} words."
        ),
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
        if len(words) > 120 or len(sentences) > 6:
            long_count += 1
            if long_count <= 5:
                _issue(
                    issues,
                    code="G2",
                    line=line,
                    severity="Minor",
                    priority="P2",
                    message=(
                        f"Long paragraph ({len(words)} words, {len(sentences)} sentences) — "
                        "cover letters read tighter when paragraphs stay under 120 words."
                    ),
                    quote=paragraph,
                )

        first_sentence = sentences[0].strip().lower() if sentences else ""
        if (
            len(words) >= 60
            and len(sentences) >= 2
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
                        "Paragraph begins with a transition rather than a claim; verify the "
                        "local argument chain."
                    ),
                    quote=sentences[0].strip() if sentences else paragraph,
                )


def _load_template_meta(skill_dir: Path, journal: str | None) -> dict[str, Any] | None:
    if not journal:
        return None
    candidate = skill_dir / "templates" / f"{journal}.md"
    if not candidate.exists():
        candidate = skill_dir / "templates" / "generic.md"
    if not candidate.exists():
        return None
    text = candidate.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    frontmatter = text[3:end]
    try:
        meta = yaml.safe_load(frontmatter)
        if isinstance(meta, dict):
            return meta
    except yaml.YAMLError:
        return None
    return None


def run_checks(
    path: str | Path,
    *,
    journal: str | None = None,
    skill_dir: Path | None = None,
) -> list[PreSubmissionIssue]:
    """Run deterministic pre-submission checks and return issue objects."""
    source_path = Path(path)
    content, fmt = _read_letter(source_path)
    views = _line_views(content, fmt)
    issues: list[PreSubmissionIssue] = []

    template_meta: dict[str, Any] | None = None
    if journal and skill_dir is not None:
        template_meta = _load_template_meta(skill_dir, journal)

    _scan_em_dashes(views, issues)
    _scan_ai_tone(views, issues)
    _scan_letter_opener_cliches(views, issues)
    _scan_letter_banned_phrases(views, issues)
    _scan_required_declarations(_visible_text(views), template_meta, issues)
    _scan_length(views, template_meta, issues)
    _scan_paragraph_shape(views, issues)

    return issues


def _format_protocol_issue(issue: PreSubmissionIssue) -> str:
    loc = f"(Line {issue.line}) " if issue.line is not None else ""
    return (
        f"% {MODULE} {loc}[Severity: {issue.severity}] "
        f"[Priority: {issue.priority}]: {issue.message}"
    )


def _render_protocol(issues: list[PreSubmissionIssue]) -> str:
    return "\n".join(_format_protocol_issue(issue) for issue in issues)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run mechanical pre-submission checks on a cover letter."
    )
    parser.add_argument("letter", help="Path to the cover letter (.md or .tex)")
    parser.add_argument(
        "--journal",
        help="Active journal template (nature|science|cell|ieee-trans|acm|"
        "springer-lncs|neurips|icml|cvpr|generic); enables declaration + length checks",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON issue list")
    args = parser.parse_args(argv)

    path = Path(args.letter).resolve()
    if not path.exists():
        print(f"File not found: {args.letter}", file=sys.stderr)
        return 2
    if path.suffix.lower() not in SOURCE_FORMATS:
        print(f"Unsupported format: {path.suffix}; expected .md or .tex", file=sys.stderr)
        return 2

    skill_dir = Path(__file__).resolve().parent.parent
    issues = run_checks(path, journal=args.journal, skill_dir=skill_dir)

    if args.json:
        print(json.dumps([asdict(issue) for issue in issues], indent=2, ensure_ascii=False))
    else:
        output = _render_protocol(issues)
        if output:
            print(output)

    if any(issue.severity == "major" for issue in issues):
        return 2
    if issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
