# NeurIPS / ICML / ICLR (Typst)

> 从 `references/VENUES.md` 中提取的特定于期刊或会议的快照。这三个
> ML 会议对 Typst 工具链抱有最多的期望；期刊或会议-
> 特定的增量（页数、影响更广泛的部分）位于源代码中
> `VENUES.md` 快速参考表。用户使用时直接加载该文件
> 将 NeurIPS / ICML / ICLR 命名为目标期刊或会议，而不是阅读
> 完整的期刊或会议目录。

## 格式要求

- **页数限制**：9 页（不包括参考文献）
- **论文尺寸**：美国信函
- **列**：单列
- **字体**：Times New Roman 10pt
- **边距**：所有边均为 1 英寸
- **行距**：单行距

## 打字机配置

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

## 写作风格

- **匿名提交**：删除作者信息以供审核
- **数字**：高质量、灰度可读
- **代码**：仅补充材料
- **可重复性**：包括实施细节

## 特殊要求

- **更广泛的影响声明**：NeurIPS 所需
- **检查表**：完整的再现性检查表
- **补充材料**：单独的 PDF
