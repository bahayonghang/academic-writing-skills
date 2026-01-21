#!/usr/bin/env python3
"""
De-AI Batch Processor for Chinese Academic Theses

Batch processes entire LaTeX chapters or documents for de-AI polishing.
Compatible with doctoral/master thesis style (Mode T).

Usage:
    python deai_batch.py main.tex --chapter chapter3/introduction.tex
    python deai_batch.py main.tex --all-sections
    python deai_batch.py main.tex --section introduction --output polished/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class ChineseDeAIBatchProcessor:
    """批量处理中文 LaTeX 文档进行去AI化编辑."""

    # Section patterns for splitting (Chinese thesis)
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

    # LaTeX structure preservation patterns
    PRESERVE_PATTERNS = [
        r'\\cite\{[^}]+\}',           # Citations
        r'\\ref\{[^}]+\}',            # References
        r'\\label\{[^}]+\}',          # Labels
        r'\\eqref\{[^}]+\}',          # Equation references
        r'\\autoref\{[^}]+\}',        # Auto references
        r'\$\$[^$]+\$\$',            # Display math
        r'\$[^$]+\$',                # Inline math
        r'\\begin\{equation\}.*?\\end\{equation\}',  # Equations
        r'\\begin\{align\}.*?\\end\{align\}',        # Align environments
        r'\\begin\{.*?\}.*?\\end\{.*?\}',           # Generic environments
        r'\\includegraphics\[?[^\]]*\]?\{[^}]+\}',  # Images
        r'\\caption\{[^}]+\}',        # Captions
    ]

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file
        self.content = tex_file.read_text(encoding='utf-8', errors='ignore')
        self.lines = self.content.split('\n')
        self.sections = self._split_sections()

    def _split_sections(self) -> Dict[str, Tuple[int, int, List[str]]]:
        """按 LaTeX 结构分割文档为章节."""
        sections = {}
        current_section = 'preamble'
        start_line = 0
        section_content = []

        for i, line in enumerate(self.lines, 1):
            matched = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1, section_content)
                    current_section = section_name
                    start_line = i
                    section_content = []
                    matched = True
                    break

            section_content.append(line)

        # Last section
        if section_content:
            sections[current_section] = (start_line, len(self.lines), section_content)

        return sections

    def extract_visible_text(self, line: str) -> str:
        """仅提取可见文本，保留 LaTeX 结构标记."""
        # 保留结构标记
        preserved = []
        temp_line = line

        # 查找并标记所有保留模式
        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group()
                })
                temp_line = temp_line[:match.start()] + ' ' * (match.end() - match.start()) + temp_line[match.end():]

        # 按位置排序保留项
        preserved.sort(key=lambda x: x['start'])

        # 提取可见文本（排除保留部分）
        visible_parts = []
        last_end = 0

        for item in preserved:
            if item['start'] > last_end:
                visible_parts.append(temp_line[last_end:item['start']])
            last_end = item['end']

        if last_end < len(temp_line):
            visible_parts.append(temp_line[last_end:])

        visible_text = ' '.join(visible_parts).strip()
        return visible_text

    def analyze_section(self, section_name: str) -> Dict:
        """分析章节的 AI 痕迹."""
        if section_name not in self.sections:
            return {
                'section': section_name,
                'found': False,
                'lines': 0,
                'traces': [],
            }

        start, end, content = self.sections[section_name]
        traces = []
        line_num = start

        for line in content:
            stripped = line.strip()
            if not stripped or stripped.startswith('%'):
                line_num += 1
                continue

            visible = self.extract_visible_text(stripped)

            # 检查 AI 模式
            ai_patterns = self._check_ai_patterns(visible)

            if ai_patterns:
                traces.append({
                    'line': line_num,
                    'original': stripped,
                    'visible': visible,
                    'patterns': ai_patterns,
                })

            line_num += 1

        return {
            'section': section_name,
            'found': True,
            'lines': end - start + 1,
            'traces': traces,
        }

    def _check_ai_patterns(self, text: str) -> List[str]:
        """检查文本的 AI 写作模式."""
        patterns = []

        # 空话与口号
        empty_phrases = [
            r'显著提升',
            r'全面(?:分析|研究|系统)',
            r'有效解决',
            r'重要(?:意义|价值|贡献)',
            r'鲁棒性(?:好|强)',
            r'新颖(?:方法|思路)',
            r'达到最先进水平',
            r'具有重要价值',
        ]

        # 过度确定
        over_confident = [
            r'显而易见',
            r'毫无疑问',
            r'必然',
            r'完全',
            r'毋庸置疑',
            r'肯定',
            r'一定',
        ]

        # 模糊量化
        vague_quantifiers = [
            r'大量研究',
            r'众多(?:实验|学者)',
            r'多种(?:方法|方案)',
            r'若干(?:方面|问题)',
            r'许多(?:研究|学者)',
            r'大部分',
            r'大幅(?:提升|改善)',
            r'显著的',
        ]

        # 模板化表达
        template_exprs = [
            r'近年来',
            r'越来越多的',
            r'发挥(?:?:着)?重要(?:?:的)?作用',
            r'随着(?:?:?:科技|技术)(?:?:的)?(?:?:快速|飞速)?发展',
            r'被广泛(?:?:?:应用|使用)',
            r'引起了(?:?:?:广泛|众多)关注',
        ]

        all_checks = [
            ('空话', empty_phrases),
            ('过度确定', over_confident),
            ('模糊量化', vague_quantifiers),
            ('模板表达', template_exprs),
        ]

        for category, pattern_list in all_checks:
            for pattern in pattern_list:
                if re.search(pattern, text):
                    patterns.append(f'{category}: {pattern}')

        return patterns

    def generate_batch_report(self, analyses: Dict[str, Dict]) -> str:
        """生成批量处理报告."""
        report = []
        report.append("=" * 70)
        report.append("中文博士论文去AI化批量处理报告")
        report.append("=" * 70)
        report.append(f"源文件: {self.tex_file}")
        report.append("")

        total_traces = 0
        total_lines = 0

        for section_name, analysis in analyses.items():
            if not analysis['found']:
                continue

            trace_count = len(analysis['traces'])
            total_traces += trace_count
            total_lines += analysis['lines']

            density = (trace_count / analysis['lines'] * 100) if analysis['lines'] > 0 else 0

            report.append(f"\n{'─' * 70}")
            report.append(f"章节: {section_name.upper()}")
            report.append(f"{'─' * 70}")
            report.append(f"行数: {analysis['lines']}")
            report.append(f"检测到 AI 痕迹: {trace_count}")
            report.append(f"密度: {density:.1f}%")

            if trace_count > 0:
                report.append(f"\n痕迹（前5条）:")
                for i, trace in enumerate(analysis['traces'][:5], 1):
                    report.append(f"\n  [{i}] 第{trace['line']}行")
                    report.append(f"      模式: {', '.join(trace['patterns'])}")
                    report.append(f"      可见文本: {trace['visible'][:100]}")

        report.append("\n" + "=" * 70)
        report.append("摘要")
        report.append("=" * 70)
        report.append(f"分析总行数: {total_lines}")
        report.append(f"AI 痕迹总数: {total_traces}")
        overall_density = (total_traces / total_lines * 100) if total_lines > 0 else 0
        report.append(f"整体密度: {overall_density:.1f}%")

        return "\n".join(report)

    def process_section_file(self, chapter_file: Path, output_dir: Path) -> bool:
        """处理单个章节文件."""
        if not chapter_file.exists():
            print(f"[错误] 章节文件未找到: {chapter_file}")
            return False

        # 读取章节内容
        content = chapter_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        # 处理每一行
        processed_lines = []
        modifications = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith('%'):
                processed_lines.append(line)
                continue

            visible = self.extract_visible_text(stripped)
            patterns = self._check_ai_patterns(visible)

            if patterns:
                # 添加去AI化编辑注释
                comment = f"% 去AI化: 第{i}行 - {', '.join(patterns)}"
                processed_lines.append(comment)
                processed_lines.append(line)
                modifications.append({
                    'line': i,
                    'patterns': patterns,
                    'original': stripped,
                })
            else:
                processed_lines.append(line)

        # 写入输出
        output_file = output_dir / chapter_file.name
        output_file.write_text('\n'.join(processed_lines), encoding='utf-8')

        print(f"[成功] 已处理: {chapter_file.name}")
        print(f"       输出: {output_file}")
        print(f"       修改: {len(modifications)}处")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='批量处理中文 LaTeX 文档进行去AI化编辑',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析所有章节
  python deai_batch.py thesis.tex --all-sections

  # 处理特定章节文件
  python deai_batch.py main.tex --chapter chapter3/introduction.tex --output polished/

  # 分析特定章节
  python deai_batch.py thesis.tex --section introduction
        """
    )

    parser.add_argument('tex_file', type=Path, help='主 LaTeX 文件')
    parser.add_argument('--chapter', type=Path, help='处理特定章节文件')
    parser.add_argument('--all-sections', action='store_true', help='分析所有章节')
    parser.add_argument('--section', type=str, help='分析特定章节')
    parser.add_argument('--output', type=Path, help='处理后文件的输出目录')
    parser.add_argument('--report', type=Path, help='保存报告到文件')

    args = parser.parse_args()

    if not args.tex_file.exists():
        print(f"[错误] 文件未找到: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    processor = ChineseDeAIBatchProcessor(args.tex_file)

    if args.all_sections:
        # 分析所有章节
        analyses = {}
        for section_name in processor.sections.keys():
            analyses[section_name] = processor.analyze_section(section_name)

        report = processor.generate_batch_report(analyses)

        if args.report:
            args.report.write_text(report, encoding='utf-8')
            print(f"[成功] 报告已保存到: {args.report}")
        else:
            print(report)

    elif args.chapter:
        # 处理特定章节文件
        if not args.output:
            print("[错误] 处理章节文件时需要 --output 参数")
            sys.exit(1)

        args.output.mkdir(parents=True, exist_ok=True)
        success = processor.process_section_file(args.chapter, args.output)

        sys.exit(0 if success else 1)

    elif args.section:
        # 分析特定章节
        analysis = processor.analyze_section(args.section.lower())

        if not analysis['found']:
            print(f"[警告] 章节未找到: {args.section}")
            sys.exit(1)

        print(f"\n章节: {args.section}")
        print(f"行数: {analysis['lines']}")
        print(f"AI 痕迹: {len(analysis['traces'])}\n")

        for trace in analysis['traces'][:10]:
            print(f"第{trace['line']}行:")
            print(f"  模式: {', '.join(trace['patterns'])}")
            print(f"  文本: {trace['visible'][:100]}")
            print()

    else:
        # 默认：列出可用章节
        print(f"[信息] 在 {args.tex_file.name} 中检测到的章节:")
        for section_name in processor.sections.keys():
            start, end, _ = processor.sections[section_name]
            print(f"  - {section_name}: 第{start}-{end}行")


if __name__ == '__main__':
    main()
