# 模块：参考文献

**触发条件**：参考文献、交叉引用、引用、图表引用、标签、编号、未定义引用、缺少图题

## 命令

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.typ
uv run python $SKILL_DIR/scripts/check_references.py main.typ --bib references.bib
uv run python $SKILL_DIR/scripts/check_references.py main.typ --json
```

> 可用标志：`--bib`（用于解析引用键的参考书目文件）、
> `--json`。省略 `--bib` 时，脚本会自动检测源文件中的
> `#bibliography("...")`。

## 细节

`check_references.py` 验证 Typst 论文中的图、表和公式交叉引用。
在 Typst 中，`@key` 既可能是文献引用，也可能是交叉引用，因此
检查器会将每个 `@key` 与以下内容核对：

- 源文件中找到的 `<key>` 标签定义；
- 参考书目键集合（来自 `--bib` 或自动检测到的 `#bibliography(..)`）；

仅当某个引用既不是已知标签，也不是已知文献引用时，才将其标记为未定义。
冒号式标签（`<fig:arch>`、`@fig:arch`）会被解析为一个完整 token。

检查：

- 未定义的引用或文献引用（Critical，P0）
- 未被引用的 `fig`/`tab`/`eq` 标签（Minor，P2）
- `#figure(...)` 块缺少图题，同时识别 `caption: [..]` 和
  `caption: "..."` 两种形式（Major，P1）
- 先引用后定义的顺序问题（Minor，P2）
- 编号标签序列存在缺号（Minor，P2）

技能层响应：将结果呈现为 `// REFERENCES (Line N) [Severity] [Priority]: ...`。
