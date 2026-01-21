#!/usr/bin/env python3
"""
De-AI Writing Trace Checker for Chinese Academic Theses

Analyzes LaTeX source code for AI writing patterns and generates reports.
Compatible with doctoral/master thesis style (Mode T).

Usage:
    python deai_check.py main.tex --section introduction
    python deai_check.py main.tex --analyze
    python deai_check.py main.tex --score
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class ChineseAITraceChecker:
    """Detect AI writing traces in Chinese LaTeX documents."""

    # 高优先级 AI 模式（类别 1：空话与口号）
    EMPTY_PHRASES = {
        r'显著提升',
        r'全面(?:分析|研究|系统)',
        r'有效解决',
        r'重要(?:意义|价值|贡献)',
        r'鲁棒性(?:好|强)',
        r'新颖(?:方法|思路)',
        r'达到最先进水平',
        r'具有重要价值',
        r'取得(?:显著|重大)进展',
    }

    # 高优先级 AI 模式（类别 2：过度确定）
    OVER_CONFIDENT = {
        r'显而易见',
        r'毫无疑问',
        r'必然',
        r'完全',
        r'毫无例外',
        r'总是',
        r'从不',
        r'肯定',
        r'一定',
        r'毋庸置疑',
    }

    # 高优先级 AI 模式（类别 4：模糊量化）
    VAGUE_QUANTIFIERS = {
        r'大量研究',
        r'众多(?:实验|学者)',
        r'多种(?:方法|方案)',
        r'若干(?:方面|问题)',
        r'许多(?:研究|学者)',
        r'大部分',
        r'大幅(?:提升|改善)',
        r'显著(?:增加|减少)',
        r'广泛的',
    }

    # 中优先级 AI 模式（类别 3：模板化表达）
    TEMPLATE_EXPRESSIONS = {
        r'近年来',
        r'越来越多的',
        r'发挥(?:?:着)?重要(?:?:的)?作用',
        r'随着(?:?:?:科技|技术)(?:?:的)?(?:?:快速|飞速)?发展',
        r'被广泛(?:?:?:应用|使用)',
        r'引起了(?:?:?:广泛|众多)关注',
        r'蓬勃(?:?:?:发展|兴起)',
    }

    # Section detection patterns (Chinese thesis)
    SECTION_PATTERNS = {
        'abstract': r'\\chapter\{摘要\}|\\section\{摘要\}',
        'introduction': r'\\chapter\{绪论\}|\\chapter\{引言\}|\\section\{绪论\}|\\section\{引言\}',
        'related': r'\\chapter\{相关工作\}|\\section\{相关工作\}|\\section\{文献综述\}',
        'method': r'\\chapter\{.*?(?:方法|原理|设计)\}',
        'experiment': r'\\chapter\{.*?(?:实验|实现|测试)\}|\\section\{.*?(?:实验|实现)\}',
        'result': r'\\chapter\{.*?(?:结果|性能)\}|\\section\{.*?(?:结果|性能)\}',
        'discussion': r'\\chapter\{.*?(?:讨论|分析)\}|\\section\{.*?(?:讨论|分析)\}',
        'conclusion': r'\\chapter\{结论\}|\\chapter\{总结与展望\}|\\section\{结论\}',
    }

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file
        self.content = tex_file.read_text(encoding='utf-8', errors='ignore')
        self.lines = self.content.split('\n')
        self.traces = defaultdict(list)
        self.section_ranges = self._detect_sections()

    def _detect_sections(self) -> Dict[str, Tuple[int, int]]:
        """检测章节行范围."""
        sections = {}
        current_section = 'preamble'
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            matched = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1)
                    current_section = section_name
                    start_line = i
                    matched = True
                    break

        # Last section
        if current_section != 'preamble':
            sections[current_section] = (start_line, len(self.lines))

        return sections

    def _find_pattern_in_section(
        self,
        pattern: str,
        section_name: str,
        category: str
    ) -> List[Dict]:
        """在特定章节中查找模式出现."""
        if section_name not in self.section_ranges:
            return []

        start, end = self.section_ranges[section_name]
        matches = []

        for i in range(start - 1, min(end, len(self.lines))):
            line = self.lines[i]
            if re.search(pattern, line):
                # 跳过注释
                stripped = line.strip()
                if stripped.startswith('%'):
                    continue
                matches.append({
                    'line': i + 1,
                    'text': stripped,
                    'pattern': pattern,
                    'category': category,
                    'section': section_name,
                })

        return matches

    def check_section(self, section_name: str) -> Dict:
        """检查特定章节的 AI 痕迹."""
        results = {
            'section': section_name,
            'total_lines': 0,
            'trace_count': 0,
            'traces': [],
        }

        if section_name not in self.section_ranges:
            start, end = 1, len(self.lines)
        else:
            start, end = self.section_ranges[section_name]

        results['total_lines'] = end - start + 1

        # 检查所有模式类别
        all_patterns = [
            ('empty_phrase', self.EMPTY_PHRASES),
            ('over_confident', self.OVER_CONFIDENT),
            ('vague_quantifier', self.VAGUE_QUANTIFIERS),
            ('template_expr', self.TEMPLATE_EXPRESSIONS),
        ]

        for category, patterns in all_patterns:
            for pattern in patterns:
                matches = self._find_pattern_in_section(pattern, section_name, category)
                results['traces'].extend(matches)

        results['trace_count'] = len(results['traces'])

        return results

    def analyze_document(self) -> Dict:
        """分析整个文档并生成分章节得分."""
        analysis = {
            'total_lines': len(self.lines),
            'sections': {},
        }

        for section_name in self.section_ranges.keys():
            section_result = self.check_section(section_name)
            analysis['sections'][section_name] = section_result

        return analysis

    def calculate_density_score(self, result: Dict) -> float:
        """计算章节的 AI 痕迹密度得分."""
        if result['total_lines'] == 0:
            return 0.0
        return (result['trace_count'] / result['total_lines']) * 100

    def generate_report(self, analysis: Dict) -> str:
        """生成可读报告."""
        report = []
        report.append("=" * 70)
        report.append("中文博士论文去AI化写作痕迹分析报告")
        report.append("=" * 70)
        report.append(f"文件: {self.tex_file}")
        report.append(f"总行数: {analysis['total_lines']}")
        report.append("")

        # 分章节摘要
        report.append("-" * 70)
        report.append("各章节 AI 痕迹密度")
        report.append("-" * 70)

        section_scores = []
        for section_name, result in analysis['sections'].items():
            score = self.calculate_density_score(result)
            section_scores.append((section_name, score, result))

            # 优先级指示器
            if score > 10:
                priority = "紧急"
            elif score > 5:
                priority = "高"
            elif score > 2:
                priority = "中"
            else:
                priority = "低"

            report.append(f"\n[{priority}] {section_name.upper()}")
            report.append(f"  AI 痕迹密度: {score:.1f}%")
            report.append(f"  痕迹数量: {result['trace_count']} / {result['total_lines']} 行")

        # 优先级排序
        report.append("")
        report.append("-" * 70)
        report.append("优先级排序（首先重写的章节）")
        report.append("-" * 70)
        section_scores.sort(key=lambda x: x[1], reverse=True)

        for i, (section_name, score, result) in enumerate(section_scores, 1):
            if score > 2:
                report.append(f"{i}. {section_name}: {score:.1f}% ({result['trace_count']} 处痕迹)")

        # 详细痕迹列表
        report.append("")
        report.append("-" * 70)
        report.append("详细痕迹列表")
        report.append("-" * 70)

        for section_name, result in analysis['sections'].items():
            if result['traces']:
                report.append(f"\n{section_name.upper()}:")
                for trace in result['traces'][:10]:  # 限制前10条
                    category_cn = {
                        'empty_phrase': '空话',
                        'over_confident': '过度确定',
                        'vague_quantifier': '模糊量化',
                        'template_expr': '模板表达',
                    }.get(trace['category'], trace['category'])
                    report.append(f"  第{trace['line']}行 [{category_cn}]")
                    report.append(f"    {trace['text'][:80]}")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='分析中文 LaTeX 文档中的 AI 写作痕迹',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析整个文档
  python deai_check.py thesis.tex --analyze

  # 检查特定章节
  python deai_check.py thesis.tex --section introduction

  # 仅生成得分报告
  python deai_check.py thesis.tex --score
        """
    )

    parser.add_argument('tex_file', type=Path, help='LaTeX 文件')
    parser.add_argument('--section', type=str, help='检查特定章节')
    parser.add_argument('--analyze', action='store_true', help='完整文档分析')
    parser.add_argument('--score', action='store_true', help='仅输出章节得分')
    parser.add_argument('--output', type=Path, help='保存报告到文件')

    args = parser.parse_args()

    if not args.tex_file.exists():
        print(f"[错误] 文件未找到: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    checker = ChineseAITraceChecker(args.tex_file)

    if args.analyze:
        # 完整文档分析
        analysis = checker.analyze_document()
        report = checker.generate_report(analysis)

        if args.output:
            args.output.write_text(report, encoding='utf-8')
            print(f"[成功] 报告已保存到: {args.output}")
        else:
            print(report)

        # 根据最差章节返回退出码
        worst_score = max(
            checker.calculate_density_score(result)
            for result in analysis['sections'].values()
        )
        if worst_score > 10:
            sys.exit(2)  # 紧急
        elif worst_score > 5:
            sys.exit(1)  # 警告
        else:
            sys.exit(0)

    elif args.section:
        # 检查特定章节
        result = checker.check_section(args.section.lower())
        score = checker.calculate_density_score(result)

        print(f"\n章节: {args.section}")
        print(f"AI 痕迹密度: {score:.1f}%")
        print(f"痕迹数量: {result['trace_count']}\n")

        for trace in result['traces']:
            category_cn = {
                'empty_phrase': '空话',
                'over_confident': '过度确定',
                'vague_quantifier': '模糊量化',
                'template_expr': '模板表达',
            }.get(trace['category'], trace['category'])
            print(f"第{trace['line']}行 [{category_cn}]")
            print(f"  {trace['text']}\n")

    elif args.score:
        # 仅输出得分
        analysis = checker.analyze_document()
        print(f"\n{'章节':<15} {'密度':<10} {'痕迹':<10}")
        print("-" * 35)

        for section_name, result in analysis['sections'].items():
            score = checker.calculate_density_score(result)
            print(f"{section_name:<15} {score:>6.1f}%     {result['trace_count']:>3} / {result['total_lines']:>3}")

    else:
        # 默认：交互式模式提示
        print("[信息] 使用 --analyze 进行完整文档分析")
        print("[信息] 使用 --section <名称> 检查特定章节")
        print("[信息] 使用 --score 查看章节密度得分")
        print(f"\n[信息] 在 {args.tex_file.name} 中检测到的章节:")
        for section_name in checker.section_ranges.keys():
            print(f"  - {section_name}")


if __name__ == '__main__':
    main()
