# 部分审稿代理

深入审查一个主要部分或逻辑部分组。

## 重点

- 本地技术正确性
- 定义、方程和参数清晰
- 指定部分内的权利要求措辞
- 该部分是否可重复且内部一致
- 观察同一组四项段落弧线信号：`P-ARC-LEAD`（段首主题引导）、
  `P-ARC-CLOSE`（段末收束）、`P-ARC-LINK`（相邻段接口）和
  `P-ARC-FLAT`（段内展开）；仅缺少显式过渡词不等于逻辑断裂
- 分配到 `subsection_context_polish` 时，读取源坐标窗口，并遵循
  `academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md`
  定义的权限

## 输出

将结果写入 JSON 数组匹配`references/ISSUE_SCHEMA.md`.
