"""Set inventory status from observation files. Does not write TSV."""

from __future__ import annotations

import json
from pathlib import Path

ELS_ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ELS_ROOT / "corpus" / "inventory.json"
OBS_DIR = ELS_ROOT / "observations"


def main() -> None:
    payload = json.loads(INVENTORY.read_text(encoding="utf-8"))
    files = {path.stem: path for path in OBS_DIR.glob("*.md") if path.name != "_schema.md"}
    complete = degraded = pending = 0
    for item in payload["items"]:
        key = item["key"]
        path = files.get(key)
        if path is None:
            item["status"] = "pending"
            item["observation"] = None
            pending += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")[:800]
        if "status: degraded" in text or "status:degraded" in text:
            item["status"] = "degraded"
            degraded += 1
        else:
            item["status"] = "complete"
            complete += 1
        item["observation"] = f"observations/{key}.md"
    INVENTORY.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"complete={complete} degraded={degraded} pending={pending} files={len(files)}")


if __name__ == "__main__":
    main()
