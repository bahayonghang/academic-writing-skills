# 模块：学术表达
**触发词**: academic tone, 学术表达, improve writing, weak verbs

**脚本用法**:
```bash
uv run python ../scripts/improve_expression.py main.typ
uv run python ../scripts/improve_expression.py main.typ --section methods
uv run python ../scripts/improve_expression.py main.typ --goal clarity --strength moderate
```

`--goal`（默认 `grammar`）与 `--strength`（默认 `minimal`）声明编辑范围，见 [skill-routing-notes.md](../skill-routing-notes.md)；`--goal coherence` 在本模块无规则，会路由到 `logic`。

**脚本自动应用的替换**（大小写随原 token 保留）:
| 弱动词/短语 | 替换 |
|----------|------------|
| get | obtain |
| a lot of | many |

**只报候选、绝不自动替换**（模式可检出，但规则无法判断是不是误用）:
| 模式 | 为何停在候选 |
|----------|------------|
| make | "Make sure"、"make use of" —— 自动替换实测产出 "develop sure" / "develop use of" |
| very | "very few" —— 自动替换实测产出 "highly few" |
| kind of | 删掉它会改变 "a kind of transformer" 的含义 |

**不要把 `use → employ`、`show → demonstrate` 加回来**：它们是被有意删除的。de-AI 指南把 "we use ..." 列为正确的学术英语，把 "demonstrate the effectiveness" 列为 AI 痕迹，套用这两条会让本模块与 [DEAI.md](DEAI.md) 互相打架（finding E15）。加搭配排除表也不是解法——`make sense`、`make up`、`make do`、`make it` 是开放集，漏一个就产出错误英文。

受保护 token（统计值、带单位数值、模型/数据集/基因名）在替换前被遮蔽，并列入 `Protected:`。完整分级见 [PROTECTED_TOKENS.md](../PROTECTED_TOKENS.md)。

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
| We get better results. | We obtain better results. | Weak verb | Replace "get" -> "obtain" for academic tone |
```

**备选格式**（源码内注释，即脚本实际输出）:
```typst
// CONTRACT [Script]: goal=grammar strength=minimal
// EXPRESSION (Line 23) [Severity: Minor] [Priority: P2] [Script]: Improve academic tone
// Original: We get 92.1% accuracy on CIFAR-100.
// Revised:  We obtain 92.1% accuracy on CIFAR-100.
// Rationale: Weak verb replaced: \bget\b -> obtain
// Changed:       1 lexical substitution(s): get -> obtain
// Protected:     92.1%, CIFAR-100
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    lexical-substitution
```

**候选块**（无 `Revised:` 行——脚本拒绝猜）:
```typst
// EXPRESSION (Line 31) [Severity: Minor] [Priority: P3] [Script]: Weak-expression candidate
// Original: Make sure the model converges.
// Candidate: weak verb "make" is context-dependent ("make sure", "make use of"); not auto-applied
// Changed:       none (candidate only: Make)
// Protected:     none
// Meaning-Check: NEEDS-LLM
// Risk-Flags:    not-assessed
```

**改写契约**：本模块产出可直接替换原文的文本，适用改写契约。`[Script]` 层输出恒为 `Meaning-Check: NEEDS-LLM`，且只允许置规则可确定的标记（`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`）；只有 `[LLM]` 层可提出 `PRESERVED`，且仍是待作者核对的提案。字段定义与 `Risk-Flags` 闭集见 `references/skill-routing-notes.md`。

**不得升高措辞强度**：把留有余地的表述换成更强的断言（`suggests` → `demonstrates`、`可能` → `能够`）是过度声称，不是语气提升。保持原强度，或置 `Risk-Flags: overstatement` 并明确说明。判据见 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

参考：[STYLE_GUIDE.md](../STYLE_GUIDE.md)

