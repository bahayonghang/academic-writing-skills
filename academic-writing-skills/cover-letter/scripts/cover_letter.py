"""Unified CLI for the cover-letter skill.

This is a lightweight orchestration wrapper around the existing deterministic
scripts. The single-purpose scripts remain supported; this entry point gives
the skill documentation one stable command surface:

    cover_letter.py --mode align-check --manuscript main.tex --letter cover.md --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from align_check import run_align_check
from extract_manuscript_facts import extract_facts, load_manuscript_text
from journal_fit_check import VENUES, findings_from_result, run_journal_fit
from presubmission_check import run_checks
from template_meta import load_template_meta

MODES = ("generate", "optimize", "align-check", "journal-fit", "presubmission")


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def _exit_code(findings: list[Any]) -> int:
    severities = {
        str(getattr(finding, "severity", "") or finding.get("severity", "")).lower()
        for finding in findings
    }
    if "major" in severities:
        return 2
    if findings:
        return 1
    return 0


def _render_findings(findings: list[Any]) -> str:
    lines: list[str] = []
    for finding in findings:
        item = _jsonable(finding)
        code = item.get("code") or item.get("axis") or item.get("comment_type", "finding")
        title = item.get("title") or item.get("message") or "Cover-letter finding"
        lines.append(
            "% COVERLETTER "
            f"[Severity: {item.get('severity', 'minor')}] "
            f"[Priority: {item.get('priority', 'P3')}] "
            f"[Source: {item.get('source_kind', 'script')}] "
            f"[Type: {item.get('comment_type', 'presentation')}] "
            f"[{code}]: {title}"
        )
    return "\n".join(lines)


def _draft_cover_letter(facts: dict[str, Any], journal: str) -> str:
    title = facts.get("title") or "[Manuscript title to be confirmed]"
    corresponding_author = facts.get("corresponding_author") or "[Corresponding author]"
    contributions = facts.get("contributions") or []
    contribution_lines = "\n".join(f"- {item}" for item in contributions[:3])
    if not contribution_lines:
        contribution_lines = "- [Key contribution to be confirmed from manuscript]"

    return (
        "Dear Editor,\n\n"
        f'We submit "{title}" for consideration at {journal}. '
        "The manuscript presents the following evidence-backed contributions:\n\n"
        f"{contribution_lines}\n\n"
        "The manuscript has not been published elsewhere and is not under concurrent "
        "consideration. All authors have approved the submission. "
        "[Competing interests / data availability details to be confirmed against the "
        "target journal template.]\n\n"
        f"Sincerely,\n{corresponding_author}\n"
    )


def _require_path(value: str | None, flag: str, *, must_exist: bool = True) -> Path:
    if not value:
        raise ValueError(f"Missing required {flag}")
    path = Path(value).resolve()
    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found for {flag}: {value}")
    return path


def _run_generate(args: argparse.Namespace, journal: str) -> tuple[dict[str, Any], int]:
    manuscript = _require_path(args.manuscript, "--manuscript")
    if manuscript.suffix.lower() != ".tex":
        raise ValueError(f"Unsupported manuscript format: {manuscript.suffix}; expected .tex")
    facts = extract_facts(load_manuscript_text(manuscript))
    # Address the venue by its display name ("IEEE Transactions"), not the slug.
    skill_dir = Path(__file__).resolve().parent.parent
    meta = load_template_meta(skill_dir, journal) or {}
    venue_name = str(meta.get("venue") or journal)
    draft = _draft_cover_letter(facts, venue_name)
    missing = [key for key in ("title", "abstract") if not facts.get(key)]
    findings = [
        {
            "title": f"Manuscript fact `{key}` could not be extracted",
            "quote": "",
            "explanation": "Generation uses a placeholder until the missing field is confirmed.",
            "comment_type": "presentation",
            "severity": "minor",
            "priority": "P3",
            "source_kind": "script",
            "source_section": "opening",
        }
        for key in missing
    ]
    payload = {
        "mode": "generate",
        "journal": journal,
        "manuscript": str(manuscript),
        "facts": facts,
        "draft": draft,
        "findings": findings,
    }
    return payload, _exit_code(findings)


def _run_align_check(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    manuscript = _require_path(args.manuscript, "--manuscript")
    letter = _require_path(args.letter, "--letter")
    issues, claim_map = run_align_check(letter, manuscript)
    payload = {
        "mode": "align-check",
        "manuscript": str(manuscript),
        "letter": str(letter),
        "claim_map": claim_map,
        "findings": _jsonable(issues),
    }
    return payload, _exit_code(payload["findings"])


def _run_presubmission(args: argparse.Namespace, journal: str) -> tuple[dict[str, Any], int]:
    letter = _require_path(args.letter, "--letter")
    skill_dir = Path(__file__).resolve().parent.parent
    issues = run_checks(letter, journal=journal, skill_dir=skill_dir)
    payload = {
        "mode": "presubmission",
        "journal": journal,
        "letter": str(letter),
        "findings": _jsonable(issues),
    }
    return payload, _exit_code(payload["findings"])


def _run_journal_fit(args: argparse.Namespace, journal: str) -> tuple[dict[str, Any], int]:
    letter = _require_path(args.letter, "--letter")
    skill_dir = Path(__file__).resolve().parent.parent
    result = run_journal_fit(letter, journal, skill_dir)
    findings = findings_from_result(result)
    payload = {
        "mode": "journal-fit",
        "journal": journal,
        "letter": str(letter),
        "journal_fit": {
            "venue": result.venue,
            "tier": result.tier,
            "overall": result.overall,
            "axes": _jsonable(result.axes),
        },
        "findings": _jsonable(findings),
    }
    if result.overall == "LOW":
        return payload, 2
    if result.overall == "MEDIUM":
        return payload, max(1, _exit_code(payload["findings"]))
    return payload, _exit_code(payload["findings"])


def _run_optimize(args: argparse.Namespace, journal: str) -> tuple[dict[str, Any], int]:
    presub_payload, _ = _run_presubmission(args, journal)
    findings = list(presub_payload["findings"])
    claim_map: dict[str, Any] | None = None
    manuscript_path = None
    if args.manuscript:
        align_payload, _ = _run_align_check(args)
        findings.extend(align_payload["findings"])
        claim_map = align_payload["claim_map"]
        manuscript_path = align_payload["manuscript"]
    payload = {
        "mode": "optimize",
        "journal": journal,
        "letter": presub_payload["letter"],
        "manuscript": manuscript_path,
        "claim_map": claim_map,
        "findings": findings,
    }
    return payload, _exit_code(findings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified cover-letter CLI: generate, optimize, align-check, journal-fit, or presubmission"
    )
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--manuscript", help="LaTeX manuscript path (.tex)")
    parser.add_argument("--letter", help="Cover letter path (.md or .tex)")
    parser.add_argument(
        "--journal",
        "--venue",
        dest="journal",
        default="generic",
        choices=sorted(VENUES),
        help="Target bundled template / venue",
    )
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    journal = args.journal or "generic"

    try:
        if args.mode == "generate":
            payload, code = _run_generate(args, journal)
        elif args.mode == "align-check":
            payload, code = _run_align_check(args)
        elif args.mode == "presubmission":
            payload, code = _run_presubmission(args, journal)
        elif args.mode == "journal-fit":
            payload, code = _run_journal_fit(args, journal)
        else:
            payload, code = _run_optimize(args, journal)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif args.mode == "generate":
        print(payload["draft"])
        rendered = _render_findings(payload["findings"])
        if rendered:
            print("\n" + rendered)
    else:
        rendered = _render_findings(payload["findings"])
        if rendered:
            print(rendered)

    return code


if __name__ == "__main__":
    raise SystemExit(main())
