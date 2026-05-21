# `bib-search-citation`

面向 BibTeX / BibLaTeX 的 `.bib` 文献库快速检索与引用提取技能。

## 适用场景

- 按主题检索大型 `.bib` 文献库
- 按作者、年份、类型、DOI、arXiv、keywords、annotation、abstract 过滤条目
- 从命中文献直接生成 LaTeX / Typst 引用片段
- 返回原始 BibTeX 便于导出或人工复核
- 清洗和筛选 Zotero 导出的混合字段文献库
- 检查哪些条目带有代码、PDF、DOI、keywords 或 abstract

## 不适用场景

- 检查 `.tex` / `.typ` 工程里的引用完整性
- 编译或格式诊断
- 代写 related work 正文
- 没有本地文献库时做在线检索

## 检索入口

| 入口 | 适用场景 | 命令 |
| --- | --- | --- |
| `query` | 一次性紧凑检索 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --query "mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:5"` |
| `spec-json` | 结构化、可复用过滤条件 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-json '{"query":"mamba time series forecasting","filters":{"year_min":2024},"citation_mode":"both"}'` |
| `spec-file` | 复用保存好的检索配置 | `uv run python academic-writing-skills/bib-search-citation/scripts/search_bib.py --bib library.bib --spec-file search.json` |
| `preview` | 把 JSON 结果压成紧凑摘要 | `uv run python academic-writing-skills/bib-search-citation/scripts/preview_bib_search.py --input results.json` |

## 最小输入

- 一个 `.bib` 文件路径
- 一条紧凑查询或一份 JSON 检索配置
- 可选的排序、数量上限和 citation mode
- 如果需要精确导出，可补充 raw BibTeX 或返回字段要求

## 推荐提示词

```text
在 references.bib 里找 2024 年后的 Cheng + Mamba 时序预测论文，并返回 LaTeX 和 Typst 引用。
```

```text
找出 library.bib 中 annotation 包含 CodeAvailable 的条目，并把原始 BibTeX 给我。
```

```text
列出 references.bib 里最新的 transformer 时序预测论文，排除 misc，并要求必须有 DOI。
```

```text
在 references.bib 里找最像 TimeMachine 的条目，返回 1 条原始 BibTeX 和引用片段。
```

## 继续阅读

- [查询语法](./resources/query-syntax.md)

## 重要说明

- `search_bib.py` 才是过滤、排序、引用格式生成的唯一真源。
- `preview_bib_search.py` 只负责把 JSON 结果渲染成更短的人工摘要。
- 紧凑过滤支持 `author:`、`year>=`、`year<=`、`type:`、`has:`、`fields:`、
  `cite:` 和 `raw:true`。
- `has:code` 会从 `url`、`annotation`、`keywords`、`note`、`howpublished`、
  `abstract` 等字段推断。
- `.bib` 命中、citation key、DOI、arXiv ID 或 URL 只是文献来源线索，
  不等于该文献已经支撑了论文中的具体论断。
- 如果查询里只有过滤条件，没有主题词，结果顺序主要由 sort 决定。
- 如果命中数量异常偏少，可能是某些 BibTeX 条目结构损坏或编码异常，导致解析时被跳过。
