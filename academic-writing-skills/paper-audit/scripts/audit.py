"""
Paper Audit Orchestrator.
Main entry point for running paper audits across LaTeX, Typst, and PDF formats.
Supports three modes: self-check, review, and gate.
"""

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from detect_language import detect_language
from parsers import get_parser
from report_generator import (
    AuditIssue,
    AuditResult,
    ChecklistItem,
    render_json_report,
    render_report,
)

# --- Mode Configuration ---

MODE_CHECKS: dict[str, list[str]] = {
    "self-check": [
        "format",
        "grammar",
        "logic",
        "sentences",
        "deai",
        "bib",
        "figures",
        "references",
        "visual",
    ],
    "review": [
        "format",
        "grammar",
        "logic",
        "sentences",
        "deai",
        "bib",
        "figures",
        "references",
        "visual",
    ],
    "gate": [
        "format",
        "bib",
        "figures",
        "references",
        "visual",
        "checklist",
    ],
    "polish": ["logic", "sentences"],  # Fast rule-based only; agents handle the rest
}

# Additional checks for Chinese documents
ZH_EXTRA_CHECKS: list[str] = ["consistency", "gbt7714"]

# --- Skill Root Resolution ---

SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_AUDIT = Path(__file__).resolve().parent  # paper-audit's own scripts
SCRIPTS_EN = SKILLS_ROOT / "latex-paper-en" / "scripts"
SCRIPTS_ZH = SKILLS_ROOT / "latex-thesis-zh" / "scripts"
SCRIPTS_TYPST = SKILLS_ROOT / "typst-paper" / "scripts"


def _resolve_script(check_name: str, lang: str, fmt: str) -> Path | None:
    """Resolve the script path for a given check, language, and format."""
    script_map: dict[str, str] = {
        "format": "check_format.py",
        "grammar": "analyze_grammar.py",
        "logic": "analyze_logic.py",
        "sentences": "analyze_sentences.py",
        "deai": "deai_check.py",
        "bib": "verify_bib.py",
        "figures": "check_figures.py",
        "consistency": "check_consistency.py",
        "references": "check_references.py",
        "visual": "visual_check.py",
    }

    script_name = script_map.get(check_name)
    if not script_name:
        return None

    # visual check lives only in paper-audit's own scripts directory
    if check_name == "visual":
        path = SCRIPTS_AUDIT / script_name
        return path if path.exists() else None

    # references: paper-audit has its own router version; fall through to others
    if check_name == "references":
        # Prefer paper-audit's router version first
        path = SCRIPTS_AUDIT / script_name
        if path.exists():
            return path

    # Choose script directory based on format and language
    if fmt == ".typ":
        candidates = [SCRIPTS_TYPST]
    elif lang == "zh":
        candidates = [SCRIPTS_ZH, SCRIPTS_EN]
    else:
        candidates = [SCRIPTS_EN]

    for scripts_dir in candidates:
        path = scripts_dir / script_name
        if path.exists():
            return path

    return None


def _run_check_script(
    script_path: Path, file_path: str, extra_args: list[str] | None = None
) -> tuple[int, str, str]:
    """Run a check script as subprocess and capture output."""
    cmd = [sys.executable, str(script_path), file_path]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(script_path.parent),
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Script timed out after 120 seconds"
    except Exception as e:
        return -1, "", str(e)


def _parse_script_output(module_name: str, stdout: str) -> list[AuditIssue]:
    """
    Parse script output into AuditIssue objects.
    Tries to detect structured output (Severity/Priority format),
    falls back to treating each non-empty line as a Minor issue.
    """
    issues = []
    if not stdout.strip():
        return issues

    # Pattern for structured output: [Severity: X] [Priority: Y]
    structured_pattern = re.compile(
        r"\[Severity:\s*(Critical|Major|Minor)\]\s*\[Priority:\s*(P[012])\]"
    )
    line_pattern = re.compile(r"\(Line\s+(\d+)\)")

    for line in stdout.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        severity = "Minor"
        priority = "P2"
        line_num = None

        # Try structured format
        sev_match = structured_pattern.search(line)
        if sev_match:
            severity = sev_match.group(1)
            priority = sev_match.group(2)

        line_match = line_pattern.search(line)
        if line_match:
            line_num = int(line_match.group(1))

        # Clean message
        msg = line
        msg = structured_pattern.sub("", msg)
        msg = line_pattern.sub("", msg)
        msg = re.sub(r"^%\s*", "", msg)  # LaTeX comment prefix
        msg = re.sub(r"^//\s*", "", msg)  # Typst comment prefix
        msg = re.sub(r"^>\s*", "", msg)  # Markdown quote prefix
        msg = re.sub(r"^\[?\w+\]?\s*", "", msg, count=1)  # Module tag
        msg = msg.strip(" :-")

        if msg:
            issues.append(
                AuditIssue(
                    module=module_name.upper(),
                    line=line_num,
                    severity=severity,
                    priority=priority,
                    message=msg,
                )
            )

    return issues


def _run_checklist(
    content: str,
    file_path: str,
    lang: str,  # noqa: ARG001
) -> list[ChecklistItem]:
    """Run pre-submission checklist checks."""
    items = []

    # Check: no TODO/FIXME/XXX
    todo_lines = [
        i + 1
        for i, line in enumerate(content.split("\n"))
        if re.search(r"\b(TODO|FIXME|XXX)\b", line)
    ]
    items.append(
        ChecklistItem(
            "No placeholder text (TODO, FIXME, XXX)",
            len(todo_lines) == 0,
            f"Found on lines: {todo_lines[:5]}" if todo_lines else "",
        )
    )

    # Check: all figures referenced (LaTeX/Typst)
    ext = Path(file_path).suffix.lower()
    if ext == ".tex":
        fig_labels = set(re.findall(r"\\label\{(fig:[^}]+)\}", content))
        fig_refs = set(re.findall(r"\\ref\{(fig:[^}]+)\}", content))
        unreferenced = fig_labels - fig_refs
        items.append(
            ChecklistItem(
                "All figures referenced in text",
                len(unreferenced) == 0,
                f"Unreferenced: {unreferenced}" if unreferenced else "",
            )
        )

    # Check: all tables referenced (LaTeX)
    if ext == ".tex":
        tab_labels = set(re.findall(r"\\label\{(tab:[^}]+)\}", content))
        tab_refs = set(re.findall(r"\\ref\{(tab:[^}]+)\}", content))
        unref_tabs = tab_labels - tab_refs
        items.append(
            ChecklistItem(
                "All tables referenced in text",
                len(unref_tabs) == 0,
                f"Unreferenced: {unref_tabs}" if unref_tabs else "",
            )
        )

    # Check: anonymous submission (no author names in common patterns)
    anon_patterns = [
        r"\\author\{[^}]*[A-Z][a-z]+",  # LaTeX \author with name
        r"#set document\(author:",  # Typst author
    ]
    has_author = any(re.search(p, content) for p in anon_patterns)
    items.append(
        ChecklistItem(
            "Anonymous submission (blind review check)",
            not has_author,
            "Author information detected — verify if blind review required" if has_author else "",
        )
    )

    # Check: consistent notation (basic — check for mixed $ and \( \))
    if ext == ".tex":
        inline_dollar = len(re.findall(r"(?<!\$)\$(?!\$)", content))
        inline_paren = len(re.findall(r"\\\(", content))
        mixed = inline_dollar > 0 and inline_paren > 0
        items.append(
            ChecklistItem(
                "Consistent math notation",
                not mixed,
                f"Mixed styles: ${inline_dollar}x $...$ and {inline_paren}x \\(...\\)"
                if mixed
                else "",
            )
        )

    # Check: acronyms defined on first use (basic heuristic)
    acronyms = set(re.findall(r"\b([A-Z]{2,6})\b", content))
    undefined = []
    for acr in acronyms:
        # Check if defined as (ACRONYM) or {ACRONYM}
        if not re.search(rf"\({acr}\)|\{{{acr}\}}", content) and acr not in {
            "PDF",
            "URL",
            "API",
            "GPU",
            "CPU",
            "RAM",
            "RGB",
            "CNN",
            "RNN",
            "GAN",
            "NLP",
            "LLM",
            "MLP",
            "LSTM",
            "IEEE",
            "ACM",
            "AAAI",
            "ICLR",
            "ICML",
            "SOTA",
            "BERT",
            "GPT",
            "TODO",
            "FIXME",
            "XXX",
            "YAML",
            "JSON",
            "HTML",
            "HTTP",
            "SQL",
        }:
            undefined.append(acr)
    items.append(
        ChecklistItem(
            "Acronyms defined on first use",
            len(undefined) <= 3,  # Allow some tolerance
            f"Potentially undefined: {undefined[:5]}" if undefined else "",
        )
    )

    return items


def _find_section_for_line(
    line_no: int | None,
    sections: dict[str, tuple[int, int]],
) -> str:
    """Map a line number to its enclosing section name."""
    if line_no is None:
        return "unknown"
    for sec_name, (start, end) in sections.items():
        if start <= line_no <= end:
            return sec_name
    return "unknown"


def _write_state_file(paper_path: Path, data: dict) -> Path:
    """Write polish precheck state JSON next to the paper file."""
    import json

    state_dir = paper_path.parent / ".polish-state"
    state_dir.mkdir(exist_ok=True)
    state_file = state_dir / "precheck.json"
    state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[polish-precheck] State written to: {state_file}")
    return state_file


def run_polish_precheck(
    file_path: str,
    style: str = "A",
    journal: str = "",
    lang: str | None = None,
    skip_logic: bool = False,
) -> AuditResult:
    """
    Fast precheck for polish mode.
    Writes .polish-state/precheck.json next to the paper file.
    Returns AuditResult for report rendering.
    """
    from datetime import datetime

    path = Path(file_path).resolve()
    fmt = path.suffix.lower()
    if fmt == ".pdf":
        raise ValueError("Polish mode requires .tex or .typ source (not PDF).")

    content = path.read_text(encoding="utf-8")
    parser = get_parser(file_path)

    if lang is None:
        clean = parser.clean_text(content)
        lang = detect_language(clean)

    print(f"[polish-precheck] {path.name} | lang={lang} style={style}")

    # Section map
    raw_sections = parser.split_sections(content)  # dict[str, tuple[int,int]]
    lines_list = content.split("\n")
    sections_meta: dict = {}
    for sec_name, (start, end) in raw_sections.items():
        sec_lines = lines_list[start - 1 : end]
        word_count = sum(len(parser.extract_visible_text(ln).split()) for ln in sec_lines)
        sections_meta[sec_name] = {"start": start, "end": end, "word_count": word_count}

    # Non-IMRaD detection
    imrad_core = {"abstract", "introduction", "method", "experiment", "conclusion"}
    non_imrad = len(imrad_core & set(raw_sections)) < 2

    # Rule-based logic check (per-section, skip if --skip-logic)
    precheck_issues: list[dict] = []
    if not skip_logic:
        logic_script = _resolve_script("logic", lang, fmt)
        if logic_script:
            for sec_name in raw_sections:
                rc, stdout, _ = _run_check_script(logic_script, str(path), ["--section", sec_name])
                if rc != -1 and stdout.strip():
                    for issue in _parse_script_output("logic", stdout):
                        precheck_issues.append(
                            {
                                "module": issue.module,
                                "section": sec_name,
                                "line": issue.line,
                                "severity": issue.severity,
                                "priority": issue.priority,
                                "message": issue.message,
                            }
                        )

    # Expression check (sentences)
    expression_issues: list[dict] = []
    sent_script = _resolve_script("sentences", lang, fmt)
    if sent_script:
        rc, stdout, _ = _run_check_script(
            sent_script, str(path), ["--max-words", "60", "--max-clauses", "3"]
        )
        if rc != -1 and stdout.strip():
            for issue in _parse_script_output("sentences", stdout):
                expression_issues.append(
                    {
                        "module": issue.module,
                        "section": _find_section_for_line(issue.line, raw_sections),
                        "line": issue.line,
                        "severity": issue.severity,
                        "priority": issue.priority,
                        "message": issue.message,
                        "original": issue.original,
                        "revised": issue.revised,
                    }
                )

    # Hard blockers = Critical severity
    blockers = [i for i in precheck_issues if i["severity"] == "Critical"]

    precheck_data = {
        "file_path": str(path),
        "language": lang,
        "style": style,
        "journal": journal,
        "sections": sections_meta,
        "precheck_issues": precheck_issues,
        "expression_issues": expression_issues,
        "blockers": blockers,
        "non_imrad": non_imrad,
        "skip_logic": skip_logic,
        "generated_at": datetime.now().isoformat(),
    }
    _write_state_file(path, precheck_data)

    # Return AuditResult so existing render_report() can display precheck issues
    all_issues = [
        AuditIssue(
            module=i["module"],
            line=i.get("line"),
            severity=i["severity"],
            priority=i["priority"],
            message=i["message"],
        )
        for i in precheck_issues + expression_issues
    ]
    return AuditResult(
        file_path=str(path),
        language=lang,
        mode="polish",
        venue=journal,
        issues=all_issues,
    )


def run_audit(
    file_path: str,
    mode: str = "self-check",
    pdf_mode: str = "basic",
    venue: str = "",
    lang: str | None = None,
    style: str = "A",
    journal: str = "",
    skip_logic: bool = False,
    online: bool = False,
    email: str = "",
    scholar_eval: bool = False,
) -> AuditResult:
    """
    Run a complete paper audit.

    Args:
        file_path: Path to the document (.tex, .typ, or .pdf).
        mode: Audit mode — "self-check", "review", or "gate".
        pdf_mode: PDF extraction mode — "basic" or "enhanced".
        venue: Target venue (e.g., "neurips", "ieee").
        lang: Force language ("en" or "zh"). Auto-detects if None.

    Returns:
        AuditResult with all findings.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    fmt = path.suffix.lower()
    if fmt not in (".tex", ".typ", ".pdf"):
        raise ValueError(f"Unsupported format: {fmt}")

    # Polish mode: early dispatch to precheck
    if mode == "polish":
        return run_polish_precheck(
            file_path,
            style=style,
            journal=journal,
            lang=lang,
            skip_logic=skip_logic,
        )

    # Step 1: Extract text
    parser = get_parser(file_path, pdf_mode=pdf_mode)

    if fmt == ".pdf":
        content = parser.extract_text_from_file(str(path))
    else:
        content = path.read_text(encoding="utf-8")

    # Step 2: Detect language
    if lang is None:
        clean = parser.clean_text(content) if fmt != ".pdf" else content
        lang = detect_language(clean)

    print(f"[audit] File: {path.name} | Format: {fmt} | Language: {lang} | Mode: {mode}")

    # Step 3: Determine checks
    checks = list(MODE_CHECKS.get(mode, MODE_CHECKS["self-check"]))
    if lang == "zh":
        checks.extend(ZH_EXTRA_CHECKS)

    # Step 4: Build task list (filter inapplicable checks first)
    all_issues: list[AuditIssue] = []
    tasks: list[tuple[str, Path, list[str]]] = []

    for check_name in checks:
        if check_name == "checklist":
            continue  # Handled separately

        script = _resolve_script(check_name, lang, fmt)
        if script is None:
            print(f"[audit] SKIP {check_name}: script not found")
            continue

        # PDF files need special handling — some scripts expect .tex/.typ
        if fmt == ".pdf" and check_name in ("format", "figures", "references"):
            print(f"[audit] SKIP {check_name}: not applicable for PDF input")
            continue

        # Visual check only applies to PDF input
        if check_name == "visual" and fmt != ".pdf":
            continue

        extra_args: list[str] = []
        if check_name == "sentences":
            extra_args = ["--max-words", "60", "--max-clauses", "3"]
        if check_name == "bib" and online:
            extra_args.append("--online")
            if email:
                extra_args.extend(["--email", email])

        tasks.append((check_name, script, extra_args))

    # Run independent checks in parallel (up to 4 workers)
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_check = {
            executor.submit(_run_check_script, script, str(path), extra_args): check_name
            for check_name, script, extra_args in tasks
        }
        for future in as_completed(future_to_check):
            check_name = future_to_check[future]
            try:
                returncode, stdout, stderr = future.result()
            except Exception as exc:
                returncode, stdout, stderr = -1, "", str(exc)

            if returncode == -1:
                print(f"[audit] ERROR {check_name}: {stderr}")
                all_issues.append(
                    AuditIssue(
                        module=check_name.upper(),
                        line=None,
                        severity="Minor",
                        priority="P2",
                        message=f"Check script failed: {stderr[:100]}",
                    )
                )
            elif stdout.strip():
                issues = _parse_script_output(check_name, stdout)
                all_issues.extend(issues)
                print(f"[audit] {check_name}: {len(issues)} issues found")
            else:
                print(f"[audit] {check_name}: clean")

    # Step 5: Run checklist
    checklist = _run_checklist(content, file_path, lang)

    # Step 6: Build result
    result = AuditResult(
        file_path=str(path),
        language=lang,
        mode=mode,
        venue=venue,
        issues=all_issues,
        checklist=checklist,
    )

    # Step 7: ScholarEval (optional)
    if scholar_eval and mode in ("self-check", "review"):
        try:
            from scholar_eval import build_result as build_scholar_result
            from scholar_eval import evaluate_from_audit

            issue_dicts = [
                {"module": i.module, "severity": i.severity, "message": i.message}
                for i in all_issues
            ]
            script_scores = evaluate_from_audit(issue_dicts)
            result.scholar_eval_result = build_scholar_result(script_scores)
            print("[audit] ScholarEval: script-based scores computed")
        except Exception as exc:
            print(f"[audit] ScholarEval: failed — {exc}")

    return result


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Paper Audit Tool — audit academic papers across formats and languages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audit.py paper.tex                         # Self-check (default)
  python audit.py paper.typ --mode review            # Peer review simulation
  python audit.py paper.pdf --mode gate --pdf-mode enhanced  # Quality gate with enhanced PDF
  python audit.py paper.tex --venue neurips --lang en        # NeurIPS self-check
        """,
    )

    parser.add_argument("file", help="Path to the document (.tex, .typ, or .pdf)")
    parser.add_argument(
        "--mode",
        choices=["self-check", "review", "gate", "polish"],
        default="self-check",
        help="Audit mode (default: self-check)",
    )
    parser.add_argument(
        "--pdf-mode",
        choices=["basic", "enhanced"],
        default="basic",
        help="PDF extraction mode (default: basic)",
    )
    parser.add_argument(
        "--venue",
        default="",
        help="Target venue (e.g., neurips, ieee, acm)",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "zh"],
        default=None,
        help="Force language (auto-detects if not specified)",
    )
    parser.add_argument(
        "--style",
        choices=["A", "B", "C"],
        default="A",
        help="Polish style: A=plain precise, B=narrative, C=formal academic",
    )
    parser.add_argument(
        "--journal",
        default="",
        help="Target journal/venue for polish mode",
    )
    parser.add_argument(
        "--skip-logic",
        action="store_true",
        help="Skip logic checking in polish mode (expression only)",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Enable online bibliography verification via CrossRef/Semantic Scholar",
    )
    parser.add_argument(
        "--email",
        default="",
        help="Email for CrossRef polite pool (faster rate limits)",
    )
    parser.add_argument(
        "--scholar-eval",
        action="store_true",
        help="Enable ScholarEval 8-dimension assessment",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Output format: 'md' for Markdown (default) or 'json' for CI/CD integration",
    )

    args = parser.parse_args()

    try:
        result = run_audit(
            file_path=args.file,
            mode=args.mode,
            pdf_mode=args.pdf_mode,
            venue=args.venue,
            lang=args.lang,
            style=getattr(args, "style", "A"),
            journal=getattr(args, "journal", ""),
            skip_logic=getattr(args, "skip_logic", False),
            online=getattr(args, "online", False),
            email=getattr(args, "email", ""),
            scholar_eval=getattr(args, "scholar_eval", False),
        )

        report = render_json_report(result) if args.format == "json" else render_report(result)

        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"\n[audit] Report saved to: {args.output}")
        else:
            print("\n" + report)

        # Exit code: 1 if critical issues found, 0 otherwise
        has_critical = any(i.severity == "Critical" for i in result.issues)
        return 1 if has_critical else 0

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
