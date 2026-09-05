# 模块：表格

**触发词**：table, 表格, 三线表, three-line, booktabs, tabular, data table, generate table, table format

## 命令

```bash
uv run python -B scripts/check_tables.py main.tex
uv run python -B scripts/check_tables.py main.tex --fix-suggestions
uv run python -B scripts/check_tables.py main.tex --json
uv run python -B scripts/generate_table.py data.csv --style booktabs --bilingual
uv run python -B scripts/generate_table.py data.json --style booktabs
```

## 详细说明

**check_tables.py**：扫描文档中的所有 `table` / `table*` 环境，检查：
- 三线表规则（只使用 toprule / midrule / bottomrule）
- 列格式中是否存在竖线
- 题注位置（真实 `\caption` / `\bicaption` 必须位于 `\begin{tabular}` 之前）
- 表注格式（"Note." 或“注：”）
- 同一列内数值精度是否一致
- 导言区是否加载 `booktabs` 宏包

**generate_table.py**：把结构化数据（CSV 或 JSON）转换为可用于论文的表格代码：
1. Markdown 预览（stdout）
2. LaTeX `booktabs` 代码
3. 双语题注建议（使用 `--bilingual` 时）
4. Word 转换提示

Skill 层响应：把脚本输出转换成 `% TABLES (Line N) [Severity] [Priority]: ...` 问题记录。

完整三线表规范见 [table-guide.md](../formatting/table-guide.md)。
检查器识别 `\caption` / `\bicaption` 命令后的可选短标题、空白和换行；注释及
`\captionsetup` 等相似命令不能满足题注检查。检查器只报告存在性和位置，长表间距、
二次缩放及编译页验收仍按表格指南人工复核。
双语（`\bicaption`）图表题措辞见 [caption-guide.md](../formatting/caption-guide.md)。
