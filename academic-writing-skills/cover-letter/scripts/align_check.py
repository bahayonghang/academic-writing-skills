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
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from build_letter_claim_map import STRONG_CLAIM_PATTERN, build_claim_map
from extract_manuscript_facts import extract_facts, load_manuscript_text
from verify_letter_against_manuscript import verify_claim_candidates

MODULE = "ALIGNCHECK"

# STRONG_CLAIM_PATTERN is owned by build_letter_claim_map (single source of
# truth) so claim-strength wording and severity classification stay in sync.


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


def candidate_to_issue(candidate: dict, facts: dict) -> AlignCheckIssue | None:
    """Convert a verified claim candidate to an AlignCheckIssue."""
    strength = candidate.get("claim_strength")
    if strength == "observed" and not _has_scope_or_wording_risk(candidate):
        return None
    if strength != "unsupported" and strength != "observed":
        return None
    severity = _classify_severity(candidate)
    section_anchor = _section_anchor_for_claim(candidate, facts)
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
        source_section="contributions",
        manuscript_section_anchor=section_anchor,
        evidence_anchor=candidate.get("evidence_anchor", []),
        claim_strength=candidate.get("claim_strength", "unsupported"),
        missing_evidence=candidate.get("missing_evidence", []),
        allowed_wording=candidate.get("allowed_wording", ""),
        forbidden_wording=candidate.get("forbidden_wording", []),
        quote_verified=bool(candidate.get("quote_verified")),
    )


def run_align_check(
    letter_path: str | Path,
    manuscript_path: str | Path,
) -> tuple[list[AlignCheckIssue], dict]:
    """Run the full align-check pipeline. Returns ``(issues, claim_map)``."""
    letter_text = Path(letter_path).read_text(encoding="utf-8", errors="replace")
    # Expand \input/\include so a multi-file manuscript (main.tex skeleton) is
    # anchored against its assembled body — otherwise facts come back empty and
    # genuinely-supported letter claims are all mis-reported as unsupported.
    manuscript_text = load_manuscript_text(manuscript_path)

    facts = extract_facts(manuscript_text)
    claim_map = build_claim_map(letter_text, manuscript_facts=facts)
    verified_candidates = verify_claim_candidates(
        claim_map.get("claim_candidates", []),
        manuscript_text,
    )
    claim_map["claim_candidates"] = verified_candidates

    issues: list[AlignCheckIssue] = []
    for candidate in verified_candidates:
        issue = candidate_to_issue(candidate, facts)
        if issue is not None:
            issues.append(issue)
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
