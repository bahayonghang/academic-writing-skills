"""Split pending inventory into PDF vs no-PDF lists."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

IEEE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(IEEE_ROOT / "scripts"))
from next_pending import sort_key  # noqa: E402

INVENTORY = IEEE_ROOT / "corpus" / "inventory.json"
OUT_DIR = IEEE_ROOT / "corpus"


def main() -> int:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    pending = [item for item in payload.get("items", []) if item.get("status") == "pending"]
    pending.sort(key=sort_key)
    pdf = [item for item in pending if item.get("has_pdf")]
    nopf = [item for item in pending if not item.get("has_pdf")]
    by_venue = Counter((item.get("venue") or "(no venue)") for item in pending)
    print(f"pending={len(pending)} pdf={len(pdf)} nopf={len(nopf)}")
    print("venues:")
    for name, n in by_venue.most_common(20):
        print(f"  {n:4d}  {name}")
    (OUT_DIR / "pending-pdf.json").write_text(
        json.dumps(pdf, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "pending-nopf.json").write_text(
        json.dumps(nopf, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
