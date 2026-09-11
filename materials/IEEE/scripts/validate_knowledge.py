"""Validate IEEE knowledge-pack TSV headers and inventory alignment."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

IEEE_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = IEEE_ROOT / "corpus" / "inventory.json"
OBSERVATIONS_DIR = IEEE_ROOT / "observations"
KNOWLEDGE_DIR = IEEE_ROOT / "knowledge"
EXPECTED_COUNT = 353

TSV_HEADERS: dict[str, str] = {
    "writing_rules.tsv": (
        "rule_id\tcategory\tdescription\tpaper_count\tseverity_votes\tseverity"
        "\texemplar_quote\tprimary_section\tevidence\tprior_row\ttop_papers\tstatus"
    ),
    "phrase_bank.tsv": (
        "phrase_id\tslot\tphrase\tpaper_count\tusage_note\tevidence\tprior_row\ttop_papers\tstatus"
    ),
    "opener_distribution.tsv": "section\topener_3gram\ttotal_occurrences\tpaper_count\ttop_papers",
    "gap_transitions.tsv": (
        "section\tpivot_word\ttemplate\toccurrences\tpaper_count\ttop_papers\texemplar_quotes"
    ),
    "hedge_verbs.tsv": "verb\ttier\ttotal_occurrences\tpaper_count\ttop_papers\texemplar_quotes",
    "cross_section_linkers.tsv": (
        "from_section\tto_section\tpattern\toccurrences\tpaper_count\ttop_papers\texemplar_quotes"
    ),
    "section_openers.tsv": "section\topener_template\ttotal_occurrences\tpaper_count\ttop_papers",
    "paper_story_patterns.tsv": (
        "pattern_id\tname\tsection_sequence\tieee_variant\tpaper_count\tnote"
    ),
    "domain_register.tsv": "domain\tpaper_count\tsecondary_paper_count\tevidence",
    "anti_ai_patterns.tsv": (
        "pattern_id\tbanned_phrase\twhy\tsmell_severity\tpaper_count"
        "\tadversarial_count\tevidence\tpapers"
    ),
    "cross_section_rules.tsv": (
        "rule_id\tcategory\tdescription\tpaper_count\tseverity\tevidence"
        "\tprior_row\ttop_papers\tstatus"
    ),
}

NATURE_FORBIDDEN = ("methods-last", "methods last", "extended data")


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _int_field(row: dict[str, str], name: str) -> int | None:
    raw = (row.get(name) or "").strip()
    if raw == "":
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _nature_forced_template(row: dict[str, str]) -> bool:
    description = (row.get("description") or "").lower()
    primary = (row.get("primary_section") or "").lower()
    blob = f"{description} {(row.get('exemplar_quote') or '').lower()}"
    if any(token in blob for token in NATURE_FORBIDDEN):
        return True
    return "here we" in description and (primary == "abstract" or "abstract" in description)


def validate(allow_pending: bool) -> list[str]:
    errors: list[str] = []

    for name, expected in TSV_HEADERS.items():
        path = KNOWLEDGE_DIR / name
        if not path.is_file():
            errors.append(f"missing TSV {name}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            errors.append(f"empty TSV {name}")
            continue
        if lines[0] != expected:
            errors.append(f"header mismatch {name}")

    if not INVENTORY_PATH.is_file():
        errors.append("missing corpus/inventory.json")
        return errors

    payload = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    items: list[dict[str, Any]] = payload.get("items") or []
    count = payload.get("count")
    if count != EXPECTED_COUNT:
        errors.append(f"inventory count {count} != {EXPECTED_COUNT}")
    if len(items) != EXPECTED_COUNT:
        errors.append(f"inventory items {len(items)} != {EXPECTED_COUNT}")

    keys = [str(item.get("key") or "") for item in items]
    if any(not key for key in keys):
        errors.append("inventory item missing key")
    if len(set(keys)) != len(keys):
        errors.append("duplicate inventory keys")

    obs_files = {
        path.stem: path for path in OBSERVATIONS_DIR.glob("*.md") if path.name != "_schema.md"
    }
    inventory_keys = set(keys)
    orphans = sorted(stem for stem in obs_files if stem not in inventory_keys)
    if orphans:
        errors.append(f"observation files not in inventory: {', '.join(orphans[:8])}")

    status_counts = {"pending": 0, "complete": 0, "degraded": 0}
    for item in items:
        key = str(item.get("key") or "")
        status = item.get("status")
        observation = item.get("observation")
        if status not in status_counts:
            errors.append(f"{key}: invalid status {status!r}")
            continue
        status_counts[status] += 1
        expected_obs = f"observations/{key}.md"
        if status in ("complete", "degraded"):
            if key not in obs_files:
                errors.append(f"{key}: status={status} but observation file missing")
            if observation != expected_obs:
                errors.append(f"{key}: observation path {observation!r} != {expected_obs!r}")
        elif status == "pending":
            if observation not in (None, ""):
                errors.append(f"{key}: pending but observation={observation!r}")
            if not allow_pending and key in obs_files:
                errors.append(f"{key}: pending but observation file exists")

    if allow_pending:
        extra_pending_files = [
            key
            for key, item in ((str(i.get("key") or ""), i) for i in items)
            if item.get("status") == "pending" and key in obs_files
        ]
        if extra_pending_files:
            errors.append(
                "pending keys have observation files: " + ", ".join(extra_pending_files[:8])
            )
    else:
        missing = sorted(inventory_keys - set(obs_files))
        if missing:
            errors.append(f"missing observation files: {len(missing)}")
        if len(obs_files) != EXPECTED_COUNT:
            errors.append(f"observation files {len(obs_files)} != {EXPECTED_COUNT}")
        if status_counts["pending"] != 0:
            errors.append(
                f"pending={status_counts['pending']} (expected 0 without --allow-pending)"
            )
        done = status_counts["complete"] + status_counts["degraded"]
        if done != EXPECTED_COUNT:
            errors.append(f"complete+degraded={done} != {EXPECTED_COUNT}")

    writing_rules_path = KNOWLEDGE_DIR / "writing_rules.tsv"
    phrase_bank_path = KNOWLEDGE_DIR / "phrase_bank.tsv"
    core_rules = 0
    core_phrases = 0
    if writing_rules_path.is_file():
        for row in _read_tsv(writing_rules_path):
            if (row.get("status") or "").strip() != "core":
                continue
            core_rules += 1
            paper_count = _int_field(row, "paper_count")
            if paper_count is None or paper_count < 3:
                errors.append(
                    f"core writing_rules {(row.get('rule_id') or '?')} paper_count={paper_count}"
                )
            if _nature_forced_template(row):
                errors.append(
                    "core writing_rules "
                    f"{(row.get('rule_id') or '?')} contains Nature-forced template"
                )
    if phrase_bank_path.is_file():
        for row in _read_tsv(phrase_bank_path):
            if (row.get("status") or "").strip() != "core":
                continue
            core_phrases += 1
            paper_count = _int_field(row, "paper_count")
            if paper_count is None or paper_count < 3:
                errors.append(
                    f"core phrase_bank {(row.get('phrase_id') or '?')} paper_count={paper_count}"
                )

    print(
        "inventory={count} observations={obs} pending={pending} "
        "complete={complete} degraded={degraded} core_rules={rules} core_phrases={phrases}".format(
            count=len(items),
            obs=len(obs_files),
            pending=status_counts["pending"],
            complete=status_counts["complete"],
            degraded=status_counts["degraded"],
            rules=core_rules,
            phrases=core_phrases,
        )
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate IEEE knowledge pack")
    parser.add_argument(
        "--allow-pending",
        action="store_true",
        help="allow inventory keys without observation files",
    )
    args = parser.parse_args()
    errors = validate(allow_pending=args.allow_pending)
    if errors:
        print("FAIL")
        for err in errors:
            print(err)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
