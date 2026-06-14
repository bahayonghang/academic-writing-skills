# Design: latex-thesis-zh Heading Structure Optimization

## Architecture Boundary

Keep this as an enhancement to the existing `latex-thesis-zh` skill. Do not create a new skill and do not add a new public module unless the implementation proves the existing module split cannot support the behavior.

Primary ownership:

- `SKILL.md`: route user wording like "大标题/小标题/章标题/小节标题/目录标题" to the correct module sequence.
- `references/writing/title-optimization.md`: body chapter title rules, including object-problem-method.
- `references/writing/structure-guide.md`: direct-section budget and section consolidation guidance.
- `references/writing/thesis-writing-guide.md`: connect title architecture with chapter mainline.
- `scripts/optimize_title.py`: deterministic heading architecture diagnostics.
- `tests/`: executable contract.
- `docs/skills/...` and `docs/zh/skills/...`: mirrored user-facing references.

## Proposed Runtime Flow

When the user asks about chapter/section titles:

1. Run or recommend `structure` first if the paper entry file is known:
   - `uv run python $SKILL_DIR/scripts/map_structure.py main.tex`
2. Run `title` heading architecture check:
   - Proposed command: `uv run python $SKILL_DIR/scripts/optimize_title.py main.tex --check --headings`
3. If the user also mentions "衔接/导语/主线/逻辑", run `logic`:
   - `uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex`
4. Return a two-part report:
   - Diagnostics: source location, severity, triggered rule.
   - Suggestions: rename/merge plan that preserves LaTeX source objects.

## Deterministic Heading Diagnostics

Implementation should reuse existing parser infrastructure:

- Assemble multi-file projects with `tex_loader.assemble`.
- Extract headings with `parsers.get_parser(...).extract_headings`.
- Locate diagnostics with source-aware line references when possible.

Checks:

1. Direct section count
   - For each level-1 body chapter, count immediate level-2 headings before the next level-1 heading.
   - If count > 5, output a structure warning.
   - Suggested merge guidance:
     - "基础理论 + 问题描述"
     - "模型框架 + 模型建模"
     - "实验设置 + 结果分析"
     - Move detailed modules under `\subsection`.

2. Chapter title facets
   - Exempt conventional titles:
     - 摘要, 绪论, 引言, 相关工作, 文献综述, 结论, 总结与展望, 参考文献, 致谢, 附录
   - For substantive body chapters, detect whether title plausibly contains:
     - Object/domain facet.
     - Problem/task facet.
     - Method/path facet.
   - Missing facets should be a suggestion, not an automatic rewrite.

3. Child title anchoring
   - Immediate sections under a substantive chapter should either:
     - play a recognized thesis role, such as 引言/基础理论/问题描述/模型/算法/框架/实验/应用/本章小结; or
     - share salient tokens with the parent chapter title; or
     - include a role that clearly advances the parent title.
   - Generic headings like "总体框架", "实验分析", "结果讨论" are acceptable only when surrounding chapter facets make their role clear; otherwise recommend a title that reuses the parent object/problem.

## Output Contract

Use LaTeX-friendly review comments, for example:

```latex
% TITLE-ARCH (chapters/method.tex:1) [Severity: Major] [Priority: P1]: 章标题缺少对象-问题-方法中的“对象”
% 当前：基于图神经网络的优化算法
% 建议：将研究对象前置，例如“水泥粉磨过程运行优化的图神经网络算法”
% 保留：不修改 \label、\ref、\cite 或数学环境。
```

For section count:

```latex
% TITLE-ARCH (chapters/chapter2.tex:1) [Severity: Major] [Priority: P1]: 直属小节过多
% 当前：7 个 \section，建议压缩到最多 5 个。
% 合并建议：将“数据预处理”和“优化问题”并入“问题描述与建模基础”，将细分模型放入 \subsection。
```

## Compatibility Notes

- Do not break the existing `optimize_title.py main.tex --check` behavior.
- If a new `--headings` flag is added, update script help, router docs, tests, and smoke tests together.
- Keep public module inventory stable unless a new module is justified.
- Keep docs mirrors synchronized:
  - `docs/skills/latex-thesis-zh/resources/...`
  - `docs/zh/skills/latex-thesis-zh/resources/...`

## Trade-Offs

- Heuristic diagnostics will not perfectly judge title quality. Treat facet detection as "needs review" style feedback, not a hard academic truth.
- A strict "every chapter title must have all three facets" would overflag 绪论/文献综述/结论. Exempt conventional chapters.
- A strict lexical overlap rule for child titles would overflag good generic roles like "引言" and "本章小结". Use a recognized-role whitelist plus token anchoring.

## Rollback Shape

The change should be easy to revert because it is localized to:

- `latex-thesis-zh` reference/docs files
- `optimize_title.py` if script support is added
- tests and eval files

No generated outputs should be committed except intended eval/review artifacts if the repository convention accepts them.
