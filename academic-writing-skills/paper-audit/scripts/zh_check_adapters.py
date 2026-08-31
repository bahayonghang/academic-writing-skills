"""Per-script adapters that turn latex-thesis-zh checker output into AuditIssue.

Each checker has its own CLI and payload. Do not share a generic
"JSON if possible, else text" decoder.
"""

from __future__ import annotations

import json
import re
from typing import Protocol

from report_generator import AuditIssue

# StyleZh Info/Warning → existing AuditIssue severity档位 (not new labels).
STYLE_ZH_SEVERITY: dict[str, str] = {"Info": "Info", "Warning": "Minor"}
STYLE_ZH_PRIORITY: dict[str, str] = {"Info": "P3", "Warning": "P2"}

SPEC_FAIL_SEVERITY = "Major"
SPEC_FAIL_PRIORITY = "P1"

TABLE_LEVEL_SEVERITY: dict[str, str] = {
    "ERROR": "Major",
    "WARNING": "Minor",
    "INFO": "Info",
}
TABLE_LEVEL_PRIORITY: dict[str, str] = {
    "ERROR": "P1",
    "WARNING": "P2",
    "INFO": "P3",
}

ABSTRACT_LEVEL_SEVERITY: dict[str, str] = {
    "Error": "Major",
    "Warning": "Minor",
    "Info": "Info",
}
ABSTRACT_LEVEL_PRIORITY: dict[str, str] = {
    "Error": "P1",
    "Warning": "P2",
    "Info": "P3",
}

CONCLUSION_SEVERITY: dict[str, str] = {
    "Error": "Major",
    "Warning": "Minor",
    "Info": "Info",
}
CONCLUSION_PRIORITY: dict[str, str] = {
    "Error": "P1",
    "Warning": "P2",
    "Info": "P3",
}

BLIND_SEVERITY: dict[str, str] = {
    "HIGH": "Major",
    "MEDIUM": "Minor",
    "INFO": "Info",
}
BLIND_PRIORITY: dict[str, str] = {
    "HIGH": "P0",
    "MEDIUM": "P1",
    "INFO": "P2",
}

_LINE_IN_LOC = re.compile(r"(?:L|:)?(\d+)")
_BLIND_FINDING = re.compile(
    r"\[(HIGH|MEDIUM|INFO)\]\s*\[(P[0123])\]",
)
_LIT_STRUCTURED = re.compile(
    r"\[Severity:\s*(Critical|Major|Minor|Info|Needs Review)\]\s*\[Priority:\s*(P[0123])\]"
)


class AdapterParseError(ValueError):
    """Stdout was present but did not match this adapter's registered schema."""


class CheckAdapter(Protocol):
    def parse(self, stdout: str) -> list[AuditIssue]: ...


def _with_script_tag(message: str) -> str:
    text = message.strip()
    if "[Script]" in text:
        return text
    return f"[Script] {text}"


def _line_from_loc(loc: object) -> int | None:
    if loc is None:
        return None
    if isinstance(loc, int):
        return loc if loc > 0 else None
    match = _LINE_IN_LOC.search(str(loc))
    if not match:
        return None
    value = int(match.group(1))
    return value if value > 0 else None


def _require_json_object(stdout: str) -> dict:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise AdapterParseError("invalid JSON") from exc
    if not isinstance(payload, dict):
        raise AdapterParseError("JSON payload is not an object")
    return payload


def _issue(
    module: str,
    message: str,
    *,
    severity: str,
    priority: str,
    line: int | None = None,
    original: str = "",
    revised: str = "",
    rationale: str = "",
) -> AuditIssue:
    return AuditIssue(
        module=module,
        line=line,
        severity=severity,
        priority=priority,
        message=_with_script_tag(message),
        original=original,
        revised=revised,
        rationale=rationale,
    )


class SpecJsonAdapter:
    """check_spec.py --json → items[].status == FAIL."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        payload = _require_json_object(stdout)
        items = payload.get("items")
        if not isinstance(items, list):
            raise AdapterParseError("check_spec JSON missing items list")
        issues: list[AuditIssue] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if str(item.get("status", "")).upper() != "FAIL":
                continue
            item_id = str(item.get("id", "")).strip() or "SPEC"
            requirement = str(item.get("requirement", "")).strip()
            evidence = str(item.get("evidence", "")).strip()
            message = f"{item_id} {requirement}".strip()
            if evidence:
                message = f"{message} — {evidence}"
            issues.append(
                _issue(
                    "SPEC",
                    message,
                    severity=SPEC_FAIL_SEVERITY,
                    priority=SPEC_FAIL_PRIORITY,
                )
            )
        return issues


class AbstractJsonAdapter:
    """analyze_abstract.py --json (thesis mode checks[] / five-mode elements)."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        payload = _require_json_object(stdout)
        issues: list[AuditIssue] = []
        if str(payload.get("status", "")).upper() == "ERROR":
            issues.append(
                _issue(
                    "ABSTRACT",
                    str(payload.get("message", "abstract analysis error")),
                    severity="Major",
                    priority="P1",
                )
            )
            return issues
        issues.extend(self._from_checks(payload.get("checks")))
        bilingual = payload.get("bilingual")
        if isinstance(bilingual, dict):
            if not bilingual.get("english_found", True):
                issues.append(
                    _issue(
                        "ABSTRACT",
                        "英文摘要缺失",
                        severity="Minor",
                        priority="P2",
                    )
                )
            issues.extend(self._from_checks(bilingual.get("checks")))
        count = payload.get("count")
        if isinstance(count, dict) and str(count.get("status", "PASS")).upper() != "PASS":
            issues.append(
                _issue(
                    "ABSTRACT",
                    f"摘要字数 {count.get('count', '?')}（status={count.get('status')}）",
                    severity="Minor",
                    priority="P2",
                )
            )
        elements = payload.get("elements")
        if isinstance(elements, dict):
            for name, element in elements.items():
                if not isinstance(element, dict):
                    continue
                if element.get("present") is False or element.get("flagged"):
                    issues.append(
                        _issue(
                            "ABSTRACT",
                            str(element.get("message") or f"abstract element {name} missing"),
                            severity="Minor",
                            priority="P2",
                        )
                    )
        return issues

    def _from_checks(self, checks: object) -> list[AuditIssue]:
        if not isinstance(checks, list):
            return []
        issues: list[AuditIssue] = []
        for check in checks:
            if not isinstance(check, dict) or not check.get("flagged"):
                continue
            level = str(check.get("level", "Warning"))
            check_id = str(check.get("id", "T"))
            message = str(check.get("message", ""))
            evidence = str(check.get("evidence", ""))
            issues.append(
                _issue(
                    "ABSTRACT",
                    f"{check_id} {message}".strip(),
                    severity=ABSTRACT_LEVEL_SEVERITY.get(level, "Minor"),
                    priority=ABSTRACT_LEVEL_PRIORITY.get(level, "P2"),
                    original=evidence,
                )
            )
        return issues


class ConclusionJsonAdapter:
    """analyze_conclusion.py --json → findings[]."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        payload = _require_json_object(stdout)
        findings = payload.get("findings")
        if findings is None:
            if str(payload.get("status", "")).upper() == "ERROR":
                return [
                    _issue(
                        "CONCLUSION",
                        str(payload.get("message", "conclusion analysis error")),
                        severity="Major",
                        priority="P1",
                    )
                ]
            raise AdapterParseError("analyze_conclusion JSON missing findings")
        if not isinstance(findings, list):
            raise AdapterParseError("analyze_conclusion findings is not a list")
        issues: list[AuditIssue] = []
        for finding in findings:
            if not isinstance(finding, dict):
                continue
            raw = str(finding.get("severity", "Warning"))
            issues.append(
                _issue(
                    "CONCLUSION",
                    f"{finding.get('code', 'CC')} {finding.get('message', '')}".strip(),
                    severity=CONCLUSION_SEVERITY.get(raw, "Minor"),
                    priority=str(finding.get("priority") or CONCLUSION_PRIORITY.get(raw, "P2")),
                    line=_line_from_loc(finding.get("loc")),
                    revised=str(finding.get("suggestion", "")),
                    rationale=str(finding.get("reason", "")),
                )
            )
        return issues


class TablesJsonAdapter:
    """check_tables.py --json → issues[]."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        payload = _require_json_object(stdout)
        rows = payload.get("issues")
        if not isinstance(rows, list):
            raise AdapterParseError("check_tables JSON missing issues list")
        issues: list[AuditIssue] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            level = str(row.get("level", "WARNING")).upper()
            issues.append(
                _issue(
                    "TABLES",
                    str(row.get("message", "table issue")),
                    severity=TABLE_LEVEL_SEVERITY.get(level, "Minor"),
                    priority=str(row.get("priority") or TABLE_LEVEL_PRIORITY.get(level, "P2")),
                    line=_line_from_loc(row.get("line")),
                )
            )
        return issues


class StyleZhJsonAdapter:
    """check_style_zh.py --json → findings[] with Info/Warning."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        payload = _require_json_object(stdout)
        findings = payload.get("findings")
        if not isinstance(findings, list):
            raise AdapterParseError("check_style_zh JSON missing findings list")
        issues: list[AuditIssue] = []
        for finding in findings:
            if not isinstance(finding, dict):
                continue
            raw = str(finding.get("severity", "Info"))
            issues.append(
                _issue(
                    "SENTENCES",
                    f"{finding.get('code', 'E')} {finding.get('title', '')}".strip(),
                    severity=STYLE_ZH_SEVERITY.get(raw, "Info"),
                    priority=str(finding.get("priority") or STYLE_ZH_PRIORITY.get(raw, "P3")),
                    line=_line_from_loc(finding.get("loc")),
                    original=str(finding.get("original", "")),
                    revised=str(finding.get("suggestion", "")),
                    rationale=str(finding.get("basis", "")),
                )
            )
        return issues


class BlindReviewTextAdapter:
    """blind_review.py text report: Markdown headings + [HIGH]/[P0] finding lines."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        if not stdout.strip():
            return []
        issues: list[AuditIssue] = []
        for raw_line in stdout.splitlines():
            line = raw_line.strip()
            match = _BLIND_FINDING.search(line)
            if not match:
                continue
            raw_sev = match.group(1)
            issues.append(
                _issue(
                    "BLIND",
                    line,
                    severity=BLIND_SEVERITY.get(raw_sev, "Minor"),
                    priority=match.group(2),
                    line=_line_from_loc(line),
                )
            )
        return issues


class LiteratureTextAdapter:
    """analyze_literature.py text protocol, including Needs Review."""

    def parse(self, stdout: str) -> list[AuditIssue]:
        issues: list[AuditIssue] = []
        in_block = False
        for raw_line in stdout.splitlines():
            line = raw_line.strip()
            if not line:
                in_block = False
                continue
            match = _LIT_STRUCTURED.search(line)
            if match:
                raw_sev = match.group(1)
                severity = "Minor" if raw_sev == "Needs Review" else raw_sev
                msg = _LIT_STRUCTURED.sub("", line).strip(" :-")
                issues.append(
                    _issue(
                        "LITERATURE",
                        msg,
                        severity=severity,
                        priority=match.group(2),
                        line=_line_from_loc(line),
                    )
                )
                in_block = True
                continue
            if in_block:
                continue
        return issues


ADAPTERS_BY_SCRIPT: dict[str, CheckAdapter] = {
    "check_spec.py": SpecJsonAdapter(),
    "analyze_abstract.py": AbstractJsonAdapter(),
    "analyze_conclusion.py": ConclusionJsonAdapter(),
    "check_tables.py": TablesJsonAdapter(),
    "check_style_zh.py": StyleZhJsonAdapter(),
    "blind_review.py": BlindReviewTextAdapter(),
    "analyze_literature.py": LiteratureTextAdapter(),
}
