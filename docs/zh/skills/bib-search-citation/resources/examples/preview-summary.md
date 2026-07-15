# 示例：预览摘要

## 用户提示词

`Search my Zotero-exported library for photovoltaic forecasting entries, then show me a compact human-readable summary.`

## 推荐模块序列

1. `query`
2. `preview`

## 命令

```bash
uv run python -B $SKILL_DIR/scripts/search_bib.py --bib references.bib --query 'photovoltaic forecasting cite:both limit:5' > results.json
uv run python -B $SKILL_DIR/scripts/preview_bib_search.py --input results.json
```

## 预期输出

- `search_bib.py` 生成作为事实来源的机器可读 JSON。
- `preview_bib_search.py` 渲染简短摘要，不暴露原始 BibTeX。
- 最终回答把过滤与评分说明严格锚定到 JSON payload。
