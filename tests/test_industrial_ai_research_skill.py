"""Smoke tests for the industrial-ai-research skill package."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "academic-writing-skills" / "industrial-ai-research"

REQUIRED_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "references" / "venue-map.md",
    SKILL_DIR / "references" / "source-priority.md",
    SKILL_DIR / "references" / "report-modes.md",
    SKILL_DIR / "references" / "question-flow.md",
    SKILL_DIR / "references" / "quality-checklist.md",
    SKILL_DIR / "evals" / "evals.json",
    SKILL_DIR / "examples" / "predictive-maintenance.md",
    SKILL_DIR / "examples" / "intelligent-scheduling.md",
    SKILL_DIR / "examples" / "industrial-anomaly-detection.md",
]

CJK_RE = re.compile(r"[\u3400-\u9fff\u3040-\u30ff\uac00-\ud7af]")


def test_required_files_exist() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    assert not missing, f"Missing industrial-ai-research files: {missing}"


def test_skill_package_contains_no_cjk() -> None:
    for path in SKILL_DIR.rglob("*"):
        if path.is_dir():
            continue
        text = path.read_text(encoding="utf-8")
        assert not CJK_RE.search(text), f"CJK text found in {path}"


def test_skill_prompts_for_report_language() -> None:
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    question_flow = (SKILL_DIR / "references" / "question-flow.md").read_text(encoding="utf-8")
    assert "report language" in skill_text.lower()
    assert "which report language should i use" in question_flow.lower()


def test_source_priority_mentions_industrial_ai_defaults_and_tiers() -> None:
    source_priority = (SKILL_DIR / "references" / "source-priority.md").read_text(encoding="utf-8")
    venue_map = (SKILL_DIR / "references" / "venue-map.md").read_text(encoding="utf-8")
    combined = f"{source_priority}\n{venue_map}".lower()
    assert "industrial ai" in combined
    assert "tier 1" in combined
    assert "t-ase" in combined
    assert "case" in combined
    assert "eess.sy" in combined
