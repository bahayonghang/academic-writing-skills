"""Contract test for ``evals/trigger_eval.json`` corpus across all skills.

The trigger-eval corpus is the input to ``skill-creator``'s ``run_loop.py``,
which iteratively optimizes each skill's frontmatter description by measuring
trigger precision / recall on this corpus. Running ``run_loop.py`` requires an
``ANTHROPIC_API_KEY`` and consumes API tokens, so it is not part of ``just
ci`` — but the corpus itself must stay healthy so the optimization is
reproducible whenever the maintainer chooses to run it.

Schema (keep in sync with skill-creator/scripts/run_loop.py):

```json
{
  "skill_name": "<matches SKILL.md frontmatter name>",
  "queries": [
    {
      "query": "user-facing prompt text",
      "should_trigger": true,
      "category": "core | edge | negative-overlap-* | negative-unrelated"
    }
  ]
}
```

Health rules enforced here:

* one ``trigger_eval.json`` per shipped skill (five total)
* ``skill_name`` matches both the directory name and the SKILL.md frontmatter
* ``queries`` has at least 12 items, at least 5 positives, at least 5 negatives
* every entry has the three required fields with the right types
* every entry's ``query`` is unique within the skill
* every entry's ``category`` is a non-empty string

Optional invocation hint (NOT run in CI):

```bash
ANTHROPIC_API_KEY=... uv run python \\
  ~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator/scripts/run_loop.py \\
  --eval-set academic-writing-skills/<skill>/evals/trigger_eval.json \\
  --skill-path academic-writing-skills/<skill> \\
  --model claude-sonnet-4-6 --verbose
```
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SKILLS_ROOT = REPO_ROOT / "academic-writing-skills"

SKILL_NAMES = (
    "latex-paper-en",
    "latex-thesis-zh",
    "typst-paper",
    "bib-search-citation",
    "paper-audit",
    "cover-letter",
)

MIN_QUERIES = 12
MIN_POSITIVES = 5
MIN_NEGATIVES = 5
REQUIRED_FIELDS = ("query", "should_trigger", "category")


def _trigger_eval_path(skill_name: str) -> Path:
    return SKILLS_ROOT / skill_name / "evals" / "trigger_eval.json"


def _frontmatter_name(skill_md_path: Path) -> str:
    text = skill_md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match, f"{skill_md_path}: missing YAML frontmatter"
    fm = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    assert name_match, f"{skill_md_path}: missing 'name' field in frontmatter"
    return name_match.group(1).strip().strip("\"'")


@pytest.fixture(scope="module")
def trigger_evals() -> dict[str, dict]:
    return {
        name: json.loads(_trigger_eval_path(name).read_text(encoding="utf-8"))
        for name in SKILL_NAMES
    }


@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_trigger_eval_file_exists(skill_name: str) -> None:
    path = _trigger_eval_path(skill_name)
    assert path.exists(), (
        f"{skill_name}: missing evals/trigger_eval.json — required for "
        "skill-creator run_loop.py optimization"
    )


@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_trigger_eval_skill_name_matches_directory_and_frontmatter(
    skill_name: str, trigger_evals: dict[str, dict]
) -> None:
    payload = trigger_evals[skill_name]
    assert payload.get("skill_name") == skill_name, (
        f"{skill_name}: trigger_eval.json skill_name "
        f"{payload.get('skill_name')!r} does not match directory"
    )
    fm_name = _frontmatter_name(SKILLS_ROOT / skill_name / "SKILL.md")
    assert payload["skill_name"] == fm_name, (
        f"{skill_name}: trigger_eval.json skill_name {payload['skill_name']!r} "
        f"does not match SKILL.md frontmatter name {fm_name!r}"
    )


@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_trigger_eval_corpus_size_and_balance(
    skill_name: str, trigger_evals: dict[str, dict]
) -> None:
    queries = trigger_evals[skill_name]["queries"]
    assert len(queries) >= MIN_QUERIES, (
        f"{skill_name}: only {len(queries)} queries; need at least {MIN_QUERIES} "
        "for stable train/test split (skill-creator default holdout=0.4)"
    )
    positives = [q for q in queries if q["should_trigger"]]
    negatives = [q for q in queries if not q["should_trigger"]]
    assert len(positives) >= MIN_POSITIVES, (
        f"{skill_name}: only {len(positives)} positive queries; need at least "
        f"{MIN_POSITIVES} so train/test split keeps positives in both halves"
    )
    assert len(negatives) >= MIN_NEGATIVES, (
        f"{skill_name}: only {len(negatives)} negative queries; need at least "
        f"{MIN_NEGATIVES} so precision is meaningfully measurable"
    )


@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_trigger_eval_entries_have_required_fields(
    skill_name: str, trigger_evals: dict[str, dict]
) -> None:
    queries = trigger_evals[skill_name]["queries"]
    for idx, entry in enumerate(queries):
        missing = [f for f in REQUIRED_FIELDS if f not in entry]
        assert not missing, f"{skill_name}[{idx}]: missing fields {missing}"
        assert isinstance(entry["query"], str) and entry["query"].strip(), (
            f"{skill_name}[{idx}]: query must be a non-empty string"
        )
        assert isinstance(entry["should_trigger"], bool), (
            f"{skill_name}[{idx}]: should_trigger must be a bool, got "
            f"{type(entry['should_trigger']).__name__}"
        )
        assert isinstance(entry["category"], str) and entry["category"].strip(), (
            f"{skill_name}[{idx}]: category must be a non-empty string"
        )


@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_trigger_eval_queries_are_unique_within_skill(
    skill_name: str, trigger_evals: dict[str, dict]
) -> None:
    queries = [q["query"] for q in trigger_evals[skill_name]["queries"]]
    seen: dict[str, int] = {}
    for q in queries:
        seen[q] = seen.get(q, 0) + 1
    duplicates = {q: c for q, c in seen.items() if c > 1}
    assert not duplicates, (
        f"{skill_name}: duplicate queries detected — each prompt must be "
        f"distinct so trigger rates are well-defined: {duplicates}"
    )
