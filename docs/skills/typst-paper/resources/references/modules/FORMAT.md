# Module: Format Check
**Trigger words**: format, format check, lint, style check

**Check Items**:
|category|Check content|standard|
|------|----------|------|
|page margins|top, bottom, left and right margins|Typically 1 inch (2.54cm)|
|line spacing|Single/double spacing|According to journal requirements|
|font|Text font and size|Times New Roman 10-12pt|
|title|Title format at all levels|Clear levels and correct numbering|
|chart|Title position and format|In the table below the figure, the numbers are consecutive|
|Quote|Reference format consistency|number/author-year format|

**Script Usage**:
```bash
uv run python ../scripts/check_format.py main.typ
uv run python ../scripts/check_format.py main.typ --strict
```

**Typst format check points**:
```typst
// 页面设置
#set page(
  paper: "a4",  // 或 "us-letter"
  margin: (x: 2.5cm, y: 2.5cm)
)

// 文本设置
#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

// 段落设置
#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

// 标题设置
#set heading(numbering: "1.1")
```

**Common formatting issues**:
- Inconsistent margins
- Mixed fonts (Chinese and English fonts are not separated)
- Chart numbers are not consecutive
- The citation format is not uniform

