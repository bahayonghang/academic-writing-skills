"""Verify that deep-review issue quotes can be located in the source text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import WorkspaceLayout

UNVERIFIED_CONFIDENCE = "unverified"
"""Confidence label applied when an issue's quote is not found in the source."""


def verify_quotes(full_text: str, issues: list[dict]) -> list[dict]:
    """Annotate issues with quote verification status.

    Each returned record is a shallow copy of the input with ``quote_verified``
    set to ``True`` when the quote substring is present in ``full_text`` and a
    non-empty string was provided. Confidence is not touched here so callers
    that only want a probe (e.g. the default ``verify_quotes.py`` invocation)
    do not silently rewrite labels.
    """
    updated: list[dict] = []
    for issue in issues:
        quote = issue.get("quote", "").strip()
        verified = bool(quote and quote in full_text)
        patched = dict(issue)
        patched["quote_verified"] = verified
        updated.append(patched)
    return updated


def demote_unverified_confidence(
    issues: list[dict], *, unverified_label: str = UNVERIFIED_CONFIDENCE
) -> list[dict]:
    """Force confidence to ``unverified`` for issues with ``quote_verified=False``.

    Returns a shallow-copied list. Issues with ``quote_verified`` truthy or
    missing keep their original confidence. The mutation only happens when
    callers commit the result back to disk (the ``--write-back`` path).
    """
    demoted: list[dict] = []
    for issue in issues:
        patched = dict(issue)
        if patched.get("quote_verified") is False:
            patched["confidence"] = unverified_label
        demoted.append(patched)
    return demoted


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify quotes in final_issues.json")
    parser.add_argument("review_dir", help="Path to a deep-review workspace")
    parser.add_argument(
        "--write-back",
        action="store_true",
        help="Rewrite final_issues.json with quote_verified annotations "
        "(also demotes confidence to 'unverified' when the quote is missing)",
    )
    args = parser.parse_args()

    review_dir = Path(args.review_dir).resolve()
    layout = WorkspaceLayout(review_dir)
    full_text = layout.full_text.read_text(encoding="utf-8")
    issues_path = layout.final_issues
    issues = json.loads(issues_path.read_text(encoding="utf-8"))
    updated = verify_quotes(full_text, issues)
    verified_count = sum(1 for issue in updated if issue.get("quote_verified"))

    if args.write_back:
        committed = demote_unverified_confidence(updated)
        issues_path.write_text(
            json.dumps(committed, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    print(f"Verified {verified_count}/{len(updated)} quotes")
    return 0 if verified_count == len(updated) else 1


if __name__ == "__main__":
    raise SystemExit(main())
