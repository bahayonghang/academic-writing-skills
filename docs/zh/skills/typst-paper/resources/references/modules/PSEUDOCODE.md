# 模块：伪代码审查

**触发条件**：Typst algorithm、algorithmic、algorithm-figure、lovelace、伪代码块、算法流程排版

## 命令

```bash
uv run python -B scripts/check_pseudocode.py main.typ --venue ieee
uv run python -B scripts/check_pseudocode.py main.typ --venue ieee --json
```

## IEEE 安全默认值

- 对于 IEEE 风格的伪代码输出，首选 Typst `algorithmic` 包，因为它提供图形包装、图题处理、行号和常规控制流渲染。
- 对于类似 IEEE 的输出，首选 `algorithm-figure(...)`。
- 将 `lovelace` 视为自定义语法的灵活后备，而不是默认建议。
- 如果 `lovelace` 用于 IEEE 风格投稿，应将输出包装在 `#figure(...)` 中并添加图题。
- 建议行号是为了方便查看，但不被视为硬性 IEEE 要求。
- 注释应保持简短，段落级解释移至周围正文。

## 该模块检查什么

- 在类似 IEEE 的上下文中缺少 `algorithm-figure(...)` 或缺少图形包装器
- 缺少 `style-algorithm`
- 缺少图题
- 缺少行号（仅供参考）
- 过长的注释行
- 本应放入正文的段落式算法行

## 产出政策

- 首先报告类似 IEEE 的硬布局风险。
- 区分 `mandatory` 与 `recommended`。
- 除非用户明确要求进行源代码编辑，否则请保持 Typst 标签、参考文献和数学完整。
