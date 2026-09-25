# 示例：未指定 venue 的中性润色

用户请求：
这段结果准备投 Journal of Cleaner Production，领域写 energy_systems，先帮我润色 experiments 里的这段话。

输入：

- `input_text`：下方合成结果片段。
- `target`：`experiments`（别名，规范节名为 `results`）。
- `journal`：`Journal of Cleaner Production`。
- `domain`：`energy_systems`。

Profile 选择与加载：

1. 请求中没有显式 venue。该期刊不在 `IEEE_JOURNALS` 与 `ELSEVIER_JOURNALS` 中，不按期刊名称推测 profile。
2. `energy_systems` 不是可映射的 domain 键。
3. 选择 `unspecified`，`selection_source` 为 `neutral baseline`，`missing_evidence` 为 `safe venue mapping`。
   不加载任何 profile 文件，`profile_version` 为 `unresolved`，`degraded` 为 `false`。

合成输入：

```text
It can be clearly seen from Table 2 that our method obviously outperforms the baselines, and the RMSE is reduced from 0.312 to 0.214.
```

输出示例：

`text`：

```text
Table 2 shows that our method outperforms the baselines; the RMSE decreases from 0.312 to 0.214.
```

`text_compact`（`render_result` 截取规范化文本的前 65% 字符，可能在词中截断）：

```text
Table 2 shows that our method outperforms the baselines; the R
```

`summary`：

```json
{
  "venue": "unspecified",
  "profile_version": "unresolved",
  "section": "results",
  "domain": null,
  "rules_applied": [],
  "patterns_used": [],
  "evidence_rows": [],
  "ai_tells_avoided": ["clearly", "obviously"],
  "untraceable_tokens": [],
  "degraded": false,
  "selection_source": "neutral baseline",
  "conflicts": [],
  "missing_evidence": ["safe venue mapping"],
  "protected_tokens": ["2", "RMSE", "0.312", "0.214"]
}
```

要点：

- `2`、`RMSE`、`0.312` 与 `0.214` 逐字保留。比较结论不超出 Table 2 的范围。
- 技能报告缺失的 venue 证据，不猜测期刊风格。
- 用户如果要按 Elsevier 写法改写，应显式给出 `venue=elsevier`。该 profile 只有路由元数据，输出会标记 `degraded`。
