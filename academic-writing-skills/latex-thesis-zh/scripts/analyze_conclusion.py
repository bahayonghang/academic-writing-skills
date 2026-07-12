#!/usr/bin/env python3
"""
结论章内容检查器 — 中文学位论文版本

对结论/总结与展望章做章内内容结构诊断 + 结论↔中文摘要比对，检查项 CC-*
对应 research/conclusion-patterns.md 的 C-* 规律与 web 最佳实践（编号见各检查器
代码注释）。与 check_spec.py 的 check_conclusion_*（\\cite/字数/模糊措辞）零重复：
本脚本不查引用、字数上限、模糊措辞，报告尾注指路 spec-check。

Usage:
    uv run python -B analyze_conclusion.py main.tex
    uv run python -B analyze_conclusion.py main.tex --json
"""

import argparse
import difflib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

try:
    from parsers import extract_abstract, get_parser
    from tex_loader import assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import extract_abstract, get_parser
    from tex_loader import assemble


# ── 词表与正则（每条标注 research/web 溯源）─────────────────────

# C-LABEL：分条列表导语（创新/成果/结论/工作…如下）。5/5 均有一句“…如下：”。
SUMMARY_LABEL_RE = re.compile(
    r"(?:创新性?工作|研究成果|主要成果|主要结论|研究结论|所取得的成果|工作总结|"
    r"具体创新|贡献)[^。]{0,12}如下|总结如下|归纳如下|得出(?:如下|以下)结论"
)
# C-TRIAD 创新表述词表（web A3 校规：博士须体现创新点）。
INNOVATION_RE = re.compile(
    r"创新|首次|新方法|新见解|新颖|新型|独创|新的.{0,4}(?:方法|模型|机制|框架)"
)
# C-OPENING：承上式总述的研究链序词（5/5）。
OPENING_ORDINALS = ("首先", "其次", "然后", "再次", "接着", "最后")
# C-ENUM / C-OUTLOOK-COUNT：贡献/展望编号（1）（2）…（1~2 位数字，避开年份/篇数）。
ENUM_RE = re.compile(r"[（(]\s*\d{1,2}\s*[)）]")
# 展望区起点信号：优先“展望”，其次未来向过渡措辞（C-OUTLOOK-FUTURE-PHRASE 5/5）。
OUTLOOK_TRIGGER_RE = re.compile(r"下一步|未来|有待进一步|进一步.{0,4}研究|作出如下展望|展望如下")
# C-OUTLOOK-FUTURE-PHRASE：未来向措辞存在性（5/5）。
FUTURE_PHRASE_RE = re.compile(r"有待|未来|下一步|将是|尚需|值得.{0,6}研究|进一步")
# C-OUTLOOK-TRANS：展望前的局限/承接过渡句（5/5）。承接式（"作出如下展望"
# "对…下一步研究"）与局限式（"仍存在不足"）均计入——研究样本中纯承接无局限的
# 写法同样满足 C-OUTLOOK-TRANS（显式列局限仅 2/5，是加分项非必要项）。
OUTLOOK_TRANS_RE = re.compile(
    r"仍存在|仍有|仍然存在|仍需|不足|悬而未决|尚需|一定不足|问题.{0,4}值得"
    r"|作出如下展望|展望如下|下一步.{0,8}(?:研究|工作)|后续研究"
)
# C-OUTLOOK-SPEC 反例黑名单（web C6）：展望空话套话。维护节律对齐 deai 词表约定，
# 命中且同句无具体技术名词才报（见 TECH_TERM_RE）。8~15 条。
OUTLOOK_EMPTY_BLACKLIST = (
    "广阔前景",
    "前景广阔",
    "值得进一步研究",
    "有待深入",
    "有待进一步完善",
    "进一步完善",
    "继续深入研究",
    "不断完善",
    "任重道远",
    "仍需努力",
    "做出更大贡献",
    "更加完善",
    "深入探讨",
    "进一步探索",
    "更好地服务",
)
# 具体技术名词启发：命中任一即认为该句有实质技术内容，不判空话。
TECH_TERM_RE = re.compile(
    r"建模|优化|控制|算法|机理|部署|模型|网络|预测|估计|识别|调度|融合|数据|系统|"
    r"工艺|方法|框架|策略|传感|监测|诊断|调控|软测量|自适应|鲁棒"
)
ENGLISH_ABBR_RE = re.compile(r"[A-Z]{2,}")
# CC-QUANT：结论中的百分比/小数指标 token（避开年份/序号/整数章号）。
# 容忍 LaTeX 转义百分号 ``\%``；纯整数须带百分号才计入（否则误捕序号/年份/篇数）。
QUANT_RE = re.compile(r"\d+\.\d+\s*\\?[%％‰]?|\d+\s*\\?[%％‰]")
# 结论章内不应出现图表环境（C-NO-FIG 5/5）。
FIG_ENV_RE = re.compile(r"\\begin\{(figure|table|tabular)\*?\}")
# CC-SUBSEC：编号章标题风格（第X章 …）。
NUMBERED_CHAPTER_RE = re.compile(r"第\s*[一二三四五六七八九十百\d]+\s*章")

_SEVERITY_PRIORITY = {"Error": "P1", "Warning": "P2", "Info": "P3"}
_VERBATIM_MIN_LEN = 15  # 句长阈值：过短句易偶然雷同，不纳入比对
_VERBATIM_RATIO = 0.85  # difflib 相似度命中阈值
_VERBATIM_HIT_SHARE = 0.30  # 命中句占结论句比 -> Warning
_RATIO_LO, _RATIO_HI = 1.5, 4.0  # 总结:展望字符比合理区间（C-RATIO 约 2:1~3:1）


@dataclass
class Finding:
    code: str
    severity: str  # Error | Warning | Info
    loc: str
    message: str
    suggestion: str = ""
    reason: str = ""

    @property
    def priority(self) -> str:
        return _SEVERITY_PRIORITY[self.severity]


@dataclass
class LlmHint:
    code: str
    hint: str


@dataclass
class AnalysisResult:
    status: str
    file: str
    conclusion: dict | None = None
    findings: list[Finding] = field(default_factory=list)
    llm_lane: list[LlmHint] = field(default_factory=list)
    quant_notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    message: str = ""


def _char_count(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def _split_sentences_zh(text: str) -> list[str]:
    parts = re.split(r"([。！？；])", text)
    sentences: list[str] = []
    for i in range(0, len(parts), 2):
        seg = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
        seg = seg.strip()
        if seg:
            sentences.append(seg)
    return sentences


class ConclusionAnalyzer:
    """结论章内容诊断（CC-* 检查项，全部为只读诊断）。"""

    def __init__(self, tex_file: str):
        self.tex_file = Path(tex_file).resolve()

    # -- 装配与定位 ------------------------------------------------

    def analyze(self) -> AnalysisResult:
        if not self.tex_file.exists():
            return AnalysisResult(
                status="ERROR", file=str(self.tex_file), message=f"文件未找到: {self.tex_file}"
            )

        # assemble 同时处理单文件直读与多文件 \include 工程组装。
        self.doc = assemble(self.tex_file)
        self.parser = get_parser(self.tex_file)
        self.content = self.doc.content
        self.lines = self.doc.lines
        sections = self.parser.split_sections(self.content)

        rng = sections.get("conclusion")
        if rng is None:
            return AnalysisResult(
                status="SKIP",
                file=str(self.tex_file),
                warnings=list(self.doc.warnings),
                message=(
                    "未识别到结论/总结与展望章（split_sections 无 conclusion 键），"
                    "跳过结论内容检查。"
                ),
            )
        self.concl_start, self.concl_end = rng
        # 章/节标题行不算内容：从内容分析中排除，避免章标题“总结与展望”里的“展望”
        # 干扰展望边界判定与逐句查重。子节标题另经 extract_headings 单独用于展望边界。
        self._heading_lines = {h["line"] for h in self.parser.extract_headings(self.content)}
        title = self._conclusion_title()
        loc = self.doc.lineref(self.concl_start, self.concl_end)

        vlines = self._visible_lines(self.concl_start, self.concl_end)
        boundary = self._outlook_boundary_line(vlines)
        if boundary is None:
            summary_lines, outlook_lines = vlines, []
        else:
            summary_lines = [x for x in vlines if x[0] < boundary]
            outlook_lines = [x for x in vlines if x[0] >= boundary]

        findings: list[Finding] = []
        findings += self._check_triad(vlines, summary_lines, outlook_lines)
        findings += self._check_open(summary_lines, loc)
        findings += self._check_enum(summary_lines, loc)
        findings += self._check_outlook_empty(outlook_lines)
        findings += self._check_outlook_trans(summary_lines, outlook_lines)
        findings += self._check_outlook_count(outlook_lines, loc)
        findings += self._check_verbatim(vlines)
        findings += self._check_no_fig()
        findings += self._check_ratio(summary_lines, outlook_lines, loc)
        findings += self._check_subsec(title, loc)

        quant_notes = self._check_quant(vlines)

        status = self._overall(findings)
        return AnalysisResult(
            status=status,
            file=str(self.tex_file),
            conclusion={"loc": loc, "title": title},
            findings=findings,
            llm_lane=self._llm_lane(),
            quant_notes=quant_notes,
            warnings=list(self.doc.warnings),
        )

    def _conclusion_title(self) -> str:
        for h in self.parser.extract_headings(self.content):
            if h["line"] == self.concl_start:
                return h["title"]
        return "结论"

    def _visible_lines(self, start: int, end: int) -> list[tuple[int, str]]:
        out: list[tuple[int, str]] = []
        prefix = self.parser.get_comment_prefix()
        for line_no in range(start, min(end, len(self.lines)) + 1):
            if line_no in self._heading_lines:
                continue
            raw = self.lines[line_no - 1].strip()
            if not raw or raw.startswith(prefix):
                continue
            visible = self.parser.extract_visible_text(raw)
            if visible:
                out.append((line_no, visible))
        return out

    def _outlook_boundary_line(self, vlines: list[tuple[int, str]]) -> int | None:
        """展望区起始行：优先“展望”子节标题，其次正文“展望”，再次未来向过渡措辞。"""
        for h in self.parser.extract_headings(self.content):
            if (
                self.concl_start < h["line"] <= self.concl_end
                and h["level"] >= 2
                and "展望" in h["title"]
            ):
                return h["line"]
        for ln, txt in vlines:
            if "展望" in txt:
                return ln
        for ln, txt in vlines:
            if OUTLOOK_TRIGGER_RE.search(txt):
                return ln
        return None

    # -- 检查器（每个返回 Finding 列表）---------------------------

    def _check_triad(
        self,
        vlines: list[tuple[int, str]],
        summary_lines: list[tuple[int, str]],
        outlook_lines: list[tuple[int, str]],
    ) -> list[Finding]:
        """CC-TRIAD（web C1/C5·HIT；C-LABEL）：总结主体 + 创新表述 + 展望三要素齐全。

        缺展望/缺总结 -> Error；缺创新表述 -> Warning。
        """
        out: list[Finding] = []
        loc = self.doc.lineref(self.concl_start, self.concl_end)
        full_text = " ".join(t for _, t in vlines)
        summary_text = " ".join(t for _, t in summary_lines)
        summary_chars = _char_count(summary_text)
        has_summary = (
            bool(SUMMARY_LABEL_RE.search(summary_text))
            or bool(ENUM_RE.search(summary_text))
            or summary_chars >= 40
        )
        if not has_summary:
            out.append(
                Finding(
                    "CC-TRIAD",
                    "Error",
                    loc,
                    "结论缺少总结主体：未见“…如下：”导语、编号贡献条或实质总结正文。",
                    "先用承上式总述复述研究问题与研究链，再以“主要工作/成果如下：”引出分条总结。",
                    "结论三段式（总结主体 + 创新表述 + 展望）中总结主体是核心，缺失会被盲审直接质询。",
                )
            )
        if not outlook_lines:
            out.append(
                Finding(
                    "CC-TRIAD",
                    "Error",
                    loc,
                    "结论缺少展望：未见“展望”或“下一步/未来/有待进一步研究”等未来向段落。",
                    "在总结之后补一段展望，给出 2~3 条具体后续研究方向。",
                    "学位论文结论应以展望收口，指明研究的局限与后续可深入的技术方向。",
                )
            )
        if not INNOVATION_RE.search(full_text):
            out.append(
                Finding(
                    "CC-TRIAD",
                    "Warning",
                    loc,
                    "结论未见明确创新表述（创新/首次/新方法/新见解等）。",
                    "在分条总结中点明本文的创新性工作（如“提出了…的新方法”“首次实现了…”）。",
                    "校规要求博士论文结论体现创新点；仅罗列工作而不点明创新会削弱贡献感。",
                )
            )
        return out

    def _check_open(self, summary_lines: list[tuple[int, str]], loc: str) -> list[Finding]:
        """CC-OPEN（C-OPENING 5/5）：首段承上式总述用序词串起研究链，<2 个 -> Info。"""
        if not summary_lines:
            return []
        summary_text = " ".join(t for _, t in summary_lines)
        m = ENUM_RE.search(summary_text)
        opening = summary_text[: m.start()] if m else summary_text
        hits = sum(1 for w in OPENING_ORDINALS if w in opening)
        if hits >= 2:
            return []
        return [
            Finding(
                "CC-OPEN",
                "Info",
                self.doc.lineref(summary_lines[0][0]),
                f"结论开篇总述的研究链序词偏少（{hits} 个，如首先/其次/最后）。",
                "在开篇用“首先…其次…最后…”复述全文研究链，再引出分条总结。",
                "承上式总述能让结论衔接全文主线，是范文结论的通用开篇写法。",
            )
        ]

    def _check_enum(self, summary_lines: list[tuple[int, str]], loc: str) -> list[Finding]:
        """CC-ENUM（C-ENUM 5/5）：贡献编号（1）（2）…存在且条数 3~4；否则 Info。"""
        summary_text = " ".join(t for _, t in summary_lines)
        n = len(ENUM_RE.findall(summary_text))
        if n == 0:
            return [
                Finding(
                    "CC-ENUM",
                    "Info",
                    loc,
                    "结论总结部分未见编号贡献列举（（1）（2）…）。",
                    "将主要贡献按“技术贡献/章”组织为（1）（2）（3）编号条，通常 3~4 条。",
                    "编号列举是范文结论呈现贡献的通用形式，便于盲审逐条核对。",
                )
            ]
        if 3 <= n <= 4:
            return []
        return [
            Finding(
                "CC-ENUM",
                "Info",
                loc,
                f"结论编号贡献条数为 {n}，通常落在 3~4 条。",
                "按核心技术贡献合并/拆分为 3~4 条，每条对应一项方法或一章工作。",
                "范文结论贡献条多为 3~4 条（≈方法章数），过多过少可斟酌。",
            )
        ]

    def _check_outlook_empty(self, outlook_lines: list[tuple[int, str]]) -> list[Finding]:
        """CC-OUTLOOK-EMPTY（C-OUTLOOK-SPEC 5/5；web C6）：展望空话且同句无技术名词 -> Warning。

        另查未来向措辞存在性，缺失 -> Info。
        """
        if not outlook_lines:
            return []
        out: list[Finding] = []
        outlook_text = " ".join(t for _, t in outlook_lines)
        for line_no, txt in outlook_lines:
            for sent in _split_sentences_zh(txt):
                blk = next((b for b in OUTLOOK_EMPTY_BLACKLIST if b in sent), None)
                if not blk:
                    continue
                concrete = bool(TECH_TERM_RE.search(sent)) or bool(ENGLISH_ABBR_RE.search(sent))
                if not concrete:
                    out.append(
                        Finding(
                            "CC-OUTLOOK-EMPTY",
                            "Warning",
                            self.doc.lineref(line_no),
                            f"展望出现空话套话“{blk}”，同句未见具体技术方向。",
                            "把展望改写为具体技术方向（如“研究…的多尺度建模方法”“工程部署 PLC/DCS”）。",
                            "展望应是可落地的后续研究计划，空话会被视为凑字数。",
                        )
                    )
                    break
        if not FUTURE_PHRASE_RE.search(outlook_text):
            out.append(
                Finding(
                    "CC-OUTLOOK-EMPTY",
                    "Info",
                    self.doc.lineref(outlook_lines[0][0]),
                    "展望段未见明确未来向措辞（有待/未来/下一步/将是等）。",
                    "在展望条中用“未来可…”“下一步将…”“有待进一步研究…”等措辞明确后续计划。",
                    "未来向措辞是展望区别于总结的语气标志。",
                )
            )
        return out

    def _check_outlook_trans(
        self, summary_lines: list[tuple[int, str]], outlook_lines: list[tuple[int, str]]
    ) -> list[Finding]:
        """CC-OUTLOOK-TRANS（C-OUTLOOK-TRANS 5/5）：展望前有局限/承接过渡句，否则 Info。"""
        if not outlook_lines:
            return []
        # 窗口取总结末 6 行 + 展望首 2 行：PDF 抽取/手工换行的源码里过渡句常被
        # 硬换行拆到边界前数行（Gate B 粉磨篇实测 2 行窗口漏检"仍存在一定不足"）。
        window = summary_lines[-6:] + outlook_lines[:2]
        window_text = " ".join(t for _, t in window)
        if OUTLOOK_TRANS_RE.search(window_text):
            return []
        return [
            Finding(
                "CC-OUTLOOK-TRANS",
                "Info",
                self.doc.lineref(outlook_lines[0][0]),
                "展望前未见局限/承接过渡句（仍存在/仍有/不足/悬而未决/尚需等）。",
                "在转入展望前加一句承接，先承认本文局限（“…仍存在一定不足”）再对应展望方向。",
                "先局限后展望能让后续方向显得有的放矢，是范文的通用过渡写法。",
            )
        ]

    def _check_outlook_count(self, outlook_lines: list[tuple[int, str]], loc: str) -> list[Finding]:
        """CC-OUTLOOK-COUNT（C-OUTLOOK-COUNT 5/5）：展望条数 2~3，否则 Info。"""
        if not outlook_lines:
            return []
        outlook_text = " ".join(t for _, t in outlook_lines)
        n = len(ENUM_RE.findall(outlook_text))
        if n == 0 or 2 <= n <= 3:
            # 0 条可能是成段式展望，不强制编号，交给 CC-OUTLOOK-EMPTY 判空话。
            return []
        return [
            Finding(
                "CC-OUTLOOK-COUNT",
                "Info",
                self.doc.lineref(outlook_lines[0][0]),
                f"展望编号条数为 {n}，通常落在 2~3 条。",
                "将展望聚焦为 2~3 条具体方向，避免过度发散或仅一句带过。",
                "范文展望多为 2~3 条，每条一个可落地的技术方向。",
            )
        ]

    def _check_verbatim(self, vlines: list[tuple[int, str]]) -> list[Finding]:
        """CC-VERBATIM（C-NO-VERBATIM-ABS；web C4·HIT）：结论逐字复制中文摘要。

        逐句 difflib.SequenceMatcher，句长≥15 字才比，ratio≥0.85 记命中；
        命中句占结论句 ≥30% -> Warning，单句命中列 Info 明细。
        """
        abstract_text = extract_abstract(self.content)
        if not abstract_text.strip():
            return []
        abstract_sents = [
            s for s in _split_sentences_zh(abstract_text) if len(s) >= _VERBATIM_MIN_LEN
        ]
        if not abstract_sents:
            return []
        concl_text = " ".join(t for _, t in vlines)
        concl_sents = [s for s in _split_sentences_zh(concl_text) if len(s) >= _VERBATIM_MIN_LEN]
        if not concl_sents:
            return []

        hits: list[str] = []
        for cs in concl_sents:
            best = 0.0
            for as_ in abstract_sents:
                r = difflib.SequenceMatcher(None, cs, as_).ratio()
                if r > best:
                    best = r
            if best >= _VERBATIM_RATIO:
                hits.append(cs)

        if not hits:
            return []
        out: list[Finding] = []
        loc = self.doc.lineref(self.concl_start, self.concl_end)
        share = len(hits) / len(concl_sents)
        if share >= _VERBATIM_HIT_SHARE:
            out.append(
                Finding(
                    "CC-VERBATIM",
                    "Warning",
                    loc,
                    f"结论与中文摘要逐字重复度偏高：{len(hits)}/{len(concl_sents)} 句"
                    f"（约 {share:.0%}）近乎雷同。",
                    "结论应对摘要做改写复述（重组句式、补足“首先/其次”连接词），而非整段照抄。",
                    "结论≠摘要：逐字复制摘要会被盲审视为凑篇幅，两者应各司其职。",
                )
            )
        for cs in hits[:5]:
            excerpt = cs if len(cs) <= 60 else cs[:57] + "..."
            out.append(
                Finding(
                    "CC-VERBATIM",
                    "Info",
                    loc,
                    f"疑似照抄摘要句：{excerpt}",
                    "改写该句或从结论删除，避免与摘要逐字重合。",
                    "",
                )
            )
        return out

    def _check_quant(self, vlines: list[tuple[int, str]]) -> list[str]:
        """CC-QUANT（C-QUANT-CONSIST）：结论数值应能在正文其他处找到；缺失出 NEEDS-LLM 软提示。

        结论无数值不报任何问题；不反向要求结论必须带数值（C-QUANT 仅 1/5）。
        """
        concl_text = " ".join(t for _, t in vlines)
        tokens = QUANT_RE.findall(concl_text)
        if not tokens:
            return []
        rest_parts: list[str] = []
        prefix = self.parser.get_comment_prefix()
        for i, line in enumerate(self.lines, 1):
            if self.concl_start <= i <= self.concl_end:
                continue
            s = line.strip()
            if not s or s.startswith(prefix):
                continue
            v = self.parser.extract_visible_text(s)
            if v:
                rest_parts.append(v)
        rest_text = " ".join(rest_parts)
        notes: list[str] = []
        seen: set[str] = set()
        for tok in tokens:
            core = re.sub(r"[^\d.]", "", tok)
            if not core or core in seen:
                continue
            seen.add(core)
            if core not in rest_text:
                notes.append(
                    f"NEEDS-LLM: 结论数值“{tok.strip()}”未在正文其他处找到，"
                    "请人工核对其与正文/摘要一致（数值可能在表格中，脚本不解析表内数字）。"
                )
        return notes

    def _check_no_fig(self) -> list[Finding]:
        """CC-NO-FIG（C-NO-FIG 5/5）：结论章内出现 figure/table 环境 -> Error。"""
        out: list[Finding] = []
        prefix = self.parser.get_comment_prefix()
        for line_no in range(self.concl_start, min(self.concl_end, len(self.lines)) + 1):
            raw = self.lines[line_no - 1]
            s = raw.strip()
            if not s or s.startswith(prefix):
                continue
            m = FIG_ENV_RE.search(re.sub(r"(?<!\\)%.*", "", raw))
            if m:
                out.append(
                    Finding(
                        "CC-NO-FIG",
                        "Error",
                        self.doc.lineref(line_no),
                        f"结论章内出现图表环境（{m.group(1)}）。",
                        "将图表移回对应正文章；结论如需重述关键结果，用文字复述已有图表数据即可。",
                        "结论不应引入新图表：图表属于正文，结论只做归纳与展望。",
                    )
                )
        return out

    def _check_ratio(
        self,
        summary_lines: list[tuple[int, str]],
        outlook_lines: list[tuple[int, str]],
        loc: str,
    ) -> list[Finding]:
        """CC-RATIO（C-RATIO 5/5）：总结:展望字符比在 1.5:1~4:1 外 -> Info。"""
        if not outlook_lines or not summary_lines:
            return []
        s_chars = _char_count(" ".join(t for _, t in summary_lines))
        o_chars = _char_count(" ".join(t for _, t in outlook_lines))
        if o_chars == 0:
            return []
        ratio = s_chars / o_chars
        if _RATIO_LO <= ratio <= _RATIO_HI:
            return []
        return [
            Finding(
                "CC-RATIO",
                "Info",
                loc,
                f"总结:展望字符比约 {ratio:.1f}:1（总结 {s_chars} 字 / 展望 {o_chars} 字），"
                f"通常落在 {_RATIO_LO:g}:1~{_RATIO_HI:g}:1。",
                "总结篇幅应明显大于展望（约 2:1~3:1）；比例失衡时可增删相应部分。",
                "范文结论总结详于展望，展望过长会喧宾夺主，过短则收口无力。",
            )
        ]

    def _check_subsec(self, title: str, loc: str) -> list[Finding]:
        """CC-SUBSEC（C-SUBSEC/C-NUM）：检测到子节号或编号章风格时只出 Info，不判对错。"""
        has_subsec = any(
            self.concl_start < h["line"] <= self.concl_end and h["level"] >= 2
            for h in self.parser.extract_headings(self.content)
        )
        numbered = bool(NUMBERED_CHAPTER_RE.search(title))
        if not has_subsec and not numbered:
            return []
        forms = []
        if numbered:
            forms.append("编号章（第X章）")
        if has_subsec:
            forms.append("子节号（如 X.1 总结 / X.2 展望）")
        return [
            Finding(
                "CC-SUBSEC",
                "Info",
                loc,
                f"结论章采用{'、'.join(forms)}风格。",
                "无需修改——与全文章节编号/分节风格保持一致即可（扁平结构与带子节均为合法体例）。",
                "范文中编号章 3/5、结论内设子节 1/5，两种体例皆可，只需与全文统一。",
            )
        ]

    def _llm_lane(self) -> list[LlmHint]:
        """[LLM] lane：脚本不判定，仅在报告输出结构化提示词要点。"""
        return [
            LlmHint(
                "CC-SKELETON",
                "逐条核对贡献条是否遵循“针对…问题，提出/建立/设计了…，(通过…)实验/应用表明/"
                "验证了…”骨架；缺“问题导向开头”或“验证收口”的条目请指出并给出改写。",
            ),
            LlmHint(
                "CC-NEW-CONCEPT",
                "核对结论出现的方法名/概念是否均在正文各章已定义；若结论首次引入正文未见的"
                "新方法名/新概念，标记为需回正文补充定义或从结论移除。",
            ),
        ]

    @staticmethod
    def _overall(findings: list[Finding]) -> str:
        sevs = {f.severity for f in findings}
        if "Error" in sevs:
            return "FAIL"
        if "Warning" in sevs:
            return "WARNING"
        if "Info" in sevs:
            return "INFO"
        return "PASS"

    # -- 报告 ------------------------------------------------------

    def generate_report(self, result: AnalysisResult) -> str:
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("结论章内容检查 (Conclusion Content Check)")
        lines.append("=" * 60)
        lines.append(f"入口文件: {result.file}")

        if result.status == "ERROR":
            lines.append(f"错误: {result.message}")
            lines.append("=" * 60)
            return "\n".join(lines)
        if result.status == "SKIP":
            lines.append("状态: SKIP")
            lines.append(result.message)
            for w in result.warnings:
                lines.append(f"% WARN: {w}")
            lines.append("=" * 60)
            return "\n".join(lines)

        concl = result.conclusion or {}
        lines.append(f"结论章: {concl.get('loc', '')} 「{concl.get('title', '')}」")
        counts = {
            s: sum(1 for f in result.findings if f.severity == s)
            for s in ("Error", "Warning", "Info")
        }
        lines.append(
            "统计: " + " · ".join(f"{k} {v}" for k, v in counts.items() if v)
            if any(counts.values())
            else "统计: 未发现规则级问题"
        )
        for w in result.warnings:
            lines.append(f"% WARN: {w}")

        if result.findings:
            lines.append("")
            lines.append("-" * 60)
            lines.append("[检查发现]（[Script] 自动判定，供人工复核）")
            for f in result.findings:
                lines.append(
                    f"% 结论章（{f.loc}）[Severity: {f.severity}] [Priority: {f.priority}]: "
                    f"[Script] {f.code} {f.message}"
                )
                if f.suggestion:
                    lines.append(f"% 建议：{f.suggestion}")
                if f.reason:
                    lines.append(f"% 理由：{f.reason}")
                lines.append("")

        if result.quant_notes:
            lines.append("-" * 60)
            lines.append("[CC-QUANT] 数值一致性（软提示，非硬报）:")
            for note in result.quant_notes:
                lines.append(f"- {note}")
            lines.append("")

        if result.llm_lane:
            lines.append("-" * 60)
            lines.append("[LLM lane] 需 agent 判读（脚本不判定）:")
            for h in result.llm_lane:
                lines.append(f"- {h.code}: {h.hint}")
            lines.append("")

        lines.append("-" * 60)
        lines.append(
            "边界说明: 结论禁 \\cite、字数上限、模糊措辞由 spec-check 承担"
            "（references/modules/spec-check.md，勿在此重复报告）；过度声明见 over-claim-guard.md；"
            "英文摘要时态见 deai 模块。"
        )
        lines.append("=" * 60)
        return "\n".join(lines)


def _result_to_json(result: AnalysisResult) -> dict:
    payload = asdict(result)
    payload["findings"] = [{**asdict(f), "priority": f.priority} for f in result.findings]
    return payload


def main() -> int:
    cli = argparse.ArgumentParser(description="中文学位论文结论章内容检查器（CC-*）")
    cli.add_argument("tex_file", help="论文入口 .tex 文件（多文件工程传 main.tex）")
    cli.add_argument("--json", "-j", action="store_true", help="以 JSON 输出")
    args = cli.parse_args()

    if not Path(args.tex_file).exists():
        print(f"[ERROR] 文件未找到: {args.tex_file}", file=sys.stderr)
        return 1

    analyzer = ConclusionAnalyzer(args.tex_file)
    result = analyzer.analyze()

    if args.json:
        print(json.dumps(_result_to_json(result), indent=2, ensure_ascii=False))
    else:
        print(analyzer.generate_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
