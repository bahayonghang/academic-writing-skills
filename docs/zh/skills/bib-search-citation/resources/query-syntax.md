# 查询语法

本页说明如何把文献检索请求映射成
`academic-writing-skills/bib-search-citation/scripts/search_bib.py`
可接受的输入。

## 两种输入方式

脚本支持：

1. JSON 检索配置
2. 紧凑查询表达式

当用户本身就写得像过滤串时，优先用紧凑表达式。

```text
time series forecasting mamba author:Cheng year>=2024 has:code type:article,misc cite:both
```

当流程已经有明确结构化条件时，再用 JSON。

## JSON 配置形状

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

- 普通词保留为主题检索词
- `author:cheng` 按作者名子串过滤
- `year>=2024` 设定最小年份
- `year<=2025` 设定最大年份
- `year:2024` 要求精确年份
- `year:2023,2024` 保留多个年份
- `type:article,misc` 保留指定条目类型
- `-type:misc` 排除指定条目类型
- `has:code,doi` 要求同时满足多个推断字段
- `-has:pdf` 排除看起来带 PDF 的条目
- `annotation:CodeAvailable` 直接过滤某个字段
- `keywords:mamba` 直接过滤另一个字段
- `sort:year_desc` 按最新优先排序
- `limit:10` 只返回 10 条
- `fields:key,title,year,doi` 限制返回字段
- `cite:latex`、`cite:typst`、`cite:both` 控制引用输出
- `raw:true` 返回原始 BibTeX
- `recent:3` 设定附加 `meta.recency` 报告的"近期"窗口（年）；也可用 `--recent-window`
- `claim:"..."` 为每条结果附加 `claim_support` 块（仅词面重叠）；含空格的主张优先用 `--claim`

### 说明

- 多个紧凑过滤可以自由组合。
- 不符合紧凑语法的 token 会保留在自由文本主题查询里。
- 即便使用 JSON，`spec.query` 里也可以混入紧凑过滤。
- 通用字段过滤支持 `title`、`shorttitle`、`annotation`、`keywords`、
  `abstract`、`file`、`copyright`、`doi`、`eprint` 等字段。
- 带否定的字段过滤写法相同，例如 `-annotation:survey`。
- 任意 `word:word` token 都会被当作通用字段过滤，因此字段名拼错会匹配不到任何条目；
  `meta.parse_warnings` 会标记不存在于任何条目的过滤字段。
- `preview_bib_search.py` 只是渲染器，不是第二套搜索引擎。

## 近期报告与主张绑定（附加）

两者都是附加功能，不会过滤或重排结果。

- **近期统计**始终在 `meta.recency` 下报告：`window_years`、`recent_threshold`
  （按当前自然年计算）、`with_year`、`recent_count`、`recent_share`，以及当返回结果
  中近期占比不足 80% 时给出的 `note`。用 `recent:N` 或 `--recent-window N`（默认 3）调节。
- **主张绑定**仅在通过 `--claim "..."`（推荐）或 `claim:"..."` 提供主张时运行。
  每条结果会获得 `claim_support` 块，含 `relevance`、`matched_fields`、`shared_terms`
  和 `provenance` 提示。这是词面重叠，**并非**支持证据——只作为核验交接，
  绝不能当成论文支持该主张的依据。

## 自然语言映射示例

### 主题检索

用户请求：

> 找用 Mamba 做长时序预测的论文。

紧凑写法：

```text
long-term time series forecasting mamba cite:both
```

建议 JSON：

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

> 找 2024 年及之后 Cheng 的 Mamba 时序预测论文，最好有代码。

紧凑写法：

```text
mamba time series forecasting author:Cheng year>=2024 has:code cite:both limit:8
```

建议 JSON：

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

### 指定字段过滤

用户请求：

> 找 annotation 含 CodeAvailable 且 abstract 提到 photovoltaic 的条目。

紧凑写法：

```text
photovoltaic annotation:CodeAvailable raw:true cite:none
```

建议 JSON：

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

### 否定与排除

用户请求：

> 找近年的 transformer 时序预测论文，排除 arXiv-only 的 misc 条目，并要求必须有 DOI。

紧凑写法：

```text
transformer time series forecasting year>=2022 -type:misc has:doi
```

建议 JSON：

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

### BibTeX 导出核对

用户请求：

> 找最匹配 TimeMachine 的条目，并返回原始 BibTeX 和两种引用形式。

紧凑写法：

```text
TimeMachine raw:true cite:both limit:1
```

建议 JSON：

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

- `relevance`：按主题找文献时的默认选项
- `year_desc`：按最新优先扫描
- `year_asc`：看历史演化
- `title`：候选集合很小时人工复核

## 边界情况

### 只有过滤条件，没有主题词

如果请求里没有主题词，所有命中条目的相关度分数相同，最终顺序由 sort 决定。

```text
author:Cheng year>=2024 type:article sort:year_desc
```

### 没有结果

如果没有任何命中，按这个顺序放宽条件：

1. 先去掉 `has:` 约束
2. 放宽或删除年份范围
3. 减少主题词，或改用同义词
4. 检查作者拼写。作者过滤是大小写不敏感、去重音的子串匹配，因此 `author:Muller`
   能命中 `M{\"u}ller`，`author:chen` 同时命中 `Chen` 和 `Cheng`。这种宽度便于
   召回，但也是误报风险——引用前请先确认作者身份，不要只凭子串命中。

## 已知限制

- 作者匹配不归一姓名顺序，因此 `author:"Jane Doe"` 不会命中 `{Doe, Jane}` 字段；
  请按姓氏检索。
- `matched_entries` 只统计结构化过滤命中数，不反映自由文本相关度淘汰的数量。
- 中文查询以连续子串（`时间序列`）命中效果最好。
- 多文件文献库不会自动合并——请对每个 `.bib` 文件分别运行。
- 截断条目（如缺少闭合花括号）会被跳过并记入 `meta.parse_warnings`，
  而不是静默吞掉文件其余部分。
