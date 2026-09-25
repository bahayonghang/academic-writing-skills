# 示例：按 IEEE Transactions 改写引言

用户请求：
把这段引言按 IEEE Transactions on Industrial Informatics 的写法改写，研究领域是过程控制，保留引用。

输入：

- `input_text`：下方合成引言片段。
- `target`：`introduction`。
- `journal`：`IEEE Transactions on Industrial Informatics`。
- `domain`：`process_control`。

Profile 选择与加载：

1. 请求中没有显式 venue。该期刊在 IEEE allowlist 中，选择 `ieee`，`selection_source` 为 `journal allowlist`。
2. domain `process_control` 映射到 `elsevier`，与期刊的映射结果不同。按优先级期刊获胜，冲突写入 `conflicts`。
3. 只读取 `profiles/ieee.json`。该 profile 只有路由元数据，本包没有 IEEE 语料快照：`degraded` 为 `true`，
   缺失的观察证据写入 `missing_evidence`，`rules_applied` 与 `evidence_rows` 为空。
4. `patterns_used` 只记录 profile 文件列出的机制 `transactions-self-reference`：正文自指用 "this article"。

合成输入：

```text
In recent years, many methods have been proposed for soft sensing [1]-[4]. However, they suffer from process drift. To address this issue, this paper proposes a DAGNN model.
```

输出示例：

`text`：

```text
Many soft sensing methods have been proposed [1]-[4]. However, these methods are sensitive to process drift. To address this drift, this article proposes a DAGNN model.
```

`text_compact`（`render_result` 截取规范化文本的前 65% 字符）：

```text
Many soft sensing methods have been proposed [1]-[4]. However, these methods are sensitive to process drift.
```

`summary`：

```json
{
  "venue": "ieee",
  "profile_version": "materials-ieee-2026-09-11",
  "section": "introduction",
  "domain": null,
  "rules_applied": [],
  "patterns_used": ["transactions-self-reference"],
  "evidence_rows": [],
  "ai_tells_avoided": ["In recent years"],
  "untraceable_tokens": [],
  "degraded": true,
  "selection_source": "journal allowlist",
  "conflicts": ["domain=elsevier conflicts with journal=ieee"],
  "missing_evidence": ["corpus rows for profiles/ieee.json load_order"],
  "protected_tokens": ["[1]", "[4]", "DAGNN"]
}
```

要点：

- `[1]`、`[4]` 与 `DAGNN` 逐字保留，引用区间 `[1]-[4]` 不变。
- "suffer from" 改为 "are sensitive to"。输出没有新增性能数字或对比结论。
- 冲突只报告，不静默丢弃。用户如果要按 Elsevier 写法改写，应显式给出 `venue=elsevier`。
