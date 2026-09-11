import sqlite3
from pathlib import Path

db = Path(r"C:\Users\lyh\Zotero\zotero.sqlite")
con = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)
tables = [
    r[0]
    for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
]
print("tables_with_delet:")
for name in tables:
    if "delet" in name.lower() or name == "items":
        print(name)
print("items columns:")
for row in con.execute("PRAGMA table_info(items)"):
    print(row)
print("deletedItems columns:")
try:
    for row in con.execute("PRAGMA table_info(deletedItems)"):
        print(row)
except sqlite3.OperationalError as exc:
    print(exc)
