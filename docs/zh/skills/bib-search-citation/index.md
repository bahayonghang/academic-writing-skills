# `bib-search-citation`

面向 BibTeX / BibLaTeX 的 `.bib` 文献库快速检索与引用提取技能，支持带有 Zotero 自定义字段的大型文献库。

## 适用场景

- 按主题词和字段过滤检索大型 `.bib` 文献库。
- 按作者、年份、类型、DOI、arXiv/eprint、PDF、代码、keywords、annotation 或 abstract 过滤。
- 生成 LaTeX 和 Typst 引用片段。
- 返回原始 BibTeX 便于导出或人工复核。
- 把 JSON 检索结果预览成紧凑摘要。

## 不适用场景

- 检查 `.tex` 或 `.typ` 项目中已经使用的引用；请用对应写作技能的 bibliography 模块。
- 编译、格式或修改论文。
- 改写 Related Work 正文。
- 没有本地文献库时做在线检索。
- 把 citation key 当成论文 claim 已被支撑的证据。

## 模块路由

| 入口 | 适用场景 | 主命令 |
| --- | --- | --- |
| `query` | 一次性紧凑检索 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"` |
| `spec-json` | 结构化过滤比紧凑查询更清晰 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-json '{"query":"mamba forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | 需要复用保存的检索配置 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-file search.json` |
| `preview` | 已有 JSON 结果，需要短摘要 | `uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## 最小输入

- 一个本地 `.bib` 文件路径。
- 紧凑 `--query`、内联 `--spec-json` 或保存的 `--spec-file`。
- 可选排序、数量上限、citation mode、raw BibTeX 或返回字段偏好。

## 输出产物

- 结构化 JSON 检索结果。
- 可选原始 BibTeX 条目。
- LaTeX 和/或 Typst 引用片段。
- 由 `preview_bib_search.py` 渲染的紧凑摘要。

## 常见请求

```text
在 references.bib 里找 2024 年后的 Cheng + Mamba 时序预测论文，并返回 LaTeX 和 Typst 引用。
```

```text
找出 annotation 包含 CodeAvailable 的条目，并显示原始 BibTeX。
```

```text
列出最新 transformer 时序预测论文，要求有 DOI 并排除 misc。
```

```text
找到最像 TimeMachine 的条目，返回一条原始 BibTeX 和引用片段。
```
