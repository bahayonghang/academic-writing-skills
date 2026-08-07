# Module: De-AI editing
**Trigger words**: deai, de-AI, humanize, reduce AI traces, reduce AI traces

**Goal**: Reduce AI writing artifacts while maintaining Typst’s grammatical and technical accuracy.

**Input requirements**:
1. **Source code type** (required): Typst
2. **Chapter** (required): Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion
3. **Source code snippet** (required): Paste directly (retain original indentation and line breaks)

**Workflow**:

**1. Grammar structure recognition**
Detect Typst syntax and keep it intact:
- Function call:`#set`, `#show`, `#let`
- Quote:`@cite`, `@ref`, `@label`
- math:`$...$`, `$ ... $`(block level)
- mark:`*bold*`, `_italic_`, `` `code` ``
- Custom function (default unchanged)

**2. AI Trace Detection**:
|type|Example|question|
|------|------|------|
|Empty slogans|significant, comprehensive, effective|lack of specificity|
|overdetermined|obviously, necessarily, completely|too absolute|
|Mechanical ratio|three paragraphs without substance|lacks depth|
|template expression|in recent years, more and more|cliche|
|structural shell|not A but B, not merely A but B|No description of comparison axes, baselines, and evidence|
|Pseudo Insight/Lecture Notes|The real question, essentially, The conclusion is:|Use cue words to replace judgments supported by evidence|
|temporal signal|shows/presents (methods/experiments/results chapter)|Use past tense narration instead|
|overstatement|caused by, for the first time, universally|Causal/first/universal transgression|

See [TENSE_GUIDE.md](../TENSE_GUIDE.md) and [OVER_CLAIM_GUARD.md](../OVER_CLAIM_GUARD.md)。

**Academic Humanity Contract**:
Protect four types of content first, and then reduce the AI ​​flavor:
- **Facts/Evidence**: data, experimental setup, charts, indicators,`@cite`、`<label>`, mathematics and macros;
- **Claim/Position**: The true conclusion of the paper, method selection, uncertainties and limitations;
- **Logic**: paragraph role, chapter role, claim-evidence mapping;
- **Boundaries**: Applicable conditions, assumptions, lack of evidence, and `待补证`.

The default output is diagnostics, risk summaries, or rewrite blueprints. Only when the user explicitly requests to rewrite the text, a prose proposal will be given; no promise should be made to lower the score of a certain detection platform.

Listing several specific mechanisms and then declaring that the current data cannot verify them is a defensive speculative explanation that requires `[LLM]` judgment. State the observation first and bind each retained mechanism to visible evidence or a discriminating test. If none is supported, state that the mechanism remains undetermined and move testable alternatives to future work. Do not delete the caveat or strengthen the inference merely to sound certain.

The script's `hedge` / `hedge_application` suggestions remain valid for overconfident wording and undemonstrated applications. `results suggest`, `may / could`, and `可能/或许` reduce the strength of a single claim; they do not replace per-mechanism evidence.

**3. Text rewriting** (only visible text is changed):
- Split long sentences (English >50 words, Chinese >50 words)
- Adjust word order to match natural expression
- Replace general statements with specific claims
- Remove redundant phrases
- Add necessary subjects (do not introduce new facts)

**4. Output generation**:
```typst
// ============================================================
// 去AI化编辑（第23行 - Introduction）
// ============================================================
// 原文：This method achieves significant performance improvement.
// 修改后：The proposed method improves performance in the experiments.
//
// 改动说明：
// 1. 删除空话："significant" -> 删除
// 2. 保留原有主张，避免新增具体指标
//
// ⚠️ 【待补证：需要实验数据支撑，补充具体指标】
// ============================================================

= Introduction
The proposed method improves performance in the experiments...
```

**Hard constraints**:
- **Never modify**:`@cite`, `@ref`, `@label`, mathematical environment
- **Never new**: Facts, data, conclusions, indicators, experimental settings, citation numbers
- **Modify only**: ordinary paragraph text, title text

**Chapter Guidelines**:
|chapter|focus|constraint|
|------|------|------|
|Abstract|Purpose/method/key results (with numbers)/conclusion|No general contributions|
|Introduction|Importance->Blank->Contribution (verifiable)|restrain words|
|Related Work|Grouping by route, differences made concrete|Specific comparison|
|Methods|Reproducibility is preferred (process, parameter, indicator definition)|Implementation details|
|Results|Report only facts and figures|No explanation|
|Discussion|Talk about mechanisms, boundaries, failures, and limitations|critical analysis|
|Conclusion|Answer research questions without introducing new experiments|Executable future work|

Reference: [DEAI_GUIDE.md](../DEAI_GUIDE.md)

## Grading mode (`--tier`) and D1-D5 dimensions

`--tier {light|medium|heavy}` is an **optional switch**. When not passed, the output is exactly the same as the original; when passed in:

- **Scale Threshold**:`light`Report less (relax the cap),`heavy`Pay more (tighten the cap),`medium`Keep existing thresholds;
- **Enable D1 sentence length check**: Mark chapters with too low sentence length variation coefficient (mechanically even rhythm), Chinese and English bilingual;
- **Annotate AIGC dimensions for each conclusion** D1-D5 and attach a teaching note (why the detector marked this pattern).

```bash
uv run python scripts/deai_check.py main.typ --analyze --tier heavy
```

Five dimensions are oriented toward readability and are **not targeted at any specific detection platform**: D1 sentence length variation, D2 paragraph structure, D3 information density, D4 connective word frequency, and D5 term-context matching. Threshold (including`sentence_length.cv_threshold`) can still pass`references/AI_TONE_THRESHOLDS.yaml`cover.
