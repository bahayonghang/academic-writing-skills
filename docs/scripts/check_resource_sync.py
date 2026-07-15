"""Validate the source-to-bilingual-doc resource contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "academic-writing-skills"
DOCS_ROOT = REPO_ROOT / "docs"
MANIFEST_PATH = DOCS_ROOT / "resource-manifest.json"

PUBLIC_KINDS = ("references", "templates", "examples", "agents")
KIND_SUFFIXES = {
    "references": {".md", ".yaml", ".yml"},
    "templates": {".md"},
    "examples": {".md"},
    "agents": {".md"},
}
SOURCE_LOCALES = {"en", "zh", "neutral"}
TEXT_RESOURCE_SUFFIXES = {".md", ".yaml", ".yml"}
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})\s+")
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
LINK_TARGET_RE = re.compile(
    r"(?P<prefix>!?\[[^\]]*\]\()"
    r"(?P<target>[^)\s]+)"
    r"(?P<suffix>(?:\s+['\"][^'\"]*['\"])?\))"
)
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")


def sha256(path: Path) -> str:
    return hashlib.sha256(_normalized_resource_bytes(path)).hexdigest()


def _normalized_resource_bytes(path: Path) -> bytes:
    content = path.read_bytes()
    if path.suffix.lower() in TEXT_RESOURCE_SUFFIXES:
        return content.replace(b"\r\n", b"\n")
    return content


def public_source_files(repo_root: Path = REPO_ROOT) -> list[tuple[str, str, Path]]:
    skills_root = repo_root / "academic-writing-skills"
    resources: list[tuple[str, str, Path]] = []
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        for kind in PUBLIC_KINDS:
            kind_root = skill_dir / kind
            if not kind_root.exists():
                continue
            for source in sorted(path for path in kind_root.rglob("*") if path.is_file()):
                if source.suffix.lower() in KIND_SUFFIXES[kind]:
                    resources.append((skill_dir.name, kind, source))
    return resources


def _strip_non_prose(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_fence = False
    fence = ""
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    for index, line in enumerate(lines):
        if in_frontmatter:
            if index > 0 and line.strip() == "---":
                in_frontmatter = False
            continue
        match = FENCE_RE.match(line.lstrip())
        if match:
            marker = match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
            continue
        if not in_fence:
            output.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(output)


def infer_source_locale(path: Path) -> str:
    if path.suffix.lower() != ".md":
        return "neutral"
    prose = _strip_non_prose(path.read_text(encoding="utf-8-sig"))
    han_count = len(HAN_RE.findall(prose))
    latin_count = len(LATIN_RE.findall(prose))
    return "zh" if han_count >= 20 and han_count >= latin_count * 0.12 else "en"


def canonical_doc_path(skill: str, kind: str, relative: Path, locale: str) -> str:
    prefix = Path("docs") if locale == "en" else Path("docs") / "zh"
    return (prefix / "skills" / skill / "resources" / kind / relative).as_posix()


def build_manifest_entries(
    repo_root: Path = REPO_ROOT, existing_locales: dict[str, str] | None = None
) -> list[dict[str, str]]:
    existing_locales = existing_locales or {}
    entries: list[dict[str, str]] = []
    for skill, kind, source in public_source_files(repo_root):
        kind_root = repo_root / "academic-writing-skills" / skill / kind
        relative = source.relative_to(kind_root)
        source_rel = source.relative_to(repo_root).as_posix()
        source_locale = existing_locales.get(source_rel, infer_source_locale(source))
        entries.append(
            {
                "skill": skill,
                "kind": kind,
                "source": source_rel,
                "sourceLocale": source_locale,
                "sourceSha256": sha256(source),
                "en": canonical_doc_path(skill, kind, relative, "en"),
                "zh": canonical_doc_path(skill, kind, relative, "zh"),
            }
        )
    return entries


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("manifest must be an object with version=1")
    entries = data.get("resources")
    if not isinstance(entries, list):
        raise ValueError("manifest resources must be a list")
    return entries


def write_manifest(repo_root: Path = REPO_ROOT, path: Path = MANIFEST_PATH) -> int:
    existing_locales: dict[str, str] = {}
    if path.exists():
        try:
            existing_locales = {
                entry["source"]: entry["sourceLocale"] for entry in load_manifest(path)
            }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            existing_locales = {}
    entries = build_manifest_entries(repo_root, existing_locales)
    payload = {"version": 1, "resources": entries}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(entries)


def validate_inventory(entries: list[dict[str, str]], repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    actual = {entry["source"]: entry for entry in build_manifest_entries(repo_root)}
    manifest: dict[str, dict[str, str]] = {}
    required = {"skill", "kind", "source", "sourceLocale", "sourceSha256", "en", "zh"}

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"resources[{index}] must be an object")
            continue
        missing = required - set(entry)
        if missing:
            errors.append(f"resources[{index}] missing fields: {sorted(missing)}")
            continue
        source = entry["source"]
        if source in manifest:
            errors.append(f"duplicate manifest source: {source}")
        manifest[source] = entry
        if entry["sourceLocale"] not in SOURCE_LOCALES:
            errors.append(f"{source}: invalid sourceLocale {entry['sourceLocale']!r}")

    missing_sources = sorted(set(actual) - set(manifest))
    extra_sources = sorted(set(manifest) - set(actual))
    errors.extend(f"manifest missing source: {source}" for source in missing_sources)
    errors.extend(f"manifest has stale source: {source}" for source in extra_sources)

    target_paths: Counter[str] = Counter()
    for source in sorted(set(actual) & set(manifest)):
        expected = actual[source]
        entry = manifest[source]
        for field in ("skill", "kind", "sourceSha256", "en", "zh"):
            if entry[field] != expected[field]:
                errors.append(
                    f"{source}: {field} is {entry[field]!r}, expected {expected[field]!r}"
                )
        target_paths.update((entry["en"], entry["zh"]))

    errors.extend(
        f"duplicate target path: {path}" for path, count in target_paths.items() if count > 1
    )
    return errors


def _markdown_shape(text: str) -> dict[str, list[Any]]:
    headings: list[int] = []
    code_blocks: list[str] = []
    prose_lines: list[str] = []
    current_code: list[str] = []
    in_fence = False
    fence = ""
    table_shape: list[int] = []

    for line in text.splitlines():
        match = FENCE_RE.match(line.lstrip())
        if match:
            marker = match.group(1)[0]
            if not in_fence:
                in_fence = True
                fence = marker
                current_code = [line]
            else:
                current_code.append(line)
                if marker == fence:
                    in_fence = False
                    code_blocks.append("\n".join(current_code))
            continue
        if in_fence:
            current_code.append(line)
            continue
        prose_lines.append(line)
        heading = HEADING_RE.match(line)
        if heading:
            headings.append(len(heading.group(1)))
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            table_shape.append(stripped.count("|") - 1)

    prose = "\n".join(prose_lines)
    return {
        "headings": headings,
        "codeBlocks": code_blocks,
        "inlineCode": INLINE_CODE_RE.findall(prose),
        "links": LINK_RE.findall(prose),
        "tableShape": table_shape,
    }


def _mask_markdown_link_targets(text: str) -> str:
    return LINK_TARGET_RE.sub(r"\g<prefix><link-target>\g<suffix>", text)


def compare_markdown(
    source: str,
    translated: str,
    label: str = "translation",
    *,
    allow_link_rewrites: bool = False,
) -> list[str]:
    source_shape = _markdown_shape(source)
    translated_shape = _markdown_shape(translated)
    errors: list[str] = []
    labels = {
        "headings": "heading levels",
        "codeBlocks": "fenced code blocks",
        "inlineCode": "inline code tokens",
        "links": "link targets",
        "tableShape": "table shape",
    }
    if allow_link_rewrites:
        labels.pop("links")
    for field, description in labels.items():
        if source_shape[field] != translated_shape[field]:
            errors.append(f"{label}: {description} differ from source")
    return errors


def _selected_entries(entries: list[dict[str, str]], skill: str | None) -> list[dict[str, str]]:
    if skill is None:
        return entries
    selected = [entry for entry in entries if entry["skill"] == skill]
    if not selected:
        raise ValueError(f"unknown or empty skill: {skill}")
    return selected


def validate_targets(
    entries: list[dict[str, str]], repo_root: Path = REPO_ROOT, skill: str | None = None
) -> list[str]:
    errors: list[str] = []
    selected = _selected_entries(entries, skill)
    expected_by_root: dict[Path, set[Path]] = {}

    for entry in selected:
        source = repo_root / entry["source"]
        targets = {locale: repo_root / entry[locale] for locale in ("en", "zh")}
        for locale, target in targets.items():
            resource_root = (
                repo_root
                / "docs"
                / ("zh" if locale == "zh" else "")
                / "skills"
                / entry["skill"]
                / "resources"
            )
            expected_by_root.setdefault(resource_root.resolve(), set()).add(target.resolve())
            if not target.is_file():
                errors.append(f"{entry['source']}: missing {locale} target {entry[locale]}")

        if not all(target.is_file() for target in targets.values()):
            continue

        source_bytes = _normalized_resource_bytes(source)
        en_bytes = _normalized_resource_bytes(targets["en"])
        zh_bytes = _normalized_resource_bytes(targets["zh"])
        source_locale = entry["sourceLocale"]
        if source_locale == "neutral":
            if en_bytes != source_bytes or zh_bytes != source_bytes:
                errors.append(f"{entry['source']}: neutral targets must match source exactly")
            continue

        if source.suffix.lower() == ".md":
            source_text = source.read_text(encoding="utf-8-sig")
            target_texts = {
                locale: target.read_text(encoding="utf-8-sig") for locale, target in targets.items()
            }
            faithful_text = target_texts[source_locale]
            if _mask_markdown_link_targets(faithful_text) != _mask_markdown_link_targets(
                source_text
            ):
                errors.append(
                    f"{entry['source']}: {source_locale} target must match source except "
                    "rewritten link targets"
                )
            for locale, _target in targets.items():
                errors.extend(
                    compare_markdown(
                        source_text,
                        target_texts[locale],
                        f"{entry['source']} {locale}",
                        allow_link_rewrites=True,
                    )
                )
            en_links = _markdown_shape(target_texts["en"])["links"]
            zh_links = _markdown_shape(target_texts["zh"])["links"]
            if en_links != zh_links:
                errors.append(f"{entry['source']}: bilingual link targets differ")
            if len(_strip_non_prose(source_text).strip()) >= 120 and en_bytes == zh_bytes:
                errors.append(f"{entry['source']}: prose translation is identical across locales")
        else:
            faithful_bytes = en_bytes if source_locale == "en" else zh_bytes
            if faithful_bytes != source_bytes:
                errors.append(
                    f"{entry['source']}: {source_locale} target must match source exactly"
                )

    for resource_root, expected in expected_by_root.items():
        actual = set()
        if resource_root.exists():
            actual = {path.resolve() for path in resource_root.rglob("*") if path.is_file()}
        for path in sorted(actual - expected):
            errors.append(f"unexpected or legacy resource: {path.relative_to(repo_root)}")
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--skill")
    parser.add_argument("--write-manifest", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.inventory_only and args.skill:
        print("error: --inventory-only and --skill cannot be combined", file=sys.stderr)
        return 2
    if args.write_manifest:
        count = write_manifest()
        print(f"wrote {count} resource entries to {MANIFEST_PATH.relative_to(REPO_ROOT)}")

    try:
        entries = load_manifest()
        errors = validate_inventory(entries)
        if not args.inventory_only:
            errors.extend(validate_targets(entries, skill=args.skill))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"resource contract failed with {len(errors)} error(s)")
        return 1

    scope = "inventory" if args.inventory_only else args.skill or "all resources"
    print(f"resource contract passed: {scope} ({len(entries)} manifest entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
