# Module: Logical Coherence & Methodological Depth

**Trigger**: logic, coherence, 逻辑, methodology, argument structure, 论证

**Purpose**: Ensure logical flow between paragraphs and strengthen methodological rigor in academic writing.

```bash
uv run python -B scripts/analyze_logic.py main.tex
uv run python -B scripts/analyze_logic.py main.tex --section methods
```

**Focus Areas**:

**1. Paragraph-Level Coherence (AXES Model)**:
| Component | Description | Example |
|-----------|-------------|---------|
| **A**ssertion | Clear topic sentence stating the main claim | "Attention mechanisms improve sequence modeling." |
| **X**ample | Concrete evidence or data supporting the claim | "In our experiments, attention achieved 95% accuracy." |
| **E**xplanation | Analysis of why the evidence supports the claim | "This improvement stems from the ability to capture long-range dependencies." |
| **S**ignificance | Connection to broader argument or next paragraph | "This finding motivates our proposed architecture." |

**2. Transition Signals**:
| Relationship | Signals |
|--------------|---------|
| Addition | furthermore, moreover, in addition, additionally |
| Contrast | however, nevertheless, in contrast, conversely |
| Cause-Effect | therefore, consequently, as a result, thus |
| Sequence | first, subsequently, finally, meanwhile |
| Example | for instance, specifically, in particular |

**3. Methodological Depth Checklist**:

- [ ] Each claim is supported by evidence (data, citation, or logical reasoning)
- [ ] Method choices are justified (why this approach over alternatives?)
- [ ] Limitations are acknowledged explicitly
- [ ] Assumptions are stated clearly
- [ ] Reproducibility details are sufficient (parameters, datasets, metrics)

**4. Common Issues**:
| Issue | Problem | Fix |
|-------|---------|-----|
| Logical gap | Missing connection between paragraphs | Add transition sentence explaining the relationship |
| Unsupported claim | Assertion without evidence | Add citation, data, or reasoning |
| Shallow methodology | "We use X" without justification | Explain why X is appropriate for this problem |
| Hidden assumptions | Implicit prerequisites | State assumptions explicitly |

**Output Format**:

```latex
% LOGIC (Line 45) [Severity: Major] [Priority: P1]: Logical gap between paragraphs
% Issue: Paragraph jumps from problem description to solution without transition
% Current: "The data is noisy. We propose a filtering method."
% Suggested: "The data is noisy, which motivates the need for preprocessing. Therefore, we propose a filtering method."
% Rationale: Add causal transition to connect problem and solution

% METHODOLOGY (Line 78) [Severity: Major] [Priority: P1]: Unsupported method choice
% Issue: Method selection lacks justification
% Current: "We use ResNet as the backbone."
% Suggested: "We use ResNet as the backbone due to its proven effectiveness in feature extraction and skip connections that mitigate gradient vanishing."
% Rationale: Justify architectural choice with technical reasoning
```

**Section-Specific Guidelines**:
| Section | Coherence Focus | Methodology Focus |
|---------|-----------------|-------------------|
| Introduction | Problem → Gap → Contribution flow | Justify research significance |
| Related Work | Group by theme, compare explicitly | Position against prior work |
| Methods | Step-by-step logical progression | Justify every design choice |
| Experiments | Setup → Results → Analysis flow | Explain evaluation metrics |
| Discussion | Findings → Implications → Limitations | Acknowledge boundaries |

**Best Practices** (Based on [Elsevier](https://elsevier.blog/logical-academic-writing/), [Proof-Reading-Service](https://www.proof-reading-service.com/blogs/academic-publishing/a-guide-to-creating-clear-and-well-structured-scholarly-arguments)):

1. **One idea per paragraph**: Each paragraph should have a single, clear focus
2. **Topic sentences first**: Start each paragraph with its main claim
3. **Evidence chain**: Every claim needs support (data, citation, or logic)
4. **Explicit transitions**: Use signal words to show relationships
5. **Justify, don't just describe**: Explain _why_, not just _what_

---

## Literature Review Quality Validation (A1-A4)

These rules ensure the Related Work section synthesizes literature rather than merely cataloguing it.

### A1: Thematic Clustering (Not Author/Year Enumeration)

**Rule**: Related Work should organize references by research theme, not by author or publication year. Detecting 3+ consecutive sentences following an "Author (Year) proposed/introduced..." pattern signals enumeration.

**Detection heuristic** (script-automated):

- Regex: `^(In \d{4}|.*\(\d{4}\).*(?:proposed|introduced|presented|developed|designed))`
- Threshold: 3+ consecutive matching lines → Major/P1

| Pattern                                                                                                                     | Verdict                   |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| "Smith (2019) proposed X. Jones (2020) introduced Y. Lee (2021) designed Z."                                                | Enumeration (flag)        |
| "Attention-based methods have evolved... Smith (2019) and Jones (2020) both explored... However, Lee (2021) showed that..." | Thematic synthesis (pass) |

**Fix**: Reorganize by theme clusters; within each cluster, compare and contrast methods critically.

### A2: Critical Analysis After Each Theme Cluster (LLM-judgment)

**Rule**: Each thematic group must end with a synthesis sentence that compares, contrasts, or evaluates the cited works — not just list them. Look for evaluative language: "however", "despite", "a common limitation", "compared to".

_This rule is too nuanced for regex and requires LLM judgment during review._

### A3: Research Gap Derivation at End of Related Work

**Rule**: The final paragraph of Related Work must contain explicit research gap language that motivates the current study.

**Detection heuristic** (script-automated):

- Scan last 10 lines of the `related` section
- Keywords: `gap|limitation|however.*(?:no|not|few)|remains|lack|overlooked|under-explored|open problem|yet to be|inadequate|insufficient`
- If no match → Major/P1

| Pattern                                                               | Verdict            |
| --------------------------------------------------------------------- | ------------------ |
| "Despite these advances, existing methods remain unable to handle X." | Gap present (pass) |
| "Lee (2021) achieved 95% accuracy on benchmark Y." (section ends)     | No gap (flag)      |

### A4: Funnel-Shaped Citation Density (LLM-judgment)

**Rule**: Citation density should follow a broad→focused→specific funnel: start with the general field, narrow to the sub-problem, end with the most relevant prior work. A flat or inverted funnel suggests poor narrative structure.

_This rule requires LLM judgment to assess the narrative arc._

---

## Cross-Section Logic Chain Closure (C3)

**Rule**: Contribution claims made in the Introduction must be explicitly answered in the Conclusion. If the Introduction states "we propose X" or "our contributions include Y", the Conclusion must contain corresponding answer language ("we have shown", "results demonstrate", "experiments confirm").

**Detection heuristic** (script-automated, `--cross-section` flag):

- Extract contribution keywords from `introduction` section
- Extract answer keywords from `conclusion` section
- If intro has claims but conclusion has zero answer language → Major/P1 (flagged as `[Script]` observation)

| Intro Claim                               | Expected Conclusion Answer                                        |
| ----------------------------------------- | ----------------------------------------------------------------- |
| "We propose a novel attention mechanism." | "We have shown that the proposed attention mechanism achieves..." |
| "Our main contributions are: (1)..."      | "Experiments confirm that contribution (1)..."                    |

**Note**: This check is inherently heuristic. Findings are framed as observations, not definitive judgments. False positives are possible when the conclusion uses different phrasing to address the same claims.

---

## Motivation Red-Thread Closure (opt-in: `--motivation-thread`)

**Rule**: A strong paper is one problem→solution arc. Every promise the Introduction makes ("we propose X to do Y") should be _tested_ in the Results/Experiments and _resolved_ in the Discussion/Conclusion. This diagnostic surfaces broken threads.

**How to run** (additive — normal logic output is unchanged when the flag is absent):

```bash
uv run python -B scripts/analyze_logic.py main.tex --motivation-thread
```

**What it produces** (read-only, all findings tagged `[Script]`):

- **Promise Map** — each Introduction promise (`CONTRIBUTION_KEYWORDS` match) → the best-overlapping Results/Experiment line. `[NO EVIDENCE FOUND]` flags a promise the experiments never test.
- **Closure Map** — each Introduction claim → the best-overlapping Discussion/Conclusion line. `[UNCLOSED]` flags a claim the paper never resolves.
- **Evidence-without-promise** — Results lines carrying numeric findings that trace back to no Introduction promise (possible scope creep).

**Mechanism**: keyword + content-token overlap (English words ≥4 chars plus CJK bigrams). It is intentionally a navigation aid, **not** a verdict — the report explicitly says false positives are possible and asks the reader to verify. When a promise looks unmatched only because the Results reuse different wording, treat it as a prompt to add an explicit echo, not a hard error.

| Pattern                                                                                   | Verdict                      |
| ----------------------------------------------------------------------------------------- | ---------------------------- |
| Intro "we propose a latency-reducing sparse attention" → Results "reduces latency by 42%" | matched (pass)               |
| Intro promises interpretability, no Results subsection mentions it                        | `[NO EVIDENCE FOUND]` (flag) |
| Intro claim never echoed in Discussion/Conclusion                                         | `[UNCLOSED]` (flag)          |
