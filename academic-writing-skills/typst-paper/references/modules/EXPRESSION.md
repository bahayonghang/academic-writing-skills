# 模块：学术表达
**触发词**: academic tone, 学术表达, improve writing, weak verbs

**脚本用法**:
```bash
uv run python ../scripts/improve_expression.py main.typ
uv run python ../scripts/improve_expression.py main.typ --section methods
```

**英文学术表达**:
| 弱动词 | 学术替代 |
|----------|------------|
| use | employ, utilize, leverage |
| get | obtain, achieve, acquire |
| make | construct, develop, generate |
| show | demonstrate, illustrate, indicate |

**中文学术表达**:
| 口语化 | 学术化 |
|----------|----------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |

**使用方式**：用户提供段落源码，Agent 分析并返回润色版本及对比表格。

**输出格式**（Markdown 对比表格）:
```markdown
| Original / 原文 | Revised / 改进版本 | Issue Type / 问题类型 | Rationale / 优化理由 |
|-----------------|---------------------|----------------------|---------------------|
| We use machine learning to get better results. | We employ machine learning to achieve superior performance. | Weak verbs | Replace "use" -> "employ", "get" -> "achieve" for academic tone |
```

**备选格式**（源码内注释）:
```typst
// EXPRESSION（第23行）[Severity: Minor] [Priority: P2] [Script]: 提升学术语气
// 原文：We use machine learning to get better results.
// 修改后：We employ machine learning to achieve superior performance.
// 理由：用学术替代词替换弱动词
// Changed:       1 lexical substitution (get -> achieve)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    lexical-substitution
```

**改写契约**：本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/skill-routing-notes.md`。

**不得升高措辞强度**：把留有余地的表述换成更强的断言（`suggests` → `demonstrates`、`可能` → `能够`）是过度声称，不是语气提升。保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

参考：[STYLE_GUIDE.md](../references/STYLE_GUIDE.md)

