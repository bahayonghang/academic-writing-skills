"""Print the next pending Elsevier inventory item as JSON."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ELS_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = ELS_ROOT / "corpus" / "inventory.json"

VENUE_ORDER = [
    "Journal of Process Control",
    "Expert Systems with Applications",
    "Engineering Applications of Artificial Intelligence",
    "Applied Energy",
    "Advanced Engineering Informatics",
    "Energy",
    "Chemical Engineering Science",
    "Control Engineering Practice",
    "ISA Transactions",
    "Computers & Chemical Engineering",
]

DATE_YMD = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
DATE_YEAR = re.compile(r"(\d{4})")


def venue_bucket(item: dict[str, Any]) -> int:
    venue = (item.get("venue") or "").strip()
    try:
        return VENUE_ORDER.index(venue) + 1
    except ValueError:
        return 99


def date_num(raw: Any) -> int:
    text = str(raw or "")
    match = DATE_YMD.search(text)
    if match:
        return int(match.group(1)) * 10000 + int(match.group(2)) * 100 + int(match.group(3))
    match = DATE_YEAR.search(text)
    if match:
        return int(match.group(1)) * 10000
    return 0


def sort_key(item: dict[str, Any]) -> tuple[int, int, int, str]:
    return (
        venue_bucket(item),
        0 if item.get("has_pdf") else 1,
        -date_num(item.get("date")),
        str(item.get("key") or ""),
    )


def main() -> int:
    payload = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    pending = [item for item in payload.get("items", []) if item.get("status") == "pending"]
    if not pending:
        json.dump({"error": "no pending items"}, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1
    item = sorted(pending, key=sort_key)[0]
    json.dump(
        {
            "key": item.get("key"),
            "venue": item.get("venue"),
            "has_pdf": item.get("has_pdf"),
            "type": item.get("type"),
            "doi": item.get("doi"),
            "title": item.get("title"),
        },
        sys.stdout,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
