"""Append eval id 54 without reordering ids 1-53."""

import json
from pathlib import Path

path = Path("academic-writing-skills/latex-thesis-zh/evals/evals.json")
raw = path.read_bytes()
newline = "\r\n" if b"\r\n" in raw else "\n"
payload = json.loads(raw.decode("utf-8"))
ids = [item["id"] for item in payload["evals"]]
assert ids == list(range(1, 54)), ids
payload["evals"].append(
    {
        "id": 54,
        "prompt": (
            "请对附带的合成稿做学院数字、公式、表身和中文题注检查。"
            "四个入口都使用 --school yanshan-ee-2025。"
            "不要改默认检查，不要接受单独的 yanshan，也不要输出整句替换或改写数学。"
        ),
        "expected_output": (
            "路由到 check_style_zh.py、check_format.py、check_tables.py 和 check_references.py "
            "的 --school yanshan-ee-2025。数字间隔和千分空只在 style；公式引导、末标点、续行、"
            "上式和下式、式中只在 format；表身同上和同单位表头、表题末标点只在 tables；"
            "非表浮动体中文题注只在 references。每项均为 [Script]、Info/P3、Meaning-Check: NEEDS-LLM。"
            "默认和 --school generic 不新增候选。"
        ),
        "files": ["evals/fixtures/number-equation-table/main.tex"],
        "assertions": [
            {
                "type": "regex",
                "pattern": "(--school|yanshan-ee-2025)",
                "description": "routes the college school flag",
            },
            {
                "type": "contains",
                "text": "Meaning-Check: NEEDS-LLM",
                "description": "script layer does not claim semantic preservation",
            },
            {
                "type": "not_contains",
                "text": "Meaning-Check: PRESERVED",
                "description": "script layer never claims semantic preservation",
            },
            {
                "type": "regex",
                "pattern": "(候选|局部|Info/P3|\\[Script\\])",
                "description": "reports a local candidate rather than a full-sentence replacement",
            },
        ],
    }
)
text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
if newline == "\r\n":
    text = text.replace("\n", "\r\n")
path.write_bytes(text.encode("utf-8"))
print("appended", len(payload["evals"]))
