# `bib-search-citation`

从一个本地 BibTeX/BibLaTeX `.bib` 文献库中检索并生成引用，支持带自定义元数据
字段的 Zotero 导出。

## 适用场景

- 按主题、作者、年份、venue、DOI、arXiv/eprint、keywords、annotation 或 abstract 检索。
- 组合 `year>=2024`、`has:code`、`cite:both` 等紧凑过滤条件。
- 返回稳定 JSON、精确原始 BibTeX 或 LaTeX/Typst 引用片段。
- 把保存的 JSON 结果预览成紧凑、便于阅读的摘要。
- 添加词汇级 claim 重叠和时效元数据，交给后续验证。

## 不适用场景

- 检查论文中已经使用的引用；请用对应写作技能的 bibliography 模块。
- 编译、格式化或改写 `.tex` 或 `.typ` 工程。
- 在没有本地 `.bib` 文件时做在线发现。
- 把文献库命中或词汇重叠当作论文支持 claim 的证明。
- 虚构源文献库中缺失的元数据。

## 模块路由

| 模块 | 适用场景 | 主命令 |
| --- | --- | --- |
| `query` | 使用内联过滤的一次性紧凑检索 | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query 'mamba forecasting author:Cheng year>=2024 has:code cite:both limit:5'` |
| `spec-json` | 复杂请求需要显式结构化过滤 | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --spec-json '{"query":"mamba forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | 保存的检索需要重复执行 | `uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --spec-file search.json` |
| `preview` | 已有检索 JSON，需要短摘要 | `uv run python -B academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## 最小输入

- 一个本地 `.bib` 路径。
- 一个紧凑 `--query`、内联 `--spec-json` 或保存的 `--spec-file`。
- 可选排序、数量上限、返回字段、引用模式、原始导出、时效窗口或 claim 偏好。

## 首条命令

```bash
uv run python -B academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib references.bib --query 'transformer forecasting year>=2024 has:doi cite:both limit:5'
uv run python -B academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json
```

`search_bib.py` 负责解析、过滤、评分、排序、原始条目保留和引用生成。
`preview_bib_search.py` 只渲染已有 JSON。

## 输出产物

- 包含解释后过滤条件和匹配条目的结构化 JSON。
- 请求的文献字段与来源标识。
- 可选的精确 `raw_bib`。
- 可选的 LaTeX 和 Typst 引用片段。
- 附加 `meta.recency` 和逐条 `claim_support`，并明确给出限制说明。

## 公开资源

### 参考资料

- [查询语法](./resources/references/query-syntax.md)
- [检索规划默认值](./resources/references/search-planning.md)
- [已知限制与错误](./resources/references/limitations-and-errors.md)

### 示例

- [紧凑查询](./resources/examples/compact-query.md)
- [原始 BibTeX 导出](./resources/examples/raw-bib-export.md)
- [预览摘要](./resources/examples/preview-summary.md)

## 常见请求与交接

本技能负责本地检索和可直接使用的引用输出。当需要检查论文源码中的引用时，交给对应
写作技能；当需要阅读论文内容并判断它是否支持 claim 时，交给研究验证工作流。
