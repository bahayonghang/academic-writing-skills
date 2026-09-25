import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "sync", Path("docs/scripts/check_resource_sync.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

pairs = [
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md",
        "docs/skills/latex-thesis-zh/resources/references/formatting/formula-guide.md",
        "en",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/number-unit-guide-zh.md",
        "docs/skills/latex-thesis-zh/resources/references/formatting/number-unit-guide-zh.md",
        "en",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/table-guide.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/formatting/table-guide.md",
        "zh",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/format.md",
        "docs/skills/latex-thesis-zh/resources/references/modules/format.md",
        "en",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/references.md",
        "docs/skills/latex-thesis-zh/resources/references/modules/references.md",
        "en",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md",
        "docs/skills/latex-thesis-zh/resources/references/modules/routing-rules.md",
        "en",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/tables.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/modules/tables.md",
        "zh",
    ),
]


def tokens(path: str):
    text = Path(path).read_text(encoding="utf-8")
    return module._markdown_shape(text)["inlineCode"]


for source, other, label in pairs:
    left = tokens(source)
    right = tokens(other)
    print("\n==", Path(source).name, label, len(left), len(right))
    limit = max(len(left), len(right))
    shown = 0
    for index in range(limit):
        a = left[index] if index < len(left) else None
        b = right[index] if index < len(right) else None
        if a != b:
            print(f"{index}: SRC={a!r}")
            print(f"{index}: {label.upper()}={b!r}")
            shown += 1
            if shown >= 12:
                break
