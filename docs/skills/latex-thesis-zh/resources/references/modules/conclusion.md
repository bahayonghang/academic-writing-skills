# Module: Conclusion

**Trigger**: 结论, 总结与展望, 结论与展望, 展望, 结论章, conclusion, 结论检查, conclusion check

## Commands

```bash
uv run python -B scripts/analyze_conclusion.py main.tex
uv run python -B scripts/analyze_conclusion.py main.tex --json
```

For a multi-file project, pass the `main.tex` entry point. The script assembles `\input`/`\include`
files and locates the conclusion chapter (结论/结论与展望/总结与展望). Conclusion-to-Chinese-abstract
comparison reuses the extracted abstract text.

## Details

Perform **in-chapter content-structure diagnosis plus conclusion-abstract comparison** on the
conclusion chapter. The 13 CC-* checks are detailed in the checker mapping and severity notes in
`../writing/conclusion-guide-zh.md`:

- **Three-part structure (CC-TRIAD)**: summary body + innovation statement + outlook must all be present. Missing outlook/summary -> Error; missing innovation statement -> Warning.
- **Opening inheritance (CC-OPEN)**, **numbered contributions (CC-ENUM)**, and **contribution skeleton (CC-SKELETON)**: opening ordinal phrases connect the research chain; list 3-4 contributions as (1)(2)(3); each follows the “for... propose... results show...” skeleton.
- **Outlook (CC-OUTLOOK-EMPTY/TRANS/COUNT)**: empty-phrase blacklist + limitation-to-outlook transition + 2-3 items.
- **Conclusion is not the abstract (CC-VERBATIM)**: sentence-level difflib comparison; verbatim repetition ratio >=30% -> Warning.
- **Numeric consistency (CC-QUANT)**: every number in the conclusion must be found in the body; missing numbers produce a soft NEEDS-LLM prompt.
- **Prohibitions (CC-NO-FIG / CC-NEW-CONCEPT)**: do not introduce new figures/tables in the conclusion (Error) or new concepts ([LLM]).
- **Style Info (CC-RATIO / CC-SUBSEC)**: summary-to-outlook length ratio and subsection/chapter numbering style are informational only, not judged right or wrong.

### Lane Separation

- `[Script]`: CC-TRIAD/OPEN/ENUM/OUTLOOK-*/VERBATIM/QUANT/NO-FIG/RATIO/SUBSEC are script-determined and output `% CONCLUSION (源文件:L##) [Severity] [Priority] [Script]: CC-码 说明`.
- `[LLM]`: CC-SKELETON (semantic completeness of the contribution skeleton) and CC-NEW-CONCEPT (new-concept detection) use the LLM lane. The script provides only prompts/coarse counts for agent judgment.

### Boundaries with Other Modules (Do Not Duplicate Reports)

- **`\cite`, maximum length (<=2000), vague wording** -> use `spec-check` (`check_spec.py`). This script's footer routes there and does not repeat hard conclusion-format rules.
- **Over-claiming** (“first/fully solves/comprehensively outperforms”) -> use the `../writing/over-claim-guard.md` workflow.
- **English-abstract tense/AI tone** -> use the `deai` module.

Skill-layer response:

1. Return findings as `% CONCLUSION (L##) [Severity] [Priority]`, separating “check results” from “rewrite suggestions.”
2. For Errors (missing outlook/summary or figures/tables in the conclusion), give structural repair suggestions first.
3. For CC-OUTLOOK-EMPTY empty phrases, provide a rewrite example with a concrete technical direction.
4. Never fabricate results or add contributions not in the original text; leave `\cite`/`\ref`/`\label`/math environments unchanged by default.

See also: [../writing/conclusion-guide-zh.md](../writing/conclusion-guide-zh.md), the dedicated
conclusion-chapter writing guide with structural templates, positive/negative examples, and the checker mapping.
