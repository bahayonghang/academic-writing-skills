# Subsection Context Protocol

This is the paper-audit mirror of the canonical subsection-context contract in
`academic-writing-skills/latex-thesis-zh/references/writing/subsection-context-zh.md`.
The marked block is synchronized by contract tests.

<!-- S-CTX-CONTRACT:BEGIN -->
## 小节上下文契约

小节深度定义为 `depth = level - root_level + 1`，其中 `root_level` 是文档内标题的最小层级；
`depth == 3` 才构成 `x.x.x` 小节单元。无 depth-3 不回退：单元列表为空，只输出声明，
不把 depth-2 标题替代为小节。

| 码 | 可复算信号 | 人工复核问题 |
| --- | --- | --- |
| `S-CTX-IN` | current 首段未命中承接标记，且与证据侧末句的端点 Jaccard 严格小于 `0.0200` | 本小节是否需要承接上一小节的结论或产出？ |
| `S-CTX-OUT` | current 末段未命中前瞻/收束标记，且 `next.head` 首句未命中回指标记 | 本小节是否需要为下一小节交出输入或问题？ |
| `S-CTX-ROLE` | current 首段未命中定位标记，也未复用父标题关键词 | 本小节在父节 `x.x` 中承担什么角色？ |

只有 current 可产出改写建议；prev.tail、next.head、parent_lead 一律只读，仅作证据。
<!-- S-CTX-CONTRACT:END -->
