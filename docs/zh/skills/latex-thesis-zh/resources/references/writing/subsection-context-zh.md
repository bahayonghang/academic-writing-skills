# 中文学位论文小节上下文接口

本指南定义 `analyze_logic.py --subsection-context` 的小节游标、跨标题接口观察与只读窗口。
这些观察只提供人工复核入口，不自动改写论文正文。

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

## 合格段与缺省语义

`SUBSECTION_CONTEXT_MIN_HAN = 20` 是构造性下限：小节入口常是一至两句定位文本，若沿用
`PARAGRAPH_ARC_MIN_HAN = 40` 会系统性漏掉合法接口；低于 20 个汉字的碎片又不足以稳定承担
承接、交棒或定位角色。可见文本中的汉字占比还必须不低于 `0.30`。

本检查器有意不复用 `_arc_is_eligible`。两者唯一的结构性分歧是：小节上下文保留
`is_heading_lead`，因为标题后的第一个合格段正是 `current` 与 `next.head` 的观察对象；列表项、
以受保护环境收尾的段落以及摘要、结论、致谢、附录、组织结构和小结范围仍然排除。

相邻单元存在但没有合格段时，对应部件不进入 `read_only`，并标记
`no_eligible_paragraph`；该侧依赖的 finding 不产出。文档不存在 depth-3 标题时，固定声明为：

```text
% 小节级：本文档无 depth-3 标题，未产出小节级观察。
```

## 命令与窗口

```bash
uv run python scripts/analyze_logic.py main.tex --subsection-context
uv run python scripts/analyze_logic.py main.tex --subsection-context --subsection 2.1.1
uv run python scripts/analyze_logic.py main.tex --emit-window --subsection 2.1.1
```

`--emit-window` 只打印部件名、源文件、文件内行号和可改/只读标记，不复制正文。多文件论文先
通过 `tex_loader.py` 装配，再把 assembled 行号映射回 `chapters/*.tex` 等真实源文件。
