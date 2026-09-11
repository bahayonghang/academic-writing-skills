import json
from pathlib import Path

items = json.loads(Path("materials/IEEE/corpus/pending-pdf.json").read_text(encoding="utf-8"))
tii = [
    i
    for i in items
    if i.get("venue") == "IEEE Transactions on Industrial Informatics"
]
print("tii_pdf_pending", len(tii))
out = Path("materials/IEEE/corpus/pending-tii.json")
out.write_text(json.dumps(tii, ensure_ascii=False, indent=2), encoding="utf-8")
for i, it in enumerate(tii):
    print(f"{i:02d}\t{it['key']}\t{it.get('date', '')}\t{it['title'][:90]}")
