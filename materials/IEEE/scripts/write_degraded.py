"""Write degraded observations for pending items that have no PDF."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import date
from pathlib import Path

IEEE_ROOT = Path(__file__).resolve().parent.parent
INVENTORY = IEEE_ROOT / "corpus" / "inventory.json"
NOPF = IEEE_ROOT / "corpus" / "pending-nopf.json"
OBS_DIR = IEEE_ROOT / "observations"
DB = Path(r"C:\Users\lyh\Zotero\zotero.sqlite")

TODAY = date.today().isoformat()
ZH_ABS = re.compile(r"【摘要翻译】.*", re.S)


def abstracts_by_key() -> dict[str, str]:
    uri = DB.resolve().as_uri() + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    rows = con.execute(
        """
        SELECT items.key, itemDataValues.value
        FROM items
        JOIN itemData ON items.itemID = itemData.itemID
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        LEFT JOIN deletedItems ON items.itemID = deletedItems.itemID
        WHERE deletedItems.itemID IS NULL
          AND fields.fieldName = 'abstractNote'
        """
    ).fetchall()
    con.close()
    return {key: value or "" for key, value in rows}


def english_abstract(raw: str) -> str:
    text = ZH_ABS.sub("", raw or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def first_sentence(text: str) -> str:
    match = re.search(r"(.+?[.!?])(?:\s|$)", text)
    if match:
        return match.group(1).strip()
    return text[:240].strip()


def opener_3gram(sentence: str) -> str:
    words = re.findall(r"[A-Za-z0-9\-']+", sentence)
    return " ".join(words[:3]) if words else ""


def observation_md(item: dict, abstract: str) -> str:
    key = item["key"]
    title = item.get("title") or ""
    venue = item.get("venue") or "early-access"
    doi = item.get("doi") or ""
    item_type = item.get("type") or "journalArticle"
    lead = first_sentence(abstract)
    gram = opener_3gram(lead)
    quotes = []
    if lead:
        quotes.append(f"- abstract: {lead}")
    propose = re.search(
        r"((?:To address[^.]*?[,.] )?(?:this article |we )?(?:propose|presents?|introduces?|develop)[^.]*\.)",
        abstract,
        re.I,
    )
    if propose:
        quotes.append(f"- method-claim: {propose.group(1).strip()}")
    return f"""---
key: {key}
title: {json.dumps(title, ensure_ascii=False)}
venue: {json.dumps(venue, ensure_ascii=False)}
doi: {json.dumps(doi, ensure_ascii=False)}
item_type: {item_type}
has_pdf: false
status: degraded
pages_read: ""
date_observed: {TODAY}
story_pattern: pending
---

## Structure

无 PDF。仅题录与 Zotero `abstractNote`（去掉中文翻译块）。章节结构未知。

## Openers

- abstract: `{gram}` — {json.dumps(lead, ensure_ascii=False) if lead else "（摘要为空）"}

## Gap transitions

摘要级缺口句见 Quotes。未核正文。

## Hedge verbs

见摘要原句；未核章节。

## Cross-section linkers

无正文，未观察。

## Candidate rules

无。degraded 不晋升 core。

## Candidate phrases

无。需 PDF 后再计。

## House style

以摘要自称句为准，未核全文。

## Quotes

{chr(10).join(quotes) if quotes else "- （无英文摘要）"}
"""


def main() -> None:
    items = json.loads(NOPF.read_text(encoding="utf-8"))
    abs_map = abstracts_by_key()
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    by_key = {item["key"]: item for item in inventory["items"]}
    written = 0
    empty = 0
    for item in items:
        key = item["key"]
        abstract = english_abstract(abs_map.get(key, ""))
        if not abstract:
            empty += 1
        path = OBS_DIR / f"{key}.md"
        path.write_text(observation_md(item, abstract), encoding="utf-8")
        inv = by_key[key]
        inv["status"] = "degraded"
        inv["observation"] = f"observations/{key}.md"
        written += 1
    INVENTORY.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"degraded_written={written} empty_abstract={empty}")


if __name__ == "__main__":
    main()
