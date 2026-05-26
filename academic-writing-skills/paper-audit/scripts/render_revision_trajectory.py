"""Render a per-round score trajectory comparing previous and current audits.

Reads ``round_scores`` from one or both ``final_issues.json`` files (the
extended dict-shaped schema) and emits a Markdown table flagging per-dimension
regressions. When neither bundle exposes ``round_scores`` the writer silently
no-ops so callers can integrate this unconditionally.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import WorkspaceLayout

DEGRADATION_THRESHOLD = 5.0
"""Default per-dimension drop (R_prev - R_current) that triggers a ⚠️↓ marker."""


def load_bundle(path: Path) -> tuple[list[dict], dict]:
    """Load issues and optional round_scores from a final_issues.json file.

    Accepts both the legacy top-level list and the dict-shaped extension
    ``{"issues": [...], "round_scores": {...}}``. Returns an empty scores
    dict when the file is in legacy form or the field is absent.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload, {}
    issues = payload.get("issues", []) or []
    scores = payload.get("round_scores", {}) or {}
    return issues, scores


def normalize_scores(scores: dict) -> dict[str, float]:
    """Coerce a raw round_scores dict into a stable {dimension: float} map.

    Non-numeric values are dropped silently; keys preserve their original
    order so the rendered table stays predictable.
    """
    out: dict[str, float] = {}
    for key, value in scores.items():
        try:
            out[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return out


def _format_cell(value: float | None, *, mark_degrade: bool = False) -> str:
    if value is None:
        return "-"
    text = f"{value:g}"
    if mark_degrade:
        text += " ⚠️↓"
    return text


def render_trajectory(
    previous: dict[str, float],
    current: dict[str, float],
    *,
    round_labels: tuple[str, str] = ("R1", "R2"),
    threshold: float = DEGRADATION_THRESHOLD,
) -> str:
    """Render a Markdown table comparing two rounds of dimension scores.

    Dimensions union both inputs while preserving the previous-round order
    first. A dimension drops are flagged when ``previous - current >=
    threshold``. Returns an empty string when both inputs are empty so the
    caller can decide whether to write any file at all.
    """
    if not previous and not current:
        return ""

    dimensions: list[str] = []
    for key in previous:
        if key not in dimensions:
            dimensions.append(key)
    for key in current:
        if key not in dimensions:
            dimensions.append(key)

    header = ["Round", *dimensions]
    separator = ["---"] * len(header)

    prev_row = [round_labels[0]]
    prev_row.extend(_format_cell(previous.get(dim)) for dim in dimensions)

    cur_row = [round_labels[1]]
    for dim in dimensions:
        cur = current.get(dim)
        prev = previous.get(dim)
        degraded = cur is not None and prev is not None and (prev - cur) >= threshold
        cur_row.append(_format_cell(cur, mark_degrade=degraded))

    rows = [header, separator, prev_row, cur_row]
    return "\n".join("| " + " | ".join(row) + " |" for row in rows) + "\n"


def write_trajectory(
    previous_path: Path,
    current_path: Path,
    output_path: Path,
    *,
    threshold: float = DEGRADATION_THRESHOLD,
    round_labels: tuple[str, str] = ("R1", "R2"),
) -> str:
    """Compute and write a trajectory Markdown file.

    Returns the rendered document text, or an empty string when neither
    bundle exposes ``round_scores`` (in which case nothing is written).
    """
    _, prev_scores = load_bundle(previous_path)
    _, cur_scores = load_bundle(current_path)

    prev_norm = normalize_scores(prev_scores)
    cur_norm = normalize_scores(cur_scores)

    table = render_trajectory(prev_norm, cur_norm, round_labels=round_labels, threshold=threshold)
    if not table:
        return ""

    body = (
        "# Revision Score Trajectory\n\n"
        f"Per-dimension drop >= {threshold:g} is flagged with `⚠️↓`.\n\n" + table
    )
    output_path.write_text(body, encoding="utf-8")
    return body


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render revision trajectory comparing previous and current scores",
    )
    parser.add_argument(
        "previous",
        help="Path to old final_issues.json (legacy list or dict with round_scores)",
    )
    parser.add_argument(
        "current",
        help="Path to new final_issues.json (legacy list or dict with round_scores)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output Markdown path (defaults to <current dir>/revision_trajectory.md)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEGRADATION_THRESHOLD,
        help="Per-dimension drop that triggers a ⚠️↓ marker (default: %(default)s)",
    )
    args = parser.parse_args()

    previous_path = Path(args.previous).resolve()
    current_path = Path(args.current).resolve()
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        workspace_root = _infer_workspace_root(current_path)
        if workspace_root is not None:
            output_path = WorkspaceLayout(workspace_root).revision_trajectory
        else:
            output_path = current_path.parent / "revision_trajectory.md"

    body = write_trajectory(
        previous_path,
        current_path,
        output_path,
        threshold=args.threshold,
    )
    if not body:
        print("[trajectory] skipped: no round_scores in either bundle")
        return 0

    print(f"Revision trajectory written to {output_path}")
    return 0


def _infer_workspace_root(final_issues_path: Path) -> Path | None:
    """Walk up from a final_issues.json path to the workspace root, or None."""
    candidate = final_issues_path.parent
    for _ in range(5):
        layout = WorkspaceLayout(candidate)
        if layout.final_issues.resolve() == final_issues_path.resolve():
            return candidate
        candidate = candidate.parent
    return None


if __name__ == "__main__":
    raise SystemExit(main())
