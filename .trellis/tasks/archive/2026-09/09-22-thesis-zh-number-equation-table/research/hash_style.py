import hashlib
from pathlib import Path

path = Path("academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py")
data = path.read_bytes().replace(b"\r\n", b"\n")
print(hashlib.sha256(data).hexdigest())
