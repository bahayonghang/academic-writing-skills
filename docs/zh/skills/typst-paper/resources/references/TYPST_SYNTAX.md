# 学术写作的 Typst 语法参考

## 目录

- [基本语法](#basic-syntax)
  - [文本格式](#text-formatting)
  - [标题](#headings)
  - [段落](#paragraphs)
  - [列表](#lists)
- [数学](#math)
  - [内联数学](#inline-math)
  - [显示数学](#display-math)
  - [常用数学符号](#common-math-symbols)
- [图表](#figures-and-tables)
  - [图](#figures)
  - [表格](#tables)
- [引文和参考文献](#citations-and-references)
  - [引文](#citations)
  - [参考书目](#bibliography)
  - [引文样式](#citation-styles)
- [页面设置](#page-setup)
  - [基本页面配置](#basic-page-configuration)
  - [两栏布局](#two-column-layout)
  - [页眉和页脚](#headers-and-footers)
- [文本格式](#text-formatting)
  - [字体设置](#font-settings)
  - [段落设置](#paragraph-settings)
  - [标题设置](#heading-settings)
- [交叉引用](#cross-references)
  - [标签](#labels)
  - [参考文献](#references)
- [函数和变量](#functions-and-variables)
  - [定义变量](#define-variables)
  - [定义函数](#define-functions)
  - [条件内容](#conditional-content)
- [展示规则（造型）](#show-rules-styling)
  - [样式标题](#style-headings)
  - [样式链接](#style-links)
  - [风格人偶](#style-figures)
- [评论](#comments)
- [特殊字符](#special-characters)
- [代码块](#code-blocks)
- [学术论文常见模式](#common-patterns-for-academic-papers)
  - [标题和作者](#title-and-authors)
  - [摘要](#abstract)
  - [致谢](#acknowledgments)
- [学术写作技巧](#tips-for-academic-writing)
- [资源](#resources)

---

## 基本语法

### 文本格式

```typst
// Bold
*bold text*

// Italic
_italic text_

// Code/Monospace
`code text`

// Combining
*_bold and italic_*
```

### 标题

```typst
= Level 1 Heading
== Level 2 Heading
=== Level 3 Heading
==== Level 4 Heading
```

### 段落

```typst
// Normal paragraph
This is a paragraph. It will be justified if you set par(justify: true).

// Line break within paragraph
This is line one. \
This is line two.

// Paragraph break (blank line)
First paragraph.

Second paragraph.
```

### 列表

```typst
// Unordered list
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3

// Ordered list
+ First item
+ Second item
  + Nested item 2.1
  + Nested item 2.2
+ Third item

// Description list
/ Term 1: Definition 1
/ Term 2: Definition 2
```

---

## 数学

### 内联数学

```typst
The equation $x^2 + y^2 = z^2$ is the Pythagorean theorem.

Variables $a$, $b$, and $c$ are defined as...
```

### 显示数学

```typst
// Centered display math
$ x = (a + b) / 2 $

// Equation numbering must be enabled first; the label only makes it
// referenceable, it does NOT auto-number on its own.
#set math.equation(numbering: "(1)")
$ y = m x + c $ <eq:line>

// Multi-line equations
$ x &= a + b \
  &= c + d $
```

### 常见的数学符号

```typst
// Greek letters
$alpha, beta, gamma, Delta, Sigma$

// Operators
$sum, product, integral, partial$

// Relations
$<=, >=, !=, approx, equiv$

// Fractions
$a/b$ or $(a)/(b)$

// Subscripts and superscripts
$x_i, x^2, x_i^2$

// Functions
$sin(x), cos(x), log(x), exp(x)$

// Matrices
$ mat(
  a, b;
  c, d
) $

// Cases
$ f(x) = cases(
  0 "if" x < 0,
  1 "if" x >= 0
) $
```

---

## 图表

### 人物

```typst
// Basic figure
#figure(
  image("figure.png", width: 80%),
  caption: [Description of the figure.]
) <fig:example>

// Figure with multiple images
#figure(
  grid(
    columns: 2,
    gutter: 1em,
    image("fig1.png"),
    image("fig2.png"),
  ),
  caption: [Two subfigures side by side.]
) <fig:comparison>

// Reference in text
As shown in @fig:example, the method...
```

### 表格

```typst
// Basic table
#figure(
  table(
    columns: 3,
    [*Method*], [*Accuracy*], [*Time*],
    [Baseline], [85.2%], [10ms],
    [Ours], [92.1%], [12ms],
  ),
  caption: [Comparison of methods.]
) <tab:results>

// Table with alignment
#figure(
  table(
    columns: (auto, 1fr, 1fr),
    align: (left, center, center),
    [*Method*], [*Accuracy*], [*Time*],
    [Baseline], [85.2%], [10ms],
    [Ours], [92.1%], [12ms],
  ),
  caption: [Results with custom alignment.]
) <tab:aligned>

// Reference in text
@tab:results shows the comparison...
```

---

## 引文和参考文献

### 引文

```typst
// Single citation
According to @smith2020, the method...

// Multiple citations
Recent studies @smith2020 @jones2021 @wang2022 show...

// Citation in parentheses
The method has been studied extensively (@smith2020, @jones2021).

// Suppress author name (Typst uses #cite with a form, NOT a bare "[1]")
The method #cite(<smith2020>, form: "normal") shows...
// (Bare "[1]" is just literal text, not a Typst citation.)
```

### 参考书目

```typst
// BibTeX file
#bibliography("references.bib", style: "ieee")

// Hayagriva YAML file
#bibliography("references.yml", style: "apa")

// Multiple files
#bibliography(("refs1.bib", "refs2.bib"), style: "ieee")
```

### 引文样式

```typst
// IEEE (numeric)
#bibliography("refs.bib", style: "ieee")

// APA (author-year)
#bibliography("refs.bib", style: "apa")

// Chicago
#bibliography("refs.bib", style: "chicago-author-date")

// MLA
#bibliography("refs.bib", style: "mla")

// GB/T 7714-2015 (Chinese). Built-in ids: gb-7714-2015-numeric /
// -author-date / -note (GB/T 7714-2025 has no built-in hayagriva style yet).
#bibliography("refs.bib", style: "gb-7714-2015-numeric")
```

---

## 页面设置

### 基本页面配置

```typst
#set page(
  paper: "a4",              // or "us-letter"
  margin: 2.5cm,            // all sides
  // or
  margin: (x: 2.5cm, y: 3cm),  // horizontal and vertical
  // or
  margin: (top: 3cm, bottom: 3cm, left: 2.5cm, right: 2.5cm),
)
```

### 两栏布局

```typst
// `#set page(columns: 2)` sets the column count. `column-gutter` is NOT a
// page parameter; control the inter-column gap with the columns() function.
#set page(
  paper: "us-letter",
  margin: 1in,
  columns: 2,
)

// To customize the gutter, wrap the body:
#columns(2, gutter: 0.33in)[
  // body content
]
```

### 页眉和页脚

```typst
#set page(
  header: [
    #set text(8pt)
    #smallcaps[Conference Name 2024]
    #h(1fr)
    Draft Version
  ],
  footer: [
    #set text(8pt)
    #h(1fr)
    #counter(page).display("1")
    #h(1fr)
  ]
)
```

---

## 文本格式

### 字体设置

```typst
#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

// Chinese font
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  size: 12pt,
  lang: "zh",
  region: "cn"
)

// Multiple fonts (fallback)
#set text(
  font: ("Linux Libertine", "Times New Roman", "Arial")
)
```

### 段落设置

```typst
#set par(
  justify: true,              // Justify text
  leading: 0.65em,            // Line spacing
  first-line-indent: 1.5em,   // First line indent
  spacing: 0.65em             // Space between paragraphs
)
```

### 标题设置

```typst
// Numbered headings
#set heading(numbering: "1.1")

// Custom heading style
#show heading.where(level: 1): it => {
  set text(size: 14pt, weight: "bold")
  block(above: 1.5em, below: 1em, it)
}
```

---

## 交叉参考

### 标签

```typst
// Label a figure
#figure(...) <fig:example>

// Label an equation
$ x = y + z $ <eq:sum>

// Label a section
= Introduction <sec:intro>

// Label a table
#figure(table(...)) <tab:results>
```

### 参考

```typst
// Reference a figure
As shown in @fig:example, ...

// Reference an equation
Equation @eq:sum defines...

// Reference a section
See @sec:intro for details.

// Reference a table
@tab:results presents the results.

// Custom reference text
See #ref(<fig:example>, supplement: [Figure])
```

---

## 函数和变量

### 定义变量

```typst
#let author = "John Smith"
#let title = "My Paper Title"

// Use variables
#author wrote #title.
```

### 定义函数

```typst
#let emphasis(body) = {
  text(weight: "bold", fill: blue, body)
}

// Use function
This is #emphasis[important].
```

### 条件内容

```typst
#let draft = true

#if draft [
  *DRAFT VERSION*
]

#if not draft [
  Final version content
]
```

---

## 显示规则（样式）

### 样式标题

```typst
#show heading.where(level: 1): it => {
  set text(size: 16pt, weight: "bold")
  block(above: 1.5em, below: 1em, it)
}

#show heading.where(level: 2): it => {
  set text(size: 14pt, weight: "bold")
  block(above: 1.2em, below: 0.8em, it)
}
```

### 样式链接

```typst
#show link: it => {
  set text(fill: blue)
  underline(it)
}
```

### 风格人物

```typst
#show figure: it => {
  set align(center)
  it
}
```

---

## 评论

```typst
// Single-line comment

/* Multi-line
   comment */

// Comments are ignored during compilation
```

---

## 特殊字符

```typst
// Non-breaking space
word~word

// Em dash
word---word

// En dash
word--word

// Ellipsis
word...

// Quotes
"double quotes"
'single quotes'
```

---

## 代码块

````typst
// Inline code
The function `main()` is the entry point.

// Code block
```python
定义你好（）：
print("你好，世界！")
```
````

---

## 学术论文的常见模式

### 标题和作者

```typst
#align(center)[
  #text(size: 16pt, weight: "bold")[
    Your Paper Title
  ]

  #v(0.5em)

  Author Name#super[1], Co-author Name#super[2]

  #v(0.3em)

  #text(size: 10pt)[
    #super[1]University Name, #super[2]Institution Name \
    #link("mailto:author@email.com")
  ]
]
```

### 摘要

```typst
#heading(outlined: false, numbering: none)[Abstract]

Your abstract text here...

#v(0.5em)

*Keywords:* keyword1, keyword2, keyword3
```

### 致谢

```typst
#heading(outlined: false, numbering: none)[Acknowledgments]

This work was supported by...
```

---

## 学术写作技巧

1. **一致地使用标签**：`<fig:name>`, `<tab:name>`, `<eq:name>`, `<sec:name>`
2. **保持数字可读**：使用 `width: 80%` 或类似的
3. **数字方程**：重要方程使用 `$ ... $ <eq:label>`
4. **一致的格式**：开头使用 `#set` 规则
5. **模块化内容**：对大型文档使用 `#include "section.typ"`
6. **版本控制**：Typst 文件是纯文本，非常适合 Git

---

## 资源

- [打字员文档](https://typst.app/docs/)
- [Typst Universe](https://typst.app/universe/) - 模板和包
- [打字教程](https://typst.app/docs/tutorial/)
- [打字员参考](https://typst.app/docs/reference/)
