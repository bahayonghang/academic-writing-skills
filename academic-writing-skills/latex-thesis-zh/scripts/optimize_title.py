#!/usr/bin/env python3
"""
标题优化工具 - 中文学位论文

基于 GB/T 7713.1-2006 规范及国际最佳实践。
生成和优化学位论文标题。
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Optional

# Import parsers from the same directory
try:
    from parsers import extract_abstract, extract_title, get_parser
    from tex_loader import assemble
except ImportError:
    import os

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from parsers import extract_abstract, extract_title, get_parser
    from tex_loader import assemble


# 无效词汇
INEFFECTIVE_WORDS = [
    "关于",
    "的研究",
    "的探索",
    "新型",
    "新颖的",
    "改进的",
    "优化的",
    "基于",
    "研究与",
    "分析与",
]

# 可接受的缩写
ACCEPTABLE_ABBREVS = {
    "AI",
    "ML",
    "DL",
    "LSTM",
    "GRU",
    "CNN",
    "RNN",
    "GAN",
    "VAE",
    "IoT",
    "5G",
    "GPS",
    "DNA",
    "RNA",
    "MRI",
    "CT",
    "PID",
    "API",
    "GPU",
    "CPU",
}

# 标题模板
TITLE_TEMPLATES = {
    "method_for_problem": "{problem}的{method}研究",
    "domain_problem_method": "{domain}{problem}的{method}",
    "method_application": "{method}及其在{domain}中的应用",
    "domain_oriented": "面向{domain}的{method}{problem}方法",
}

CONVENTIONAL_CHAPTER_RE = re.compile(
    r"^(?:摘要|绪论|引言|相关工作|文献综述|创新点|主要贡献|结论|总结与展望|"
    r"参考文献|致谢|附录|攻读学位期间.*)$"
)

OBJECT_RE = re.compile(
    r"(?:过程|系统|场景|数据|序列|指标|变量|工况|设备|对象|工业|制造|"
    r"水泥|粉磨|煅烧|比表面积|单位电耗|故障|异常路径|图像|文本)"
)
PROBLEM_RE = re.compile(
    r"(?:预测|检测|诊断|监测|评估|优化|控制|调控|识别|辨识|分类|分割|"
    r"软测量|决策|故障|异常|根因|质量|电耗)"
)
METHOD_RE = re.compile(
    r"(?:基于|方法|模型|算法|框架|系统|策略|机制|网络|学习|融合|自适应|"
    r"多步|单步|双通道|因果|图神经|Transformer|LSTM|CVAE|SFA|CIE|MOCS)"
)

SECTION_ROLE_RE = re.compile(
    r"^(?:引言|本章小结|小结)$|"
    r"(?:基础理论|理论基础|问题描述|问题定义|模型|算法|方法|框架|实验|案例|"
    r"应用|结果|分析|讨论|验证|评价指标|流程|建模|设计|优化|预测|监测|"
    r"诊断|调控|决策)"
)
GENERIC_ANCHOR_TERMS = {"研究", "方法", "模型", "算法", "系统", "章节", "本章"}


def extract_keywords_from_abstract(abstract: str) -> dict[str, list[str]]:
    """从摘要中提取关键词"""
    method_keywords = []
    problem_keywords = []
    domain_keywords = []

    # 方法关键词模式
    method_patterns = [
        r"(Transformer|注意力机制|LSTM|GRU|卷积神经网络|循环神经网络|"
        r"深度学习|机器学习|强化学习|图神经网络|神经网络)"
    ]

    # 问题关键词模式
    problem_patterns = [
        r"(预测|检测|分类|分割|识别|优化|控制|诊断|监测|"
        r"时间序列|故障|异常|图像|文本)"
    ]

    # 领域关键词模式
    domain_patterns = [
        r"(工业|制造|医疗|医学|自动驾驶|智能|实时|"
        r"工业控制|智能制造|医学影像)"
    ]

    for pattern in method_patterns:
        method_keywords.extend(re.findall(pattern, abstract))

    for pattern in problem_patterns:
        problem_keywords.extend(re.findall(pattern, abstract))

    for pattern in domain_patterns:
        domain_keywords.extend(re.findall(pattern, abstract))

    return {
        "method": list(set(method_keywords))[:3],
        "problem": list(set(problem_keywords))[:3],
        "domain": list(set(domain_keywords))[:2],
    }


def count_chinese_chars(text: str) -> int:
    """统计中文字符数"""
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def score_title(title: str) -> dict[str, Any]:
    """根据最佳实践评分标题"""
    scores = {}
    issues = []

    # 1. 简洁性 (25%)
    ineffective_found = [word for word in INEFFECTIVE_WORDS if word in title]
    if ineffective_found:
        conciseness_score = max(0, 25 - len(ineffective_found) * 10)
        issues.append(f"[严重] 包含无效词汇: {', '.join(ineffective_found)}")
    else:
        conciseness_score = 25
    scores["conciseness"] = conciseness_score

    # 2. 可搜索性 (30%)
    # 检查前20字是否包含关键术语
    first_20 = title[:20]
    # 简单启发式：检查技术术语
    has_method = bool(re.search(r"(Transformer|LSTM|神经网络|深度学习|机器学习)", first_20))
    has_problem = bool(re.search(r"(预测|检测|分类|控制|优化)", first_20))

    if has_method and has_problem:
        searchability_score = 30
    elif has_method or has_problem:
        searchability_score = 20
        issues.append("[重要] 建议在前20字内同时包含方法和问题关键词")
    else:
        searchability_score = 10
        issues.append("[严重] 关键术语应出现在标题前20字内")
    scores["searchability"] = searchability_score

    # 3. 长度 (15%)
    char_count = count_chinese_chars(title)
    if 15 <= char_count <= 25:
        length_score = 15
    elif 10 <= char_count <= 30:
        length_score = 10
        issues.append(f"[次要] 长度可接受（{char_count}字）但可优化")
    else:
        length_score = 5
        issues.append(f"[重要] 长度不理想（{char_count}字，建议：15-25字）")
    scores["length"] = length_score

    # 4. 具体性 (20%)
    # 检查模糊术语
    vague_terms = ["方法", "系统", "模型", "算法", "技术"]
    vague_count = sum(1 for term in vague_terms if term in title)
    if vague_count <= 1:
        specificity_score = 20
    elif vague_count == 2:
        specificity_score = 15
        issues.append("[次要] 标题包含一些通用术语，可更具体")
    else:
        specificity_score = 10
        issues.append("[重要] 标题过于宽泛，需要更具体")
    scores["specificity"] = specificity_score

    # 5. 规范性 (10%)
    # 检查生僻缩写
    words = title.split()
    abbrevs = [w for w in words if w.isupper() and len(w) > 1]
    obscure_abbrevs = [a for a in abbrevs if a not in ACCEPTABLE_ABBREVS]
    if obscure_abbrevs:
        norm_score = 5
        issues.append(f"[次要] 发现生僻缩写: {', '.join(obscure_abbrevs)}")
    else:
        norm_score = 10
    scores["norm"] = norm_score

    total_score = sum(scores.values())

    return {"total": total_score, "breakdown": scores, "issues": issues}


def _normalize_heading_title(parser, title: str) -> str:
    normalizer = getattr(parser, "normalize_heading_title", None)
    normalized: object = normalizer(title) if callable(normalizer) else re.sub(r"\s+", "", title)
    title = normalized if isinstance(normalized, str) else str(normalized)
    title = re.sub(r"^第?[一二三四五六七八九十百零\d]+章", "", title)
    return title.strip()


def _is_conventional_chapter(title: str) -> bool:
    return bool(CONVENTIONAL_CHAPTER_RE.search(title))


def _heading_facets(title: str) -> dict[str, bool]:
    return {
        "对象": bool(OBJECT_RE.search(title)),
        "问题": bool(PROBLEM_RE.search(title)),
        "方法": bool(METHOD_RE.search(title)),
    }


def _salient_terms(title: str) -> set[str]:
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])*\{([^}]*)\}", r"\1", title)
    text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]+", "", text)
    terms: set[str] = set()
    for size in range(2, min(6, len(text) + 1)):
        for index in range(0, len(text) - size + 1):
            term = text[index : index + size]
            if term not in GENERIC_ANCHOR_TERMS:
                terms.add(term)
    return terms


def _section_anchors_parent(section_title: str, chapter_title: str) -> bool:
    if SECTION_ROLE_RE.search(section_title):
        return True
    chapter_terms = _salient_terms(chapter_title)
    section_terms = _salient_terms(section_title)
    return bool(chapter_terms & section_terms)


def _direct_sections_for_chapter(
    headings: list[dict[str, Any]], index: int
) -> list[dict[str, Any]]:
    chapter = headings[index]
    next_chapter_line = next(
        (h["line"] for h in headings[index + 1 :] if h["level"] == 1),
        None,
    )
    return [
        h
        for h in headings[index + 1 :]
        if h["level"] == 2
        and h["line"] > chapter["line"]
        and (next_chapter_line is None or h["line"] < next_chapter_line)
    ]


def _suggest_anchor_terms(chapter_title: str) -> str:
    preferred = []
    for pattern in (OBJECT_RE, PROBLEM_RE, METHOD_RE):
        match = pattern.search(chapter_title)
        if match and match.group(0) not in preferred:
            preferred.append(match.group(0))
    return " / ".join(preferred[:3]) or chapter_title


def analyze_heading_architecture(tex_path: Path) -> str:
    """Check body chapter and direct-section title architecture.

    This is intentionally heuristic: it surfaces "needs review" style
    diagnostics for thesis heading design without modifying the source.
    """
    doc = assemble(tex_path)
    parser = get_parser(tex_path)
    headings = parser.extract_headings(doc.content)
    chapters = [h for h in headings if h["level"] == 1]
    findings: list[str] = []

    for chapter in chapters:
        chapter_index = headings.index(chapter)
        raw_title = chapter["title"]
        title = _normalize_heading_title(parser, raw_title)
        if _is_conventional_chapter(title):
            continue

        direct_sections = _direct_sections_for_chapter(headings, chapter_index)
        loc = doc.lineref(chapter["line"])
        facets = _heading_facets(title)
        missing = [label for label, present in facets.items() if not present]
        if missing:
            missing_text = "；".join(f"缺少{label}" for label in missing)
            findings.append(
                f"% TITLE-ARCH（{loc}）[Severity: Major] [Priority: P1]: "
                f"章标题缺少对象-问题-方法要素（{missing_text}）\n"
                f"% 当前章标题：「{raw_title}」\n"
                "% 建议：将章标题改成“研究对象 + 问题/任务 + 方法/路径”的结构，"
                "使答辩委员能从目录看出本章解决什么对象上的什么问题。"
            )

        if len(direct_sections) > 5:
            findings.append(
                f"% TITLE-ARCH（{loc}）[Severity: Major] [Priority: P1]: "
                "直属小节过多\n"
                f"% 当前：{len(direct_sections)} 个 \\section，建议压缩到最多 5 个。\n"
                "% 合并建议：将背景/数据/问题类小节合并为“问题描述与建模基础”，"
                "将细分模块下沉到 \\subsection，并保留“引言-方法-实验/应用-本章小结”闭环。"
            )

        for section in direct_sections:
            section_title = _normalize_heading_title(parser, section["title"])
            if _section_anchors_parent(section_title, title):
                continue
            section_loc = doc.lineref(section["line"])
            anchor_terms = _suggest_anchor_terms(title)
            findings.append(
                f"% TITLE-ARCH（{section_loc}）[Severity: Minor] [Priority: P2]: "
                "小节标题未扣合章标题\n"
                f"% 当前小节：「{section['title']}」；所属章：「{raw_title}」\n"
                f"% 建议：在小节标题或导语中补入与本章相关的关键词（如 {anchor_terms}），"
                "避免小节看起来像可移动到任意章节的通用标题。"
            )

    if not findings:
        return "% TITLE-ARCH: 未发现明显的章节标题架构问题。"
    return "\n".join(findings)


def generate_title_candidates(
    keywords: dict[str, list[str]], current_title: Optional[str] = None
) -> list[tuple[str, str]]:
    """根据提取的关键词生成标题候选"""
    candidates = []

    method = keywords.get("method", ["深度学习"])[0]
    problem = keywords.get("problem", ["分析"])[0]
    domain = keywords.get("domain", [""])[0]

    # 模板 1: 问题的方法研究
    if method and problem:
        title = f"{problem}的{method}研究"
        if domain:
            title = f"{domain}{problem}的{method}研究"
        candidates.append((title, "method_for_problem"))

    # 模板 2: 领域问题的方法
    if method and problem and domain:
        title = f"{domain}{problem}的{method}"
        candidates.append((title, "domain_problem_method"))

    # 模板 3: 方法及其应用
    if method and domain:
        title = f"{method}及其在{domain}中的应用"
        if problem:
            title = f"{method}{problem}及其在{domain}中的应用"
        candidates.append((title, "method_application"))

    # 模板 4: 面向领域的方法
    if method and problem and domain:
        title = f"面向{domain}的{method}{problem}方法"
        candidates.append((title, "domain_oriented"))

    return candidates


def optimize_title(title: str) -> str:
    """通过删除无效词汇优化现有标题"""
    optimized = title

    for word in INEFFECTIVE_WORDS:
        optimized = optimized.replace(word, "")

    # 清理多余空格
    optimized = re.sub(r"\s+", "", optimized).strip()

    return optimized


def generate_english_title(chinese_title: str) -> str:
    """生成对应的英文标题（简单翻译）"""
    # 简单的关键词映射
    translations = {
        "Transformer": "Transformer",
        "LSTM": "LSTM",
        "神经网络": "Neural Networks",
        "深度学习": "Deep Learning",
        "机器学习": "Machine Learning",
        "时间序列": "Time Series",
        "预测": "Forecasting",
        "检测": "Detection",
        "分类": "Classification",
        "控制": "Control",
        "工业": "Industrial",
        "智能制造": "Smart Manufacturing",
        "方法": "Methods",
        "研究": "Research",
        "应用": "Applications",
    }

    english = chinese_title
    for cn, en in translations.items():
        english = english.replace(cn, en)

    # 简单清理
    english = re.sub(r"[的及其在中]", " ", english)
    english = re.sub(r"\s+", " ", english).strip()

    return english


def format_report(title: str, score_data: dict, candidates: list[tuple[str, str]] = None) -> str:
    """格式化优化报告"""
    report = []
    report.append("% " + "=" * 60)
    report.append("% 标题优化报告")
    report.append("% " + "=" * 60)
    report.append(f"% 当前标题：「{title}」")
    report.append(f"% 质量评分：{score_data['total']}/100")
    report.append("%")

    if score_data["issues"]:
        report.append("% 检测到的问题：")
        for i, issue in enumerate(score_data["issues"], 1):
            report.append(f"% {i}. {issue}")
        report.append("%")

    if candidates:
        report.append("% 推荐标题（按评分排序）：")
        report.append("%")
        for i, (candidate, _template) in enumerate(candidates, 1):
            cand_score = score_title(candidate)
            char_count = count_chinese_chars(candidate)
            report.append(f"% {i}. 「{candidate}」 [评分: {cand_score['total']}/100]")
            report.append(
                f"%    - 简洁性：{'✅' if cand_score['breakdown']['conciseness'] >= 20 else '⚠️'}"
            )
            report.append(
                f"%    - 可搜索性：{'✅' if cand_score['breakdown']['searchability'] >= 20 else '⚠️'}"
            )
            report.append(
                f"%    - 长度：{'✅' if cand_score['breakdown']['length'] >= 10 else '⚠️'} ({char_count}字)"
            )

            # 生成对应英文标题
            english = generate_english_title(candidate)
            report.append(f"%    - 英文：{english}")
            report.append("%")

    report.append("% 建议的 LaTeX 更新：")
    if candidates:
        best_title = candidates[0][0]
        best_english = generate_english_title(best_title)
        report.append(f"% \\title{{{best_title}}}")
        report.append(f"% \\englishtitle{{{best_english}}}")
    report.append("% " + "=" * 60)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="优化中文学位论文标题，遵循 GB/T 7713.1-2006 规范")
    parser.add_argument("tex_file", help="主 .tex 文件")
    parser.add_argument("--generate", action="store_true", help="根据内容生成标题候选")
    parser.add_argument("--optimize", action="store_true", help="优化现有标题")
    parser.add_argument("--check", action="store_true", help="检查标题质量")
    parser.add_argument("--headings", action="store_true", help="检查章标题/小节标题架构")

    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"错误：文件不存在：{tex_path}", file=sys.stderr)
        return 1

    # 提取当前标题（多文件工程下标题/摘要可能位于 include 文件中）
    doc = assemble(tex_path)
    content = doc.content
    for warn in doc.warning_lines("%"):
        print(warn)

    current_title = extract_title(content)

    handled_title = False

    if args.check or not (args.generate or args.optimize or args.headings):
        # 检查模式（默认）
        if not current_title:
            print("错误：文档中未找到标题", file=sys.stderr)
            return 1

        score_data = score_title(current_title)
        print(format_report(current_title, score_data))
        handled_title = True

    elif args.generate:
        # 生成模式
        abstract = extract_abstract(content)
        if not abstract:
            print("警告：未找到摘要，使用有限的关键词提取", file=sys.stderr)
            abstract = content[:1000]

        keywords = extract_keywords_from_abstract(abstract)
        candidates = generate_title_candidates(keywords, current_title)

        # 评分并排序
        scored_candidates = [(c, t, score_title(c)["total"]) for c, t in candidates]
        scored_candidates.sort(key=lambda x: x[2], reverse=True)

        top_candidates = [(c, t) for c, t, s in scored_candidates[:5]]

        if current_title:
            score_data = score_title(current_title)
            print(format_report(current_title, score_data, top_candidates))
        else:
            print("% 生成的标题候选：")
            for i, (candidate, _template) in enumerate(top_candidates, 1):
                cand_score = score_title(candidate)
                print(f"% {i}. 「{candidate}」 [评分: {cand_score['total']}/100]")
        handled_title = True

    elif args.optimize:
        # 优化模式
        if not current_title:
            print("错误：文档中未找到标题", file=sys.stderr)
            return 1

        optimized = optimize_title(current_title)
        score_before = score_title(current_title)
        score_after = score_title(optimized)

        print(f"% 原标题：「{current_title}」 [评分: {score_before['total']}/100]")
        print(f"% 优化后：「{optimized}」 [评分: {score_after['total']}/100]")
        print(f"% 提升：+{score_after['total'] - score_before['total']} 分")
        handled_title = True

    if args.headings:
        if handled_title:
            print("%")
        print(analyze_heading_architecture(tex_path))

    return 0


if __name__ == "__main__":
    sys.exit(main())
