# ACM 会议和期刊 (Typst)

> 从 `references/VENUES.md` 中提取的特定于期刊或会议的快照。加载这个
> 当用户将 ACM 指定为目标期刊或会议时直接文件，而不是
> 阅读完整的期刊或会议目录。

## 格式要求

- **论文尺寸**：US Letter 或 A4
- **列**：两列格式
- **字体**：Linux Libertine 或类似字体
- **字体大小**：9-10pt
- **边距**：左/右 0.75 英寸，顶部/底部 1 英寸

## 打字机配置

```typst
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
)
// column-gutter is not a #set page parameter; use #columns(2, gutter: 0.33in)[..]

#set text(
  font: "Linux Libertine",
  size: 9pt
)

#set par(justify: true)
```

## 写作风格

- **时态**：一般真理的现在时
- **数字**：始终如一的“图 1”
- **表**：“表 1”一致
- **引文**：数字或作者年份取决于地点

## 引文样式

- **数字**：[1], [2, 3]
- **作者年份**：（Smith 等人，2020）
