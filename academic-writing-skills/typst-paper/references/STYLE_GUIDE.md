# Academic Writing Style Guide (Typst)

## Core Principles

### 1. Clarity Over Complexity
- One idea per sentence
- Avoid nested clauses when possible
- Define terms on first use

### 2. Precision Over Vagueness
- Use specific numbers instead of "several" or "many"
- Quantify claims whenever possible
- Avoid hedging without evidence

### 3. Active Voice (When Appropriate)
- ✅ "We propose a novel method..."
- ✅ "This paper presents..."
- ❌ "A novel method is proposed by us..."

## Sentence Length Guidelines

| Type | Word Count | Use Case |
|------|------------|----------|
| Short | 10-15 | Key findings, transitions |
| Medium | 15-25 | Most content |
| Long | 25-40 | Complex relationships |
| Very Long | >40 | ⚠️ Consider splitting |

## Paragraph Structure

### Topic Sentence
First sentence states the main point.

### Supporting Sentences
- Evidence, examples, or elaboration
- 3-5 sentences typical
- Clear logical flow

### Transition
Connect to next paragraph if needed.

## Academic Vocabulary

### Reporting Verbs (Neutral)
- states, notes, observes, reports, describes

### Reporting Verbs (Strong Agreement)
- demonstrates, shows, proves, confirms, establishes

### Reporting Verbs (Tentative)
- suggests, implies, indicates, proposes, hypothesizes

### Reporting Verbs (Critical)
- claims, argues, asserts, alleges, maintains

## Transition Words

### Addition
- Furthermore, Moreover, Additionally, In addition

### Contrast
- However, Nevertheless, Conversely, On the other hand

### Cause/Effect
- Therefore, Consequently, As a result, Thus

### Example
- For instance, For example, Specifically, In particular

### Sequence
- First, Second, Subsequently, Finally

## Citation Integration (Typst Syntax)

### Integral (Author as Subject)
```typst
@smith2020 demonstrated that...
According to @jones2021, the method...
```

### Non-Integral (Content Focus)
```typst
Deep learning has shown remarkable success @smith2020 @jones2021 @wang2022.
```

### Paraphrase (Preferred)
Restate the idea in your own words with citation.

### Direct Quote (Sparingly)
Only for definitions or exceptionally well-phrased ideas.

## Common Section Patterns

### Introduction
1. General context → Specific problem
2. Gap in existing work
3. Contributions of this work
4. Paper organization

### Related Work
1. Categorize existing approaches
2. Compare and contrast
3. Position your work

### Methodology
1. Overview of approach
2. Detailed steps
3. Justification for choices

### Results
1. Experimental setup
2. Quantitative results
3. Qualitative analysis
4. Comparison with baselines

### Conclusion
1. Summary of contributions
2. Limitations
3. Future work

## Typst-Specific Formatting

### Headings
```typst
= Introduction          // Level 1
== Background          // Level 2
=== Related Work       // Level 3
```

### Emphasis
```typst
*bold text*            // Bold
_italic text_          // Italic
`code text`            // Code/monospace
```

### Lists
```typst
// Unordered list
- Item 1
- Item 2
  - Nested item

// Ordered list
+ First item
+ Second item
  + Nested item
```

### Math
```typst
// Inline math
The equation $x^2 + y^2 = z^2$ shows...

// Display math
$ x^2 + y^2 = z^2 $

// Numbered equation
$ x = (a + b) / 2 $ <eq:mean>
```

### Figures and Tables
```typst
// Figure
#figure(
  image("figure.png", width: 80%),
  caption: [Description of the figure.]
) <fig:example>

// Table
#figure(
  table(
    columns: 3,
    [Header 1], [Header 2], [Header 3],
    [Data 1], [Data 2], [Data 3],
  ),
  caption: [Description of the table.]
) <tab:example>
```

### Cross-references
```typst
As shown in @fig:example, the method...
Table @tab:example presents the results...
Equation @eq:mean defines the average...
```
