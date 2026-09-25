# 示例：按 Nature 风格润色摘要

用户请求：
按 Nature 风格润色这段 abstract，保留数字和引用。

输入：

- `input_text`：下方合成摘要片段。
- `target`：`abstract`。
- `venue`：`nature`（用户显式给出）。

Profile 选择与加载：

1. 用户显式给出 venue，`selection_source` 为 `explicit venue`。请求中没有 journal 与 domain，`conflicts` 为空。
2. 只读取 `profiles/nature.json`，按其 `load_order` 加载系统提示、风格指南、`abstract` 节提示与写作规则 TSV。
3. `source_path` 为 `ref/nature-writing-studio/skill`。本例在安装到论文项目的副本中运行，该路径不存在：`degraded` 为 `true`，
   缺失来源写入 `missing_evidence`，`rules_applied` 与 `evidence_rows` 为空，不改用 IEEE 或 Elsevier 的规则。

合成输入：

```text
In this paper, we propose a novel graph model which achieves 12.5% lower error than the baseline [3], and it is very robust (see \ref{tab:main}).
```

输出示例：

`text`：

```text
Here we present a graph model that lowers the error by 12.5% relative to the baseline [3] and remains robust (\ref{tab:main}).
```

`text_compact`（`render_result` 截取规范化文本的前 65% 字符，可能在词中截断）：

```text
Here we present a graph model that lowers the error by 12.5% relative to the base
```

`summary`：

```json
{
  "venue": "nature",
  "profile_version": "2.0.1",
  "section": "abstract",
  "domain": null,
  "rules_applied": [],
  "patterns_used": [],
  "evidence_rows": [],
  "ai_tells_avoided": ["novel", "very"],
  "untraceable_tokens": [],
  "degraded": true,
  "selection_source": "explicit venue",
  "conflicts": [],
  "missing_evidence": ["source_path ref/nature-writing-studio/skill"],
  "protected_tokens": ["12.5%", "[3]", "\\ref{tab:main}"]
}
```

要点：

- `12.5%`、`[3]` 与 `\ref{tab:main}` 在输出中逐字保留。输出没有新增数字、引用或结果。
- `ai_tells_avoided` 记录删去的强调词。本例没有加载 anti-AI 行，所以不写行号，`rules_applied` 为空。
- 在本开发仓库中，若 `ref/nature-writing-studio/skill` 存在且所需行全部加载，`rules_applied` 与 `evidence_rows` 列出实际加载的行，
  `degraded` 为 `false`。
