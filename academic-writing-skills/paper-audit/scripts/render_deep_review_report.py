"""Render a deep-review Markdown report from workspace artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import WorkspaceLayout
from report_generator import (
    AuditResult,
    coerce_deep_review_issue,
    render_deep_review_report,
    render_peer_review_report,
)


def _read_json_if_exists(
    path: Path, default: list[dict] | dict | None = None
) -> list[dict] | dict | None:
    """Load JSON from path when present, otherwise return the provided default."""
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text_if_exists(path: Path, *, strip: bool = False) -> str:
    """Load text from path when present, otherwise return an empty string."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text.strip() if strip else text


def _load_revision_roadmap(layout: WorkspaceLayout) -> list[dict]:
    """Load roadmap items from revision_suggestions.md if present."""
    roadmap_path = layout.revision_suggestions_md
    if not roadmap_path.exists():
        return []

    items: list[dict] = []
    current_priority = ""
    for raw_line in roadmap_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("### Priority "):
            current_priority = line.removeprefix("### ").strip().split(" ---")[0].strip()
            continue
        if line.startswith("## Priority "):
            current_priority = line.removeprefix("## ").strip()
            continue
        if line.startswith("## "):
            # Top-level section like "## Revision Roadmap" — keep prior priority context.
            continue
        if not line.startswith("- [ ] "):
            continue
        body = line.removeprefix("- [ ] ")
        title, _, meta = body.partition(" (")
        meta = meta.rstrip(")")
        source, _, section = meta.partition("; ")
        items.append(
            {
                "priority": current_priority or "Priority 3",
                "title": title.strip(),
                "source": source.strip() or "[LLM]",
                "section": section.strip() or "unknown",
            }
        )
    return items


def load_result(review_dir: Path) -> AuditResult:
    """Load workspace artifacts into an AuditResult for rendering."""
    layout = WorkspaceLayout(review_dir)
    metadata = _read_json_if_exists(layout.metadata, {}) or {}
    final_issues = _read_json_if_exists(layout.final_issues, []) or []
    section_index = _read_json_if_exists(layout.section_index, []) or []

    return AuditResult(
        file_path=metadata.get("source_path", metadata.get("title", "paper")),
        language=metadata.get("language", "en"),
        mode="deep-review",
        review_focus=metadata.get("review_focus", "full"),
        issue_bundle=[coerce_deep_review_issue(issue) for issue in final_issues],
        summary=_read_text_if_exists(layout.paper_summary),
        overall_assessment=_read_text_if_exists(layout.overall_assessment, strip=True),
        section_index=section_index,
        revision_roadmap=_load_revision_roadmap(layout),
        artifact_dir=str(review_dir),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deep-review report from workspace")
    parser.add_argument("review_dir", help="Path to the deep-review workspace")
    parser.add_argument(
        "--style",
        choices=("deep-review", "peer-review"),
        default="deep-review",
        help="Report style to render (defaults to deep-review)",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh"),
        default=None,
        help="Report language (defaults to metadata.json language, fallback en)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help=(
            "Optional output path "
            "(defaults to <review_dir>/review_report.md or "
            "<review_dir>/artifacts/summary/peer_review_report.md)"
        ),
    )
    args = parser.parse_args()

    review_dir = Path(args.review_dir).resolve()
    layout = WorkspaceLayout(review_dir)
    result = load_result(review_dir)
    lang = args.lang or result.language or "en"
    if lang not in {"en", "zh"}:
        lang = "en"
    if args.style == "peer-review":
        report = render_peer_review_report(result, lang=lang)
        default_output = layout.peer_review_report
    else:
        report = render_deep_review_report(result, lang=lang)
        default_output = layout.review_report_md
    output_path = Path(args.output).resolve() if args.output else default_output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
