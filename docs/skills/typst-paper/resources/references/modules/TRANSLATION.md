# Module: Translation (Chinese to English)
**Trigger words**: translate, translation, 中译英, Chinese to English

**Script Usage**:
```bash
uv run python ../scripts/translate_academic.py "中文文本"
uv run python ../scripts/translate_academic.py input_zh.txt --domain deep-learning
```

**Translation Process**:

**Step 1: Domain Identification**
Identify professional domain terms:
- Deep learning: neural networks, attention, loss functions
- Time series: forecasting, ARIMA, temporal patterns
- Industrial control: PID, fault detection, SCADA

**Step 2: Terminology Confirmation**
```markdown
| 中文 | English | 领域 |
|------|---------|------|
| 注意力机制 | attention mechanism | DL |
| 时间序列预测 | time series forecasting | TS |
```

**Step 3: Translate and annotate**
```typst
// 原文：本文提出了一种基于Transformer的方法
// 译文：We propose a Transformer-based approach
// 注释："本文提出" -> "We propose"（学术标准表达）
```

**Step 4: Chinglish Check**
|Chinglish|authentic expression|
|----------|----------|
|more and more|increasingly|
|in recent years|recently|
|play an important role|is crucial for|

**Commonly used academic sentence patterns**:
|Chinese|English|
|------|---------|
|This article proposes...|We propose... / This paper presents...|
|Experimental results show...|Experimental results demonstrate that...|
|compared to|Compared with.../In comparison to...|
|In summary|In summary/In conclusion|

**Step 5: Contract block**
After `### Notes` the script appends a `### Contract` block, using the same field names as the comment-stream modules:

```markdown
### Contract
- Changed: rule-based draft translation (2 glossary term(s) applied)
- Protected: none — this copy does not mask Typst syntax; check `@cite`, `<label>`, and math spans by hand before applying
- Meaning-Check: NEEDS-LLM
- Risk-Flags: not-assessed
- Envelope: goal=grammar strength=minimal
```

The Typst copy performs **no syntax masking** (a deliberate difference from the EN copy, not covered by the byte lock): a glossary substitution may land inside `@cite`, `<label>`, or a math block, so check before applying. A rule-based draft is never a finished translation — `Meaning-Check` stays `NEEDS-LLM`, and raising claim strength while translating is likewise an over-claim; criteria in [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md). Field definitions: [skill-routing-notes.md](../skill-routing-notes.md).

Reference: [STYLE_GUIDE.md](../STYLE_GUIDE.md),[COMMON_ERRORS.md](../COMMON_ERRORS.md)

