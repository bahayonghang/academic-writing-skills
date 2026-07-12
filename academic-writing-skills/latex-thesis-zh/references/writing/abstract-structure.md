# Abstract Structure Guide

An effective academic abstract contains five structural elements that together tell a complete research story. This guide defines each element, how to detect it, and what makes it strong or weak.

## Five-Element Model

### 1. Background

**Purpose**: Establish the research context — the real-world problem, knowledge gap, or motivation.

**Detection markers (EN)**: "however", "remains unclear", "limited research", "growing interest", "challenge", "gap", "despite", "little is known", "increasingly important"

**Detection markers (ZH)**: "然而", "尚不清楚", "研究不足", "日益增长", "挑战", "空白", "尽管", "鲜有研究"

**Quality criteria**: Moves from broad context to specific gap in 1-2 sentences. A vague background restates the field name without identifying a gap.

### 2. Objective

**Purpose**: State what this specific study aims to answer or accomplish.

**Detection markers (EN)**: "this study aims", "we investigate", "the purpose of", "this paper presents", "we propose", "our goal", "in this work", "we address", "this research examines"

**Detection markers (ZH)**: "本文旨在", "本研究探讨", "本文提出", "研究目的", "为此我们", "本工作", "本文研究"

**Quality criteria**: Specific and falsifiable. A vague objective says "we study X" without specifying what aspect or what question about X.

### 3. Methods

**Purpose**: Describe the approach, data, tools, or analytical framework used.

**Detection markers (EN)**: "we propose", "using", "dataset", "participants", "method", "approach", "framework", "model", "algorithm", "collected", "trained", "evaluated", "sample", "experiment"

**Detection markers (ZH)**: "采用", "方法", "数据集", "样本", "模型", "算法", "框架", "实验", "训练", "评估"

**Quality criteria**: Names the specific technique, data source, or experimental setup. Missing methods make the abstract feel like an opinion piece.

### 4. Results

**Purpose**: Report the key findings with concrete data.

**Detection markers (EN)**: "results show", "achieved", "outperforms", "accuracy", "improved", "reduced", "found that", "demonstrates", "significant", numbers, percentages, p-values

**Detection markers (ZH)**: "结果表明", "达到", "优于", "准确率", "提高", "降低", "发现", "显著", numbers

**Quality criteria**: Must contain at least one quantitative finding (number, percentage, ratio, or comparative statement with magnitude). A results section without numbers is classified as VAGUE.

### 5. Conclusion / Significance

**Purpose**: State the contribution, implications, or practical value of the findings.

**Detection markers (EN)**: "our findings suggest", "contributes to", "implications", "demonstrates that", "can be used", "enables", "provides", "advances", "potential"

**Detection markers (ZH)**: "研究发现表明", "为...提供", "有助于", "具有...意义", "可用于", "推动", "贡献"

**Quality criteria**: Goes beyond restating results — connects findings to the broader field or practice. A hollow conclusion just repeats the results in different words.

## Common Defect Patterns

| Defect | Description | Typical fix |
|--------|-------------|-------------|
| Missing background | Jumps straight to "We propose..." | Add 1 sentence on the problem context |
| Vague objective | "We study deep learning for NLP" | Specify: "We investigate whether... improves..." |
| No methods | Describes results without explaining how | Add the core technique and data source |
| Data-free results | "Our method performs well" | Add a key metric: "achieves 94.2% F1" |
| Echo conclusion | Restates results verbatim | Add implication: "enabling real-time..." |

## Word Count Guidelines

| Context | Language | Range |
|---------|----------|-------|
| Default (no venue specified) | English | 150–250 words |
| Default (no venue specified) | Chinese | 200–300 characters |
| IEEE conference | English | 150–200 words |
| ACM conference | English | 150–250 words |
| NeurIPS/ICML | English | ≤ 200 words (strict) |
| Chinese thesis (GB/T) | Chinese | 300–500 characters |

Venue-specific limits override defaults. Check catalog.md for exact requirements.

## Diagnostic Output Format

The analyzer outputs a per-element diagnosis:

```
Background:  ✅ PRESENT  — "Despite growing interest in X, the impact of Y remains unclear."
Objective:   ⚠️ VAGUE    — "This paper studies X." → Suggestion: specify the research question
Methods:     ✅ PRESENT  — "We propose a framework based on Z, evaluated on dataset W."
Results:     ❌ MISSING  — No quantitative findings detected → Add key metrics
Conclusion:  ⚠️ VAGUE    — Restates results without implications → Add practical significance
```

## 学位论文摘要骨架（thesis 模型）

上面的五要素模型是**会议/期刊小论文**口径。中文学位论文（尤其工科博士）摘要遵循一套不同的
**骨架结构**：不是 Background/Objective/Methods/Results/Conclusion 五段，而是"对象定位 → 痛点 →
总起句冒号收束 → 编号工作段 → 可选收尾段"。`analyze_abstract.py` 的 **`--model thesis` 为默认**，
诊断这套骨架；`--model five` 保留上面的五要素模型作后备（本技能只服务学位论文，五要素模型对
博士摘要会系统性误报，如 Results 无数值判 MISSING，而合规博士摘要常定性收口）。

### 骨架顺序（宏观）

```text
① 对象定位首句："X 是……" / "X 产生于……"（研究对象为主语，非方法开头）
② 痛点/挑战段："然而，……难以/挑战/瓶颈……"
③ 总起句 + 冒号收束："本文主要研究工作/创新点如下："
④ 编号工作段 (1)(2)(3)…：每段"针对……问题，提出/建立……，实验/应用表明……"
⑤ 可选收尾段：综述成果/工程应用（"优化/工程应用"类论文常见，非必需）
```

段落数 = 背景段(1~2) + 工作段(编号数) + 可选收尾段。

### 与五要素模型的关系

| 维度 | 五要素模型（`--model five`） | 学位论文骨架（`--model thesis`，默认） |
| --- | --- | --- |
| 适用 | 会议/期刊小论文 | 中文博士/硕士学位论文 |
| 主体 | Background/Objective/Methods/Results/Conclusion 五段 | 编号工作段 (1)(2)(3)… |
| 数值 | Results 无数值判 VAGUE/MISSING | 数值可选（4/5 定性收口合规），出现才查稳健表述 |
| 字数 | EN 150~250 词 / ZH 200~300 字 | 对齐 check_spec 燕山常量：博士 900~1200 字 / 硕士 500~650 字 |

字数阈值由 `--degree {doctor,master}` 切换（默认 doctor），`--max-chars` 可覆盖上界。

### T-* 分级规律表

诊断项对应 research `abstract-patterns.md` 编号；**★ 标记（≥4/5）为默认告警，2~3/5 规律仅 Info**：

| 检查码 | 内容 | 级别 | 溯源 |
| --- | --- | --- | --- |
| T-OPEN | 首句以研究对象为主语定位，非方法开头 | Warning | ★A1 5/5 |
| T-PAIN | 存在痛点/挑战句（难以/挑战/尚未/瓶颈） | Warning | ★A2 5/5 |
| T-LEAD | 编号段前有总起句且以"："收束 | Warning | ★A4 5/5 |
| T-ENUM | 主体为 (1)(2)… 编号工作段，段数与编号一致 | Warning | ★A5 5/5、D4 |
| T-VERIFY | 验证方式点名（仿真/实测/生产数据/现场应用），非空泛"验证有效" | Warning | ★C2 5/5 |
| T-ABBR | 缩略语首现即定义中英全称 | Warning | ★E3 5/5 |
| T-INNOV | 出现创新表述（创新/首次/新方法 或编号工作段本身） | Warning | web A3 校规 |
| T-TOC-STYLE | 非目录式摘要 / 背景铺陈不过长 | Warning | web A10 软性 |
| T-PROB | 各工作段以问题导向短语开头（全篇 <50% 才报） | Info | ★B1 |
| T-VERB | 方法动词属规范集（提出/建立/设计/构建/研究/采用） | Info | ★B4 |
| T-NUM-HEDGE | 数值指标带"约/以上/区间"稳健表述（有数值才查） | Info | C3 2/2 |
| T-KW-FIRST | 首个关键词≈研究对象/过程名 | Info | ★D2 |
| T-VOICE | 只查"我/我们/笔者"；"本文/本论文"合法 | Info | web A6 |

### 中英摘要一致性（`--bilingual`）

thesis 模式加 `--bilingual` 时额外比对英文 Abstract 与中文摘要：

| 检查码 | 内容 | 级别 | 溯源 |
| --- | --- | --- | --- |
| B-ORD | 首先/其次/然后/最后 ↔ First/Second/Then/Finally 数量与顺序对齐 | Warning | ★F3 5/5 |
| B-NUM | 中英数值 token 集合一致 | Error（数值不一致是硬伤） | ★F1；web A9 |
| B-ENUM | 编号工作段条数一致 | Warning | ★F1 |
| B-LEN | 英文摘要缺失/过短 | Warning | web A9 |
| B-SEM | 逐句/逐要素语义对应（[LLM] lane，报告给对照提示词） | — | ★F1 |

时态/语态（★F2 英摘方法句一般现在时被动）**不在此实现**：deai 模块已有英文摘要区域门控的
时态检测（[tense-guide-zh.md](tense-guide-zh.md) + deai_check），`--bilingual` 报告尾注指路 deai，
避免双实现漂移（deai trace 不流入本模块）。

## Constraints

- Never alter the author's core claims or fabricate data
- Never add results or conclusions not present in the original text
- Preserve all citations, labels, and math environments
- Mark all modifications with brackets: [ADDED: ...] or [REVISED: ...]
