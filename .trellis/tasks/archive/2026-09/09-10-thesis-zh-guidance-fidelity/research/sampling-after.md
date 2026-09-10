# Public writing rules

## references/writing/writing-philosophy-zh.md

# 学位论文写作哲学

> "论文不是实验的堆砌，而是一个有清晰贡献的学术故事。" — 改编自 Neel Nanda

## 目录
- [叙事原则](#叙事原则)
- [摘要五句公式](#摘要五句公式)
- [读者期望七原则](#读者期望七原则)
- [用词精准](#用词精准)
- [精确优先](#精确优先)
- [微观写作技巧](#微观写作技巧)
- [分章节指南](#分章节指南)

## 叙事原则
(核心要义)

学位论文的核心是围绕**一个明确的研究贡献**展开叙述。

**三大支柱**（绪论结束前必须清晰呈现）：

| 支柱 | 说明 | 示例 |
|------|------|------|
| **做了什么** | 1-3 个具体的创新点 | "本文提出了X方法，在Y条件下实现了Z" |
| **为什么可信** | 与主张匹配的证据 | 理论证明、受控比较或有范围的工程验证 |
| **为什么重要** | 读者为何应该关注 | 与领域公认问题的联系 |

**如果你不能用一句话陈述你的贡献，你还没有形成一篇完整的论文。**

## 摘要五句公式

(改编自 Sebastian Farquhar, DeepMind)

五句公式仅是短篇摘要的构思辅助，不是学位论文的固定句数或篇幅规范。先遵循用户当前要求和
学校模板，再按[摘要结构指南](abstract-structure.md)选择适合的骨架；博士摘要不强套五句。

1. 本文的核心成果（"本文提出..."、"本文证明..."）
2. 为什么这个问题困难且重要
3. 采用的方法（含关键术语以提升可搜索性）
4. 已有验证证据（按工作类型选择证明、实验或工程记录）
5. 最关键的已支持结果（可以是有明确条件的定性结论）

没有定量结果时不得补造数字；没有实验的理论工作也不为凑齐公式新增实验。

**删除**泛泛的开头，如"随着深度学习的快速发展..."

## 读者期望七原则

(改编自 Gopen & Swan)

| # | 原则 | 规则 | 示例 |
|---|------|------|------|
| 1 | **主谓邻近** | 主语和谓语紧密相连 | ❌ "本文提出的基于...的方法，取得了" → ✅ "本文方法取得了..." |
| 2 | **重点置尾** | 句子重心放在末尾 | ✅ "本节讨论的重点是**输入条件**" |
| 3 | **旧信息在前** | 已知信息开头，新信息在后 | ✅ "基于上述分析，本文提出..." |
| 4 | **一段一义** | 每段只讲一个要点 | 拆分多要点段落 |
| 5 | **动作用动词** | 避免名词化 | ❌ "进行了分析" → ✅ "分析了" |
| 6 | **先铺垫后展示** | 先解释背景再给公式 | 公式前先说明含义 |
| 7 | **衔接清楚** | 先核对真实关系，必要时用信号词 | 关系已由对象和论证承接时，无需补"因此"或"此外" |

## 用词精准

(改编自 Zachary Lipton)

### 具体化
- "性能"：只有输入已明确指标时，才具体写成"准确率"或"推理延迟"；不得猜测指标。
- "显著"：只有已给出统计检验时，才报告实际统计量；否则删去无依据的强度词，不补 p 值。

### 消除模糊
| 给定输入 | 可支持的处理 |
| --- | --- |
| 只有"该方法可能有助于提升预测性能"，无新数据 | 可写"该方法可能改善预测性能"，保留不确定性；不新增数字或提升事实 |
| 已给出同一协议的比较记录及实际差值 | 按原记录写清指标、比较对象和范围；没有统计检验就不补"统计显著" |

具体化不能创造证据。观察、比较和机制各能支持多强的结论，按
[结果分析指南](results-analysis-guide-zh.md)的证据阶梯判断。

### 避免空话
删除：显然、毫无疑问、众所周知、不可否认

## 精确优先

(改编自 Jacob Steinhardt, UC Berkeley)

- **术语一致**：同一概念全文使用相同术语；共现或词频不能证明不同技术名称是同义词
- **假设明示**：在定理前明确列出所有假设条件
- **直觉+严谨**：给出直觉解释的同时提供形式化证明
- **先定义后使用**：每个符号和术语在首次使用前定义

## 微观写作技巧

(改编自 Ethan Perez, Anthropic)

- [ ] **避免模糊指代**：❌ "这说明..." → ✅ "该实验结果说明..."
- [ ] **动词前置**：谓语动词尽量靠近句首
- [ ] **删除填充词**：实际上、某种程度上、相当、比较、基本上
- [ ] **主动语态**：❌ "该方法被应用于" → ✅ "本文将该方法应用于"
- [ ] **量化表述**：有比较记录才写实际差值；只有"大幅提升"而无数据时，标明待补证据，不替入示例数字

## 分章节指南

以下是写作建议，篇幅以用户提供的学校要求、模板和实际章目标为准。

| 章节 | 篇幅依据 | 核心要求 |
|------|----------|----------|
| **摘要** | 学校要求与摘要类型 | 按已有工作和证据组织，见[摘要结构](abstract-structure.md) |
| **绪论** | 研究问题与学校要求 | 研究背景→问题→贡献→章节安排，见[绪论指南](introduction-guide-zh.md) |
| **文献综述** | 主题比较所需证据 | 主题综合与代表文献分析结合，见[综述模块](../modules/literature.md) |
| **研究方法** | 实际方法与证明需求 | 交代已有假设、接口和复现条件，见[方法描述指南](method-description-guide-zh.md) |
| **实验/工程验证** | 主张与验证类型 | 结果分析见[结果指南](results-analysis-guide-zh.md)，工程章见[工程应用指南](engineering-application-chapter-guide-zh.md) |
| **总结与展望** | 研究问题与证据范围 | 回答研究问题与可执行后续工作，见[总结指南](conclusion-guide-zh.md) |

### 绪论必须包含：
- 清晰的研究问题陈述
- 与实际独立工作对应的贡献说明，不为凑条数拆分或合并主张
- 简要的方法概述
- 章节安排说明
- 引用整合：主题综合句可归并多篇引用，关键差异处选择性展开代表文献；不把所有引用强制拆成逐篇介绍

### 按实际工作选择验证说明：
- 有实验时说明它验证的具体主张；有重复测量时区分标准差与标准误
- 有超参数搜索时报告实际范围；有计算实验时记录相关资源和时长
- 非 GPU 工程系统无需补 GPU 型号；理论章无需编造训练超参数或实验
- 工程记录只支持已验证的范围，离线回放不等于现场或操作者验收

## 时间分配建议

将大约**等量时间**用于：
1. 摘要
2. 绪论
3. 图表
4. 其余所有内容合计

**原因**：大多数评审在阅读方法章节之前就形成判断。

**读者阅读顺序**：题目 → 摘要 → 绪论 → 图表 → 可能阅读其余部分。

## 修改顺序（逻辑 → 句子 → 词汇，不可逆）

当一次润色需要多轮处理时，按以下顺序、且不可颠倒：

1. **论证 / 逻辑**：段落顺序、主旨重复或缺失、章节过渡。
2. **句子结构**：拆分超长句、被动改主动、信息密度高的成分前置。
3. **词汇 / 排版**：AI 高频词、数字与单位格式、术语与缩写一致性。

为何顺序固定：若先抠某句措辞（第 3 层），第 1 层修改又把该段删除或合并，前面的
功夫就白费。先粗后细，效率高数倍。

## 来源

| 来源 | 核心贡献 |
|------|----------|
| Neel Nanda (Google DeepMind) | 叙事原则 |
| Sebastian Farquhar (DeepMind) | 五句摘要公式 |
| Gopen & Swan | 读者期望七原则 |
| Zachary Lipton | 用词精准 |
| Jacob Steinhardt (UC Berkeley) | 精确性 |
| Ethan Perez (Anthropic) | 微观写作技巧 |


## references/writing/over-claim-guard.md

# 保守表达 Guard（过度声称防护）

中文学位论文的保守措辞参考。目的**不是**把话写得软弱无力，而是**精确表述证据强度**：
强证据用强表达，弱证据用弱表达。盲审专家对 over-claim 高度警觉，主动保守比被质询后再改省事。

## 与"证据是否充分"的边界

本文件管的是"**当证据强度已知时，措辞该用多重**"——选哪个动词/限定词，使句子不超出证据。
先判断证据是否支撑该论断（图/表/指标/引用是否真支持），再用本文件挑措辞。措辞与实质冲突时，实质优先。
结果证据资格以[结果分析指南](results-analysis-guide-zh.md)的五级证据阶梯为准。
下列措辞不是自动替换表；每项替代表达也必须有原文证据，不能凭空添加相关、影响或统计结果。

## 确定性阶梯（由强到弱）

```
证明 / 表明（强）                 ← 对应主张已通过实质证据审查，且限定适用范围
  ↓
揭示 / 发现 / 识别出               ← 强效应，多方法或可复现
  ↓
表明 / 提示                       ← 显著但单一方法
  ↓
支持 / 与……一致                  ← 趋势性，与前人一致
  ↓
可能表明 / 或许提示 / 似乎         ← 边缘显著或预测性
  ↓
暗示 / 倾向于                     ← 极弱信号或假说
```

按证据匹配台阶，不要爬到数据够不到的那一级。

## 替换表

### 1. 因果（最常见的 over-claim：把相关说成因果）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 由……导致 / 引起 | 与……相关 / 关联 |
| 驱动 / 决定 | 影响 / 与……相关 |
| 是……的根本原因 | 与……有关 / 可能与……有关 |
| 证明了 | 表明 / 提供了……的证据 |
| 造成了 | 伴随出现 / 与……同时出现 |

“消融”“随机对照”或“A/B”名称本身不授予因果资格。训练预算不同的消融含混杂，
不能把差异归因于组件；受控组件移除可支持组件贡献，但未必能解释其具体机制。
是否达到因果归因，仍按结果分析指南核对区分性证据。证据只支持观察时就报告观察，
机制未知时明确尚未确定，不强行改成另一项同样无依据的“相关”。

### 2. 首创 / 唯一性（评审会立刻去检索核实）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 首次 / 第一个 | 未检索时移除优先权主张或标为待核，只陈述实际完成的工作 |
| 新颖的（自我标榜） | 直接说明新在哪里，删掉"新颖"标签 |
| 前所未有的 | 显著的 / 值得注意的 |
| 此前未知的 | 此前研究不充分的 |

“据我们所知”不能替代检索，“最早的工作之一”仍是优先权主张。只有检索范围、时间和
相关工作比较支持该主张时，才讨论带范围的首创表述；不能用 hedge 保留未核实的“首次”。

### 3. 普适性（只研究一个场景，却宣称适用所有场景）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 总是 / 永远 / 从不 | 通常 / 很少 |
| 在所有情况下 | 在所研究的情形中 |
| 普遍地 | 在所评测的基准上 |
| 任意数据集 | 所采样的数据集 |

### 4. 效应大小（用"显著/大幅"却不给数字）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 大幅提升 | 误差降低了 X% |
| 显著的效应 | β = X.XX（95% CI：…） |
| 明显改善 | 从 X 提升到 Y（p = …） |
| 高度显著 | 报告实际检验的 p 值，不替入示例统计量 |
| 鲁棒 / 稳健 | 在 N 次独立运行中一致 / 在[扰动]下稳定 |

表中 X、Y、N 和统计量位置只能填入已有记录；没有记录就标待补证据，不补造数字。
如果数字本身就够说明问题，删掉形容词——让数字说话。

### 5. 时间 / 推断先后（用当代数据反推历史因果）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| X 驱动了该变化 | 该变化与 X 一致 |
| 发生在 T 时刻 | 估计约为 T（置信区间：…） |
| 从 A 迁移到 B | 数据与 A→B 的路径一致 |

### 6. 应用前景（本文未演示的下游用途）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 将带来变革 | 对……具有潜在意义 |
| 将被广泛使用 | 可能有助于 / 可为……提供参考 |
| 解决了 X 问题 | 处理了 X 的一个方面 |
| 可直接落地部署 | 为[场景]提供了候选方法 |

### 7. 比较（贬低前人工作）

| ❌ 过度声称 | ✅ 保守表达 |
|---|---|
| 前人方法未能…… | 前人方法受限于…… |
| 优于所有已有方法 | 与[具体方法]相比具有优势 |
| 终结了长期争论 | 为该争论的一方补充了证据 |

## 高频陷阱句式

| 陷阱 | 安全替代 |
|---|---|
| "本文结果证明了 X。"（X 是因果） | "本文结果与 X 一致。" |
| “这是首个……的工作。” | 未检索时删去“首个”，只说明本文做了什么；优先权待核 |
| "X 在 Y 中起关键作用。" | "X 与 Y 有关 / 可能对 Y 有贡献。" |
| "这些发现对……具有重要意义。" | "这些发现为进一步研究……提供了基础。" |
| "X 是 Y 的关键驱动因素。" | "X 与 Y 相关。" |
| "强烈支持" | "与……一致 / 提供了与……一致的证据" |

## 反向校准：什么时候**不该**保守

弱证据该保守，强证据再保守就是软弱。下列情况应当用强表达：

- 区分性证据支持具体因果主张 → 保留证据支持的强结论，同时写明协议、对象和范围；
- 多方法 / 多数据集 / 多随机种子复现 → 用"稳健"，并写明具体证据;
- 复现了已确立的机制 → 可用"确认 / 验证";
- 大效应 + 强统计量 → 强表达**并附上数字**。

## 自查清单（写完一段后扫一遍）

- [ ] 用了"首次/新颖"吗？未检索时移除优先权主张或标为待核，不能只加"据我们所知"
- [ ] 用了"导致/驱动/决定"吗？按结果分析指南核对实际设计与证据，不只看干预或消融标签
- [ ] 用了"所有/总是/普遍"吗？范围限定到实际研究范围了吗？
- [ ] 用了"显著/大幅/明显"吗？后面跟数字了吗？
- [ ] 列了本文没演示的应用意义吗？加"可能/或许"
- [ ] 贬低前人了吗？改成"受限于"，而非"未能/失败"

## 脚本支持

`deai_check.py` 会对一小批无歧义的过度声称短语（因果/首创/普适/应用）发 `[Script]` LOW
痕迹并指回本文件。脚本只兜底显而易见的情形；上面的表覆盖脚本无法判断的判断题。


## references/writing/abstract-structure.md

# Abstract Structure Guide

The five-element model below is a fallback for short conference/journal abstracts, not a required five-sentence formula for a Chinese degree thesis. Start with the user's current requirements and school template; the thesis model later in this guide is the default for this skill.

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

**Quality criteria**: In the five-model heuristic, results without a quantitative finding may be classified as VAGUE. This is a diagnostic signal, not permission to invent a number, comparison, or experiment. A supported theoretical result or a qualitative thesis conclusion must retain its actual evidence form.

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
| Data-free results | "Our method performs well" | Report a metric only if the input supplies it; otherwise identify missing evidence |
| Echo conclusion | Restates results verbatim | Explain the supported contribution within its scope; do not invent an application |

## Word Count Guidelines

These are five-model writing references for short abstracts, not verified venue limits or school requirements.

| Context | Language | Range |
|---------|----------|-------|
| Short abstract reference (five model only) | English | 150–250 words |
| Short abstract reference (five model only) | Chinese | 200–300 characters |

Use the supplied target requirements for length decisions. Do not apply these ranges to a doctoral abstract or attribute a generic thesis length to GB/T without a source.

## Diagnostic Output Format

The analyzer outputs a per-element diagnosis:

In five-model output, an invitation to add metrics means to locate existing evidence, not to create results. Reassess such findings against the selected thesis type before proposing any change.

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

### 编号工作段中的多组件关系

一个编号工作包含两个以上组件时，先核对它们的真实接口，再决定叙述顺序：

- **串行依赖**：只有原文已说明后组件接收前组件的输出，或针对前组件留下的明确约束继续处理时，才按“当前约束 -> 前组件作用/输出 -> 剩余约束 -> 后组件作用 -> 验证对象”组织；共同面向同一验证对象本身不能证明串行。
- **并行协作**：组件共享输入、分别处理不同对象或只在末端融合时，保留并行关系，分别说明各自对象与汇合点；不得写成“后组件修复前组件”。

组件名称本身不能证明因果、增益或消融贡献。原文未给出接口、作用或验证证据时，标明缺失信息，
不得补造模块功能、数值、引用或“带来提升”等结论。

### 与五要素模型的关系

| 维度 | 五要素模型（`--model five`） | 学位论文骨架（`--model thesis`，默认） |
| --- | --- | --- |
| 适用 | 会议/期刊小论文 | 中文博士/硕士学位论文 |
| 主体 | Background/Objective/Methods/Results/Conclusion 五段 | 编号工作段 (1)(2)(3)… |
| 数值 | Results 无数值判 VAGUE/MISSING | 数值可选（4/5 定性收口合规），出现才查稳健表述 |
| 字数 | EN 150~250 词 / ZH 200~300 字 | 对齐 check_spec 燕山常量：博士 900~1200 字 / 硕士 500~650 字 |

字数阈值由 `--degree {doctor,master}` 切换（默认 doctor），`--max-chars` 可覆盖上界。

这些是当前脚本默认值，不是所有学校的统一规范；用户给定的学校要求优先。核读时按实际
模板、摘要类型和已有材料判断，不为了满足默认长度或数值提示补写实验、GPU 或定量结果。

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
| B-NAT | 期刊式摘要修辞候选：开头缺领域上下文（需结合摘要类型判断）、末句缺范围限定，或全文缺数字、比较或具体测试（[LLM]，非判定） | Info | nature-writing N3（社区归纳） |

B-NAT 改造自 `ref/claude-scholar/skills/nature-writing` 的社区归纳 Nature-leaning 修辞
启发式。该来源未提供文章或 DOI 清单、样本选择方法，也未引用 Nature 官方作者指南；部分摘要
模板与 `ref/Research-Paper-Writing-Skills` 同源，已由本仓库既有章节写作资源吸收。B-NAT 只提供
候选提示，不构成 Nature 官方规则、投稿合规判定或脚本硬规则。

时态/语态（★F2 英摘方法句一般现在时被动）**不在此实现**：deai 模块已有英文摘要区域门控的
时态检测（[tense-guide-zh.md](tense-guide-zh.md) + deai_check），`--bilingual` 报告尾注指路 deai，
避免双实现漂移（deai trace 不流入本模块）。

## Constraints

- Never alter the author's core claims or fabricate data
- Never add results or conclusions not present in the original text
- Preserve all citations, labels, and math environments
- Mark all modifications with brackets: [ADDED: ...] or [REVISED: ...]


## references/modules/logic.md

# Logic Module Reference

Purpose: Check logical coherence, introduction funnel, heading lead-ins, literature review quality, chapter mainline, and cross-section closure.

For chapter-level rewrite planning, also read `../writing/thesis-writing-guide.md`. Keep `logic` as the diagnostic route, but use the guide to turn findings into a thesis-specific mainline plan. For an engineering-application or system-implementation chapter, first classify it from the thesis context and body content, then read `../writing/engineering-application-chapter-guide-zh.md`.

## AXES Model (Paragraph-Level Coherence)

给定输入仅为“注意力模型在测试集 T 上的准确率为95%”，没有比较基线或组件试验。
AXES 用来检查论证角色，不要求把一个观察补成提升或机制结论：

| Component | Role | Example |
|-----------|------|---------|
| **A**ssertion | Clear topic sentence | "本段报告注意力模型在测试集 T 上的预测表现。" |
| **X**ample | Supporting evidence/data | "该模型在测试集 T 上的准确率为95%。" |
| **E**xplanation | Why evidence supports claim | 该值只支持本次准确率观察，不能单独推导改进幅度或长程依赖机制 |
| **S**ignificance | Connection to broader argument | 将该记录关联到本章的评测问题；没有章目标时先标明缺失，不补造架构合理性 |

比较、组件贡献与因果资格按[结果分析指南](../writing/results-analysis-guide-zh.md)判断。
需要定位段主题与章目标、证据与段主题的关系时，参考
[逆向提纲示例](../../examples/logic-and-experiment.md)，不要求每次局部检查生成全篇台账。

## Heading Lead-In Check (S1)

**Rule**: Every chapter, section, subsection, and content-bearing subsubsection must have a lead-in paragraph before any list, figure, table, formula, or child heading.

**Lead-in minimum**: State what will be discussed, why here, connection to previous content, and preview of internal structure.

**Detection**: Script scans `\chapter`, `\section`, `\subsection`, `\subsubsection`, `\paragraph` — flags if first child is non-prose content.

### Chapter Intro Specialization (承上启下)

S1 只判断"有没有导语"。对正文各章（第 2 章至结论前、且含下级小节）的**章引言**，脚本另做承上启下专项检查（`% 章引言 ... [Script]`），与 S1 互补：

- **承上缺失 / 启下缺失**（Major/P1）：章引言未承接前章（无章节号/桥接），或未交代本章问题与各节安排。
- **相对指代**（Minor/P2）：出现"上一章/上文"，建议改用章节号"第 X 章"。
- **篇幅过简 / 过长**（Minor/P2）：偏离"1~2 段、约 300~500 字"的约定。

绪论（第 1 章）由 `_check_introduction_funnel` 负责，章引言检查按标题显式排除，零重叠。改写指导见 [`../writing/thesis-writing-guide.md`](../writing/thesis-writing-guide.md) 的"正文章引言"一节。

## Literature Review Quality (A1-A4)

| Check | Rule | Detection |
|-------|------|-----------|
| A1: Topic clustering | Organize by theme, not author/year listing | Script: regex for 3+ consecutive "Author(Year) proposed..." |
| A2: Critical analysis | Each topic group needs evaluative commentary | LLM judgment required |
| A3: Gap derivation | Last paragraph must identify research gap | Script: keyword scan in final 10 lines |
| A4: Funnel citation density | Citations should narrow from broad to specific | LLM judgment required |

## Cross-Section Closure (C3)

**Rule**: Contribution claims in introduction must be echoed in conclusion.

**Detection**: Script extracts contribution keywords from `introduction`, checks for response keywords ("验证了", "证明了", "实验表明") in `conclusion`. Missing echo → Major/P1.

## Intro Mainline Checks (`--intro-mainline`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --intro-mainline
```

绪论主线四项专项检查，全部 `[Script]` 启发式，仅在传入该 flag 时运行（默认行为不变）：

| Check | Rule | Severity |
|-------|------|----------|
| L-SCI | 科学问题（表格“科学问题”列或枚举条目）不得是短名词短语，须含对象-问题-方法三要素 | Major/P1 |
| L-MAP | 科学问题/研究内容/创新点条数应闭合；正文声明不等量（如“工程验证贡献，不与……等量”）则降级 Info | Major/P1 |
| L-FUN | 绪论首段须完成 领域背景 -> 技术瓶颈 -> 本文 三层漏斗 | Minor/P2 |
| L-DOM | 标题写“国内外研究现状”就必须分述国内/国外，或声明按主题混排 | Info/P3 |

改写模板与判别表见 [`../writing/introduction-guide-zh.md`](../writing/introduction-guide-zh.md)。

## Process Chapter Mainline Checks (`--process-chapter`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --process-chapter
```

过程分析章（工业/过程背景第二章"工艺分析 + 全文方法框架"章式）主线专项检查，全部
`[Script]` 启发式，仅在传入该 flag 时运行（默认行为不变）。默认扫描第 2 章，`--section` 可覆盖目标章。

**章式预判（双信号）**：目标章的章/节标题须同时命中①过程信号（工艺/流程/过程分析/变量分析）
与②框架信号（总体框架/技术框架/研究方案/总体方案/方案框架）才套用 P-\* 检查；否则只输出一条
Info（"若为方法+实验章式请走方法章规则"），不强套过程分析章检查（方法章常见的"问题描述/
总体框架"节名不再单独触发）。

| Check | Rule | Severity |
|-------|------|----------|
| P-FLOW | 工艺/过程分析节内无 `\ref{fig:...}` 流程图引用（工艺章无流程图） | Major/P1 |
| P-DERIVE | 难点/问题节缺工艺特性词 → Major；有特性词但无因果连接（导致/使得/难以/造成…）→ Minor | Major/P1 或 Minor/P2 |
| P-FRAME | 框架节无框架图引用，或未覆盖 ≥2 个方法模块名/后续章指向（框架空泛）；"第 X 章"显式章号映射缺失仅 Info（推荐加强项，5/5 范文框架节均不写章号、章号映射惯例放绪论组织结构节，不写亦合规） | Major/P1（缺图/空泛）；Info/P3（缺章号映射） |
| P-ORDER | 框架节先于难点/问题节出现（违顺序不变式） | Minor/P2 |

写作规范与正反例见 [`../writing/process-chapter-guide-zh.md`](../writing/process-chapter-guide-zh.md)。

## Method Narrative Checks (`--method-narrative`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --method-narrative --section 〈章名〉
```

当方法章包含多个核心模块，或需要审阅模块动机、输入输出、公式解释和相邻接口时运行本分支。
`--section` 每次必须显式选择一个章；缺失时脚本只列候选章并以退出码 2 结束，不自动判断方法章。
解释 finding 或改写正文前，读取
[`../writing/method-description-guide-zh.md`](../writing/method-description-guide-zh.md)，以其中的六角色、
逐边接口和证据分级为完整语义契约。

| Check | Script lane | Severity |
| --- | --- | --- |
| M-HEADING | 标出可能以标题报幕替代模块衔接的位置 | Minor/P2 |
| M-SEQWORD | 标出只表达排版顺序、尚未说明技术关系的小节首句 | Info/P3 |
| M-EQUATION | 标出编号公式后可能缺少符号释义入口的位置 | Minor/P2 |
| M-EDGETABLE | 输出小节清单和逐边接口表骨架；由 LLM 填写，不是 finding | 不计 |

三项 finding 都是 `[Script]` 候选且 `Meaning-Check: NEEDS-LLM`。脚本不判断模块动机、设计理由、
完整输入输出、非直接依赖、证据强度或最终闭合；这些项目按方法描述指南逐模块复核。

## Paragraph Arc Checks (`--paragraph-arc`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --paragraph-arc [--section introduction]
```

该附加分支检查 `P-ARC-LEAD`、`P-ARC-CLOSE`、`P-ARC-LINK` 和 `P-ARC-FLAT`。单项默认
Info/P3；只有绪论/相关工作中连续 3 个合格段同时缺少 LEAD+CLOSE 时追加一条 Minor/P2
汇总。标题导语、列表、受保护环境边界和专用章节豁免；LINK 只比较同一 prose segment 的
原始相邻段。

所有 finding 为 `[Script]` 观察并含 `Meaning-Check: NEEDS-LLM`，不输出改写文本。判据表、
阈值边界、段落范式及与 AXES 的关系见
[`../writing/paragraph-arc-zh.md`](../writing/paragraph-arc-zh.md)。

## Subsection Context Checks (`--subsection-context`)

```bash
uv run python -B scripts/analyze_logic.py thesis.tex --subsection-context [--subsection 2.1.1]
uv run python -B scripts/analyze_logic.py thesis.tex --emit-window --subsection 2.1.1
```

该附加分支把 `depth == 3` 的标题作为 `x.x.x` 小节单元，观察 `S-CTX-IN`、
`S-CTX-OUT` 与 `S-CTX-ROLE` 三类跨标题接口。没有 depth-3 标题时不回退到 depth-2。
正文经 `\include` / `\input` 拆分时先装配，再把窗口坐标映射回真实源文件。

窗口只输出 `current`、`prev.tail`、`next.head`、必要时的 `parent_lead` 及源行号，不复制正文；
只有 `current` 可改，其余部件只作证据。完整判据、合格段规则和协议见
[`../writing/subsection-context-zh.md`](../writing/subsection-context-zh.md)，词表见
[`../writing/subsection-context-terms.yaml`](../writing/subsection-context-terms.yaml)。

## Body-Chapter Stitching & Intro Bridging (default)

- **P-PAPER（默认全章，无需 flag）**：可见正文出现"源论文/小论文/N 篇论文"表述即报（Minor/P2），
  **逐处报告**不截断——这是盲审最直接的拼接铁证，建议改"核心问题/研究内容/本章"。
- **缺承上分级**：第 3 章起章引言缺承接时，若章内其余部分出现"第 X 章"依赖线索（复用前章
  产出）→ 维持 Major；纯并列章 → 降 Info（并列方法章可不承上，5 篇范文核实）。推荐承接
  写法（角色复用句）见 [`../writing/method-chapter-guide-zh.md`](../writing/method-chapter-guide-zh.md)。
- **`--first-chapter N`**：单章文件运行时声明文件内首个 `\chapter` 的真实章号，使承上启下
  检查按真实章序生效（缺省时单章文件被视为第一正文章，承上检查静默）。跨章检查（承上启下、
  章间主线、P-PAPER 全文覆盖）**建议在装配 document.tex 上运行**。

## Thesis Writing Mainline

When the user asks how to rewrite 绪论、方法章节、工程应用/系统实现章、实验讨论、总结与展望, map the section to:

```text
研究背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文方法/章节工作 -> 实验证据 -> 贡献闭合 -> 局限与展望
```

Return paragraph roles and evidence status. Do not invent citations, experiments, or contribution claims.

For an engineering-application chapter, use the existing `logic` route and the engineering guide to map
`research artifact -> operational constraint -> design goal/system property -> evidenced mechanism -> validation evidence`.
Chapter numbers and words such as “平台” are not sufficient classifiers: inspect the body before routing. Do not
run method-chapter `--per-chapter` checks on the whole engineering chapter. Add the existing
`experiment --results-analysis` route only when the user requests it or the chapter contains a quantitative results
subsection that needs analysis. Missing APIs, formulas, metrics, deployment facts, or usability evidence remain
`missing evidence`; no new script or checker is implied by this guidance.

## Transition Signals

| Relation | Chinese | English |
|----------|---------|---------|
| Addition | 此外、进一步 | furthermore, moreover |
| Contrast | 然而、但是 | however, nevertheless |
| Causation | 因此、由此可见 | therefore, consequently |
| Sequence | 首先、随后 | first, subsequently |

> Full details: see [`../writing/logic-coherence.md`](../writing/logic-coherence.md)


## examples/logic-and-experiment.md

# 示例：主线逻辑与实验章节联查

用户请求：
请先检查这篇学位论文从绪论到结论的主线是不是闭合，再看看实验章节是不是更像项目汇报而不是论文讨论。

推荐模块顺序：
1. `logic`
2. `experiment`

命令：
```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex
uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex
```

说明：`analyze_logic.py` 全文档模式默认包含绪论漏斗、章节主线与 C3 绪论-结论闭合检查；
只关注单章时可加 `--section 绪论`（中文章节名与英文键均可）。

预期输出：
- 先指出绪论、贡献来源、结论之间是否错位。
- 再指出实验章节是否缺少比较、机制解释、限制讨论和未来工作。
- 两类问题分模块回报，不混成泛泛的“表达优化”。

## 用逆向提纲复核已有段落

以下为合成材料，演示人工核读，不是新增脚本输出格式。用户只要求检查时，给可定位的诊断
和处置蓝图，不改正文，也不自动移动段落。

章目标：第2章比较时序重建方法的输入假设，并推导本文问题。当前小节为 `2.1.2`。

```text
chapters/review.tex:18 [prev.tail]
下节比较上述方法对输入完整性的要求。

chapters/review.tex:24 [current]
现有时序重建方法对输入完整性的假设不同。固定采样方法要求等间隔观测，掩码建模方法显式接收缺失位置\cite{regular,masked,survey}。两类输入条件划定了本章比较的范围。

chapters/review.tex:29 [current]
方法B在数据集D上的准确率为95%，证明其在所有缺失条件下都能重建真实动态。

chapters/review.tex:33 [current]
本文界面提供深色配色和菜单折叠选项，见\ref{fig:ui}。

chapters/review.tex:38 [next.head]
本节据此分析不规则观测下的输入定义。
```

先从原段提取主题，核对“段主题→章目标”；再核对“证据→段主题”，最后决定是否需要处置：

| 源位置 | 段主题与章目标 | 可见证据及边界 | 处置与理由 |
| --- | --- | --- | --- |
| `chapters/review.tex:24` | 输入完整性假设直接服务本章比较目标 | 两类假设形成比较，综合引用保留；具体文献归因仍需核对原文 | 保留（Info/P3 [LLM]）：段内关系已成立，即使没有显式过渡词也不补“因此”；不将主题综合拆成逐篇罗列 |
| `chapters/review.tex:29` | 性能观察尚未解释输入假设差异 | 数据集D的95%仅支持当前观察，不能证明所有缺失条件或重建机制 | 收窄（Major/P1 [LLM]）：保留原数值和数据集范围，指出比较协议与机制证据缺口，不补结论 |
| `chapters/review.tex:33` | 界面偏好与本章输入假设目标没有已说明的联系 | 仅给出界面描述和图引用 | 移位提案（Minor/P2 [LLM]）：核实工程章是否需要后再考虑移动；本次不执行、不编造衔接关系 |

可按需结合[段落弧线](../references/writing/paragraph-arc-zh.md)的 `P-ARC` 观察和
[小节上下文](../references/writing/subsection-context-zh.md)的 `S-CTX` 窗口定位，形态提示
不能代替上面的语义核读。只有用户明确要求改写时才对 `current` 给出提案；`prev.tail`、
`next.head` 和 `parent_lead` 仅作证据。引用、标签、公式、术语、数字、确定性与范围都要保真，
不得因改写增添因果、实验或作者意图；移出 `current` 的操作需另有对应范围的授权。


# Additional public rules

## 七、按五级证据阶梯限制解释强度

方法章按主张类型选证据时使用
[`method-description-guide-zh.md`](method-description-guide-zh.md#六按证据强度陈述收益) 的
四级表；结果章按已有证据决定可写内容时使用下方五级阶梯。前者回答“这类主张需要什么证据”，
后者回答“当前证据允许写到哪一级”。措辞选择另见
[`over-claim-guard.md`](over-claim-guard.md)，不在本指南复制其词表和替换表。

| 证据等级 | 可写内容 | 推荐谓词 |
| --- | --- | --- |
| 图表事实 | 当前测试块直接观察到的数值与形态 | “为”“低于”“集中在” |
| 结构事实 | 公式或算法直接定义的输入与计算 | “使用”“保留”“调节”“回退” |
| 一致性解释 | 结果形态与结构机制相互对应 | “与……一致”“与……相符”“支持……的关联” |
| 组件贡献 | 同一框架中的受控组件变化 | “去除后……变化”“该记录支持……” |
| 因果归因 | 严格受控、预算一致且能够排除替代解释 | “由……带来”“主要归因于” |

四级主张表到五级证据阶梯的映射如下：

| 方法章四级主张 | 结果章五级落点 | 使用方式 |
| --- | --- | --- |
| 定义事实 | 结构事实 | 用公式或算法定义说明实际输入、处理和输出 |
| 机制级作用 | 结构事实 -> 一致性解释 | 先写结构事实；有对应结果形态时再写一致性解释 |
| 经验性能 | 图表事实 + 组件贡献 | 先报告图表事实；受控组件记录可支持组件贡献 |
| 因果归因 | 因果归因 | 仅在区分性设计排除替代解释时使用 |

从结果章五级证据阶梯回看方法章主张时，使用反向映射：

| 结果章五级证据 | 可回接的方法章主张 | 不得外推 |
| --- | --- | --- |
| 图表事实 | 经验性能的观察部分 | 不能单独证明机制级作用或因果归因 |
| 结构事实 | 定义事实；机制级作用的定义部分 | 不能单独证明经验性能 |
| 一致性解释 | 经降级的机制级作用 | 不能写成组件贡献 |
| 组件贡献 | 有受控记录的经验性能 | 不能自动排除全部替代机制 |
| 因果归因 | 有区分性证据的因果主张 | 不能外推到未测试数据块或协议 |

完整模型之间的排名通常只支持一致性解释。因果谓词附近没有组件证据时，应降级或标记机制
尚未确定。`RA-CAUSAL` 只检查“单句因果谓词与窗口内组件证据线索”的词面组合；“多机制堆叠、
逐项无证据、末句统一撤回”的防御性推测解释仍由 [`experiment.md`](../modules/experiment.md)
中的 B3 按 `[LLM]` 组合判据处理，不得用单词或 hedge 数量替代证据映射。

依据：用户规范 §5.6、§6；外部来源 #1、#9、#10。


# 路由规则详解（latex-thesis-zh）

SKILL.md 的「路由规则」节给出串行顺序与指针；本文件保留完整判据。

## 总则

- 先根据用户问题自动推断模块，不把“你想用哪个模块”当成默认追问。
- 如果一个请求同时包含 2-3 个兼容目标，按固定顺序串行执行，而不是只做第一个：`template` -> `compile` -> `format` -> `structure` / `consistency` -> `bibliography` / `references` -> `logic` / `literature` -> `experiment` / `title` / `deai` / `tables` / `abstract`。
- 对同一段文字做多轮润色时，按“论证/逻辑 -> 句子结构 -> 词汇/排版”由粗到细处理，顺序不可颠倒；详见 `references/writing/writing-philosophy-zh.md`。
- 某个脚本失败时，先返回精确命令、退出码和关键报错，再给出最小下一步，不要静默切换到别的模块掩盖失败。

# User requests and inputs

```latex
% 合成输入；各场景独立，不代表真实论文结果或学校规范。

% 场景 1
% 请求：请把这句话润色得准确、清楚，给出可替换的句子。
% 材料：没有其他结果记录。
该方法可能有助于提升预测性能。

% 场景 2
% 请求：请按 AXES 检查并改写这段结果分析。
% 材料：仅有本段数值，没有比较基线或组件试验。
注意力模型在测试集 T 上的准确率为95\%。这一提升源于模型捕获长程依赖的能力。结果见\ref{tab:single}。

% 场景 3
% 请求：请检查这段消融分析，给出局部改写建议。
% 材料：同一数据划分，完整模型训练100轮，去除模块A的模型训练50轮；其余训练条件未记录。
消融实验中，完整模型的准确率为95\%，去除模块A后为91\%。这证明模块A通过抑制噪声带来性能提升。

% 场景 4
% 请求：请检查结论强度，并给出局部改写建议。
% 材料：同一框架、数据划分、训练预算、优化器与种子集合，仅移除模块A。配对重复记录中，完整模型平均准确率95\%，移除后91\%；未观测中间噪声变量，也没有区分噪声抑制与其他机制的试验。
移除模块A后平均准确率由95\%降至91\%，说明模块A的噪声抑制机制导致了该差异。

% 场景 5
% 请求：请审阅以下结论能否保留，不需要重写已成立的句子。
% 材料：在协议P和测试块T内，以随机受控干预启用或关闭噪声通路N；数据、训练预算及其余模块固定，配对重复结果方向一致。中介测量和恢复通路试验排除了预先列出的容量变化及训练时长解释，支持噪声通路N对该协议下准确率差异的因果作用。
在协议P和测试块T内，准确率差异由噪声通路N的启用带来。通路定义为$z=x+\epsilon$，证据见\ref{tab:intervention}。

% 场景 6
% 请求：请润色这句贡献陈述。
% 材料：作者没有检索相关文献，没有优先权证据；X、Y为给定技术对象。
本文首次将X用于Y。

% 场景 7
% 请求：请检查摘要和章节安排是否适合当前博士论文，只提出诊断，不扩写正文。
% 材料：作者提供的本校要求为摘要1000—1500字、按研究工作编号，可定性陈述理论成果。当前摘要实测1100字，有对象背景与编号的两个工作段。第一项工作给出在假设H下的收敛证明，第二项为在CPU上运行的工程系统，只有离线日志回放证据。全文没有GPU训练或模型超参数搜索，不打算增加实验。
摘要工作段分别陈述假设H下的收敛结论与CPU工程系统的离线日志回放。第3章给出定理及证明，第4章按运行约束、接口机制与回放证据组织。收敛条件为$0<\eta<1$，理论定义见\cite{definition}。

% 场景 8
% 请求：请作一次逆向提纲审阅，定位段主题、章目标、证据与处置；只检查，不改正文。
% 材料：第2章目标是比较时序重建方法的输入假设并推导本文问题。当前窗口为2.1.2；prev.tail和next.head仅供理解衔接。下面给出源位置。
% prev.tail，chapters/review.tex:18
下节比较上述方法对输入完整性的要求。
% current，chapters/review.tex:24
现有时序重建方法对输入完整性的假设不同。固定采样方法要求等间隔观测，掩码建模方法显式接收缺失位置\cite{regular,masked,survey}。两类输入条件划定了本章比较的范围。
% current，chapters/review.tex:29
方法B在数据集D上的准确率为95\%，证明其在所有缺失条件下都能重建真实动态。
% current，chapters/review.tex:33
本文界面提供深色配色和菜单折叠选项，见\ref{fig:ui}。
% next.head，chapters/review.tex:38
本节据此分析不规则观测下的输入定义。
```
