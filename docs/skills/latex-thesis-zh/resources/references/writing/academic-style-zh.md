# Chinese Academic Writing Standards

## Contents

- [1. Correcting Colloquial Expressions](#一口语化表达纠正)
  - [1.1 Replacing Degree Adverbs](#11-程度副词替换)
  - [1.2 Replacing Subjects](#12-主语替换)
  - [1.3 Standardizing Verbs](#13-动词规范化)
- [2. Avoiding Absolute Terms](#二绝对化词汇规避)
  - [2.1 Forbidden Terms](#21-禁用词汇)
  - [2.2 Alternatives](#22-替代表达)
- [3. Logical Connectors](#三逻辑连接词)
  - [3.1 Progression](#31-递进关系)
  - [3.2 Contrast](#32-转折关系)
  - [3.3 Causation](#33-因果关系)
  - [3.4 Examples](#34-举例说明)
- [4. Common Language Errors](#四常见语病)
  - [4.1 Collocation Errors](#41-搭配不当)
  - [4.2 Missing Components](#42-成分残缺)
  - [4.3 Word-Order Errors](#43-语序不当)
- [5. Punctuation Standards](#五标点符号规范)
  - [5.1 Chinese Punctuation](#51-中文标点)
  - [5.2 English Punctuation](#52-英文标点)
  - [5.3 Mixed-Language Rules](#53-混用规则)
  - [5.4 Colons, Semicolons, and Inter-Sentence Logic in Prose](#punctuation-prose)
- [6. Numbers and Units](#六数字与单位)
  - [6.1 Number Usage](#61-数字使用)
  - [6.2 Unit Standards](#62-单位规范)

---

## 1. Correcting Colloquial Expressions

### 1.1 Replacing Degree Adverbs
| Colloquial | Academic |
|------|------|
| 很多 | 大量、众多、若干 |
| 非常 | 极为、显著、相当 |
| 特别 | 尤其、尤为、格外 |
| 一些 | 部分、若干、某些 |
| 很好 | 优异、显著、卓越 |

### 1.2 Replacing Subjects
| Avoid | Use |
|------|------|
| 我们 | 本文、本研究、作者 |
| 我 | Avoid first-person singular when possible |
| 你们 | Must not appear |

### 1.3 Standardizing Verbs
| Colloquial | Academic |
|------|------|
| 用 | 采用、使用、运用、利用 |
| 做 | 进行、开展、实施、执行 |
| 看 | 观察、分析、研究、考察 |
| 想 | 认为、推测、假设、考虑 |
| 试 | 尝试、探索、验证 |

## 2. Avoiding Absolute Terms

### 2.1 Forbidden Terms
- ❌ 显然、毫无疑问、众所周知
- ❌ 必然、绝对、完全、最好、最优
- ❌ 肯定、一定、当然、无疑

### 2.2 Alternatives
| Absolute | Academic |
|--------|--------|
| 显然 | 研究表明、实验结果显示 |
| 毫无疑问 | 可以认为、有理由相信 |
| 众所周知 | 已有研究指出、文献表明 |
| 必然 | 往往、通常、一般而言 |
| 最好 | 较优、更优、具有优势 |

## 3. Logical Connectors

### 3.1 Progression
- 此外、另外、进一步、更为重要的是
- 不仅...而且...、既...又...

### 3.2 Contrast
- 然而、但是、不过、尽管如此
- 与此相反、相比之下

### 3.3 Causation
- 因此、由此可见、综上所述
- 鉴于此、基于上述分析

### 3.4 Examples
- 例如、譬如、以...为例
- 具体而言、特别是

## 4. Common Language Errors

### 4.1 Collocation Errors
| Incorrect | Correct |
|------|------|
| 发挥问题 | 发现问题 |
| 增加效率 | 提高效率 |
| 扩大精度 | 提高精度 |
| 改进缺点 | 改正缺点 |

### 4.2 Missing Components
❌ “通过实验，验证了方法的有效性。” (missing subject)
✅ “通过实验，本文验证了该方法的有效性。”

### 4.3 Word-Order Errors
❌ “该方法不仅提高了效率，而且也降低了成本。”
✅ “该方法不仅降低了成本，而且提高了效率。” (easier point before harder point)

## 5. Punctuation Standards

### 5.1 Chinese Punctuation
- Use Chinese punctuation: ，。！？；：""''（）【】
- End Chinese sentences with the Chinese full stop “。”

### 5.2 English Punctuation
- English punctuation may follow English terms
- Use an English comma in explanations following a formula

### 5.3 Mixed-Language Rules
- Use Chinese punctuation after English words in Chinese context
- Use English punctuation when the entire parenthetical is English

<a id="punctuation-prose"></a>

### 5.4 Colons, Semicolons, and Inter-Sentence Logic in Prose

Continuous Chinese thesis prose should use complete sentences by default. Avoid repeatedly using
colon shells such as “label: content” or “the reason is: conclusion,” and do not chain an entire
paragraph with semicolons as if it were a list. The rewrite should make existing relationships
between propositions explicit instead of mechanically replacing punctuation. When the material
supports only parallel facts, keep them parallel and do not invent causation, progression, or order.

This judgment belongs to the `[LLM]` layer. Process it in this order:

1. Protect data, citations, formulas, terms, qualifiers, and LaTeX commands, then extract the fact or
   claim in each clause.
2. Decide whether explicit evidence in the source supports a causal, progressive, contrastive,
   conditional, or parallel relationship, and check claim strength against
   [over-claim-guard.md](over-claim-guard.md). The mere presence of an experiment, ablation,
   mechanism analysis, or source text does not prove causation. State the propositions in separate
   complete sentences when the relationship is unclear.
3. Remove label shells such as “result:”, “the reason is:”, and “limitation:”. Supply the research
   object, method, or evidence as the subject. Prefer full stops between propositions, then use only
   the connective wording justified by the established relationship.
4. Recheck facts, claim strength, and scope. Do not simply replace colons or semicolons with commas,
   and do not infer AI authorship from these marks alone.

Retain a colon that genuinely introduces or defines material, a semicolon needed between complex
parallel clauses, the abstract overview “主要研究工作如下：”, keyword separators, and punctuation
required by formulas, code, URLs, quotations, citations, or the university template.

| Scenario | Before | After |
|------|--------|--------|
| A component-removal comparison is available | 结果：表 4-2 显示误差下降；原因是：移除校正模块后误差回升；局限：仅完成离线验证。 | 表 4-2 显示误差下降。组件移除对照中，移除校正模块后误差回升，说明该模块与误差改善相关。该结论目前限于离线验证。 |
| Only parallel facts are available | 数据集 A 包含 120 个样本；数据集 B 包含 118 个样本；因此模型 C 更稳定。 | 数据集 A 包含 120 个样本，数据集 B 包含 118 个样本。现有样本数不能证明模型 C 更稳定。 |
| Legitimate introduction and complex parallel clauses | 主要研究工作如下：当输入完整时，系统执行联合估计；当输入缺失时，系统保留上一时刻状态。 | Keep the sentence; the colon introduces content and the semicolon separates conditional clauses that already contain commas. |

## 6. Numbers and Units

### 6.1 Number Usage
- Exact values: Arabic numerals (1, 2, 3)
- Approximate quantities: Chinese characters (几十、数百)
- Ordinals: 第一、第二, not 1st or 2nd

### 6.2 Unit Standards
- International System of Units (SI)
- Put one space between value and unit
- Use upright letters, not italics
