# 模块：表格

**触发器**：表格、表格、三线表、三行、booktabs、表格、数据表、生成表、表格格式

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ --fix-suggestions
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ --json
uv run python -B $SKILL_DIR/scripts/generate_table.py data.csv --style booktabs --bilingual
uv run python -B $SKILL_DIR/scripts/generate_table.py data.json --style plain
```

## 细节

**check_tables.py**：扫描 Typst 源中的 `table(...)` 调用。检查：

- 三行规则合规性（`table.hline`规则，没有`table.vline`)
- 垂直线存在（标记为 `table.vline`）
- `stroke: none` 在具有显式 hlines 的表上（三行习惯用法）
- 列内数字精度一致性

`--fix-suggestions`为每个发现附上具体的修复方法；`--json`发出
原始问题列表。

**generate_table.py**：将结构化数据（CSV或JSON）转换为
可供出版的 Typst 表代码：

1. Markdown 预览（标准输出）
2. 打字机`table(...)`代码 -`--style booktabs`（三行，默认）或
`--style plain`（全格）
3. 双语字幕建议（如果 `--bilingual`）
4. 统计显着性注释（如果 `--stats`）
5. 单词转换技巧

技能层响应：将脚本输出转换为 `// TABLES (Line N) [Severity] [Priority]: ...` 结果。

另请参阅：[TABLE_GUIDE.md](../TABLE_GUIDE.md) 了解完整的三行表规范。
