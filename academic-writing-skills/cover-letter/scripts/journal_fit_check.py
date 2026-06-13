"""Journal-fit scoring for a cover letter.

Four sub-axes, each labeled HIGH / MEDIUM / LOW based on deterministic rules
that read the active template's frontmatter:

* scope_fit         — does the letter mention the venue's named scope dimensions?
* novelty_framing   — is the novelty pitch calibrated for the venue's tier?
* evidence_density  — does claim density match what the venue expects?
* format_compliance — word count, banned phrases, required declarations.

Overall verdict = worst sub-axis: LOW anywhere ⇒ LOW; else MEDIUM if any
MEDIUM; HIGH only when all four sub-axes are HIGH.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from parsers import LatexParser
from template_meta import split_frontmatter

MODULE = "JOURNALFIT"

VENUES = {
    "nature",
    "science",
    "cell",
    "ieee-trans",
    "acm",
    "springer-lncs",
    "neurips",
    "icml",
    "cvpr",
    "generic",
}

TIER_BUDGETS = {
    "top-journal": {"word_min": 200, "word_max": 350, "claims_min": 2, "claims_max": 5},
    "mid-journal": {"word_min": 250, "word_max": 500, "claims_min": 3, "claims_max": 6},
    "conference": {"word_min": 200, "word_max": 400, "claims_min": 2, "claims_max": 5},
}

VERDICTS = ("HIGH", "MEDIUM", "LOW")


@dataclass
class AxisVerdict:
    axis: str
    verdict: str  # HIGH | MEDIUM | LOW
    evidence: list[str]
    suggestions: list[str]


@dataclass
class JournalFitResult:
    venue: str
    tier: str
    overall: str
    axes: list[AxisVerdict]


@dataclass
class JournalFitFinding:
    title: str
    quote: str
    explanation: str
    comment_type: str
    severity: str
    priority: str
    source_kind: str
    source_section: str
    axis: str
    verdict: str
    suggestions: list[str]


def _read_template(skill_dir: Path, venue: str) -> tuple[dict[str, Any], str]:
    """Return ``(frontmatter_dict, body_text)`` of the named template."""
    path = skill_dir / "templates" / f"{venue}.md"
    if not path.exists():
        path = skill_dir / "templates" / "generic.md"
    return split_frontmatter(path.read_text(encoding="utf-8", errors="replace"))


def _read_letter_visible(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".tex":
        parser = LatexParser()
        return parser.clean_text(text)
    # Markdown / plain text fallback
    cleaned = re.sub(r"^---.*?---\n", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"^#+\s+", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()


def _count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _count_claims(text: str) -> int:
    return len(
        re.findall(
            r"\bwe (?:report|present|show|demonstrate|find|propose|introduce|describe|provide)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def _check_scope_fit(letter_text: str, venue: str) -> AxisVerdict:
    evidence: list[str] = []
    suggestions: list[str] = []
    venue_words = {
        "nature": ("broad scientific", "general scientific", "field", "discipline"),
        "science": ("broad", "general scientific", "field", "discipline"),
        "cell": ("mechanism", "mechanistic", "biological", "molecular"),
        "ieee-trans": ("methodological", "algorithmic", "system", "evaluation"),
        "acm": ("system", "software", "algorithm", "reproducibility"),
        "springer-lncs": ("computer science", "method", "approach"),
        "neurips": ("learning", "neural", "machine learning", "model"),
        "icml": ("learning", "machine learning", "algorithm", "model"),
        "cvpr": ("vision", "image", "video", "recognition"),
        "generic": (),
    }
    scope_keywords = venue_words.get(venue, ())
    if not scope_keywords:
        return AxisVerdict(
            axis="scope_fit",
            verdict="MEDIUM",
            evidence=["No venue-specific scope keywords for `generic` template; cannot judge."],
            suggestions=["Specify the venue explicitly if a fit score is needed."],
        )
    lowered = letter_text.lower()
    hits = [kw for kw in scope_keywords if kw in lowered]
    if len(hits) >= 2:
        evidence.append(f"Letter references scope keywords: {', '.join(hits)}")
        return AxisVerdict(
            axis="scope_fit",
            verdict="HIGH",
            evidence=evidence,
            suggestions=[],
        )
    if len(hits) == 1:
        evidence.append(f"Letter references only one scope keyword: {hits[0]}")
        suggestions.append(f"Strengthen scope fit by referencing more of {list(scope_keywords)}.")
        return AxisVerdict(
            axis="scope_fit",
            verdict="MEDIUM",
            evidence=evidence,
            suggestions=suggestions,
        )
    evidence.append("Letter does not name venue-specific scope dimensions.")
    suggestions.append(
        f"Explicitly tie the contribution to one of {list(scope_keywords)} in the journal-fit paragraph."
    )
    return AxisVerdict(
        axis="scope_fit",
        verdict="LOW",
        evidence=evidence,
        suggestions=suggestions,
    )


def _check_novelty_framing(letter_text: str, tier: str) -> AxisVerdict:
    """Top-tier needs paradigm-shift framing; mid-tier needs methodological framing; conference needs contribution framing."""
    paradigm_signals = re.findall(
        r"\b(?:resolve|answer|establish|address|reframe|paradigm|broad scientific)\b",
        letter_text,
        flags=re.IGNORECASE,
    )
    methodology_signals = re.findall(
        r"\b(?:algorithm|framework|method|approach|baseline|benchmark|evaluation)\b",
        letter_text,
        flags=re.IGNORECASE,
    )
    contribution_signals = re.findall(
        r"\b(?:contribut\w+|propose|introduce|present|report)\b",
        letter_text,
        flags=re.IGNORECASE,
    )

    if tier == "top-journal":
        if len(paradigm_signals) >= 2:
            return AxisVerdict(
                axis="novelty_framing",
                verdict="HIGH",
                evidence=[f"Letter uses paradigm-shift framing ({len(paradigm_signals)} signals)."],
                suggestions=[],
            )
        if len(paradigm_signals) == 1:
            return AxisVerdict(
                axis="novelty_framing",
                verdict="MEDIUM",
                evidence=["Only one paradigm-shift signal detected."],
                suggestions=[
                    "Strengthen the framing: name what open question is resolved or what"
                    " was previously impossible."
                ],
            )
        return AxisVerdict(
            axis="novelty_framing",
            verdict="LOW",
            evidence=["Letter reads as a contribution list, not a paradigm-shift pitch."],
            suggestions=[
                "Top-tier venues expect broader-impact framing. Lead with what the field"
                " can now do that it could not before."
            ],
        )
    if tier == "mid-journal":
        if len(methodology_signals) >= 3:
            return AxisVerdict(
                axis="novelty_framing",
                verdict="HIGH",
                evidence=[
                    f"Letter has solid methodological framing ({len(methodology_signals)} signals)."
                ],
                suggestions=[],
            )
        return AxisVerdict(
            axis="novelty_framing",
            verdict="MEDIUM",
            evidence=["Methodological framing is thin."],
            suggestions=["Name the algorithm, framework, or methodological advance explicitly."],
        )
    # conference
    if len(contribution_signals) >= 3:
        return AxisVerdict(
            axis="novelty_framing",
            verdict="HIGH",
            evidence=[f"Letter enumerates contributions ({len(contribution_signals)} signals)."],
            suggestions=[],
        )
    return AxisVerdict(
        axis="novelty_framing",
        verdict="MEDIUM",
        evidence=["Contribution enumeration is light."],
        suggestions=[
            "Conference letters benefit from 3 explicit contributions, each one sentence."
        ],
    )


def _check_evidence_density(letter_text: str, tier: str) -> AxisVerdict:
    """Claim density should match the tier's expected budget."""
    claims = _count_claims(letter_text)
    budget = TIER_BUDGETS.get(tier, TIER_BUDGETS["mid-journal"])
    if budget["claims_min"] <= claims <= budget["claims_max"]:
        return AxisVerdict(
            axis="evidence_density",
            verdict="HIGH",
            evidence=[f"Detected {claims} claim sentences; tier budget {budget}."],
            suggestions=[],
        )
    if claims < budget["claims_min"]:
        return AxisVerdict(
            axis="evidence_density",
            verdict="LOW",
            evidence=[
                f"Only {claims} claim sentences; tier expects at least {budget['claims_min']}."
            ],
            suggestions=["Add at least one quantitative anchor with explicit comparator naming."],
        )
    return AxisVerdict(
        axis="evidence_density",
        verdict="MEDIUM",
        evidence=[
            f"{claims} claim sentences exceeds the tier ceiling of {budget['claims_max']};"
            " editors may read this as overpitching."
        ],
        suggestions=["Trim secondary claims; focus the letter on the headline contribution."],
    )


def _check_format_compliance(
    letter_text: str,
    meta: dict[str, Any],
) -> AxisVerdict:
    evidence: list[str] = []
    suggestions: list[str] = []
    word_count = _count_words(letter_text)
    limit = int(meta.get("word_limit") or 400)
    if word_count > int(limit * 1.20):
        evidence.append(f"Letter is {word_count} words; template ceiling {limit} (+20%).")
        suggestions.append(f"Trim by at least {word_count - limit} words.")
        return AxisVerdict(
            axis="format_compliance",
            verdict="LOW",
            evidence=evidence,
            suggestions=suggestions,
        )
    if word_count > limit:
        evidence.append(f"Letter is {word_count} words; template ceiling {limit}.")
        suggestions.append(f"Tighten by {word_count - limit} words to stay within budget.")
    # Banned phrases
    banned = meta.get("banned_phrases") or []
    hits: list[str] = []
    lowered = letter_text.lower()
    for phrase in banned:
        if phrase.lower() in lowered:
            hits.append(phrase)
    if hits:
        evidence.append(f"Letter contains banned phrases: {', '.join(hits)}")
        suggestions.append("Remove banned phrases listed in the template.")
        return AxisVerdict(
            axis="format_compliance",
            verdict="LOW",
            evidence=evidence,
            suggestions=suggestions,
        )
    if evidence:
        return AxisVerdict(
            axis="format_compliance",
            verdict="MEDIUM",
            evidence=evidence,
            suggestions=suggestions,
        )
    return AxisVerdict(
        axis="format_compliance",
        verdict="HIGH",
        evidence=[f"Letter is {word_count} words; no banned phrases detected."],
        suggestions=[],
    )


def _overall_verdict(axes: list[AxisVerdict]) -> str:
    verdicts = {axis.verdict for axis in axes}
    if "LOW" in verdicts:
        return "LOW"
    if "MEDIUM" in verdicts:
        return "MEDIUM"
    return "HIGH"


def _finding_for_axis(axis: AxisVerdict) -> JournalFitFinding | None:
    """Map non-HIGH journal-fit axes to protocol findings.

    Axis verdicts stay uppercase because that is the public journal-fit scale.
    Findings use the shared lowercase severity and P1/P2 priority protocol.
    """
    if axis.verdict == "HIGH":
        return None
    severity = "major" if axis.verdict == "LOW" else "moderate"
    priority = "P1" if axis.verdict == "LOW" else "P2"
    evidence = "; ".join(axis.evidence)
    return JournalFitFinding(
        title=f"Journal-fit axis `{axis.axis}` is {axis.verdict}",
        quote=evidence[:280],
        explanation=evidence or "Journal-fit check found a venue-framing mismatch.",
        comment_type="journal_fit",
        severity=severity,
        priority=priority,
        source_kind="script",
        source_section="fit",
        axis=axis.axis,
        verdict=axis.verdict,
        suggestions=axis.suggestions,
    )


def findings_from_result(result: JournalFitResult) -> list[JournalFitFinding]:
    """Return protocol findings for MEDIUM / LOW axes."""
    findings: list[JournalFitFinding] = []
    for axis in result.axes:
        finding = _finding_for_axis(axis)
        if finding is not None:
            findings.append(finding)
    return findings


def run_journal_fit(letter_path: Path, venue: str, skill_dir: Path) -> JournalFitResult:
    """Run all four sub-axis checks and return the consolidated verdict."""
    meta, _ = _read_template(skill_dir, venue)
    tier = str(meta.get("tier") or "mid-journal")
    letter_text = _read_letter_visible(letter_path)

    axes = [
        _check_scope_fit(letter_text, venue),
        _check_novelty_framing(letter_text, tier),
        _check_evidence_density(letter_text, tier),
        _check_format_compliance(letter_text, meta),
    ]
    return JournalFitResult(
        venue=meta.get("venue", venue),
        tier=tier,
        overall=_overall_verdict(axes),
        axes=axes,
    )


def _format_protocol(result: JournalFitResult) -> str:
    lines = [
        f"% {MODULE} Venue: {result.venue}  Tier: {result.tier}  Overall: {result.overall}",
    ]
    for axis in result.axes:
        lines.append(f"% {MODULE} [Axis: {axis.axis}] [Verdict: {axis.verdict}]")
        for ev in axis.evidence:
            lines.append(f"%   Evidence:  {ev}")
        for sug in axis.suggestions:
            lines.append(f"%   Suggest:   {sug}")
    for finding in findings_from_result(result):
        lines.append(
            f"% {MODULE} [Severity: {finding.severity}] [Priority: {finding.priority}] "
            f"[Comment: {finding.comment_type}]: {finding.title}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score a cover letter's fit to a target journal/conference"
    )
    parser.add_argument("letter", help="Path to cover letter (.md or .tex)")
    parser.add_argument(
        "--venue",
        required=True,
        help=f"Target venue: one of {sorted(VENUES)}",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--output", "-o", help="Optional output path")
    args = parser.parse_args(argv)

    if args.venue not in VENUES:
        print(
            f"Unknown venue `{args.venue}`; expected one of {sorted(VENUES)}",
            file=sys.stderr,
        )
        return 2

    letter_path = Path(args.letter).resolve()
    if not letter_path.exists():
        print(f"File not found: {args.letter}", file=sys.stderr)
        return 2

    skill_dir = Path(__file__).resolve().parent.parent
    result = run_journal_fit(letter_path, args.venue, skill_dir)

    if args.json:
        payload = json.dumps(
            {
                "venue": result.venue,
                "tier": result.tier,
                "overall": result.overall,
                "axes": [asdict(axis) for axis in result.axes],
                "findings": [asdict(finding) for finding in findings_from_result(result)],
            },
            indent=2,
            ensure_ascii=False,
        )
    else:
        payload = _format_protocol(result)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    if result.overall == "LOW":
        return 2
    if result.overall == "MEDIUM":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
