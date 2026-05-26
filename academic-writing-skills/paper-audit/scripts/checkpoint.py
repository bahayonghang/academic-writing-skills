"""Checkpoint protocol for deep-review long-running tasks.

Stores per-workspace progress in ``<review_dir>/checkpoint.json`` so an
interrupted deep-review session can resume from the last successful lane
instead of restarting from scratch. The protocol is intentionally narrow:
this module owns the schema, atomic read/write helpers, and the small set
of mutators that the prepare / audit / lane / consolidate scripts need.

Status lifecycle: ``prepared`` -> ``in_progress`` -> ``suspended`` -> ``completed``.
A ``suspended`` checkpoint is the signal that a resume is in flight; an
explicit ``--no-resume`` invocation calls :func:`reset_checkpoint` to clear
state without removing other workspace artifacts.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from paths import WorkspaceLayout

CHECKPOINT_FILENAME = "checkpoint.json"
CHECKPOINT_VERSION = 1

DEFAULT_PHASES: tuple[str, ...] = (
    "prepare",
    "phase0_audit",
    "committee",
    "lanes",
    "consolidation",
    "present",
)
"""Canonical Phase 1-5 names from `references/MODE_GUIDE.md`.

Mapping (1:1 with MODE_GUIDE deep-review phases):
- prepare       -> Phase 1: prepare workspace
- phase0_audit  -> Phase 2: Phase 0 automated audit
- committee     -> Phase 3A: Academic Pre-Review Committee
- lanes         -> Phase 3B: section / cross-cutting lanes
- consolidation -> Phase 4: consolidate + verify quotes + render report
- present       -> Phase 5: present result
"""

VALID_STATUSES = frozenset({"prepared", "in_progress", "suspended", "completed"})


def _now() -> str:
    return datetime.now().isoformat()


def _checkpoint_path(review_dir: Path | str) -> Path:
    return WorkspaceLayout(review_dir).checkpoint


def init_checkpoint(
    review_dir: Path | str,
    *,
    phases: tuple[str, ...] = DEFAULT_PHASES,
    generated_files: list[str] | None = None,
) -> dict:
    """Create a fresh checkpoint for ``review_dir`` and persist it.

    Overwrites any existing checkpoint so a re-prepared workspace always
    starts from a clean state. The ``prepare`` phase is auto-marked
    completed because :func:`init_checkpoint` is called as the last step of
    workspace preparation.
    """
    now = _now()
    payload: dict[str, Any] = {
        "version": CHECKPOINT_VERSION,
        "status": "prepared",
        "phase_index": 1,  # next phase to execute is phase0_audit
        "phases": [
            {"name": name, "status": "completed" if name == "prepare" else "pending"}
            for name in phases
        ],
        "completed_lanes": [],
        "suspended_lanes": [],
        "generated_files": sorted(set(generated_files or [])),
        "created_at": now,
        "updated_at": now,
    }
    save_checkpoint(review_dir, payload)
    return payload


def load_checkpoint(review_dir: Path | str) -> dict | None:
    """Return the checkpoint dict, or ``None`` if no checkpoint exists."""
    path = _checkpoint_path(review_dir)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_checkpoint(review_dir: Path | str, payload: dict) -> None:
    """Persist a checkpoint payload, refreshing ``updated_at``."""
    payload = dict(payload)
    payload["updated_at"] = _now()
    path = _checkpoint_path(review_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _require_checkpoint(review_dir: Path | str) -> dict:
    checkpoint = load_checkpoint(review_dir)
    if checkpoint is None:
        raise FileNotFoundError(
            f"No checkpoint at {_checkpoint_path(review_dir)} — "
            "run prepare_review_workspace.py first."
        )
    return checkpoint


def mark_phase(review_dir: Path | str, phase: str, status: str) -> dict:
    """Update the status of a named phase in the checkpoint."""
    checkpoint = _require_checkpoint(review_dir)
    for entry in checkpoint["phases"]:
        if entry["name"] == phase:
            entry["status"] = status
            break
    else:
        raise ValueError(f"Unknown phase: {phase}")
    checkpoint["phase_index"] = next(
        (
            index
            for index, entry in enumerate(checkpoint["phases"])
            if entry["status"] != "completed"
        ),
        len(checkpoint["phases"]),
    )
    save_checkpoint(review_dir, checkpoint)
    return checkpoint


def mark_lane_completed(review_dir: Path | str, lane: str) -> dict:
    """Record that ``lane`` finished successfully and drop it from suspended."""
    checkpoint = _require_checkpoint(review_dir)
    if lane not in checkpoint["completed_lanes"]:
        checkpoint["completed_lanes"].append(lane)
    if lane in checkpoint["suspended_lanes"]:
        checkpoint["suspended_lanes"].remove(lane)
    save_checkpoint(review_dir, checkpoint)
    return checkpoint


def mark_lane_suspended(review_dir: Path | str, lane: str) -> dict:
    """Record that ``lane`` is in flight but did not complete this session."""
    checkpoint = _require_checkpoint(review_dir)
    if lane in checkpoint["completed_lanes"]:
        # already done — nothing to suspend
        return checkpoint
    if lane not in checkpoint["suspended_lanes"]:
        checkpoint["suspended_lanes"].append(lane)
    if checkpoint["status"] != "completed":
        checkpoint["status"] = "suspended"
    save_checkpoint(review_dir, checkpoint)
    return checkpoint


def register_generated_file(review_dir: Path | str, file_name: str) -> dict:
    """Record a newly written artifact in ``generated_files`` (idempotent)."""
    checkpoint = _require_checkpoint(review_dir)
    if file_name not in checkpoint["generated_files"]:
        checkpoint["generated_files"].append(file_name)
        checkpoint["generated_files"].sort()
        save_checkpoint(review_dir, checkpoint)
    return checkpoint


def set_status(review_dir: Path | str, status: str) -> dict:
    """Update top-level checkpoint status with validation."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}; expected one of {sorted(VALID_STATUSES)}")
    checkpoint = _require_checkpoint(review_dir)
    checkpoint["status"] = status
    save_checkpoint(review_dir, checkpoint)
    return checkpoint


def reset_checkpoint(review_dir: Path | str) -> dict:
    """Restore an in-place checkpoint to its initial prepared state.

    Used by the ``--no-resume`` flag: the workspace and its artifacts are
    preserved, but the checkpoint forgets prior progress so the next
    deep-review run executes every phase / lane again.
    """
    checkpoint = load_checkpoint(review_dir)
    generated_files = checkpoint.get("generated_files", []) if checkpoint else []
    return init_checkpoint(review_dir, generated_files=generated_files)


def summarize_checkpoint(checkpoint: dict) -> str:
    """Return a single-line human summary for CLI display."""
    completed = len(checkpoint.get("completed_lanes", []))
    suspended = len(checkpoint.get("suspended_lanes", []))
    status = checkpoint.get("status", "unknown")
    phase_index = checkpoint.get("phase_index", 0)
    return (
        f"[checkpoint] status={status} phase_index={phase_index} "
        f"lanes_completed={completed} lanes_suspended={suspended}"
    )
