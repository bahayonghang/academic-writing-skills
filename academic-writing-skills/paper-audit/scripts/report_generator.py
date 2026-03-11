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
                lines.append(
                    f"- **Why it matters**: {w.get('why', 'Impacts paper quality')}"
                )
                lines.append(
                    f"- **Suggestion**: {w.get('suggestion', 'See detailed issues')}"
                )
                lines.append(
                    f"- **Severity**: {w.get('severity', 'Major')}"
                )
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
            for idx, issue in enumerate(minor, 1):
                loc = f" (Line {issue.line})" if issue.line else ""
                lines.append(f"- [ ] [{issue.module}]{loc} {issue.message}")
            lines.append("")

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
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
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
        lines.append("| # | Module | Prior Severity | Status | Current | Message |")
        lines.append("|---|--------|---------------|--------|---------|---------|")
        for idx, c in enumerate(classifications, 1):
            status = c["status"]
            if status == "FULLY_ADDRESSED":
                status_label = "FIXED"
            elif status == "PARTIALLY_ADDRESSED":
                status_label = "PARTIAL"
            else:
                status_label = "OPEN"
            cur_sev = c.get("current_severity") or "\u2014"
            msg = c["prior_message"]
            if len(msg) > 80:
                msg = msg[:77] + "..."
            lines.append(
                f"| {idx} | {c['prior_module']} | {c['prior_severity']} "
                f"| {status_label} | {cur_sev} | {msg} |"
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
            lines.append(
                f"| {idx} | {ni['module']} | {loc} | {ni['severity']} | {ni['message']} |"
            )
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
            f"*{remaining} prior issue(s) still unresolved. "
            f"Continue revision and re-run audit.*"
        )
    lines.append("")

    return "\n".join(lines)


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

    return report
