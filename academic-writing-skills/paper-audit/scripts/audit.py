"""
Paper Audit Orchestrator.
Main entry point for running paper audits across LaTeX, Typst, and PDF formats.
Supports three modes: self-check, review, and gate.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from detect_language import detect_language
from parsers import get_parser
from report_generator import (
    AuditIssue,
    AuditResult,
    ChecklistItem,
    render_report,
)

# --- Mode Configuration ---

MODE_CHECKS: dict[str, list[str]] = {
    "self-check": [
        "format", "grammar", "logic", "sentences", "deai", "bib", "figures",
    ],
    "review": [
        "format", "grammar", "logic", "sentences", "deai", "bib", "figures",
    ],
    "gate": [
        "format", "bib", "figures", "checklist",
    ],
}

# Additional checks for Chinese documents
ZH_EXTRA_CHECKS: list[str] = ["consistency", "gbt7714"]

# --- Skill Root Resolution ---

SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
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
    }

    script_name = script_map.get(check_name)
    if not script_name:
        return None

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


def _parse_script_output(
    module_name: str, stdout: str
) -> list[AuditIssue]:
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
        msg = re.sub(r"^%\s*", "", msg)       # LaTeX comment prefix
        msg = re.sub(r"^//\s*", "", msg)       # Typst comment prefix
        msg = re.sub(r"^>\s*", "", msg)        # Markdown quote prefix
        msg = re.sub(r"^\[?\w+\]?\s*", "", msg, count=1)  # Module tag
        msg = msg.strip(" :-")

        if msg:
            issues.append(AuditIssue(
                module=module_name.upper(),
                line=line_num,
                severity=severity,
                priority=priority,
                message=msg,
            ))

    return issues


def _run_checklist(
    content: str, file_path: str, lang: str  # noqa: ARG001
) -> list[ChecklistItem]:
    """Run pre-submission checklist checks."""
    items = []

    # Check: no TODO/FIXME/XXX
    todo_lines = [
        i + 1 for i, line in enumerate(content.split("\n"))
        if re.search(r"\b(TODO|FIXME|XXX)\b", line)
    ]
    items.append(ChecklistItem(
        "No placeholder text (TODO, FIXME, XXX)",
        len(todo_lines) == 0,
        f"Found on lines: {todo_lines[:5]}" if todo_lines else "",
    ))

    # Check: all figures referenced (LaTeX/Typst)
    ext = Path(file_path).suffix.lower()
    if ext == ".tex":
        fig_labels = set(re.findall(r"\\label\{(fig:[^}]+)\}", content))
        fig_refs = set(re.findall(r"\\ref\{(fig:[^}]+)\}", content))
        unreferenced = fig_labels - fig_refs
        items.append(ChecklistItem(
            "All figures referenced in text",
            len(unreferenced) == 0,
            f"Unreferenced: {unreferenced}" if unreferenced else "",
        ))

    # Check: all tables referenced (LaTeX)
    if ext == ".tex":
        tab_labels = set(re.findall(r"\\label\{(tab:[^}]+)\}", content))
        tab_refs = set(re.findall(r"\\ref\{(tab:[^}]+)\}", content))
        unref_tabs = tab_labels - tab_refs
        items.append(ChecklistItem(
            "All tables referenced in text",
            len(unref_tabs) == 0,
            f"Unreferenced: {unref_tabs}" if unref_tabs else "",
        ))

    # Check: anonymous submission (no author names in common patterns)
    anon_patterns = [
        r"\\author\{[^}]*[A-Z][a-z]+",  # LaTeX \author with name
        r"#set document\(author:",         # Typst author
    ]
    has_author = any(re.search(p, content) for p in anon_patterns)
    items.append(ChecklistItem(
        "Anonymous submission (blind review check)",
        not has_author,
        "Author information detected — verify if blind review required" if has_author else "",
    ))

    # Check: consistent notation (basic — check for mixed $ and \( \))
    if ext == ".tex":
        inline_dollar = len(re.findall(r"(?<!\$)\$(?!\$)", content))
        inline_paren = len(re.findall(r"\\\(", content))
        mixed = inline_dollar > 0 and inline_paren > 0
        items.append(ChecklistItem(
            "Consistent math notation",
            not mixed,
            f"Mixed styles: ${inline_dollar}x $...$ and {inline_paren}x \\(...\\)" if mixed else "",
        ))

    # Check: acronyms defined on first use (basic heuristic)
    acronyms = set(re.findall(r"\b([A-Z]{2,6})\b", content))
    undefined = []
    for acr in acronyms:
        # Check if defined as (ACRONYM) or {ACRONYM}
        if not re.search(rf"\({acr}\)|\{{{acr}\}}", content):
            # Common acronyms to skip
            if acr not in {"PDF", "URL", "API", "GPU", "CPU", "RAM", "RGB", "CNN",
                          "RNN", "GAN", "NLP", "LLM", "MLP", "LSTM", "IEEE", "ACM",
                          "AAAI", "ICLR", "ICML", "SOTA", "BERT", "GPT", "TODO",
                          "FIXME", "XXX", "YAML", "JSON", "HTML", "HTTP", "SQL"}:
                undefined.append(acr)
    items.append(ChecklistItem(
        "Acronyms defined on first use",
        len(undefined) <= 3,  # Allow some tolerance
        f"Potentially undefined: {undefined[:5]}" if undefined else "",
    ))

    return items


def run_audit(
    file_path: str,
    mode: str = "self-check",
    pdf_mode: str = "basic",
    venue: str = "",
    lang: str | None = None,
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

    # Step 4: Run checks
    all_issues: list[AuditIssue] = []

    for check_name in checks:
        if check_name == "checklist":
            continue  # Handled separately

        script = _resolve_script(check_name, lang, fmt)
        if script is None:
            print(f"[audit] SKIP {check_name}: script not found")
            continue

        # PDF files need special handling — some scripts expect .tex/.typ
        if fmt == ".pdf" and check_name in ("format", "figures"):
            print(f"[audit] SKIP {check_name}: not applicable for PDF input")
            continue

        print(f"[audit] Running {check_name}...")

        extra_args = []
        if check_name == "sentences":
            extra_args = ["--max-words", "60", "--max-clauses", "3"]

        returncode, stdout, stderr = _run_check_script(script, str(path), extra_args)

        if returncode == -1:
            print(f"[audit] ERROR {check_name}: {stderr}")
            all_issues.append(AuditIssue(
                module=check_name.upper(),
                line=None,
                severity="Minor",
                priority="P2",
                message=f"Check script failed: {stderr[:100]}",
            ))
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

    parser.add_argument(
        "file", help="Path to the document (.tex, .typ, or .pdf)"
    )
    parser.add_argument(
        "--mode", choices=["self-check", "review", "gate"],
        default="self-check",
        help="Audit mode (default: self-check)",
    )
    parser.add_argument(
        "--pdf-mode", choices=["basic", "enhanced"],
        default="basic",
        help="PDF extraction mode (default: basic)",
    )
    parser.add_argument(
        "--venue", default="",
        help="Target venue (e.g., neurips, ieee, acm)",
    )
    parser.add_argument(
        "--lang", choices=["en", "zh"],
        default=None,
        help="Force language (auto-detects if not specified)",
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    try:
        result = run_audit(
            file_path=args.file,
            mode=args.mode,
            pdf_mode=args.pdf_mode,
            venue=args.venue,
            lang=args.lang,
        )

        report = render_report(result)

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
