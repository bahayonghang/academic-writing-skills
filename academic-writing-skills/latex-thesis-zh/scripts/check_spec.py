#!/usr/bin/env python3
"""
Spec Compliance Final Check - 对照学校规范清单逐项终检

从 templates/<template>.md（或 --spec-file 自定义文件）的「## 逐项检查清单」表格
读取条目，逐项执行 script: 检查器，输出 PASS/FAIL/NEEDS-LLM/MODULE/MANUAL/SKIP
逐项报告。版式渲染类条目不做静态判定，归入打印前自查单。

Usage:
    uv run python check_spec.py main.tex --template yanshan --degree doctor
    uv run python check_spec.py main.tex --spec-file my-school.md --degree master
    uv run python check_spec.py main.tex --template yanshan --degree doctor --json
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

try:
    from parsers import LatexParser, extract_title, get_parser
    from tex_loader import assemble, read_text_robust
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import LatexParser, extract_title, get_parser
    from tex_loader import assemble, read_text_robust

# ── 清单解析 ─────────────────────────────────────────────────

CHECKLIST_HEADING = "## 逐项检查清单"
ITEM_ID_RE = re.compile(r"^[A-Z]{2,4}-\d{2,3}$")
METHOD_RE = re.compile(r"^(script:[a-z0-9_]+|module:[a-z-]+|llm|manual)$")
VALID_SCOPES = {"通用", "硕士", "博士"}


@dataclass
class ChecklistItem:
    id: str
    requirement: str
    basis: str
    method: str
    scope: str


@dataclass
class ItemResult:
    id: str
    requirement: str
    basis: str
    method: str
    scope: str
    status: str  # PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP
    evidence: str


def parse_checklist(md_path: Path) -> list[ChecklistItem]:
    """解析模板快照中「## 逐项检查清单」下第一个表格（容忍格式化 hook 的空格重排）。"""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == CHECKLIST_HEADING)
    except StopIteration:
        raise ValueError(f"{md_path.name}: 未找到「{CHECKLIST_HEADING}」段") from None

    items: list[ChecklistItem] = []
    in_table = False
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 5:
            raise ValueError(f"{md_path.name}: 清单行应为 5 列，得到 {len(cells)} 列: {stripped}")
        if cells[0] in ("ID", "---") or set(cells[0]) <= {"-", " "}:
            in_table = True
            continue
        in_table = True
        item = ChecklistItem(
            id=cells[0], requirement=cells[1], basis=cells[2], method=cells[3], scope=cells[4]
        )
        if not ITEM_ID_RE.match(item.id):
            raise ValueError(f"{md_path.name}: 非法条目 ID: {item.id}")
        if not METHOD_RE.match(item.method):
            raise ValueError(f"{md_path.name}: {item.id} 非法检查方式: {item.method}")
        if item.scope not in VALID_SCOPES:
            raise ValueError(f"{md_path.name}: {item.id} 非法适用范围: {item.scope}")
        items.append(item)

    if not items:
        raise ValueError(f"{md_path.name}: 「{CHECKLIST_HEADING}」下未解析到任何条目")
    dup = {i for i in [x.id for x in items] if [x.id for x in items].count(i) > 1}
    if dup:
        raise ValueError(f"{md_path.name}: 条目 ID 重复: {sorted(dup)}")
    return items


# ── 阈值（依据各校规范原文；无依据的模板不设阈值） ───────────
# Recognized keys (all optional; a missing key keeps the checker's built-in
# default behaviour, i.e. the pre-parameterization hardcoded values):
#   body / intro / abstract: (lo, hi) char ranges; bib_min: int floor;
#   title_max (default 25) / title_sub_max (default 35): title length caps;
#   kw_range (default (3, 8)): keyword count range;
#   kw_sep (default ";"): required keyword separator, ";" / "," / None (no rule).

TEMPLATE_THRESHOLDS: dict[str, dict[str, dict]] = {
    # 燕山大学 2024 版：正文/绪论字数 §2.1，摘要字数 §2.2，文献数量 §1.6。
    # 绪论(博士)规范原文为“1 万字左右”，取 ±40% 为可判区间。
    "yanshan": {
        "doctor": {
            "body": (60000, 100000),
            "intro": (6000, 14000),
            "abstract": (900, 1200),
            "bib_min": 100,
        },
        "master": {
            "body": (30000, 50000),
            "intro": (3000, 5000),
            "abstract": (500, 650),
            "bib_min": 40,
        },
    },
    # Tsinghua grad-school guide (2025-03 public copy): title strictly <= 25
    # chars (§2.3.1, no combined-subtitle clause -> subtitle counts into the
    # same cap), abstract 800~1000 for both degrees (§2.3.5). Keyword rule
    # "<= 5, no lower bound" (§2.3.5) has no decidable range -> checklist item
    # stays llm, so no kw_range here. No wordcount/intro/conclusion/bib rules
    # exist in the guide -> those keys must stay absent.
    "thuthesis": {
        "doctor": {"title_max": 25, "title_sub_max": 25, "abstract": (800, 1000)},
        "master": {"title_max": 25, "title_sub_max": 25, "abstract": (800, 1000)},
    },
    # PKU grad-school guide V2.0 (2014-05): title "generally" <= 20 chars
    # (§1.1; subtitle joined by a dash, no extra length allowance), keywords
    # 3~5 comma-separated (§1.3), doctoral abstract 800~1000 (§1.3). Master
    # abstract "about 600" has no official range -> checklist item stays llm,
    # so the master dict has no "abstract" key. No wordcount/intro/conclusion/
    # bib rules exist in the guide -> those keys must stay absent.
    "pkuthss": {
        "doctor": {
            "title_max": 20,
            "title_sub_max": 20,
            "kw_range": (3, 5),
            "kw_sep": ",",
            "abstract": (800, 1000),
        },
        "master": {"title_max": 20, "title_sub_max": 20, "kw_range": (3, 5), "kw_sep": ","},
    },
    # GB/T 7713.1-2006 (superseded by the 2025 edition since 2026-02-01;
    # school rules take precedence): title <= 20 chars (§5.1.1.2), keywords
    # 3~8 (§5.1.6, national default; no separator rule -> kw_sep None skips
    # the separator check). The national abstract length (200~300) conflicts
    # with common school-level rules -> no "abstract" key, the checker only
    # reports the measured count.
    "generic": {
        "doctor": {"title_max": 20, "title_sub_max": 20, "kw_sep": None},
        "master": {"title_max": 20, "title_sub_max": 20, "kw_sep": None},
    },
}

# module: 条目 → 建议命令（与 SKILL.md Module Router 主命令一致）
MODULE_COMMANDS = {
    "tables": "uv run python $SKILL_DIR/scripts/check_tables.py main.tex",
    "references": "uv run python $SKILL_DIR/scripts/check_references.py main.tex",
    # 2026-07-01 起可改用 --standard gb7714-2025 按新国标检查。
    "bibliography": "uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714",
    "consistency": "uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms",
    "format": "uv run python $SKILL_DIR/scripts/check_format.py main.tex",
}

FRONT_BACK_TITLE_RE = re.compile(
    r"摘要|abstract|目次|目录|符号|物理量|参考文献|致谢|谢辞|附录|成果|索引|声明|授权|简历"
    r"|denotation|acknowledg",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[一-鿿]")
HEDGE_RE = re.compile(r"大概|或许|可能是")
SUMMARY_TITLE_RE = re.compile(r"(本章)?小结$")
SUBTITLE_SEP_RE = re.compile(r"——|―|—|[:：]")


def _char_count(text: str) -> int:
    """近似字数口径：可见文本去空白后的字符数（含图表内文字与英文字母）。"""
    return len(re.sub(r"\s+", "", text))


# ── 文档上下文 ───────────────────────────────────────────────


class SpecContext:
    """一次性组装文档并预计算各检查器共用的中间结果。"""

    ABSTRACT_ENV_RE = re.compile(
        r"\\begin\{(cabstract|eabstract|enabstract|englishabstract|abstract\*|abstract)\}"
        r"(.*?)\\end\{\1\}",
        re.DOTALL,
    )

    def __init__(
        self,
        tex_file: Path,
        degree: str,
        template_id: str,
        bib_arg: Optional[str],
        ref_year: int,
        doc=None,
    ):
        self.tex_file = tex_file
        self.degree = degree
        self.template_id = template_id
        self.ref_year = ref_year
        self.doc = doc if doc is not None else assemble(tex_file)
        self.parser = get_parser(tex_file)
        self.content = self.doc.content
        self.lines = self.doc.lines
        self.sections = self.parser.split_sections(self.content)
        self.chapters = self.parser.chapter_ranges(self.content)
        self.thresholds: Optional[dict] = TEMPLATE_THRESHOLDS.get(template_id, {}).get(degree)
        self.bib_entries, self.bib_years, self.bib_note = self._load_bib(bib_arg)

    # -- 文本切片 --------------------------------------------------

    def range_visible(self, start: int, end: int) -> str:
        """区间 [start, end]（1-based，含端点）的可见文本。"""
        parts = []
        for i in range(max(start, 1), min(end, len(self.lines)) + 1):
            line = self.lines[i - 1]
            if line.strip().startswith("%"):
                continue
            parts.append(self.parser.extract_visible_text(line))
        return "\n".join(p for p in parts if p)

    def range_raw(self, start: int, end: int) -> list[tuple[int, str]]:
        """区间内 (行号, 原始行)，跳过注释行。"""
        out = []
        for i in range(max(start, 1), min(end, len(self.lines)) + 1):
            line = self.lines[i - 1]
            if line.strip().startswith("%"):
                continue
            out.append((i, re.sub(r"(?<!\\)%.*", "", line)))
        return out

    def body_chapters(self) -> list[dict]:
        return [
            ch
            for ch in self.chapters
            if not FRONT_BACK_TITLE_RE.search(LatexParser.normalize_heading_title(ch["title"]))
        ]

    def loc(self, line_no: int) -> str:
        return self.doc.lineref_en(line_no)

    # -- 摘要 / 关键词 ----------------------------------------------

    def abstract_spans(self) -> list[dict]:
        """全部摘要环境：{env, start_pos, text, is_zh}，按出现顺序。"""
        spans = []
        for m in self.ABSTRACT_ENV_RE.finditer(self.content):
            body = m.group(2)
            cjk = len(CJK_RE.findall(body))
            spans.append(
                {
                    "env": m.group(1),
                    "pos": m.start(),
                    "text": body,
                    "is_zh": m.group(1) == "cabstract" or cjk >= 10,
                }
            )
        return spans

    def keywords(self, lang: str) -> Optional[list[str]]:
        """提取关键词列表；找不到返回 None。lang: zh|en。"""
        if lang == "zh":
            patterns = [
                r"\\ckeywords\{([^{}]*)\}",
                r"(?<![\w*])keywords\s*=\s*\{([^{}]*)\}",
                r"keywordszh\s*=\s*\{([^{}]*)\}",
                r"\\keywords\{([^{}]*)\}",
            ]
            line_re = re.compile(r"关键词[:：](.+)")
        else:
            patterns = [
                r"\\ekeywords\{([^{}]*)\}",
                r"keywords\*\s*=\s*\{([^{}]*)\}",
                r"keywordsen\s*=\s*\{([^{}]*)\}",
            ]
            line_re = re.compile(r"key\s?words?\s*[:：](.+)", re.IGNORECASE)

        raw: Optional[str] = None
        for pat in patterns:
            m = re.search(pat, self.content)
            if m:
                raw = m.group(1)
                break
        if raw is None:
            for line in self.lines:
                if line.strip().startswith("%"):
                    continue
                m = line_re.search(self.parser.extract_visible_text(line))
                if m:
                    raw = m.group(1)
                    break
        if raw is None:
            return None
        parts = [p.strip() for p in re.split(r"[;；,，]", raw) if p.strip()]
        # 记录原始分隔符供 kw_count 判断分号要求
        self._kw_raw = raw
        return parts

    # -- 参考文献 ----------------------------------------------------

    def _load_bib(self, bib_arg: Optional[str]) -> tuple[Optional[int], list[int], str]:
        paths: list[Path] = []
        if bib_arg:
            paths = [Path(bib_arg)]
        else:
            for m in re.finditer(r"\\(?:bibliography|addbibresource)\{([^}]+)\}", self.content):
                for name in m.group(1).split(","):
                    name = name.strip()
                    if not name.endswith(".bib"):
                        name += ".bib"
                    cand = (self.tex_file.parent / name).resolve()
                    if cand.exists():
                        paths.append(cand)
        years: list[int] = []
        if paths:
            count = 0
            encoding_notes: list[str] = []
            for p in paths:
                try:
                    text, warning = read_text_robust(p)
                except OSError:
                    continue
                if warning:
                    encoding_notes.append(warning)
                starts = [
                    m
                    for m in re.finditer(r"@(\w+)\s*[{(]", text)
                    if m.group(1).lower() not in ("comment", "string", "preamble")
                ]
                count += len(starts)
                for i, m in enumerate(starts):
                    chunk = text[m.end() : starts[i + 1].start() if i + 1 < len(starts) else None]
                    ym = re.search(r"year\s*=\s*[{\"]?\s*(\d{4})", chunk)
                    if not ym:
                        ym = re.search(r"date\s*=\s*[{\"]?\s*(\d{4})", chunk)
                    if ym:
                        years.append(int(ym.group(1)))
            note = f"来源: {', '.join(p.name for p in paths)}"
            if encoding_notes:
                note += f"；编码提示: {'; '.join(encoding_notes)}"
            return count, years, note
        # thebibliography 环境兜底
        items = re.findall(
            r"\\bibitem(?:\[[^\]]*\])?\{[^}]*\}((?:.|\n)*?)(?=\\bibitem|\\end\{)", self.content
        )
        if items:
            for chunk in items:
                ym = re.search(r"(19|20)\d{2}", chunk)
                if ym:
                    years.append(int(ym.group(0)))
            return len(items), years, "来源: thebibliography 环境"
        return None, [], "未找到 .bib 文件或 thebibliography 环境"


# ── 检查器 ───────────────────────────────────────────────────
# 每个检查器返回 (status, evidence)。缺少可判定输入时返回 NEEDS-LLM 并说明缺什么。

CheckOutcome = tuple[str, str]
Checker = Callable[[SpecContext], CheckOutcome]


def _range_verdict(value: int, lo: int, hi: int, label: str) -> CheckOutcome:
    ev = f"{label}实测约 {value} 字（口径：可见文本去空白字符数）；规范区间 {lo}~{hi}"
    if lo <= value <= hi:
        return "PASS", ev
    if lo * 0.9 <= value <= hi * 1.1:
        return "NEEDS-LLM", ev + "（临界，规范用语为“一般”，请人工判断）"
    return "FAIL", ev


def check_title_len(ctx: SpecContext) -> CheckOutcome:
    title = extract_title(ctx.content)
    if not title:
        return "NEEDS-LLM", "未找到 \\title/\\ctitle，题名可能在封面模板中，请人工核对"
    n = _char_count(title)
    has_sub = bool(SUBTITLE_SEP_RE.search(title))
    th = ctx.thresholds or {}
    t_max = th.get("title_max", 25)
    sub_max = th.get("title_sub_max", 35)
    if n <= t_max:
        return "PASS", f"题名 {n} 字: {title}"
    if has_sub and n <= sub_max:
        return "PASS", f"含副题名合计 {n} 字（≤{sub_max}）: {title}"
    if has_sub:
        return "FAIL", f"含副题名合计 {n} 字 > {sub_max}: {title}"
    return "FAIL", f"题名 {n} 字 > {t_max} 且未见副题名结构: {title}"


def check_abstract_no_cite(ctx: SpecContext) -> CheckOutcome:
    spans = ctx.abstract_spans()
    if not spans:
        return "NEEDS-LLM", "未找到摘要环境（cabstract/abstract 等），请人工核对"
    problems, soft = [], []
    for span in spans:
        if re.search(r"\\cite\b", span["text"]):
            problems.append(f"{span['env']} 内出现 \\cite")
        if re.search(r"\\begin\{(figure|table|equation|align|gather)", span["text"]):
            problems.append(f"{span['env']} 内出现图表/公式环境")
        if re.search(r"(?<!\\)\$[^$]+\$", span["text"]):
            soft.append(f"{span['env']} 内出现行内数学")
    if problems:
        return "FAIL", "；".join(problems)
    if soft:
        return "NEEDS-LLM", "；".join(soft) + "（规范不宜使用公式，请确认必要性）"
    return "PASS", "摘要未见引用编号/图表/公式环境"


def check_kw_count(ctx: SpecContext) -> CheckOutcome:
    th = ctx.thresholds or {}
    lo, hi = th.get("kw_range", (3, 8))
    sep = th.get("kw_sep", ";")  # ";" / "," / None = no separator rule
    if sep == ",":
        sep_re, sep_name = r"[,，]", "逗号"
    elif sep is None:
        sep_re, sep_name = None, ""
    else:
        sep_re, sep_name = r"[;；]", "分号"
    hint = f"且{sep_name}分隔" if sep_re else ""
    kws = ctx.keywords("zh")
    if kws is None:
        return (
            "NEEDS-LLM",
            f"未找到中文关键词（可能使用封面自定义宏），请人工核对 {lo}~{hi} 个{hint}",
        )
    n = len(kws)
    raw = getattr(ctx, "_kw_raw", "")
    if sep_re and n > 1 and not re.search(sep_re, raw):
        return "FAIL", f"关键词 {n} 个，但未用{sep_name}分隔: {raw.strip()}"
    if lo <= n <= hi:
        return "PASS", f"关键词 {n} 个: {'；'.join(kws)}"
    return "FAIL", f"关键词 {n} 个（规范要求 {lo}~{hi} 个）: {'；'.join(kws)}"


def check_kw_zh_en_match(ctx: SpecContext) -> CheckOutcome:
    zh, en = ctx.keywords("zh"), ctx.keywords("en")
    if zh is None or en is None:
        missing = "中文" if zh is None else "英文"
        return "NEEDS-LLM", f"未找到{missing}关键词，请人工核对中英一一对应"
    if len(zh) == len(en):
        return "PASS", f"中英关键词各 {len(zh)} 个（逐条语义对应请人工确认）"
    return "FAIL", f"中文 {len(zh)} 个 vs 英文 {len(en)} 个，数量不一致"


def check_abstract_len(ctx: SpecContext) -> CheckOutcome:
    spans = [s for s in ctx.abstract_spans() if s["is_zh"]]
    if not spans:
        return "NEEDS-LLM", "未找到中文摘要环境，请人工核对字数"
    n = _char_count(re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?|[{}]", "", spans[0]["text"]))
    bounds = (ctx.thresholds or {}).get("abstract")
    if bounds is None:
        return "NEEDS-LLM", f"摘要实测约 {n} 字；当前模板无字数阈值依据，请对照本校规范判断"
    lo, hi = bounds
    return _range_verdict(n, lo, hi, "中文摘要")


def check_abstract_order(ctx: SpecContext) -> CheckOutcome:
    spans = ctx.abstract_spans()
    zh = next((s for s in spans if s["is_zh"]), None)
    en = next((s for s in spans if not s["is_zh"]), None)
    if zh is None or en is None:
        missing = "中文" if zh is None else "英文"
        return "NEEDS-LLM", f"未找到{missing}摘要环境，请人工核对中前英后与内容一致性"
    if zh["pos"] < en["pos"]:
        return (
            "PASS",
            f"中文摘要({zh['env']})在前，英文摘要({en['env']})在后（内容一致性请人工核对）",
        )
    return "FAIL", f"英文摘要({en['env']})出现在中文摘要({zh['env']})之前"


def check_wordcount(ctx: SpecContext) -> CheckOutcome:
    body = ctx.body_chapters()
    if not body:
        return "NEEDS-LLM", "未识别到正文章（\\chapter），请人工核对字数"
    n = sum(_char_count(ctx.range_visible(ch["start"], ch["end"])) for ch in body)
    bounds = (ctx.thresholds or {}).get("body")
    if bounds is None:
        return "NEEDS-LLM", f"正文实测约 {n} 字；当前模板无字数阈值依据"
    lo, hi = bounds
    return _range_verdict(n, lo, hi, "正文（含图表文字）")


def check_intro_len(ctx: SpecContext) -> CheckOutcome:
    rng = ctx.sections.get("introduction")
    if rng is None:
        return "NEEDS-LLM", "未识别到绪论/引言章，请人工核对绪论字数"
    n = _char_count(ctx.range_visible(rng[0], rng[1]))
    bounds = (ctx.thresholds or {}).get("intro")
    if bounds is None:
        return "NEEDS-LLM", f"绪论实测约 {n} 字；当前模板无字数阈值依据"
    lo, hi = bounds
    return _range_verdict(n, lo, hi, "绪论")


def check_chapter_summary(ctx: SpecContext) -> CheckOutcome:
    intro = ctx.sections.get("introduction")
    concl = ctx.sections.get("conclusion")
    headings = ctx.parser.extract_headings(ctx.content)
    missing = []
    checked = 0
    for ch in ctx.body_chapters():
        if intro and ch["start"] == intro[0]:
            continue
        if concl and ch["start"] == concl[0]:
            continue
        checked += 1
        has_summary = any(
            h["level"] >= 2
            and ch["start"] <= h["line"] <= ch["end"]
            and SUMMARY_TITLE_RE.search(LatexParser.normalize_heading_title(h["title"]))
            for h in headings
        )
        if not has_summary:
            missing.append(ch["title"])
    if checked == 0:
        return "SKIP", "无绪论/结论之外的正文章"
    if missing:
        return (
            "FAIL",
            f"缺「本章小结」的章: {'、'.join(missing)}（实验方法/材料类章可免，请复核，依据 §1.5.2）",
        )
    return "PASS", f"{checked} 个正文章均有小结节"


def check_conclusion_no_cite(ctx: SpecContext) -> CheckOutcome:
    rng = ctx.sections.get("conclusion")
    if rng is None:
        return "NEEDS-LLM", "未识别到结论/总结与展望章，请人工核对"
    hits = [
        ctx.loc(no) for no, line in ctx.range_raw(rng[0], rng[1]) if re.search(r"\\cite\b", line)
    ]
    body = ctx.body_chapters()
    after = [ch["title"] for ch in body if ch["start"] > rng[1]]
    problems = []
    if hits:
        problems.append(f"结论章内出现 \\cite: {', '.join(hits[:5])}")
    if after:
        problems.append(f"结论之后仍有正文章: {'、'.join(after)}")
    if problems:
        return "FAIL", "；".join(problems)
    return "PASS", "结论为最后一章且未标注引用文献"


def check_conclusion_len(ctx: SpecContext) -> CheckOutcome:
    rng = ctx.sections.get("conclusion")
    if rng is None:
        return "NEEDS-LLM", "未识别到结论章，请人工核对结论字数（≤2000 字）"
    n = _char_count(ctx.range_visible(rng[0], rng[1]))
    ev = f"结论实测约 {n} 字（上限 2000）"
    if n <= 2000:
        return "PASS", ev
    if n <= 2200:
        return "NEEDS-LLM", ev + "（临界，请人工判断）"
    return "FAIL", ev


def check_conclusion_hedge(ctx: SpecContext) -> CheckOutcome:
    rng = ctx.sections.get("conclusion")
    if rng is None:
        return "NEEDS-LLM", "未识别到结论章，请人工核对模糊措辞"
    hits = []
    for no, line in ctx.range_raw(rng[0], rng[1]):
        visible = ctx.parser.extract_visible_text(line)
        for m in HEDGE_RE.finditer(visible):
            hits.append(f"{ctx.loc(no)}“{m.group()}”")
    if hits:
        return "FAIL", "结论出现模糊措辞: " + ", ".join(hits[:5])
    return "PASS", "结论未见“大概/或许/可能是”"


def check_bib_count(ctx: SpecContext) -> CheckOutcome:
    if ctx.bib_entries is None:
        return "NEEDS-LLM", ctx.bib_note + "，请人工核对文献数量"
    n = ctx.bib_entries
    need = (ctx.thresholds or {}).get("bib_min")
    if need is None:
        return "NEEDS-LLM", f"参考文献 {n} 篇（{ctx.bib_note}）；当前模板无数量阈值依据"
    ev = f"参考文献 {n} 篇，{ctx.degree} 下限 {need}（{ctx.bib_note}；外文数量请一并人工确认）"
    if n >= need:
        return "PASS", ev
    if n >= need * 0.9:
        return "NEEDS-LLM", ev + "（临界，规范用语为“一般不少于”）"
    return "FAIL", ev


def check_bib_recency(ctx: SpecContext) -> CheckOutcome:
    if ctx.bib_entries is None:
        return "NEEDS-LLM", ctx.bib_note + "，请人工核对文献年份分布"
    if not ctx.bib_years:
        return "NEEDS-LLM", "未能从文献条目解析出年份字段，请人工核对近五年/近两年占比"
    y = ctx.ref_year
    dated = ctx.bib_years
    recent5 = [v for v in dated if v >= y - 4]
    recent2 = [v for v in dated if v >= y - 1]
    ratio = len(recent5) / len(dated)
    ev = (
        f"有年份条目 {len(dated)} 篇；近五年({y - 4}~{y}) {len(recent5)} 篇"
        f"（占 {ratio:.0%}，要求≥1/3）；近两年({y - 1}~{y}) {len(recent2)} 篇（要求≥1）"
    )
    if ratio >= 1 / 3 and recent2:
        return "PASS", ev
    if not recent2 or ratio < 0.3:
        return "FAIL", ev
    return "NEEDS-LLM", ev + "（占比临界，请人工判断）"


def check_heading_len(ctx: SpecContext) -> CheckOutcome:
    over = []
    for h in ctx.parser.extract_headings(ctx.content):
        if h["level"] > 4:
            continue
        title = LatexParser.normalize_heading_title(h["title"])
        title = re.sub(r"\\[a-zA-Z]+", "", title)
        n = _char_count(title)
        if n > 15:
            over.append(f"{ctx.loc(h['line'])}「{h['title']}」({n} 字)")
    if over:
        return "FAIL", "超 15 字标题: " + "; ".join(over[:5])
    return "PASS", "各级标题均在 15 字以内"


def check_heading_depth(ctx: SpecContext) -> CheckOutcome:
    deep = [
        f"{ctx.loc(h['line'])}\\{h['command']}{{{h['title']}}}"
        for h in ctx.parser.extract_headings(ctx.content)
        if h["level"] >= 5
    ]
    if deep:
        return "FAIL", "出现第五级标题（规范不超过四级）: " + "; ".join(deep[:5])
    return "PASS", "章节层次不超过四级"


def check_cite_in_heading(ctx: SpecContext) -> CheckOutcome:
    pat = re.compile(
        r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{[^}]*\\cite"
    )
    hits = [ctx.loc(no) for no, line in ctx.range_raw(1, len(ctx.lines)) if pat.search(line)]
    if hits:
        return "FAIL", "标题内出现引用标示: " + ", ".join(hits[:5])
    return "PASS", "各级标题内未见 \\cite"


def check_new_page_chapter(ctx: SpecContext) -> CheckOutcome:
    if any(h["command"] == "chapter" for h in ctx.parser.extract_headings(ctx.content)):
        return "PASS", "各章使用 \\chapter（book 类默认另起一页）"
    return "FAIL", "未使用 \\chapter 分章，各章可能未另起一页"


def check_appendix_letter(ctx: SpecContext) -> CheckOutcome:
    content_nc = "\n".join(line for _, line in ctx.range_raw(1, len(ctx.lines)))
    has_appendix_cmd = re.search(r"\\appendix\b", content_nc) is not None
    appendix_chapters = [ch["title"] for ch in ctx.chapters if "附录" in ch["title"]]
    if has_appendix_cmd:
        return "PASS", "检测到 \\appendix（附录按大写字母编号由文档类处理）"
    if appendix_chapters:
        return (
            "FAIL",
            f"存在附录章（{'、'.join(appendix_chapters)}）但未见 \\appendix，编号可能不是附录 A/B 形式",
        )
    return "SKIP", "未检测到附录"


CHECKERS: dict[str, Checker] = {
    "title_len": check_title_len,
    "abstract_no_cite": check_abstract_no_cite,
    "kw_count": check_kw_count,
    "kw_zh_en_match": check_kw_zh_en_match,
    "abstract_len": check_abstract_len,
    "abstract_order": check_abstract_order,
    "wordcount": check_wordcount,
    "intro_len": check_intro_len,
    "chapter_summary": check_chapter_summary,
    "conclusion_no_cite": check_conclusion_no_cite,
    "conclusion_len": check_conclusion_len,
    "conclusion_hedge": check_conclusion_hedge,
    "bib_count": check_bib_count,
    "bib_recency": check_bib_recency,
    "heading_len": check_heading_len,
    "heading_depth": check_heading_depth,
    "cite_in_heading": check_cite_in_heading,
    "new_page_chapter": check_new_page_chapter,
    "appendix_letter": check_appendix_letter,
}


# ── 执行与报告 ───────────────────────────────────────────────


def _templates_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "templates"


def _available_checklists() -> list[str]:
    names = []
    for md in sorted(_templates_dir().glob("*.md")):
        if CHECKLIST_HEADING in md.read_text(encoding="utf-8"):
            names.append(md.stem)
    return names


def _detect_degree(content: str) -> tuple[str, str]:
    doctor = len(re.findall(r"博士|doctor|doctoral|dissertation", content, re.IGNORECASE))
    master = len(re.findall(r"硕士|master", content, re.IGNORECASE))
    if doctor > master:
        return "doctor", "自动识别为博士"
    if master > doctor:
        return "master", "自动识别为硕士"
    return "master", "未能识别学位类型，默认按硕士（可用 --degree 指定）"


def run_checklist(items: list[ChecklistItem], ctx: SpecContext) -> list[ItemResult]:
    scope_ok = {"通用", "博士" if ctx.degree == "doctor" else "硕士"}
    results: list[ItemResult] = []
    for item in items:
        if item.scope not in scope_ok:
            status, ev = "SKIP", f"适用范围为「{item.scope}」，当前学位为 {ctx.degree}"
        elif item.method.startswith("script:"):
            key = item.method.split(":", 1)[1]
            checker = CHECKERS.get(key)
            if checker is None:
                status, ev = "NEEDS-LLM", f"检查器 {key} 不存在（自定义清单？），降级为 LLM 判读"
            else:
                status, ev = checker(ctx)
        elif item.method.startswith("module:"):
            mod = item.method.split(":", 1)[1]
            cmd = MODULE_COMMANDS.get(mod, "见 SKILL.md Module Router")
            status, ev = "MODULE", f"由 {mod} 模块覆盖: {cmd}"
        elif item.method == "llm":
            status, ev = "NEEDS-LLM", "由 agent 对照正文与规范依据逐项判读"
        else:
            status, ev = "MANUAL", "需编译 PDF/打印核对，列入打印前自查单"
        results.append(
            ItemResult(
                id=item.id,
                requirement=item.requirement,
                basis=item.basis,
                method=item.method,
                scope=item.scope,
                status=status,
                evidence=ev,
            )
        )
    return results


def generate_report(
    results: list[ItemResult],
    ctx: SpecContext,
    spec_label: str,
    degree_note: str,
) -> str:
    counts: dict[str, int] = dict.fromkeys(
        ("PASS", "FAIL", "NEEDS-LLM", "MODULE", "MANUAL", "SKIP"), 0
    )
    for r in results:
        counts[r.status] += 1
    lines = []
    lines.append("=" * 60)
    lines.append("规范逐项终检报告 (Spec Compliance Final Check)")
    lines.append("=" * 60)
    lines.append(f"入口文件: {ctx.tex_file}")
    lines.append(f"规范清单: {spec_label} · {len(results)} 项")
    lines.append(f"学位: {ctx.degree}（{degree_note}）· 年份基准: {ctx.ref_year}")
    lines.append("统计: " + " · ".join(f"{k} {v}" for k, v in counts.items() if v))
    for warn in ctx.doc.warning_lines():
        lines.append(warn)

    fails = [r for r in results if r.status == "FAIL"]
    if fails:
        lines.append("")
        lines.append("-" * 60)
        lines.append("[FAIL] 不符合项（[Script] 自动判定）:")
        for r in fails:
            lines.append(
                f"% SPEC-CHECK [High] [P1] [Script]: {r.id} {r.requirement}"
                f" — {r.evidence}（依据 {r.basis}）"
            )

    needs = [r for r in results if r.status == "NEEDS-LLM"]
    if needs:
        lines.append("")
        lines.append("-" * 60)
        lines.append("[NEEDS-LLM] 待 agent 逐项判读（流程见 references/modules/spec-check.md）:")
        for r in needs:
            lines.append(f"- {r.id} ({r.basis}) {r.requirement} — {r.evidence}")

    modules = [r for r in results if r.status == "MODULE"]
    if modules:
        lines.append("")
        lines.append("-" * 60)
        lines.append("[MODULE] 由既有模块覆盖，建议命令:")
        for r in modules:
            lines.append(f"- {r.id} ({r.basis}) {r.evidence}")

    manuals = [r for r in results if r.status == "MANUAL"]
    if manuals:
        lines.append("")
        lines.append("-" * 60)
        lines.append("[MANUAL] 打印前自查单（版式/印刷项，无法静态判定）:")
        for r in manuals:
            lines.append(f"- {r.id} ({r.basis}) {r.requirement}")

    passes = [r for r in results if r.status == "PASS"]
    if passes:
        lines.append("")
        lines.append("-" * 60)
        lines.append("[PASS] 通过项:")
        for r in passes:
            lines.append(f"- {r.id} {r.requirement} — {r.evidence}")

    skips = [r for r in results if r.status == "SKIP"]
    if skips:
        lines.append("")
        lines.append("[SKIP] " + "; ".join(f"{r.id}（{r.evidence}）" for r in skips))

    lines.append("")
    lines.append("=" * 60)
    lines.append(
        f"结论: {'存在不符合项' if fails else '自动检查未发现不符合项'}"
        f"（FAIL {counts['FAIL']} · NEEDS-LLM {counts['NEEDS-LLM']}"
        f" · MANUAL {counts['MANUAL']}）"
    )
    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Spec Compliance Final Check（对照学校规范清单逐项终检）"
    )
    parser.add_argument("tex_file", help="论文入口 .tex 文件")
    parser.add_argument(
        "--template",
        help="规范清单模板 id（templates/<id>.md，需含「逐项检查清单」段），如 yanshan",
    )
    parser.add_argument(
        "--spec-file", help="自定义规范清单文件路径（格式同 templates/*.md 的清单表格）"
    )
    parser.add_argument(
        "--degree",
        choices=["master", "doctor"],
        help="学位类型（默认从正文自动识别，识别失败按 master）",
    )
    parser.add_argument("--bib", help="参考文献 .bib 路径（默认从 \\bibliography 自动发现）")
    parser.add_argument("--year", type=int, help="近五年/近两年判定的基准年份（默认当前年份）")
    parser.add_argument("--json", "-j", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    if args.spec_file:
        spec_path = Path(args.spec_file)
        template_id = spec_path.stem
        spec_label = str(spec_path)
    else:
        template_id = args.template or ""
        if not template_id:
            entry_text = tex_path.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"\\documentclass(?:\[[^\]]*\])?\{(\w+)\}", entry_text)
            template_id = m.group(1) if m else "generic"
        spec_path = _templates_dir() / f"{template_id}.md"
        spec_label = f"{template_id} (templates/{template_id}.md)"
    if not spec_path.exists():
        print(f"[ERROR] 清单文件不存在: {spec_path}", file=sys.stderr)
        print(
            f"当前带逐项清单的模板: {', '.join(_available_checklists()) or '(无)'}", file=sys.stderr
        )
        sys.exit(2)

    try:
        items = parse_checklist(spec_path)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        print(
            f"当前带逐项清单的模板: {', '.join(_available_checklists()) or '(无)'}", file=sys.stderr
        )
        sys.exit(2)

    ref_year = args.year or datetime.now().year
    doc = assemble(tex_path)
    if args.degree:
        degree, degree_note = args.degree, "--degree 指定"
    else:
        degree, degree_note = _detect_degree(doc.content)

    ctx = SpecContext(tex_path, degree, template_id, args.bib, ref_year, doc=doc)
    results = run_checklist(items, ctx)

    if args.json:
        payload = {
            "tex_file": str(ctx.tex_file),
            "spec": spec_label,
            "template": template_id,
            "degree": degree,
            "ref_year": ref_year,
            "items": [asdict(r) for r in results],
            "summary": {
                s: sum(1 for r in results if r.status == s)
                for s in ("PASS", "FAIL", "NEEDS-LLM", "MODULE", "MANUAL", "SKIP")
            },
            "status": "FAIL" if any(r.status == "FAIL" for r in results) else "PASS",
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(generate_report(results, ctx, spec_label, degree_note))

    sys.exit(1 if any(r.status == "FAIL" for r in results) else 0)


if __name__ == "__main__":
    main()
