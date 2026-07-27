# 模块：翻译（中译英）
**触发词**: translate, 翻译, 中译英, Chinese to English

**脚本用法**:
```bash
uv run python ../scripts/translate_academic.py "中文文本"
uv run python ../scripts/translate_academic.py input_zh.txt --domain deep-learning
```

**翻译流程**:

**步骤 1：领域识别**
确定专业领域术语：
- 深度学习：neural networks, attention, loss functions
- 时间序列：forecasting, ARIMA, temporal patterns
- 工业控制：PID, fault detection, SCADA

**步骤 2：术语确认**
```markdown
| 中文 | English | 领域 |
|------|---------|------|
| 注意力机制 | attention mechanism | DL |
| 时间序列预测 | time series forecasting | TS |
```

**步骤 3：翻译并注释**
```typst
// 原文：本文提出了一种基于Transformer的方法
// 译文：We propose a Transformer-based approach
// 注释："本文提出" -> "We propose"（学术标准表达）
```

**步骤 4：Chinglish 检查**
| 中式英语 | 地道表达 |
|----------|----------|
| more and more | increasingly |
| in recent years | recently |
| play an important role | is crucial for |

**常用学术句式**:
| 中文 | English |
|------|---------|
| 本文提出... | We propose... / This paper presents... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... / In comparison to... |
| 综上所述 | In summary / In conclusion |

**步骤 5：契约块**
脚本在 `### Notes` 之后追加 `### Contract`，字段名与注释流模块逐字一致：

```markdown
### Contract
- Changed: rule-based draft translation (2 glossary term(s) applied)
- Protected: none — this copy does not mask Typst syntax; check `@cite`, `<label>`, and math spans by hand before applying
- Meaning-Check: NEEDS-LLM
- Risk-Flags: not-assessed
- Envelope: goal=grammar strength=minimal
```

Typst 副本**不做语法遮蔽**（与 EN 副本的差异，未纳入字节锁）：术语替换有可能碰到 `@cite`、`<label>` 或数学块，应用前必须人工核对。规则草稿永远不是成品译文，`Meaning-Check` 恒为 `NEEDS-LLM`；翻译时升高措辞强度同样属于过度声称，判据见 [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。字段定义见 [skill-routing-notes.md](../skill-routing-notes.md)。

参考：[STYLE_GUIDE.md](../STYLE_GUIDE.md)、[COMMON_ERRORS.md](../COMMON_ERRORS.md)

