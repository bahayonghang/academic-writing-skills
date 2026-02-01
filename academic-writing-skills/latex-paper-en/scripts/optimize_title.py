#!/usr/bin/env python3
"""
Title Optimization Tool for LaTeX Academic Papers (English)

Based on IEEE Author Center and top-tier venue best practices.
Generates and optimizes paper titles following academic standards.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# Import parsers from the same directory
try:
    from parsers import extract_abstract, extract_title
except ImportError:
    # Fallback for direct execution
    import os

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from parsers import extract_abstract, extract_title


# Ineffective words to remove
INEFFECTIVE_WORDS = [
    "a study of",
    "research on",
    "novel",
    "new",
    "improved",
    "enhanced",
    "based on",
    "using",
    "utilizing",
    "an investigation of",
    "analysis of",
]

# Common abbreviations acceptable in titles
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
    "RAM",
    "SQL",
    "HTTP",
    "TCP",
    "IP",
}

# Title templates
TITLE_TEMPLATES = {
    "method_for_problem": "{method} for {problem}",
    "method_problem_domain": "{method}: {problem} in {domain}",
    "problem_via_method": "{problem} via {method}",
    "method_feature": "{feature} {method} for {problem}",
}


def extract_keywords_from_abstract(abstract: str) -> dict[str, list[str]]:
    """Extract potential keywords from abstract."""
    # Simple keyword extraction (can be enhanced with NLP)
    method_keywords = []
    problem_keywords = []
    domain_keywords = []

    # Method patterns
    method_patterns = [
        r"\b(transformer|attention|lstm|gru|cnn|neural network|deep learning|"
        r"machine learning|reinforcement learning|graph neural network|"
        r"convolutional|recurrent)\b"
    ]

    # Problem patterns
    problem_patterns = [
        r"\b(forecasting|prediction|detection|classification|segmentation|"
        r"recognition|optimization|control|diagnosis|monitoring)\b"
    ]

    # Domain patterns
    domain_patterns = [
        r"\b(industrial|manufacturing|medical|healthcare|autonomous|"
        r"smart|intelligent|real-time|time series)\b"
    ]

    abstract_lower = abstract.lower()

    for pattern in method_patterns:
        method_keywords.extend(re.findall(pattern, abstract_lower, re.IGNORECASE))

    for pattern in problem_patterns:
        problem_keywords.extend(re.findall(pattern, abstract_lower, re.IGNORECASE))

    for pattern in domain_patterns:
        domain_keywords.extend(re.findall(pattern, abstract_lower, re.IGNORECASE))

    return {
        "method": list(set(method_keywords))[:3],
        "problem": list(set(problem_keywords))[:3],
        "domain": list(set(domain_keywords))[:2],
    }


def score_title(title: str) -> dict[str, any]:
    """Score a title based on best practices."""
    scores = {}
    issues = []

    # 1. Conciseness (25%)
    title_lower = title.lower()
    ineffective_found = [word for word in INEFFECTIVE_WORDS if word in title_lower]
    if ineffective_found:
        conciseness_score = max(0, 25 - len(ineffective_found) * 10)
        issues.append(f"[Critical] Contains ineffective words: {', '.join(ineffective_found)}")
    else:
        conciseness_score = 25
    scores["conciseness"] = conciseness_score

    # 2. Searchability (30%)
    # Check if key terms appear in first 65 characters
    first_65 = title[:65]
    # Simple heuristic: check for technical terms
    technical_terms = re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b", first_65)
    if len(technical_terms) >= 2:
        searchability_score = 30
    elif len(technical_terms) == 1:
        searchability_score = 20
        issues.append("[Major] Consider placing more key terms in first 65 characters")
    else:
        searchability_score = 10
        issues.append("[Critical] Key terms should appear in first 65 characters")
    scores["searchability"] = searchability_score

    # 3. Length (15%)
    word_count = len(title.split())
    if 10 <= word_count <= 15:
        length_score = 15
    elif 8 <= word_count <= 20:
        length_score = 10
        issues.append(f"[Minor] Length is acceptable ({word_count} words) but could be optimized")
    else:
        length_score = 5
        issues.append(f"[Major] Length is suboptimal ({word_count} words, target: 10-15)")
    scores["length"] = length_score

    # 4. Specificity (20%)
    # Check for vague terms
    vague_terms = ["method", "approach", "system", "model", "algorithm"]
    vague_found = sum(1 for term in vague_terms if term in title_lower)
    if vague_found == 0:
        specificity_score = 20
    elif vague_found == 1:
        specificity_score = 15
    else:
        specificity_score = 10
        issues.append("[Major] Title contains vague terms, be more specific")
    scores["specificity"] = specificity_score

    # 5. Jargon-Free (10%)
    # Check for obscure abbreviations
    words = title.split()
    abbrevs = [w for w in words if w.isupper() and len(w) > 1]
    obscure_abbrevs = [a for a in abbrevs if a not in ACCEPTABLE_ABBREVS]
    if obscure_abbrevs:
        jargon_score = 5
        issues.append(f"[Minor] Obscure abbreviations found: {', '.join(obscure_abbrevs)}")
    else:
        jargon_score = 10
    scores["jargon"] = jargon_score

    total_score = sum(scores.values())

    return {"total": total_score, "breakdown": scores, "issues": issues}


def generate_title_candidates(
    keywords: dict[str, list[str]], current_title: Optional[str] = None
) -> list[tuple[str, str]]:
    """Generate title candidates based on extracted keywords."""
    candidates = []

    method = keywords.get("method", ["Deep Learning"])[0].title()
    problem = keywords.get("problem", ["Analysis"])[0].title()
    domain = keywords.get("domain", [""])[0].title()

    # Template 1: Method for Problem
    if method and problem:
        title = f"{method} for {problem}"
        if domain:
            title += f" in {domain}"
        candidates.append((title, "method_for_problem"))

    # Template 2: Method: Problem in Domain
    if method and problem and domain:
        title = f"{method}: {problem} in {domain}"
        candidates.append((title, "method_problem_domain"))

    # Template 3: Problem via Method
    if problem and method:
        title = f"{problem} via {method}"
        candidates.append((title, "problem_via_method"))

    # Template 4: Feature + Method for Problem
    if method and problem:
        features = ["Lightweight", "Efficient", "Robust", "Scalable"]
        for feature in features[:1]:  # Just one variant
            title = f"{feature} {method} for {problem}"
            candidates.append((title, "method_feature"))
            break

    return candidates


def optimize_title(title: str) -> str:
    """Optimize an existing title by removing ineffective words."""
    optimized = title

    for word in INEFFECTIVE_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        optimized = pattern.sub("", optimized)

    # Clean up extra spaces
    optimized = re.sub(r"\s+", " ", optimized).strip()

    # Remove leading articles if present
    optimized = re.sub(r"^(A|An|The)\s+", "", optimized, flags=re.IGNORECASE)

    return optimized


def format_report(title: str, score_data: dict, candidates: list[tuple[str, str]] = None) -> str:
    """Format optimization report."""
    report = []
    report.append("% " + "=" * 60)
    report.append("% TITLE OPTIMIZATION REPORT")
    report.append("% " + "=" * 60)
    report.append(f'% Current Title: "{title}"')
    report.append(f"% Quality Score: {score_data['total']}/100")
    report.append("%")

    if score_data["issues"]:
        report.append("% Issues Detected:")
        for i, issue in enumerate(score_data["issues"], 1):
            report.append(f"% {i}. {issue}")
        report.append("%")

    if candidates:
        report.append("% Recommended Titles (Ranked):")
        report.append("%")
        for i, (candidate, _template) in enumerate(candidates, 1):
            cand_score = score_title(candidate)
            report.append(f'% {i}. "{candidate}" [Score: {cand_score["total"]}/100]')
            report.append(
                f"%    - Concise: {'✅' if cand_score['breakdown']['conciseness'] >= 20 else '⚠️'}"
            )
            report.append(
                f"%    - Searchable: {'✅' if cand_score['breakdown']['searchability'] >= 20 else '⚠️'}"
            )
            report.append(
                f"%    - Length: {'✅' if cand_score['breakdown']['length'] >= 10 else '⚠️'} ({len(candidate.split())} words)"
            )
            report.append("%")

    report.append("% Suggested LaTeX Update:")
    if candidates:
        best_title = candidates[0][0]
        report.append(f"% \\title{{{best_title}}}")
    report.append("% " + "=" * 60)

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Optimize LaTeX paper titles following IEEE/ACM/Springer best practices"
    )
    parser.add_argument("tex_file", help="Main .tex file")
    parser.add_argument(
        "--generate", action="store_true", help="Generate title candidates from content"
    )
    parser.add_argument("--optimize", action="store_true", help="Optimize existing title")
    parser.add_argument("--check", action="store_true", help="Check title quality")
    parser.add_argument(
        "--interactive", action="store_true", help="Interactive mode with user input"
    )

    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"Error: File not found: {tex_path}", file=sys.stderr)
        return 1

    # Extract current title
    with open(tex_path, encoding="utf-8") as f:
        content = f.read()

    current_title = extract_title(content)

    if args.check or not (args.generate or args.optimize):
        # Check mode (default)
        if not current_title:
            print("Error: No title found in document", file=sys.stderr)
            return 1

        score_data = score_title(current_title)
        print(format_report(current_title, score_data))

    elif args.generate:
        # Generate mode
        abstract = extract_abstract(content)
        if not abstract:
            print("Warning: No abstract found, using limited keyword extraction", file=sys.stderr)
            abstract = content[:1000]  # Use first 1000 chars

        keywords = extract_keywords_from_abstract(abstract)
        candidates = generate_title_candidates(keywords, current_title)

        # Score and sort candidates
        scored_candidates = [(c, t, score_title(c)["total"]) for c, t in candidates]
        scored_candidates.sort(key=lambda x: x[2], reverse=True)

        # Format as tuples for report
        top_candidates = [(c, t) for c, t, s in scored_candidates[:5]]

        if current_title:
            score_data = score_title(current_title)
            print(format_report(current_title, score_data, top_candidates))
        else:
            print("% Generated Title Candidates:")
            for i, (candidate, _template) in enumerate(top_candidates, 1):
                cand_score = score_title(candidate)
                print(f'% {i}. "{candidate}" [Score: {cand_score["total"]}/100]')

    elif args.optimize:
        # Optimize mode
        if not current_title:
            print("Error: No title found in document", file=sys.stderr)
            return 1

        optimized = optimize_title(current_title)
        score_before = score_title(current_title)
        score_after = score_title(optimized)

        print(f'% Original: "{current_title}" [Score: {score_before["total"]}/100]')
        print(f'% Optimized: "{optimized}" [Score: {score_after["total"]}/100]')
        print(f"% Improvement: +{score_after['total'] - score_before['total']} points")

    return 0


if __name__ == "__main__":
    sys.exit(main())
