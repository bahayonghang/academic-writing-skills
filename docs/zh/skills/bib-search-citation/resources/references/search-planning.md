# 检索规划默认值与紧凑操作符

## 默认值

除非用户另有说明，否则使用以下默认值：

- 研究发现请求 -> `sort: relevance`
- 未明确数量上限 -> `limit: 5`
- 未明确字段列表 -> 返回 `key`、`title`、`shorttitle`、`author`、`year`、
  `venue`、`doi`、`eprint`、`keywords`、`annotation` 和 `abstract`
- 请求“original”“full entry”或“bib” -> `include_raw_bib: true`
- 在 LaTeX/Typst 混合工作流中请求引用片段 -> `citation_mode: both`

## 支持的紧凑操作符

- `author:cheng`
- `year>=2024`、`year<=2025`、`year:2024`、`year:2023,2024`
- `type:article,misc`、`-type:misc`
- `has:code,doi`、`-has:pdf`
- `annotation:CodeAvailable`、`keywords:mamba`、`abstract:photovoltaic`
- `sort:year_desc`、`limit:10`、`fields:key,title,year,doi`
- `cite:latex`、`cite:typst`、`cite:both`、`cite:none`
- `raw:true`
- `recent:3`（用于附加 `meta.recency` 报告的时间窗口；也可用 `--recent-window`）
- `claim:"..."`（为每条结果增加 `claim_support`；包含空格的 claim 优先使用 `--claim`）

有用的 `has` 值包括 `doi`、`abstract`、`keywords`、`annotation`、
`shorttitle`、`eprint`、`pdf` 和 `code`。当 `code` 标志涉及的 `url`、`abstract`、
`keywords`、`annotation`、`note` 或 `howpublished` 等字段提到 GitHub、GitLab、
code、repository 或 source 时，脚本会自动推断该标志。
