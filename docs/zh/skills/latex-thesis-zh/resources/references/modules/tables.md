# 模块：表格

**触发词**：table、表格、三线表、three-line、booktabs、tabular、data table、generate table、table format

## 命令

```bash
uv run python -B scripts/check_tables.py main.tex
uv run python -B scripts/check_tables.py main.tex --fix-suggestions
uv run python -B scripts/check_tables.py main.tex --json
uv run python -B scripts/generate_table.py data.csv --style booktabs --bilingual
uv run python -B scripts/generate_table.py data.json --style booktabs
```

## 详细说明

**check_tables.py**：扫描文档中的所有 `table` / `table*` 环境。检查：
- 三线表规则合规性（只能使用 toprule / midrule / bottomrule）
- 列格式中是否存在竖线
- 表题位置（必须位于 `\begin{tabular}` 之前）
- 表注格式（“Note.”或“注：”）
- 同一列中的数值精度一致性
- 导言区是否加载 `booktabs` 宏包

**generate_table.py**：把结构化数据（CSV 或 JSON）转换为可发表的表格代码：
1. Markdown 预览（stdout）
2. LaTeX `booktabs` 代码
3. 双语表题建议（指定 `--bilingual` 时）
4. Word 转换提示

技能层响应：把脚本输出转换为 `% TABLES (Line N) [Severity] [Priority]: ...` 发现。

另见：[table-guide.md](../formatting/table-guide.md) 中的完整三线表规范。
双语图/表标题措辞参见 [caption-guide.md](../formatting/caption-guide.md)。
