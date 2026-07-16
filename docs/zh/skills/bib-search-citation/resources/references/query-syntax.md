# 查询语法指南

本参考帮助把文献检索请求映射为 `scripts/search_bib.py` 的 search spec。

## 两种受支持的输入方式

脚本同时支持以下两种方式：

1. JSON search spec
2. 紧凑查询表达式

当用户自然地写出类似以下内容时，使用紧凑形式：

```text
time series forecasting mamba author:Cheng year>=2024 has:code type:article,misc cite:both
```

当工作流已有结构化 spec，或需要明确表达多个过滤条件时，使用 JSON 形式。

## JSON search spec 结构

```json
{
  "query": "mamba time series forecasting",
  "filters": {
    "year_min": 2024,
    "year_max": 2026,
    "author_contains": ["Cheng"],
    "type_in": ["article", "misc"],
    "has": ["code", "abstract"],
    "exclude_has": ["pdf"],
    "field_contains": {
      "annotation": ["CodeAvailable"],
      "keywords": ["forecasting"]
    }
  },
  "sort": "relevance",
  "limit": 5,
  "return_fields": [
    "key",
    "title",
    "shorttitle",
    "author",
    "year",
    "venue",
    "doi",
    "eprint",
    "keywords",
    "annotation",
    "abstract"
  ],
  "include_raw_bib": true,
  "citation_mode": "both"
}
```

## 紧凑查询语言

### 核心语法

- 普通词语保留为主题查询
- `author:cheng` -> 作者包含 `cheng`
- `year>=2024` -> 最小年份为 2024
- `year<=2025` -> 最大年份为 2025
- `year:2024` -> 精确年份 2024
- `year:2023,2024` -> 年份为 2023 或 2024
- `type:article,misc` -> 条目类型为 article 或 misc
- `-type:misc` -> 排除 misc 条目
- `has:code,doi` -> 同时要求 code 和 doi
- `-has:pdf` -> 排除看起来包含 PDF 的条目
- `annotation:CodeAvailable` -> annotation 包含 `CodeAvailable`
- `keywords:mamba` -> keywords 包含 `mamba`
- `sort:year_desc` -> 最新条目优先
- `limit:10` -> 返回 10 条结果
- `fields:key,title,year,doi` -> 限制返回字段
- `cite:latex` / `cite:typst` / `cite:both`
- `raw:true` -> 包含原始 BibTeX
- `recent:3` -> 设置附加 `meta.recency` 报告的时间窗口（年）；也可使用 `--recent-window` flag
- `claim:"low-latency forecasting"` -> 为每条结果附加 `claim_support` block（仅词汇重叠）；
  对包含空格的 claim，优先使用 `--claim` flag

### 说明

- 可以自由混用多个紧凑过滤条件。
- 不匹配紧凑语法的 token 会保留在自由文本主题查询中。
- 使用 JSON spec 时，解析器也接受 `spec.query` 中的紧凑语法。
- 通用字段过滤支持多个字段，包括 `title`、`shorttitle`、`annotation`、`keywords`、
  `abstract`、`file`、`copyright`、`doi` 和 `eprint`。
- 取反的通用字段过滤写作 `-annotation:survey`。
- 任意 `word:word` token 都会被视为通用字段过滤，因此拼错的字段名（`tilte:...`）
  不会匹配任何内容；当过滤字段在所有条目中都不存在时，`meta.parse_warnings` 会发出警告。
- 如果希望检索后得到紧凑、便于阅读的摘要，应把 JSON 传给
  `scripts/preview_bib_search.py`，而不是修改查询语法。

## 时效报告与 claim 绑定（附加功能）

这两个功能都是附加功能，不会过滤或重新排序结果。

- **时效性**始终报告在 `meta.recency` 下：`window_years`、`recent_threshold`
  （根据当前日历年份计算，因此会随时间保持正确）、`with_year`、`recent_count`、
  `recent_share`，以及当窗口内结果少于 80% 时发出警告的 `note`。使用 `recent:N`
  或 `--recent-window N` 调整窗口（默认 3）。
- **Claim 绑定**仅在通过 `--claim "..."`（推荐）或 `claim:"..."` 提供 claim 时运行。
  每条结果随后增加一个 `claim_support` block，其中包含 `relevance`、
  `matched_fields`、`shared_terms` 和 `provenance` note。这只是词汇重叠，**不是**
  支持性证明。应把它作为交给后续验证的线索，绝不能当作论文支持 claim 的证据。

JSON spec 形式：

```json
{
  "query": "low-latency time-series forecasting",
  "recent_window": 3,
  "claim": "our sparse attention reduces inference latency"
}
```

## 自然语言映射示例

### 主题检索

用户请求：

> 查找使用 Mamba 的长期时间序列预测论文。

紧凑形式：

```text
long-term time series forecasting mamba cite:both
```

建议的 JSON spec：

```json
{
  "query": "long-term time series forecasting mamba",
  "sort": "relevance",
  "limit": 5,
  "citation_mode": "both"
}
```

### 带显式过滤的主题检索

用户请求：

> 查找 Cheng 在 2024 年或之后发表的 Mamba 时间序列预测论文，最好带有代码。

紧凑形式：

```text
mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:8
```

建议的 JSON spec：

```json
{
  "query": "mamba time series forecasting",
  "filters": {
    "year_min": 2024,
    "author_contains": ["Cheng"],
    "has": ["code"]
  },
  "sort": "relevance",
  "limit": 8,
  "citation_mode": "both"
}
```

### 字段专用过滤

用户请求：

> 显示 annotation 包含 CodeAvailable 且 abstract 提到 photovoltaic 的条目。

紧凑形式：

```text
photovoltaic annotation:CodeAvailable raw:true cite:none
```

建议的 JSON spec：

```json
{
  "query": "photovoltaic",
  "filters": {
    "field_contains": {
      "annotation": ["CodeAvailable"],
      "abstract": ["photovoltaic"]
    }
  },
  "include_raw_bib": true,
  "citation_mode": "none"
}
```

### 取反与排除

用户请求：

> 查找近期用于时间序列预测的 transformer 论文，但排除仅有 arXiv 的 misc 条目，并排除没有 DOI 的条目。

紧凑形式：

```text
transformer time series forecasting year>=2022 -type:misc has:doi
```

建议的 JSON spec：

```json
{
  "query": "transformer time series forecasting",
  "filters": {
    "year_min": 2022,
    "exclude_type_in": ["misc"],
    "has": ["doi"]
  },
  "sort": "relevance"
}
```

### 文献导出检查

用户请求：

> 返回与 TimeMachine 最匹配的原始 BibTeX 条目，以及 LaTeX 和 Typst 两种引用形式。

紧凑形式：

```text
TimeMachine raw:true cite:both limit:1
```

建议的 JSON spec：

```json
{
  "query": "TimeMachine",
  "sort": "relevance",
  "limit": 1,
  "include_raw_bib": true,
  "citation_mode": "both"
}
```

## 排序建议

- `relevance`：主题发现的最佳默认值
- `year_desc`：适合按最新优先浏览
- `year_asc`：适合查看历史发展
- `title`：适合检查范围较窄的候选集

## 边缘情况

### 自由文本中的冒号

当紧凑 token 形如 `name:value`，且 `name` 以 ASCII 字母或下划线开头时，它会被解释为
字段过滤。这也适用于陌生字段名：`genotype:phenotype` 会变成对 `genotype` 字段的过滤，
因此该 token 会从自由文本查询中移除，不再参与相关性评分。当所有条目都没有该字段时，
`meta.parse_warnings` 会报告 `unknown_field_filter` 警告。

前缀以数字开头的 token 不匹配字段过滤语法，例如 `10:30` 仍保留为自由文本。如果以字母
开头的冒号 token 本意是自由文本，请把冒号替换为空格（`genotype phenotype`）。相关性
tokenizer 本来就会把标点当作分隔符，因此这种改写会保留参与评分的词。`note:`、`title:`
等真实字段始终按过滤条件处理；只要文献库中存在该字段，就不会发出警告。

### 仅过滤查询（没有主题词）

当用户只想过滤而不做主题检索时，所有匹配条目的分数均为零，由排序模式决定顺序。
例如：

```text
author:Cheng year>=2024 type:article sort:year_desc
```

该查询返回 Cheng 在 2024 年及之后发表的所有 article，并按最新优先排序，不执行
相关性排名。

### 空结果建议

如果没有条目匹配查询，按以下步骤逐步放宽过滤条件：

1. 移除 `has:` 约束。最严格的通常是 `has:code` 和 `has:pdf`
2. 扩大或删除年份范围
3. 减少主题关键词，或尝试同义词
4. 检查作者姓名拼写。作者过滤采用不区分大小写、折叠重音符号的子字符串匹配，因此
   `author:Muller` 能匹配 `M{\"u}ller`，而 `author:chen` 这样的部分姓名会
   同时匹配 `Chen` 和 `Cheng`。这种宽松匹配便于恢复结果，但也有误报风险：
   引用前必须核实作者身份，不能信任一次子字符串命中。

## 已知限制

- 作者匹配不会规范姓名顺序，也不处理 `von`/particle，因此
  `author:"Jane Doe"` 无法匹配 `{Doe, Jane}` 字段；请按姓氏检索。
- `matched_entries` 只统计结构化过滤的匹配，不报告自由文本相关性阈值丢弃了多少条目。
- CJK 查询最适合连续子字符串（`时间序列`）；以空格分隔的 CJK 词语可能无法全部匹配。
- 多文件文献库不会合并。每个 `.bib` 文件分别运行一次脚本。
- 年份识别范围为 1500–2099；任何年份过滤都会排除没有可解析年份的条目。
