# Chinese Thesis (latex-thesis-zh)

Specialized toolkit for Chinese thesis writing with LaTeX.

## Overview

The `latex-thesis-zh` skill provides comprehensive support for writing Chinese theses in LaTeX, with focus on GB/T 7714 compliance and major university templates (Tsinghua, PKU, USTC, Fudan).

### Key Features

- **XeLaTeX/LuaLaTeX compilation** (optimized for Chinese)
- **University template detection** (thuthesis, pkuthss, ustcthesis, fduthesis)
- **Structure mapping** for multi-file thesis projects
- **GB/T 7714-2015 compliance** checking
- **Terminology consistency** verification
- **Bibliography management** with Biber/BibTeX
- **Chinese academic writing** style guides

## Installation

```bash
claude skill install github:bahayonghang/academic-writing-skills/dist/latex-thesis-zh.skill.zip
```

## Quick Start

```bash
# Map thesis structure
python ~/.claude/skills/latex-thesis-zh/scripts/map_structure.py thesis.tex

# Compile with XeLaTeX and Biber
python ~/.claude/skills/latex-thesis-zh/scripts/compile.py thesis.tex --recipe xelatex-biber

# Check GB/T 7714 compliance
python ~/.claude/skills/latex-thesis-zh/scripts/verify_bib.py references.bib --standard gbt7714

# Check terminology consistency
python ~/.claude/skills/latex-thesis-zh/scripts/check_consistency.py data/
```

## Scripts

### map_structure.py

Analyze and map thesis structure, detect university template.

**Usage**:
```bash
python map_structure.py <tex_file> [options]

Options:
  --output FORMAT      Output format (text, json, markdown)
  --detect-only        Only detect template, don't map structure
  --verbose            Show detailed analysis
```

**Detection capabilities**:
- University template identification
- Main file and chapter structure
- Required vs. optional components
- File organization patterns
- Bibliography location

**Supported templates**:
- **Tsinghua University** (thuthesis)
- **Peking University** (pkuthesis, pkuthss)
- **USTC** (ustcthesis)
- **Fudan University** (fduthesis)
- **Generic** Chinese thesis template

**Example output**:
```
Thesis Structure Analysis
========================

Template: Tsinghua University (thuthesis)
Main file: thesis.tex
Encoding: UTF-8

Structure:
├── 封面 (Cover)
│   └── data/cover.tex
├── 中文摘要 (Chinese Abstract)
│   └── data/abstract_zh.tex
├── English Abstract
│   └── data/abstract_en.tex
├── 目录 (Contents)
│   └── [auto-generated]
├── 第1章 绪论
│   └── data/chap01.tex
├── 第2章 相关工作
│   └── data/chap02.tex
├── 第3章 方法
│   └── data/chap03.tex
├── 第4章 实验
│   └── data/chap04.tex
├── 第5章 结论
│   └── data/chap05.tex
├── 参考文献 (References)
│   └── ref/refs.bib
├── 致谢 (Acknowledgements)
│   └── data/ack.tex
└── 附录 (Appendix)
    └── data/appendix.tex

Template-specific requirements:
✓ Cover page format: thuthesis style
✓ Abstract: Bilingual (Chinese + English)
✓ Bibliography: GB/T 7714-2015
✓ Chapter naming: 第X章 format
```

**Examples**:
```bash
# Basic structure mapping
python map_structure.py thesis.tex

# JSON output for automation
python map_structure.py thesis.tex --output json

# Template detection only
python map_structure.py thesis.tex --detect-only

# Verbose analysis
python map_structure.py thesis.tex --verbose
```

### compile.py

Compile Chinese thesis with XeLaTeX/LuaLaTeX.

**Usage**:
```bash
python compile.py <tex_file> [options]

Options:
  --recipe RECIPE      Compilation recipe (default: xelatex)
  --output-dir DIR     Output directory
  --clean              Clean auxiliary files
  --verbose            Show detailed output
```

**Available recipes**:
- `xelatex`: Single-pass XeLaTeX (recommended for Chinese)
- `lualatex`: Single-pass LuaLaTeX (alternative)
- `xelatex-bibtex`: XeLaTeX + BibTeX workflow
- `xelatex-biber`: XeLaTeX + Biber workflow (recommended)
- `lualatex-biber`: LuaLaTeX + Biber workflow
- `latexmk`: Automated compilation

**Why XeLaTeX for Chinese?**
- Native Unicode support
- System font access (SimSun, SimHei, KaiTi, FangSong)
- Better CJK typesetting
- GB/T 7714 compatibility

**Examples**:
```bash
# Quick draft
python compile.py thesis.tex --recipe xelatex

# Final version with bibliography
python compile.py thesis.tex --recipe xelatex-biber --clean

# Alternative compiler
python compile.py thesis.tex --recipe lualatex-biber

# Automated handling
python compile.py thesis.tex --recipe latexmk
```

### verify_bib.py

Verify bibliography compliance with GB/T 7714-2015.

**Usage**:
```bash
python verify_bib.py <bib_file> [options]

Options:
  --standard STANDARD  Standard to check (gbt7714, ieee, acm)
  --strict             Strict mode (fail on warnings)
  --fix                Auto-fix common issues
  --output FORMAT      Output format (text, json)
```

**GB/T 7714-2015 checks**:
- Author name format (Chinese vs. English)
- Title format (Chinese vs. English)
- Journal/conference name format
- Year, volume, issue, page format
- DOI format
- Language field requirement

**Common issues detected**:
1. **Mixed language entries**:
   ```bibtex
   % Bad
   @article{key,
     author = {张三 and Smith, John},  % Mixed!
     ...
   }

   % Good
   @article{key,
     author = {张三 and 李四},  % All Chinese
     ...
   }
   ```

2. **Missing language field**:
   ```bibtex
   % Bad
   @article{key,
     author = {张三},
     title = {深度学习研究},
     % Missing language field!
   }

   % Good
   @article{key,
     author = {张三},
     title = {深度学习研究},
     language = {zh},  % Required for Chinese
   }
   ```

3. **Incorrect name format**:
   ```bibtex
   % Bad
   author = {San Zhang}  % Western order for Chinese name

   % Good
   author = {张三}  % Chinese characters
   % or
   author = {Zhang, San}  % Pinyin with comma
   ```

**Examples**:
```bash
# Basic GB/T 7714 check
python verify_bib.py refs.bib --standard gbt7714

# Strict mode (fail on warnings)
python verify_bib.py refs.bib --standard gbt7714 --strict

# Auto-fix common issues
python verify_bib.py refs.bib --standard gbt7714 --fix

# JSON output for CI/CD
python verify_bib.py refs.bib --standard gbt7714 --output json
```

### check_consistency.py

Check terminology consistency across thesis chapters.

**Usage**:
```bash
python check_consistency.py <directory> [options]

Options:
  --terms FILE         Custom terminology list
  --ignore-case        Case-insensitive matching
  --output FORMAT      Output format (text, json)
```

**Checks**:
1. **Inconsistent translations**:
   ```
   Chapter 1: "机器学习" (machine learning)
   Chapter 3: "机器学习" vs "机器学习算法"
   → Inconsistent: Use one term consistently
   ```

2. **Mixed English/Chinese terms**:
   ```
   Chapter 1: "深度学习"
   Chapter 2: "deep learning"
   → Mixed: Choose Chinese or English consistently
   ```

3. **Inconsistent punctuation**:
   ```
   Chapter 1: "首先，其次，最后。"
   Chapter 2: "首先,其次,最后."
   → Inconsistent: Use Chinese or English punctuation
   ```

4. **Abbreviation inconsistency**:
   ```
   Chapter 1: "卷积神经网络 (Convolutional Neural Network, CNN)"
   Chapter 3: "CNN" without definition
   → Missing: Define abbreviation on first use
   ```

**Examples**:
```bash
# Check all .tex files in data/
python check_consistency.py data/

# Use custom terminology list
python check_consistency.py data/ --terms my_terms.txt

# Case-insensitive check
python check_consistency.py data/ --ignore-case

# JSON output
python check_consistency.py data/ --output json
```

### extract_prose.py

Extract Chinese prose for grammar checking.

**Usage**:
```bash
python extract_prose.py <tex_file> [options]

Options:
  --sections SECTIONS  Extract specific sections
  --exclude EXCLUDE    Exclude sections
  --output FILE        Output file
  --format FORMAT      Output format (text, markdown)
```

**Examples**:
```bash
# Extract all prose
python extract_prose.py thesis.tex > prose.txt

# Extract specific chapters
python extract_prose.py thesis.tex --sections chap01,chap02

# Use with Chinese grammar tools
python extract_prose.py thesis.tex | chinese-grammar-checker
```

## University Templates

### Tsinghua University (thuthesis)

**Template**: [thuthesis](https://github.com/tuna/thuthesis)

**Requirements**:
- Cover page: Specific format with university logo
- Abstract: Bilingual (Chinese + English)
- Keywords: Bilingual
- Bibliography: GB/T 7714-2015
- Chapter naming: "第X章" format

**Structure**:
```
thesis.tex              # Main file
├── data/
│   ├── cover.tex       # Cover page
│   ├── abstract.tex    # Abstracts (bilingual)
│   ├── chap01.tex      # Chapter 1
│   ├── chap02.tex      # Chapter 2
│   └── ...
└── ref/
    └── refs.bib        # Bibliography
```

**Compilation**:
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

### Peking University (pkuthss)

**Template**: [pkuthss](https://github.com/CasperVector/pkuthss)

**Requirements**:
- Cover page: PKU-specific format
- Declaration: Original work declaration
- Abstract: Bilingual with keywords
- Bibliography: GB/T 7714-2015

**Structure**:
```
thesis.tex              # Main file
├── chap/
│   ├── abstract.tex    # Abstracts
│   ├── chap1.tex       # Chapter 1
│   └── ...
└── bib/
    └── thesis.bib      # Bibliography
```

**Compilation**:
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

### USTC (ustcthesis)

**Template**: [ustcthesis](https://github.com/ustctug/ustcthesis)

**Requirements**:
- Cover page: USTC format
- Abstract: Bilingual
- Bibliography: GB/T 7714-2015
- Chapter structure: Flexible

**Compilation**:
```bash
python compile.py main.tex --recipe xelatex-biber
```

### Fudan University (fduthesis)

**Template**: [fduthesis](https://github.com/stone-zeng/fduthesis)

**Requirements**:
- Cover page: Fudan format
- Abstract: Bilingual
- Bibliography: GB/T 7714-2015

**Compilation**:
```bash
python compile.py thesis.tex --recipe xelatex-biber
```

## GB/T 7714-2015 Standard

### Overview

GB/T 7714-2015 is the Chinese national standard for bibliographic references.

**Key requirements**:
1. Author names in original language
2. Title in original language
3. Language field for non-English entries
4. Specific punctuation rules
5. Specific ordering rules

### Entry Types

**Journal article** (期刊文章):
```bibtex
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习在自然语言处理中的应用},
  journal = {计算机学报},
  year = {2024},
  volume = {47},
  number = {3},
  pages = {123--145},
  language = {zh},
  doi = {10.11897/SP.J.1016.2024.00123}
}
```

**Conference paper** (会议论文):
```bibtex
@inproceedings{wang2024neural,
  author = {王五 and 赵六},
  title = {神经网络优化方法研究},
  booktitle = {中国计算机大会论文集},
  year = {2024},
  pages = {45--52},
  address = {北京},
  language = {zh}
}
```

**Book** (图书):
```bibtex
@book{liu2023machine,
  author = {刘七},
  title = {机器学习基础},
  publisher = {清华大学出版社},
  year = {2023},
  address = {北京},
  language = {zh},
  isbn = {978-7-302-12345-6}
}
```

**Thesis** (学位论文):
```bibtex
@phdthesis{chen2023research,
  author = {陈八},
  title = {深度强化学习理论与应用研究},
  school = {清华大学},
  year = {2023},
  address = {北京},
  language = {zh}
}
```

### Mixed Bibliography

For theses with both Chinese and English references:

```bibtex
% Chinese entry
@article{zhang2024deep,
  author = {张三 and 李四},
  title = {深度学习研究},
  journal = {计算机学报},
  year = {2024},
  language = {zh}
}

% English entry
@article{smith2024machine,
  author = {Smith, John and Doe, Jane},
  title = {Machine Learning Advances},
  journal = {Journal of Machine Learning Research},
  year = {2024},
  language = {en}
}
```

**Important**: Always include `language` field!

## Chinese Academic Writing

### Style Guide

See: `~/.claude/skills/latex-thesis-zh/references/ACADEMIC_STYLE_ZH.md`

**Topics**:
- 学术写作规范 (Academic writing norms)
- 标点符号使用 (Punctuation usage)
- 数字和单位 (Numbers and units)
- 图表标题 (Figure/table captions)
- 专业术语 (Technical terminology)

### Common Issues

1. **Mixed punctuation**:
   ```latex
   % Bad
   首先,其次,最后.

   % Good (Chinese punctuation)
   首先，其次，最后。

   % Or (English punctuation in English context)
   First, second, finally.
   ```

2. **Inconsistent terminology**:
   ```latex
   % Bad
   第一章使用"机器学习"
   第二章使用"机器学习算法"
   第三章使用"ML"

   % Good
   统一使用"机器学习"或"机器学习算法"
   首次出现时定义缩写：机器学习 (Machine Learning, ML)
   ```

3. **Figure/table captions**:
   ```latex
   % Bad
   \caption{实验结果}  % Too brief

   % Good
   \caption{不同模型在测试集上的准确率对比}  % Descriptive
   ```

## Integration with Claude Code

### Natural Language Commands

```
You: 帮我编译清华大学的学位论文模板

Claude: 我会使用 XeLaTeX + Biber 编译您的清华大学论文模板。

[检测到 thuthesis 模板]
[执行 xelatex-biber 编译流程]

Claude: 编译成功！生成了 thesis.pdf。
检测到您使用的是 thuthesis 模板，已自动应用 GB/T 7714-2015 参考文献格式。
```

### Workflow Automation

```yaml
# .claude/workflows/thesis-check.yaml
name: Thesis Check
triggers:
  - file_save: "data/*.tex"
steps:
  - skill: latex-thesis-zh
    script: check_consistency.py
    args: "data/"
  - skill: latex-thesis-zh
    script: compile.py
    args: "thesis.tex --recipe xelatex-biber"
```

## Advanced Usage

### Custom Terminology List

Create custom terminology list for consistency checking:

```text
# my_terms.txt
机器学习 = machine learning
深度学习 = deep learning
神经网络 = neural network
卷积神经网络 = convolutional neural network = CNN
```

Use with:
```bash
python check_consistency.py data/ --terms my_terms.txt
```

### Batch Processing

Process multiple chapters:

```bash
# Check all chapters
for file in data/chap*.tex; do
  python check_format.py "$file"
done

# Extract prose from all chapters
for file in data/chap*.tex; do
  python extract_prose.py "$file" >> all_prose.txt
done
```

### CI/CD Integration

```yaml
# .github/workflows/thesis-ci.yml
- name: Check GB/T 7714 compliance
  run: |
    python verify_bib.py ref/refs.bib --standard gbt7714 --output json

- name: Check consistency
  run: |
    python check_consistency.py data/ --output json

- name: Compile thesis
  run: |
    python compile.py thesis.tex --recipe xelatex-biber
```

## Troubleshooting

### Chinese Characters Not Displaying

**Error**: Chinese text shows as boxes or compilation errors

**Solution**: Use XeLaTeX or LuaLaTeX
```bash
python compile.py thesis.tex --recipe xelatex
```

### Font Not Found

**Error**: `! Font \xxx not found`

**Solution**: Install Chinese fonts
```bash
# macOS: Fonts usually pre-installed

# Ubuntu/Debian
sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei

# Windows: Install SimSun, SimHei, KaiTi, FangSong
```

### GB/T 7714 Format Issues

**Error**: Bibliography not following GB/T 7714

**Solution**: Use biblatex with gb7714-2015 style
```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
```

### Template Not Detected

**Error**: `map_structure.py` doesn't detect template

**Solution**: Check document class
```latex
% Ensure you're using the correct document class
\documentclass{thuthesis}  % For Tsinghua
\documentclass{pkuthss}    % For PKU
```

## Next Steps

- [Compilation Recipes Guide](/guides/compilation)
- [Bibliography Guide](/guides/bibliography)
- [GB/T 7714 Reference](/references/gb-standard)
- [Usage Guide](/usage)
