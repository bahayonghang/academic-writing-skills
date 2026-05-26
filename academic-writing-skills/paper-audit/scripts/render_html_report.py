"""Render HTML reports from deep-review workspace artifacts via Jinja2."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from i18n import normalize_lang, t
from paths import WorkspaceLayout
from render_deep_review_report import load_result
from report_generator import (
    AuditResult,
    _committee_signal_from_artifacts,
    _count_deep_review_issues,
    _journal_recommendation,
    _recommendation_display,
    _severity_display,
    _sort_deep_review_issues,
    coerce_deep_review_issue,
)

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _strip_markdown_bold(text: str) -> str:
    """Remove leading ``**`` / trailing ``**`` markers used in MD labels."""
    return re.sub(r"\*\*", "", text)


def _strip_md_filter(value: str) -> str:
    return _strip_markdown_bold(value)


def _committee_blocks(layout: WorkspaceLayout, lang: str) -> list[dict]:
    committee_dir = layout.committee_dir
    if not committee_dir.exists():
        legacy = layout.root / "committee"
        if legacy.exists():
            committee_dir = legacy
        else:
            return []
    ordered = [
        ("editor.md", t("subsection.committee.editor", lang)),
        ("theory.md", t("subsection.committee.theory", lang)),
        ("literature.md", t("subsection.committee.literature", lang)),
        ("methodology.md", t("subsection.committee.methodology", lang)),
        ("logic.md", t("subsection.committee.logic", lang)),
        ("consensus.md", t("subsection.committee.consensus", lang)),
    ]
    blocks: list[dict] = []
    for filename, heading in ordered:
        path = committee_dir / filename
        if not path.exists():
            continue
        body = path.read_text(encoding="utf-8").strip()
        if not body:
            continue
        # Strip leading ### from heading for HTML h3
        clean_heading = heading.replace("### ", "")
        blocks.append({"heading": clean_heading, "body": body})
    return blocks


def _build_review_context(layout: WorkspaceLayout, result: AuditResult, lang: str) -> dict:
    issues = _sort_deep_review_issues(result.issue_bundle)
    issue_counts = _count_deep_review_issues(issues)
    recommendation = _journal_recommendation(issues)
    committee_score, editor_verdict = _committee_signal_from_artifacts(result.artifact_dir)

    issue_buckets = []
    severity_keys = [
        ("major", "section.major_issues", "M"),
        ("moderate", "section.moderate_issues", "S"),
        ("minor", "section.minor_issues", "N"),
    ]
    for severity, heading_key, prefix in severity_keys:
        bucket_items = [issue for issue in issues if issue.severity == severity]
        if not bucket_items:
            continue
        issue_buckets.append(
            {
                "anchor": f"{severity}-issues",
                "heading": t(heading_key, lang).replace("## ", ""),
                "prefix": prefix,
                "issues": bucket_items,
            }
        )

    issue_bundle_summary = t(
        "status.issue_bundle_template",
        lang,
        major=issue_counts["major"],
        moderate=issue_counts["moderate"],
        minor=issue_counts["minor"],
    )

    overall_assessment_text = (
        result.overall_assessment.strip()
        if result.overall_assessment
        else t("status.deep_review_default_assessment_long", lang)
    )

    toc_entries = [
        {
            "anchor": "overall-assessment",
            "label": t("section.overall_assessment", lang).replace("## ", ""),
        }
    ]
    committee_sections = _committee_blocks(layout, lang)
    if committee_sections:
        toc_entries.append(
            {
                "anchor": "committee",
                "label": t("section.committee", lang).replace("## ", ""),
            }
        )
    if result.summary:
        toc_entries.append(
            {
                "anchor": "paper-summary",
                "label": t("section.paper_summary", lang).replace("## ", ""),
            }
        )
    for bucket in issue_buckets:
        toc_entries.append({"anchor": bucket["anchor"], "label": bucket["heading"]})
    toc_entries.append(
        {
            "anchor": "decision-signals",
            "label": t("section.decision_signals", lang).replace("## ", ""),
        }
    )

    def source_label(issue) -> str:
        return "[Script]" if getattr(issue, "source_kind", "") == "script" else "[LLM]"

    return {
        "lang": lang,
        "title_text": t("title.deep_review", lang).replace("# ", ""),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "result": result,
        "issue_counts": issue_counts,
        "overall_assessment_text": overall_assessment_text,
        "committee_sections": committee_sections,
        "issue_buckets": issue_buckets,
        "committee_score": committee_score,
        "editor_verdict": editor_verdict,
        "recommendation_display": _recommendation_display(recommendation, lang),
        "issue_bundle_summary": issue_bundle_summary,
        "toc_label": t("section.overall_assessment", lang).replace("## ", "").upper(),
        "toc_entries": toc_entries,
        "severity_display": lambda value: _severity_display(value, lang),
        "source_label": source_label,
    }


def _build_revision_context(
    result: AuditResult,
    lang: str,
    suggestions: list[dict],
) -> dict:
    roadmap = result.revision_roadmap or []
    priority_keys = {
        "Priority 1": "subsection.priority_1",
        "Priority 2": "subsection.priority_2",
        "Priority 3": "subsection.priority_3",
    }
    roadmap_buckets = []
    for priority, key in priority_keys.items():
        items = [item for item in roadmap if item.get("priority") == priority]
        if not items:
            continue
        roadmap_buckets.append(
            {
                "heading": t(key, lang).replace("### ", ""),
                "tasks": items,
            }
        )

    toc_entries = []
    if roadmap_buckets:
        toc_entries.append(
            {
                "anchor": "revision-roadmap",
                "label": t("section.revision_roadmap", lang).replace("## ", ""),
            }
        )
    if suggestions:
        toc_entries.append(
            {
                "anchor": "detailed-suggestions",
                "label": t("section.suggestions_breakdown", lang).replace("## ", ""),
            }
        )

    return {
        "lang": lang,
        "title_text": t("title.revision_suggestions", lang).replace("# ", ""),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "result": result,
        "opening_text": t("suggestions.opening", lang),
        "roadmap_buckets": roadmap_buckets,
        "suggestions": suggestions,
        "toc_label": t("section.revision_suggestions", lang).replace("## ", "").upper(),
        "toc_entries": toc_entries,
        "severity_display": lambda value: _severity_display(value, lang),
    }


def _get_environment():
    """Lazy-import Jinja2 so the rest of the script imports cleanly."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.filters["striptags_md"] = _strip_md_filter
    return env


def render_html_reports(review_dir: Path, *, lang: str = "en") -> tuple[Path, Path]:
    """Render both review_report.html and revision_suggestions.html.

    Returns the paths of the two generated files.
    """
    lang = normalize_lang(lang)
    layout = WorkspaceLayout(review_dir)
    result = load_result(review_dir)

    # Use the same in-memory result that the MD renderer uses, but make sure
    # the issue bundle is coerced (load_result already does this).
    result.issue_bundle = [coerce_deep_review_issue(issue) for issue in result.issue_bundle]

    env = _get_environment()

    # Review report ---------------------------------------------------------
    review_ctx = _build_review_context(layout, result, lang)

    def _t(key: str, **kwargs):
        return t(key, lang, **kwargs)

    review_ctx["t"] = _t

    review_template = env.get_template("review_report.html.j2")
    review_html = review_template.render(**review_ctx)
    layout.review_report_html.write_text(review_html, encoding="utf-8")

    # Revision suggestions --------------------------------------------------
    suggestions: list[dict] = []
    if layout.revision_suggestions_json.exists():
        try:
            payload = json.loads(layout.revision_suggestions_json.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                suggestions = payload
        except (OSError, json.JSONDecodeError):
            suggestions = []

    revision_ctx = _build_revision_context(result, lang, suggestions)
    revision_ctx["t"] = _t
    revision_template = env.get_template("revision_suggestions.html.j2")
    revision_html = revision_template.render(**revision_ctx)
    layout.revision_suggestions_html.write_text(revision_html, encoding="utf-8")

    return layout.review_report_html, layout.revision_suggestions_html


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deep-review HTML reports")
    parser.add_argument("review_dir", help="Path to a deep-review workspace")
    parser.add_argument(
        "--lang",
        choices=("en", "zh"),
        default=None,
        help="Report language (defaults to metadata.json language, fallback en)",
    )
    args = parser.parse_args()

    review_dir = Path(args.review_dir).resolve()
    layout = WorkspaceLayout(review_dir)
    if not layout.metadata.exists():
        raise FileNotFoundError(f"metadata.json missing at {layout.metadata}")

    inferred_lang = "en"
    try:
        metadata = json.loads(layout.metadata.read_text(encoding="utf-8"))
        inferred_lang = metadata.get("language", "en") or "en"
    except (OSError, json.JSONDecodeError):
        pass
    lang = args.lang or inferred_lang
    review_html, revision_html = render_html_reports(review_dir, lang=lang)
    print(f"HTML written to {review_html}")
    print(f"HTML written to {revision_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
