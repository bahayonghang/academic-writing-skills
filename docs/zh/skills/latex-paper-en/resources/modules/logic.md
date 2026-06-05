# Module: Logical Coherence & Methodological Depth

**Trigger**: logic, coherence, 逻辑, methodology, argument structure, 论证

**Purpose**: Ensure logical flow between paragraphs and strengthen methodological rigor in academic writing.

```bash
python scripts/analyze_logic.py main.tex
python scripts/analyze_logic.py main.tex --section methods
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
5. **Justify, don't just describe**: Explain *why*, not just *what*
