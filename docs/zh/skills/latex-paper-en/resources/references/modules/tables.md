# 模块：表格

**触发器**：表格、表格、三线表、三行、booktabs、表格、数据表、生成表、表格格式

## 命令

```bash
uv run python -B scripts/check_tables.py main.tex
uv run python -B scripts/check_tables.py main.tex --fix-suggestions
uv run python -B scripts/check_tables.py main.tex --json
uv run python -B scripts/generate_table.py data.csv --style booktabs --bilingual
uv run python -B scripts/generate_table.py data.json --style booktabs
```

## 细节

**check_tables.py**：扫描所有`table` / `table*`文档中的环境。检查：
- 三行规则合规性（仅顶部规则/中间规则/底部规则）
- 色谱柱规格中存在垂直线
- 标题位置（必须位于 `\begin{tabular}` 之前）
- 表注格式（“注.”或“注：”）
- 列内数字精度一致性
- `booktabs` 包已加载到序言中

**generate_table.py**：将结构化数据（CSV 或 JSON）转换为可发布的表代码：
1. Markdown 预览（标准输出）
2. LaTeX `booktabs` 代码
3. 双语字幕建议（如果 `--bilingual`）
4. 单词转换技巧

技能层响应：将脚本输出转换为 `% TABLES (Line N) [Severity] [Priority]: ...` 结果。

另请参阅：[table-guide.md](../formatting/table-guide.md) 了解完整的三行表规范。
