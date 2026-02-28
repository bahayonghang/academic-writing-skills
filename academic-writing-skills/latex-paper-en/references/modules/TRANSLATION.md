# Module: Translation (Chinese → English)

**Trigger**: translate, 翻译, 中译英, Chinese to English

**Step 1: Domain Selection**
Identify domain for terminology:
- Deep Learning: neural networks, attention, loss functions
- Time Series: forecasting, ARIMA, temporal patterns
- Industrial Control: PID, fault detection, SCADA

**Step 2: Terminology Confirmation**
```markdown
| 中文 | English | Domain |
|------|---------|--------|
| 注意力机制 | attention mechanism | DL |
```
Reference: [TERMINOLOGY.md](../references/TERMINOLOGY.md)
If a term is ambiguous or domain-specific, pause and ask for confirmation before translating.

**Step 3: Translation with Notes**
```latex
% ORIGINAL: 本文提出了一种基于Transformer的方法
% TRANSLATION: We propose a Transformer-based approach
% NOTES: "本文提出" → "We propose" (standard academic)
```

```bash
python scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
python scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

**Step 4: Chinglish Check**
Reference: [TRANSLATION_GUIDE.md](../references/TRANSLATION_GUIDE.md)

Common fixes:
- "more and more" → "increasingly"
- "in recent years" → "recently"
- "play an important role" → "is crucial for"

**Quick Patterns**:
| 中文 | English |
|------|---------|
| 本文提出... | We propose... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... |
