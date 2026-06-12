#!/usr/bin/env python3
"""
Thesis Structure Mapper - Map multi-file thesis structure

Usage:
    uv run python map_structure.py main.tex
    uv run python map_structure.py main.tex --json
    uv run python map_structure.py main.tex --detect-template
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

try:
    from tex_loader import iter_files
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from tex_loader import iter_files


class ThesisStructureMapper:
    """Map LaTeX thesis file structure and detect template type."""

    # Known university templates — documentclass detection patterns only.
    # 展示性事实（图表编号风格、参考文献样式等）单源于 templates/<id>.md。
    TEMPLATES = {
        "thuthesis": {
            "pattern": r"\\documentclass.*\{thuthesis\}",
            "name": "Tsinghua University (thuthesis)",
        },
        "pkuthss": {
            "pattern": r"\\documentclass.*\{pkuthss\}",
            "name": "Peking University (pkuthss)",
        },
        "ustcthesis": {
            "pattern": r"\\documentclass.*\{ustcthesis\}",
            "name": "USTC (ustcthesis)",
        },
        "fduthesis": {
            "pattern": r"\\documentclass.*\{fduthesis\}",
            "name": "Fudan University (fduthesis)",
        },
        "ctexbook": {
            "pattern": r"\\documentclass.*\{ctexbook\}",
            "name": "Generic Chinese Book (ctexbook)",
        },
    }

    # File type detection patterns
    FILE_TYPES = {
        "cover": ["cover", "titlepage", "frontpage", "封面"],
        "abstract": ["abstract", "abs", "摘要"],
        "declaration": ["declaration", "authorization", "声明", "原创性"],
        "toc": ["toc", "contents", "目录"],
        "symbol": ["symbol", "notation", "nomenclature", "符号", "术语"],
        "chapter": ["chap", "chapter", "章"],
        "appendix": ["appendix", "app", "附录"],
        "bibliography": ["bib", "ref", "reference", "参考文献"],
        "acknowledgment": ["ack", "thanks", "致谢", "后记"],
        "resume": ["resume", "publication", "简历", "论文目录", "发表"],
    }

    def __init__(self, main_file: str):
        self.main_file = Path(main_file).resolve()
        self.root_dir = self.main_file.parent
        self.visited: set[Path] = set()
        self.structure: list[dict] = []
        self.template: Optional[str] = None

    def map(self) -> list[dict]:
        """Map the thesis structure starting from main file."""
        self.structure = []
        self.visited = set()
        for node in iter_files(self.main_file):
            if not node.exists:
                self.structure.append(
                    {
                        "file": node.rel,
                        "level": node.level,
                        "type": "missing",
                        "exists": False,
                    }
                )
                continue
            self.visited.add(node.path)
            self.structure.append(
                {
                    "file": node.rel,
                    "level": node.level,
                    "type": self._detect_file_type(node.path),
                    "exists": True,
                }
            )
            if node.level == 0 and node.content is not None:
                self.template = self._detect_template(node.content)
        return self.structure

    def _detect_file_type(self, tex_file: Path) -> str:
        """Detect the type of a LaTeX file based on name and content."""
        name = tex_file.stem.lower()

        for file_type, patterns in self.FILE_TYPES.items():
            for pattern in patterns:
                if pattern in name:
                    # Special handling for chapters
                    if file_type == "chapter":
                        match = re.search(r"(\d+)", name)
                        if match:
                            return f"第{match.group(1)}章"
                    return file_type

        return "other"

    def _detect_template(self, content: str) -> Optional[str]:
        """Detect university template from document class."""
        for template_id, info in self.TEMPLATES.items():
            if re.search(info["pattern"], content):
                return template_id
        return None

    def get_template_info(self) -> Optional[dict]:
        """Get information about detected template."""
        if self.template and self.template in self.TEMPLATES:
            return self.TEMPLATES[self.template]
        return None

    def get_processing_order(self) -> list[str]:
        """Get recommended processing order."""
        if not self.structure:
            self.map()

        # Priority order
        priority = {
            "cover": 0,
            "declaration": 1,
            "abstract": 2,
            "toc": 3,
            "symbol": 4,
            "第1章": 5,
            "第2章": 6,
            "第3章": 7,
            "第4章": 8,
            "第5章": 9,
            "chapter": 10,
            "appendix": 11,
            "bibliography": 12,
            "acknowledgment": 13,
            "resume": 14,
            "other": 15,
            "missing": 99,
        }

        def get_priority(item):
            t = item["type"]
            for key in priority:
                if t.startswith(key) or t == key:
                    return priority[key]
            return priority["other"]

        sorted_structure = sorted(self.structure, key=get_priority)
        return [item["file"] for item in sorted_structure if item["exists"]]

    def check_completeness(self) -> dict:
        """Check thesis structure completeness."""
        if not self.structure:
            self.map()

        found_types = {item["type"] for item in self.structure if item["exists"]}

        required = ["cover", "abstract", "bibliography", "acknowledgment"]
        recommended = ["declaration", "symbol", "resume"]

        missing_required = [
            t for t in required if not any(ft.startswith(t) or ft == t for ft in found_types)
        ]
        missing_recommended = [
            t for t in recommended if not any(ft.startswith(t) or ft == t for ft in found_types)
        ]

        # Check for chapters
        chapters = [item for item in self.structure if item["type"].startswith("第")]
        has_intro = any("1" in item["type"] for item in chapters)
        has_conclusion = len(chapters) >= 2

        return {
            "complete": len(missing_required) == 0,
            "missing_required": missing_required,
            "missing_recommended": missing_recommended,
            "chapter_count": len(chapters),
            "has_introduction": has_intro,
            "has_conclusion": has_conclusion,
        }

    def generate_tree(self) -> str:
        """Generate a tree-style visualization."""
        if not self.structure:
            self.map()

        lines = []
        lines.append("=" * 60)
        lines.append("Thesis Structure / 论文结构树")
        lines.append("=" * 60)

        if self.template:
            template_info = self.get_template_info()
            lines.append(f"Template: {template_info['name'] if template_info else self.template}")
            lines.append("")

        for i, item in enumerate(self.structure):
            indent = "  " * item["level"]
            prefix = "├── " if i < len(self.structure) - 1 else "└── "
            prefix = indent + prefix if item["level"] > 0 else ""

            status = "" if item["exists"] else " [MISSING]"
            type_label = f"({item['type']})"

            lines.append(f"{prefix}{item['file']} {type_label}{status}")

        # Completeness check
        completeness = self.check_completeness()
        lines.append("")
        lines.append("-" * 60)
        lines.append("Completeness Check / 完整性检查")
        lines.append("-" * 60)
        lines.append(f"Status: {'✅ Complete' if completeness['complete'] else '⚠️ Incomplete'}")
        lines.append(f"Chapters: {completeness['chapter_count']}")

        if completeness["missing_required"]:
            lines.append(f"Missing Required: {', '.join(completeness['missing_required'])}")
        if completeness["missing_recommended"]:
            lines.append(f"Missing Recommended: {', '.join(completeness['missing_recommended'])}")

        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Thesis Structure Mapper")
    parser.add_argument("tex_file", help="Main .tex file")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--detect-template", "-d", action="store_true", help="Only detect and report template type"
    )
    parser.add_argument("--order", "-o", action="store_true", help="Output processing order")

    args = parser.parse_args()

    # Validate input
    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    # Map structure
    mapper = ThesisStructureMapper(args.tex_file)
    structure = mapper.map()

    if args.detect_template:
        template = mapper.template
        info = mapper.get_template_info()
        if template:
            print(f"Template: {template}")
            if info:
                print(f"Name: {info['name']}")
            # 模板事实快照（图表编号风格等）见 templates/；精确映射用 detect_template.py
        else:
            print("Template: Unknown (generic)")
        sys.exit(0)

    if args.order:
        order = mapper.get_processing_order()
        print("Recommended processing order:")
        for i, f in enumerate(order, 1):
            print(f"  {i}. {f}")
        sys.exit(0)

    if args.json:
        import json

        output = {
            "template": mapper.template,
            "template_info": mapper.get_template_info(),
            "structure": structure,
            "completeness": mapper.check_completeness(),
            "processing_order": mapper.get_processing_order(),
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(mapper.generate_tree())


if __name__ == "__main__":
    main()
