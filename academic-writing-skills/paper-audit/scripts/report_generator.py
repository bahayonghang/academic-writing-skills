"""
Report Generator for Paper Audit skill.
Handles scoring engine, issue aggregation, and Markdown report rendering.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

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
    mode: str  # "self-check", "review", "gate", "polish"
    venue: str = ""  # e.g., "neurips", "ieee"
    issues: list[AuditIssue] = field(default_factory=list)
    checklist: list[ChecklistItem] = field(default_factory=list)
    # Review mode extras
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    summary: str = ""
    # ScholarEval result (optional, populated when --scholar-eval is used)
    scholar_eval_result: object | None = None


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
    "sentences": ["clarity"],
    "deai": ["clarity", "originality"],
    "bib": ["quality"],
    "figures": ["clarity"],
    "consistency": ["clarity"],
    "gbt7714": ["quality"],
    "checklist": ["quality", "clarity", "significance", "originality"],
    "references": ["clarity", "quality"],
    "visual": ["clarity"],
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
    """Render a self-check mode Markdown report."""
    scores = calculate_scores(result.issues)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

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

    # Issues by Severity
    lines.extend(["## Issues", ""])
    for severity in ["Critical", "Major", "Minor"]:
        sev_issues = [i for i in result.issues if i.severity == severity]
        if sev_issues:
            lines.append(f"### {severity}")
            lines.append("")
            for issue in sev_issues:
                loc = f"(Line {issue.line}) " if issue.line else ""
                lines.append(
                    f"- **[{issue.module}]** {loc}"
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

    # Checklist
    if result.checklist:
        lines.extend(["## Pre-Submission Checklist", ""])
        for item in result.checklist:
            mark = "x" if item.passed else " "
            lines.append(f"- [{mark}] {item.description}")
            if not item.passed and item.details:
                lines.append(f"  - {item.details}")
        lines.append("")

    return "\n".join(lines)


def render_review_report(result: AuditResult) -> str:
    """Render a peer-review simulation Markdown report."""
    scores = calculate_scores(result.issues)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    label = _score_label(scores["overall"])

    lines = [
        "# Peer Review Report",
        "",
        f"**File**: `{result.file_path}` | **Language**: {result.language.upper()}",
        f"**Generated**: {now}" + (f" | **Target Venue**: {result.venue}" if result.venue else ""),
        "",
    ]

    # Summary
    if result.summary:
        lines.extend(["## Summary", "", result.summary, ""])

    # Strengths
    if result.strengths:
        lines.extend(["## Strengths", ""])
        for s in result.strengths:
            lines.append(f"- {s}")
        lines.append("")

    # Weaknesses
    if result.weaknesses:
        lines.extend(["## Weaknesses", ""])
        for w in result.weaknesses:
            lines.append(f"- {w}")
        lines.append("")

    # Questions
    if result.questions:
        lines.extend(["## Questions for Authors", ""])
        for q in result.questions:
            lines.append(f"- {q}")
        lines.append("")

    # Detailed Issues
    if result.issues:
        lines.extend(["## Detailed Issues", ""])
        for issue in sorted(
            result.issues,
            key=lambda i: (
                ("Critical", "Major", "Minor").index(i.severity)
                if i.severity in ("Critical", "Major", "Minor")
                else 3
            ),
        ):
            loc = f"(Line {issue.line}) " if issue.line else ""
            lines.append(f"- **[{issue.module}]** {loc}[{issue.severity}]: {issue.message}")
        lines.append("")

    # Score & Recommendation
    lines.extend(
        [
            "## Overall Assessment",
            "",
            "| Dimension | Score |",
            "|-----------|-------|",
        ]
    )
    for dim in ["quality", "clarity", "significance", "originality"]:
        lines.append(f"| {dim.capitalize()} | {scores[dim]:.1f}/6.0 |")
    lines.extend(
        [
            f"| **Overall** | **{scores['overall']:.1f}/6.0** |",
            "",
            f"**Recommendation**: {label}",
            "",
        ]
    )

    return "\n".join(lines)


def render_gate_report(result: AuditResult) -> str:
    """Render a quality gate pass/fail Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    blocking = [i for i in result.issues if i.severity == "Critical"]
    passed = len(blocking) == 0 and all(item.passed for item in result.checklist)
    verdict = "PASS ✅" if passed else "FAIL ❌"

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
            lines.append(f"- ❌ **[{issue.module}]** {loc}{issue.message}")
        lines.append("")

    # Checklist
    if result.checklist:
        lines.extend(["## Checklist", ""])
        for item in result.checklist:
            icon = "✅" if item.passed else "❌"
            lines.append(f"- {icon} {item.description}")
            if not item.passed and item.details:
                lines.append(f"  - {item.details}")
        lines.append("")

    # Non-blocking issues (informational)
    non_blocking = [i for i in result.issues if i.severity != "Critical"]
    if non_blocking:
        lines.extend(["## Non-Blocking Issues (informational)", ""])
        for issue in non_blocking:
            loc = f"(Line {issue.line}) " if issue.line else ""
            lines.append(f"- ⚠️ **[{issue.module}]** {loc}{issue.message}")
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
    return json.dumps(data, indent=2, ensure_ascii=False)


def render_report(result: AuditResult) -> str:
    """
    Render the appropriate report based on audit mode.

    Args:
        result: Complete audit result.

    Returns:
        Formatted Markdown report string.
    """
    if result.mode == "review":
        report = render_review_report(result)
    elif result.mode == "gate":
        report = render_gate_report(result)
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

    return report
