#!/usr/bin/env python3
"""
逻辑与方法论分析器 — 中文学位论文版本

检查：段落级逻辑衔接、方法论论证、文献综述质量（A1/A3）、跨章节逻辑链闭合（C3）。
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from parsers import get_parser
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser


TRANSITIONS_ZH = {
    "递进": {"此外", "进一步", "更重要的是", "不仅如此", "同时"},
    "转折": {"然而", "但是", "相反", "尽管如此", "不过"},
    "因果": {"因此", "由此可见", "故而", "所以", "从而"},
}


def _has_transition_zh(text: str) -> bool:
    return any(token in text for values in TRANSITIONS_ZH.values() for token in values)


def _needs_method_justification_zh(text: str) -> bool:
    if "本文采用" not in text and "本文使用" not in text and "我们采用" not in text:
        return False
    return not any(m in text for m in ["因为", "由于", "鉴于", "考虑到", "基于", "原因"])


# ── 文献综述质量检查 (A1, A3) ──────────────────────────────────

AUTHOR_ENUM_ZH = re.compile(
    r"^.*?[（(]\d{4}[)）].*?(?:提出|引入|设计|开发|采用|构建|建立)",
)

GAP_KEYWORDS_ZH = re.compile(
    r"(研究空白|不足|然而.*?尚未|仍然.*?(?:挑战|困难)|有待|缺乏|"
    r"尚未解决|亟待|亟需|鲜有研究|未能充分)",
)


def _check_lit_review_enumeration(lines: list[str], start: int, end: int, parser) -> list[str]:
    """A1: 检测3条及以上连续的作者/年份罗列模式。"""
    out: list[str] = []
    consecutive = 0
    streak_start = 0
    comment_prefix = parser.get_comment_prefix()
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        if AUTHOR_ENUM_ZH.search(visible):
            if consecutive == 0:
                streak_start = line_no
            consecutive += 1
        else:
            if consecutive >= 3:
                out.extend(
                    [
                        f"% 文献综述（第{streak_start}-{line_no - 1}行）"
                        "[Severity: Major] [Priority: P1]: "
                        f"检测到作者/年份罗列模式（连续{consecutive}条）",
                        "% 建议：按研究主题分组，组内进行批判性对比分析。",
                        "% 理由：按时间或作者罗列文献会削弱文献综述的综合深度。",
                        "",
                    ]
                )
            consecutive = 0
    if consecutive >= 3:
        out.extend(
            [
                f"% 文献综述（第{streak_start}-{min(end, len(lines))}行）"
                "[Severity: Major] [Priority: P1]: "
                f"检测到作者/年份罗列模式（连续{consecutive}条）",
                "% 建议：按研究主题分组，组内进行批判性对比分析。",
                "% 理由：按时间或作者罗列文献会削弱文献综述的综合深度。",
                "",
            ]
        )
    return out


def _check_gap_derivation(lines: list[str], start: int, end: int, parser) -> list[str]:
    """A3: 检查相关工作末尾是否包含研究空白描述。"""
    out: list[str] = []
    scan_start = max(start, end - 10)
    comment_prefix = parser.get_comment_prefix()
    found_gap = False
    for line_no in range(scan_start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and GAP_KEYWORDS_ZH.search(visible):
            found_gap = True
            break
    if not found_gap:
        out.extend(
            [
                f"% 文献综述（第{scan_start}-{end}行）"
                "[Severity: Major] [Priority: P1]: "
                "相关工作末尾未发现研究空白推导",
                "% 建议：添加明确的研究空白陈述，连接文献综述与本文贡献。",
                "% 理由：相关工作应以识别研究空白作为结尾，为本研究提供动机。",
                "",
            ]
        )
    return out


# ── 跨章节逻辑链闭合 (C3) ──────────────────────────────────────

CONTRIBUTION_KEYWORDS_ZH = re.compile(
    r"(本文提出|本文的贡献|本文设计|本文开发|主要贡献|本研究提出|本文构建)",
)
ANSWER_KEYWORDS_ZH = re.compile(
    r"(本文证明了|实验表明|结果表明|本文提出了|验证了|证实了|研究发现)",
)


def _check_cross_section_closure(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    """C3: 验证绪论中的贡献声明在结论中得到回应。"""
    out: list[str] = []
    if "introduction" not in sections or "conclusion" not in sections:
        return out

    intro_start, intro_end = sections["introduction"]
    concl_start, concl_end = sections["conclusion"]
    comment_prefix = parser.get_comment_prefix()

    intro_claims = 0
    for line_no in range(intro_start, min(intro_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and CONTRIBUTION_KEYWORDS_ZH.search(visible):
            intro_claims += 1

    if intro_claims == 0:
        return out

    concl_answers = 0
    for line_no in range(concl_start, min(concl_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and ANSWER_KEYWORDS_ZH.search(visible):
            concl_answers += 1

    if concl_answers == 0:
        out.extend(
            [
                f"% 逻辑衔接（第{concl_start}-{concl_end}行）"
                "[Severity: Major] [Priority: P1]: "
                "[Script] 跨章节逻辑链可能不完整",
                f"% 观察：绪论中有{intro_claims}处贡献声明，但结论中未发现明确回应。",
                "% 建议：在结论中添加明确回应每项贡献的陈述。",
                "% 理由：结论应当闭合绪论中开启的逻辑链。",
                "",
            ]
        )
    return out


def analyze(file_path: Path, section: str | None = None, cross_section: bool = False) -> list[str]:
    parser = get_parser(file_path)
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    sections = parser.split_sections(content)

    if section:
        key = section.lower()
        if key not in sections:
            return [f"% ERROR [Severity: Critical] [Priority: P0]: 未找到章节: {section}"]
        ranges = [sections[key]]
    else:
        ranges = list(sections.values()) if sections else [(1, len(lines))]

    out: list[str] = []
    previous_visible = ""
    comment_prefix = parser.get_comment_prefix()
    for start, end in ranges:
        for line_no in range(start, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(comment_prefix):
                continue

            visible = parser.extract_visible_text(raw)
            if not visible:
                continue

            if _needs_method_justification_zh(visible):
                out.extend(
                    [
                        f"% 方法论深度（第{line_no}行）[Severity: Major] [Priority: P1]: "
                        "方法选择缺乏论证",
                        f"% 原文: {visible}",
                        "% 建议：添加选择理由（如效率/准确率/可复现性）。",
                        "% 理由：方法选择应说明为何采用该方案。",
                        "",
                    ]
                )

            if (
                previous_visible
                and not _has_transition_zh(visible)
                and any(k in previous_visible for k in ["问题", "挑战", "困难", "噪声"])
                and any(k in visible for k in ["本文提出", "本文设计", "我们的方法"])
            ):
                out.extend(
                    [
                        f"% 逻辑衔接（第{line_no}行）[Severity: Major] [Priority: P1]: "
                        "问题与解决方案间可能存在逻辑跳跃",
                        f"% 原文: {visible}",
                        '% 建议：添加显式过渡（如"因此"、"为解决上述问题"）。',
                        "% 理由：增强段落间的逻辑连贯性。",
                        "",
                    ]
                )

            previous_visible = visible

    # ── 章节级检查 ─────────────────────────────────────────────
    if sections:
        related_key = "related"
        if related_key in sections:
            r_start, r_end = sections[related_key]
            if not section or section.lower() == related_key:
                out.extend(_check_lit_review_enumeration(lines, r_start, r_end, parser))
                out.extend(_check_gap_derivation(lines, r_start, r_end, parser))

        if cross_section and not section:
            out.extend(_check_cross_section_closure(lines, sections, parser))

    if not out:
        out.append("% 逻辑/方法论：未检测到规则级逻辑问题。")
    return out


def main() -> int:
    cli = argparse.ArgumentParser(description="中文学位论文逻辑与方法论分析")
    cli.add_argument("file", type=Path, help="目标 .tex/.typ 文件")
    cli.add_argument("--section", help="指定分析章节")
    cli.add_argument(
        "--cross-section",
        action="store_true",
        help="启用跨章节逻辑链闭合检查",
    )
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[错误] 文件未找到: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section, args.cross_section)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
