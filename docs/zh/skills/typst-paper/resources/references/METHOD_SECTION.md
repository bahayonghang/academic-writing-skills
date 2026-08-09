# Typst 方法部分适配

> **权威契约：** `latex-paper-en/references/writing/section-writing/method.md`。
> 方法接口、公式完整性、标题、证据和改写规则均从该文件加载。本文件只说明 Typst 语法与
> 命令差异。

## 语法映射

| 契约对象 | Typst 形式 | 边界 |
| --- | --- | --- |
| 模块小节 | `== Encoder` 或 `=== Alignment` | 每个标题只承载一个技术单元 |
| 行内小标题 | `*Input contract.*` | 只负责导航；后续正文负责说明接口 |
| 被引用的块公式 | `$ ... $ <eq:aligned>` | label 表明脚本需要检查后续 `where` 释义 |
| 源码注释 | `// ...` | 诊断使用 Typst 注释，并保持源码 token 不变 |

## 相邻边表

改写过渡前，为每对相邻模块填写一行：

| 上游模块 | 上游输出 | 连接类型 | 中间变换 | 下游用途 |
| --- | --- | --- | --- | --- |
| `== Encoder` | `z_enc` | 串行数据 | `project(z_enc)` | `== Decoder` 的直接输入 |
| `== Candidate generator` | `candidates` | 校准/选择 | 阈值与预算筛选 | 加权监督 |

当表格覆盖每对相邻的 `==`/`===` 小节，且每一行都通过权威契约中的
「生产者-变换-使用者」检查时，Typst 适配才算完成。

## 诊断

```bash
uv run python scripts/analyze_logic.py main.typ --section methods
```

该命令只报告 `[Script]` 候选。根据权威契约复核 `M-HEADING`、`M-SEQWORD` 和
`M-EQUATION`，然后在编辑前填写脚本输出的 `M-EDGETABLE`。
