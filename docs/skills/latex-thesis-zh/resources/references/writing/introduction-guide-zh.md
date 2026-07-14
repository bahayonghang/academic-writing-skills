# Dedicated Guide to Writing the Introduction (Chapter 1)

For writing and diagnosing the introduction of a Chinese doctoral/master's degree thesis. Diagnostic entry points:

```bash
uv run python $SKILL_DIR/scripts/analyze_literature.py main.tex --intro-citations --bib refs.bib
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex --intro-mainline
```

> All thresholds here are common criteria from multiple university rules and writing practice, with
> sources noted in each section. **The latest rules of the author's graduate school take precedence**;
> command-line options can override defaults.

## Six-Section Funnel Skeleton and Length Allocation

The introduction should total about 10,000 Chinese characters and no more than 20 pages (expert consensus: “get to the point; 20 pages are enough”).

| Section | Function | Reference Share |
| --- | --- | --- |
| Research background and significance | Domain context -> engineering/theoretical value, ending at “why this is worth doing” | ~15% |
| Domestic and international research status | Thematic review + evolution path + visual synthesis | ~45% |
| Existing problems/key challenges | Derive unresolved problems from review boundaries | ~10% |
| Research contents and innovations | Scientific problem -> research content -> innovation four-way closure | ~20% |
| Research method/technical route (optional by university) | Overall solution and technical-route figure | ~5% |
| Thesis organization | Progressive relationship among chapters, not a mechanical title list | ~5% |

The opening paragraph must complete a three-level funnel: **domain background -> technical bottleneck ->
what this thesis addresses**. Do not begin directly with terminology or system details (script check L-FUN).

## Citation Quota (B1/B4 Defaults and Sources)

| Metric | Default | Source |
| --- | --- | --- |
| Unique introduction citations | 120-160 or more (doctoral level) | Several university rules, including Beijing University of Technology and Harbin Institute of Technology, require >=100 across the thesis; the introduction carries most citations |
| Latest-three-year share | >=30% | Common strict criterion; the broad criterion is latest-five-year share >=1/3 and must include latest-two-year literature |
| Latest-five-year share | >=50% | Same as above |
| Foreign-language share | >=1/2 (whole-thesis scope) | Rules at Beijing University of Technology and others; script does not yet check, review manually |

Literature-selection proportions, used when collaborating with `bib-search-citation`:

- Each thematic cluster = **1-2 foundational works + 2-3 works from the latest three years**, balancing domestic and international sources;
- Discuss multiple works by the same author/team **separately**, comparing method evolution and limitations instead of placing the whole cluster in one `\cite` (script checks B2/B3);
- Prefer primary literature: cite the original work being discussed, not a secondary retelling;
- Textbooks, newspapers, and unpublished reports should generally not support arguments;
- **When citations are insufficient, search only the user's .bib or a real literature database; never fabricate entries.**

## Organization and Visualization of Domestic/International Research Status (B5)

Choose one organization and declare it explicitly:

1. **Separate domestic/international discussion**: foreign then domestic, or the reverse, followed by comparison of differences and connections (general-specific-general);
2. **Thematic mixing**: open with “this section is organized by theme; domestic and international work is compared within each theme” (script check L-DOM: a title containing “domestic and international” must fulfill one of these forms).

Within each thematic cluster, follow `共识 -> 分歧 -> 局限 -> 空白`; end with a comparison/concession/
limitation sentence (literature module A2). Order from distant to close relevance.

**Visual synthesis (at least one; script check B5):**

- **Research-evolution timeline**: time on the horizontal axis, divided into phases such as emergence/development/deepening, with 2-3 representative works and landmark turns per phase;
- **Literature-comparison matrix**: rows = representative works; columns = method route / key assumption / scope / limitation; close with a general-specific-general paragraph after the table;
- Note: **a Gantt chart belongs to proposal scheduling and does not go in the introduction**. Use a research-evolution or technical-route figure when a route must be shown.

Three prohibitions (common review anti-patterns): lecture-style lists of theoretical schools; subjective straw-man criticism of prior work; vague sources or mixing prior work with the author's own work.

## Refining Scientific Problems (L-SCI)

A scientific problem must contain all three elements: **object, problem, method**. Sentence template:

```text
针对〈对象〉的〈现象/瓶颈〉，研究〈科学问题〉，拟采用〈方法路径〉。
```

Decision table:

| Form | Example | Judgment |
| --- | --- | --- |
| Short noun phrase | “多速率状态重叠” | Invalid: only a topic term, with neither object nor method; script match |
| Technical task | “开发一套软测量系统” | Invalid: an engineering task, not a scientific problem |
| Valid problem sentence | “针对多速率异步采样的烧成过程，研究低频质量条件如何调制高频动态特征，拟采用条件特征调制机制” | Valid: object + problem + method, testable |

Requirement: one clear, testable sentence that can guide data collection and verification. Keep one topic and decompose it top-down with a hypothesis tree; do not overreach.

## Four-Way Closure (L-MAP)

**Scientific problem <-> research content <-> innovation <-> chapter arrangement** should map one to one. Recommended practice:

- include a “scientific problem-research content-innovation-corresponding chapter” mapping table in the introduction;
- when counts differ, state the reason in the body, such as “system implementation is an engineering-validation contribution and is not stated as equal to method innovations”; the script then degrades to Info;
- answer every innovation in the conclusion chapter (logic module C3).

## Holistic Writing Order

1. **Theme first**: establish the thesis's single mainline sentence before selecting material; delete content unrelated to the research problem;
2. **Write body first, introduction later**: refine background, status, and significance after gaining a holistic understanding of the research;
3. Organize the review around this thesis's innovations, clearly explaining the “shoulders of predecessors” to position the contribution;
4. Describe progressive chapter relationships (how Chapter N output becomes Chapter N+1 input), not chapter titles one by one.

## Recommended Output Format

```latex
% 绪论引用（chapters/chapter1.tex:55）[Severity: Minor] [Priority: P2]: [Script] B3 前缀“zhao”文献 5 篇，且在第55行整簇共引
% 建议：拆开分述并比较该团队方法的演进与局限；若为不同作者请人工复核后忽略。
```

---

## Further Reading

- [thesis-writing-guide.md](thesis-writing-guide.md): full-thesis mainline, chapter introductions, and chapter summaries.
- [../modules/literature.md](../modules/literature.md): details of A1-A3 and B1-B5 checks.
- [../modules/logic.md](../modules/logic.md): details of L-SCI/L-MAP/L-FUN/L-DOM checks.
