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

Reference: [STYLE_GUIDE.md](../STYLE_GUIDE.md),[COMMON_ERRORS.md](../COMMON_ERRORS.md)

