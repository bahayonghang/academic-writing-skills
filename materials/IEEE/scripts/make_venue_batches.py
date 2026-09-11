"""Split remaining PDF pending items (non-TII) into batch JSON files."""

from __future__ import annotations

import json
from pathlib import Path

IEEE_ROOT = Path(__file__).resolve().parent.parent
PDF = IEEE_ROOT / "corpus" / "pending-pdf.json"
OUT = IEEE_ROOT / "corpus" / "batches"
TII = "IEEE Transactions on Industrial Informatics"
SIZE = 8


def main() -> None:
    items = json.loads(PDF.read_text(encoding="utf-8"))
    rest = [i["key"] for i in items if i.get("venue") != TII]
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for start in range(0, len(rest), SIZE):
        n += 1
        chunk = rest[start : start + SIZE]
        (OUT / f"rest-{n:02d}.json").write_text(
            json.dumps(chunk, ensure_ascii=False), encoding="utf-8"
        )
    print(f"rest_keys={len(rest)} batches={n} size={SIZE}")


if __name__ == "__main__":
    main()
