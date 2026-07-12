#!/usr/bin/env python3
"""
Abstract Structure Analyzer.

Default model is the degree-thesis skeleton (object → pain-point → lead-in →
enumerated work segments → verification). Pass --model five for the legacy
five-element conference-paper model.

Usage:
    uv run python -B analyze_abstract.py main.tex                    # thesis skeleton (doctor)
    uv run python -B analyze_abstract.py main.tex --degree master
    uv run python -B analyze_abstract.py main.tex --bilingual        # + zh/en consistency
    uv run python -B analyze_abstract.py main.tex --model five --lang en --max-words 250
    uv run python -B analyze_abstract.py main.tex --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from parsers import _strip_latex_markup, extract_abstract, extract_title
    from tex_loader import assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import _strip_latex_markup, extract_abstract, extract_title
    from tex_loader import assemble


class AbstractAnalyzer:
    """Analyze abstract structure against the five-element model."""

    STATUS_PRESENT = "PRESENT"
    STATUS_VAGUE = "VAGUE"
    STATUS_MISSING = "MISSING"

    # Detection markers per element
    MARKERS_EN = {
        "background": [
            r"\bhowever\b",
            r"\bremains?\s+unclear\b",
            r"\blimited\s+research\b",
            r"\bgrowing\s+interest\b",
            r"\bchalleng\w*\b",
            r"\bgap\b",
            r"\bdespite\b",
            r"\blittle\s+is\s+known\b",
            r"\bincreasingly\s+important\b",
            r"\bproblem\b",
            r"\bmotivat\w+\b",
            r"\bcrucial\b",
            r"\bcritical\b",
        ],
        "objective": [
            r"\bthis\s+(?:study|paper|work|research)\s+(?:aims?|presents?|proposes?|investigates?|examines?|addresses?|introduces?)\b",
            r"\bwe\s+(?:investigate|propose|present|introduce|address|examine|aim)\b",
            r"\bthe\s+purpose\s+of\b",
            r"\bour\s+goal\b",
            r"\bin\s+this\s+(?:paper|work|study)\b",
            r"\bwe\s+aim\s+to\b",
            r"\bthe\s+objective\b",
        ],
        "methods": [
            r"\bwe\s+propose\b",
            r"\busing\b",
            r"\bdataset\b",
            r"\bparticipants?\b",
            r"\bmethod\b",
            r"\bapproach\b",
            r"\bframework\b",
            r"\bmodel\b",
            r"\balgorithm\b",
            r"\bcollect\w*\b",
            r"\btrain\w*\b",
            r"\bevaluat\w*\b",
            r"\bsample\b",
            r"\bexperiment\w*\b",
            r"\bimplement\w*\b",
            r"\bsurve[ys]\w*\b",
            r"\banalysi[sz]\b",
            r"\bsimulat\w*\b",
        ],
        "results": [
            r"\bresults?\s+show\b",
            r"\bachiev\w*\b",
            r"\boutperform\w*\b",
            r"\baccuracy\b",
            r"\bimprov\w*\b",
            r"\breduc\w*\b",
            r"\bfound\s+that\b",
            r"\bdemonstr\w*\b",
            r"\bsignificant\w*\b",
            r"\bF1\b",
            r"\bprecision\b",
            r"\brecall\b",
            r"\bAUC\b",
            r"\bBLEU\b",
        ],
        "conclusion": [
            r"\bour\s+findings?\s+suggest\b",
            r"\bcontribut\w*\b",
            r"\bimplication\w*\b",
            r"\bcan\s+be\s+used\b",
            r"\benabl\w*\b",
            r"\bprovid\w*\b",
            r"\badvance\w*\b",
            r"\bpotential\b",
            r"\bfuture\s+work\b",
            r"\bpromising\b",
        ],
    }

    MARKERS_ZH = {
        "background": [
            r"然而",
            r"尚不清楚",
            r"研究不足",
            r"日益增长",
            r"挑战",
            r"空白",
            r"尽管",
            r"鲜有研究",
            r"亟需",
            r"问题",
            r"随着",
            r"近年来",
        ],
        "objective": [
            r"本文旨在",
            r"本研究探讨",
            r"本文提出",
            r"研究目的",
            r"为此",
            r"本工作",
            r"本文研究",
            r"旨在",
            r"目的是",
            r"针对",
        ],
        "methods": [
            r"采用",
            r"方法",
            r"数据集",
            r"样本",
            r"模型",
            r"算法",
            r"框架",
            r"实验",
            r"训练",
            r"评估",
            r"构建",
            r"设计",
            r"基于",
        ],
        "results": [
            r"结果表明",
            r"达到",
            r"优于",
            r"准确率",
            r"提高",
            r"降低",
            r"发现",
            r"显著",
            r"表现",
            r"性能",
        ],
        "conclusion": [
            r"研究发现表明",
            r"为.*提供",
            r"有助于",
            r"具有.*意义",
            r"可用于",
            r"推动",
            r"贡献",
            r"展望",
            r"未来",
        ],
    }

    # Vague patterns — signs that an element is present but weak
    VAGUE_PATTERNS_EN = {
        "objective": [
            r"\bwe\s+study\b(?!\s+(?:how|whether|the\s+effect))",
            r"\bthis\s+paper\s+is\s+about\b",
        ],
        "results": [
            r"\bperforms?\s+well\b",
            r"\beffective\b(?!.*\d)",
            r"\bgood\s+results?\b(?!.*\d)",
        ],
        "conclusion": [
            # Conclusion that just echoes results without adding implications
        ],
    }

    def __init__(
        self,
        tex_file: str,
        lang: str = "auto",
        max_words: int = 250,
        max_chars: int = 300,
    ):
        self.tex_file = Path(tex_file).resolve()
        self.lang = lang
        self.max_words = max_words
        self.max_chars = max_chars

    def analyze(self) -> dict:
        """Run the full abstract structure analysis."""
        if not self.tex_file.exists():
            return {
                "status": "ERROR",
                "message": f"File not found: {self.tex_file}",
                "elements": {},
            }

        # Assemble multi-file projects: the abstract often lives in an
        # \include'd front-matter file rather than main.tex itself.
        doc = assemble(self.tex_file)
        abstract_text = extract_abstract(doc.content)

        if not abstract_text.strip():
            return {
                "status": "ERROR",
                "message": "No abstract found in document.",
                "elements": {},
                "warnings": doc.warnings,
            }

        # Detect language
        lang = self.lang
        if lang == "auto":
            lang = self._detect_lang(abstract_text)

        # Split into sentences
        sentences = self._split_sentences(abstract_text, lang)

        # Analyze each element
        markers = self.MARKERS_ZH if lang == "zh" else self.MARKERS_EN
        vague_patterns = {} if lang == "zh" else self.VAGUE_PATTERNS_EN

        elements = {}
        for element_name in ["background", "objective", "methods", "results", "conclusion"]:
            elements[element_name] = self._analyze_element(
                element_name,
                sentences,
                markers.get(element_name, []),
                vague_patterns.get(element_name, []),
                lang,
            )

        # Word/char count
        count_info = self._check_count(abstract_text, lang)

        # Overall status
        statuses = [e["status"] for e in elements.values()]
        if self.STATUS_MISSING in statuses:
            overall = "FAIL"
        elif self.STATUS_VAGUE in statuses:
            overall = "WARNING"
        else:
            overall = "PASS"

        return {
            "status": overall,
            "file": str(self.tex_file),
            "language": lang,
            "elements": elements,
            "count": count_info,
            "warnings": doc.warnings,
        }

    def _detect_lang(self, text: str) -> str:
        """Detect language from text content."""
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        total_chars = len(text.strip())
        if total_chars == 0:
            return "en"
        return "zh" if chinese_chars / total_chars > 0.3 else "en"

    def _split_sentences(self, text: str, lang: str) -> list[str]:
        """Split text into sentences."""
        if lang == "zh":
            # Split on Chinese sentence-ending punctuation
            parts = re.split(r"([。！？；])", text)
            sentences = []
            for i in range(0, len(parts) - 1, 2):
                sent = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
                sent = sent.strip()
                if sent:
                    sentences.append(sent)
            # Handle trailing text
            if len(parts) % 2 == 1 and parts[-1].strip():
                sentences.append(parts[-1].strip())
            return sentences if sentences else [text]
        else:
            # English: split on period/question/exclamation followed by space or end
            raw = re.split(r"(?<=[.!?])\s+", text)
            return [s.strip() for s in raw if s.strip()]

    def _analyze_element(
        self,
        element_name: str,
        sentences: list[str],
        markers: list[str],
        vague_patterns: list[str],
        lang: str,
    ) -> dict:
        """Analyze a single structural element."""
        matched_sentences = []
        for sent in sentences:
            for marker in markers:
                if re.search(marker, sent, re.IGNORECASE):
                    matched_sentences.append(sent)
                    break

        if not matched_sentences:
            return {
                "status": self.STATUS_MISSING,
                "evidence": "",
                "suggestion": self._get_suggestion(element_name, self.STATUS_MISSING, lang),
            }

        # Check for vagueness
        is_vague = False
        for sent in matched_sentences:
            for pattern in vague_patterns:
                if re.search(pattern, sent, re.IGNORECASE):
                    is_vague = True
                    break

        # Special check: results must contain numbers
        if element_name == "results":
            has_numbers = False
            for sent in matched_sentences:
                if re.search(r"\d+\.?\d*\s*[%‰]?", sent):
                    has_numbers = True
                    break
            if not has_numbers:
                is_vague = True

        # Pick the best evidence sentence (first match)
        evidence = matched_sentences[0]
        if len(evidence) > 120:
            evidence = evidence[:117] + "..."

        if is_vague:
            return {
                "status": self.STATUS_VAGUE,
                "evidence": evidence,
                "suggestion": self._get_suggestion(element_name, self.STATUS_VAGUE, lang),
            }

        return {
            "status": self.STATUS_PRESENT,
            "evidence": evidence,
            "suggestion": "",
        }

    def _get_suggestion(self, element: str, status: str, lang: str) -> str:
        """Get improvement suggestion for an element."""
        suggestions = {
            "en": {
                "background": {
                    "MISSING": "Add 1-2 sentences establishing the research context and knowledge gap.",
                    "VAGUE": "Sharpen the background: identify the specific gap this work addresses.",
                },
                "objective": {
                    "MISSING": "Add a sentence starting with 'This study aims to...' or 'We investigate...'",
                    "VAGUE": "Specify the research question: what exactly are you testing or proposing?",
                },
                "methods": {
                    "MISSING": "Describe the core methodology, data source, and evaluation approach.",
                    "VAGUE": "Name the specific technique, dataset, or experimental setup used.",
                },
                "results": {
                    "MISSING": "Report at least one key finding with a concrete number or comparison.",
                    "VAGUE": "Add quantitative evidence: accuracy, improvement percentage, or effect size.",
                },
                "conclusion": {
                    "MISSING": "Add a sentence on the broader significance or practical implications.",
                    "VAGUE": "Go beyond restating results: what does this mean for the field or practice?",
                },
            },
            "zh": {
                "background": {
                    "MISSING": "添加1-2句研究背景，明确研究领域的知识空白或现实需求。",
                    "VAGUE": "细化背景描述：指出本研究要解决的具体问题。",
                },
                "objective": {
                    "MISSING": "添加以'本文旨在...'或'本研究探讨...'开头的研究目标句。",
                    "VAGUE": "明确研究问题：具体要验证什么假设或解决什么问题?",
                },
                "methods": {
                    "MISSING": "描述核心方法、数据来源和评估方式。",
                    "VAGUE": "指明具体的技术手段、数据集或实验设置。",
                },
                "results": {
                    "MISSING": "报告至少一项包含具体数值的关键发现。",
                    "VAGUE": "补充定量证据：准确率、提升百分比或效果量。",
                },
                "conclusion": {
                    "MISSING": "补充研究的理论意义或实践价值。",
                    "VAGUE": "超越结果复述，阐明对领域或实践的启示。",
                },
            },
        }
        lang_key = "zh" if lang == "zh" else "en"
        return suggestions.get(lang_key, {}).get(element, {}).get(status, "")

    def _check_count(self, text: str, lang: str) -> dict:
        """Check word/character count against limits."""
        if lang == "zh":
            # Count Chinese characters (excluding punctuation and spaces)
            chars = len(re.findall(r"[\u4e00-\u9fff]", text))
            return {
                "type": "characters",
                "count": chars,
                "limit": {"min": 200, "max": self.max_chars},
                "status": "PASS" if 200 <= chars <= self.max_chars else "WARNING",
            }
        else:
            words = len(text.split())
            return {
                "type": "words",
                "count": words,
                "limit": {"min": 150, "max": self.max_words},
                "status": "PASS" if 150 <= words <= self.max_words else "WARNING",
            }

    def generate_report(self, result: dict) -> str:
        """Generate human-readable diagnostic report."""
        lines = []
        lines.append("=" * 60)
        lines.append("Abstract Structure Diagnosis")
        lines.append("=" * 60)
        lines.append(f"File: {result.get('file', 'N/A')}")
        lines.append(f"Language: {result.get('language', 'N/A')}")
        lines.append(f"Status: {result['status']}")
        for warn in result.get("warnings", []):
            lines.append(f"WARN: {warn}")

        if result["status"] == "ERROR":
            lines.append(f"Error: {result.get('message', '')}")
            return "\n".join(lines)

        lines.append("")
        lines.append("-" * 60)
        lines.append("Element Diagnosis")
        lines.append("-" * 60)

        icons = {
            self.STATUS_PRESENT: "PRESENT ",
            self.STATUS_VAGUE: "VAGUE   ",
            self.STATUS_MISSING: "MISSING ",
        }

        element_labels = {
            "background": "Background",
            "objective": "Objective",
            "methods": "Methods",
            "results": "Results",
            "conclusion": "Conclusion",
        }

        for key in ["background", "objective", "methods", "results", "conclusion"]:
            elem = result["elements"].get(key, {})
            status = elem.get("status", self.STATUS_MISSING)
            label = element_labels[key]
            icon = icons.get(status, "???")

            lines.append(f"\n  {label:12s}: [{icon}]")
            if elem.get("evidence"):
                ev = elem["evidence"]
                lines.append(f'    Evidence: "{ev}"')
            if elem.get("suggestion"):
                lines.append(f"    Suggestion: {elem['suggestion']}")

        # Word count
        count = result.get("count", {})
        if count:
            lines.append("")
            lines.append("-" * 60)
            ctype = count.get("type", "words")
            cval = count.get("count", 0)
            lim = count.get("limit", {})
            cstatus = count.get("status", "N/A")
            lines.append(
                f"  {ctype.capitalize()}: {cval} "
                f"(limit: {lim.get('min', '?')}–{lim.get('max', '?')}) "
                f"[{cstatus}]"
            )

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


# Yanshan degree-thesis abstract character ranges. Kept byte-identical to
# check_spec.py TEMPLATE_THRESHOLDS["yanshan"]["doctor"|"master"]["abstract"];
# test_abstract_thesis_mode locks the two modules in sync. Deliberately not
# imported from check_spec to avoid pulling in its CLI/template machinery.
THESIS_ABSTRACT_CHARS: dict[str, tuple[int, int]] = {
    "doctor": (900, 1200),
    "master": (500, 650),
}

# Enumerated work-segment marker: （1）（2）… (full-width) or (1)(2)… (half-width).
_ENUM_RE = re.compile(r"[（(]\s*(\d{1,2})\s*[)）]")


def _thesis_sentences(text: str) -> list[str]:
    """Split Chinese abstract text into sentences on 。！？；."""
    parts = re.split(r"[。！？；]", text)
    return [p.strip() for p in parts if p.strip()]


def _enum_segments(text: str) -> list[tuple[int, str]]:
    """Return (number, following-text) for each （1）（2）… enumerated marker."""
    marks = list(_ENUM_RE.finditer(text))
    segments: list[tuple[int, str]] = []
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        segments.append((int(m.group(1)), text[start:end].strip()))
    return segments


def _extract_keywords(content: str) -> list[str]:
    """Extract keyword list from common Chinese-thesis macros/environments.

    Handles \\keywords{}, \\cnkeywords{}, \\thusetup{keywords={...}},
    and \\begin{keyword(s)}...\\end{keyword(s)}. Returns [] when none found.
    """
    raw = ""
    for pat in (
        r"\\cnkeywords\s*\{(.+?)\}",
        r"\\keywords\s*\{(.+?)\}",
        r"\\thusetup\s*\{[^}]*keywords\s*=\s*\{(.+?)\}",
        r"\\begin\{keywords?\}(.+?)\\end\{keywords?\}",
    ):
        m = re.search(pat, content, re.DOTALL)
        if m:
            raw = m.group(1)
            break
    if not raw:
        return []
    raw = _strip_latex_markup(raw)
    parts = re.split(r"[；;，,、]\s*", raw)
    return [p.strip() for p in parts if p.strip()]


def _extract_english_abstract(content: str) -> str:
    """Extract the English abstract from a Chinese-thesis source.

    Supports, in order: dedicated \\begin{eabstract|enabstract|englishabstract}
    environments; the plain \\begin{abstract} environment when the Chinese text
    lives in \\begin{cabstract}; and a \\chapter{Abstract}/\\section{Abstract}
    heading-style block. Returns "" when no English abstract is present.
    Does not touch parsers.py (hash-locked).
    """
    for env in ("eabstract", "enabstract", "englishabstract"):
        m = re.search(rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}", content, re.DOTALL)
        if m:
            return _strip_latex_markup(m.group(1))
    if re.search(r"\\begin\{cabstract\}", content):
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", content, re.DOTALL)
        if m:
            return _strip_latex_markup(m.group(1))
    m = re.search(
        r"\\(?:chapter|section)\*?\s*\{\s*Abstract\s*\}"
        r"(.*?)(?=\\(?:chapter|section)\b|\\end\{document\}|\Z)",
        content,
        re.DOTALL,
    )
    if m:
        return _strip_latex_markup(m.group(1))
    return ""


def _num_tokens(text: str) -> set[str]:
    """Normalized numeric tokens for bilingual comparison (B-NUM).

    Normalizes ％→%, full-width/EN-dash minus→-, drops document-metric counts
    (数字幅/个/篇/页, e.g. "参考文献139篇") that English abstracts routinely omit.
    """
    t = text.replace("％", "%").replace("－", "-").replace("—", "-").replace("−", "-")
    t = re.sub(r"\d+(?:\.\d+)?\s*(?:幅|个|篇|页|章|节)", "", t)
    return set(re.findall(r"\d+(?:\.\d+)?%?", t))


# Canonical ordinal for sequence-word alignment (B-ORD).
_ZH_SEQ = [("首先", 1), ("其次", 2), ("然后", 3), ("最后", 4)]
_EN_SEQ = [("first", 1), ("second", 2), ("then", 3), ("finally", 4)]


def _seq_order(text: str, table: list[tuple[str, int]], word_boundary: bool) -> list[int]:
    """Ordered list of canonical ordinals as sequence words appear in text."""
    hits: list[tuple[int, int]] = []
    for word, rank in table:
        pat = rf"\b{word}\b" if word_boundary else re.escape(word)
        for m in re.finditer(pat, text, re.IGNORECASE):
            hits.append((m.start(), rank))
    hits.sort()
    return [rank for _, rank in hits]


class ThesisAbstractAnalyzer:
    """Diagnose the degree-thesis abstract skeleton (T-* checks).

    Parallel to AbstractAnalyzer (not a subclass): degree theses follow an
    object→pain-point→lead-in→enumerated-work→verification skeleton rather
    than the five-element conference-paper model. See research
    abstract-patterns.md (A/B/C/D/E/F rules) and design.md D1/D3.
    """

    REPORT_HEADER = "Thesis Abstract Skeleton Diagnosis"

    PAIN_WORDS = ["难以", "挑战", "尚未", "无法", "瓶颈", "难题", "困难", "亟需", "制约", "受限"]
    LEAD_RE = re.compile(
        r"(主要研究工作和创新点|研究工作和创新点|主要研究工作|主要研究内容|研究工作|"
        r"研究内容|主要工作|主要创新点|创新点)[^。！？\n]{0,20}(如下|包括)[：:]"
    )
    OPEN_BAD = ["本文", "本论文", "本课题", "针对", "为了", "为解决", "为实现", "提出", "我们"]
    PROB_RE = re.compile(r"^(针对|鉴于|为解决|为了|为实现|为|解决了|面向)")
    VERIFY_WORDS = [
        "仿真",
        "实际生产数据",
        "实测数据",
        "实测",
        "现场应用",
        "工程应用",
        "工业现场",
        "生产数据",
        "实验结果",
        "实验",
    ]
    ORAL_VERBS = ["搞定", "搞了", "搞", "弄好", "弄", "做了"]
    INNOV_WORDS = ["创新", "首次", "新方法", "新见解", "新颖", "创新点", "新框架", "新模型"]
    HEDGE_WORDS = ["约", "以上", "左右", "以内", "区间", "范围", "近", "～", "~", "—", "余"]

    def __init__(
        self,
        tex_file: str,
        degree: str = "doctor",
        max_chars: int | None = None,
        bilingual: bool = False,
    ):
        self.tex_file = Path(tex_file).resolve()
        self.degree = degree if degree in THESIS_ABSTRACT_CHARS else "doctor"
        self.max_chars = max_chars
        self.bilingual = bilingual

    def analyze(self) -> dict:
        if not self.tex_file.exists():
            return {
                "status": "ERROR",
                "mode": "thesis",
                "message": f"File not found: {self.tex_file}",
            }

        doc = assemble(self.tex_file)
        content = doc.content
        text = extract_abstract(content)
        if not text.strip():
            return {
                "status": "ERROR",
                "mode": "thesis",
                "message": "No abstract found in document.",
                "warnings": doc.warnings,
            }

        checks = self._run_checks(text, content)
        count = self._check_count(text)
        bilingual = self._run_bilingual(text, content) if self.bilingual else None

        levels = [c["level"] for c in checks if c["flagged"]]
        if bilingual:
            levels += [c["level"] for c in bilingual["checks"] if c["flagged"]]
        if count["status"] != "PASS":
            levels.append("Warning")
        if "Error" in levels or "Warning" in levels:
            overall = "WARNING"
        elif "Info" in levels:
            overall = "INFO"
        else:
            overall = "PASS"

        return {
            "status": overall,
            "mode": "thesis",
            "file": str(self.tex_file),
            "degree": self.degree,
            "checks": checks,
            "count": count,
            "bilingual": bilingual,
            "warnings": doc.warnings,
        }

    def _run_checks(self, text: str, content: str) -> list[dict]:
        sentences = _thesis_sentences(text)
        first = sentences[0] if sentences else ""
        segments = _enum_segments(text)
        checks: list[dict] = []

        # T-OPEN ★A1 5/5 — first sentence positions the research object, not a method.
        open_bad = any(first.startswith(w) for w in self.OPEN_BAD)
        checks.append(
            self._finding(
                "T-OPEN",
                "Warning",
                "[Script]",
                flagged=open_bad,
                message=(
                    "首句以方法/主体口吻开头，建议改为以研究对象为主语定位（如“X 是/产生于…”）"
                    if open_bad
                    else "首句以研究对象定位"
                ),
                ref="★A1 5/5",
                evidence=first if open_bad else "",
                llm_note=open_bad,
            )
        )

        # T-PAIN ★A2 5/5 — a pain-point / challenge statement is present.
        has_pain = any(w in text for w in self.PAIN_WORDS)
        checks.append(
            self._finding(
                "T-PAIN",
                "Warning",
                "[Script]",
                flagged=not has_pain,
                message="未发现痛点/挑战句（难以/挑战/尚未/瓶颈…）"
                if not has_pain
                else "存在痛点/挑战句",
                ref="★A2 5/5",
            )
        )

        # T-LEAD ★A4 5/5 — a lead-in sentence closing with "：" precedes the list.
        has_lead = bool(self.LEAD_RE.search(text))
        checks.append(
            self._finding(
                "T-LEAD",
                "Warning",
                "[Script]",
                flagged=not has_lead,
                message=(
                    "编号工作段前缺总起句（“主要研究工作如下：”式，以冒号收束）"
                    if not has_lead
                    else "存在总起句并以冒号收束"
                ),
                ref="★A4 5/5",
            )
        )

        # T-ENUM ★A5 5/5, D4 — body is （1）（2）… work segments, sequentially numbered.
        nums = [n for n, _ in segments]
        enum_ok = len(nums) >= 2 and nums == list(range(1, len(nums) + 1))
        if not nums:
            enum_msg = "未发现编号工作段（（1）（2）…）"
        elif not enum_ok:
            enum_msg = f"编号工作段不连续或不足：{nums}"
        else:
            enum_msg = f"{len(nums)} 个编号工作段，编号连续"
        checks.append(
            self._finding(
                "T-ENUM",
                "Warning",
                "[Script]",
                flagged=not enum_ok,
                message=enum_msg,
                ref="★A5 5/5、D4",
            )
        )

        # T-PROB ★B1 — work segments open with a problem-oriented phrase (Info; skip if none).
        if segments:
            prob_hits = sum(1 for _, seg in segments if self.PROB_RE.search(seg))
            prob_flag = prob_hits < len(segments) * 0.5
            checks.append(
                self._finding(
                    "T-PROB",
                    "Info",
                    "[Script]",
                    flagged=prob_flag,
                    message=f"仅 {prob_hits}/{len(segments)} 个工作段以问题导向短语开头（针对/鉴于/为…）",
                    ref="★B1",
                )
            )
        else:
            checks.append(self._skip("T-PROB", "Info", "[Script]", "无编号工作段，跳过", "★B1"))

        # T-VERIFY ★C2 5/5 — verification method is named, not a vague "验证了有效性".
        has_verify = any(w in text for w in self.VERIFY_WORDS)
        checks.append(
            self._finding(
                "T-VERIFY",
                "Warning",
                "[Script]",
                flagged=not has_verify,
                message=(
                    "未点名验证方式（仿真/实际生产数据/实测/现场应用/实验…），避免空泛“验证了有效性”"
                    if not has_verify
                    else "验证方式已点名"
                ),
                ref="★C2 5/5",
            )
        )

        # T-VERB ★B4 — oral method verbs (搞/弄/做了) are out of the normative set (Info).
        oral = [v for v in self.ORAL_VERBS if v in text]
        checks.append(
            self._finding(
                "T-VERB",
                "Info",
                "[Script]",
                flagged=bool(oral),
                message=(
                    f"出现口语动词 {oral}，建议改用 提出/建立/设计/构建/研究/采用"
                    if oral
                    else "方法动词属规范集"
                ),
                ref="★B4",
            )
        )

        # T-ABBR ★E3 5/5 — abbreviations defined at first occurrence (heuristic + LLM).
        undefined = self._undefined_abbrs(text)
        checks.append(
            self._finding(
                "T-ABBR",
                "Warning",
                "[Script]",
                flagged=bool(undefined),
                message=(
                    f"疑似缩略语首现未定义中英全称：{undefined}（需人工复核）"
                    if undefined
                    else "未发现未定义缩略语"
                ),
                ref="★E3 5/5",
                llm_note=bool(undefined),
            )
        )

        # T-NUM-HEDGE C3 2/2 — numeric metrics carry robust hedging (Info; only if numbers).
        has_pct = bool(re.search(r"\d+(?:\.\d+)?\s*[%％]", text))
        if has_pct:
            has_hedge = any(w in text for w in self.HEDGE_WORDS)
            checks.append(
                self._finding(
                    "T-NUM-HEDGE",
                    "Info",
                    "[Script]",
                    flagged=not has_hedge,
                    message=(
                        "数值指标建议加“约/以上/区间”等稳健表述"
                        if not has_hedge
                        else "数值指标带稳健表述"
                    ),
                    ref="C3 2/2",
                )
            )
        else:
            checks.append(
                self._skip("T-NUM-HEDGE", "Info", "[Script]", "摘要无数值指标，跳过", "C3 2/2")
            )

        # T-KW-FIRST ★D2 — first keyword ≈ research object / process (Info; skip if no keywords).
        keywords = _extract_keywords(content)
        if not keywords:
            checks.append(self._skip("T-KW-FIRST", "Info", "[Script]", "未找到关键词，跳过", "★D2"))
        else:
            title = extract_title(content)
            first_kw = keywords[0]
            overlap = sum(1 for ch in first_kw if ch in title)
            kw_flag = bool(title) and overlap < max(2, len(first_kw) // 2)
            checks.append(
                self._finding(
                    "T-KW-FIRST",
                    "Info",
                    "[Script]",
                    flagged=kw_flag,
                    message=(
                        f"首个关键词“{first_kw}”与标题主名词重叠低，建议对齐研究对象/过程名"
                        if kw_flag
                        else f"首个关键词“{first_kw}”与标题呼应"
                    ),
                    ref="★D2",
                )
            )

        # T-INNOV web A3 校规 — innovation is stated (words or enumerated work segments).
        has_innov = any(w in text for w in self.INNOV_WORDS) or len(nums) >= 2
        checks.append(
            self._finding(
                "T-INNOV",
                "Warning",
                "[Script]",
                flagged=not has_innov,
                message=(
                    "未体现创新表述（创新/首次提出/新方法…或编号工作段）"
                    if not has_innov
                    else "体现创新表述"
                ),
                ref="web A3 校规",
            )
        )

        # T-TOC-STYLE web A10 — not a table-of-contents / over-long background (Warning + LLM).
        toc_chapters = len(re.findall(r"第[一二三四五六七八九十\d]+章", text))
        bg_ratio = 0.0
        if segments:
            first_mark = _ENUM_RE.search(text)
            if first_mark:
                bg_ratio = first_mark.start() / max(len(text), 1)
        toc_flag = toc_chapters >= 2 or bg_ratio > 0.4
        checks.append(
            self._finding(
                "T-TOC-STYLE",
                "Warning",
                "[Script]",
                flagged=toc_flag,
                message=(
                    f"疑似目录式/背景铺陈过长（第X章 {toc_chapters} 处，背景占比 {bg_ratio:.0%}）"
                    if toc_flag
                    else "非目录式，背景比例合理"
                ),
                ref="web A10 软性",
                llm_note=toc_flag,
            )
        )

        # T-VOICE PRD 约束2 — first person 我/我们/笔者 only; 本文/本论文 are legal (Info).
        voice_hits = re.findall(r"笔者|我们|我(?!国)", text)
        checks.append(
            self._finding(
                "T-VOICE",
                "Info",
                "[Script]",
                flagged=bool(voice_hits),
                message=(
                    "出现第一人称（我/我们/笔者），学位论文摘要建议改“本文/本论文”"
                    if voice_hits
                    else "无第一人称（“本文/本论文”合法）"
                ),
                ref="PRD 约束2",
            )
        )
        return checks

    def _undefined_abbrs(self, text: str) -> list[str]:
        """Heuristic: uppercase abbreviations lacking a nearby parenthetical definition."""
        undefined: list[str] = []
        seen: set[str] = set()
        for m in re.finditer(r"[A-Za-z]*[A-Z]{2,}[A-Za-z]*", text):
            tok = m.group(0)
            if tok in seen or len(tok) < 2:
                continue
            seen.add(tok)
            window = text[max(0, m.start() - 25) : m.end() + 2]
            # Defined if a parenthesis sits in the window (中英全称括注 or the token
            # itself appears inside parentheses, e.g. 长短期记忆(long ..., LSTM)).
            if any(p in window for p in "（(）)"):
                continue
            undefined.append(tok)
        return undefined

    def _check_count(self, text: str) -> dict:
        chars = len(re.findall(r"[一-鿿]", text))
        lo, hi = THESIS_ABSTRACT_CHARS[self.degree]
        if self.max_chars is not None:
            hi = self.max_chars
        return {
            "type": "characters",
            "count": chars,
            "limit": {"min": lo, "max": hi},
            "status": "PASS" if lo <= chars <= hi else "WARNING",
        }

    def _run_bilingual(self, zh_text: str, content: str) -> dict:
        en_text = _extract_english_abstract(content)
        checks: list[dict] = []
        found = bool(en_text.strip())

        # B-LEN web A9 — English abstract present and not obviously truncated.
        if not found:
            checks.append(
                self._finding(
                    "B-LEN",
                    "Warning",
                    "[Script]",
                    flagged=True,
                    message="未找到英文摘要（eabstract/englishabstract/abstract/\\chapter{Abstract}）",
                    ref="web A9",
                )
            )
        else:
            too_short = len(en_text) < 0.5 * len(zh_text)
            checks.append(
                self._finding(
                    "B-LEN",
                    "Warning",
                    "[Script]",
                    flagged=too_short,
                    message=(
                        f"英文摘要明显过短（{len(en_text)} vs 中文 {len(zh_text)} 字符）"
                        if too_short
                        else "英文摘要长度合理"
                    ),
                    ref="web A9",
                )
            )

        # B-ORD ★F3 5/5 — sequence words align in count and order.
        zh_order = _seq_order(zh_text, _ZH_SEQ, word_boundary=False)
        en_order = _seq_order(en_text, _EN_SEQ, word_boundary=True)
        if zh_order or en_order:
            ord_flag = zh_order != en_order
            checks.append(
                self._finding(
                    "B-ORD",
                    "Warning",
                    "[Script]",
                    flagged=ord_flag,
                    message=(
                        f"序词数量/顺序不一致：中 {zh_order} vs 英 {en_order}"
                        if ord_flag
                        else "首先/其次/然后/最后 与 First/Second/Then/Finally 对齐"
                    ),
                    ref="★F3 5/5",
                )
            )
        else:
            checks.append(
                self._skip("B-ORD", "Warning", "[Script]", "中英均无序词，跳过", "★F3 5/5")
            )

        # B-NUM ★F1；web A9 — numeric token sets match (Error; hard mismatch).
        zh_nums, en_nums = _num_tokens(zh_text), _num_tokens(en_text)
        if zh_nums or en_nums:
            num_flag = zh_nums != en_nums
            diff = zh_nums ^ en_nums
            checks.append(
                self._finding(
                    "B-NUM",
                    "Error",
                    "[Script]",
                    flagged=num_flag,
                    message=(
                        f"中英数值不一致，差异 token：{sorted(diff)}"
                        if num_flag
                        else "中英数值 token 集合一致"
                    ),
                    ref="★F1；web A9",
                )
            )
        else:
            checks.append(
                self._skip("B-NUM", "Error", "[Script]", "中英均无数值，跳过", "★F1；web A9")
            )

        # B-ENUM ★F1 — enumerated work-segment count matches.
        zh_cnt, en_cnt = len(_enum_segments(zh_text)), len(_enum_segments(en_text))
        if zh_cnt or en_cnt:
            enum_flag = zh_cnt != en_cnt
            checks.append(
                self._finding(
                    "B-ENUM",
                    "Warning",
                    "[Script]",
                    flagged=enum_flag,
                    message=(
                        f"编号工作段条数不一致：中 {zh_cnt} vs 英 {en_cnt}"
                        if enum_flag
                        else f"编号工作段条数一致（{zh_cnt}）"
                    ),
                    ref="★F1",
                )
            )
        else:
            checks.append(
                self._skip("B-ENUM", "Warning", "[Script]", "中英均无编号段，跳过", "★F1")
            )

        # B-SEM ★F1 — per-element semantic correspondence is an LLM-lane task.
        checks.append(
            self._finding(
                "B-SEM",
                "Info",
                "[LLM]",
                flagged=False,
                message="逐句/逐要素语义对应需 LLM 复核：请对照中英摘要，核查每个工作段的对象、方法、结论是否一一对译",
                ref="★F1",
            )
        )
        return {"english_found": found, "checks": checks}

    @staticmethod
    def _finding(
        check_id: str,
        level: str,
        source: str,
        flagged: bool,
        message: str,
        ref: str,
        evidence: str = "",
        llm_note: bool = False,
    ) -> dict:
        return {
            "id": check_id,
            "level": level,
            "source": source,
            "flagged": flagged,
            "skipped": False,
            "message": message,
            "ref": ref,
            "evidence": evidence,
            "needs_llm": llm_note,
        }

    @staticmethod
    def _skip(check_id: str, level: str, source: str, message: str, ref: str) -> dict:
        return {
            "id": check_id,
            "level": level,
            "source": source,
            "flagged": False,
            "skipped": True,
            "message": message,
            "ref": ref,
            "evidence": "",
            "needs_llm": False,
        }

    def generate_report(self, result: dict) -> str:
        lines = ["=" * 60, self.REPORT_HEADER, "=" * 60]
        lines.append(f"File: {result.get('file', 'N/A')}")
        if result["status"] == "ERROR":
            lines.append(f"Error: {result.get('message', '')}")
            return "\n".join(lines)
        lines.append(f"Degree: {result['degree']}")
        lines.append(f"Status: {result['status']}")
        for warn in result.get("warnings", []):
            lines.append(f"WARN: {warn}")

        count = result["count"]
        lines.append(
            f"Characters: {count['count']} "
            f"(limit: {count['limit']['min']}–{count['limit']['max']}) [{count['status']}]"
        )

        lines.append("")
        lines.append("-" * 60)
        lines.append("Skeleton Checks")
        lines.append("-" * 60)
        for c in result["checks"]:
            lines.append(self._render_check(c))

        bilingual = result.get("bilingual")
        if bilingual is not None:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Bilingual Consistency (中英摘要一致性)")
            lines.append("-" * 60)
            for c in bilingual["checks"]:
                lines.append(self._render_check(c))
            lines.append("")
            lines.append(
                "注：英文摘要方法句时态/语态检测不在本模块，见 deai 模块"
                "（tense-guide-zh.md 英文摘要区域门控）。"
            )

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    @staticmethod
    def _render_check(c: dict) -> str:
        if c["skipped"]:
            icon = "·"
        elif not c["flagged"]:
            icon = "✅"
        elif c["level"] == "Error":
            icon = "❌"
        elif c["level"] == "Warning":
            icon = "⚠️"
        else:
            icon = "ℹ️"
        tag = f"[{c['level']}]" if c["flagged"] else ""
        llm = " [需LLM复核]" if c.get("needs_llm") else ""
        parts = [f"[{icon}] {c['id']:<12} {c['source']}", tag, c["message"], f"({c['ref']})"]
        line = " ".join(p for p in parts if p) + llm
        if c.get("evidence"):
            line += f'\n      证据: "{c["evidence"]}"'
        return line


def main():
    parser = argparse.ArgumentParser(
        description="Abstract Structure Analyzer - degree-thesis skeleton (default) or five-element"
    )
    parser.add_argument("tex_file", help=".tex or .typ file to analyze")
    parser.add_argument(
        "--model",
        choices=["thesis", "five"],
        default="thesis",
        help="Diagnosis model: 'thesis' degree-thesis skeleton (default) or 'five' five-element",
    )
    parser.add_argument(
        "--degree",
        choices=["doctor", "master"],
        default="doctor",
        help="Degree level for thesis-mode char limits (default: doctor)",
    )
    parser.add_argument(
        "--bilingual",
        action="store_true",
        help="thesis mode: also check zh/en abstract consistency (B-* checks)",
    )
    parser.add_argument(
        "--lang",
        choices=["en", "zh", "auto"],
        default="auto",
        help="five mode: abstract language (default: auto-detect)",
    )
    parser.add_argument(
        "--max-words", type=int, default=250, help="five mode: max word count for EN (default: 250)"
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=None,
        help="Max char count. thesis mode overrides the degree upper bound; five mode default 300",
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}")
        sys.exit(1)

    if args.model == "thesis":
        analyzer = ThesisAbstractAnalyzer(
            args.tex_file,
            degree=args.degree,
            max_chars=args.max_chars,
            bilingual=args.bilingual,
        )
    else:
        analyzer = AbstractAnalyzer(
            args.tex_file,
            lang=args.lang,
            max_words=args.max_words,
            max_chars=args.max_chars if args.max_chars is not None else 300,
        )
    result = analyzer.analyze()

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(analyzer.generate_report(result))

    sys.exit(1 if result["status"] == "ERROR" else 0)


if __name__ == "__main__":
    main()
