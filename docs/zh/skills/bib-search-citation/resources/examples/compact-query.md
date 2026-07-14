# 示例：紧凑查询检索

## 用户提示词

`Search references.bib for Cheng papers after 2024 on Mamba forecasting and return both LaTeX and Typst citations.`

## 推荐模块

`query`

## 检索映射

- 主题查询：`mamba forecasting`
- 作者过滤：`Cheng`
- 年份过滤：`year>=2024`
- 推断字段：`has:code`
- 引用模式：`cite:both`
- 结果上限：`5`

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/search_bib.py --bib references.bib --query 'mamba forecasting author:Cheng year>=2024 has:code cite:both limit:5'
```

## 预期输出

- JSON `meta.applied_filters` 显示解释后的作者、年份和 `has` 过滤条件。
- 每条返回记录包含文献字段以及 LaTeX 和 Typst 两种引用片段。
- 如果没有匹配项，响应会建议优先放宽哪些过滤条件。
