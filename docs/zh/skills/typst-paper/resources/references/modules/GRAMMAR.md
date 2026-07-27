# 模块：语法分析（英文）
**触发词**: grammar, 语法, proofread, 润色, article usage

**脚本用法**:
```bash
uv run python ../scripts/analyze_grammar.py main.typ
uv run python ../scripts/analyze_grammar.py main.typ --section introduction
```

**重点检查领域**:
- 主谓一致
- 冠词使用（a/an/the）
- 时态一致性（方法用过去时，结果用现在时）
- Chinglish 检测

**输出格式**:
```typst
// GRAMMAR（第23行）[Severity: Major] [Priority: P1] [Script]: 冠词缺失
// 原文：We propose method for...
// 修改后：We propose a method for...
// 理由：单数可数名词前缺少不定冠词
// Changed:       1 article insertion (propose method -> propose a method)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    none
```

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

