"""
Report Generator for Paper Audit skill.
Handles scoring engine, issue aggregation, and Markdown report rendering.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# --- Data Models ---


@dataclass
class AuditIssue:
    """A single issue found during audit."""

    module: str  # e.g., "FORMAT", "GRAMMAR", "LOGIC"
    line: Optional[int]  # Line number (None if not applicable)
    severity: str  # "Critical", "Major", "Minor"
    priority: str  # "P0", "P1", "P2"
    message: str  # Issue description
    original: str = ""  # Original text (if applicable)
    revised: str = ""  # Suggested revision (if applicable)
    rationale: str = ""  # Explanation


@dataclass
class DeepReviewIssue:
    """A structured reviewer finding used by deep-review workflows."""

    ISSUE_KEYS = (
        "title",
        "quote",
        "explanation",
        "comment_type",
        "severity",
        "confidence",
        "source_kind",
        "source_section",
        "related_sections",
        "root_cause_key",
        "review_lane",
        "gate_blocker",
        "quote_verified",
    )

    title: str
    quote: str
    explanation: str
    comment_type: str
    severity: str
    confidence: str = "medium"
    source_kind: str = "llm"
    source_section: str = ""
    related_sections: list[str] = field(default_factory=list)
    root_cause_key: str = ""
    review_lane: str = ""
    gate_blocker: bool = False
    quote_verified: Optional[bool] = None

    @classmethod
    def from_dict(cls, issue: dict) -> "DeepReviewIssue":
        """Build a DeepReviewIssue from a persisted issue mapping."""
        payload = {key: issue[key] for key in cls.ISSUE_KEYS if key in issue}
        return cls(**payload)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "quote": self.quote,
            "explanation": self.explanation,
            "comment_type": self.comment_type,
            "severity": self.severity,
            "confidence": self.confidence,
            "source_kind": self.source_kind,
            "source_section": self.source_section,
            "related_sections": list(self.related_sections),
            "root_cause_key": self.root_cause_key,
            "review_lane": self.review_lane,
            "gate_blocker": self.gate_blocker,
            "quote_verified": self.quote_verified,
        }


@dataclass
class ChecklistItem:
    """A single pre-submission checklist item."""

    description: str
    passed: bool
    details: str = ""  # Additional context for failures


@dataclass
class AuditResult:
    """Complete audit result from all checks."""

    file_path: str
    language: str  # "en" or "zh"
    mode: str  # "quick-audit", "deep-review", "gate", "polish", "re-audit"
    venue: str = ""  # e.g., "neurips", "ieee"
    mode_alias_used: str | None = None
    issues: list[AuditIssue] = field(default_factory=list)
    issue_bundle: list[DeepReviewIssue] = field(default_factory=list)
    checklist: list[ChecklistItem] = field(default_factory=list)
    # Review mode extras
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    summary: str = ""
    overall_assessment: str = ""
    revision_roadmap: list[dict] = field(default_factory=list)
    section_index: list[dict] = field(default_factory=list)
    artifact_dir: str = ""
    review_focus: str = "full"
    # ScholarEval result (optional, populated when --scholar-eval is used)
    scholar_eval_result: object | None = None
    # Literature context (optional, populated when --literature-search is used)
    literature_context: object | None = None
    # Multi-perspective review extras (populated by SKILL.md agent workflow)
    agent_reviews: list[dict] = field(default_factory=list)
    consensus: str = ""
    # Re-audit comparison data (populated by run_reaudit)
    reaudit_data: dict | None = None


@dataclass
class PolishSectionVerdict:
    """Critic's verdict for a single section."""

    section: str
    logic_score: int  # 1-5
    expression_score: int  # 1-5
    blocks_mentor: bool
    blocking_reason: str = ""
    top_issues: list[dict] = field(default_factory=list)
    mentor_done: bool = False
    mentor_suggestions_count: int = 0


# --- Dimension Mapping & Scoring ---

DIMENSION_MAP: dict[str, list[str]] = {
    "format": ["clarity"],
    "grammar": ["clarity"],
    "logic": ["quality", "significance"],
    "experiment": ["quality", "significance"],
    "sentences": ["clarity"],
    "deai": ["clarity", "originality"],
    "citations": ["quality"],
    "bib": ["quality"],
    "figures": ["clarity"],
    "consistency": ["clarity"],
    "gbt7714": ["quality"],
    "checklist": ["quality", "clarity", "significance", "originality"],
    "references": ["clarity", "quality"],
    "visual": ["clarity"],
    "literature_grounding": ["quality", "significance", "originality"],
}

DIMENSION_WEIGHTS: dict[str, float] = {
    "quality": 0.30,
    "clarity": 0.30,
    "significance": 0.20,
    "originality": 0.20,
}

SEVERITY_DEDUCTIONS: dict[str, float] = {
    "Critical": 1.5,
    "Major": 0.75,
    "Minor": 0.25,
}

SCORE_LABELS: list[tuple[float, str]] = [
    (5.5, "Strong Accept"),
    (4.5, "Accept"),
    (3.5, "Borderline Accept"),
    (2.5, "Borderline Reject"),
    (1.5, "Reject"),
    (0.0, "Strong Reject"),
]

DEEP_REVIEW_SEVERITY_ORDER: dict[str, int] = {
    "major": 0,
    "moderate": 1,
    "minor": 2,
}

SOURCE_KIND_LABELS: dict[str, str] = {
    "llm": "[LLM]",
    "script": "[Script]",
}

DEEP_REVIEW_ISSUE_KEYS: tuple[str, ...] = (
    "title",
    "quote",
    "explanation",
    "comment_type",
    "severity",
    "confidence",
    "source_kind",
    "source_section",
    "related_sections",
    "root_cause_key",
    "review_lane",
    "gate_blocker",
    "quote_verified",
)

DEEP_REVIEW_PRIORITY_LABELS: dict[str, str] = {
    "major": "Priority 1",
    "moderate": "Priority 2",
    "minor": "Priority 3",
}

JOURNAL_RECOMMENDATION_ORDER: tuple[str, ...] = (
    "Accept",
    "Minor Revision",
    "Major Revision",
    "Reject",
)

DEEP_REVIEW_SECTIONS: tuple[tuple[str, str], ...] = (
    ("major", "Major Issues"),
    ("moderate", "Moderate Issues"),
    ("minor", "Minor Issues"),
)


def coerce_deep_review_issue(issue: DeepReviewIssue | dict[str, Any]) -> DeepReviewIssue:
    """Convert an issue payload into the canonical DeepReviewIssue dataclass."""
    if isinstance(issue, DeepReviewIssue):
        return issue

    payload = {key: issue[key] for key in DEEP_REVIEW_ISSUE_KEYS if key in issue}
    payload["related_sections"] = [
        section for section in payload.get("related_sections", []) if section
    ]
    return DeepReviewIssue(**payload)


def normalize_deep_review_issue_dict(issue: DeepReviewIssue | dict[str, Any]) -> dict[str, Any]:
    """Convert an issue payload into the canonical persisted dict schema."""
    return coerce_deep_review_issue(issue).to_dict()


def _score_label(score: float) -> str:
    """Map numeric score to NeurIPS-style label."""
    for threshold, label in SCORE_LABELS:
        if score >= threshold:
            return label
    return "Strong Reject"


def calculate_scores(issues: list[AuditIssue]) -> dict[str, float]:
    """
    Calculate per-dimension scores based on issues found.

    Returns:
        Dict with keys: "quality", "clarity", "significance", "originality", "overall".
    """
    dimension_issues: dict[str, list[AuditIssue]] = {
        "quality": [],
        "clarity": [],
        "significance": [],
        "originality": [],
    }

    # Map issues to dimensions
    for issue in issues:
        module_key = issue.module.lower()
        dimensions = DIMENSION_MAP.get(module_key, ["clarity"])
        for dim in dimensions:
            if dim in dimension_issues:
                dimension_issues[dim].append(issue)

    # Calculate per-dimension scores
    scores: dict[str, float] = {}
    for dim, dim_issues in dimension_issues.items():
        score = 6.0
        for issue in dim_issues:
            deduction = SEVERITY_DEDUCTIONS.get(issue.severity, 0.25)
            score -= deduction
        scores[dim] = max(1.0, score)

    # Weighted average
    overall = sum(scores[dim] * weight for dim, weight in DIMENSION_WEIGHTS.items())
    scores["overall"] = round(overall, 2)

    return scores


def _count_issues(issues: list[AuditIssue]) -> str:
    """Count issues by severity: C/M/m format."""
    c = sum(1 for i in issues if i.severity == "Critical")
    m = sum(1 for i in issues if i.severity == "Major")
    n = sum(1 for i in issues if i.severity == "Minor")
    return f"{c}/{m}/{n}"


def _count_deep_review_issues(issues: list[DeepReviewIssue]) -> dict[str, int]:
    """Count deep-review issues by severity."""
    return {
        "major": sum(1 for i in issues if i.severity == "major"),
        "moderate": sum(1 for i in issues if i.severity == "moderate"),
        "minor": sum(1 for i in issues if i.severity == "minor"),
    }


def _default_revision_roadmap(issues: list[DeepReviewIssue]) -> list[dict]:
    """Build a minimal roadmap from issue severities when none is provided."""
    return [
        {
            "priority": DEEP_REVIEW_PRIORITY_LABELS.get(issue.severity, "Priority 3"),
            "title": issue.title,
            "source": SOURCE_KIND_LABELS.get(issue.source_kind, "[LLM]"),
            "section": issue.source_section or "unknown",
        }
        for issue in issues
    ]


def _clean_peer_review_text(text: str) -> str:
    """Normalize summary text before rendering reviewer prose."""
    text = text.strip()
    text = text.removeprefix("- ").strip()
    text = text.lstrip("#").strip()
    text = " ".join(text.split())
    text = re.sub(
        r"^(abstract|introduction|conclusion|discussion|method|methods|results)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )
    return text.strip()


def _rewrite_opening_focus(text: str) -> str:
    """Rewrite extracted cues into more natural reviewer-opening prose fragments."""
    cleaned = _clean_peer_review_text(text).rstrip(".")
    lowered = cleaned.lower()
    if lowered.startswith("we achieve state-of-the-art efficiency across "):
        tail = cleaned[39:].strip()
        tail = re.sub(r"^across\s+", "", tail, flags=re.IGNORECASE)
        return "improved efficiency across " + tail
    if lowered.startswith("we achieve "):
        return cleaned[11:].strip()
    if lowered.startswith("we propose "):
        body = cleaned[11:].strip()
        body = re.sub(r"^a\s+", "", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+and\s+claims\s+", " with ", body, flags=re.IGNORECASE)
        return "the proposed method offers a " + body
    if lowered.startswith("this paper proposes "):
        body = cleaned[19:].strip()
        body = re.sub(r"^a\s+", "", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+and\s+claims\s+", " with ", body, flags=re.IGNORECASE)
        body = re.sub(
            r"\s+broad\s+superiority\s+over\s+",
            " broader advantages over ",
            body,
            flags=re.IGNORECASE,
        )
        return "the proposed method offers a " + body
    if lowered.startswith("we demonstrate "):
        return cleaned[15:].strip()
    if lowered.startswith("we show "):
        return cleaned[8:].strip()
    return cleaned


def _compress_peer_review_opening(research_question: str, thesis: str) -> str:
    """Compress extracted summary cues into a reviewer-style opening paragraph."""
    rq = _rewrite_opening_focus(research_question)
    th = _rewrite_opening_focus(thesis)

    if rq and th:
        return f"The manuscript examines {rq} and argues that {th}."
    if th:
        return f"The manuscript argues that {th}."
    if rq:
        return f"The manuscript examines {rq}."
    return (
        "This manuscript addresses a potentially relevant research problem, but its current argument "
        "still needs tighter evidence alignment and clearer support for the main claims."
    )


def _sort_deep_review_issues(issues: list[DeepReviewIssue]) -> list[DeepReviewIssue]:
    """Sort structured findings by severity, confidence, and location."""
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(
        issues,
        key=lambda issue: (
            DEEP_REVIEW_SEVERITY_ORDER.get(issue.severity, 99),
            confidence_order.get(issue.confidence, 3),
            0 if issue.gate_blocker else 1,
            -(len(issue.related_sections) or 0),
            issue.source_section or "",
            issue.title.lower(),
        ),
    )


def _journal_recommendation(issues: list[DeepReviewIssue]) -> str:
    """Map structured deep-review findings to a journal-style decision."""
    major = sum(1 for issue in issues if issue.severity == "major")
    moderate = sum(1 for issue in issues if issue.severity == "moderate")
    blocking = any(issue.gate_blocker for issue in issues)

    if blocking and major >= 1:
        return "Reject"
    if major >= 3:
        return "Reject"
    if major >= 1 or moderate >= 4:
        return "Major Revision"
    if moderate >= 1 or len(issues) >= 3:
        return "Minor Revision"
    return "Accept"


def _build_peer_review_summary(result: AuditResult, issue_counts: dict[str, int]) -> str:
    """Build a concise journal-style summary paragraph block."""
    summary_text = (result.summary or "").strip()
    overall = (result.overall_assessment or "").strip()

    research_question = ""
    core_thesis = ""
    headline_claim = ""
    current_section = ""
    for raw_line in summary_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("## "):
            current_section = line.removeprefix("## ").strip().lower()
            continue
        normalized = _clean_peer_review_text(line)
        if not normalized or normalized.upper() == "TODO" or "TODO" in normalized:
            continue
        if current_section == "research question" and not research_question:
            research_question = normalized
        elif current_section == "core thesis" and not core_thesis:
            core_thesis = normalized
        elif current_section == "headline claims" and not headline_claim:
            headline_claim = normalized

    opening = _compress_peer_review_opening(research_question, core_thesis or headline_claim)

    evaluative = overall or (
        f"At this stage, the paper raises {issue_counts['major']} major, {issue_counts['moderate']} "
        f"moderate, and {issue_counts['minor']} minor concerns that should be addressed before submission."
    )

    closing = (
        "In its current form, the paper would benefit most from revisions that better align the headline "
        "contribution with the presented evidence, clarify the methodological basis of the claims, and "
        "tighten the overall argumentative coherence."
    )

    return "\n\n".join([opening, evaluative, closing])


def _peer_review_issue_location(issue: DeepReviewIssue) -> str:
    """Render a reviewer-friendly location label for a structured issue."""
    if issue.source_section:
        return issue.source_section
    if issue.related_sections:
        return issue.related_sections[0]
    return "the manuscript"


def _peer_review_issue_text(issue: DeepReviewIssue) -> str:
    """Translate a structured finding into reviewer-style prose."""
    location = _peer_review_issue_location(issue)
    quote = issue.quote.strip()
    quote_text = (
        f' The quoted text ("{quote}") sharpens this concern.'
        if quote and issue.quote_verified is True
        else ""
    )
    related = ""
    if issue.related_sections:
        extras = [
            section
            for section in issue.related_sections
            if section and section != issue.source_section
        ]
        if extras:
            related = f" This issue also affects {', '.join(extras)}."
    source_label = "[Script]" if issue.source_kind == "script" else "[LLM]"
    return (
        f"In {location}, the manuscript shows a problem with {issue.title.lower()}. "
        f"{issue.explanation.strip()} This matters because it weakens the credibility or interpretability "
        f"of the corresponding claim. The authors should revise this part directly and make the supporting "
        f"evidence or reasoning explicit.{quote_text}{related} {source_label}"
    ).strip()


def render_peer_review_report(result: AuditResult) -> str:
    """Render a concise journal-style reviewer report from deep-review artifacts."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    issues = _sort_deep_review_issues(result.issue_bundle)
    issue_counts = _count_deep_review_issues(issues)
    recommendation = _journal_recommendation(issues)
    major_issues = [issue for issue in issues if issue.severity == "major"][:5]
    minor_issues = [issue for issue in issues if issue.severity in {"moderate", "minor"}][:4]

    lines = [
        "# Peer Review Report",
        "",
        f"**Paper**: `{result.file_path}` | **Language**: {result.language.upper()} | **Mode**: deep-review",
        f"**Generated**: {now}" + (f" | **Venue**: {result.venue}" if result.venue else ""),
    ]
    if result.artifact_dir:
        lines.append(f"**Artifacts**: `{result.artifact_dir}`")
    lines.extend(["", "## Summary", "", _build_peer_review_summary(result, issue_counts), ""])

    lines.extend(["## Major Issues", ""])
    if major_issues:
        for idx, issue in enumerate(major_issues, 1):
            lines.append(f"{idx}. {_peer_review_issue_text(issue)}")
            lines.append("")
    else:
        lines.append(
            "1. No major validity-threatening issue was identified in the current deep-review bundle."
        )
        lines.append("")

    lines.extend(["## Minor Issues", ""])
    if minor_issues:
        for idx, issue in enumerate(minor_issues, 1):
            lines.append(f"{idx}. {_peer_review_issue_text(issue)}")
            lines.append("")
    else:
        lines.append("1. No minor issue requiring additional comment was identified.")
        lines.append("")

    rationale = {
        "Accept": "The central contribution appears supportable and only non-substantive edits remain.",
        "Minor Revision": "The paper is potentially publishable, but several clarifications or limited corrections are still needed.",
        "Major Revision": "The paper may become publishable, but key issues still affect the credibility, completeness, or transparency of the claims.",
        "Reject": "The current version has unresolved issues that materially weaken the core conclusions or submission readiness.",
    }[recommendation]
    lines.extend(["## Recommendation", "", f"**{recommendation}**. {rationale}"])
    return "\n".join(lines)


def _committee_signal_from_artifacts(artifact_dir: str) -> tuple[float | None, str]:
    """Load committee score and verdict from the generated consensus artifact when present."""
    if not artifact_dir:
        return None, ""

    consensus_path = Path(artifact_dir) / "committee" / "consensus.md"
    if not consensus_path.exists():
        return None, ""

    text = consensus_path.read_text(encoding="utf-8")
    score_match = re.search(r"Overall Score:\s*([0-9]+(?:\.[0-9]+)?)\/10", text)
    verdict_match = re.search(r"Editor Verdict:\s*(.+)", text)
    score = float(score_match.group(1)) if score_match else None
    verdict = verdict_match.group(1).strip() if verdict_match else ""
    return score, verdict


def _artifact_path(result: AuditResult, filename: str) -> str:
    """Return an artifact path label for reports and summaries."""
    if not result.artifact_dir:
        return filename
    return str(Path(result.artifact_dir) / filename)


def render_deep_review_summary(
    result: AuditResult,
    *,
    primary_style: str = "deep-review",
) -> str:
    """Render the compact CLI-facing deep-review summary with both report paths."""
    primary_style = (
        primary_style if primary_style in {"deep-review", "peer-review"} else "deep-review"
    )
    primary_name = "peer_review_report.md" if primary_style == "peer-review" else "review_report.md"
    companion_name = (
        "review_report.md" if primary_style == "peer-review" else "peer_review_report.md"
    )

    issues = _sort_deep_review_issues(result.issue_bundle)
    issue_counts = _count_deep_review_issues(issues)
    recommendation = _journal_recommendation(issues)
    committee_score, editor_verdict = _committee_signal_from_artifacts(result.artifact_dir)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Deep Review Summary",
        "",
        f"**Paper**: `{result.file_path}` | **Language**: {result.language.upper()} | **Mode**: deep-review",
        f"**Generated**: {now}" + (f" | **Venue**: {result.venue}" if result.venue else ""),
    ]
    if result.review_focus != "full":
        lines.append(f"**Focus**: `{result.review_focus}`")
    lines.extend(
        [
            f"**Primary View**: `{primary_style}`",
            "",
            "## Overall Assessment",
            "",
            result.overall_assessment
            or "Deep review completed. Inspect the primary artifact and issue bundle before revising.",
            "",
            "## Decision Signals",
            "",
        ]
    )
    if committee_score is not None:
        lines.append(f"- **Committee Score**: {committee_score:.1f}/10")
    if editor_verdict:
        lines.append(f"- **Editor Verdict**: {editor_verdict}")
    lines.extend(
        [
            f"- **Reviewer Recommendation**: {recommendation}",
            (
                f"- **Issue Bundle**: {issue_counts['major']} major / {issue_counts['moderate']} moderate / "
                f"{issue_counts['minor']} minor"
            ),
            "",
            "## Artifacts",
            "",
            f"- **Primary**: `{_artifact_path(result, primary_name)}`",
            f"- **Companion**: `{_artifact_path(result, companion_name)}`",
            f"- **Structured Issues**: `{_artifact_path(result, 'final_issues.json')}`",
            f"- **Revision Roadmap**: `{_artifact_path(result, 'revision_roadmap.md')}`",
        ]
    )
    return "\n".join(lines)


def render_deep_review_report(result: AuditResult) -> str:
    """Render a deep-review-first Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    issues = _sort_deep_review_issues(result.issue_bundle)
    issue_counts = _count_deep_review_issues(issues)
    recommendation = _journal_recommendation(issues)
    roadmap = result.revision_roadmap or _default_revision_roadmap(result.issue_bundle)
    committee_score, editor_verdict = _committee_signal_from_artifacts(result.artifact_dir)

    lines = [
        "# Deep Review Report",
        "",
        f"**Paper**: `{result.file_path}` | **Language**: {result.language.upper()} | **Mode**: {result.mode}",
        f"**Generated**: {now}" + (f" | **Venue**: {result.venue}" if result.venue else ""),
    ]
    if result.review_focus != "full":
        lines.append(f"**Focus**: `{result.review_focus}`")
    if result.mode_alias_used:
        lines.append(
            f"**Compatibility Note**: legacy mode alias `{result.mode_alias_used}` mapped to `{result.mode}`."
        )
    if result.artifact_dir:
        lines.append(f"**Artifacts**: `{result.artifact_dir}`")
    lines.extend(["", "## Overall Assessment", ""])

    if result.overall_assessment:
        lines.append(result.overall_assessment)
    else:
        lines.append(
            "Deep review completed. Inspect the structured issue list below for the highest-impact "
            "claim, methodology, and consistency risks before revising."
        )
    lines.extend(
        [
            "",
            f"- **Major**: {issue_counts['major']}",
            f"- **Moderate**: {issue_counts['moderate']}",
            f"- **Minor**: {issue_counts['minor']}",
            "",
        ]
    )

    committee_blocks: list[str] = []
    if result.artifact_dir:
        committee_dir = Path(result.artifact_dir) / "committee"
        if committee_dir.exists():
            ordered = [
                ("editor.md", "### Editor (Desk Reject Screen)"),
                ("theory.md", "### Reviewer 1 (Theory Contribution)"),
                ("literature.md", "### Reviewer 3 (Literature Dialogue)"),
                ("methodology.md", "### Reviewer 2 (Methodology & Transparency)"),
                ("logic.md", "### Reviewer 4 (Logic Chain)"),
                ("consensus.md", "### Committee Consensus"),
            ]
            for filename, heading in ordered:
                path = committee_dir / filename
                if not path.exists():
                    continue
                text = path.read_text(encoding="utf-8").strip()
                if not text:
                    continue
                committee_blocks.extend([heading, "", text, ""])

    if committee_blocks:
        lines.extend(["## Academic Pre-Review Committee", ""])
        lines.extend(committee_blocks)

    if result.summary:
        lines.extend(["## Paper Summary", "", result.summary, ""])

    if result.issue_bundle:
        for severity, title in DEEP_REVIEW_SECTIONS:
            bucket = [issue for issue in issues if issue.severity == severity]
            if not bucket:
                continue
            lines.extend([f"## {title}", ""])
            for idx, issue in enumerate(bucket, 1):
                related = ", ".join(issue.related_sections) if issue.related_sections else "—"
                source_label = SOURCE_KIND_LABELS.get(issue.source_kind, "[LLM]")
                lines.append(f"### {severity[:1].upper()}{idx}: {issue.title}")
                lines.append(f"- **Type**: {issue.comment_type}")
                lines.append(f"- **Source**: {source_label} via `{issue.review_lane or 'review'}`")
                lines.append(f"- **Confidence**: {issue.confidence}")
                lines.append(f"- **Section**: {issue.source_section or 'unknown'}")
                lines.append(f"- **Related Sections**: {related}")
                if issue.root_cause_key:
                    lines.append(f"- **Root Cause Key**: `{issue.root_cause_key}`")
                if issue.quote_verified is not None:
                    lines.append(f"- **Quote Verified**: {'yes' if issue.quote_verified else 'no'}")
                lines.append(f"- **Quote**: `{issue.quote}`" if issue.quote else "- **Quote**: —")
                lines.append(f"- **Explanation**: {issue.explanation}")
                lines.append("")

    if result.issues:
        lines.extend(["## Phase 0 Automated Findings", ""])
        modules: dict[str, list[AuditIssue]] = {}
        for issue in result.issues:
            modules.setdefault(issue.module, []).append(issue)

        for module_name in sorted(modules.keys()):
            lines.extend([f"### [Script] {module_name}", ""])
            lines.extend(["| Line | Severity | Issue |", "|------|----------|-------|"])
            for issue in modules[module_name]:
                loc = str(issue.line) if issue.line else "---"
                lines.append(f"| {loc} | {issue.severity} | {issue.message} |")
            lines.append("")

    lines.extend(["## Decision Signals", ""])
    if committee_score is not None:
        lines.append(f"- **Committee Score**: {committee_score:.1f}/10")
    if editor_verdict:
        lines.append(f"- **Editor Verdict**: {editor_verdict}")
    lines.extend(
        [
            f"- **Reviewer Recommendation**: {recommendation}",
            (
                f"- **Issue Bundle**: {issue_counts['major']} major / {issue_counts['moderate']} moderate / "
                f"{issue_counts['minor']} minor"
            ),
            "",
        ]
    )

    if roadmap:
        lines.extend(["## Revision Roadmap", ""])
        for priority in ("Priority 1", "Priority 2", "Priority 3"):
            items = [item for item in roadmap if item.get("priority") == priority]
            if not items:
                continue
            lines.extend([f"### {priority}", ""])
            for item in items:
                source = item.get("source", "[LLM]")
                section = item.get("section", "unknown")
                title = item.get("title", "Untitled issue")
                lines.append(f"- [ ] {title} ({source}; {section})")
            lines.append("")

    return "\n".join(lines)


def render_polish_precheck_report(result: AuditResult, precheck: dict) -> str:
    """Render precheck summary shown before Critic agent is spawned."""
    lines = [
        "# Polish Precheck Report",
        "",
        f"**File**: `{result.file_path}` | **Language**: {result.language.upper()} "
        f"| **Style**: {precheck.get('style', 'A')}",
    ]
    if precheck.get("journal"):
        lines[-1] += f" | **Journal**: {precheck['journal']}"
    lines += [""]

    # Section map table
    lines += [
        "## Detected Sections",
        "",
        "| Section | Lines | Words |",
        "|---------|-------|-------|",
    ]
    for sec, meta in precheck.get("sections", {}).items():
        lines.append(f"| {sec} | {meta['start']}-{meta['end']} | {meta['word_count']} |")
    lines.append("")

    # Blockers
    blockers = precheck.get("blockers", [])
    if blockers:
        lines += ["## Blockers (must fix before polish)", ""]
        for b in blockers:
            loc = f"(Line {b['line']}) " if b.get("line") else ""
            lines.append(f"- **[{b['module']}]** {loc}{b['message']}")
        lines += ["", "Resolve these Critical issues and re-run before proceeding."]
    else:
        lines += ["## Status: Ready for Critic Phase", ""]

    n_logic = len(precheck.get("precheck_issues", []))
    n_expr = len(precheck.get("expression_issues", []))
    lines.append(f"**Pre-check findings**: {n_logic} logic, {n_expr} expression issues")
    if precheck.get("non_imrad"):
        lines += ["", "> **Note**: Non-standard section structure detected."]
    return "\n".join(lines)


# --- Report Renderers ---


def render_self_check_report(result: AuditResult) -> str:
    """Render a quick-audit-style Markdown report."""
    scores = calculate_scores(result.issues)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    blockers = [issue for issue in result.issues if issue.severity == "Critical"]
    quality_improvements = [issue for issue in result.issues if issue.severity != "Critical"]

    lines = [
        "# Paper Audit Report",
        "",
        f"**File**: `{result.file_path}` | **Language**: {result.language.upper()} | **Mode**: {result.mode}",
        f"**Generated**: {now}" + (f" | **Venue**: {result.venue}" if result.venue else ""),
        "",
    ]

    # Executive Summary
    total = len(result.issues)
    critical = sum(1 for i in result.issues if i.severity == "Critical")
    label = _score_label(scores["overall"])
    lines.extend(
        [
            "## Executive Summary",
            "",
            f"Found **{total} issues** ({critical} critical). "
            f"Overall score: **{scores['overall']:.1f}/6.0** ({label}).",
            "",
        ]
    )

    # Submission blockers first.
    lines.extend(["## Submission Blockers", ""])
    if blockers:
        for issue in blockers:
            loc = f"(Line {issue.line}) " if issue.line else ""
            lines.append(
                f"- [Script] **[{issue.module}]** {loc}"
                f"[Severity: {issue.severity}] [Priority: {issue.priority}]: "
                f"{issue.message}"
            )
            if issue.original:
                lines.append(f"  - Original: `{issue.original}`")
            if issue.revised:
                lines.append(f"  - Revised: `{issue.revised}`")
            if issue.rationale:
                lines.append(f"  - Rationale: {issue.rationale}")
    else:
        lines.append("- No submission blockers detected.")
    lines.append("")

    # High-signal quality improvements next.
    lines.extend(["## Quality Improvements", ""])
    if quality_improvements:
        for severity, heading in [
            ("Major", "### High-Signal Quality Issues"),
            ("Minor", "### Additional Quality Improvements"),
        ]:
            sev_issues = [issue for issue in quality_improvements if issue.severity == severity]
            if not sev_issues:
                continue
            lines.extend([heading, ""])
            for issue in sev_issues:
                loc = f"(Line {issue.line}) " if issue.line else ""
                lines.append(
                    f"- [Script] **[{issue.module}]** {loc}"
                    f"[Severity: {issue.severity}] [Priority: {issue.priority}]: "
                    f"{issue.message}"
                )
                if issue.original:
                    lines.append(f"  - Original: `{issue.original}`")
                if issue.revised:
                    lines.append(f"  - Revised: `{issue.revised}`")
                if issue.rationale:
                    lines.append(f"  - Rationale: {issue.rationale}")
            lines.append("")
    else:
        lines.append("- No quality improvements identified.")
        lines.append("")

    # Checklist
    if result.checklist:
        lines.extend(["## Pre-Submission Checklist", ""])
        for item in result.checklist:
            mark = "x" if item.passed else " "
            lines.append(f"- [{mark}] {item.description}")
            if not item.passed and item.details:
                lines.append(f"  - {item.details}")
        lines.append("")

    # Scores Table
    dim_issues_map: dict[str, list[AuditIssue]] = {
        "quality": [],
        "clarity": [],
        "significance": [],
        "originality": [],
    }
    for issue in result.issues:
        for dim in DIMENSION_MAP.get(issue.module.lower(), ["clarity"]):
            if dim in dim_issues_map:
                dim_issues_map[dim].append(issue)

    lines.extend(
        [
            "## Scores",
            "",
            "| Dimension | Score | Issues (C/M/m) | Key Finding |",
            "|-----------|-------|-----------------|-------------|",
        ]
    )
    for dim in ["quality", "clarity", "significance", "originality"]:
        dim_issues = dim_issues_map[dim]
        key_finding = dim_issues[0].message[:50] + "..." if dim_issues else "No issues"
        lines.append(
            f"| {dim.capitalize()} | {scores[dim]:.1f} | "
            f"{_count_issues(dim_issues)} | {key_finding} |"
        )
    lines.append(
        f"| **Overall** | **{scores['overall']:.1f}** | "
        f"{_count_issues(result.issues)} | **{label}** |"
    )
    lines.append("")

    return "\n".join(lines)


def render_review_report(result: AuditResult) -> str:
    """Render a peer-review simulation Markdown report."""
    if result.issue_bundle or result.mode == "deep-review":
        return render_deep_review_report(result)

    scores = calculate_scores(result.issues)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    label = _score_label(scores["overall"])

    lines = [
        "# Peer Review Report",
        "",
        f"**Paper**: `{result.file_path}` | **Language**: {result.language.upper()}",
        f"**Generated**: {now}"
        + (f" | **Venue**: {result.venue}" if result.venue else "")
        + " | **Review Round**: 1",
        "",
    ]

    # Summary
    if result.summary:
        lines.extend(["## Paper Summary", "", result.summary, ""])

    # Strengths (structured: S1, S2, ...)
    if result.strengths:
        lines.extend(["## Strengths", ""])
        for idx, s in enumerate(result.strengths, 1):
            if isinstance(s, dict):
                lines.append(f"### S{idx}: {s.get('title', 'Strength')}")
                lines.append(s.get("description", ""))
            else:
                lines.append(f"### S{idx}: {s}")
            lines.append("")

    # Weaknesses (structured: Problem + Why + Suggestion + Severity)
    if result.weaknesses:
        lines.extend(["## Weaknesses", ""])
        for idx, w in enumerate(result.weaknesses, 1):
            if isinstance(w, dict):
                lines.append(f"### W{idx}: {w.get('title', 'Weakness')}")
                lines.append(f"- **Problem**: {w.get('problem', w.get('title', ''))}")
                lines.append(f"- **Why it matters**: {w.get('why', 'Impacts paper quality')}")
                lines.append(f"- **Suggestion**: {w.get('suggestion', 'See detailed issues')}")
                lines.append(f"- **Severity**: {w.get('severity', 'Major')}")
            else:
                lines.append(f"### W{idx}: {w}")
            lines.append("")

    # Questions
    if result.questions:
        lines.extend(["## Questions for Authors", ""])
        for idx, q in enumerate(result.questions, 1):
            lines.append(f"{idx}. {q}")
        lines.append("")

    # Detailed Automated Findings (grouped by module)
    if result.issues:
        lines.extend(["## Detailed Automated Findings", ""])
        # Group by module
        modules: dict[str, list[AuditIssue]] = {}
        for issue in result.issues:
            modules.setdefault(issue.module, []).append(issue)

        for module_name in sorted(modules.keys()):
            module_issues = sorted(
                modules[module_name],
                key=lambda i: (
                    ("Critical", "Major", "Minor").index(i.severity)
                    if i.severity in ("Critical", "Major", "Minor")
                    else 3
                ),
            )
            lines.extend(
                [
                    f"### {module_name}",
                    "",
                    "| Line | Severity | Issue |",
                    "|------|----------|-------|",
                ]
            )
            for issue in module_issues:
                loc = str(issue.line) if issue.line else "---"
                lines.append(f"| {loc} | {issue.severity} | {issue.message} |")
            lines.append("")

    # Score & Recommendation
    lines.extend(
        [
            "## Overall Assessment",
            "",
            "| Dimension | Score | Label |",
            "|-----------|-------|-------|",
        ]
    )
    for dim in ["quality", "clarity", "significance", "originality"]:
        dim_label = _score_label(scores[dim])
        lines.append(f"| {dim.capitalize()} | {scores[dim]:.1f}/6.0 | {dim_label} |")
    lines.extend(
        [
            f"| **Overall** | **{scores['overall']:.1f}/6.0** | **{label}** |",
            "",
            f"**Recommendation**: {label}",
            "",
        ]
    )

    # Revision Roadmap
    critical = [i for i in result.issues if i.severity == "Critical"]
    major = [i for i in result.issues if i.severity == "Major"]
    minor = [i for i in result.issues if i.severity == "Minor"]

    if critical or major or minor:
        lines.extend(["## Revision Roadmap", ""])

        if critical:
            lines.extend(["### Priority 1 --- Must Address (Blocking)", ""])
            for idx, issue in enumerate(critical, 1):
                loc = f" (Line {issue.line})" if issue.line else ""
                lines.append(f"- [ ] R{idx}: [{issue.module}]{loc} {issue.message}")
            lines.append("")

        if major:
            lines.extend(["### Priority 2 --- Strongly Recommended", ""])
            for idx, issue in enumerate(major, 1):
                loc = f" (Line {issue.line})" if issue.line else ""
                lines.append(f"- [ ] S{idx}: [{issue.module}]{loc} {issue.message}")
            lines.append("")

        if minor:
            lines.extend(["### Priority 3 --- Optional Improvements", ""])
            for issue in minor:
                loc = f" (Line {issue.line})" if issue.line else ""
                lines.append(f"- [ ] [{issue.module}]{loc} {issue.message}")
            lines.append("")

    return "\n".join(lines)


def render_gate_report(result: AuditResult) -> str:
    """Render a quality gate pass/fail Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    blocking = [i for i in result.issues if i.severity == "Critical"]
    passed = len(blocking) == 0 and all(item.passed for item in result.checklist)
    verdict = "PASS" if passed else "FAIL"

    lines = [
        "# Quality Gate Report",
        "",
        f"**File**: `{result.file_path}` | **Language**: {result.language.upper()}",
        f"**Generated**: {now}",
        "",
        f"## Verdict: {verdict}",
        "",
    ]

    # Blocking Issues
    if blocking:
        lines.extend(["## Blocking Issues (must fix)", ""])
        for issue in blocking:
            loc = f"(Line {issue.line}) " if issue.line else ""
            lines.append(f"- [BLOCKING] **[{issue.module}]** {loc}{issue.message}")
        lines.append("")

    # Checklist
    if result.checklist:
        lines.extend(["## Checklist", ""])
        for item in result.checklist:
            status = "[PASS]" if item.passed else "[FAIL]"
            lines.append(f"- {status} {item.description}")
            if not item.passed and item.details:
                lines.append(f"  - {item.details}")
        lines.append("")

    # Non-blocking issues (informational)
    non_blocking = [i for i in result.issues if i.severity != "Critical"]
    if non_blocking:
        lines.extend(["## Advisory Recommendations (non-blocking)", ""])
        lines.append("These are advisory recommendations, not submission blockers.")
        lines.append("")
        for issue in non_blocking:
            loc = f"(Line {issue.line}) " if issue.line else ""
            lines.append(f"- [INFO] **[{issue.module}]** {loc}{issue.message}")
        lines.append("")

    return "\n".join(lines)


def render_json_report(result: AuditResult) -> str:
    """
    Export audit result as structured JSON for CI/CD integration.

    Args:
        result: Complete audit result.

    Returns:
        Formatted JSON string with file metadata, scores, verdict, issues, and checklist.
    """
    import json

    scores = calculate_scores(result.issues)
    data = {
        "file": result.file_path,
        "language": result.language,
        "mode": result.mode,
        "mode_alias_used": result.mode_alias_used,
        "venue": result.venue,
        "generated_at": datetime.now().isoformat(),
        "scores": {k: round(v, 2) for k, v in scores.items()},
        "verdict": _score_label(scores["overall"]),
        "issues": [
            {
                "module": i.module,
                "line": i.line,
                "severity": i.severity,
                "priority": i.priority,
                "message": i.message,
                "original": i.original,
                "revised": i.revised,
            }
            for i in result.issues
        ],
        "checklist": [
            {
                "description": c.description,
                "passed": c.passed,
                "details": c.details,
            }
            for c in result.checklist
        ],
    }
    if result.issue_bundle:
        data["issue_bundle"] = [
            normalize_deep_review_issue_dict(issue) for issue in result.issue_bundle
        ]
        data["overall_assessment"] = result.overall_assessment
        data["paper_summary"] = result.summary
        data["revision_roadmap"] = result.revision_roadmap or _default_revision_roadmap(
            result.issue_bundle
        )
        data["section_index"] = result.section_index
        data["artifact_dir"] = result.artifact_dir
        data["review_focus"] = result.review_focus
        data["review_recommendation"] = _journal_recommendation(
            _sort_deep_review_issues(result.issue_bundle)
        )
        committee_score, editor_verdict = _committee_signal_from_artifacts(result.artifact_dir)
        if committee_score is not None:
            data["committee_score"] = committee_score
        if editor_verdict:
            data["committee_verdict"] = editor_verdict
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_reaudit_report(result: AuditResult) -> str:
    """Render a re-audit comparison report.

    Shows which prior issues were addressed, partially addressed,
    still present, and which new issues appeared.
    """
    lines: list[str] = []
    data = result.reaudit_data or {}
    summary = data.get("summary", {})
    classifications = data.get("classifications", [])
    new_issues = data.get("new_issues", [])

    lines.append("# Re-Audit Report")
    lines.append("")
    lines.append(
        f"**File**: `{result.file_path}` | **Language**: {result.language} | **Mode**: re-audit"
    )
    if result.venue:
        lines.append(f"**Venue**: {result.venue}")
    lines.append(f"**Previous Report**: `{data.get('previous_report', 'N/A')}`")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}")
    lines.append("")

    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## Revision Summary")
    lines.append("")
    total_prior = data.get("prior_issue_count", 0)
    fixed = summary.get("fully_addressed", 0)
    partial = summary.get("partially_addressed", 0)
    remaining = summary.get("not_addressed", 0)
    new_count = summary.get("new", 0)
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Prior issues | {total_prior} |")
    lines.append(f"| Fully addressed | {fixed} |")
    lines.append(f"| Partially addressed | {partial} |")
    lines.append(f"| Not addressed | {remaining} |")
    lines.append(f"| New issues | {new_count} |")
    lines.append("")

    # Progress indicator
    if total_prior > 0:
        pct = round((fixed / total_prior) * 100)
        lines.append(f"**Resolution rate**: {pct}% ({fixed}/{total_prior} fully resolved)")
    lines.append("")

    # Prior issue verification
    if classifications:
        lines.append("---")
        lines.append("")
        lines.append("## Prior Issue Verification")
        lines.append("")
        lines.append(
            "| # | root_cause_key | Module | Prior Severity | Status | Current | Message |"
        )
        lines.append("|---|----------------|--------|---------------|--------|---------|---------|")
        for idx, c in enumerate(classifications, 1):
            cur_sev = c.get("current_severity") or "\u2014"
            root_cause = c.get("root_cause_key") or "root cause unavailable"
            msg = c["prior_message"]
            if len(msg) > 80:
                msg = msg[:77] + "..."
            lines.append(
                f"| {idx} | {root_cause} | {c['prior_module']} | {c['prior_severity']} "
                f"| {c['status']} | {cur_sev} | {msg} |"
            )
        lines.append("")

    # New issues
    if new_issues:
        lines.append("---")
        lines.append("")
        lines.append("## New Issues (not in previous report)")
        lines.append("")
        lines.append("| # | Module | Line | Severity | Issue |")
        lines.append("|---|--------|------|----------|-------|")
        for idx, ni in enumerate(new_issues, 1):
            loc = str(ni.get("line")) if ni.get("line") else "\u2014"
            lines.append(f"| {idx} | {ni['module']} | {loc} | {ni['severity']} | {ni['message']} |")
        lines.append("")

    # Current scores
    scores = calculate_scores(result.issues)
    overall = scores.get("overall", 6.0)
    lines.append("---")
    lines.append("")
    lines.append("## Current Scores")
    lines.append("")
    lines.append("| Dimension | Score |")
    lines.append("|-----------|-------|")
    for dim in ("quality", "clarity", "significance", "originality"):
        lines.append(f"| {dim.title()} | {scores.get(dim, 6.0):.1f} / 6.0 |")
    lines.append(f"| **Overall** | **{overall:.2f} / 6.0** |")
    lines.append("")

    # Recommendation
    lines.append("---")
    lines.append("")
    if remaining == 0 and new_count == 0:
        lines.append("*All prior issues resolved and no new issues found. Ready for next step.*")
    elif remaining == 0:
        lines.append(
            f"*All prior issues resolved, but {new_count} new issue(s) detected. "
            f"Review new issues before proceeding.*"
        )
    else:
        lines.append(
            f"*{remaining} prior issue(s) still unresolved. Continue revision and re-run audit.*"
        )
    lines.append("")

    return "\n".join(lines)


def render_report(result: AuditResult, *, report_style: str = "deep-review") -> str:
    """
    Render the appropriate report based on audit mode.

    Args:
        result: Complete audit result.

    Returns:
        Formatted Markdown report string.
    """
    if result.mode == "deep-review":
        report = render_deep_review_summary(result, primary_style=report_style)
    elif result.mode == "review":
        report = render_review_report(result)
    elif result.mode == "quick-audit":
        report = render_self_check_report(result)
    elif result.mode == "gate":
        report = render_gate_report(result)
    elif result.mode == "re-audit":
        report = render_reaudit_report(result)
    elif result.mode == "polish":
        # For polish mode, render_self_check_report shows precheck issues
        report = render_self_check_report(result)
    else:
        report = render_self_check_report(result)

    # Append ScholarEval report if available
    if result.scholar_eval_result is not None:
        try:
            from scholar_eval import render_scholar_eval_report

            report += "\n\n" + render_scholar_eval_report(result.scholar_eval_result)
        except Exception:
            pass

    # Append literature comparison section if available
    if result.literature_context is not None:
        try:
            from literature_compare import render_comparison_report

            if hasattr(result.literature_context, "comparison_result"):
                report += "\n\n" + render_comparison_report(
                    result.literature_context.comparison_result
                )
            elif hasattr(result.literature_context, "filtered_results"):
                from literature_search import render_literature_summary

                report += "\n\n" + render_literature_summary(result.literature_context)
        except Exception:
            pass

    return report
