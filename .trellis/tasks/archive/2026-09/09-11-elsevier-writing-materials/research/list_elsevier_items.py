"""Read-only inventory of domain Elsevier items from local Zotero."""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

DB = Path(r"C:\Users\lyh\Zotero\zotero.sqlite")
OUT = Path(__file__).with_name("elsevier-inventory.json")

ALLOWLIST = (
    "Expert Systems with Applications",
    "Journal of Process Control",
    "Engineering Applications of Artificial Intelligence",
    "Applied Energy",
    "Advanced Engineering Informatics",
    "Energy",
    "Chemical Engineering Science",
    "Control Engineering Practice",
    "ISA Transactions",
    "Computers & Chemical Engineering",
    "Computers and Chemical Engineering",
)

SQL = r"""
WITH field_map AS (
    SELECT fieldID, fieldName FROM fields
),
item_fields AS (
    SELECT
        items.itemID,
        items.key,
        itemTypes.typeName,
        MAX(CASE WHEN field_map.fieldName = 'title' THEN itemDataValues.value END) AS title,
        MAX(CASE WHEN field_map.fieldName = 'publicationTitle' THEN itemDataValues.value END) AS publicationTitle,
        MAX(CASE WHEN field_map.fieldName = 'publisher' THEN itemDataValues.value END) AS publisher,
        MAX(CASE WHEN field_map.fieldName = 'DOI' THEN itemDataValues.value END) AS doi,
        MAX(CASE WHEN field_map.fieldName = 'url' THEN itemDataValues.value END) AS url,
        MAX(CASE WHEN field_map.fieldName = 'date' THEN itemDataValues.value END) AS date
    FROM items
    JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
    LEFT JOIN deletedItems ON items.itemID = deletedItems.itemID
    LEFT JOIN itemData ON items.itemID = itemData.itemID
    LEFT JOIN field_map ON itemData.fieldID = field_map.fieldID
    LEFT JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    WHERE deletedItems.itemID IS NULL
    AND items.itemTypeID NOT IN (
        SELECT itemTypeID FROM itemTypes WHERE typeName IN ('attachment', 'note', 'annotation')
    )
    GROUP BY items.itemID
),
pdf_items AS (
    SELECT DISTINCT parentItemID AS itemID
    FROM itemAttachments
    WHERE contentType = 'application/pdf'
)
SELECT
    item_fields.key,
    item_fields.typeName,
    item_fields.title,
    item_fields.publicationTitle,
    item_fields.publisher,
    item_fields.doi,
    item_fields.url,
    item_fields.date,
    CASE WHEN pdf_items.itemID IS NULL THEN 0 ELSE 1 END AS has_pdf
FROM item_fields
LEFT JOIN pdf_items ON item_fields.itemID = pdf_items.itemID
WHERE
    (
        IFNULL(item_fields.publisher, '') LIKE '%Elsevier%'
        OR IFNULL(item_fields.doi, '') LIKE '10.1016/%'
        OR LOWER(IFNULL(item_fields.url, '')) LIKE '%sciencedirect.com%'
        OR LOWER(IFNULL(item_fields.url, '')) LIKE '%elsevier.com%'
    )
"""


def normalize_venue(name: str) -> str:
    text = (name or "").strip()
    if text == "Computers and Chemical Engineering":
        return "Computers & Chemical Engineering"
    return text


def main() -> None:
    uri = DB.resolve().as_uri() + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(SQL).fetchall()]
    con.close()
    allow = {normalize_venue(name) for name in ALLOWLIST}
    selected = []
    for row in rows:
        venue = normalize_venue(row.get("publicationTitle") or "")
        if venue not in allow:
            continue
        row["venue"] = venue
        selected.append(row)
    by_venue = Counter(r["venue"] for r in selected)
    pdf_yes = sum(int(r["has_pdf"]) for r in selected)
    payload = {
        "count": len(selected),
        "pdf_count": pdf_yes,
        "by_venue": by_venue.most_common(),
        "items": [
            {
                "key": r["key"],
                "type": r["typeName"],
                "title": r["title"],
                "venue": r["venue"],
                "has_pdf": bool(r["has_pdf"]),
                "publisher": r["publisher"],
                "doi": r["doi"],
                "url": r["url"],
                "date": r["date"],
            }
            for r in selected
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"count={len(selected)} pdf_count={pdf_yes}")
    for name, n in by_venue.most_common():
        print(f"  {n:4d}  {name}")


if __name__ == "__main__":
    main()
