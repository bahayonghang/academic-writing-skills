# 示例：导出原始 BibTeX

## 用户提示词

`Find the best TimeMachine match in references.bib and return one raw entry plus cite snippets.`

## 推荐模块

`query`

## 检索映射

- 主题查询：`TimeMachine`
- 原始导出：`raw:true`
- 引用模式：`cite:both`
- 结果上限：`1`

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/search_bib.py --bib references.bib --query 'TimeMachine raw:true cite:both limit:1'
```

## 预期输出

- 首条匹配结果包含从源文件解析得到且保持原样的 `raw_bib`。
- 结果包含 LaTeX 和 Typst 引用片段。
- 回答不会重写、规范化或虚构缺失的元数据。
