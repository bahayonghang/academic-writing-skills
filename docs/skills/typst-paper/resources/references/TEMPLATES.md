# Typst Academic Template Example

## Table of contents

- [IEEE Template](#ieee-模板)
- [ACM Template](#acm-模板)
- [General English Template](#通用英文模板)
- [Chinese paper template](#中文论文模板)
- [Usage Tips](#使用提示)

## IEEE template

```typst
#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (
    (
      name: "Author Name",
      department: [Department],
      organization: [University],
      location: [City, Country],
      email: "author@email.com"
    ),
  ),
  abstract: [
    Your abstract here...
  ],
  index-terms: ("Machine Learning", "Deep Learning"),
  bibliography: bibliography("references.bib"),
)

// Your content here
```

## ACM template

```typst
// 使用 ACM 两栏格式
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(font: "Linux Libertine", size: 9pt)
#set par(justify: true)
```

## Universal English template

```typst
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm)
)

#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

#set heading(numbering: "1.1")

// 标题
#align(center)[
  #text(size: 16pt, weight: "bold")[Your Paper Title]

  #v(0.5em)

  Author Name#super[1], Co-author Name#super[2]

  #v(0.3em)

  #text(size: 10pt)[
    #super[1]University Name, #super[2]Institution Name
  ]
]

// 摘要
#heading(outlined: false, numbering: none)[Abstract]
Your abstract here...

// 正文
= Introduction
Your content here...
```

## Chinese paper template

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

// 标题
#align(center)[
  #text(size: 18pt, weight: "bold")[论文标题]

  #v(0.5em)

  作者姓名#super[1]，合作者姓名#super[2]

  #v(0.3em)

  #text(size: 10.5pt)[
    #super[1]大学名称，#super[2]机构名称
  ]
]

// 摘要
#heading(outlined: false, numbering: none)[摘要]
摘要内容...

*关键词*：关键词1；关键词2；关键词3

// 正文
= 引言
正文内容...
```

## Usage tips

- If using the Typst Universe package, please confirm that the network is available and fix the version number.
- It is recommended that Chinese templates be configured with Western fonts at the same time to ensure consistent display of English and numbers.
- If the target journal provides an official template, use the official template first and fine-tune it according to its guidelines.
