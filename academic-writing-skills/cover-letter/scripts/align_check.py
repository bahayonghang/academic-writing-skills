"""Cross-cutting align-check orchestrator.

Verifies that claims in a cover letter are supported by visible evidence in the
corresponding LaTeX manuscript. Pipes ``extract_manuscript_facts`` →
``build_letter_claim_map`` → ``verify_letter_against_manuscript``, then emits
findings using the simplified cover-letter ISSUE_SCHEMA.

Importable as a module by ``generate`` and ``optimize`` flows:

    from align_check import run_align_check
    issues = run_align_check(letter_path, manuscript_path)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from build_letter_claim_map import (
    _SALUTATION_RE,
    STRONG_CLAIM_PATTERN,
    build_claim_map,
    strip_tex_comments,
)
from extract_manuscript_facts import extract_facts, load_manuscript_text
from presubmission_check import DECLARATION_PATTERNS
from verify_letter_against_manuscript import verify_claim_candidates

MODULE = "ALIGNCHECK"

_VALEDICTION_RE = re.compile(
    r"^(?:Sincerely|Best regards|Kind regards|Yours (?:sincerely|faithfully)|Respectfully)\b",
    re.IGNORECASE | re.MULTILINE,
)

# STRONG_CLAIM_PATTERN is owned by build_letter_claim_map (single source of
# truth) so claim-strength wording and severity classification stay in sync.

# Negative AI-disclosure statements ("we did not use AI"). Checked before the
# positive ai_disclosure family (which includes "no AI tools were used") so a
# denial is classified as ``negative`` rather than a bare disclosure presence.
# All variants stay AI-scoped so ordinary "did not use X" / "without Y" prose
# in a manuscript never reads as an AI-disclosure signal.
NO_AI_PATTERNS: tuple[str, ...] = (
    r"\bno (?:generative )?ai\b",
    r"\bno (?:use of )?(?:large language models?|llms?|generative ai)\b",
    r"\b(?:did not|didn't|do not|don't) (?:use|employ|rely on)\s+"
    r"(?:any )?(?:generative )?(?:ai|large language models?|llms?)\b",
    r"\bwithout (?:the use of )?(?:any )?(?:generative )?"
    r"(?:ai|large language models?|llms?)\b",
)


@dataclass
class AlignCheckIssue:
    """Cover-letter align-check finding (simplified ISSUE_SCHEMA)."""

    title: str
    quote: str
    explanation: str
    comment_type: str
    severity: str
    priority: str
    source_kind: str
    confidence: str
    source_section: str
    manuscript_section_anchor: str
    evidence_anchor: list[dict[str, str]]
    claim_strength: str
    missing_evidence: list[str]
    allowed_wording: str
    forbidden_wording: list[str]
    quote_verified: bool
    char_offset: int = -1


def _section_anchor_for_claim(candidate: dict, facts: dict) -> str:
    """Heuristic mapping from claim text to a manuscript section anchor."""
    text = (candidate.get("claim", "") or "").lower()
    anchors = facts.get("section_anchors") or {}
    # Direct hint words → section keys
    hints = [
        ("conclu", "conclusion"),
        ("discuss", "discussion"),
        ("result", "result"),
        ("experiment", "experiment"),
        ("method", "method"),
        ("approach", "method"),
        ("introduction", "introduction"),
        ("background", "introduction"),
        ("abstract", "abstract"),
    ]
    for hint, key in hints:
        if hint in text and key in anchors:
            return key
    # Fallback to whichever section we have most evidence in.
    if "result" in anchors:
        return "result"
    if "abstract" in anchors:
        return "abstract"
    return "none"


def _classify_severity(candidate: dict) -> str:
    strength = candidate.get("claim_strength", "unsupported")
    has_strong_wording = bool(STRONG_CLAIM_PATTERN.search(candidate.get("claim", "") or ""))
    if strength == "unsupported" and has_strong_wording:
        return "major"
    if strength == "unsupported":
        return "moderate"
    if strength == "observed" and has_strong_wording:
        return "moderate"
    if strength == "observed" and not (
        bool(candidate.get("quote_verified")) or bool(candidate.get("manuscript_supported"))
    ):
        return "moderate"
    return "minor"


def _priority_for_severity(severity: str) -> str:
    if severity == "major":
        return "P1"
    if severity == "moderate":
        return "P2"
    return "P3"


def _has_scope_or_wording_risk(candidate: dict) -> bool:
    """Return True when an observed claim still deserves a finding.

    ``observed`` means the letter sentence contains local evidence such as a
    metric. If the same claim is anchored in the manuscript and has no strong
    wording, it is an acceptable cover-letter claim and should not be reported.
    """
    claim = candidate.get("claim", "") or ""
    has_strong_wording = bool(STRONG_CLAIM_PATTERN.search(claim))
    lacks_anchor = not (
        bool(candidate.get("quote_verified")) or bool(candidate.get("manuscript_supported"))
    )
    return has_strong_wording or lacks_anchor


def _source_section_for_offset(offset: int, letter_text: str) -> str:
    """Map a claim offset to structural cover-letter sections only."""
    if offset < 0:
        return "body"

    salutation = _SALUTATION_RE.search(letter_text)
    if salutation is None:
        return "body"
    if offset < salutation.end():
        return "header"

    valediction = _VALEDICTION_RE.search(letter_text)
    if valediction is not None and offset >= valediction.start():
        return "closing"

    opening_start = salutation.end()
    opening_end_match = re.search(r"\n\s*\n", letter_text[opening_start:])
    opening_end = (
        opening_start + opening_end_match.start()
        if opening_end_match is not None
        else len(letter_text)
    )
    if opening_start <= offset < opening_end:
        return "opening"
    return "body"


def candidate_to_issue(
    candidate: dict,
    facts: dict,
    letter_text: str | None = None,
) -> AlignCheckIssue | None:
    """Convert a verified claim candidate to an AlignCheckIssue."""
    strength = candidate.get("claim_strength")
    if strength == "observed" and not _has_scope_or_wording_risk(candidate):
        return None
    if strength != "unsupported" and strength != "observed":
        return None
    severity = _classify_severity(candidate)
    section_anchor = _section_anchor_for_claim(candidate, facts)
    char_offset = int(candidate.get("char_offset", -1))
    return AlignCheckIssue(
        title="Cover letter claim lacks manuscript support",
        quote=candidate.get("claim", "")[:280],
        explanation=(
            "The claim sentence in the cover letter could not be matched to a supporting"
            " passage in the manuscript with the same scope, numbers, or evidence anchors."
            " Either soften the wording to match what the manuscript demonstrates, or add"
            " a matching passage to the manuscript."
        ),
        comment_type="claim_accuracy",
        severity=severity,
        priority=_priority_for_severity(severity),
        source_kind="script",
        confidence=candidate.get("confidence", "unverified"),
        source_section=(
            _source_section_for_offset(char_offset, letter_text)
            if letter_text is not None
            else "body"
        ),
        manuscript_section_anchor=section_anchor,
        evidence_anchor=candidate.get("evidence_anchor", []),
        claim_strength=candidate.get("claim_strength", "unsupported"),
        missing_evidence=candidate.get("missing_evidence", []),
        allowed_wording=candidate.get("allowed_wording", ""),
        forbidden_wording=candidate.get("forbidden_wording", []),
        quote_verified=bool(candidate.get("quote_verified")),
        char_offset=char_offset,
    )


def _ai_disclosure_polarity(text: str) -> str:
    """Classify AI-disclosure polarity as ``positive`` / ``negative`` / ``absent``.

    ``negative`` (an explicit denial) is checked first because the shared
    ``ai_disclosure`` family also matches denials like "no AI tools were used".
    Known limitation: a mixed statement ("used ChatGPT for editing; analysis
    used no AI") is classified ``negative``; the finding quotes the sentence so
    the user can adjudicate.
    """
    if any(re.search(p, text, re.IGNORECASE) for p in NO_AI_PATTERNS):
        return "negative"
    if any(re.search(p, text, re.IGNORECASE) for p in DECLARATION_PATTERNS["ai_disclosure"]):
        return "positive"
    return "absent"


def _sentence_around(text: str, pos: int, limit: int = 280) -> str:
    """Return the sentence containing offset ``pos``, whitespace-collapsed."""
    start = 0
    for i in range(pos - 1, -1, -1):
        if text[i] in ".!?\n":
            start = i + 1
            break
    end = len(text)
    for i in range(pos, len(text)):
        if text[i] in ".!?\n":
            end = i + 1
            break
    return re.sub(r"\s+", " ", text[start:end]).strip()[:limit]


def _disclosure_sentence(text: str) -> str:
    """Return the sentence carrying the first AI-disclosure signal, else ``""``."""
    best_start: int | None = None
    for pattern in NO_AI_PATTERNS + DECLARATION_PATTERNS["ai_disclosure"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match and (best_start is None or match.start() < best_start):
            best_start = match.start()
    if best_start is None:
        return ""
    return _sentence_around(text, best_start)


def _check_ai_disclosure_consistency(
    letter_text: str,
    manuscript_text: str,
    *,
    letter_is_tex: bool,
) -> AlignCheckIssue | None:
    """Flag an AI-disclosure mismatch between the letter and the manuscript.

    Three inconsistencies are reported (all ``moderate`` / ``P2``): the
    manuscript discloses but the letter is silent, the letter discloses but the
    manuscript is silent, or the two disagree on polarity. When both sides agree
    (or both are silent) nothing is reported — whether a silent venue *requires*
    disclosure is the presubmission ``D-ai_disclosure`` check's job, not this
    lane's.
    """
    manuscript_clean = strip_tex_comments(manuscript_text)
    letter_clean = strip_tex_comments(letter_text) if letter_is_tex else letter_text
    letter_polarity = _ai_disclosure_polarity(letter_clean)
    manuscript_polarity = _ai_disclosure_polarity(manuscript_clean)
    if letter_polarity == manuscript_polarity:
        return None

    manuscript_sentence = _disclosure_sentence(manuscript_clean)
    letter_sentence = _disclosure_sentence(letter_clean)

    if letter_polarity == "absent":
        quote = ""
        evidence_anchor = [{"type": "section", "text": manuscript_sentence}]
        explanation = (
            "The manuscript contains an AI-use disclosure but the cover letter is silent."
            " Several venues (ICMJE Jan 2026 Section V; Science/AAAS) require the disclosure"
            " to appear in the cover letter as well; mirror the manuscript statement here."
        )
    elif manuscript_polarity == "absent":
        quote = letter_sentence
        evidence_anchor = [
            {"type": "missing", "text": "no AI-disclosure statement found in the manuscript"}
        ]
        explanation = (
            "The cover letter discloses AI use but the manuscript has no matching statement."
            " Add or reconcile the disclosure in the manuscript so the two submission"
            " documents agree."
        )
    else:
        quote = letter_sentence
        evidence_anchor = [{"type": "section", "text": manuscript_sentence}]
        explanation = (
            "The cover letter and the manuscript disagree on whether generative AI was used"
            " (one affirms it, the other denies it). Reconcile the two statements before"
            " submission."
        )

    return AlignCheckIssue(
        title="Cover letter and manuscript disagree on AI-use disclosure",
        quote=quote[:280],
        explanation=explanation,
        comment_type="disclosure_consistency",
        severity="moderate",
        priority="P2",
        source_kind="script",
        confidence="high",
        source_section="declarations",
        manuscript_section_anchor="none",
        evidence_anchor=evidence_anchor,
        claim_strength="observed",
        missing_evidence=[],
        allowed_wording="",
        forbidden_wording=[],
        quote_verified=bool(quote),
    )


def run_align_check(
    letter_path: str | Path,
    manuscript_path: str | Path,
) -> tuple[list[AlignCheckIssue], dict]:
    """Run the full align-check pipeline. Returns ``(issues, claim_map)``."""
    letter_text = Path(letter_path).read_text(encoding="utf-8", errors="replace")
    letter_is_tex = Path(letter_path).suffix.lower() == ".tex"
    # A-CL-2: a `.tex` letter's `%` comments must not surface as claim
    # candidates (e.g. `% Our work demonstrates a 99% reduction ...`); `.md`
    # letters keep their raw text — `%` there is prose, not a comment marker.
    # The disclosure check below still receives the original `letter_text`; it
    # strips comments itself via `letter_is_tex`.
    claim_source_text = strip_tex_comments(letter_text) if letter_is_tex else letter_text
    # Expand \input/\include so a multi-file manuscript (main.tex skeleton) is
    # anchored against its assembled body — otherwise facts come back empty and
    # genuinely-supported letter claims are all mis-reported as unsupported.
    manuscript_text = load_manuscript_text(manuscript_path)

    facts = extract_facts(manuscript_text)
    claim_map = build_claim_map(claim_source_text, manuscript_facts=facts)
    verified_candidates = verify_claim_candidates(
        claim_map.get("claim_candidates", []),
        manuscript_text,
    )
    claim_map["claim_candidates"] = verified_candidates
    # verify_claim_candidates may clear manuscript_supported (CL-1), so the
    # aggregate computed at claim-map build time must be refreshed to match.
    claim_map["manuscript_supported_count"] = sum(
        1 for c in verified_candidates if c.get("manuscript_supported")
    )

    issues: list[AlignCheckIssue] = []
    for candidate in verified_candidates:
        issue = candidate_to_issue(candidate, facts, claim_source_text)
        if issue is not None:
            issues.append(issue)

    disclosure_issue = _check_ai_disclosure_consistency(
        letter_text,
        manuscript_text,
        letter_is_tex=letter_is_tex,
    )
    if disclosure_issue is not None:
        issues.append(disclosure_issue)
    return issues, claim_map


def _format_protocol_issue(issue: AlignCheckIssue) -> str:
    return (
        f"% {MODULE} [Severity: {issue.severity}] "
        f"[Priority: {issue.priority}] "
        f"[Section: {issue.source_section} → {issue.manuscript_section_anchor}]: "
        f"{issue.title}\n"
        f"% Quote:        {issue.quote}\n"
        f"% Manuscript:   {'verified' if issue.quote_verified else 'not found'}\n"
        f"% Strength:     {issue.claim_strength}\n"
        f"% Allowed:      {issue.allowed_wording[:200]}\n"
    )


def _render_protocol(issues: list[AlignCheckIssue]) -> str:
    return "\n".join(_format_protocol_issue(issue) for issue in issues)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Align-check a cover letter against a LaTeX manuscript"
    )
    parser.add_argument("--letter", required=True, help="Cover letter path (.md or .tex)")
    parser.add_argument("--manuscript", required=True, help="Manuscript path (.tex)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--output",
        "-o",
        help="Optional output path (issues JSON when --json, protocol text otherwise)",
    )
    args = parser.parse_args(argv)

    letter_path = Path(args.letter).resolve()
    manuscript_path = Path(args.manuscript).resolve()
    if not letter_path.exists():
        print(f"File not found: {args.letter}", file=sys.stderr)
        return 2
    if not manuscript_path.exists():
        print(f"File not found: {args.manuscript}", file=sys.stderr)
        return 2
    if manuscript_path.suffix.lower() != ".tex":
        print(
            f"Unsupported manuscript format: {manuscript_path.suffix}; expected .tex",
            file=sys.stderr,
        )
        return 2

    issues, _ = run_align_check(letter_path, manuscript_path)

    if args.json:
        payload = json.dumps([asdict(issue) for issue in issues], indent=2, ensure_ascii=False)
    else:
        payload = _render_protocol(issues)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    elif payload:
        print(payload)

    if any(issue.severity == "major" for issue in issues):
        return 2
    if issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
