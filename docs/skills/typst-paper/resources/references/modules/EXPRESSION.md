# Module: Academic Expression
**Trigger words**: academic tone, academic expression, improve writing, weak verbs

**Script Usage**:
```bash
uv run python ../scripts/improve_expression.py main.typ
uv run python ../scripts/improve_expression.py main.typ --section methods
```

**English academic expression**:
|weak verb|academic alternative|
|----------|------------|
|use|employ, utilize, leverage|
|get|obtain, achieve, acquire|
|make|construct, develop, generate|
|show|demonstrate, illustrate, indicate|

**Chinese academic expression**:
|colloquial|academic|
|----------|----------|
|Many studies show|A lot of research shows|
|works very well|has significant advantages|
|we use|This article adopts|
|It can be seen|It can be seen that|

**How ​​to use**: The user provides the source code of the paragraph, and the Agent analyzes and returns the polished version and comparison table.

**Output format** (Markdown comparison table):
```markdown
| Original / 原文 | Revised / 改进版本 | Issue Type / 问题类型 | Rationale / 优化理由 |
|-----------------|---------------------|----------------------|---------------------|
| We use machine learning to get better results. | We employ machine learning to achieve superior performance. | Weak verbs | Replace "use" -> "employ", "get" -> "achieve" for academic tone |
```

**Alternative format** (comments in source code):
```typst
// EXPRESSION（第23行）[Severity: Minor] [Priority: P2]: 提升学术语气
// 原文：We use machine learning to get better results.
// 修改后：We employ machine learning to achieve superior performance.
// 理由：用学术替代词替换弱动词
```

Reference: [STYLE_GUIDE.md](../STYLE_GUIDE.md)

