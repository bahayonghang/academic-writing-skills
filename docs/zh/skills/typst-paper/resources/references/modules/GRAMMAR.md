# 模块：语法分析（英文）
**触发词**: grammar, 语法, proofread, 润色, article usage

**脚本用法**:
```bash
uv run python ../scripts/analyze_grammar.py main.typ
uv run python ../scripts/analyze_grammar.py main.typ --section introduction
```

`--goal`（默认 `grammar`）与 `--strength`（默认 `minimal`）声明编辑范围，见 [skill-routing-notes.md](../skill-routing-notes.md)；`--goal concision` 路由到 `sentences`，`--goal coherence` 路由到 `logic`——本模块对二者均无规则。

**重点检查领域**:
- 主谓一致
- 冠词使用（a/an/the）
- 时态一致性（方法用过去时，结果用现在时）
- Chinglish 检测

**输出格式**（脚本实际输出）:
```typst
// CONTRACT [Script]: goal=grammar strength=minimal
// GRAMMAR (Line 23) [Severity: Major] [Priority: P1] [Script]: Rule hit: \bwe propose method\b
// Original: We propose method for time series forecasting.
// Revised:  We propose a method for time series forecasting.
// Rationale: Grammar: Article missing before singular count noun.
// Changed:       1 rule-based correction (\bwe propose method\b)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    none
```

规则按大小写不敏感匹配，因此行内其他位置的缩写（`BERT`）保持原形；命中片段本身保留自己的首字母大小写——旧版对句首命中会返回 `we propose a method`，修一个错的同时引入另一个。

**改写契约**：本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/skill-routing-notes.md`。

**不得升高措辞强度**：把留有余地的表述"修"成断言（`the results may indicate` → `the results indicate`）是披着语法修复外衣的过度声称。保持原强度，或置 `Risk-Flags: overstatement`。判据见 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

**常见语法错误**:
| 错误类型 | 示例 | 修正 |
|----------|------|------|
| 冠词缺失 | propose method | propose a method |
| 主谓不一致 | The data shows | The data show |
| 时态混乱 | We proposed... The results shows | We proposed... The results show |
| Chinglish | more and more | increasingly |

参考：[COMMON_ERRORS.md](../COMMON_ERRORS.md)、[STYLE_GUIDE.md](../STYLE_GUIDE.md)

