#!/usr/bin/env python3
"""
中文表达/语句级检查器 — 中文学位论文版本

规则真相源：references/writing/academic-style-zh.md；数字与单位另见
references/formatting/number-unit-guide-zh.md。九个检查器 E-* 的分档、输入区域与排除条件
见 references/modules/expression.md。

零重复边界（重造必冲突，勿在本脚本实现）：
  - 人称（我们/本文）→ abstract 模块的 T-VOICE / T-OPEN
  - 论断强度分级 → references/writing/over-claim-guard.md
  - 模板专属数字规范终检 → spec-check 的 YS-36
  - 句长均匀度（CV，AI 痕迹）→ deai 的 D1；本脚本只查单句可读性长度
  - 段落顺序与论证 → logic

Usage:
    uv run python -B check_style_zh.py main.tex
    uv run python -B check_style_zh.py main.tex --section 绪论
    uv run python -B check_style_zh.py main.tex --goal concision --strength moderate
    uv run python -B check_style_zh.py main.tex --json
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

try:
    from parsers import get_parser, resolve_section_keys
    from tex_loader import assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser, resolve_section_keys
    from tex_loader import assemble


GOAL_CHOICES = ("grammar", "clarity", "concision", "coherence")
STRENGTH_CHOICES = ("minimal", "moderate", "restructure")

# 本模块无规则的编辑目标 → 显式路由，而不是返回空结果假装"没问题"。
UNSUPPORTED_GOALS = {"coherence": "logic"}

DEFAULT_MAX_CHARS = 80

# ── E-COLLOQ：口语化程度副词（style-zh §1.1，闭集） ──────────────────────────
# §1.3 的单字动词（用/做/看/想/试）**不实现**：它们是"采用""制作""看法"等合法词的子串，
# 规则层无法判定，属 llm-only，只在模块文档指导 LLM。
COLLOQ_MAP = {
    "很多": "大量、众多、若干",
    "非常": "极为、显著、相当",
    "一些": "部分、若干、某些",
    "很好": "优异、显著、卓越",
    "特别": "尤其、尤为、格外",
}
# 「特别是」是 style-zh §3.4 推荐的举例连接词，不算口语化。
COLLOQ_EXCLUDE = {"特别": ("特别是",)}

# ── E-ABSOLUTE：绝对化词汇（style-zh §2.1） ─────────────────────────────────
ABSOLUTE_TERMS = {
    "显然": "研究表明、实验结果显示",
    "毫无疑问": "可以认为、有理由相信",
    "众所周知": "已有研究指出、文献表明",
    "必然": "往往、通常、一般而言",
    "最好": "较优、更优、具有优势",
    "绝对": "在本文实验条件下",
    "完全": "在本文实验条件下基本",
}
# 引述他人观点时这些词属于转述而非本文论断，不报。
CITATION_CONTEXT_RE = re.compile(r"文献\s*[\[［]|等[\[［]|已有研究|前人研究|该文献|作者认为")
# --degree-wording 才启用。只跳过这些合法搭配里的「绝对」词位，不跳过整句。
LEGAL_ABSOLUTE_COLLOCATIONS = (
    "绝对误差",
    "绝对值",
    "绝对温度",
    "绝对湿度",
    "绝对压力",
    "绝对坐标",
)
DEGREE_PHRASES = ("极易", "极低", "完全忽略", "高度贴合")

# ── E-COLLOC：搭配不当（style-zh §4.1，闭集错误搭配对） ─────────────────────
# 动词与宾语之间允许「了/过」与不超过 6 字的定语（"增加了模型的效率"），但不跨标点——
# 跨句会把"增加了训练数据，效率也提高"误判成搭配错误。
COLLOC_ERRORS = (
    ("发挥", "发现", "问题"),
    ("增加", "提高", "效率"),
    ("扩大", "提高", "精度"),
    ("改进", "改正", "缺点"),
)

# ── E-INCOMP：成分残缺（style-zh §4.2） ────────────────────────────────────
# 中文承前省略主语合法且普遍，规则只能识别句式，不能判定是否真缺主语 → 只报候选。
INCOMP_LEAD_RE = re.compile(r"^(?:通过|经过|利用|借助|采用)[^，。；]{2,30}，")
# 只列真正能充当主语的标记。「所提」修饰宾语（"验证了所提方法的有效性"仍缺主语），
# 放进来会把 design 里的标准正例判成合法句。
SUBJECT_MARKERS = ("本文", "本研究", "本章", "本节", "作者", "笔者", "文中", "该方法", "我们")

# ── E-PUNCT：中英标点混用（style-zh §5.3） ─────────────────────────────────
CJK_RE = re.compile(r"[一-鿿]")
ASCII_PUNCT_RE = re.compile(r"[,;:?!]")
# §5.2/§5.3 的两条豁免：英文术语内部、括号内全英文。另排除 URL/路径/文件名。
URL_LIKE_RE = re.compile(
    r"https?://\S+|\S+\.(?:tex|bib|pdf|png|jpg|eps|csv|py|m)\b|[\\/][\w./\\-]+"
)
PAREN_ALL_ASCII_RE = re.compile(r"[(（][^()（）]*[)）]")
ASCII_RUN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ,;:?!.\'\"()\[\]/+*=<>_-]*[A-Za-z0-9]")

# ── E-NUMSPACE：数值与单位空格（style-zh §6.2） ────────────────────────────
UNIT_WORDS = (
    "kg|mg|g|t|km|cm|mm|nm|m|s|ms|ns|h|min|Hz|kHz|MHz|GHz|"
    "Pa|kPa|MPa|GPa|N|J|kJ|W|kW|MW|V|kV|A|mA|K|mol|L|mL|dB|bit|B|KB|MB|GB|TB"
)
NUM_UNIT_NOSPACE_RE = re.compile(rf"(?<![A-Za-z0-9])(\d+(?:\.\d+)?)({UNIT_WORDS})(?![A-Za-z0-9])")
# 国标规定不空格的量：百分号、角度、摄氏度。默认 E-NUMSPACE 仍用此例外。
# 学院模式不把 ℃ 并入平面角豁免，见 _check_college_numbers。
UNIT_NO_SPACE = ("%", "°", "℃", "‰", "′", "″")
SCHOOL_CHOICES = ("yanshan-ee-2025", "generic")
_COLLEGE_SCHOOL = "yanshan-ee-2025"
_UNIT_WORD_RE = re.compile(rf"(?:{UNIT_WORDS})(?![A-Za-z0-9])")
_COLLEGE_NUM_RE = re.compile(r"(?<![A-Za-z0-9\\.])(-?)(\d+(?:\\,\d+)*(?:\.\d+(?:\\,\d+)*)?)")
_COLLEGE_SPACE_RE = re.compile(
    r"(?<![A-Za-z0-9\\])"
    r"(-?(?:\d+(?:\\,\d+)*)(?:\.\d+(?:\\,\d+)*)?)"
    r"("
    r"\\%|%|℃|°C(?![A-Za-z])|\\celsius(?![A-Za-z])|"
    r"(?:\^\\circ|\^\{\\circ\})\s*(?:\\mathrm\{C\}|C)|"
    rf"\\mathrm\{{(?:{UNIT_WORDS})\}}"
    r")"
)
_MATH_SPAN_ANY_RE = re.compile(r"(?<!\\)\$(?:\\.|[^$])+\$|\\\[(?:\\.|[^\]])+\\\]")
_VERBATIM_NAME_RE = re.compile(r"\\(begin|end)\{(verbatim|lstlisting|minted)\*?\}")
_TIKZ_NAME_RE = re.compile(r"\\(begin|end)\{tikzpicture\}")
_TIKZ_LINE_RE = re.compile(r"\\(?:draw|node|coordinate|path|fill|tikzset|tikz)\b")
_TABULAR_EDGE_RE = re.compile(r"\\(begin|end)\{tabular\*?\}")
_LONGTABLE_EDGE_RE = re.compile(r"\\(begin|end)\{longtable\*?\}")
_SIDEWAYS_EDGE_RE = re.compile(r"\\(begin|end)\{sidewaystable\*?\}")
_UNCLEAR_COL_RE = re.compile(r"\\(?:multicolumn|multirow)\b")
_NUMERIC_CELL_RE = re.compile(
    r"-?(?:\d+(?:\\,\d+)*)(?:\.\d+(?:\\,\d+)*)?(?:(?:~|\\,|\s)*(?:\\%|%|℃))?$"
)

# ── E-UNITFONT：数学环境内单位斜体（style-zh §6.2） ────────────────────────
MATH_SPAN_RE = re.compile(r"\$[^$]+\$")
UPRIGHT_WRAPPERS = ("\\mathrm", "\\text", "\\si", "\\unit", "\\operatorname")
MATH_UNIT_RE = re.compile(rf"(?<![A-Za-z\\])({UNIT_WORDS})(?![A-Za-z])")

# ── E-NUMSTYLE：概数与序数用字（style-zh §6.1） ────────────────────────────
APPROX_NUM_RE = re.compile(r"(?<![A-Za-z])(\d+)\s*(?=[几多余])")
ORDINAL_LATIN_RE = re.compile(r"\b(\d+)(?:st|nd|rd|th)\b")
# 图/表/式/章/节/参考文献编号是编号不是概数，排除。
NUMBERING_PREFIX_RE = re.compile(r"[图表式章节条页卷册第]\s*$")

# ── E-LONGSENT：单句可读性长度 ─────────────────────────────────────────────
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？；])")
ENUM_ITEM_RE = re.compile(r"^\s*(?:[（(]\s*\d{1,2}\s*[)）]|\d{1,2}[.、]|[-*•]|\\item)")

SEVERITY_ORDER = {"Error": 0, "Warning": 1, "Info": 2}


@dataclass
class Finding:
    code: str
    tier: str
    loc: str
    severity: str
    priority: str
    title: str
    original: str
    suggestion: str = ""
    candidate: str = ""
    basis: str = ""
    changed: str = "none"
    protected: str = "none"
    risk_flags: str = "not-assessed"


@dataclass
class StyleResult:
    entry: str
    goal: str
    strength: str
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    routed_to: str = ""


def _is_skippable(raw: str) -> bool:
    """跳过公式行、表格行、列举项与代码/引文环境行。"""
    stripped = raw.strip()
    if not stripped or stripped.startswith("%"):
        return True
    if ENUM_ITEM_RE.match(stripped):
        return True
    if "&" in stripped and "\\\\" in stripped:  # 表格行
        return True
    if re.match(r"^\\(?:begin|end)\{", stripped):
        return True
    return bool(re.match(r"^\\(?:documentclass|usepackage|input|include|bibliography)", stripped))


def _ascii_islands(text: str) -> list[tuple[int, int]]:
    """行内英文片段与全英文括号的区间——§5.2/§5.3 的两条标点豁免区。"""
    spans = [(m.start(), m.end()) for m in ASCII_RUN_RE.finditer(text)]
    spans += [(m.start(), m.end()) for m in URL_LIKE_RE.finditer(text)]
    for m in PAREN_ALL_ASCII_RE.finditer(text):
        if not CJK_RE.search(m.group(0)):
            spans.append((m.start(), m.end()))
    return spans


def _in_spans(index: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in spans)


class ChineseStyleChecker:
    """九个 E-* 检查器：A 档给替换建议，B 档只报候选（见模块文档的分档表）。"""

    def __init__(
        self,
        entry: Path,
        max_chars: int = DEFAULT_MAX_CHARS,
        degree_wording: bool = False,
        school: str = "generic",
    ) -> None:
        self.entry = Path(entry)
        self.max_chars = max_chars
        self.degree_wording = degree_wording
        self.school = school

    def analyze(
        self,
        section: str | None = None,
        goal: str = "grammar",
        strength: str = "minimal",
    ) -> StyleResult:
        doc = assemble(self.entry)
        parser = get_parser(self.entry)
        result = StyleResult(entry=str(self.entry), goal=goal, strength=strength)
        result.warnings = list(doc.warnings)

        if goal in UNSUPPORTED_GOALS:
            result.routed_to = UNSUPPORTED_GOALS[goal]
            return result

        lines = doc.lines
        sections = parser.split_sections(doc.content)
        if section:
            matched, available = resolve_section_keys(section, sections)
            if not matched:
                result.warnings.append(
                    f"未找到章节: {section}；可用: "
                    f"{'、'.join(available) if available else '(未识别到章节)'}"
                )
                return result
            ranges = [sections[key] for key in matched]
        else:
            ranges = list(sections.values()) if sections else [(1, len(lines))]

        for start, end in ranges:
            for line_no in range(start, min(end, len(lines)) + 1):
                raw = lines[line_no - 1]
                loc = doc.lineref(line_no)
                self._check_math_units(raw, loc, result)
                if _is_skippable(raw):
                    continue
                visible = parser.extract_visible_text(raw).strip()
                if not visible or not CJK_RE.search(visible):
                    continue
                self._check_colloquial(visible, loc, result)
                self._check_absolute(visible, loc, result)
                if self.degree_wording:
                    self._check_degree(visible, loc, result)
                self._check_collocation(visible, loc, result)
                self._check_incomplete(visible, loc, result)
                self._check_punctuation(visible, loc, result)
                self._check_number_unit_space(visible, loc, result)
                self._check_number_style(visible, loc, result)
                self._check_long_sentence(visible, loc, result)

        if self.school == _COLLEGE_SCHOOL:
            self._check_college_numbers(lines, ranges, doc, result)

        result.findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.loc, f.code))
        return result

    # ── A 档 ────────────────────────────────────────────────────────────────

    def _check_colloquial(self, text: str, loc: str, result: StyleResult) -> None:
        for term, replacement in COLLOQ_MAP.items():
            if term not in text:
                continue
            if any(exc in text for exc in COLLOQ_EXCLUDE.get(term, ())):
                continue
            result.findings.append(
                Finding(
                    code="E-COLLOQ",
                    tier="auto",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="口语化程度副词",
                    original=text,
                    suggestion=f"「{term}」宜改为「{replacement}」",
                    basis="academic-style-zh.md §1.1（口语化表达纠正）",
                    changed=f"1 lexical substitution ({term} -> {replacement.split('、')[0]})",
                    risk_flags="lexical-substitution",
                )
            )

    def _check_collocation(self, text: str, loc: str, result: StyleResult) -> None:
        for wrong, right, obj in COLLOC_ERRORS:
            pattern = re.compile(rf"{wrong}((?:了|过)?[^，。；！？]{{0,6}}?{obj})")
            match = pattern.search(text)
            if not match:
                continue
            hit = match.group(0)
            fixed = right + match.group(1)
            result.findings.append(
                Finding(
                    code="E-COLLOC",
                    tier="auto",
                    loc=loc,
                    severity="Warning",
                    priority="P2",
                    title="搭配不当",
                    original=text,
                    suggestion=text.replace(hit, fixed, 1),
                    basis=f"academic-style-zh.md §4.1（{wrong}{obj} → {right}{obj}）",
                    changed=f"1 collocation fix ({hit} -> {fixed})",
                    risk_flags="lexical-substitution",
                )
            )

    def _check_number_unit_space(self, text: str, loc: str, result: StyleResult) -> None:
        for match in NUM_UNIT_NOSPACE_RE.finditer(text):
            number, unit = match.group(1), match.group(2)
            result.findings.append(
                Finding(
                    code="E-NUMSPACE",
                    tier="auto",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="数值与单位之间缺空格",
                    original=text,
                    suggestion=text.replace(f"{number}{unit}", f"{number}\\,{unit}", 1),
                    basis=(
                        "academic-style-zh.md §6.2；GB 3100 系列。"
                        f"百分号/角度/摄氏度（{'、'.join(UNIT_NO_SPACE[:3])}）按国标不空格，不在此列"
                    ),
                    changed=f"1 spacing fix ({number}{unit} -> {number}\\,{unit})",
                    risk_flags="whitespace-normalized",
                )
            )

    # ── B 档：只报候选，不给可直接套用的替换文本 ──────────────────────────

    def _absolute_term_active(self, text: str, term: str) -> bool:
        if term != "绝对" or not self.degree_wording:
            return term in text
        covered: list[tuple[int, int]] = []
        for phrase in LEGAL_ABSOLUTE_COLLOCATIONS:
            start = 0
            while True:
                index = text.find(phrase, start)
                if index < 0:
                    break
                covered.append((index, index + len("绝对")))
                start = index + len(phrase)
        start = 0
        while True:
            index = text.find(term, start)
            if index < 0:
                return False
            if not any(span_start <= index < span_end for span_start, span_end in covered):
                return True
            start = index + len(term)
        return False

    def _check_absolute(self, text: str, loc: str, result: StyleResult) -> None:
        if CITATION_CONTEXT_RE.search(text):
            return
        for term, replacement in ABSOLUTE_TERMS.items():
            if not self._absolute_term_active(text, term):
                continue
            result.findings.append(
                Finding(
                    code="E-ABSOLUTE",
                    tier="candidate",
                    loc=loc,
                    severity="Warning",
                    priority="P2",
                    title="绝对化词汇",
                    original=text,
                    candidate=(
                        f"「{term}」是绝对化措辞，可考虑「{replacement}」；"
                        "是否降级取决于该论断本身的证据强度，请人工判断"
                    ),
                    basis=(
                        "academic-style-zh.md §2（绝对化词汇规避）；"
                        "论断强度分级见 ../writing/over-claim-guard.md，本模块只做词汇层建议"
                    ),
                )
            )

    def _check_degree(self, text: str, loc: str, result: StyleResult) -> None:
        """Opt-in degree-word candidates. No full-sentence replacement."""
        if CITATION_CONTEXT_RE.search(text):
            return
        complete_already_reported = "完全" in text
        for phrase in DEGREE_PHRASES:
            start = 0
            while True:
                index = text.find(phrase, start)
                if index < 0:
                    break
                start = index + len(phrase)
                if phrase == "完全忽略" and complete_already_reported:
                    continue
                result.findings.append(
                    Finding(
                        code="E-DEGREE",
                        tier="candidate",
                        loc=loc,
                        severity="Info",
                        priority="P3",
                        title="程度词",
                        original=phrase,
                        candidate=f"「{phrase}」是程度词候选，需人工判断；不提供整句替换",
                        basis="academic-style-zh.md 程度词（--degree-wording）",
                    )
                )

    def _check_incomplete(self, text: str, loc: str, result: StyleResult) -> None:
        for sentence in (s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()):
            if not INCOMP_LEAD_RE.match(sentence):
                continue
            if any(marker in sentence for marker in SUBJECT_MARKERS):
                continue
            result.findings.append(
                Finding(
                    code="E-INCOMP",
                    tier="candidate",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="疑似成分残缺",
                    original=sentence,
                    candidate=(
                        "「通过/经过/利用…，<动词>了…」句式疑似缺主语；"
                        "中文承前省略主语亦合法，请人工判断"
                    ),
                    basis="academic-style-zh.md §4.2（成分残缺）",
                )
            )

    def _check_punctuation(self, text: str, loc: str, result: StyleResult) -> None:
        if not CJK_RE.search(text):
            return
        islands = _ascii_islands(text)
        hits = [
            match.group(0)
            for match in ASCII_PUNCT_RE.finditer(text)
            if not _in_spans(match.start(), islands)
        ]
        if not hits:
            return
        result.findings.append(
            Finding(
                code="E-PUNCT",
                tier="candidate",
                loc=loc,
                severity="Info",
                priority="P3",
                title="中英标点混用",
                original=text,
                candidate=(
                    f"中文语境中出现英文标点 {'、'.join(sorted(set(hits)))}；"
                    "英文术语后与全英文括号内允许英文标点（§5.2/§5.3），请人工确认是否属豁免"
                ),
                basis="academic-style-zh.md §5.3（混用规则）；GB/T 15834",
            )
        )

    def _check_number_style(self, text: str, loc: str, result: StyleResult) -> None:
        for match in APPROX_NUM_RE.finditer(text):
            if NUMBERING_PREFIX_RE.search(text[: match.start()]):
                continue
            result.findings.append(
                Finding(
                    code="E-NUMSTYLE",
                    tier="candidate",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="概数宜用汉字",
                    original=text,
                    candidate=(
                        f"「{match.group(1)}」后接概数词，按 GB/T 15835 概数宜用汉字"
                        "（如「数十」「几百」）；若确为精确值则忽略"
                    ),
                    basis=(
                        "academic-style-zh.md §6.1；GB/T 15835。"
                        "模板专属数字规范终检见 spec-check 的 YS-36，勿重复报告"
                    ),
                )
            )
        for match in ORDINAL_LATIN_RE.finditer(text):
            result.findings.append(
                Finding(
                    code="E-NUMSTYLE",
                    tier="candidate",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="序数宜用中文",
                    original=text,
                    candidate=f"「{match.group(0)}」宜写作「第{match.group(1)}」",
                    basis="academic-style-zh.md §6.1；GB/T 15835",
                )
            )

    def _check_long_sentence(self, text: str, loc: str, result: StyleResult) -> None:
        for sentence in (s.strip() for s in SENTENCE_SPLIT_RE.split(text) if s.strip()):
            length = len(CJK_RE.findall(sentence)) + len(re.findall(r"[A-Za-z0-9]+", sentence))
            if length <= self.max_chars:
                continue
            result.findings.append(
                Finding(
                    code="E-LONGSENT",
                    tier="candidate",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title=f"单句过长（约 {length} 字）",
                    original=sentence,
                    candidate=(
                        f"单句长度超过 {self.max_chars} 字，建议按语义拆分；"
                        "拆句属结构性编辑，需 --strength moderate 及以上才可应用"
                    ),
                    basis="可读性判据（非 AI 痕迹）；句长均匀度 CV 见 deai 模块 D1，两者不重复报告",
                )
            )

    def _check_math_units(self, raw: str, loc: str, result: StyleResult) -> None:
        """E-UNITFONT：只读数学环境、只报告、永不给替换文本（红线一）。"""
        for span in MATH_SPAN_RE.finditer(raw):
            body = span.group(0)
            if any(wrapper in body for wrapper in UPRIGHT_WRAPPERS):
                continue
            units = MATH_UNIT_RE.findall(body)
            if not units:
                continue
            result.findings.append(
                Finding(
                    code="E-UNITFONT",
                    tier="candidate",
                    loc=loc,
                    severity="Info",
                    priority="P3",
                    title="数学环境内单位疑似斜体",
                    original=body,
                    candidate=(
                        f"单位 {'、'.join(sorted(set(units)))} 位于数学环境内且未加正体包裹"
                        "（\\mathrm/\\text/\\si）。红线一禁止本工具修改数学环境，"
                        "需作者手动调整；本条永不给替换文本"
                    ),
                    basis="academic-style-zh.md §6.2（单位用正体）；GB/T 3101",
                )
            )

    def _check_college_numbers(self, lines: list[str], ranges, doc, result: StyleResult) -> None:
        """Opt-in college number spacing and grouping. Candidates only; no math rewrite."""
        verbatim = 0
        tikz = 0
        seen: set[tuple[str, str, str]] = set()
        tab_depth = 0
        tab_buf: list[tuple[int, str]] = []
        tab_complex = False
        long_depth = 0
        side_depth = 0
        for start, end in ranges:
            for line_no in range(start, min(end, len(lines)) + 1):
                raw = lines[line_no - 1]
                verbatim, tikz, prose_skip = _college_line_state(raw, verbatim, tikz)
                if verbatim or tikz:
                    continue
                visible = _strip_college_comment(raw)
                long_b, long_e = _env_counts(visible, _LONGTABLE_EDGE_RE)
                side_b, side_e = _env_counts(visible, _SIDEWAYS_EDGE_RE)
                if long_depth == 0 and long_b:
                    self._college_table_gap(doc, line_no, "longtable", result, seen)
                if side_depth == 0 and side_b:
                    self._college_table_gap(doc, line_no, "sidewaystable", result, seen)
                long_depth = max(0, long_depth + long_b - long_e)
                side_depth = max(0, side_depth + side_b - side_e)
                if long_depth or side_depth or long_b or long_e or side_b or side_e:
                    continue
                tab_b, tab_e = _env_counts(visible, _TABULAR_EDGE_RE)
                if tab_depth or tab_b:
                    if tab_depth and tab_b:
                        tab_complex = True
                    if _UNCLEAR_COL_RE.search(visible):
                        tab_complex = True
                    tab_buf.append((line_no, visible))
                    tab_depth = max(0, tab_depth + tab_b - tab_e)
                    if tab_depth == 0:
                        self._finish_college_tabular(tab_buf, tab_complex, doc, result, seen)
                        tab_buf = []
                        tab_complex = False
                    continue
                if prose_skip:
                    continue
                masked = _mask_college_line(raw)
                if not masked.strip():
                    continue
                loc = doc.lineref(line_no)
                math_at = _math_indexes(masked)
                self._college_spacing(masked, math_at, loc, result, seen)
                self._college_grouping(masked, math_at, loc, result, seen)
        if tab_buf:
            self._college_table_gap(doc, tab_buf[0][0], "unclosed", result, seen)

    def _finish_college_tabular(
        self,
        buf: list[tuple[int, str]],
        complex_table: bool,
        doc,
        result: StyleResult,
        seen: set,
    ) -> None:
        if complex_table:
            self._college_table_gap(doc, buf[0][0], "unclear", result, seen)
            return
        for line_no, text in buf:
            cleaned = _strip_table_structure(text)
            if not cleaned.strip():
                continue
            loc = doc.lineref(line_no)
            for cell in _split_cells(_mask_college_line(cleaned)):
                if not cell.strip():
                    continue
                math_at = _math_indexes(cell)
                self._college_spacing(cell, math_at, loc, result, seen)
                self._college_grouping(
                    cell,
                    math_at,
                    loc,
                    result,
                    seen,
                    force_quantity=_numeric_cell(cell),
                )

    def _college_table_gap(
        self, doc, line_no: int, kind: str, result: StyleResult, seen: set
    ) -> None:
        messages = {
            "longtable": "longtable 不做单元格数字扫描，列覆盖不足。这不是确定违规，也不作为通过。",
            "sidewaystable": (
                "sidewaystable 不做单元格数字扫描，列覆盖不足。这不是确定违规，也不作为通过。"
            ),
            "unclear": "multicolumn、multirow 或嵌套表列归属不明，不合并命中，不作为通过。",
            "unclosed": "表格环境未闭合，覆盖不足，不作为通过。",
        }
        token = kind if kind in {"longtable", "sidewaystable"} else "tabular"
        loc = doc.lineref(line_no)
        key = (loc, "NUM-COVERAGE", f"{token}:{kind}")
        if key in seen:
            return
        seen.add(key)
        result.findings.append(
            _college_finding(
                "NUM-COVERAGE",
                loc,
                token,
                messages[kind],
                title="表格数字未覆盖",
            )
        )

    def _college_spacing(self, text, math_at, loc, result: StyleResult, seen: set) -> None:
        for match in _COLLEGE_SPACE_RE.finditer(text):
            token = match.group(0)
            if _college_space_excluded(text, match.start(), match.end()):
                continue
            key = (loc, "NUM-SPACE", token)
            if key in seen:
                continue
            seen.add(key)
            in_math = match.start() in math_at
            result.findings.append(
                _college_finding(
                    "NUM-SPACE",
                    loc,
                    token,
                    "数值与 %、\\% 或 ℃ 之间缺间隔。平面角度分秒保持紧贴。"
                    "推荐源码间隔为 ~；已有空格或 \\, 等显式间隔不算违规。"
                    + ("只报告位置，不改写数学。" if in_math else "只报告该片段，不给整句替换。"),
                )
            )

    def _college_grouping(
        self,
        text,
        math_at,
        loc,
        result: StyleResult,
        seen: set,
        *,
        force_quantity: bool = False,
    ) -> None:
        for match in _COLLEGE_NUM_RE.finditer(text):
            sign, body = match.group(1), match.group(2)
            token = sign + body
            context = _college_number_context(text, match.start(), match.end(), token, body)
            if context == "skip":
                continue
            if context == "bare" and force_quantity:
                context = "quantity"
            in_math = match.start() in math_at
            if context == "quantity":
                if _college_groups_ok(body):
                    continue
                code = "NUM-GROUP"
                detail = (
                    "千分空应从小数点向两侧每 3 位分组。负号不计位数。"
                    "只报告该数值，不改写、不换算。"
                )
            else:
                digits = body.replace("\\,", "").replace(".", "")
                if "." in body or "\\," in body or len(digits) < 4:
                    continue
                code = "NUM-COVERAGE"
                detail = "未分类裸数字。这不是确定违规，也不构成学院豁免。"
            if in_math:
                detail += "只报告位置，不改写数学。"
            key = (loc, code, token)
            if key in seen:
                continue
            seen.add(key)
            result.findings.append(_college_finding(code, loc, token, detail))


def _college_finding(code: str, loc: str, token: str, detail: str, title: str = "") -> Finding:
    titles = {
        "NUM-SPACE": "数值与单位缺间隔",
        "NUM-GROUP": "千分空分组",
        "NUM-COVERAGE": "未分类裸数字",
    }
    return Finding(
        code=code,
        tier="candidate",
        loc=loc,
        severity="Info",
        priority="P3",
        title=title or titles[code],
        original=token,
        candidate=f"「{token}」{detail}",
        basis="学院 yanshan-ee-2025 源码体例；~ 与 \\, 的选择见 number-unit-guide-zh.md",
    )


def _college_line_state(raw: str, verbatim: int, tikz: int) -> tuple[int, int, bool]:
    stripped = raw.strip()
    was_verbatim = verbatim > 0
    was_tikz = tikz > 0
    opens_verbatim = False
    opens_tikz = False
    for kind, _name in _VERBATIM_NAME_RE.findall(raw):
        if kind == "begin":
            verbatim += 1
            opens_verbatim = True
        else:
            verbatim -= 1
    for match in _TIKZ_NAME_RE.finditer(raw):
        if match.group(1) == "begin":
            tikz += 1
            opens_tikz = True
        else:
            tikz -= 1
    verbatim = max(verbatim, 0)
    tikz = max(tikz, 0)
    skip = bool(
        not stripped
        or stripped.startswith("%")
        or was_verbatim
        or was_tikz
        or opens_verbatim
        or opens_tikz
        or _TIKZ_LINE_RE.search(stripped)
        or re.match(
            r"^\\(?:documentclass|usepackage|input|include|bibliography|"
            r"newcommand|renewcommand|def)\b",
            stripped,
        )
    )
    return verbatim, tikz, skip


def _strip_college_comment(raw: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", raw)


def _env_counts(text: str, pattern: re.Pattern[str]) -> tuple[int, int]:
    begins = 0
    ends = 0
    for match in pattern.finditer(text):
        if match.group(1) == "begin":
            begins += 1
        else:
            ends += 1
    return begins, ends


def _skip_braces(text: str, index: int) -> int:
    if index >= len(text) or text[index] != "{":
        return index
    depth = 0
    while index < len(text):
        if text[index] == "\\" and index + 1 < len(text):
            index += 2
            continue
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return index


def _strip_begin_tabular(line: str) -> str:
    match = re.search(r"\\begin\{tabular\*?\}", line)
    if not match:
        return line
    index = match.end()
    if index < len(line) and line[index] == "[":
        close = line.find("]", index)
        if close < 0:
            return line[: match.start()]
        index = close + 1
    groups = 0
    while groups < 2 and index < len(line):
        while index < len(line) and line[index].isspace():
            index += 1
        if index >= len(line) or line[index] != "{":
            break
        index = _skip_braces(line, index)
        groups += 1
    return line[: match.start()] + line[index:]


def _strip_table_structure(line: str) -> str:
    line = _strip_begin_tabular(line)
    line = re.sub(r"\\end\{tabular\*?\}", "", line)
    line = re.sub(r"\\(?:toprule|midrule|bottomrule|hline)\b(?:\[[^\]]*\])?", "", line)
    line = re.sub(r"\\(?:cline|cmidrule)(?:\[[^\]]*\])?\{[^{}]*\}", "", line)
    return re.sub(r"\\\\(?:\[[^\]]*\])?", "", line)


def _split_cells(text: str) -> list[str]:
    cells: list[str] = []
    start = 0
    for match in re.finditer(r"(?<!\\)&", text):
        cells.append(text[start : match.start()])
        start = match.end()
    cells.append(text[start:])
    return cells


def _numeric_cell(cell: str) -> bool:
    piece = cell.replace("$", "")
    piece = re.sub(r"\\(?:mathrm|textbf|text)\{([^{}]*)\}", r"\1", piece)
    return _NUMERIC_CELL_RE.fullmatch(piece.strip()) is not None


def _mask_college_line(raw: str) -> str:
    masked = re.sub(r"(?<!\\)%.*", lambda match: " " * len(match.group(0)), raw)

    def _blank(match: re.Match[str]) -> str:
        return " " * len(match.group(0))

    patterns = (
        r"\\(?:includegraphics|url|path)\*?(?:\[[^\]]*\])?\{[^{}]*\}",
        r"\\href\s*\{[^{}]*\}\s*\{[^{}]*\}",
        r"\\(?:resizebox|rule)\*?\s*\{[^{}]*\}\s*\{[^{}]*\}",
        r"\\(?:scalebox|hspace|vspace)\*?\s*\{[^{}]*\}",
        r"\\begin\{minipage\}(?:\[[^\]]*\])*\s*\{[^{}]*\}",
        r"\\(?:cite|citep|citet|ref|eqref|autoref|cref|Cref|pageref|label|tag)\*?"
        r"(?:\[[^\]]*\])?\{[^{}]*\}",
    )
    for pattern in patterns:
        masked = re.sub(pattern, _blank, masked)
    return masked


def _math_indexes(text: str) -> set[int]:
    indexes: set[int] = set()
    for match in _MATH_SPAN_ANY_RE.finditer(text):
        indexes.update(range(match.start(), match.end()))
    return indexes


def _college_space_excluded(text: str, start: int, _end: int) -> bool:
    prefix = text[max(0, start - 12) : start]
    return bool(re.search(r"[A-Za-z]-?$", prefix))


def _college_number_context(text: str, start: int, end: int, token: str, body: str) -> str:
    prefix = text[max(0, start - 16) : start]
    suffix = text[end : end + 32]
    if re.search(r"(?:编号|学号|序号|证号|工号|No\.?|ID)\s*[:：]?\s*$", prefix, re.I):
        return "skip"
    if re.search(r"[A-Za-z]-?$", prefix):
        return "skip"
    if suffix.startswith("年"):
        return "skip"
    if re.match(r":\d{2}", suffix) or re.match(r"[-/]\d{1,2}[-/]\d{1,2}", suffix):
        return "skip"
    if re.match(r"\s*(?:\\times|\\cdot)\s*10\b", suffix) or re.match(r"[eE][+-]?\d", suffix):
        return "skip"
    if re.match(r"10\.\d{4,}", body) and suffix.startswith("/"):
        return "skip"
    if re.search(r"doi\s*[:=]\s*$", prefix, re.I):
        return "skip"
    if _college_path_token(text, start, end):
        return "skip"
    if (
        re.match(r"[A-Za-z]", suffix)
        and not _UNIT_WORD_RE.match(suffix)
        and not suffix.startswith("\\")
    ):
        return "skip"
    if "." in body or "\\," in body or _college_unit_follows(suffix):
        return "quantity"
    return "bare"


def _college_path_token(text: str, start: int, end: int) -> bool:
    left = start
    while left > 0 and text[left - 1] not in " \t\n{}":
        left -= 1
    right = end
    while right < len(text) and text[right] not in " \t\n{}":
        right += 1
    token = text[left:right]
    if "/" in token or "\\\\" in token:
        return True
    return bool(re.search(r"\.(?:png|jpe?g|pdf|tex|eps|svg|csv|bib)\b", token, re.I))


def _college_unit_follows(suffix: str) -> bool:
    trimmed = re.sub(r"^(?:~|\\,|\\ |\\;|\\:|\s)+", "", suffix)
    if trimmed.startswith(("%", "\\%", "℃")):
        return True
    if trimmed.startswith("\\mathrm{"):
        return True
    return bool(_UNIT_WORD_RE.match(trimmed))


def _college_groups_ok(body: str) -> bool:
    integer, _, fraction = body.partition(".")
    if not _college_side_ok(integer, fractional=False):
        return False
    if fraction == "":
        return "." not in body
    return _college_side_ok(fraction, fractional=True)


def _college_side_ok(part: str, *, fractional: bool) -> bool:
    groups = part.split("\\,")
    if any(not group.isdigit() for group in groups):
        return False
    if len(groups) == 1:
        return len(groups[0]) <= 3
    if fractional:
        if not 1 <= len(groups[-1]) <= 3:
            return False
        return all(len(group) == 3 for group in groups[:-1])
    if not 1 <= len(groups[0]) <= 3:
        return False
    return all(len(group) == 3 for group in groups[1:])


def _contract_lines(finding: Finding) -> list[str]:
    return [
        f"% Changed:       {finding.changed}",
        f"% Protected:     {finding.protected}",
        "% Meaning-Check: NEEDS-LLM",
        f"% Risk-Flags:    {finding.risk_flags}",
    ]


def generate_report(result: StyleResult) -> str:
    lines = ["=" * 60, "中文表达检查（expression）", "=" * 60]
    lines.append(f"% CONTRACT [Script]: goal={result.goal} strength={result.strength}")
    for warning in result.warnings:
        lines.append(f"% WARN: {warning}")

    if result.routed_to:
        lines.append(
            f"% EXPRESSION [Severity: Info] [Priority: P3] [Script]: "
            f"本模块没有 {result.goal} 相关规则，请改用 `{result.routed_to}` 模块。"
        )
        lines.append("=" * 60)
        return "\n".join(lines)

    if not result.findings:
        lines.append("% EXPRESSION: 未发现规则级表达问题。")
    for finding in result.findings:
        lines.append("")
        lines.append(
            f"% EXPRESSION ({finding.loc}) [Severity: {finding.severity}] "
            f"[Priority: {finding.priority}] [Script]: {finding.code} {finding.title}"
        )
        lines.append(f"% 原文: {finding.original}")
        if finding.suggestion:
            lines.append(f"% 建议: {finding.suggestion}")
        if finding.candidate:
            lines.append(f"% 候选: {finding.candidate}")
        if finding.basis:
            lines.append(f"% 依据: {finding.basis}")
        lines.extend(_contract_lines(finding))

    lines.append("")
    lines.append("-" * 60)
    lines.append(
        "边界说明: 人称（我们/本文）走 abstract 的 T-VOICE / T-OPEN；论断强度分级走 "
        "over-claim-guard.md；模板专属数字规范终检走 spec-check 的 YS-36；句长均匀度（CV）"
        "走 deai 的 D1；段落顺序与论证走 logic。以上均不在本模块重复报告。"
    )
    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> int:
    cli = argparse.ArgumentParser(description="中文学位论文表达/语句级检查器（E-*）")
    cli.add_argument("tex_file", help="论文入口 .tex 文件（多文件工程传 main.tex）")
    cli.add_argument("--section", help="只检查某一章节（英文键或中文名）")
    cli.add_argument(
        "--goal",
        choices=GOAL_CHOICES,
        default="grammar",
        help="编辑目标：这次编辑要解决什么（默认 grammar）",
    )
    cli.add_argument(
        "--strength",
        choices=STRENGTH_CHOICES,
        default="minimal",
        help="编辑幅度：允许改到多深（默认 minimal）",
    )
    cli.add_argument(
        "--max-chars", type=int, default=DEFAULT_MAX_CHARS, help="单句长度阈值（默认 80 字）"
    )
    cli.add_argument("--json", "-j", action="store_true", help="以 JSON 输出")
    cli.add_argument(
        "--degree-wording",
        action="store_true",
        help="报告程度词候选，并按词位豁免合法绝对化搭配（默认关闭）",
    )
    cli.add_argument(
        "--school",
        choices=SCHOOL_CHOICES,
        default="generic",
        help="学院源码体例。仅 yanshan-ee-2025 启用数字/单位候选；默认 generic",
    )
    args = cli.parse_args()

    if not Path(args.tex_file).exists():
        print(f"[ERROR] 文件未找到: {args.tex_file}", file=sys.stderr)
        return 1

    checker = ChineseStyleChecker(
        Path(args.tex_file),
        max_chars=args.max_chars,
        degree_wording=args.degree_wording,
        school=args.school,
    )
    result = checker.analyze(args.section, args.goal, args.strength)

    if args.json:
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print(generate_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
