# IEEE 会议和期刊 (Typst)

> 这是从 `references/VENUES.md` 提取的期刊/会议专项快照。
> 当用户指定 IEEE 为目标投稿场所时，直接加载此文件，无需读取完整目录。

## 格式要求

- **论文尺寸**：US Letter (8.5" × 11")
- **列**：两列格式
- **柱宽**：3.5 英寸（8.89 厘米）
- **柱间距**：0.33 英寸（0.84 厘米）
- **边距**：顶部/底部 0.75 英寸，左侧/右侧 0.625 英寸
- **字体**：Times New Roman 10pt
- **行距**：单行距

## 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: (top: 0.75in, bottom: 0.75in, left: 0.625in, right: 0.625in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(
  font: "Times New Roman",
  size: 10pt
)

#set par(justify: true, leading: 0.55em)
```

## 写作风格

- **语音**：主动语音优先
- **时态**：方法的过去时，结果的现在时
- **图**：文字中为“图 1”，标题为“图 1”
- **表格**：罗马数字（表 I、表 II）
- **方程式**：连续编号

## 引文风格

- 方括号中的数字引用：[1]、[2-4]
- IEEE 参考格式

## 模板

```typst
#import "@preview/charged-ieee:0.1.4": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (...),
  abstract: [...],
  index-terms: ("Keyword1", "Keyword2"),
  bibliography: bibliography("refs.bib", style: "ieee"),
)
```

## 伪代码

- IEEE 风格的 Typst 伪代码优先使用 `algorithmic` 包，因为它提供 `algorithm-figure`、图题支持和常规控制流渲染。
- 当用户明确想要更自由的语法时，将 `lovelace` 视为灵活的后备方案。
- 在 IEEE 风格输出中，将伪代码包装在带图题的 `algorithm-figure(...)` 或 `#figure(...)` 中。
- 建议行号是为了方便审查，但此处并不将其作为 IEEE 硬规则强制执行。
- 保持评论简短并将段落级解释移回到正文中。
