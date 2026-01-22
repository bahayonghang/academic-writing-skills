# Venue-Specific Requirements for Typst Papers

## IEEE Conferences and Journals

### Format Requirements
- **Paper Size**: US Letter (8.5" × 11")
- **Columns**: Two-column format
- **Column Width**: 3.5" (8.89 cm)
- **Column Separation**: 0.33" (0.84 cm)
- **Margins**: 0.75" top/bottom, 0.625" left/right
- **Font**: Times New Roman 10pt
- **Line Spacing**: Single

### Typst Configuration
```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 0.75in, left: 0.625in, right: 0.625in),
  columns: 2,
  column-gutter: 0.33in
)

#set text(
  font: "Times New Roman",
  size: 10pt
)

#set par(justify: true, leading: 0.55em)
```

### Writing Style
- **Voice**: Active voice preferred
- **Tense**: Past tense for methods, present for results
- **Figures**: "Fig. 1" in text, "Figure 1" in captions
- **Tables**: Roman numerals (Table I, Table II)
- **Equations**: Numbered consecutively

### Citation Style
- Numeric citations in square brackets: [1], [2-4]
- IEEE reference format

### Template
```typst
#import "@preview/charged-ieee:0.1.0": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (...),
  abstract: [...],
  index-terms: ("Keyword1", "Keyword2"),
  bibliography: bibliography("refs.bib", style: "ieee"),
)
```

---

## ACM Conferences and Journals

### Format Requirements
- **Paper Size**: US Letter or A4
- **Columns**: Two-column format
- **Font**: Linux Libertine or similar
- **Font Size**: 9-10pt
- **Margins**: 0.75" left/right, 1" top/bottom

### Typst Configuration
```typst
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
  column-gutter: 0.33in
)

#set text(
  font: "Linux Libertine",
  size: 9pt
)

#set par(justify: true)
```

### Writing Style
- **Tense**: Present tense for general truths
- **Figures**: "Figure 1" consistently
- **Tables**: "Table 1" consistently
- **Citation**: Numeric or author-year depending on venue

### Citation Styles
- **Numeric**: [1], [2, 3]
- **Author-Year**: (Smith et al., 2020)

---

## Springer Journals

### Format Requirements
- **Paper Size**: A4
- **Columns**: Single or two-column (venue-specific)
- **Font**: Times New Roman or similar
- **Font Size**: 10-12pt
- **Margins**: 2.5 cm all sides

### Typst Configuration
```typst
#set page(
  paper: "a4",
  margin: 2.5cm
)

#set text(
  font: "Times New Roman",
  size: 11pt
)

#set par(
  justify: true,
  first-line-indent: 1.5em
)
```

### Writing Style
- **Figures**: Caption below figure
- **Tables**: Caption above table
- **References**: Alphabetical order by author
- **Sections**: Numbered (1, 1.1, 1.1.1)

### Special Requirements
- Abstract: 150-250 words
- Keywords: 4-6 keywords
- Acknowledgments: Separate section before references

---

## NeurIPS / ICML / ICLR (Machine Learning Conferences)

### Format Requirements
- **Page Limit**: 8 pages (excluding references)
- **Paper Size**: US Letter
- **Columns**: Single column
- **Font**: Times New Roman 10pt
- **Margins**: 1" all sides
- **Line Spacing**: Single

### Typst Configuration
```typst
#set page(
  paper: "us-letter",
  margin: 1in
)

#set text(
  font: "Times New Roman",
  size: 10pt
)

#set par(
  justify: true,
  leading: 0.65em
)

#set heading(numbering: none)  // No section numbering
```

### Writing Style
- **Anonymous Submission**: Remove author info for review
- **Figures**: High-quality, readable in grayscale
- **Code**: Supplementary material only
- **Reproducibility**: Include implementation details

### Special Requirements
- **Broader Impact Statement**: Required for NeurIPS
- **Checklist**: Complete reproducibility checklist
- **Supplementary Material**: Separate PDF

---

## CVPR / ICCV / ECCV (Computer Vision Conferences)

### Format Requirements
- **Page Limit**: 8 pages (excluding references)
- **Paper Size**: US Letter
- **Columns**: Two-column format
- **Font**: Times New Roman 10pt
- **Margins**: 1" all sides

### Typst Configuration
```typst
#set page(
  paper: "us-letter",
  margin: 1in,
  columns: 2,
  column-gutter: 0.33in
)

#set text(
  font: "Times New Roman",
  size: 10pt
)
```

### Writing Style
- **Figures**: Essential for visual results
- **Qualitative Results**: Show visual comparisons
- **Quantitative Results**: Tables with metrics
- **Ablation Studies**: Required

---

## AAAI / IJCAI (AI Conferences)

### Format Requirements
- **Page Limit**: 7 pages (excluding references)
- **Paper Size**: US Letter
- **Columns**: Two-column format
- **Font**: Times New Roman 10pt

### Typst Configuration
```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 1in, left: 0.875in, right: 0.875in),
  columns: 2,
  column-gutter: 0.25in
)

#set text(
  font: "Times New Roman",
  size: 10pt
)
```

---

## Nature / Science (High-Impact Journals)

### Format Requirements
- **Word Limit**: Strict (e.g., 3000 words for Nature)
- **Figures**: Limited number (4-6 typically)
- **References**: Limited (30-50 typically)
- **Supplementary**: Extensive supplementary material

### Writing Style
- **Broad Audience**: Accessible to non-specialists
- **Significance**: Emphasize broader impact
- **Concise**: Every word counts
- **Figures**: Publication-quality, self-explanatory

---

## Chinese Journals (中文期刊)

### GB/T 7714-2015 Standard

#### Format Requirements
- **Paper Size**: A4
- **Margins**: 2.5-3 cm
- **Font**: 宋体 (SimSun) for Chinese, Times New Roman for English
- **Font Size**: 小四 (12pt) for body text
- **Line Spacing**: 1.5 or double

#### Typst Configuration
```typst
#set page(
  paper: "a4",
  margin: (x: 3.17cm, y: 2.54cm)
)

#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  size: 12pt,
  lang: "zh",
  region: "cn"
)

#set par(
  justify: true,
  leading: 1em,
  first-line-indent: 2em
)

#set heading(numbering: "1.1")
```

#### Citation Style
- **GB/T 7714-2015**: Chinese national standard
- **Format**: [序号] 作者. 题名[文献类型标识]. 出版地: 出版者, 出版年: 页码.

```typst
#bibliography("refs.bib", style: "gb-7714-2015")
```

#### Special Requirements
- **Abstract**: Chinese and English versions
- **Keywords**: 3-5 keywords in both languages
- **Figures**: 图 1, 图 2 (图下表上)
- **Tables**: 表 1, 表 2 (表上图下)
- **Equations**: Numbered as (1), (2) or (1-1), (1-2)

---

## Comparison Table

| Venue | Columns | Font Size | Page Limit | Citation Style |
|-------|---------|-----------|------------|----------------|
| IEEE | 2 | 10pt | Varies | Numeric [1] |
| ACM | 2 | 9-10pt | Varies | Numeric or Author-Year |
| Springer | 1-2 | 10-12pt | Varies | Alphabetical |
| NeurIPS | 1 | 10pt | 8 pages | Numeric [1] |
| CVPR | 2 | 10pt | 8 pages | Numeric [1] |
| Nature | 1 | Varies | ~3000 words | Numeric [1] |
| Chinese | 1 | 12pt | Varies | GB/T 7714-2015 |

---

## General Tips for All Venues

### Before Submission
1. **Read Guidelines**: Check venue-specific requirements
2. **Check Template**: Use official template if available
3. **Page Limit**: Respect strict page limits
4. **Figures**: Ensure high quality and readability
5. **References**: Format correctly for venue
6. **Anonymity**: Remove identifying information if required
7. **Supplementary**: Prepare if allowed/required

### Common Mistakes to Avoid
- ❌ Wrong paper size (US Letter vs A4)
- ❌ Incorrect margins or font size
- ❌ Missing page numbers (if required)
- ❌ Inconsistent citation format
- ❌ Low-quality figures
- ❌ Exceeding page limit
- ❌ Author information in anonymous submission

### Typst Advantages for Venue Compliance
- ✅ Fast compilation for quick format checks
- ✅ Easy template switching
- ✅ Consistent formatting across document
- ✅ Built-in support for multiple citation styles
- ✅ Simple figure and table management
