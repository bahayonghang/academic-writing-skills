"""Diff two deep-review issue bundles for re-audit style comparisons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from paths import WorkspaceLayout
from render_revision_trajectory import write_trajectory


def load_issues(path: Path) -> list[dict]:
    """Load issue list from a final_issues.json file.

    Accepts either a top-level list (legacy schema) or a dict containing
    an ``issues`` key (extended schema with ``round_scores``).
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("issues", []) or []


def diff_issues(previous: list[dict], current: list[dict]) -> dict:
    """Compare previous and current issue bundles by root cause key."""
    current_by_key = {issue.get("root_cause_key", issue.get("title")): issue for issue in current}
    previous_by_key = {issue.get("root_cause_key", issue.get("title")): issue for issue in previous}
    statuses: list[dict] = []

    for key, old_issue in previous_by_key.items():
        new_issue = current_by_key.get(key)
        if new_issue is None:
            status = "FULLY_ADDRESSED"
        elif old_issue.get("severity") == new_issue.get("severity"):
            status = "NOT_ADDRESSED"
        else:
            status = "PARTIALLY_ADDRESSED"

        statuses.append(
            {
                "root_cause_key": key,
                "title": old_issue.get("title"),
                "previous_severity": old_issue.get("severity"),
                "current_severity": new_issue.get("severity") if new_issue else None,
                "status": status,
            }
        )

    new_items = [issue for key, issue in current_by_key.items() if key not in previous_by_key]
    return {"statuses": statuses, "new_issues": new_items}


def main() -> int:
    parser = argparse.ArgumentParser(description="Diff two deep-review issue bundle files")
    parser.add_argument("previous", help="Path to old final_issues.json")
    parser.add_argument("current", help="Path to new final_issues.json")
    parser.add_argument(
        "--trajectory-output",
        default=None,
        help="Optional path for revision_trajectory.md (defaults next to <current>).",
    )
    parser.add_argument(
        "--no-trajectory",
        action="store_true",
        help="Skip writing revision_trajectory.md even when round_scores are present.",
    )
    args = parser.parse_args()

    previous_path = Path(args.previous)
    current_path = Path(args.current)

    diff = diff_issues(load_issues(previous_path), load_issues(current_path))
    print(json.dumps(diff, indent=2, ensure_ascii=False))

    if not args.no_trajectory:
        if args.trajectory_output:
            trajectory_path = Path(args.trajectory_output).resolve()
        else:
            # current_path may be `<workspace>/artifacts/data/final_issues.json`
            # so map to <workspace>/artifacts/data/revision_trajectory.md when possible.
            resolved_current = current_path.resolve()
            workspace_root = _infer_workspace_root(resolved_current)
            if workspace_root is not None:
                trajectory_path = WorkspaceLayout(workspace_root).revision_trajectory
            else:
                trajectory_path = resolved_current.parent / "revision_trajectory.md"
        body = write_trajectory(
            previous_path.resolve(),
            current_path.resolve(),
            trajectory_path,
        )
        if body:
            print(f"[trajectory] wrote {trajectory_path}")

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
