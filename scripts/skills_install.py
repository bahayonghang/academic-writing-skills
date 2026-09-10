"""Install catalog skills into a project's agent skill directories.

UX follows ``npx skills add`` (select skills, agents, copy vs symlink) but
does not call npx. Source is this repository's ``academic-writing-skills/``
catalog. Agent paths match this repository's five applicable tools plus Cursor.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import yaml

CATALOG_SKILL_NAMES: tuple[str, ...] = (
    "bib-search-citation",
    "cover-letter",
    "latex-paper-en",
    "latex-thesis-zh",
    "paper-audit",
    "typst-paper",
)

AGENT_PATHS: dict[str, Path] = {
    "claude-code": Path(".claude") / "skills",
    "cursor": Path(".cursor") / "skills",
    "codex": Path(".agents") / "skills",
    "grok": Path(".grok") / "skills",
    "kimi-code": Path(".kimi-code") / "skills",
    "omp": Path(".omp") / "skills",
}

AGENT_ROOTS: dict[str, Path] = {
    "claude-code": Path(".claude"),
    "cursor": Path(".cursor"),
    "codex": Path(".agents"),
    "grok": Path(".grok"),
    "kimi-code": Path(".kimi-code"),
    "omp": Path(".omp"),
}

WRITING_SKILL_NAMES = frozenset(
    {"latex-paper-en", "latex-thesis-zh", "typst-paper"},
)
ALL_TOKENS = frozenset({"all", "*"})
COPY_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

LIMITED_COVERAGE_WARNING = (
    "warning: paper-audit-only install is limited coverage; "
    "sibling writing-skill scripts are skipped. "
    "Install latex-paper-en, latex-thesis-zh, and/or typst-paper "
    "as siblings for full .tex/.typ script-backed checks."
)


@dataclass(frozen=True)
class Skill:
    name: str
    path: Path
    description: str


def default_source_root() -> Path:
    return Path(__file__).resolve().parents[1] / "academic-writing-skills"


def default_method() -> str:
    return "copy" if os.name == "nt" else "symlink"


def parse_frontmatter(skill_md: Path) -> dict[str, object]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


def discover_skills(source_root: Path) -> list[Skill]:
    if not source_root.is_dir():
        return []
    catalog = frozenset(CATALOG_SKILL_NAMES)
    found: list[Skill] = []
    for child in sorted(source_root.iterdir(), key=lambda path: path.name):
        skill_md = child / "SKILL.md"
        if not child.is_dir() or not skill_md.is_file():
            continue
        meta = parse_frontmatter(skill_md)
        name = meta.get("name")
        if name != child.name or name not in catalog:
            continue
        description = meta.get("description", "")
        found.append(
            Skill(
                name=str(name),
                path=child,
                description=str(description).strip(),
            )
        )
    return found


def parse_selection(line: str, items: Sequence[str]) -> list[str]:
    raw = line.strip()
    if not raw:
        raise ValueError("empty selection")
    if raw.lower() in ALL_TOKENS:
        return list(items)
    chosen: list[str] = []
    seen: set[str] = set()
    for part in raw.replace(" ", "").split(","):
        index = int(part)
        if index < 1 or index > len(items):
            raise ValueError(f"selection out of range: {part}")
        name = items[index - 1]
        if name not in seen:
            chosen.append(name)
            seen.add(name)
    if not chosen:
        raise ValueError("empty selection")
    return chosen


def resolve_requested_names(
    requested: Sequence[str],
    allowed: Sequence[str],
    kind: str,
) -> list[str]:
    cleaned = [name for name in requested if name]
    if not cleaned:
        return []
    allowed_list = list(allowed)
    allowed_set = set(allowed_list)
    if any(name.lower() in ALL_TOKENS for name in cleaned):
        return allowed_list
    unknown = [name for name in cleaned if name not in allowed_set]
    if unknown:
        known = ", ".join(allowed_list)
        raise ValueError(f"unknown {kind} {unknown!r}; expected one of: {known}")
    ordered: list[str] = []
    seen: set[str] = set()
    for name in cleaned:
        if name not in seen:
            ordered.append(name)
            seen.add(name)
    return ordered


def detect_existing_agents(dest: Path) -> list[str]:
    found: list[str] = []
    for name, rel in AGENT_ROOTS.items():
        if (dest / rel).is_dir():
            found.append(name)
    return found


def default_agents_for_dest(dest: Path) -> list[str]:
    existing = detect_existing_agents(dest)
    return existing if existing else list(AGENT_PATHS)


def limited_coverage_warning(skill_names: Sequence[str]) -> str | None:
    selected = set(skill_names)
    if "paper-audit" in selected and not (selected & WRITING_SKILL_NAMES):
        return LIMITED_COVERAGE_WARNING
    return None


def remove_install_target(path: Path) -> None:
    """Remove a previous install at ``path`` without following a symlink.

    A prior symlink install points at the catalog. ``rmtree`` on that path
    would delete the catalog skill itself.
    """
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)


def install_skill(source: Path, dest_parent: Path, method: str) -> Path:
    dest_parent.mkdir(parents=True, exist_ok=True)
    dest = dest_parent / source.name
    remove_install_target(dest)
    if method == "copy":
        shutil.copytree(source, dest, ignore=COPY_IGNORE)
        return dest
    if method == "symlink":
        try:
            dest.symlink_to(source.resolve(), target_is_directory=True)
        except OSError as exc:
            raise OSError(f"symlink failed for {dest}: {exc}. Retry with --copy.") from exc
        return dest
    raise ValueError(f"unknown method: {method}")


def _prompt(stdout: IO[str], stdin: IO[str], message: str) -> str:
    stdout.write(message)
    stdout.flush()
    return stdin.readline()


def _prompt_multi(
    stdout: IO[str],
    stdin: IO[str],
    title: str,
    items: Sequence[str],
    labels: Sequence[str] | None = None,
) -> list[str]:
    stdout.write(f"{title}\n")
    display = labels if labels is not None else items
    for index, label in enumerate(display, start=1):
        stdout.write(f"  [{index}] {label}\n")
    stdout.write("Enter numbers (e.g. 1,2,6) or * for all: ")
    stdout.flush()
    line = stdin.readline()
    if not line:
        raise ValueError("empty selection")
    return parse_selection(line, items)


def _confirm(stdout: IO[str], stdin: IO[str]) -> bool:
    answer = _prompt(stdout, stdin, "Proceed with installation? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def _print_summary(
    stdout: IO[str],
    dest: Path,
    skill_names: Sequence[str],
    agents: Sequence[str],
    method: str,
) -> None:
    stdout.write("Installation summary\n")
    stdout.write(f"  dest:   {dest}\n")
    stdout.write(f"  method: {method}\n")
    stdout.write(f"  skills: {', '.join(skill_names)}\n")
    for agent in agents:
        stdout.write(f"  {agent}: {AGENT_PATHS[agent]}\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills-install",
        description=(
            "Install catalog skills from academic-writing-skills/ into a "
            "project's agent skill directories."
        ),
        epilog=(
            "just treats leading hyphens as its own flags. Pass GNU-style "
            "options as: just -- skills-install --copy -y"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill names to install, or 'all'",
    )
    parser.add_argument(
        "-s",
        "--skill",
        action="append",
        default=[],
        dest="skill_flags",
        metavar="NAME",
        help="Skill name (repeatable). Use '*' for all.",
    )
    parser.add_argument(
        "-a",
        "--agent",
        action="append",
        default=[],
        dest="agents",
        metavar="NAME",
        help="Target agent (repeatable). Use '*' for all.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Project root to install into (default: current directory)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Catalog root (default: this repository's academic-writing-skills/)",
    )
    method = parser.add_mutually_exclusive_group()
    method.add_argument(
        "--copy",
        action="store_true",
        help="Copy skill directories instead of creating symlinks",
    )
    method.add_argument(
        "--symlink",
        action="store_true",
        help="Symlink skill directories to the catalog (fails if unsupported)",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List catalog skills without installing",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompts",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Install all catalog skills to all agents without prompts",
    )
    return parser


def _resolve_method(copy_flag: bool, symlink_flag: bool) -> str:
    if copy_flag:
        return "copy"
    if symlink_flag:
        return "symlink"
    return default_method()


def _list_skills(skills: Sequence[Skill], stdout: IO[str]) -> int:
    if not skills:
        stdout.write("No catalog skills found.\n")
        return 1
    for skill in skills:
        description = skill.description.splitlines()[0] if skill.description else ""
        if description:
            stdout.write(f"{skill.name}\t{description}\n")
        else:
            stdout.write(f"{skill.name}\n")
    return 0


def install_plan(
    dest: Path,
    skills: Sequence[Skill],
    agents: Sequence[str],
    method: str,
    stderr: IO[str],
) -> None:
    warning = limited_coverage_warning([skill.name for skill in skills])
    if warning:
        stderr.write(warning + "\n")
    for agent in agents:
        dest_parent = dest / AGENT_PATHS[agent]
        for skill in skills:
            install_skill(skill.path, dest_parent, method)


def main(
    argv: Sequence[str] | None = None,
    *,
    stdin: IO[str] | None = None,
    stdout: IO[str] | None = None,
    stderr: IO[str] | None = None,
    isatty: bool | None = None,
) -> int:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    in_stream = sys.stdin if stdin is None else stdin
    out_stream = sys.stdout if stdout is None else stdout
    err_stream = sys.stderr if stderr is None else stderr
    tty = in_stream.isatty() if isatty is None else isatty

    parser = _build_parser()
    try:
        args = parser.parse_args(argv_list)
    except SystemExit as exc:
        code = exc.code
        return 0 if code is None else int(code)

    source_root = (args.source if args.source is not None else default_source_root()).resolve()
    dest = (args.dest if args.dest is not None else Path.cwd()).resolve()
    catalog = discover_skills(source_root)
    catalog_names = [skill.name for skill in catalog]
    by_name = {skill.name: skill for skill in catalog}

    if args.list:
        return _list_skills(catalog, out_stream)

    if not catalog:
        err_stream.write(f"error: no catalog skills found under {source_root}\n")
        return 1

    try:
        if args.all:
            skill_names = list(catalog_names)
            agents = list(AGENT_PATHS)
            method = _resolve_method(args.copy, args.symlink)
            skip_confirm = True
        else:
            requested_skills = list(args.skills) + list(args.skill_flags)
            requested_agents = list(args.agents)
            has_skill_request = any(name for name in requested_skills)
            has_agent_request = any(name for name in requested_agents)

            if not has_skill_request and not has_agent_request and not args.yes and not tty:
                err_stream.write(
                    "error: non-interactive session requires skill names, --all, or -y\n"
                )
                return 1

            if not has_skill_request and not has_agent_request and not args.yes and tty:
                skill_labels = [
                    f"{skill.name} — {skill.description.splitlines()[0]}"
                    if skill.description
                    else skill.name
                    for skill in catalog
                ]
                skill_names = _prompt_multi(
                    out_stream,
                    in_stream,
                    "Available skills:",
                    catalog_names,
                    skill_labels,
                )
                agents = _prompt_multi(
                    out_stream,
                    in_stream,
                    "Available agents:",
                    list(AGENT_PATHS),
                )
                method_options = ["symlink", "copy"]
                default = default_method()
                method_choice = _prompt_multi(
                    out_stream,
                    in_stream,
                    f"Install method (platform default: {default}):",
                    method_options,
                )
                method = method_choice[0]
                skip_confirm = False
            else:
                if has_skill_request:
                    skill_names = resolve_requested_names(requested_skills, catalog_names, "skill")
                elif tty and not args.yes:
                    skill_names = _prompt_multi(
                        out_stream, in_stream, "Available skills:", catalog_names
                    )
                else:
                    skill_names = list(catalog_names)

                if has_agent_request:
                    agents = resolve_requested_names(requested_agents, list(AGENT_PATHS), "agent")
                elif tty and not args.yes:
                    agents = _prompt_multi(
                        out_stream, in_stream, "Available agents:", list(AGENT_PATHS)
                    )
                else:
                    agents = default_agents_for_dest(dest)

                method = _resolve_method(args.copy, args.symlink)
                skip_confirm = args.yes or not tty
    except ValueError as exc:
        err_stream.write(f"error: {exc}\n")
        return 1

    selected_skills = [by_name[name] for name in skill_names]
    if dest.exists() and not dest.is_dir():
        err_stream.write(f"error: dest is not a directory: {dest}\n")
        return 1

    _print_summary(out_stream, dest, skill_names, agents, method)
    if not skip_confirm:
        try:
            if not _confirm(out_stream, in_stream):
                err_stream.write("installation cancelled\n")
                return 1
        except ValueError as exc:
            err_stream.write(f"error: {exc}\n")
            return 1

    dest.mkdir(parents=True, exist_ok=True)
    try:
        install_plan(dest, selected_skills, agents, method, err_stream)
    except OSError as exc:
        err_stream.write(f"error: {exc}\n")
        return 1

    out_stream.write(f"Installed {len(selected_skills)} skill(s) to {len(agents)} agent(s).\n")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    raise SystemExit(main())
