#!/usr/bin/env python3
"""Simple skill packager without emoji output."""

import sys
import zipfile
import re
from pathlib import Path


def validate_frontmatter(skill_md_path):
    """Validate SKILL.md frontmatter."""
    content = skill_md_path.read_text(encoding='utf-8')

    # Check for frontmatter
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    return True, "Validation passed"


def package_skill(skill_path, output_dir):
    """Package a skill folder into a .skill file."""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"[ERROR] Skill folder not found: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}")
        return None

    # Validate
    print("[INFO] Validating skill...")
    valid, message = validate_frontmatter(skill_md)
    if not valid:
        print(f"[ERROR] Validation failed: {message}")
        return None
    print(f"[OK] {message}")

    # Prepare output
    skill_name = skill_path.name
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    skill_filename = output_path / f"{skill_name}.skill"

    # Create zip
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n[SUCCESS] Packaged to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"[ERROR] {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python simple_package.py <skill-folder> <output-dir>")
        sys.exit(1)

    result = package_skill(sys.argv[1], sys.argv[2])
    sys.exit(0 if result else 1)
