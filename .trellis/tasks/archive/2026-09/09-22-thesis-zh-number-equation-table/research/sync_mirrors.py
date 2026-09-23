"""Copy C2 source pages onto the same-language docs mirrors."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAIRS = (
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/formatting/formula-guide.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/number-unit-guide-zh.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/formatting/number-unit-guide-zh.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/caption-guide.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/formatting/caption-guide.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/formatting/table-guide.md",
        "docs/skills/latex-thesis-zh/resources/references/formatting/table-guide.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/expression.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/modules/expression.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/format.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/modules/format.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/references.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/modules/references.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md",
        "docs/zh/skills/latex-thesis-zh/resources/references/modules/routing-rules.md",
    ),
    (
        "academic-writing-skills/latex-thesis-zh/references/modules/tables.md",
        "docs/skills/latex-thesis-zh/resources/references/modules/tables.md",
    ),
)


def main() -> None:
    for source, target in PAIRS:
        src = ROOT / source
        dst = ROOT / target
        dst.write_bytes(src.read_bytes())
        print(f"copied {source}")


if __name__ == "__main__":
    main()
