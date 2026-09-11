"""Read-only inventory of IEEE items from local Zotero SQLite."""

from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path

DB = Path(r"C:\Users\lyh\Zotero\zotero.sqlite")
OUT = Path(__file__).with_name("ieee-inventory.json")

IEEE_SQL = r"""
WITH field_map AS (
    SELECT fieldID, fieldName FROM fields
),
item_fields AS (
    SELECT
        items.itemID,
        items.key,
        itemTypes.typeName,
        items.dateAdded,
        items.dateModified,
        MAX(CASE WHEN field_map.fieldName = 'title' THEN itemDataValues.value END) AS title,
        MAX(CASE WHEN field_map.fieldName = 'publicationTitle' THEN itemDataValues.value END) AS publicationTitle,
        MAX(CASE WHEN field_map.fieldName = 'proceedingsTitle' THEN itemDataValues.value END) AS proceedingsTitle,
        MAX(CASE WHEN field_map.fieldName = 'conferenceName' THEN itemDataValues.value END) AS conferenceName,
        MAX(CASE WHEN field_map.fieldName = 'publisher' THEN itemDataValues.value END) AS publisher,
        MAX(CASE WHEN field_map.fieldName = 'journalAbbreviation' THEN itemDataValues.value END) AS journalAbbreviation,
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
    item_fields.proceedingsTitle,
    item_fields.conferenceName,
    item_fields.publisher,
    item_fields.journalAbbreviation,
    item_fields.doi,
    item_fields.url,
    item_fields.date,
    CASE WHEN pdf_items.itemID IS NULL THEN 0 ELSE 1 END AS has_pdf
FROM item_fields
LEFT JOIN pdf_items ON item_fields.itemID = pdf_items.itemID
WHERE
    IFNULL(item_fields.publicationTitle, '') LIKE '%IEEE%'
    OR IFNULL(item_fields.proceedingsTitle, '') LIKE '%IEEE%'
    OR IFNULL(item_fields.conferenceName, '') LIKE '%IEEE%'
    OR IFNULL(item_fields.publisher, '') LIKE '%IEEE%'
    OR IFNULL(item_fields.journalAbbreviation, '') LIKE '%IEEE%'
    OR IFNULL(item_fields.doi, '') LIKE '10.1109%'
    OR LOWER(IFNULL(item_fields.url, '')) LIKE '%ieeexplore.ieee.org%'
    OR LOWER(IFNULL(item_fields.url, '')) LIKE '%ieee.org%'
ORDER BY item_fields.typeName, item_fields.publicationTitle, item_fields.title
"""


def venue(row: dict) -> str:
    return (
        row.get("publicationTitle")
        or row.get("proceedingsTitle")
        or row.get("conferenceName")
        or row.get("publisher")
        or "(no venue)"
    )


def main() -> None:
    uri = DB.resolve().as_uri() + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(IEEE_SQL).fetchall()]
    con.close()

    def match_reasons(row: dict) -> list[str]:
        reasons: list[str] = []
        if "IEEE" in (row.get("publicationTitle") or ""):
            reasons.append("publicationTitle")
        if "IEEE" in (row.get("proceedingsTitle") or ""):
            reasons.append("proceedingsTitle")
        if "IEEE" in (row.get("conferenceName") or ""):
            reasons.append("conferenceName")
        if "IEEE" in (row.get("publisher") or ""):
            reasons.append("publisher")
        if "IEEE" in (row.get("journalAbbreviation") or ""):
            reasons.append("journalAbbreviation")
        doi = (row.get("doi") or "").lower()
        if doi.startswith("10.1109"):
            reasons.append("doi")
        url = (row.get("url") or "").lower()
        if "ieeexplore.ieee.org" in url:
            reasons.append("ieeexplore")
        elif "ieee.org" in url:
            reasons.append("ieee.org")
        return reasons

    by_type = Counter(r["typeName"] for r in rows)
    by_venue = Counter(venue(r) for r in rows)
    pdf_yes = sum(int(r["has_pdf"]) for r in rows)
    no_venue = [r for r in rows if venue(r) == "(no venue)"]
    payload = {
        "count": len(rows),
        "pdf_count": pdf_yes,
        "no_venue_count": len(no_venue),
        "by_type": dict(by_type),
        "top_venues": by_venue.most_common(40),
        "items": [
            {
                "key": r["key"],
                "type": r["typeName"],
                "title": r["title"],
                "venue": venue(r),
                "has_pdf": bool(r["has_pdf"]),
                "match_reasons": match_reasons(r),
                "publicationTitle": r["publicationTitle"],
                "proceedingsTitle": r["proceedingsTitle"],
                "conferenceName": r["conferenceName"],
                "publisher": r["publisher"],
                "journalAbbreviation": r["journalAbbreviation"],
                "doi": r["doi"],
                "url": r["url"],
                "date": r["date"],
            }
            for r in rows
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"count={len(rows)}")
    print(f"pdf_count={pdf_yes}")
    print(f"no_venue_count={len(no_venue)}")
    print("by_type=" + json.dumps(by_type, ensure_ascii=False))
    print("top_venues:")
    for name, n in by_venue.most_common(25):
        print(f"  {n:4d}  {name}")
    print("no_venue_samples:")
    for row in no_venue[:8]:
        print(
            f"  {row['key']}  {row['typeName']}  doi={row['doi']}  "
            f"url={row['url']}  title={row['title']}"
        )


if __name__ == "__main__":
    main()
