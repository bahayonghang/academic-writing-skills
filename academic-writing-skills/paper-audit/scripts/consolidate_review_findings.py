"""Consolidate deep-review lane findings into a final issue bundle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from paths import WorkspaceLayout

SEVERITY_ORDER = {"major": 0, "moderate": 1, "minor": 2}
CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2, "unverified": 3}
VALID_TYPES = {"methodology", "claim_accuracy", "presentation", "missing_information"}
VALID_SOURCE_KINDS = {"llm", "script"}

FRAME_LOCK_THRESHOLD = 0.6
"""Surrender rate above which a reviewer file is treated as frame-locked.

Issues that originated from a reviewer payload exposing
``surrender_rate > FRAME_LOCK_THRESHOLD`` are demoted by one confidence step
and tagged with an advisory note. The gate decision is not modified — this is
informational, not a blocker.
"""

CONFIDENCE_DOWNGRADE = {
    "high": "medium",
    "medium": "low",
    "low": "low",
    "unverified": "unverified",
}


def slugify(value: str) -> str:
    """Create a normalized key for root cause comparisons."""
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "issue"


def sanitize_issue(issue: dict) -> dict:
    """Fill defaults and normalize the expected issue schema."""
    title = issue.get("title", "Untitled issue").strip()
    quote = issue.get("quote", "").strip()
    explanation = issue.get("explanation", "").strip()
    severity = str(issue.get("severity", "moderate")).lower()
    comment_type = issue.get("comment_type", "missing_information")
    source_kind = str(issue.get("source_kind", "llm")).lower()
    confidence = str(issue.get("confidence", "medium")).lower()

    if severity not in SEVERITY_ORDER:
        severity = "moderate"
    if comment_type not in VALID_TYPES:
        comment_type = "missing_information"
    if source_kind not in VALID_SOURCE_KINDS:
        source_kind = "llm"
    if confidence not in CONFIDENCE_ORDER:
        confidence = "medium"

    related = [item for item in issue.get("related_sections", []) if item]
    section = issue.get("source_section", "").strip()
    if section and section not in related:
        related = [section, *related]

    return {
        "title": title,
        "quote": quote,
        "explanation": explanation,
        "comment_type": comment_type,
        "severity": severity,
        "confidence": confidence,
        "source_kind": source_kind,
        "source_section": section,
        "related_sections": related,
        "root_cause_key": issue.get("root_cause_key") or slugify(title),
        "review_lane": issue.get("review_lane", "").strip(),
        "gate_blocker": bool(issue.get("gate_blocker", severity == "major")),
        "quote_verified": issue.get("quote_verified"),
    }


def apply_frame_lock_advisory(issues: list[dict], rate: float) -> list[dict]:
    """Demote confidence and tag explanation when a reviewer file is frame-locked.

    Mutates each issue in place: confidence drops by one step (high -> medium,
    medium -> low, low stays, unverified stays) and a short advisory marker is
    appended to ``explanation`` so the downstream report can surface why the
    confidence was lowered. The advisory is appended at most once per issue.
    """
    advisory = f"(advisory: frame_lock_alert, surrender_rate={rate:.2f})"
    for issue in issues:
        issue["confidence"] = CONFIDENCE_DOWNGRADE.get(issue["confidence"], issue["confidence"])
        if advisory not in issue["explanation"]:
            issue["explanation"] = (issue["explanation"] + " " + advisory).strip()
    return issues


def load_comment_files(comments_dir: Path) -> list[dict]:
    """Load every JSON file from the comments directory.

    Recognises two payload shapes per file:
    * a plain list of issues (legacy / lane output)
    * a dict ``{"issues": [...], "surrender_rate": float, ...}`` (critical
      reviewer style). When ``surrender_rate > FRAME_LOCK_THRESHOLD``, the
      file's issues are demoted via :func:`apply_frame_lock_advisory`.
    """
    findings: list[dict] = []
    for path in sorted(comments_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            items = payload.get("issues", []) or []
            rate_raw = payload.get("surrender_rate")
            try:
                rate_value = float(rate_raw) if rate_raw is not None else None
            except (TypeError, ValueError):
                rate_value = None
        else:
            items = payload
            rate_value = None

        batch: list[dict] = []
        for raw_issue in items:
            issue = sanitize_issue(raw_issue)
            issue["source_file"] = path.name
            batch.append(issue)

        if rate_value is not None and rate_value > FRAME_LOCK_THRESHOLD:
            batch = apply_frame_lock_advisory(batch, rate_value)

        findings.extend(batch)
    return findings


def consolidate_findings(issues: list[dict]) -> list[dict]:
    """Deduplicate exact overlaps while keeping distinct consequences separate."""
    consolidated: list[dict] = []
    seen: dict[tuple[str, str, str, str], int] = {}

    for issue in issues:
        key = (
            issue["root_cause_key"],
            issue["comment_type"],
            issue["source_section"],
            slugify(issue["quote"][:160] or issue["title"]),
        )
        if key not in seen:
            seen[key] = len(consolidated)
            consolidated.append(issue)
            continue

        current = consolidated[seen[key]]
        if SEVERITY_ORDER[issue["severity"]] < SEVERITY_ORDER[current["severity"]]:
            current["severity"] = issue["severity"]
        if CONFIDENCE_ORDER[issue["confidence"]] < CONFIDENCE_ORDER[current["confidence"]]:
            current["confidence"] = issue["confidence"]
        if len(issue["explanation"]) > len(current["explanation"]):
            current["explanation"] = issue["explanation"]
        for section in issue["related_sections"]:
            if section and section not in current["related_sections"]:
                current["related_sections"].append(section)
        if issue["review_lane"] and issue["review_lane"] not in current["review_lane"]:
            current["review_lane"] = ", ".join(
                [part for part in [current["review_lane"], issue["review_lane"]] if part]
            )
        current["gate_blocker"] = current["gate_blocker"] or issue["gate_blocker"]

    return sorted(
        consolidated,
        key=lambda item: (
            SEVERITY_ORDER[item["severity"]],
            item["source_section"],
            item["title"].lower(),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolidate deep-review finding JSON files")
    parser.add_argument("review_dir", help="Path to a prepared review workspace")
    args = parser.parse_args()

    review_dir = Path(args.review_dir).resolve()
    layout = WorkspaceLayout(review_dir)
    findings = load_comment_files(layout.comments_dir)
    consolidated = consolidate_findings(findings)

    layout.all_comments.parent.mkdir(parents=True, exist_ok=True)
    layout.all_comments.write_text(
        json.dumps(findings, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    layout.final_issues.write_text(
        json.dumps(consolidated, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    for issue in consolidated:
        print(f"- {issue['severity'].upper()}: {issue['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
